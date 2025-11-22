from src.apps.alpha.analyzer import analyze_earnings_call


def test_analyze_earnings_call_runs():
    result = analyze_earnings_call("Q3 earnings exceeded expectations")
    assert "archetype" in result
    assert "bias_score" in result
    assert "confidence" in result
