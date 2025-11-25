"""
Tests for Kindra Layer 1 Rules (Option B).
"""

from src.kindras.scoring.layer1_rules import KindraLayer1CulturalMacroRules


def test_layer1_scoring_brazil_tech():
    """Test Layer 1 scoring for Brazil + tech sector."""
    scorer = KindraLayer1CulturalMacroRules()
    context = {"country": "BR", "sector": "tech"}
    scores = scorer.score(context, {})

    assert "E01" in scores
    assert "P17" in scores
    assert "T25" in scores

    for v in scores.values():
        assert -1.0 <= v <= 1.0


def test_layer1_scoring_germany_industrial():
    """Test Layer 1 scoring for Germany + industrial sector."""
    scorer = KindraLayer1CulturalMacroRules()
    context = {"country": "DE", "sector": "industrial"}
    scores = scorer.score(context, {})

    assert "T25" in scores
    for v in scores.values():
        assert -1.0 <= v <= 1.0


def test_layer1_scoring_china():
    """Test Layer 1 scoring for China."""
    scorer = KindraLayer1CulturalMacroRules()
    context = {"country": "CN"}
    scores = scorer.score(context, {})

    # China has high hierarchy
    assert "P17" in scores
    assert scores["P17"] > 0

    for v in scores.values():
        assert -1.0 <= v <= 1.0
