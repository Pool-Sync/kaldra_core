import numpy as np

from kaldra_core.core.delta144 import infer_state, evaluate_sequence_stability


def test_infer_state_runs():
    vec = np.random.randn(144)
    result = infer_state(vec)
    assert "state_vector" in result
    assert "meta" in result


def test_evaluate_sequence_stability_runs():
    seq = [np.random.randn(144) for _ in range(5)]
    result = evaluate_sequence_stability(seq)
    assert "stability_score" in result
    assert 0.0 <= result["stability_score"] <= 1.0
