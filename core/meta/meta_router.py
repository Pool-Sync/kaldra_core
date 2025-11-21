"""
KALDRA CORE — Meta-operator router.
"""
from __future__ import annotations

from typing import Any, Dict

import numpy as np

from .nietzsche import apply_strength_operator
from .campbell import apply_journey_operator
from .aurelius import apply_disciplined_rationality


def apply_meta_operators(
    vec: np.ndarray,
    config: Dict[str, Any] | None = None,
) -> Dict[str, np.ndarray]:
    """
    Apply the three meta-operators to a vector and return the results.

    Args:
        vec: Input vector
        config: Optional configuration dictionary with keys:
            - strength_factor: Nietzschean amplification factor
            - journey_phase: Campbellian ramp maximum
            - discipline_smoothing: Stoic smoothing factor

    Returns:
        Dictionary containing transformed vectors:
            - strength: Nietzschean transformation
            - journey: Campbellian transformation
            - discipline: Stoic transformation
    """
    cfg = config or {}
    v = np.asarray(vec, dtype=float)

    v_strength = apply_strength_operator(v, factor=cfg.get("strength_factor", 1.1))
    v_journey = apply_journey_operator(v, phase=cfg.get("journey_phase", 0.5))
    v_discipline = apply_disciplined_rationality(
        v, smoothing=cfg.get("discipline_smoothing", 0.2)
    )

    return {
        "strength": v_strength,
        "journey": v_journey,
        "discipline": v_discipline,
    }
