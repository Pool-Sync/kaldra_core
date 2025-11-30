"""
Unified Signal Definitions for KALDRA Core.
Contains signal objects for various engines (Meta, Safeguard, Story).
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
import uuid
import time

# ---------------------------------------------------------------------------
# Meta Signal (from Meta Engines)
# ---------------------------------------------------------------------------

@dataclass
class MetaSignal:
    """
    Output signal from a meta-engine analysis.
    """
    name: str
    score: float
    label: str
    details: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.score = max(0.0, min(1.0, self.score))

# ---------------------------------------------------------------------------
# Safeguard Signal (from Safeguard Engine)
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# Story Event (from Story Engine)
# ---------------------------------------------------------------------------

@dataclass
class StoryEvent:
    """
    Single event in the narrative timeline.
    Captures complete KALDRA signal state at a moment in time.
    """
    event_id: str
    timestamp: float
    sequence_id: int
    text: str
    
    # Core KALDRA components
    delta12: Optional[Dict[str, float]] = None
    delta144_state: Optional[str] = None
    kindra: Optional[Dict[str, Any]] = None
    
    # Meta-engine scores
    meta_scores: Optional[Dict[str, Any]] = None
    
    # TW369 state
    drift_state: Optional[Dict[str, Any]] = None
    tw_state: Optional[Dict[str, Any]] = None
    
    # Polarity state
    polarity_scores: Optional[Dict[str, float]] = None
    
    # Optional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> StoryEvent:
        return cls(**data)
