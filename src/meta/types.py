"""
Shared types for Meta Engines (v3.1).
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from src.unification.states.unified_state import KindraContext
from src.tw369.tw369_integration import TWState

@dataclass
class MetaInput:
    """
    Standard input for meta-engine analysis (v3.1).
    
    Attributes:
        text: Input text to analyze
        delta144_state: Optional current Δ144 state identifier
        archetype_scores: Optional archetype distribution scores
        kindra: Optional KindraContext with 3×48 vectors
        tw_state: Optional TWState for drift/regime awareness
        bias_score: Optional bias detection score
        polarity_scores: Optional polarity scores
        modifiers: Optional adjustment modifiers
    """
    text: str
    delta144_state: Optional[str] = None
    archetype_scores: Dict[str, float] = field(default_factory=dict)
    kindra: Optional[KindraContext] = None
    tw_state: Optional[TWState] = None
    bias_score: Optional[float] = None
    polarity_scores: Optional[Dict[str, float]] = None
    modifiers: Optional[Dict[str, float]] = None
