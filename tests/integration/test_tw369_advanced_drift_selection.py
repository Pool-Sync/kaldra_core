"""
Integration tests for TW369 advanced drift model selection.
"""

import pytest
from src.tw369.tw369_integration import TW369Integrator, TWState


def _make_dummy_state() -> TWState:
    return TWState(
        plane3_cultural_macro={"E01": 0.3},
        plane6_semiotic_media={"E01": 0.1},
        plane9_structural_systemic={"E01": -0.2},
        metadata={},
    )


class TestTW369AdvancedDriftSelection:
    def test_tw369_integrator_uses_model_a_by_default(self):
        integrator = TW369Integrator()
        state = _make_dummy_state()

        result_linear = integrator.compute_drift(state)
        assert isinstance(result_linear, dict)
        assert set(result_linear.keys()) == {
            "plane3_to_6",
            "plane6_to_9",
            "plane9_to_3",
        }

    def test_tw369_integrator_accepts_nonlinear_model_when_enabled(self):
        integrator = TW369Integrator()
        state = _make_dummy_state()

        # Manually override config fields
        integrator._drift_model = "nonlinear"
        cfg = integrator._drift_model_config
        cfg.nonlinear_enabled = True

        result_nl = integrator.compute_drift(state)
        assert isinstance(result_nl, dict)
        assert set(result_nl.keys()) == {
            "plane3_to_6",
            "plane6_to_9",
            "plane9_to_3",
        }

    def test_tw369_integrator_multiscale_model(self):
        integrator = TW369Integrator()
        state = _make_dummy_state()

        # Enable multiscale
        integrator._drift_model = "multiscale"
        cfg = integrator._drift_model_config
        cfg.multiscale_enabled = True

        result1 = integrator.compute_drift(state)
        result2 = integrator.compute_drift(state)

        # Both should be valid drifts
        assert isinstance(result1, dict)
        assert isinstance(result2, dict)
        
        # State should be updated
        assert integrator._drift_state is not None

    def test_tw369_integrator_stochastic_model_with_seed(self):
        integrator = TW369Integrator()
        state = _make_dummy_state()

        # Enable stochastic with seed
        integrator._drift_model = "stochastic"
        cfg = integrator._drift_model_config
        cfg.stochastic_enabled = True
        cfg.stochastic_seed = 123

        result1 = integrator.compute_drift(state)
        result2 = integrator.compute_drift(state)

        # With seed, results should be reproducible
        assert result1 == result2

    def test_tw369_integrator_fallback_to_model_a_on_invalid_model(self):
        integrator = TW369Integrator()
        state = _make_dummy_state()

        # Set invalid model
        integrator._drift_model = "invalid_model"

        result = integrator.compute_drift(state)
        
        # Should fallback to Model A
        assert isinstance(result, dict)
        assert set(result.keys()) == {
            "plane3_to_6",
            "plane6_to_9",
            "plane9_to_3",
        }
