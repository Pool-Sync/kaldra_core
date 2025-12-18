"""
KALDRA CORE — Kindra normalization utilities.
"""
from __future__ import annotations

import numpy as np


def l2_normalize(vec: np.ndarray) -> np.ndarray:
    """
    L2-normalize a vector. Returns a new array.

    Args:
        vec: Input vector to normalize

    Returns:
        L2-normalized vector
    """
    v = np.asarray(vec, dtype=float)
    norm = float(np.linalg.norm(v, ord=2) + 1e-8)
    return v / norm


def softmax(vec: np.ndarray) -> np.ndarray:
    """
    Compute softmax over a 1D vector.

    Args:
        vec: Input vector for softmax computation

    Returns:
        Probability distribution (sums to 1)
    """
    v = np.asarray(vec, dtype=float)
    if v.size == 0:
        return v
    v = v - np.max(v)
    exp_v = np.exp(v)
    return exp_v / (np.sum(exp_v) + 1e-8)
