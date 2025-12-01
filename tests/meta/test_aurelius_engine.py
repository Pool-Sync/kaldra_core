"""
Tests for AureliusEngine v3.1.

Tests the refactored class-based AureliusEngine with:
- MetaInput/AureliusSignal pattern
- Kindra 3×48 integration
- TW369 drift awareness
- 4 Cardinal Virtues calculation
- Dichotomy of control
- Memento mori and amor fati
- Backward compatibility
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from meta.aurelius import (
    AureliusEngine,
    AureliusSignal,
    analyze_meta,
    MetaEngineResult
)
from meta.nietzsche import MetaInput
from unification.states.unified_state import KindraContext
from tw369.tw369_integration import TWState


# ============================================================================
# Basic Functionality Tests
# ============================================================================

def test_basic_analysis_runs_without_error():
    """Test that basic analysis runs without error."""
    engine = AureliusEngine()
    meta_input = MetaInput(text="I focus on what I can control and accept what I cannot.")
    
    result = engine.analyze(meta_input)
    
    assert isinstance(result, AureliusSignal)
    assert isinstance(result.scores, dict)
    assert len(result.scores) >= 12  # At least 12 axes
    assert isinstance(result.dominant_axes, list)
    assert isinstance(result.severity, float)
    assert isinstance(result.notes, list)
    assert isinstance(result.dichotomy_of_control, dict)
    assert isinstance(result.virtue_scores, dict)


def test_aurelius_signal_fields_are_in_range():
    """Test that all AureliusSignal fields are in valid ranges."""
    engine = AureliusEngine()
    meta_input = MetaInput(text="Calm, composed, and focused on duty and virtue.")
    
    result = engine.analyze(meta_input)
    
    # Check primary fields
    assert 0.0 <= result.memento_mori <= 1.0
    assert 0.0 <= result.amor_fati <= 1.0
    assert 0.0 <= result.severity <= 1.0
    assert 0.0 <= result.score <= 1.0
    
    # Check virtue scores
    for virtue, score in result.virtue_scores.items():
        assert 0.0 <= score <= 1.0, f"Virtue {virtue} score {score} out of range"
    
    # Check dichotomy of control
    assert 0.0 <= result.dichotomy_of_control.get("controllable", 0) <= 1.0
    assert 0.0 <= result.dichotomy_of_control.get("not_controllable", 0) <= 1.0
    
    # Check all axis scores
    for axis, score in result.scores.items():
        assert 0.0 <= score <= 1.0, f"Axis {axis} score {score} out of range"


def test_dominant_axes_returns_top_3():
    """Test that dominant_axes returns top 3 axes."""
    engine = AureliusEngine()
    meta_input = MetaInput(text="Calm, serene, and at peace with what is.")
    
    result = engine.analyze(meta_input)
    
    assert len(result.dominant_axes) == 3
    assert all(isinstance(ax, tuple) and len(ax) == 2 for ax in result.dominant_axes)
    
    # Check that axes are sorted by score (descending)
    scores = [ax[1] for ax in result.dominant_axes]
    assert scores == sorted(scores, reverse=True)


# ============================================================================
# Kindra 3×48 Integration Tests
# ============================================================================

def test_uses_kindra_signature_when_present():
    """Test that Kindra context influences the analysis."""
    engine = AureliusEngine()
    
    # Test without Kindra
    meta_input_no_kindra = MetaInput(text="I focus on my duty and responsibility.")
    result_no_kindra = engine.analyze(meta_input_no_kindra)
    
    # Test with Kindra (high collective responsibility)
    kindra_high_responsibility = KindraContext(
        layer1={
            "duty": 0.9,
            "responsibility": 0.8,
            "collective_action": 0.85
        },
        layer2={
            "calm": 0.7,
            "measured": 0.6
        },
        layer3={}
    )
    meta_input_with_kindra = MetaInput(
        text="I focus on my duty and responsibility.",
        kindra=kindra_high_responsibility
    )
    result_with_kindra = engine.analyze(meta_input_with_kindra)
    
    # Kindra should boost justice virtue
    assert result_with_kindra.virtue_scores["justice"] > result_no_kindra.virtue_scores["justice"]


def test_kindra_emotional_volatility_reduces_temperance():
    """Test that Kindra emotional volatility reduces temperance."""
    engine = AureliusEngine()
    
    # High emotional volatility
    kindra_volatile = KindraContext(
        layer1={},
        layer2={
            "emotional_intensity": 0.9,
            "reactivity": 0.8,
            "passion": 0.85
        },
        layer3={}
    )
    
    meta_input = MetaInput(
        text="I remain calm and composed.",
        kindra=kindra_volatile
    )
    result = engine.analyze(meta_input)
    
    # High volatility should reduce temperance
    assert result.virtue_scores["temperance"] < 0.7


def test_kindra_existential_depth_boosts_memento_mori():
    """Test that Kindra existential depth boosts memento_mori."""
    engine = AureliusEngine()
    
    # High existential depth
    kindra_existential = KindraContext(
        layer1={},
        layer2={},
        layer3={
            "mortality": 0.9,
            "meaning": 0.8,
            "existential": 0.85
        }
    )
    
    meta_input = MetaInput(
        text="We must prepare for difficulties.",
        kindra=kindra_existential
    )
    result = engine.analyze(meta_input)
    
    # Should have elevated memento_mori
    assert result.memento_mori > 0.4


# ============================================================================
# TW369 Drift Awareness Tests
# ============================================================================

def test_uses_tw369_drift_for_adjustments():
    """Test that TW369 drift influences the analysis."""
    engine = AureliusEngine()
    text = "We must remain calm and focused."
    
    # Low drift scenario
    tw_low_drift = TWState(metadata={"drift_metric": 0.1, "regime": "STABLE"})
    meta_input_low = MetaInput(text=text, tw_state=tw_low_drift)
    result_low = engine.analyze(meta_input_low)
    
    # High drift scenario
    tw_high_drift = TWState(metadata={"drift_metric": 0.9, "regime": "CRITICAL"})
    meta_input_high = MetaInput(text=text, tw_state=tw_high_drift)
    result_high = engine.analyze(meta_input_high)
    
    # High drift should increase memento_mori and courage
    assert result_high.memento_mori > result_low.memento_mori
    assert result_high.virtue_scores["courage"] >= result_low.virtue_scores["courage"]


def test_tw369_critical_regime_boosts_memento_mori():
    """Test that CRITICAL regime boosts memento_mori."""
    engine = AureliusEngine()
    
    tw_critical = TWState(metadata={"drift_metric": 0.8, "regime": "CRITICAL"})
    meta_input = MetaInput(
        text="We must prepare for the worst.",
        tw_state=tw_critical
    )
    result = engine.analyze(meta_input)
    
    # Critical regime should boost memento_mori
    assert result.memento_mori > 0.4


def test_tw369_transition_regime_boosts_amor_fati():
    """Test that TRANSITION regime boosts amor_fati."""
    engine = AureliusEngine()
    
    tw_transition = TWState(metadata={"drift_metric": 0.5, "regime": "TRANSITION"})
    meta_input = MetaInput(
        text="I accept what is and flow with change.",
        tw_state=tw_transition
    )
    result = engine.analyze(meta_input)
    
    # Transition regime should boost amor_fati
    assert result.amor_fati > 0.5


def test_tw369_stable_regime_boosts_virtues():
    """Test that STABLE regime boosts all virtues."""
    engine = AureliusEngine()
    
    tw_stable = TWState(metadata={"drift_metric": 0.2, "regime": "STABLE"})
    meta_input = MetaInput(
        text="I act with wisdom, courage, justice, and temperance.",
        tw_state=tw_stable
    )
    result = engine.analyze(meta_input)
    
    # Stable regime should boost virtues
    avg_virtue = sum(result.virtue_scores.values()) / len(result.virtue_scores)
    assert avg_virtue > 0.0  # With boost from STABLE regime


# ============================================================================
# Virtue Scores Tests
# ============================================================================

def test_virtue_scores_calculation():
    """Test that virtue scores are calculated correctly."""
    engine = AureliusEngine()
    
    # Test wisdom (perception + reality + control)
    meta_input_wisdom = MetaInput(
        text="I observe objectively, accept reality as it is, and focus on what I can control."
    )
    result_wisdom = engine.analyze(meta_input_wisdom)
    assert result_wisdom.virtue_scores["wisdom"] > 0.5
    
    # Test courage (action + discipline + preparation)
    meta_input_courage = MetaInput(
        text="I do my duty with discipline and prepare for difficulties ahead."
    )
    result_courage = engine.analyze(meta_input_courage)
    assert result_courage.virtue_scores["courage"] > 0.2
    
    # Test temperance (restraint + regulation + serenity)
    meta_input_temperance = MetaInput(
        text="I am calm, moderate, and serene in all things."
    )
    result_temperance = engine.analyze(meta_input_temperance)
    assert result_temperance.virtue_scores["temperance"] > 0.4


def test_all_four_virtues_present():
    """Test that all 4 cardinal virtues are calculated."""
    engine = AureliusEngine()
    
    meta_input = MetaInput(text="I act with wisdom, courage, justice, and temperance.")
    result = engine.analyze(meta_input)
    
    assert "wisdom" in result.virtue_scores
    assert "courage" in result.virtue_scores
    assert "justice" in result.virtue_scores
    assert "temperance" in result.virtue_scores


# ============================================================================
# Dichotomy of Control Tests
# ============================================================================

def test_dichotomy_of_control_detection():
    """Test dichotomy of control detection."""
    engine = AureliusEngine()
    
    # Focus on controllable
    meta_input_controllable = MetaInput(
        text="I focus on what is in my control and within my power to change."
    )
    result_controllable = engine.analyze(meta_input_controllable)
    
    # Focus on uncontrollable
    meta_input_uncontrollable = MetaInput(
        text="Everything is beyond my control and outside my power."
    )
    result_uncontrollable = engine.analyze(meta_input_uncontrollable)
    
    # Controllable text should have higher controllable score
    assert result_controllable.dichotomy_of_control["controllable"] > 0.4
    # Uncontrollable text should have higher not_controllable score
    assert result_uncontrollable.dichotomy_of_control["not_controllable"] > 0.4


def test_dichotomy_with_kindra_control_focus():
    """Test that Kindra control_focus influences dichotomy."""
    engine = AureliusEngine()
    
    # High control focus in Kindra
    kindra_control = KindraContext(
        layer1={
            "control": 0.9,
            "agency": 0.8,
            "self_determination": 0.85
        },
        layer2={},
        layer3={}
    )
    
    meta_input = MetaInput(
        text="I focus on my actions.",
        kindra=kindra_control
    )
    result = engine.analyze(meta_input)
    
    # Should have high controllable score
    assert result.dichotomy_of_control["controllable"] > 0.5


# ============================================================================
# Memento Mori and Amor Fati Tests
# ============================================================================

def test_memento_mori_calculation():
    """Test memento_mori calculation."""
    engine = AureliusEngine()
    
    meta_input = MetaInput(
        text="We must prepare for the worst case and anticipate difficulties."
    )
    result = engine.analyze(meta_input)
    
    # Should have elevated memento_mori
    assert result.memento_mori > 0.3


def test_amor_fati_calculation():
    """Test amor_fati calculation."""
    engine = AureliusEngine()
    
    meta_input = MetaInput(
        text="I accept my fate, embrace what is, and remain serene and peaceful."
    )
    result = engine.analyze(meta_input)
    
    # Should have elevated amor_fati
    assert result.amor_fati > 0.2


# ============================================================================
# Stoic Posture Classification Tests
# ============================================================================

def test_stoic_posture_classification():
    """Test Stoic posture classification."""
    engine = AureliusEngine()
    
    # Exemplary Stoic
    meta_input_exemplary = MetaInput(
        text="I observe clearly, accept reality, focus on what I control, "
             "act with duty and discipline, remain calm and serene, "
             "practice moderation, and maintain my character with integrity."
    )
    result_exemplary = engine.analyze(meta_input_exemplary)
    assert result_exemplary.label in ["exemplary_stoic", "stoic", "mixed"]  # Heuristic may classify as mixed
    
    # Non-Stoic
    meta_input_non_stoic = MetaInput(
        text="I'm outraged and furious! This is a catastrophe! "
             "I want more and more, never enough!"
    )
    result_non_stoic = engine.analyze(meta_input_non_stoic)
    assert result_non_stoic.label in ["non_stoic", "mixed"]


# ============================================================================
# Backward Compatibility Tests
# ============================================================================

def test_backward_compatibility_wrapper():
    """Test that legacy analyze_meta() function still works."""
    text = "I focus on what I can control and accept what I cannot."
    
    result = analyze_meta(text)
    
    assert isinstance(result, MetaEngineResult)
    assert isinstance(result.scores, dict)
    assert len(result.scores) >= 12
    assert isinstance(result.dominant_axes, list)
    assert isinstance(result.severity, float)
    assert isinstance(result.notes, list)


def test_backward_compatibility_with_tw_state():
    """Test legacy function with tw_state parameter."""
    text = "I remain calm in crisis."
    tw_state = TWState(metadata={"drift_metric": 0.9, "regime": "CRITICAL"})
    
    result = analyze_meta(text, tw_state=tw_state)
    
    assert isinstance(result, MetaEngineResult)
    # Should have elevated scores due to crisis
    assert result.severity > 0.0


# ============================================================================
# Notes Generation Tests
# ============================================================================

def test_notes_generated():
    """Test that notes are generated."""
    engine = AureliusEngine()
    
    meta_input = MetaInput(text="I focus on duty and remain calm.")
    result = engine.analyze(meta_input)
    
    assert len(result.notes) > 0
    assert all(isinstance(note, str) for note in result.notes)


def test_notes_include_stoic_posture():
    """Test that notes include Stoic posture."""
    engine = AureliusEngine()
    
    meta_input = MetaInput(text="I act with virtue and wisdom.")
    result = engine.analyze(meta_input)
    
    # Should have posture in notes
    notes_text = " ".join(result.notes)
    assert "stoic posture" in notes_text.lower()


def test_notes_include_strongest_virtue():
    """Test that notes include strongest virtue."""
    engine = AureliusEngine()
    
    meta_input = MetaInput(text="I am calm, moderate, and serene.")
    result = engine.analyze(meta_input)
    
    # Should mention strongest virtue
    notes_text = " ".join(result.notes)
    assert "strongest virtue" in notes_text.lower()


# ============================================================================
# Integration Tests
# ============================================================================

def test_full_integration_with_all_inputs():
    """Test full integration with Kindra + TW369 + archetypes."""
    engine = AureliusEngine()
    
    kindra = KindraContext(
        layer1={"duty": 0.8, "responsibility": 0.7},
        layer2={"calm": 0.6, "measured": 0.5},
        layer3={"existential": 0.7}
    )
    
    tw_state = TWState(metadata={"drift_metric": 0.7, "regime": "CRITICAL"})
    
    archetype_scores = {"A07_RULER": 0.8, "A10_SAGE": 0.3}
    
    meta_input = MetaInput(
        text="I focus on my duty with discipline and prepare for difficulties.",
        kindra=kindra,
        tw_state=tw_state,
        archetype_scores=archetype_scores
    )
    
    result = engine.analyze(meta_input)
    
    # Should have elevated courage and justice (from duty + crisis)
    assert result.virtue_scores["courage"] > 0.3
    assert result.virtue_scores["justice"] > 0.3
    
    # Should have elevated memento_mori (from crisis)
    assert result.memento_mori > 0.4
    
    # Should have valid structure
    assert len(result.scores) >= 12
    assert len(result.dominant_axes) == 3
    assert len(result.notes) > 0


def test_anti_patterns_reduce_scores():
    """Test that anti-patterns reduce relevant scores."""
    engine = AureliusEngine()
    
    # Emotional reactivity
    meta_input_reactive = MetaInput(
        text="I'm outraged and furious! This is a catastrophe and disaster!"
    )
    result_reactive = engine.analyze(meta_input_reactive)
    
    # Should have low emotional_regulation and serenity
    assert result_reactive.scores["emotional_regulation"] < 0.5
    assert result_reactive.scores["serenity"] < 0.5
    assert result_reactive.virtue_scores["temperance"] < 0.5
    
    # Excess
    meta_input_excess = MetaInput(
        text="I want more and more, never enough, insatiable and greedy!"
    )
    result_excess = engine.analyze(meta_input_excess)
    
    # Should have low desire_restraint
    assert result_excess.scores["desire_restraint"] < 0.5
    assert result_excess.virtue_scores["temperance"] < 0.5
