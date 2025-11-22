"""
KALDRA CORE — Campbellian journey operator.
"""
from __future__ import annotations

import numpy as np


def apply_journey_operator(vec: np.ndarray, phase: float = 0.5) -> np.ndarray:
    """
    Simple ramp operator over the vector positions.

    v'_i = v_i * (1 + ramp_i), where ramp_i goes from 0 to phase.

    Args:
        vec: Input vector
        phase: Maximum ramp value (default: 0.5)

    Returns:
        Transformed vector with progressive amplification
    """
    v = np.asarray(vec, dtype=float)
    n = v.size
    if n == 0:
        return v
    ramp = np.linspace(0.0, phase, n)
    return v * (1.0 + ramp)
