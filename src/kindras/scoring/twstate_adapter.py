"""
TWState Adapter for Kindra Scoring Engine.

Bridges Kindra scoring to TW369 engine via TWState.
"""

from __future__ import annotations

from typing import Dict, Any

from src.tw369.tw369_integration import TWState
from .dispatcher import KindraScoringDispatcher


def build_twstate_from_context(context: Dict[str, Any]) -> TWState:
    """
    Adapter: runs Kindra scoring dispatcher and builds a TWState instance
    with layer scores mapped into planes 3, 6, 9.

    Plane 3  <- Layer 1 (Cultural Macro)
    Plane 6  <- Layer 2 (Semiotic / Media)
    Plane 9  <- Layer 3 (Structural / Systemic)
    
    Args:
        context: Context dict with country, sector, media_tone, etc.
        
    Returns:
        TWState instance ready for TW369 engine
    """
    dispatcher = KindraScoringDispatcher()
    result = dispatcher.run_all(context, base_vectors={})

    plane3 = result.get("layer1", {})
    plane6 = result.get("layer2", {})
    plane9 = result.get("layer3", {})

    return TWState(
        plane3_cultural_macro=plane3,
        plane6_semiotic_media=plane6,
        plane9_structural_systemic=plane9,
        metadata={"source": "kindra_rule_engine", "context_snapshot": context},
    )
