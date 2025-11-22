"""
KALDRA CORE — TW369 module
Placeholder implementation. Subject to refinement in later iterations.
"""
from __future__ import annotations

from typing import Dict, Literal

TWRegime = Literal["STABLE", "CRITICAL", "UNSTABLE"]


def tw_guard_regime(
    tw_index: float,
    low: float = 0.3,
    high: float = 0.7,
) -> TWRegime:
    """
    Map a TW instability index into a coarse regime.

    Args:
        tw_index: Tracy-Widom instability index in [0, 1]
        low: Lower threshold for STABLE regime (default: 0.3)
        high: Upper threshold for UNSTABLE regime (default: 0.7)

    Returns:
        Regime classification: STABLE, CRITICAL, or UNSTABLE
    """
    if tw_index < low:
        return "STABLE"
    if tw_index > high:
        return "UNSTABLE"
    return "CRITICAL"


def compute_tw_adjustments(
    tw_index: float,
    base_lambda: float = 1.0,
    base_tau: float = 1.0,
) -> Dict[str, float]:
    """
    Produce simple lambda/tau adjustments based on instability.

    Args:
        tw_index: Tracy-Widom instability index in [0, 1]
        base_lambda: Base lambda parameter (default: 1.0)
        base_tau: Base tau parameter (default: 1.0)

    Returns:
        Dictionary containing regime, lambda_adjust, and tau_adjust
    """
    regime = tw_guard_regime(tw_index)
    if regime == "STABLE":
        return {"regime": regime, "lambda_adjust": 0.8 * base_lambda, "tau_adjust": 1.2 * base_tau}
    if regime == "UNSTABLE":
        return {"regime": regime, "lambda_adjust": 1.2 * base_lambda, "tau_adjust": 0.8 * base_tau}
    # CRITICAL
    return {"regime": regime, "lambda_adjust": 1.0 * base_lambda, "tau_adjust": 1.0 * base_tau}
