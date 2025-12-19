"""
Unified State Definitions for KALDRA Core.
Contains state objects for various engines (TW369, Tau, Archetypes).
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Archetypal State (from Delta144)
# ---------------------------------------------------------------------------


@dataclass
class Archetype:
    id: str
    label: str
    essence: str
    light: str
    shadow: str
    drives: list[str]
    journey_role: str
    stoic_axis: str
    description: str


@dataclass
class ArchetypeState:
    """
    Represents a cell in the Delta144 matrix (archetype x state).
    """

    id: str
    archetype_id: str
    row: int
    col: int
    label: str
    profile: str  # "EXPANSIVE" | "CONTRACTIVE" | "TRANSCENDENT"
    tw_plane_default: str  # "3", "6", "9"
    description: str
    default_modifiers: list[str] = field(default_factory=list)
    allowed_modifiers: list[str] = field(default_factory=list)


@dataclass
class Modifier:
    """
    Dynamic qualifier that can be applied to a Delta144 state.
    """

    id: str
    label: str
    category: str
    description: str
    tw_alignment: list[str]


@dataclass
class Polarity:
    """
    Dimensional tension structuring the experience.
    """

    id: str
    label: str
    description: str
    dimension: str
    tw_alignment: list[str]


@dataclass
class StateInferenceResult:
    """
    Final result of Delta144 state inference.
    """

    archetype: Archetype
    state: ArchetypeState
    active_modifiers: list[Modifier]
    scores: dict[str, Any]
    probs: list[float] | None = None
    polarity_scores: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "archetype": {
                "id": self.archetype.id,
                "label": self.archetype.label,
                "essence": self.archetype.essence,
            },
            "state": {
                "id": self.state.id,
                "label": self.state.label,
                "profile": self.state.profile,
                "description": self.state.description,
            },
            "active_modifiers": [asdict(m) for m in self.active_modifiers],
            "scores": self.scores,
            "probs": self.probs,
            "polarity_scores": self.polarity_scores,
        }


# ---------------------------------------------------------------------------
# Drift State (from TW369)
# ---------------------------------------------------------------------------


@dataclass
class DriftState:
    """
    Represents the state of TW369 drift at a point in time.
    """

    timestamp: float = field(default_factory=time.time)
    plane_values: dict[str, float] = field(default_factory=lambda: {"3": 0.0, "6": 0.0, "9": 0.0})
    drift_metric: float = 0.0
    painleve_coherence: float = 0.0
    history_window: list[dict[str, Any]] = field(default_factory=list)
    regime: str = "UNKNOWN"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DriftState:
        return cls(**data)


# ---------------------------------------------------------------------------
# Tau State (from Tau Layer)
# ---------------------------------------------------------------------------


@dataclass
class TauState:
    """
    Represents the epistemic reliability state of the system.
    """

    tau_score: float
    tau_risk: str
    tau_modifiers: dict[str, float] = field(default_factory=dict)
    tau_actions: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tau_score": self.tau_score,
            "tau_risk": self.tau_risk,
            "tau_modifiers": self.tau_modifiers,
            "tau_actions": self.tau_actions,
            "details": self.details,
        }
