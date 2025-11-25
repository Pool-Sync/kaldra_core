"""
Tests for LLM Scoring Service.
"""

from src.kindras.scoring.llm_scoring_service import LLMScoringService


def test_llm_scoring_service_score_all_layers():
    """Test LLM scoring service scoring all 3 layers."""
    service = LLMScoringService()
    text = "Narrative about a tech company operating in Brazil with regulatory uncertainty."
    context = {
        "country": "BR",
        "sector": "tech",
        "media_tone": "sensational",
        "channel": "social",
        "sentiment": "negative",
        "intensity": 0.8,
        "institutional_strength": 0.9,
        "power_concentration": 0.8,
        "regulatory_stability": 0.2,
    }

    results = service.score_all_layers(text=text, context=context)

    assert set(results.keys()) == {1, 2, 3}
    for layer, resp in results.items():
        assert resp.error is None
        for v in resp.scores.values():
            assert -1.0 <= v <= 1.0


def test_llm_scoring_service_score_single_layer():
    """Test LLM scoring service scoring a single layer."""
    service = LLMScoringService()
    text = "Tech innovation narrative."
    context = {"country": "US", "sector": "tech"}

    response = service.score_layer(
        layer=1,
        text=text,
        context=context,
        mode="kindra_layer1",
    )

    assert response.error is None
    assert isinstance(response.scores, dict)
    for v in response.scores.values():
        assert -1.0 <= v <= 1.0
