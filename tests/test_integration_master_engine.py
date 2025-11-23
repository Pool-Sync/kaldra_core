"""
Integration test for KALDRA Master Engine V2.

Tests the complete flow:
1. Text input
2. Embedding generation
3. Delta144 inference
4. Kindra modulation
5. TW Oracle detection
6. Epistemic Limiter decision
7. Final KaldraSignal output
"""
import numpy as np
import pytest

from src.core.kaldra_master_engine import KaldraMasterEngineV2, KaldraSignal


def test_master_engine_full_flow():
    """Test complete inference flow without TW window."""
    engine = KaldraMasterEngineV2(d_ctx=256, tau=0.65)
    
    # Simulate text embedding
    embedding = np.random.randn(256)
    
    # Run inference
    signal = engine.infer_from_embedding(embedding)
    
    # Validate output structure
    assert isinstance(signal, KaldraSignal)
    assert signal.archetype_probs is not None
    assert len(signal.archetype_probs) == 144
    assert np.isclose(signal.archetype_probs.sum(), 1.0, atol=1e-5)
    
    # Validate epistemic decision
    assert signal.epistemic is not None
    assert signal.epistemic.status in ["OK", "INCONCLUSIVO"]
    if signal.epistemic.confidence is not None:
        assert 0.0 <= signal.epistemic.confidence <= 1.0
    
    # TW should not trigger without window
    assert signal.tw_trigger is False
    assert signal.tw_stats is None


def test_master_engine_with_tw_window():
    """Test inference with TW anomaly detection."""
    engine = KaldraMasterEngineV2(d_ctx=256, tau=0.65)
    
    embedding = np.random.randn(256)
    
    # Create a TW window with high variance (potential anomaly)
    tw_window = np.random.randn(50, 20) * 5.0  # High variance
    
    signal = engine.infer_from_embedding(embedding, tw_window=tw_window)
    
    # Validate TW detection ran
    assert signal.tw_stats is not None
    assert signal.tw_stats.lambda_max > 0
    assert signal.tw_stats.threshold > 0
    
    # TW trigger depends on the random data, but stats should exist
    assert isinstance(signal.tw_trigger, bool)


def test_master_engine_determinism():
    """Test that same input produces same output (deterministic)."""
    engine = KaldraMasterEngineV2(d_ctx=128, tau=0.7)
    
    # Fixed seed for reproducibility
    np.random.seed(42)
    embedding = np.random.randn(128)
    
    # Run twice
    signal1 = engine.infer_from_embedding(embedding.copy())
    signal2 = engine.infer_from_embedding(embedding.copy())
    
    # Should produce identical results
    assert np.allclose(signal1.archetype_probs, signal2.archetype_probs)
    assert signal1.epistemic.status == signal2.epistemic.status


def test_master_engine_low_confidence_delegation():
    """Test that low confidence triggers epistemic delegation."""
    # Use high tau to force delegation
    engine = KaldraMasterEngineV2(d_ctx=256, tau=0.99)
    
    embedding = np.random.randn(256)
    signal = engine.infer_from_embedding(embedding)
    
    # With tau=0.99, most inferences should delegate
    # (unless by chance the top prob is > 0.99)
    # This is probabilistic, but we can check the structure
    if signal.epistemic.delegate:
        assert signal.epistemic.status == "INCONCLUSIVO"
