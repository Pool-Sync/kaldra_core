"""
Utility functions for applying adaptive state-plane mapping to TW369 calculations.
"""

from __future__ import annotations

from typing import Dict

from .state_plane_mapping import PlaneMappingResult


def apply_plane_weights_to_tensions(
    plane_tensions: Dict[int, float],
    mapping: PlaneMappingResult,
) -> Dict[int, float]:
    """
    Apply plane weights from mapping to raw plane tensions.

    Input:
        plane_tensions: {3: t3, 6: t6, 9: t9}
        mapping: plane_weights from AdaptiveStatePlaneMapper

    Output:
        {3: t3', 6: t6', 9: t9'} where tN' = tN * wN

    This does NOT modify the original tension model, only reweights per-plane contribution.
    """
    w = mapping.plane_weights
    weighted = {}

    t3 = plane_tensions.get(3, 0.0)
    t6 = plane_tensions.get(6, 0.0)
    t9 = plane_tensions.get(9, 0.0)

    weighted[3] = t3 * w.plane3
    weighted[6] = t6 * w.plane6
    weighted[9] = t9 * w.plane9

    return weighted
