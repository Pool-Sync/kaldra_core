"""
Tests for Dummy LLM Scoring Client.
"""

from src.kindras.scoring.llm_dummy_client import DummyLLMScoringClient
from src.kindras.scoring.llm_types import LLMScoringRequest


def test_dummy_llm_scoring_client_layer1_basic():
    """Test dummy LLM client with Layer 1 request."""
    client = DummyLLMScoringClient()
    request = LLMScoringRequest(
        layer=1,
        text="Sample text about a tech company in Brazil.",
        context={"country": "BR", "sector": "tech"},
        mode="kindra_layer1_v1",
    )

    response = client.score(request)

    assert response.error is None
    assert isinstance(response.scores, dict)
    assert response.metadata.get("backend") == "dummy_rule_based"
    assert response.metadata.get("layer") == 1

    # At least something should be scored for BR + tech
    assert response.scores
    for v in response.scores.values():
        assert -1.0 <= v <= 1.0


def test_dummy_llm_scoring_client_layer2():
    """Test dummy LLM client with Layer 2 request."""
    client = DummyLLMScoringClient()
    request = LLMScoringRequest(
        layer=2,
        text="Sensational news article.",
        context={"media_tone": "sensational", "channel": "social"},
        mode="kindra_layer2_v1",
    )

    response = client.score(request)

    assert response.error is None
    assert isinstance(response.scores, dict)
    for v in response.scores.values():
        assert -1.0 <= v <= 1.0


def test_dummy_llm_scoring_client_max_vectors():
    """Test dummy LLM client with max_vectors limit."""
    client = DummyLLMScoringClient()
    request = LLMScoringRequest(
        layer=1,
        text="Test text.",
        context={"country": "US", "sector": "finance"},
        mode="kindra",
        max_vectors=3,
    )

    response = client.score(request)

    assert response.error is None
    assert len(response.scores) <= 3
