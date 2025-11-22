"""
KALDRA CORE — Nietzschean strength operator.
"""
from __future__ import annotations

import numpy as np


def apply_strength_operator(vec: np.ndarray, factor: float = 1.1) -> np.ndarray:
    """
    Simple operator that amplifies deviations from the mean.

    v' = v + factor * (v - mean(v))

    Args:
        vec: Input vector
        factor: Amplification factor (default: 1.1)

    Returns:
        Transformed vector with amplified deviations
    """
    v = np.asarray(vec, dtype=float)
    mean = float(np.mean(v))
    centered = v - mean
    return v + factor * centered
