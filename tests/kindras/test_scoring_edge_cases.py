import pytest
import numpy as np
from src.core.kaldra_master_engine import KaldraMasterEngineV2

@pytest.fixture
def engine():
    return KaldraMasterEngineV2(d_ctx=256)

def test_empty_embedding(engine):
    """Test behavior with zero embedding."""
    emb = np.zeros(256, dtype=np.float32)
    result = engine.infer_from_embedding(emb)
    
    # Should not crash
    assert result is not None
    assert len(result.archetype_probs) == 144

def test_extreme_embedding_values(engine):
    """Test with very large embedding values."""
    emb = np.ones(256, dtype=np.float32) * 1000.0
    result = engine.infer_from_embedding(emb)
    
    # Should handle gracefully
    assert result is not None
    assert np.all(np.isfinite(result.archetype_probs))

def test_negative_embedding(engine):
    """Test with all-negative embedding."""
    emb = -np.ones(256, dtype=np.float32)
    result = engine.infer_from_embedding(emb)
    
    assert result is not None
    assert result.archetype_probs.sum() > 0.99
