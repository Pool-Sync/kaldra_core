"""
Unit tests for advanced drift models.
"""

import pytest
from src.tw369.advanced_drift_models import (
    DriftModelConfig,
    DriftState,
    model_a_linear_drift,
    model_b_nonlinear_drift,
    model_c_multiscale_drift,
    model_d_stochastic_drift,
)


class TestAdvancedDriftModels:
    def test_model_a_linear_drift_scales_with_severity(self):
        gradients = {"plane3_to_6": 1.0, "plane6_to_9": -2.0, "plane9_to_3": 0.5}
        d_low = model_a_linear_drift(gradients, severity=0.2, normalization_k=3.5)
        d_high = model_a_linear_drift(gradients, severity=0.8, normalization_k=3.5)

        assert abs(d_high["plane3_to_6"]) > abs(d_low["plane3_to_6"])
        assert d_low["plane6_to_9"] < 0.0
        assert d_high["plane6_to_9"] < 0.0

    def test_model_b_nonlinear_drift_is_bounded_by_tanh(self):
        cfg = DriftModelConfig(
            nonlinear_enabled=True,
            nonlinear_exponent=1.5,
            nonlinear_tanh_scale=1.0,
        )
        gradients = {"plane3_to_6": 10.0, "plane6_to_9": -10.0, "plane9_to_3": 5.0}
        drift = model_b_nonlinear_drift(gradients, severity=1.0, cfg=cfg, normalization_k=1.0)

        for v in drift.values():
            assert -1.0 <= v <= 1.0

    def test_model_c_multiscale_drift_accumulates_memory(self):
        cfg = DriftModelConfig(
            multiscale_enabled=True,
            multiscale_alpha=0.5,
            multiscale_beta=0.5,
        )
        gradients = {"plane3_to_6": 1.0, "plane6_to_9": 0.0, "plane9_to_3": -1.0}
        base = model_a_linear_drift(gradients, severity=1.0, normalization_k=1.0)

        d1, state1 = model_c_multiscale_drift(base, cfg=cfg, prev_state=None)
        d2, state2 = model_c_multiscale_drift(base, cfg=cfg, prev_state=state1)

        # After repeated application with the same base, second drift should be closer
        # to base than the first (memory effect).
        assert abs(d2["plane3_to_6"] - base["plane3_to_6"]) < abs(d1["plane3_to_6"] - base["plane3_to_6"])

    def test_model_d_stochastic_drift_is_reproducible_with_seed(self):
        cfg = DriftModelConfig(
            stochastic_enabled=True,
            stochastic_base_sigma=0.1,
            stochastic_severity_scale=0.5,
            stochastic_seed=42,
        )
        base = {"plane3_to_6": 0.1, "plane6_to_9": 0.2, "plane9_to_3": -0.1}

        d1 = model_d_stochastic_drift(base, severity=0.7, cfg=cfg)
        d2 = model_d_stochastic_drift(base, severity=0.7, cfg=cfg)

        # With fixed seed, two calls should produce the same noise sequence.
        assert d1 == d2

    def test_model_a_preserves_gradient_signs(self):
        gradients = {"plane3_to_6": 1.0, "plane6_to_9": -1.0, "plane9_to_3": 0.5}
        drift = model_a_linear_drift(gradients, severity=0.5, normalization_k=2.5)

        assert drift["plane3_to_6"] > 0.0
        assert drift["plane6_to_9"] < 0.0
        assert drift["plane9_to_3"] > 0.0

    def test_model_b_nonlinear_preserves_gradient_signs(self):
        cfg = DriftModelConfig(
            nonlinear_enabled=True,
            nonlinear_exponent=1.5,
            nonlinear_tanh_scale=1.0,
        )
        gradients = {"plane3_to_6": 1.0, "plane6_to_9": -1.0, "plane9_to_3": 0.5}
        drift = model_b_nonlinear_drift(gradients, severity=0.5, cfg=cfg, normalization_k=2.5)

        assert drift["plane3_to_6"] > 0.0
        assert drift["plane6_to_9"] < 0.0
        assert drift["plane9_to_3"] > 0.0
