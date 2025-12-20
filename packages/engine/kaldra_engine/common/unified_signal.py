"""
Unified Signal Definitions for KALDRA Core.
Contains signal objects for various engines (Meta, Safeguard, Story).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

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
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.score = max(0.0, min(1.0, self.score))


# ---------------------------------------------------------------------------
# Safeguard Signal (from Safeguard Engine)
# ---------------------------------------------------------------------------


@dataclass
class SafeguardSignal:
    """Output signal from the Safeguard Engine."""

    bias: dict[str, Any]
    polarity_risk: dict[str, float]
    drift_risk: dict[str, float]
    journey_risk: dict[str, float]
    meta_risk: dict[str, float]
    final_risk: str  # "LOW", "MID", "HIGH", "CRITICAL"
    risk_score: float  # 0.0 - 1.0
    mitigation_actions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Story Event (from Story Engine)
# ---------------------------------------------------------------------------


@dataclass
class StoryEvent:
    """
    Single event in the narrative timeline.
    Captures complete KALDRA signal state at a moment in time.

    Extended in v3.3 Phase 2:
    - stream_id: Optional identifier for multi-stream narrative tracking
    """

    event_id: str
    timestamp: float
    sequence_id: int
    text: str

    # Core KALDRA components
    delta12: dict[str, float] | None = None
    delta144_state: str | None = None
    kindra: dict[str, Any] | None = None

    # Meta-engine scores
    meta_scores: dict[str, Any] | None = None

    # TW369 state
    drift_state: dict[str, Any] | None = None
    tw_state: dict[str, Any] | None = None

    # Polarity state
    polarity_scores: dict[str, float] | None = None

    # v3.3 Phase 2 — Multi-Stream Narratives
    stream_id: str | None = None  # e.g., "nyt", "twitter", "report_42"

    # Optional metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StoryEvent:
        return cls(**data)
