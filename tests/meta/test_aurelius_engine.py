"""
Tests for AureliusEngine-12.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from meta.aurelius import analyze_meta, AureliusProfile, MetaEngineResult


def test_analyze_meta_basic_structure():
    """Test that analyze_meta returns proper MetaEngineResult."""
    text = "We must act with duty and responsibility, maintaining our principles."
    
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


def test_serenity_high_in_calm_text():
    """Test serenity detection in calm text."""
    text = "I remain peaceful and tranquil. Calm and serene, at peace with everything."
    
    result = analyze_meta(text)
    
    assert result.scores["serenity"] > 0.5


def test_emotional_regulation_vs_reactivity():
    """Test emotional regulation vs reactivity."""
    # Regulated text
    text_calm = "I will pause, reflect, and respond with measured calm and composure."
    result_calm = analyze_meta(text_calm)
    
    # Reactive text
    text_reactive = "I'm outraged! This is a catastrophe! Absolutely devastating and terrible!"
    result_reactive = analyze_meta(text_reactive)
    
    assert result_calm.scores["emotional_regulation"] > result_reactive.scores["emotional_regulation"]
    assert result_reactive.scores["emotional_regulation"] < 0.3


def test_control_dichotomy_detected():
    """Test control dichotomy awareness."""
    text = "This is in my control, but that is not. I focus on what depends on me and let go of what doesn't."
    
    result = analyze_meta(text)
    
    assert result.scores["control_dichotomy"] > 0.5


def test_premeditatio_malorum_detected():
    """Test negative visualization detection."""
    text = "If it fails, we'll prepare for the worst case. Anticipate obstacles and have contingency plans ready."
    
    result = analyze_meta(text)
    
    assert result.scores["premeditatio_malorum"] > 0.4


def test_desire_restraint_vs_excess():
    """Test desire restraint detection."""
    # Restrained text
    text_restrained = "Enough is sufficient. We need moderate and temperate limits, not excess."
    result_restrained = analyze_meta(text_restrained)
    
    # Excessive text
    text_excess = "More and more! Never enough! Insatiable and unlimited desires!"
    result_excess = analyze_meta(text_excess)
    
    assert result_restrained.scores["desire_restraint"] > result_excess.scores["desire_restraint"]


def test_character_integrity_detected():
    """Test character integrity detection."""
    text = "We must maintain our character, honor our values, and stay true to our principles and virtue."
    
    result = analyze_meta(text)
    
    assert result.scores["character_integrity"] > 0.5


def test_self_mastery_detected():
    """Test self-mastery detection."""
    text = "I have self-control and master myself. Unmoved by externals, centered and grounded in inner strength."
    
    result = analyze_meta(text)
    
    assert result.scores["self_mastery"] > 0.5


def test_low_alignment_in_chaotic_text():
    """Test low Stoic alignment in chaotic text."""
    text = "Everything is terrible! I'm panicked and furious! This is a disaster!"
    
    result = analyze_meta(text)
    
    # Overall alignment should be low
    assert result.severity < 0.4


def test_high_alignment_in_stoic_text():
    """Test high Stoic alignment."""
    text = """I accept what I cannot control with calm discipline. 
    Acting with duty and right action, I maintain steady emotional regulation. 
    My character and integrity guide me. I practice self-mastery and remain serene, 
    composed, and balanced. This is within my power, that is not."""
    
    result = analyze_meta(text)
    
    # Overall alignment should be moderate to high
    assert result.severity > 0.3, f"Expected alignment > 0.3, got {result.severity}"


def test_dominant_axes_returns_top_3():
    """Test that dominant_axes returns top 3."""
    text = "Duty, responsibility, and right action guide everything."
    
    result = analyze_meta(text)
    
    assert len(result.dominant_axes) == 3
    assert all(isinstance(ax, tuple) and len(ax) == 2 for ax in result.dominant_axes)


def test_notes_generated():
    """Test that notes are generated."""
    text = "We must act with discipline and honor."
    
    result = analyze_meta(text)
    
    assert len(result.notes) > 0
    assert all(isinstance(note, str) for note in result.notes)
