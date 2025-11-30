"""
Hardening Tests: Master Engine Degraded Mode.
"""
import pytest
import numpy as np
from unittest.mock import MagicMock
from src.core.kaldra_master_engine import KaldraMasterEngineV2

def test_master_engine_degraded_flag():
    # Mock a Delta engine that fails
    mock_delta = MagicMock()
    mock_delta.infer_from_vector.side_effect = Exception("Delta Failure")
    
    engine = KaldraMasterEngineV2(delta_engine=mock_delta)
    
    # Run inference
    embedding = np.random.rand(256)
    signal = engine.infer_from_embedding(embedding)
    
    # Should return a signal, but marked degraded
    assert signal is not None
    assert signal.degraded is True
    assert signal.risk_summary == "CRITICAL_FAILURE" or signal.risk_summary == "LOW" # Depends on where it failed
