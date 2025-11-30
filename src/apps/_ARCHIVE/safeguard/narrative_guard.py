"""
KALDRA-SAFEGUARD — Narrative guard (placeholder).
"""
from __future__ import annotations

from typing import Any, Dict

from src.kaldra_engine.kaldra_engine import generate_kaldra_signal


def evaluate_narrative_risk(raw_text: str) -> Dict[str, Any]:
    """
    Run the KALDRA Engine and interpret the result as narrative risk.

    Args:
        raw_text: Text to evaluate for narrative risk

    Returns:
        KALDRA signal with additional narrative_risk field
    """
    signal = generate_kaldra_signal(raw_text)
    # Interpret risk from bias_score for now (placeholder)
    risk = "low"
    score = signal.get("bias_score", 0.0)
    if score > 0.8:
        risk = "high"
    elif score > 0.5:
        risk = "medium"

    signal["narrative_risk"] = risk
    return signal
