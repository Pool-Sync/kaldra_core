"""
Tests for Kindra Layer 1 (Cultural Macro) Scoring.

Tests rule-based scoring for country and sector contexts.
"""

from src.kindras.layer1_cultural_macro_scoring import KindraLayer1CulturalMacroScoring


def test_layer1_scoring_brazil_tech():
    """Test Layer 1 scoring for Brazil + tech sector."""
    scorer = KindraLayer1CulturalMacroScoring()
    context = {"country": "BR", "sector": "tech"}
    scores = scorer.score(context, {})

    assert "E01" in scores  # expressiveness
    assert "P17" in scores  # hierarchy
    assert "T25" in scores  # innovation

    assert -1.0 <= scores["E01"] <= 1.0
    assert -1.0 <= scores["P17"] <= 1.0
    assert -1.0 <= scores["T25"] <= 1.0


def test_layer1_scoring_us_finance():
    """Test Layer 1 scoring for US + finance sector."""
    scorer = KindraLayer1CulturalMacroScoring()
    context = {"country": "US", "sector": "finance"}
    scores = scorer.score(context, {})

    assert "R33" in scores  # risk aversion
    assert "P17" in scores  # hierarchy

    # All scores should be clamped
    for value in scores.values():
        assert -1.0 <= value <= 1.0


def test_layer1_scoring_japan():
    """Test Layer 1 scoring for Japan."""
    scorer = KindraLayer1CulturalMacroScoring()
    context = {"country": "JP"}
    scores = scorer.score(context, {})

    assert "E01" in scores  # expressiveness (should be negative)
    assert "P17" in scores  # hierarchy (should be positive)

    # Japan has lower expressiveness
    assert scores["E01"] < 0

    # Japan has higher hierarchy
    assert scores["P17"] > 0


def test_layer1_scoring_with_baseline():
    """Test Layer 1 scoring with baseline vector scores."""
    scorer = KindraLayer1CulturalMacroScoring()
    context = {"country": "IN"}
    baseline = {"E01": 0.2, "P17": 0.1}

    scores = scorer.score(context, baseline)

    # Scores should be modified from baseline
    assert scores["E01"] != baseline["E01"]
    assert scores["P17"] != baseline["P17"]

    # Still clamped
    for value in scores.values():
        assert -1.0 <= value <= 1.0
