"""
KALDRA-SAFEGUARD — Continuous bias monitor (placeholder).
"""
from __future__ import annotations

from typing import Any, Dict, List

from kaldra_engine.kaldra_engine import generate_kaldra_signal


def monitor_bias_over_texts(texts: List[str]) -> List[Dict[str, Any]]:
    """
    Run the KALDRA Engine over multiple texts and collect bias scores.

    Args:
        texts: List of texts to monitor for bias

    Returns:
        List of KALDRA signals, one per input text
    """
    results: List[Dict[str, Any]] = []
    for t in texts:
        signal = generate_kaldra_signal(t)
        results.append(signal)
    return results
