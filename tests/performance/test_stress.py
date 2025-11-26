import pytest
import time
import numpy as np
from src.core.kaldra_master_engine import KaldraMasterEngineV2
from src.tw369.tw369_integration import TW369Integrator, TWState

@pytest.fixture
def engine():
    return KaldraMasterEngineV2(d_ctx=256)

@pytest.fixture
def tw369():
    return TW369Integrator()

@pytest.mark.slow
def test_stress_many_inferences(engine):
    """Stress test with many inference calls."""
    N = 100
    embeddings = [np.random.randn(256).astype(np.float32) for _ in range(N)]
    
    start_time = time.time()
    for emb in embeddings:
        result = engine.infer_from_embedding(emb)
        assert result is not None
        assert len(result.archetype_probs) == 144
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = total_time / N
    
    print(f"\nStress Test: {N} inferences in {total_time:.4f}s (Avg: {avg_time:.4f}s)")
    
    # Conservative assertion: should process 100 items in under 30 seconds
    assert total_time < 30.0

@pytest.mark.slow
def test_stress_tw369_drift_evolution(tw369):
    """Stress test TW369 drift calculation over many steps."""
    steps = 500
    
    # Create initial state
    tw_state = TWState(
        plane3_cultural_macro={"E01": 0.5},
        plane6_semiotic_media={"S01": 0.3},
        plane9_structural_systemic={"T01": -0.2}
    )
    
    start_time = time.time()
    for _ in range(steps):
        drift = tw369.compute_drift(tw_state)
        
        # Verify no NaN or Inf in any drift values
        for key, val in drift.items():
            assert not np.isnan(val)
            assert not np.isinf(val)
        
        # Update state slightly (use first drift value)
        first_drift = list(drift.values())[0] if drift else 0.0
        tw_state.metadata = {"last_drift": first_drift}
        
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nTW369 Drift Stress: {steps} steps in {total_time:.4f}s")
    
    # Conservative bound: 500 steps should run in less than 10s
    assert total_time < 10.0

@pytest.mark.slow  
def test_stress_batch_processing(engine):
    """Stress test batch processing."""
    N = 50
    embeddings = [np.random.randn(256).astype(np.float32) for _ in range(N)]
    
    start_time = time.time()
    results = []
    for emb in embeddings:
        result = engine.infer_from_embedding(emb)
        results.append(result)
        assert result.archetype_probs.sum() > 0.99  # Valid probability distribution
        
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / N
    
    print(f"\nBatch Processing Stress: {N} items in {total_time:.4f}s (Avg: {avg_time:.4f}s)")
    
    # Conservative assertion: Avg time < 1s per item
    assert avg_time < 1.0
