"""
Advanced Drift Models for TW369.

Implements Models B, C, D while preserving Model A as baseline.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Dict, Optional, Tuple


@dataclass
class DriftModelConfig:
    """
    Configuration slice for advanced drift models extracted from
    schema/tw369/drift_parameters.json and TW369 config.
    """
    default_model: str = "model_a"
    nonlinear_enabled: bool = False
    nonlinear_exponent: float = 1.5
    nonlinear_tanh_scale: float = 1.0
    nonlinear_mode: str = "power_then_tanh"
    multiscale_enabled: bool = False
    multiscale_alpha: float = 0.7
    multiscale_beta: float = 0.3
    stochastic_enabled: bool = False
    stochastic_base_sigma: float = 0.05
    stochastic_severity_scale: float = 0.5
    stochastic_seed: Optional[int] = None


@dataclass
class DriftState:
    """
    Holds persistent state for multiscale models.

    last_drift: last step drift values { 'plane3_to_6': ..., ... }
    long_term_drift: slower moving drift baseline.
    """
    last_drift: Dict[str, float]
    long_term_drift: Dict[str, float]


def model_a_linear_drift(
    gradients: Dict[str, float],
    severity: float,
    normalization_k: float,
) -> Dict[str, float]:
    """
    Baseline linear drift (Model A), preserved for backward compatibility.

    drift = (grad / k) * severity
    """
    k = max(1.0, normalization_k)
    return {
        key: (g / k) * severity
        for key, g in gradients.items()
    }


def nonlinear_transform_gradient(
    g: float,
    exponent: float,
    tanh_scale: float,
    mode: str = "power_then_tanh",
) -> float:
    """
    Apply a non-linear transformation to a single gradient value.

    - 'power_then_tanh': g' = tanh(sign(g) * |g|^p / tanh_scale)
    """
    if mode == "power_then_tanh":
        sign = 1.0 if g >= 0.0 else -1.0
        mag = abs(g) ** exponent
        if tanh_scale <= 0.0:
            tanh_scale = 1.0
        return math.tanh(sign * mag / tanh_scale)
    # future modes can be added here
    return g


def model_b_nonlinear_drift(
    gradients: Dict[str, float],
    severity: float,
    cfg: DriftModelConfig,
    normalization_k: float,
) -> Dict[str, float]:
    """
    Nonlinear drift model (Model B).

    Steps:
    1. Apply non-linear transform to each gradient (power + tanh).
    2. Normalize by k.
    3. Scale by severity.
    """
    transformed: Dict[str, float] = {}
    for key, g in gradients.items():
        g_nl = nonlinear_transform_gradient(
            g,
            exponent=cfg.nonlinear_exponent,
            tanh_scale=cfg.nonlinear_tanh_scale,
            mode=cfg.nonlinear_mode,
        )
        transformed[key] = g_nl

    k = max(1.0, normalization_k)
    return {
        key: (g_nl / k) * severity
        for key, g_nl in transformed.items()
    }


def model_c_multiscale_drift(
    instantaneous_drift: Dict[str, float],
    cfg: DriftModelConfig,
    prev_state: Optional[DriftState],
) -> Tuple[Dict[str, float], DriftState]:
    """
    Multiscale drift model (Model C).

    Combines:
        - instantaneous drift (current step)
        - short-term memory (last_drift)
        - long-term memory (long_term_drift)

    Using:
        d_short = alpha * inst + (1 - alpha) * last
        d_long  = beta  * inst + (1 - beta)  * long_prev
    """
    alpha = cfg.multiscale_alpha
    beta = cfg.multiscale_beta

    if prev_state is None:
        prev_last = {k: 0.0 for k in instantaneous_drift.keys()}
        prev_long = {k: 0.0 for k in instantaneous_drift.keys()}
    else:
        prev_last = dict(prev_state.last_drift)
        prev_long = dict(prev_state.long_term_drift)

    new_short: Dict[str, float] = {}
    new_long: Dict[str, float] = {}

    for key, inst_val in instantaneous_drift.items():
        last_val = prev_last.get(key, 0.0)
        long_val = prev_long.get(key, 0.0)

        d_short = alpha * inst_val + (1.0 - alpha) * last_val
        d_long = beta * inst_val + (1.0 - beta) * long_val

        new_short[key] = d_short
        new_long[key] = d_long

    new_state = DriftState(last_drift=new_short, long_term_drift=new_long)

    # For now, return short-term as effective drift; long-term is stored for analysis/future.
    return new_short, new_state


def model_d_stochastic_drift(
    base_drift: Dict[str, float],
    severity: float,
    cfg: DriftModelConfig,
) -> Dict[str, float]:
    """
    Stochastic drift model (Model D).

    Adds Gaussian noise to each drift component with:
        sigma = base_sigma * (1 + severity * severity_scale)

    If stochastic_seed is set, uses it once to seed the RNG for reproducibility.
    """
    if cfg.stochastic_seed is not None:
        random.seed(cfg.stochastic_seed)

    sev_clamped = max(0.0, min(1.0, severity))
    sigma = cfg.stochastic_base_sigma * (1.0 + sev_clamped * cfg.stochastic_severity_scale)

    noisy: Dict[str, float] = {}
    for key, val in base_drift.items():
        noise = random.gauss(0.0, sigma)
        noisy[key] = val + noise
    return noisy
