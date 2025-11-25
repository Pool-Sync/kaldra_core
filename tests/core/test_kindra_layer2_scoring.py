"""
Tests for Kindra Layer 2 (Semiotic/Media) Scoring.

Tests rule-based scoring for media tone, channel, and sentiment.
"""

from src.kindras.layer2_semiotic_media_scoring import KindraLayer2SemioticMediaScoring


def test_layer2_scoring_sensational_social_negative_high_intensity():
    """Test Layer 2 scoring with sensational tone, social media, negative sentiment, high intensity."""
    scorer = KindraLayer2SemioticMediaScoring()
    context = {
        "media_tone": "sensational",
        "channel": "social",
        "sentiment": "negative",
        "intensity": 0.9,
    }
    scores = scorer.score(context, {})

    assert "M12" in scores  # sensationalism
    assert "S09" in scores  # semiotic tension

    # All scores should be clamped
    for v in scores.values():
        assert -1.0 <= v <= 1.0


def test_layer2_scoring_analytical_print():
    """Test Layer 2 scoring with analytical tone and print media."""
    scorer = KindraLayer2SemioticMediaScoring()
    context = {
        "media_tone": "analytical",
        "channel": "newspaper",
    }
    scores = scorer.score(context, {})

    # Analytical should reduce sensationalism
    if "M12" in scores:
        assert scores["M12"] <= 0

    for v in scores.values():
        assert -1.0 <= v <= 1.0


def test_layer2_scoring_positive_sentiment():
    """Test Layer 2 scoring with positive sentiment."""
    scorer = KindraLayer2SemioticMediaScoring()
    context = {
        "sentiment": "positive",
        "intensity": 0.5,
    }
    scores = scorer.score(context, {})

    # Positive sentiment should affect expressiveness
    if "E01" in scores:
        assert scores["E01"] > 0

    for v in scores.values():
        assert -1.0 <= v <= 1.0


def test_layer2_scoring_high_intensity():
    """Test Layer 2 scoring with very high intensity."""
    scorer = KindraLayer2SemioticMediaScoring()
    context = {
        "intensity": 0.8,
    }
    scores = scorer.score(context, {})

    # High intensity should boost semiotic tension
    assert "S09" in scores
    assert scores["S09"] > 0

    for v in scores.values():
        assert -1.0 <= v <= 1.0
