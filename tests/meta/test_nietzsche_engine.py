"""
Tests for NietzscheEngine-12.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from meta.nietzsche import analyze_meta, NietzscheProfile, MetaEngineResult


def test_analyze_meta_basic_structure():
    """Test that analyze_meta returns proper MetaEngineResult."""
    text = "We must overcome and dominate our challenges with strength."
    
    result = analyze_meta(text)
    
    assert isinstance(result, MetaEngineResult)
    assert isinstance(result.scores, dict)
    assert len(result.scores) == 12  # All 12 axes
    assert isinstance(result.dominant_axes, list)
    assert isinstance(result.severity, float)
    assert isinstance(result.notes, list)
    
    # All scores should be [0, 1]
    for score in result.scores.values():
        assert 0.0 <= score <= 1.0


def test_will_to_power_detected():
    """Test will to power detection."""
    text = "We will dominate the market, lead with power, and conquer all obstacles. Our strength will triumph."
    
    result = analyze_meta(text)
    
    assert result.scores["will_to_power"] > 0.5
    assert "will_to_power" in [ax[0] for ax in result.dominant_axes]


def test_resentment_detected():
    """Test resentment detection."""
    text = "It's so unfair. They don't deserve what they have. I'm the victim here. Why them and not me?"
    
    result = analyze_meta(text)
    
    assert result.scores["resentment"] > 0.5


def test_life_affirmation_vs_negation():
    """Test life affirmation detection."""
    text = "Yes to life! Embrace every moment with joy and vitality. Celebrate existence and thrive!"
    
    result = analyze_meta(text)
    
    assert result.scores["life_affirmation"] > result.scores["life_negation"]
    assert result.scores["life_affirmation"] > 0.4


def test_dionysian_vs_apollonian():
    """Test dionysian vs apollonian detection."""
    # Apollonian text
    text_order = "We need structure, order, and systematic organization. Harmony and balance are essential."
    result_order = analyze_meta(text_order)
    
    # Dionysian text
    text_chaos = "Wild chaos and primal passion! Embrace the frenzy and ecstasy of raw instinct!"
    result_chaos = analyze_meta(text_chaos)
    
    assert result_order.scores["apollonian_order"] > result_order.scores["dionysian_force"]
    assert result_chaos.scores["dionysian_force"] > result_chaos.scores["apollonian_order"]


def test_active_vs_passive_nihilism():
    """Test nihilism detection."""
    # Active nihilism
    text_active = "Tear down the old structures! Destroy and rebuild. Creative destruction is necessary."
    result_active = analyze_meta(text_active)
    
    # Passive nihilism
    text_passive = "Nothing matters anymore. Why bother? I'm just numb and indifferent to everything."
    result_passive = analyze_meta(text_passive)
    
    assert result_active.scores["active_nihilism"] > 0.4
    assert result_passive.scores["passive_nihilism"] > 0.4


def test_amor_fati_detection():
    """Test amor fati detection."""
    text = "I accept and embrace my fate. I love what is and wouldn't change a thing. It's perfect as is."
    
    result = analyze_meta(text)
    
    assert result.scores["amor_fati"] > 0.5


def test_dominant_axes_returns_top_3():
    """Test that dominant_axes returns top 3."""
    text = "Power, strength, and dominance are everything!"
    
    result = analyze_meta(text)
    
    assert len(result.dominant_axes) == 3
    assert all(isinstance(ax, tuple) and len(ax) == 2 for ax in result.dominant_axes)


def test_notes_generated():
    """Test that notes are generated."""
    text = "We must dominate with power!"
    
    result = analyze_meta(text)
    
    assert len(result.notes) > 0
    assert all(isinstance(note, str) for note in result.notes)
