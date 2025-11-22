"""
KALDRA CORE — Bias scoring utilities.
"""
from __future__ import annotations


def classify_bias(score: float) -> str:
    """
    Classify a bias score in [0, 1] into coarse labels.

    Args:
        score: Bias score in range [0.0, 1.0]

    Returns:
        Classification label: "neutral", "negative", "positive", or "extreme"
    """
    if score < 0.3:
        return "neutral"
    if score < 0.6:
        return "negative"
    if score < 0.8:
        return "positive"
    return "extreme"
