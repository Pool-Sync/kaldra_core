
"""
KALDRA-GEO — Geopolitical analyzer (placeholder).
"""
from __future__ import annotations

from typing import Any, Dict
from src.bias import compute_bias_score_from_text

from src.kaldra_engine.kaldra_engine import generate_kaldra_signal
from .geo_ingest import ingest_source


def analyze_geopolitical_text(raw_text: str) -> Dict[str, Any]:
    """
    Run the KALDRA Engine over geopolitical text.

    Args:
        raw_text: Raw geopolitical text

    Returns:
        Complete KALDRA signal dictionary
    """
    text = ingest_source(raw_text)
    return generate_kaldra_signal(text)
