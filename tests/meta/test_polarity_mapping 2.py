"""
Test polarity mapping functionality.

v2.7: Tests for extract_polarity_scores() from meta-engines.
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.archetypes.polarity_mapping import extract_polarity_scores


def test_extract_polarity_scores_nietzsche():
    """Test extraction from Nietzsche engine results."""
    meta_results = {
        "nietzsche": {
            "scores": {
                "will_to_power": 0.9,
                "dionysian_force": 0.8,  # Should map to low ORDER (high CHAOS)
                "nihilism": 0.2          # Should map to high MEANING
            }
        }
    }
    
    scores = extract_polarity_scores(meta_results)
    
    # Check Will to Power -> Dominance
    assert "POL_DOMINANCE_SERVICE" in scores
    assert scores["POL_DOMINANCE_SERVICE"] == 0.9
    
    # Check Dionysian -> Order/Chaos
    # Dionysian is -1 direction for ORDER_CHAOS. So 0.8 -> 0.2 Order (High Chaos)
    assert "POL_ORDER_CHAOS" in scores
    assert scores["POL_ORDER_CHAOS"] == pytest.approx(0.2)
    
    # Check Nihilism -> Meaning/Void
    # Nihilism is -1 direction for MEANING_VOID. So 0.2 -> 0.8 Meaning
    assert "POL_MEANING_VOID" in scores
    assert scores["POL_MEANING_VOID"] == pytest.approx(0.8)


def test_extract_polarity_scores_aurelius():
    """Test extraction from Aurelius engine results."""
    meta_results = {
        "aurelius": {
            "scores": {
                "serenity": 0.7,
                "control_dichotomy": 0.6
            }
        }
    }
    
    scores = extract_polarity_scores(meta_results)
    
    assert "POL_CALM_ANXIETY" in scores
    assert scores["POL_CALM_ANXIETY"] == 0.7
    
    assert "POL_CONTROL_SURRENDER" in scores
    assert scores["POL_CONTROL_SURRENDER"] == 0.6


def test_extract_polarity_scores_campbell():
    """Test extraction from Campbell engine results."""
    meta_results = {
        "campbell": {
            "stage": "belly_of_whale"
        }
    }
    
    scores = extract_polarity_scores(meta_results)
    
    # Belly of Whale -> Low Descent/Ascent (Descent), High Metanoia
    assert "POL_DESCENT_ASCENT" in scores
    assert scores["POL_DESCENT_ASCENT"] == 0.1
    
    assert "POL_METANOIA_STAGNATION" in scores
    assert scores["POL_METANOIA_STAGNATION"] == 0.8


def test_extract_polarity_scores_combined():
    """Test aggregation from multiple engines."""
    meta_results = {
        "nietzsche": {
            "scores": {
                "will_to_power": 0.8  # Dominance 0.8
            }
        },
        "campbell": {
            "stage": "apotheosis" # Light/Shadow 0.9
        }
    }
    
    scores = extract_polarity_scores(meta_results)
    
    assert scores["POL_DOMINANCE_SERVICE"] == 0.8
    assert scores["POL_LIGHT_SHADOW"] == 0.9


def test_extract_polarity_scores_empty():
    """Test with empty results."""
    scores = extract_polarity_scores({})
    assert scores == {}
