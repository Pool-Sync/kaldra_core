"""
KALDRA CORE — Bias Engine (detection + scoring).
"""
from __future__ import annotations

from .detector import compute_bias_score_from_text
from .scoring import classify_bias

__all__ = ["compute_bias_score_from_text", "classify_bias"]
