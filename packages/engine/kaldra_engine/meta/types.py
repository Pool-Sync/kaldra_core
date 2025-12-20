"""
Shared types for Meta Engines (v3.1+).
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from kaldra_engine.common.types import TWState
from kaldra_engine.unification.states.unified_state import KindraContext

if TYPE_CHECKING:
    from kaldra_engine.unification.states.unified_state import (
        DriftContext,
        StoryContext,
    )


@dataclass
class MetaInput:
    """
    Standard input for meta-engine analysis (v3.1+).

    Attributes:
        text: Input text to analyze
        delta144_state: Optional current Δ144 state identifier
        archetype_scores: Optional archetype distribution scores
        kindra: Optional KindraContext with 3×48 vectors
        tw_state: Optional TWState for drift/regime awareness
        bias_score: Optional bias detection score
        polarity_scores: Optional polarity scores
        modifiers: Optional adjustment modifiers
        drift_ctx: Optional DriftContext for v3.2 topological drift (TODO v3.3: unified refactor)
        story_ctx: Optional StoryContext for v3.2 temporal narrative (TODO v3.3: unified refactor)
    """

    text: str
    delta144_state: str | None = None
    archetype_scores: dict[str, float] = field(default_factory=dict)
    kindra: KindraContext | None = None
    tw_state: TWState | None = None
    bias_score: float | None = None
    polarity_scores: dict[str, float] | None = None
    modifiers: dict[str, float] | None = None

    # v3.2: Temporal contexts (TODO v3.3: unified refactor across meta-engines)
    drift_ctx: Optional["DriftContext"] = None
    story_ctx: Optional["StoryContext"] = None
