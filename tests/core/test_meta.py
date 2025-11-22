import numpy as np

from src.meta import apply_meta_operators


def test_apply_meta_operators_runs():
    vec = np.random.randn(144)
    result = apply_meta_operators(vec)
    assert "strength" in result
    assert "journey" in result
    assert "discipline" in result


def test_meta_operators_output_shapes():
    vec = np.random.randn(144)
    result = apply_meta_operators(vec)
    assert result["strength"].shape == (144,)
    assert result["journey"].shape == (144,)
    assert result["discipline"].shape == (144,)
