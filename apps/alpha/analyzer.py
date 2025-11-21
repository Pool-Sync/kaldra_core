"""
KALDRA-ALPHA — Earnings call analyzer (placeholder).
"""
from __future__ import annotations

from typing import Any, Dict

from kaldra_core.kaldra_engine import generate_kaldra_signal
from .ingest import ingest_source


def analyze_earnings_call(raw_text: str) -> Dict[str, Any]:
    """
    Run the KALDRA Engine over an earnings call transcript.

    Args:
        raw_text: Raw earnings call transcript text

    Returns:
        Complete KALDRA signal dictionary
    """
    text = ingest_source(raw_text)
    return generate_kaldra_signal(text)
