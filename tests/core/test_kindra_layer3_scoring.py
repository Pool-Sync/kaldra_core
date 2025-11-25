"""
Tests for Kindra Layer 3 (Structural/Systemic) Scoring.

Tests rule-based scoring for institutional and structural context.
"""

from src.kindras.layer3_structural_systemic_scoring import KindraLayer3StructuralSystemicScoring


def test_layer3_scoring_high_institutional_strength_concentrated_power():
    """Test Layer 3 scoring with high institutional strength and concentrated power."""
    scorer = KindraLayer3StructuralSystemicScoring()
    context = {
        "institutional_strength": 0.9,
        "power_concentration": 0.8,
        "regulatory_stability": 0.7,
    }
    scores = scorer.score(context, {})

    # guardian / order axis
    assert "G21" in scores
    assert scores["G21"] > 0  # High institutional strength

    # hierarchy / control axis
    assert "P17" in scores
    assert scores["P17"] > 0  # High power concentration

    for v in scores.values():
        assert -1.0 <= v <= 1.0


def test_layer3_scoring_weak_institutions():
    """Test Layer 3 scoring with weak institutions."""
    scorer = KindraLayer3StructuralSystemicScoring()
    context = {
        "institutional_strength": 0.2,
        "power_concentration": 0.3,
        "regulatory_stability": 0.3,
    }
    scores = scorer.score(context, {})

    # Weak institutions
    assert "G21" in scores
    assert scores["G21"] < 0

    # Decentralized power
    assert "P17" in scores
    assert scores["P17"] < 0

    # High structural risk
    assert "R33" in scores
    assert scores["R33"] > 0

    for v in scores.values():
        assert -1.0 <= v <= 1.0


def test_layer3_scoring_stable_regulations():
    """Test Layer 3 scoring with stable regulations."""
    scorer = KindraLayer3StructuralSystemicScoring()
    context = {
        "regulatory_stability": 0.9,
    }
    scores = scorer.score(context, {})

    # Stable regulations reduce structural risk
    assert "R33" in scores
    assert scores["R33"] < 0

    for v in scores.values():
        assert -1.0 <= v <= 1.0
