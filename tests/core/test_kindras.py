import numpy as np

from core.kindras import infer_kindra_distribution


def test_infer_kindra_distribution_runs():
    vec = np.ones(48, dtype=float)
    result = infer_kindra_distribution(vec)
    assert "distribution" in result
    assert "labels" in result


def test_infer_kindra_distribution_output_format():
    vec = np.random.randn(48)
    result = infer_kindra_distribution(vec)
    assert isinstance(result["distribution"], dict)
    assert isinstance(result["labels"], list)
