from kaldra_engine.postprocessing import build_explanation


def test_build_explanation_runs():
    summary = {
        "archetype": "TEST",
        "tw_regime": "STABLE",
        "bias_score": 0.5,
    }
    result = build_explanation(summary)
    assert isinstance(result, str)
    assert "TEST" in result
    assert "STABLE" in result
