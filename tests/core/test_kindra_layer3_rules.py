"""
Tests for Kindra Layer 3 Rules (Option B).
"""

from src.kindras.scoring.layer3_rules import KindraLayer3StructuralSystemicRules


def test_layer3_scoring_high_institutional_strength_concentrated_power():
    """Test Layer 3 scoring with high institutional strength and concentrated power."""
    scorer = KindraLayer3StructuralSystemicRules()
    context = {
        "institutional_strength": 0.9,
        "power_concentration": 0.8,
        "regulatory_stability": 0.7,
    }
    scores = scorer.score(context, {})

    assert "G21" in scores
    assert "P17" in scores
    for v in scores.values():
        assert -1.0 <= v <= 1.0
