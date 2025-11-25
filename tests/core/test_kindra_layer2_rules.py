"""
Tests for Kindra Layer 2 Rules (Option B).
"""

from src.kindras.scoring.layer2_rules import KindraLayer2SemioticMediaRules


def test_layer2_scoring_sensational_social_negative_high_intensity():
    """Test Layer 2 scoring with sensational tone, social media, negative sentiment, high intensity."""
    scorer = KindraLayer2SemioticMediaRules()
    context = {
        "media_tone": "sensational",
        "channel": "social",
        "sentiment": "negative",
        "intensity": 0.9,
    }
    scores = scorer.score(context, {})

    assert "M12" in scores
    assert "S09" in scores
    for v in scores.values():
        assert -1.0 <= v <= 1.0


def test_layer2_scoring_podcast_opinionated():
    """Test Layer 2 scoring with podcast channel and opinionated tone."""
    scorer = KindraLayer2SemioticMediaRules()
    context = {
        "channel": "podcast",
        "media_tone": "opinionated",
    }
    scores = scorer.score(context, {})

    assert "T25" in scores or "S09" in scores
    for v in scores.values():
        assert -1.0 <= v <= 1.0
