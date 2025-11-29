"""
Meta-Engine Base Interface for KALDRA v2.5.

Defines the common interface for meta-analysis engines (Nietzsche, Campbell, Aurelius).
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Protocol


@dataclass
class MetaSignal:
    """
    Output signal from a meta-engine analysis.
    
    Attributes:
        name: Engine name ("nietzsche", "campbell", "aurelius")
        score: Confidence/strength of the signal [0.0, 1.0]
        label: Primary classification label
        details: Additional context and metadata
    """
    name: str
    score: float
    label: str
    details: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate score is in [0, 1]."""
        self.score = max(0.0, min(1.0, self.score))


class MetaEngineBase:
    """
    Abstract base class for meta-analysis engines.
    
    Meta-engines analyze the complete KALDRA signal (Δ12, Δ144, TWState, Bias, etc.)
    and produce high-level interpretations for routing and decision-making.
    """
    
    name: str = "base"
    
    def run(self, signal: Dict[str, Any]) -> MetaSignal:
        """
        Execute meta-analysis on a complete KALDRA signal.
        
        Args:
            signal: Complete KALDRA signal containing:
                - delta12: Delta12Vector (archetype distribution)
                - delta144: StateInferenceResult (state + archetype)
                - tw_state: TWState (plane values, drift)
                - bias_score: float (bias detection score)
                - drift_history: List[DriftState] (recent drift states)
                - metadata: Dict (additional context)
                
        Returns:
            MetaSignal with analysis results
            
        Raises:
            Should not raise - must be fail-safe and return valid MetaSignal
        """
        raise NotImplementedError(f"{self.__class__.__name__}.run() not implemented")
