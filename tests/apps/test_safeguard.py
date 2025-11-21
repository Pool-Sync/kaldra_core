from apps.safeguard.narrative_guard import evaluate_narrative_risk
from apps.safeguard.bias_monitor import monitor_bias_over_texts


def test_evaluate_narrative_risk_runs():
    result = evaluate_narrative_risk("Test text")
    assert "narrative_risk" in result
    assert result["narrative_risk"] in ["low", "medium", "high"]


def test_monitor_bias_over_texts_runs():
    texts = ["text1", "text2", "text3"]
    results = monitor_bias_over_texts(texts)
    assert len(results) == 3
    assert all("bias_score" in r for r in results)
