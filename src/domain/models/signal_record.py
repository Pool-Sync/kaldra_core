"""
Signal record model for Supabase.
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


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
    created_at: Optional[datetime]
    domain: str
    
    title: str
    summary: Optional[str] = None
    source_anchor: Optional[str] = None
    source_url: Optional[str] = None
    
    delta144_state: Optional[str] = None
    dominant_archetype: Optional[str] = None
    dominant_polarity: Optional[str] = None
    tw_regime: Optional[str] = None
    journey_stage: Optional[str] = None
    
    importance: Optional[float] = None
    confidence: Optional[float] = None
    divergence: Optional[float] = None
    
    raw_payload: Optional[Dict[str, Any]] = None
