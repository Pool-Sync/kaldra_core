# DEPRECATED — Legacy Kindra scoring (Option A original).
# This module remains only for backward compatibility.
# New scoring engines: Rule-Based v2, LLM-Based (Option B), Hybrid (Option C).
"""
KALDRA CORE — Kindra scoring utilities.
"""
from __future__ import annotations

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.

    Args:
        a: First vector
        b: Second vector

    Returns:
        Cosine similarity in [-1, 1]
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    num = float(np.dot(a, b))
    denom = float(np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)
    return num / denom
