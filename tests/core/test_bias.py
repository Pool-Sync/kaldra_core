from kaldra_core.core.bias import compute_bias_score_from_text, classify_bias


def test_compute_bias_score_from_text_runs():
    result = compute_bias_score_from_text("Test text")
    assert "bias_score" in result
    assert "features" in result
    assert 0.0 <= result["bias_score"] <= 1.0


def test_classify_bias_runs():
    label = classify_bias(0.5)
    assert label in ["neutral", "negative", "positive", "extreme"]


def test_bias_classification_thresholds():
    assert classify_bias(0.1) == "neutral"
    assert classify_bias(0.4) == "negative"
    assert classify_bias(0.7) == "positive"
    assert classify_bias(0.9) == "extreme"
