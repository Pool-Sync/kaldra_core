"""
Tests for Safeguard Engine.
"""
import pytest
from src.safeguard.safeguard_engine import SafeguardEngine
from src.tau.tau_state import TauState

@pytest.fixture
def safeguard_engine():
    return SafeguardEngine()

def test_safeguard_neutral(safeguard_engine):
    """Test Safeguard with safe state."""
    tau_state = TauState(
        tau_score=0.95,
        tau_risk="LOW",
        tau_modifiers={},
        tau_actions=[],
        details={"features": {"bias_score": 0.0}}
    )
    drift_state = {"velocity": 0.1}
    polarities = {"POL_A": 0.5}
    meta = {}
    
    signal = safeguard_engine.evaluate(tau_state, drift_state, polarities, meta)
    
    assert signal.final_risk == "LOW"
    assert signal.risk_score < 0.3
    assert not signal.mitigation_actions

def test_safeguard_critical(safeguard_engine):
    """Test Safeguard with critical risk factors."""
    tau_state = TauState(
        tau_score=0.1,
        tau_risk="CRITICAL",
        tau_modifiers={},
        tau_actions=[],
        details={"features": {"bias_score": 0.9}}
    )
    drift_state = {"velocity": 1.5} # High drift
    polarities = {"POL_A": 0.0, "POL_B": 1.0} # Extreme polarization
    meta = {"nietzsche": {"scores": {"active_nihilism": 0.9}}} # High nihilism
    
    signal = safeguard_engine.evaluate(tau_state, drift_state, polarities, meta)
    
    assert signal.final_risk in ["HIGH", "CRITICAL"]
    assert signal.risk_score > 0.6
    assert "BLOCK_OUTPUT" in signal.mitigation_actions or "FLAG_RISK_HIGH" in signal.mitigation_actions
