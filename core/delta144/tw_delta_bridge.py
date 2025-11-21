"""
KALDRA CORE — Delta144 integration layer
Placeholder implementation. Subject to refinement in later iterations.
"""
from __future__ import annotations

from typing import Any, Dict, List
import numpy as np

from kaldra_core.core.tw369.core import compute_tw_instability_index
from kaldra_core.core.tw369.tw_guard import tw_guard_regime, compute_tw_adjustments

from .api_adapter import evaluate_sequence_stability


def apply_tw_guard_to_sequence(
    activations_sequence: List[np.ndarray],
) -> Dict[str, Any]:
    """
    Combine Delta144 sequence stability with TW-based guard logic.

    This function integrates Tracy-Widom instability analysis with Delta144
    sequence stability evaluation, providing a unified view of system state.

    Args:
        activations_sequence: List of 144-dimensional activation vectors over time

    Returns:
        Dictionary containing:
            - tw_index: Tracy-Widom instability index
            - tw_regime: Regime classification (STABLE/CRITICAL/UNSTABLE)
            - tw_adjustments: Lambda and tau adjustments based on regime
            - delta144_stability: Delta144 sequence stability metrics
    """
    # Simple strategy: treat last activation as eigenvalues proxy.
    last = np.asarray(activations_sequence[-1], dtype=float)
    tw_index = compute_tw_instability_index(last)

    guard = compute_tw_adjustments(tw_index)
    regime = guard["regime"]

    stability = evaluate_sequence_stability(activations_sequence, tau=guard["tau_adjust"])

    return {
        "tw_index": tw_index,
        "tw_regime": regime,
        "tw_adjustments": guard,
        "delta144_stability": stability,
    }
