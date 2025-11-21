"""
KALDRA CORE — Stoic disciplined rationality operator.
"""
from __future__ import annotations

import numpy as np


def apply_disciplined_rationality(vec: np.ndarray, smoothing: float = 0.2) -> np.ndarray:
    """
    Blend each component towards the overall mean.

    v' = (1 - s) * v + s * mean(v)

    Args:
        vec: Input vector
        smoothing: Smoothing factor towards mean (default: 0.2)

    Returns:
        Smoothed vector blended towards mean
    """
    v = np.asarray(vec, dtype=float)
    mean = float(np.mean(v))
    return (1.0 - smoothing) * v + smoothing * mean
