"""
Integration tests for Kindra Scoring to TWState adapter.
"""

from src.kindras.scoring.twstate_adapter import build_twstate_from_context


def test_build_twstate_from_context_shapes_planes():
    """Test that TWState adapter creates proper plane structure."""
    context = {
        "country": "BR",
        "sector": "tech",
        "media_tone": "sensational",
        "channel": "social",
        "sentiment": "negative",
        "intensity": 0.9,
        "institutional_strength": 0.9,  # High to trigger G21
        "power_concentration": 0.8,     # High to trigger P17
        "regulatory_stability": 0.2,    # Low to trigger R33
    }

    tw_state = build_twstate_from_context(context)

    assert isinstance(tw_state.plane3_cultural_macro, dict)
    assert isinstance(tw_state.plane6_semiotic_media, dict)
    assert isinstance(tw_state.plane9_structural_systemic, dict)

    assert tw_state.plane3_cultural_macro  # non-empty
    assert tw_state.plane6_semiotic_media  # non-empty
    assert tw_state.plane9_structural_systemic  # non-empty


def test_build_twstate_includes_metadata():
    """Test that TWState includes metadata from adapter."""
    context = {"country": "US"}

    tw_state = build_twstate_from_context(context)

    assert tw_state.metadata is not None
    assert "source" in tw_state.metadata
    assert tw_state.metadata["source"] == "kindra_rule_engine"
