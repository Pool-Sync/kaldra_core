"""
Tests for Kindra Scoring Dispatcher.

Tests orchestration of all 3 scoring layers.
"""

from src.kindras.scoring_dispatcher import KindraScoringDispatcher


def test_kindra_scoring_dispatcher_runs_all_layers():
    """Test that dispatcher runs all 3 layers and returns correct structure."""
    dispatcher = KindraScoringDispatcher()
    context = {
        "country": "BR",
        "sector": "tech",
        "media_tone": "sensational",
        "channel": "social",
        "sentiment": "negative",
        "intensity": 0.8,
        "institutional_strength": 0.6,
        "power_concentration": 0.5,
        "regulatory_stability": 0.4,
    }

    result = dispatcher.run_all(context, {})

    # Should have all 3 layers
    assert set(result.keys()) == {"layer1", "layer2", "layer3"}

    # Each layer should return dict of scores
    for layer_scores in result.values():
        assert isinstance(layer_scores, dict)
        for v in layer_scores.values():
            assert -1.0 <= v <= 1.0


def test_kindra_scoring_dispatcher_with_baseline():
    """Test dispatcher with baseline vector scores."""
    dispatcher = KindraScoringDispatcher()
    context = {"country": "US"}
    baseline = {"E01": 0.1, "P17": 0.2}

    result = dispatcher.run_all(context, baseline)

    assert "layer1" in result
    assert "layer2" in result
    assert "layer3" in result


def test_kindra_scoring_dispatcher_empty_context():
    """Test dispatcher with minimal context."""
    dispatcher = KindraScoringDispatcher()
    context = {}

    result = dispatcher.run_all(context, {})

    # Should still return all 3 layers
    assert len(result) == 3
