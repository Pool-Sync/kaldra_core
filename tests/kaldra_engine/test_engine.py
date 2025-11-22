from src.kaldra_engine.kaldra_engine import generate_kaldra_signal


def test_generate_kaldra_signal_minimal():
    sig = generate_kaldra_signal("texto de teste")
    for key in [
        "archetype",
        "delta_state",
        "tw_regime",
        "kindra_distribution",
        "bias_score",
        "meta_modifiers",
        "confidence",
        "explanation",
    ]:
        assert key in sig


def test_generate_kaldra_signal_ranges():
    sig = generate_kaldra_signal("test text")
    assert 0.0 <= sig["bias_score"] <= 1.0
    assert 0.0 <= sig["confidence"] <= 1.0
    assert sig["tw_regime"] in ["STABLE", "CRITICAL", "UNSTABLE"]
