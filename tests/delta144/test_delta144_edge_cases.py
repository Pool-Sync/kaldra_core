import pytest
import numpy as np
from src.archetypes.delta144_engine import Delta144Engine

@pytest.fixture
def delta144():
    return Delta144Engine.from_default_files(d_ctx=256)

def test_delta144_zero_embedding(delta144):
    """Test with zero embedding."""
    emb = np.zeros(256, dtype=np.float32)
    result = delta144.infer_from_vector(emb)
    
    # Should not crash
    assert result is not None

def test_delta144_random_embedding(delta144):
    """Test with random embedding."""
    emb = np.random.randn(256).astype(np.float32)
    result = delta144.infer_from_vector(emb)
    
    assert result is not None
    # Check that probs are valid if returned
    if result.probs is not None:
        assert len(result.probs) == 144
