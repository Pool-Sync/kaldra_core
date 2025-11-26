import pytest
from src.core.kaldra_master_engine import KaldraMasterEngineV2

def test_config_initialization():
    """Test engine initialization with different tau values."""
    engine1 = KaldraMasterEngineV2(tau=0.5)
    engine2 = KaldraMasterEngineV2(tau=0.9)
    
    assert engine1.tau_layer.tau == 0.5
    assert engine2.tau_layer.tau == 0.9

def test_config_d_ctx_values():
    """Test with different context dimensions."""
    engine128 = KaldraMasterEngineV2(d_ctx=128)
    engine512 = KaldraMasterEngineV2(d_ctx=512)
    
    assert engine128.kindra_mod.ctx_norm.normalized_shape == (128,)
    assert engine512.kindra_mod.ctx_norm.normalized_shape == (512,)
