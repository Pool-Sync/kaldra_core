"""
Safeguard Engine.

Main entry point for the Safeguard system.
"""
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
from .safeguard_risk_model import SafeguardRiskModel
from .safeguard_policy import SafeguardPolicy
from ..tau.tau_state import TauState
from src.core.hardening.retries import with_retries
from src.core.hardening.circuit_breaker import circuit_breaker
from src.core.hardening.fallbacks import safe_fallback
from src.core.hardening.timeouts import with_timeout

@dataclass
class SafeguardSignal:
    """Output signal from the Safeguard Engine."""
    bias: Dict[str, Any]
    polarity_risk: Dict[str, float]
    drift_risk: Dict[str, float]
    journey_risk: Dict[str, float]
    meta_risk: Dict[str, float]
    final_risk: str  # "LOW", "MID", "HIGH", "CRITICAL"
    risk_score: float  # 0.0 - 1.0
    mitigation_actions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class SafeguardEngine:
    """
    The KALDRA Safeguard Engine.
    Evaluates system state for narrative and semantic risks.
    """
    
    def __init__(self):
        self.risk_model = SafeguardRiskModel()
        self.policy = SafeguardPolicy()
        
    @circuit_breaker(name="safeguard_evaluate", fail_threshold=5, reset_time=30)
    @with_retries(max_attempts=2, backoff=0.5)
    @with_timeout(seconds=5)
    def evaluate(
        self,
        tau_state: TauState,
        drift_state: Dict[str, Any],
        polarities: Dict[str, float],
        meta: Dict[str, Any],
        journey_state: Any = None # StorySignal or similar
    ) -> SafeguardSignal:
        """
        Evaluate the complete system state for risks.
        """
        # 1. Extract Risk Features
        
        # Bias (from Tau details or passed separately, here assuming we can get it)
        # For now, placeholder extraction
        bias_score = 0.0 
        if tau_state.details and "features" in tau_state.details:
            bias_score = tau_state.details["features"].get("bias_score", 0.0)
            
        # Polarity Risk (e.g., extreme polarization)
        polarity_risk_score = 0.0
        if polarities:
            # Simple heuristic: avg deviation from 0.5
            deviations = [abs(v - 0.5) * 2 for v in polarities.values()]
            if deviations:
                polarity_risk_score = sum(deviations) / len(deviations)
                
        # Drift Risk
        drift_risk_score = 0.0
        if drift_state:
            # High velocity or acceleration is risky
            drift_risk_score = min(1.0, abs(drift_state.get("velocity", 0.0)) * 2.0)
            
        # Meta Risk (e.g., Nihilism)
        meta_risk_score = 0.0
        if meta and "nietzsche" in meta:
            # Example: Active Nihilism
            meta_risk_score = meta["nietzsche"].get("scores", {}).get("active_nihilism", 0.0)
            
        # Journey Risk (e.g., stuck in Abyss)
        journey_risk_score = 0.0
        # Placeholder
        
        # 2. Calculate Risk
        score, components = self.risk_model.evaluate_risk(
            bias_score=bias_score,
            polarity_risk=polarity_risk_score,
            drift_risk=drift_risk_score,
            journey_risk=journey_risk_score,
            meta_risk=meta_risk_score
        )
        
        # 3. Classify and Resolve Policy
        final_risk = self.risk_model.classify_risk(score)
        actions = self.policy.resolve_actions(final_risk, components)
        
        return SafeguardSignal(
            bias={"score": bias_score},
            polarity_risk={"score": polarity_risk_score},
            drift_risk={"score": drift_risk_score},
            journey_risk={"score": journey_risk_score},
            meta_risk={"score": meta_risk_score},
            final_risk=final_risk,
            risk_score=score,
            mitigation_actions=actions
        )
