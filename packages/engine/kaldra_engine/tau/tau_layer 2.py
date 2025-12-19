"""
Tau Layer (Epistemic Limiter v2).

Main entry point for the Tau Layer.
"""
from typing import Dict, Any, Optional
from .tau_state import TauState
from .tau_risk_model import TauRiskModel
from .tau_policy import TauPolicy
from src.core.hardening.retries import with_retries
from src.core.hardening.circuit_breaker import circuit_breaker
from src.core.hardening.fallbacks import safe_fallback
from src.core.hardening.timeouts import with_timeout

class TauLayer:
    """
    The Guardian Layer's epistemic control unit.
    Calculates reliability scores and enforces safety policies.
    """
    
    def __init__(self):
        self.risk_model = TauRiskModel()
        self.policy = TauPolicy()
        
    @circuit_breaker(name="tau_input_phase", fail_threshold=5, reset_time=30)
    @with_retries(max_attempts=2, backoff=0.5)
    @with_timeout(seconds=5)
    def compute_tau_input_phase(
        self,
        bias_result: Dict[str, Any],
        polarity_scores: Dict[str, float],
        modifier_scores: Dict[str, float]
    ) -> TauState:
        """
        Calculate Tau State at the Input Phase (before core processing).
        
        Args:
            bias_result: Output from Bias Engine.
            polarity_scores: Extracted polarity scores.
            modifier_scores: Inferred modifier scores.
            
        Returns:
            TauState: Initial epistemic state.
        """
        # 1. Extract features
        features = {}
        
        # Bias
        features["bias_score"] = bias_result.get("score", 0.0)
        
        # Polarity Extremity (avg distance from 0.5)
        if polarity_scores:
            extremity = sum(abs(v - 0.5) for v in polarity_scores.values()) / len(polarity_scores)
            # Normalize: max possible avg distance is 0.5. Map 0.0-0.5 to 0.0-1.0
            features["polarity_extremity"] = min(1.0, extremity * 2.0)
        else:
            features["polarity_extremity"] = 0.0
            
        # 2. Calculate Score
        score = self.risk_model.calculate_score(features)
        
        # 3. Determine Policy
        risk_level = self.risk_model.classify_risk(score)
        modifiers, actions = self.policy.resolve_policy(risk_level)
        
        return TauState(
            tau_score=score,
            tau_risk=risk_level,
            tau_modifiers=modifiers,
            tau_actions=actions,
            details={"phase": "input", "features": features}
        )

    @circuit_breaker(name="tau_output_phase", fail_threshold=5, reset_time=30)
    @with_retries(max_attempts=2, backoff=0.5)
    @with_timeout(seconds=5)
    def compute_tau_output_phase(
        self,
        story_state: Any, # StorySignal or dict
        drift_state: Dict[str, Any],
        meta_scores: Dict[str, Any]
    ) -> TauState:
        """
        Calculate Tau State at the Output Phase (after core processing).
        
        Args:
            story_state: Output from Story Engine.
            drift_state: Current drift state.
            meta_scores: Meta-engine outputs.
            
        Returns:
            TauState: Final epistemic state.
        """
        # 1. Extract features
        features = {}
        
        # TW Severity
        if drift_state:
             # Assuming drift_state has 'severity' or similar, or we use metadata
             features["tw_severity"] = drift_state.get("severity", 0.0)
             # Drift Instability (e.g., high velocity)
             features["drift_instability"] = min(1.0, abs(drift_state.get("velocity", 0.0)))
        
        # Narrative Instability (from Story Engine)
        if hasattr(story_state, "drift_trajectory"):
             traj = story_state.drift_trajectory
             if traj:
                 # Handle both dict and object access
                 volatility = 0.0
                 if isinstance(traj, dict):
                     volatility = traj.get("drift_volatility", 0.0)
                 elif hasattr(traj, "drift_volatility"):
                     volatility = getattr(traj, "drift_volatility", 0.0)
                     
                 features["drift_instability"] = max(features.get("drift_instability", 0.0), volatility)
        
        # Meta Inversions (placeholder logic)
        # Real logic would check for specific pathological meta-states
        features["meta_inversions"] = 0.0 # TODO: Implement meta-inversion detection
        
        # 2. Calculate Score
        score = self.risk_model.calculate_score(features)
        
        # 3. Determine Policy
        risk_level = self.risk_model.classify_risk(score)
        modifiers, actions = self.policy.resolve_policy(risk_level)
        
        return TauState(
            tau_score=score,
            tau_risk=risk_level,
            tau_modifiers=modifiers,
            tau_actions=actions,
            details={"phase": "output", "features": features}
        )
