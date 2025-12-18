"""
KALDRA CORE — TW369 module
Placeholder implementation. Subject to refinement in later iterations.
"""
from __future__ import annotations

import numpy as np


def finite_diff_first(series: np.ndarray) -> np.ndarray:
    """
    Compute first-order finite difference of a series.

    Args:
        series: Input time series array

    Returns:
        First derivative approximation
    """
    series = np.asarray(series, dtype=float)
    if series.size < 2:
        return np.zeros_like(series)
    return np.diff(series, n=1, prepend=series[0])


def finite_diff_second(series: np.ndarray) -> np.ndarray:
    """
    Compute second-order finite difference of a series.

    Args:
        series: Input time series array

    Returns:
        Second derivative approximation
    """
    series = np.asarray(series, dtype=float)
    if series.size < 3:
        return np.zeros_like(series)
    first = finite_diff_first(series)
    return np.diff(first, n=1, prepend=first[0])


def compute_painleve_curvature(
    series: np.ndarray,
    eps: float = 1e-8,
) -> float:
    """
    Placeholder for a Painlevé-II-inspired curvature index over a drift series.

    Returns a scalar in [0, 1] obtained by normalizing the L2 norm of the
    second derivative.

    Args:
        series: Input time series array
        eps: Small epsilon for numerical stability (default: 1e-8)

    Returns:
        Curvature index in [0, 1]
    """
    series = np.asarray(series, dtype=float)
    if series.size < 3:
        return 0.0

    second = finite_diff_second(series)
    norm_val = float(np.linalg.norm(second, ord=2))
    # Simple normalization by (1 + norm) to keep in (0,1)
    curvature = norm_val / (1.0 + norm_val + eps)
    return float(curvature)
