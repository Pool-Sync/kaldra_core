"""
Integration tests for LLM to TWState Service.
"""

from src.kindras.scoring.llm_twstate_service import LLMToTWStateService


def test_llm_to_twstate_service_builds_twstate():
    """Test LLM to TWState service builds valid TWState."""
    service = LLMToTWStateService()
    text = "Earnings call narrative with high uncertainty and structural risk."
    context = {
        "country": "US",
        "sector": "energy",
        "media_tone": "analytical",
        "channel": "tv_news",
        "sentiment": "negative",
        "intensity": 0.7,
        "institutional_strength": 0.7,
        "power_concentration": 0.6,
        "regulatory_stability": 0.5,
    }

    tw_state = service.build_twstate_from_text(text=text, context=context)

    assert tw_state.plane3_cultural_macro
    assert tw_state.plane6_semiotic_media
    assert tw_state.plane9_structural_systemic
    assert isinstance(tw_state.metadata, dict)
    assert tw_state.metadata.get("source") == "llm_scoring_service"


def test_llm_to_twstate_service_includes_layer_metadata():
    """Test TWState includes metadata from all layers."""
    service = LLMToTWStateService()
    text = "Test narrative."
    context = {"country": "BR"}

    tw_state = service.build_twstate_from_text(text=text, context=context)

    assert "layers_meta" in tw_state.metadata
    assert 1 in tw_state.metadata["layers_meta"]
    assert 2 in tw_state.metadata["layers_meta"]
    assert 3 in tw_state.metadata["layers_meta"]
