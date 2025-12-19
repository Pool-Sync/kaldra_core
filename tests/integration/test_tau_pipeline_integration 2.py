"""
Integration Tests for Tau Pipeline (v2.8).
"""
import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from src.core.kaldra_master_engine import KaldraMasterEngineV2, KaldraSignal
from src.tau.tau_state import TauState

@pytest.fixture
def master_engine():
    # Mock dependencies to avoid loading heavy models
    with patch("src.core.kaldra_master_engine.Delta144Engine") as MockDelta, \
         patch("src.core.kaldra_master_engine.KaldraKindraCulturalMod") as MockKindra, \
         patch("src.core.kaldra_master_engine.TWPainleveOracle") as MockOracle, \
         patch("src.core.kaldra_master_engine.TW369Integrator") as MockIntegrator:
         
        engine = KaldraMasterEngineV2(d_ctx=10)
        
        # Setup mocks
        engine.delta.infer_from_vector.return_value = MagicMock(probs=np.ones(144)/144, to_dict=lambda: {})
        engine.delta.infer_modifier_scores_from_embedding.return_value = {}
        engine.kindra_mod.return_value = (MagicMock(detach=lambda: MagicMock(cpu=lambda: MagicMock(numpy=lambda: np.ones(144)/144))),)
        engine.tw_integrator.compute_drift.return_value = {"plane3_to_6": 0.1}
        engine.tw_integrator.create_state.return_value = MagicMock()
        
        return engine

def test_end_to_end_tau_flow(master_engine):
    """Test that Tau and Safeguard are executed in the pipeline."""
    embedding = np.random.rand(10)
    
    # Run inference
    signal = master_engine.infer_from_embedding(embedding)
    
    # Verify signal structure
    assert isinstance(signal, KaldraSignal)
    assert signal.tau is not None
    assert "tau_score" in signal.tau
    assert signal.safeguard is not None
    assert "final_risk" in signal.safeguard
    
    # Verify Tau Layer was called
    # (We can't easily check internal calls without mocking TauLayer itself, 
    # but the presence of output confirms it ran)
    assert signal.tau["tau_risk"] in ["LOW", "MID", "HIGH", "CRITICAL"]

def test_tau_modulation_flow(master_engine):
    """Test that Tau modifiers are passed to Delta engine."""
    embedding = np.random.rand(10)
    
    # Mock Tau Layer to return specific modifiers
    with patch.object(master_engine.tau_layer, 'compute_tau_input_phase') as mock_tau_input:
        mock_tau_input.return_value = TauState(
            tau_score=0.5,
            tau_risk="MID",
            tau_modifiers={"drift_damping": 0.5, "archetype_smoothing": 0.8},
            tau_actions=[]
        )
        
        master_engine.infer_from_embedding(embedding)
        
        # Verify Delta engine received modifiers
        master_engine.delta.infer_from_vector.assert_called()
        call_kwargs = master_engine.delta.infer_from_vector.call_args[1]
        assert "tau_modifiers" in call_kwargs
        assert call_kwargs["tau_modifiers"]["drift_damping"] == 0.5
        
        # Verify TW Integrator received modifiers
        master_engine.tw_integrator.compute_drift.assert_called()
        call_kwargs_tw = master_engine.tw_integrator.compute_drift.call_args[1]
        assert "tau_modifiers" in call_kwargs_tw
        assert call_kwargs_tw["tau_modifiers"]["drift_damping"] == 0.5
