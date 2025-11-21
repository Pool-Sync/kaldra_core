"""
KALDRA-PRODUCT — Product analyzer (placeholder).
"""
from __future__ import annotations

from typing import Any, Dict

from kaldra_engine.kaldra_engine import generate_kaldra_signal
from .product_ingest import ingest_source


def analyze_product_text(raw_text: str) -> Dict[str, Any]:
    """
    Run the KALDRA Engine over product-related text.

    Args:
        raw_text: Raw product review or UX feedback text

    Returns:
        Complete KALDRA signal dictionary
    """
    text = ingest_source(raw_text)
    return generate_kaldra_signal(text)
