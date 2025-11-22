from src.apps.geo.geo_analyzer import analyze_geopolitical_text


def test_analyze_geopolitical_text_runs():
    result = analyze_geopolitical_text("Diplomatic tensions escalate")
    assert "archetype" in result
    assert "bias_score" in result
    assert "tw_regime" in result
