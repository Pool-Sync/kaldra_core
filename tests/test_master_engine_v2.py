import numpy as np
import pytest
from src.core.kaldra_master_engine import KaldraMasterEngineV2, KaldraSignal

def test_master_engine_initialization():
    engine = KaldraMasterEngineV2(d_ctx=128, tau=0.7)
    assert engine.tau_layer.tau == 0.7
    assert engine.kindra_mod.ctx_norm.normalized_shape == (128,)

def test_master_engine_inference_no_tw():
    engine = KaldraMasterEngineV2(d_ctx=128)
    
    embedding = np.random.randn(128)
    signal = engine.infer_from_embedding(embedding)
    
    assert isinstance(signal, KaldraSignal)
    assert signal.archetype_probs.shape == (144,)
    assert signal.tw_trigger is False
    assert signal.tw_stats is None
    # Epistemic check
    assert signal.epistemic.status in ["OK", "INCONCLUSIVO"]

def test_master_engine_inference_with_tw():
    engine = KaldraMasterEngineV2(d_ctx=128)
    
    embedding = np.random.randn(128)
    tw_window = np.random.randn(50, 20)
    
    signal = engine.infer_from_embedding(embedding, tw_window=tw_window)
    
    assert signal.tw_stats is not None
    assert isinstance(signal.tw_trigger, bool)
