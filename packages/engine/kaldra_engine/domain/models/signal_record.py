"""
Signal record model for Supabase.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class SignalRecord:
    """
    Aggregated signal record for dashboard.

    Attributes:
        id: Unique identifier
        created_at: Creation timestamp
        domain: Signal domain (alpha, geo, product, safeguard)
        title: Signal title
        summary: Brief summary
        source_anchor: Source identifier (nyt, twitter, bloomberg)
        source_url: Source URL
        delta144_state: Delta144 state (threshold, eruption, etc.)
        dominant_archetype: Dominant archetype (hero, rebel, etc.)
        dominant_polarity: Dominant polarity (order, chaos, etc.)
        tw_regime: TW369 regime (STABLE, CRITICAL, etc.)
        journey_stage: Journey stage (call_to_adventure, etc.)
        importance: Importance score [0-1]
        confidence: Confidence score [0-1]
        divergence: Multi-stream divergence [0-1]
        raw_payload: Raw KALDRA output
    """

    id: str
    created_at: datetime | None
    domain: str

    title: str
    summary: str | None = None
    source_anchor: str | None = None
    source_url: str | None = None

    delta144_state: str | None = None
    dominant_archetype: str | None = None
    dominant_polarity: str | None = None
    tw_regime: str | None = None
    journey_stage: str | None = None

    importance: float | None = None
    confidence: float | None = None
    divergence: float | None = None

    raw_payload: dict[str, Any] | None = None
