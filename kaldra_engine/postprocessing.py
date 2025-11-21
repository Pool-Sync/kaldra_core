"""
KALDRA CORE — Postprocessing utilities.
"""
from __future__ import annotations

from typing import Any, Dict


def build_explanation(summary: Dict[str, Any]) -> str:
    """
    Build a minimal textual explanation from a KALDRA signal summary.

    Args:
        summary: KALDRA signal summary dictionary

    Returns:
        Human-readable explanation string
    """
    return (
        f"KALDRA signal generated with archetype={summary.get('archetype')}, "
        f"tw_regime={summary.get('tw_regime')}, "
        f"bias_score={summary.get('bias_score'):.3f}."
    )
