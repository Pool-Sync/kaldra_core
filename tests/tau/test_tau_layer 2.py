"""
Tests for Tau Layer (Epistemic Limiter v2).
"""
import pytest
from src.tau.tau_layer import TauLayer
from src.tau.tau_state import TauState

@pytest.fixture
def tau_layer():
    return TauLayer()

def test_tau_input_phase_neutral(tau_layer):
    """Test Tau Layer with neutral/safe inputs."""
    bias = {"score": 0.0}
    polarity = {"POL_LIGHT_SHADOW": 0.5, "POL_ORDER_CHAOS": 0.5} # Perfectly balanced
    modifiers = {}
    
    state = tau_layer.compute_tau_input_phase(bias, polarity, modifiers)
    
    assert state.tau_score > 0.9
    assert state.tau_risk == "LOW"
    assert not state.tau_actions
    assert state.tau_modifiers["drift_damping"] == 1.0

def test_tau_input_phase_high_risk(tau_layer):
    """Test Tau Layer with high risk inputs (extreme polarity)."""
    bias = {"score": 0.8} # High bias
    polarity = {
        "POL_LIGHT_SHADOW": 0.0, # Extreme Shadow
        "POL_ORDER_CHAOS": 1.0,  # Extreme Chaos (if 1.0 is chaos)
        "POL_LIFE_DEATH": 0.0    # Extreme Death
    }
    modifiers = {}
    
    state = tau_layer.compute_tau_input_phase(bias, polarity, modifiers)
    
    assert state.tau_score < 0.5
    assert state.tau_risk in ["HIGH", "CRITICAL"]
    assert "drift_damping" in state.tau_modifiers
    assert state.tau_modifiers["drift_damping"] < 1.0
    assert "archetype_smoothing" in state.tau_modifiers
    assert state.tau_modifiers["archetype_smoothing"] < 1.0

def test_tau_output_phase_instability(tau_layer):
    """Test Tau Layer output phase with high drift instability."""
    drift_state = {"velocity": 2.0, "severity": 0.9} # High velocity/severity
    meta = {}
    
    state = tau_layer.compute_tau_output_phase(None, drift_state, meta)
    
    assert state.tau_score < 0.6
    assert state.tau_risk in ["MID", "HIGH", "CRITICAL"]
    assert "FLAG_RISK" in state.tau_actions or "CLAMP_DRIFT" in state.tau_actions
