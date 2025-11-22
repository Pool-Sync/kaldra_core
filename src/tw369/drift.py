"""
KALDRA CORE — TW369 module
Placeholder implementation. Subject to refinement in later iterations.
"""
from __future__ import annotations

import numpy as np
from typing import Dict


def compute_l2_drift(vec_t: np.ndarray, vec_t1: np.ndarray) -> float:
    """
    L2 drift between two vectors.

    Args:
        vec_t: Vector at time t
        vec_t1: Vector at time t+1

    Returns:
        L2 norm of the difference between vectors
    """
    diff = np.asarray(vec_t1) - np.asarray(vec_t)
    return float(np.linalg.norm(diff, ord=2))


def compute_cosine_drift(vec_t: np.ndarray, vec_t1: np.ndarray) -> float:
    """
    1 - cosine similarity between two vectors.

    Args:
        vec_t: Vector at time t
        vec_t1: Vector at time t+1

    Returns:
        Cosine drift (1 - cosine similarity)
    """
    a = np.asarray(vec_t, dtype=float)
    b = np.asarray(vec_t1, dtype=float)
    num = float(np.dot(a, b))
    denom = float(np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)
    cos_sim = num / denom
    return float(1.0 - cos_sim)


def compute_drift_metrics(
    vec_t: np.ndarray,
    vec_t1: np.ndarray,
    delta_time: float = 1.0,
) -> Dict[str, float]:
    """
    Return basic drift metrics, including a normalized temporal drift.

    Args:
        vec_t: Vector at time t
        vec_t1: Vector at time t+1
        delta_time: Time difference between vectors (default: 1.0)

    Returns:
        Dictionary containing l2_drift, cosine_drift, and temporal_drift
    """
    l2 = compute_l2_drift(vec_t, vec_t1)
    cos = compute_cosine_drift(vec_t, vec_t1)
    temporal = l2 / max(delta_time, 1e-8)
    return {
        "l2_drift": l2,
        "cosine_drift": cos,
        "temporal_drift": temporal,
    }
