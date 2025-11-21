import numpy as np

from core.tw369 import compute_tw_instability_index, compute_drift_metrics


def test_compute_tw_instability_index_runs():
    vec = np.random.randn(144)
    result = compute_tw_instability_index(vec)
    assert isinstance(result, float)
    assert 0.0 <= result <= 1.0


def test_compute_drift_metrics_runs():
    vec_t = np.random.randn(144)
    vec_t1 = np.random.randn(144)
    result = compute_drift_metrics(vec_t, vec_t1)
    assert "l2_drift" in result
    assert "cosine_drift" in result
    assert "temporal_drift" in result
