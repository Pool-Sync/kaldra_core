from dataclasses import dataclass
from typing import Any, Optional

import numpy as np
import torch

from src.archetypes.delta144_engine import Delta144Engine
from src.kindras.kindra_cultural_mod import KaldraKindraCulturalMod
from src.tw369.oracle_tw_painleve import TWPainleveOracle, TWConfig, TWStats
from src.core.epistemic_limiter import EpistemicLimiter, EpistemicDecision
from src.core.kaldra_logger import KALDRALogger, make_default_logger
from src.core.audit_trail import AuditTrail

@dataclass
class KaldraSignal:
    """Sinal final do KALDRA Master Engine."""
    archetype_probs: np.ndarray
    tw_trigger: bool
    tw_stats: Optional[TWStats]
    epistemic: EpistemicDecision
    delta_state: Optional[Any] = None  # Dict with archetype+state from Delta144

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
        self.tau_layer = EpistemicLimiter(tau=tau)
        self.tw_oracle = TWPainleveOracle(config=tw_config or TWConfig())
        self.d_ctx = d_ctx
        self.tau = tau
        self.logger = logger if logger is not None else make_default_logger()
        self.audit_trail = audit_trail

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
            status = getattr(epistemic, "status", None)
            summary["epistemic_status"] = status

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
        tw_window: Optional[np.ndarray] = None,
    ) -> KaldraSignal:
        """
        Realiza a inferência completa.
        
        embedding: vetor de contexto (d_ctx)
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
        # 1) Δ144 — get base archetype distribution
        # Usa o método infer_from_vector que adicionamos ao Delta144Engine
        result = self.delta.infer_from_vector(embedding)
        
        # Se result.probs for None (caso antigo), cria uniforme
        if result.probs is None:
            base_probs = np.ones(144) / 144.0
        else:
            base_probs = np.asarray(result.probs, dtype=float)

        # 2) Kindra modulation (usa torch internamente)
        ctx = torch.tensor(embedding, dtype=torch.float32).unsqueeze(0)
        probs_t = torch.tensor(base_probs, dtype=torch.float32).unsqueeze(0)
        
        # Aplica modulação cultural
        modulated = self.kindra_mod(probs_t, ctx, apply_softmax=True)[0]
        modulated_np = modulated.detach().cpu().numpy()

        # 3) TW oracle (se janela fornecida)
        tw_trigger = False
        tw_stats = None
        if tw_window is not None:
            tw_trigger, tw_stats = self.tw_oracle.detect(tw_window)

        # 4) τ layer (Epistemic Limiter)
        epistemic = self.tau_layer.from_probs(modulated_np)

        signal = KaldraSignal(
            archetype_probs=modulated_np,
            tw_trigger=tw_trigger,
            tw_stats=tw_stats,
            epistemic=epistemic,
            delta_state=result.to_dict(),  # Include Delta144 state snapshot
        )
        
        # Log inference end
        self._log_inference_end(request_id=request_id, signal=signal)
        
        return signal
