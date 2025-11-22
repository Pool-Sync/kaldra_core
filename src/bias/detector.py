"""
KALDRA CORE — Bias detector (placeholder).
"""
from __future__ import annotations

from typing import Any, Dict


def compute_bias_score_from_text(text: str) -> Dict[str, Any]:
    """
    Very simple placeholder bias detector based on basic heuristics.

    This is not a real bias model. It only provides a numeric surrogate:
    - exclamation marks
    - upper-case ratio
    - text length

    Args:
        text: Input text to analyze for bias

    Returns:
        Dictionary containing:
            - bias_score: Numeric score in [0.0, 1.0]
            - features: Dictionary of extracted features
    """
    length = len(text)
    exclam = text.count("!")
    caps = sum(1 for ch in text if ch.isupper())

    raw_score = 0.0
    raw_score += min(exclam / 10.0, 1.0) * 0.4
    raw_score += min(caps / max(length, 1), 0.5) * 0.3
    raw_score += min(length / 1000.0, 1.0) * 0.3

    raw_score = max(0.0, min(1.0, raw_score))
    return {
        "bias_score": raw_score,
        "features": {
            "length": length,
            "exclamations": exclam,
            "upper_case_chars": caps,
        },
    }
