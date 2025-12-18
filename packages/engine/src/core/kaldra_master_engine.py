from dataclasses import dataclass
from typing import Any, Optional
import json
import os

import numpy as np
import torch

from src.archetypes.delta144_engine import Delta144Engine
from src.kindras.kindra_cultural_mod import KaldraKindraCulturalMod
from src.tw369.oracle_tw_painleve import TWPainleveOracle, TWConfig, TWStats
from src.tw369.tw369_integration import TW369Integrator
from src.common.types import TWState
from src.tau.tau_layer import TauLayer
from src.tau.tau_state import TauState
from src.safeguard.safeguard_engine import SafeguardEngine, SafeguardSignal
from src.core.kaldra_logger import KALDRALogger, make_default_logger
from src.core.audit_trail import AuditTrail
from src.archetypes.polarity_mapping import extract_polarity_scores
from src.config import KALDRA_TW_POLARITY_ENABLED, KALDRA_DELTA12_POLARITY_ENABLED
from src.meta.nietzsche import analyze_meta as analyze_nietzsche
from src.meta.aurelius import analyze_meta as analyze_aurelius
from src.meta.campbell import CampbellEngine
from src.archetypes.delta12_vector import Delta12Vector
from src.core.hardening.fallbacks import safe_fallback
from src.core.hardening.timeouts import with_timeout
from src.execution.execution.parallel_executor import ParallelExecutor, TaskStatus

@dataclass
class KaldraSignal:
    """Sinal final do KALDRA Master Engine."""
    archetype_probs: np.ndarray
    tw_trigger: bool
    tw_stats: Optional[TWStats]
    # epistemic: EpistemicDecision  <-- Replaced by TauState
    tau: Optional[Any] = None # TauState dict
    safeguard: Optional[Any] = None # SafeguardSignal dict
    risk_summary: str = "LOW"
    delta_state: Optional[Any] = None  # Dict with archetype+state from Delta144
    polarity_scores: Optional[Any] = None  # Dict[str, float] (v2.7)
    degraded: bool = False # v2.9 Hardening flag

class KaldraMasterEngineV2:
    """
    Orquestrador mínimo do KALDRA v2.0:
    - recebe texto ou vetor de contexto
    - roda Δ144 (Base)
    - aplica Kindra 3×48 (Modulação Cultural)
    - passa pelo oracle TW (Detecção de Anomalia)
    - aplica τ / EpistemicLimiter (Segurança Epistêmica)
    """

    def __init__(
        self,
        delta_engine: Optional[Delta144Engine] = None,
        d_ctx: int = 256,
        tau: float = 0.65,
        tw_config: Optional[TWConfig] = None,
        logger: Optional[KALDRALogger] = None,
        audit_trail: Optional[AuditTrail] = None,
    ):
        self.delta = delta_engine or Delta144Engine.from_default_files(d_ctx=d_ctx)
        self.kindra_mod = KaldraKindraCulturalMod(d_ctx=d_ctx)
        
        # v2.8: The Guardian Layer
        self.tau_layer = TauLayer()
        self.safeguard_engine = SafeguardEngine()
        self.tw_integrator = TW369Integrator() # For drift calculation
        
        self.tw_oracle = TWPainleveOracle(config=tw_config or TWConfig())
        self.d_ctx = d_ctx
        self.tau = tau
        self.logger = logger if logger is not None else make_default_logger()
        self.audit_trail = audit_trail
        
        # v3.5: Parallel Execution Engine
        self._load_parallel_config()
    
    def _load_parallel_config(self) -> None:
        """Load parallel execution configuration from file."""
        config_path = "configs/execution/parallel.config.json"
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
            else:
                # Default configuration
                config = {
                    "parallel_mode": True,
                    "max_workers": 6,
                    "timeout_ms": 85,
                    "task_timeouts": {}
                }
            
            self.parallel_enabled = config.get("parallel_mode", True)
            self.parallel_executor = ParallelExecutor(
                max_workers=config.get("max_workers", 6),
                default_timeout_ms=config.get("timeout_ms", 85),
                enabled=self.parallel_enabled
            )
            self.task_timeouts = config.get("task_timeouts", {})
            
            if self.logger:
                self.logger.log_event("parallel_config_loaded", {
                    "enabled": self.parallel_enabled,
                    "max_workers": config.get("max_workers", 6)
                })
        
        except Exception as e:
            if self.logger:
                self.logger.log_event("parallel_config_error", {"error": str(e)})
            # Fallback: disable parallel execution
            self.parallel_enabled = False
            self.parallel_executor = ParallelExecutor(enabled=False)
            self.task_timeouts = {}

    def _log_inference_start(self, request_id: str, embedding_shape: Any, has_tw_window: bool) -> None:
        """Log the start of an inference request."""
        if not hasattr(self, "logger") or self.logger is None:
            return
        self.logger.log_event(
            "inference_start",
            {
                "request_id": request_id,
                "embedding_shape": str(embedding_shape),
                "has_tw_window": has_tw_window,
                "d_ctx": self.d_ctx,
                "tau": self.tau,
            },
        )

    def _log_inference_end(self, request_id: str, signal: "KaldraSignal") -> None:
        """Log the end of an inference request with summary."""
        if not hasattr(self, "logger") or self.logger is None:
            return

        # Extract signal attributes safely
        probs = getattr(signal, "archetype_probs", None)
        epistemic = getattr(signal, "epistemic", None)
        tw_trigger = getattr(signal, "tw_trigger", None)
        delta_state = getattr(signal, "delta_state", None)

        summary: dict = {}

        if probs is not None:
            try:
                max_prob = float(probs.max())
                max_idx = int(probs.argmax())
                summary["max_prob"] = max_prob
                summary["max_index"] = max_idx
            except Exception:
                pass

        if epistemic is not None:
            # Legacy support
            status = getattr(epistemic, "status", None)
            summary["epistemic_status"] = status
            
        tau = getattr(signal, "tau", None)
        if tau is not None:
            summary["tau_score"] = tau.get("tau_score")
            summary["tau_risk"] = tau.get("tau_risk")
            
        safeguard = getattr(signal, "safeguard", None)
        if safeguard is not None:
            summary["safeguard_risk"] = safeguard.get("final_risk")

        if tw_trigger is not None:
            summary["tw_trigger"] = bool(tw_trigger)

        if delta_state is not None:
            summary["has_delta_state"] = True

        self.logger.log_event(
            "inference_end",
            {
                "request_id": request_id,
                "summary": summary,
            },
        )

        # Audit trail (if configured)
        if hasattr(self, "audit_trail") and self.audit_trail is not None:
            try:
                self.audit_trail.record_inference(
                    request_id=request_id,
                    context={
                        "d_ctx": self.d_ctx,
                        "tau": self.tau,
                    },
                    summary=summary,
                )
            except Exception:
                # Audit trail never breaks the flow
                pass

    def infer_from_embedding(
        self,
        embedding: np.ndarray,
        text: Optional[str] = None,
        tw_window: Optional[np.ndarray] = None,
    ) -> KaldraSignal:
        """
        Realiza a inferência completa (v2.8 Guardian Layer Enabled).
        
        embedding: vetor de contexto (d_ctx)
        text: texto original (opcional, para meta-análise)
        tw_window: janela opcional de sinais para o oracle TW (T, m)
        """
        # Generate request ID and log start
        import uuid
        request_id = uuid.uuid4().hex
        embedding_shape = getattr(embedding, "shape", None)
        has_tw_window = tw_window is not None
        
        self._log_inference_start(
            request_id=request_id,
            embedding_shape=embedding_shape,
            has_tw_window=has_tw_window,
        )
        
        # --- GLOBAL HARDENING WRAPPER ---
        degraded_mode = False
        try:
            # --- PHASE 1: PRE-ANALYSIS (Meta & Polarity) ---
            polarity_scores = {}
            meta_results = {}
            if text:
                try:
                    nietzsche_res = analyze_nietzsche(text)
                    aurelius_res = analyze_aurelius(text)
                    meta_results = {
                        "nietzsche": nietzsche_res.to_dict(),
                        "aurelius": aurelius_res.to_dict()
                    }
                    polarity_scores = extract_polarity_scores(meta_results)
                except Exception as e:
                    if self.logger:
                        self.logger.log_event("meta_analysis_error", {"error": str(e)})
                    # Non-critical failure, continue degraded
                    degraded_mode = True

            # --- PHASE 2: TAU INPUT PHASE ---
            # Calculate initial epistemic state
            # For now, bias is placeholder or derived from polarity
            bias_placeholder = {"score": 0.0} 
            modifier_scores_placeholder = {} # Will be inferred by Delta144, but we need them for Tau? 
            # Actually Tau uses them to MODULATE Delta144.
            # Let's infer modifier scores from embedding first if possible, or let Delta144 do it.
            # Delta144 has `infer_modifier_scores_from_embedding`.
            try:
                modifier_scores = self.delta.infer_modifier_scores_from_embedding(embedding)
            except Exception:
                modifier_scores = {}
                degraded_mode = True
            
            try:
                tau_input = self.tau_layer.compute_tau_input_phase(
                    bias_result=bias_placeholder,
                    polarity_scores=polarity_scores,
                    modifier_scores=modifier_scores
                )
                tau_modifiers = tau_input.tau_modifiers
            except Exception as e:
                if self.logger:
                    self.logger.log_event("tau_input_error", {"error": str(e)})
                # Fallback Tau State
                tau_modifiers = {}
                tau_input = TauState(tau_score=0.5, tau_risk="MID", tau_modifiers={}, tau_actions=[])
                degraded_mode = True
            
            # --- PHASE 3: CORE INFERENCE (Parallel Execution) ---
            
            if self.parallel_enabled:
                # Parallel execution mode
                try:
                    # Define parallel tasks
                    tasks = {
                        'delta144': lambda: self.delta.infer_from_vector(embedding, tau_modifiers=tau_modifiers),
                        'kindra': lambda: self._run_kindra_modulation(embedding, base_probs=np.ones(144) / 144.0),
                        'tw369': lambda: self._run_tw369_drift(tau_modifiers),
                        'polarities': lambda: polarity_scores  # Already computed, just return
                    }
                    
                    # Execute in parallel
                    results = self.parallel_executor.run_parallel(
                        tasks=tasks,
                        task_timeouts=self.task_timeouts
                    )
                    
                    # Extract results
                    if results['delta144'].status == TaskStatus.COMPLETED:
                        result = results['delta144'].result
                        base_probs = np.asarray(result.probs if result.probs is not None else [1.0/144]*144, dtype=float)
                    else:
                        if self.logger:
                            self.logger.log_event("delta_parallel_error", {"error": results['delta144'].error})
                        from src.archetypes.delta144_engine import DeltaState
                        result = DeltaState(probs=[1.0/144]*144, dominant_id="A01_INNOCENT", confidence=0.0)
                        base_probs = np.ones(144) / 144.0
                        degraded_mode = True
                    
                    if results['kindra'].status == TaskStatus.COMPLETED:
                        modulated_np = results['kindra'].result
                    else:
                        if self.logger:
                            self.logger.log_event("kindra_parallel_error", {"error": results['kindra'].error})
                        modulated_np = base_probs
                        degraded_mode = True
                    
                    if results['tw369'].status == TaskStatus.COMPLETED:
                        drift_state = results['tw369'].result
                        driftvalues = drift_state.get("values", {})
                    else:
                        if self.logger:
                            self.logger.log_event("tw369_parallel_error", {"error": results['tw369'].error})
                        drift_state = {"velocity": 0.0, "values": {}}
                        degraded_mode = True
                    
                except Exception as e:
                    if self.logger:
                        self.logger.log_event("parallel_execution_error", {"error": str(e)})
                    # Fallback to sequential
                    degraded_mode = True
                    result, modulated_np, drift_state = self._run_sequential_core(
                        embedding, tau_modifiers, degraded_mode
                    )
                    if result.probs is None:
                        base_probs = np.ones(144) / 144.0
                    else:
                        base_probs = np.asarray(result.probs, dtype=float)
            
            else:
                # Sequential execution mode (fallback)
                result, modulated_np, drift_state = self._run_sequential_core(
                    embedding, tau_modifiers, degraded_mode
                )
                if result.probs is None:
                    base_probs = np.ones(144) / 144.0
                else:
                    base_probs = np.asarray(result.probs, dtype=float)

            # 3) TW Oracle (still sequential as it depends on tw_window)
            tw_trigger = False
            tw_stats = None
            
            try:
                if tw_window is not None:
                    tw_trigger, tw_stats = self.tw_oracle.detect(tw_window)
            except Exception as e:
                if self.logger:
                    self.logger.log_event("tw_oracle_error", {"error": str(e)})
                degraded_mode = True

            # --- PHASE 4: TAU OUTPUT PHASE ---
            try:
                tau_output = self.tau_layer.compute_tau_output_phase(
                    story_state=None, # No story engine in this minimal loop
                    drift_state=drift_state,
                    meta_scores=meta_results
                )
            except Exception as e:
                if self.logger:
                    self.logger.log_event("tau_output_error", {"error": str(e)})
                tau_output = TauState(tau_score=0.5, tau_risk="MID", tau_modifiers={}, tau_actions=[])
                degraded_mode = True
            
            # --- PHASE 5: SAFEGUARD ENGINE ---
            try:
                safeguard_signal = self.safeguard_engine.evaluate(
                    tau_state=tau_output,
                    drift_state=drift_state,
                    polarities=polarity_scores,
                    meta=meta_results,
                    journey_state=None
                )
            except Exception as e:
                if self.logger:
                    self.logger.log_event("safeguard_error", {"error": str(e)})
                # Fail Safe: Assume High Risk if Safeguard fails
                safeguard_signal = SafeguardSignal(
                    bias={}, polarity_risk={}, drift_risk={}, journey_risk={}, meta_risk={},
                    final_risk="HIGH", risk_score=0.8, mitigation_actions=["FLAG_RISK"]
                )
                degraded_mode = True

            signal = KaldraSignal(
                archetype_probs=modulated_np,
                tw_trigger=tw_trigger,
                tw_stats=tw_stats,
                tau=tau_output.to_dict(),
                safeguard=safeguard_signal.to_dict(),
                risk_summary=safeguard_signal.final_risk,
                delta_state=result.to_dict(),
                polarity_scores=polarity_scores,
                degraded=degraded_mode
            )
            
            # Log inference end
            self._log_inference_end(request_id=request_id, signal=signal)
            
            return signal

        except Exception as e:
            # CATASTROPHIC FAILURE FALLBACK
            if self.logger:
                self.logger.log_event("catastrophic_inference_failure", {"error": str(e)})
            
            # Return a minimal valid signal
            fallback_probs = np.ones(144) / 144.0
            return KaldraSignal(
                archetype_probs=fallback_probs,
                tw_trigger=False,
                tw_stats=None,
                risk_summary="CRITICAL_FAILURE",
                degraded=True
            )
    
    def _run_kindra_modulation(self, embedding: np.ndarray, base_probs: np.ndarray) -> np.ndarray:
        """Run Kindra modulation (helper for parallel execution)."""
        try:
            ctx = torch.tensor(embedding, dtype=torch.float32).unsqueeze(0)
            probs_t = torch.tensor(base_probs, dtype=torch.float32).unsqueeze(0)
            
            # Apply cultural modulation
            modulated = self.kindra_mod(probs_t, ctx, apply_softmax=True)[0]
            return modulated.detach().cpu().numpy()
        except Exception:
            return base_probs
    
    def _run_tw369_drift(self, tau_modifiers: dict) -> dict:
        """Run TW369 drift calculation (helper for parallel execution)."""
        try:
            tw_state = self.tw_integrator.create_state()
            drift_values = self.tw_integrator.compute_drift(tw_state, tau_modifiers=tau_modifiers)
            return {"velocity": sum(drift_values.values()), "values": drift_values}
        except Exception:
            return {"velocity": 0.0, "values": {}}
    
    def _run_sequential_core(self, embedding: np.ndarray, tau_modifiers: dict, degraded_mode: bool) -> tuple:
        """
        Run core modules sequentially (fallback mode).
        
        Returns:
            Tuple of (result, modulated_np, drift_state)
        """
        # 1) Δ144
        try:
            result = self.delta.infer_from_vector(embedding, tau_modifiers=tau_modifiers)
        except Exception as e:
            if self.logger:
                self.logger.log_event("delta_inference_error", {"error": str(e)})
            from src.archetypes.delta144_engine import DeltaState
            result = DeltaState(probs=[1.0/144]*144, dominant_id="A01_INNOCENT", confidence=0.0)
            degraded_mode = True
        
        if result.probs is None:
            base_probs = np.ones(144) / 144.0
        else:
            base_probs = np.asarray(result.probs, dtype=float)
        
        # 2) Kindra modulation
        try:
            ctx = torch.tensor(embedding, dtype=torch.float32).unsqueeze(0)
            probs_t = torch.tensor(base_probs, dtype=torch.float32).unsqueeze(0)
            modulated = self.kindra_mod(probs_t, ctx, apply_softmax=True)[0]
            modulated_np = modulated.detach().cpu().numpy()
        except Exception as e:
            if self.logger:
                self.logger.log_event("kindra_mod_error", {"error": str(e)})
            modulated_np = base_probs
            degraded_mode = True
        
        # 3) TW369 Drift
        try:
            tw_state = self.tw_integrator.create_state()
            drift_values = self.tw_integrator.compute_drift(tw_state, tau_modifiers=tau_modifiers)
            drift_state = {"velocity": sum(drift_values.values()), "values": drift_values}
        except Exception as e:
            if self.logger:
                self.logger.log_event("tw369_error", {"error": str(e)})
            drift_state = {"velocity": 0.0, "values": {}}
            degraded_mode = True
        
        return result, modulated_np, drift_state
