"""
Tau State Definition.

Defines the data structure for the Tau Layer's epistemic state.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class TauState:
    """
    Represents the epistemic reliability state of the system.
    
    Attributes:
        tau_score: Float [0.0, 1.0] representing confidence/safety.
                   1.0 = High Confidence/Safety
                   0.0 = Critical Uncertainty/Risk
        tau_risk: Classification of risk level ("LOW", "MID", "HIGH", "CRITICAL").
        tau_modifiers: Dictionary of damping factors and adjustments.
                       e.g., {"drift_damping": 0.5, "archetype_suppression": 0.2}
        tau_actions: List of actions taken by the Tau Policy.
                     e.g., ["CLAMP_DRIFT", "FLAG_UNCERTAINTY"]
        details: Additional context about risk factors.
    """
    tau_score: float
    tau_risk: str
    tau_modifiers: Dict[str, float] = field(default_factory=dict)
    tau_actions: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "tau_score": self.tau_score,
            "tau_risk": self.tau_risk,
            "tau_modifiers": self.tau_modifiers,
            "tau_actions": self.tau_actions,
            "details": self.details
        }
