import pytest
import numpy as np
from src.core.kaldra_master_engine import KaldraMasterEngineV2, KaldraSignal

# Deterministic RNG for reproducible tests
RNG_SEED = 42
rng = np.random.default_rng(RNG_SEED)

@pytest.fixture
def engine():
    """Create a KaldraMasterEngineV2 instance for testing."""
    return KaldraMasterEngineV2(d_ctx=256, tau=0.65)

@pytest.fixture
def sample_embedding():
    """Create a deterministic sample embedding vector."""
    return rng.standard_normal(256, dtype=np.float32)

def test_full_pipeline_basic(engine, sample_embedding):
    """Test basic end-to-end pipeline execution."""
    result = engine.infer_from_embedding(sample_embedding)
    
    # Check result structure
    assert isinstance(result, KaldraSignal)
    assert result.archetype_probs is not None
    assert len(result.archetype_probs) == 144
    assert np.isclose(result.archetype_probs.sum(), 1.0, atol=0.01)
    
    # Check epistemic decision
    assert result.epistemic is not None
    assert hasattr(result.epistemic, 'status')
    assert result.epistemic.status in ["OK", "INCONCLUSIVO"]

def test_full_pipeline_with_tw_window(engine, sample_embedding):
    """Test pipeline with TW oracle window."""
    tw_window = rng.standard_normal((10, 5), dtype=np.float32)
    result = engine.infer_from_embedding(sample_embedding, tw_window=tw_window)
    
    assert isinstance(result, KaldraSignal)
    # TW trigger may or may not be activated
    assert isinstance(result.tw_trigger, bool)

def test_full_pipeline_tw_window_low_tension(engine, sample_embedding):
    """TW window with low-tension values should not produce pathological behavior."""
    # Small values around zero
    tw_window = np.zeros((10, 5), dtype=np.float32)
    result = engine.infer_from_embedding(sample_embedding, tw_window=tw_window)
    
    assert isinstance(result, KaldraSignal)
    assert isinstance(result.tw_trigger, bool)
    # Sanity: distribution remains valid
    assert result.archetype_probs.shape[0] == 144
    assert np.isclose(result.archetype_probs.sum(), 1.0, atol=0.01)

def test_full_pipeline_tw_window_high_tension(engine, sample_embedding):
    """TW window with high-tension values should stay numerically stable."""
    tw_window = np.full((10, 5), 5.0, dtype=np.float32)  # High artificial tension
    result = engine.infer_from_embedding(sample_embedding, tw_window=tw_window)
    
    assert isinstance(result, KaldraSignal)
    assert isinstance(result.tw_trigger, bool)
    # Check that it didn't explode
    assert np.all(np.isfinite(result.archetype_probs))
    assert np.all(result.archetype_probs >= 0)
    assert np.all(result.archetype_probs <= 1)
    assert np.isclose(result.archetype_probs.sum(), 1.0, atol=0.01)
    
def test_full_pipeline_determinism(engine, sample_embedding):
    """Verify deterministic behavior with same input."""
    result1 = engine.infer_from_embedding(sample_embedding)
    result2 = engine.infer_from_embedding(sample_embedding)
    
    # Results should be identical for same input
    np.testing.assert_array_almost_equal(result1.archetype_probs, result2.archetype_probs)
    assert result1.epistemic.status == result2.epistemic.status

def test_full_pipeline_different_inputs(engine):
    """Test that different inputs produce different outputs."""
    rng_local = np.random.default_rng(123)
    emb1 = rng_local.standard_normal(256, dtype=np.float32)
    emb2 = rng_local.standard_normal(256, dtype=np.float32)
    
    result1 = engine.infer_from_embedding(emb1)
    result2 = engine.infer_from_embedding(emb2)
    
    # Results should differ for different inputs
    assert not np.allclose(result1.archetype_probs, result2.archetype_probs)

def test_full_pipeline_probability_validity(engine, sample_embedding):
    """Test that output probabilities are valid."""
    result = engine.infer_from_embedding(sample_embedding)
    
    # All probabilities should be non-negative
    assert np.all(result.archetype_probs >= 0)
    # All probabilities should be <= 1
    assert np.all(result.archetype_probs <= 1)
    # Sum should be approximately 1
    assert np.isclose(result.archetype_probs.sum(), 1.0, atol=0.01)

def test_full_pipeline_delta_state(engine, sample_embedding):
    """Test that delta state is captured."""
    result = engine.infer_from_embedding(sample_embedding)
    
    assert result.delta_state is not None
    assert isinstance(result.delta_state, dict)
