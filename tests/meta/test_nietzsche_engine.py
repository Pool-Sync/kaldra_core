"""
Tests for NietzscheEngine v3.1.

Tests the refactored class-based NietzscheEngine with:
- MetaInput/NietzscheSignal pattern
- Kindra 3×48 integration
- TW369 drift awareness
- Morality type classification
- Backward compatibility
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from meta.nietzsche import (
    NietzscheEngine,
    MetaInput,
    NietzscheSignal,
    analyze_meta,
    MetaEngineResult
)
from unification.states.unified_state import KindraContext
from tw369.tw369_integration import TWState


# ============================================================================
# Basic Functionality Tests
# ============================================================================

def test_basic_analysis_runs_without_error():
    """Test that basic analysis runs without error."""
    engine = NietzscheEngine()
    meta_input = MetaInput(text="We must overcome and dominate our challenges with strength.")
    
    result = engine.analyze(meta_input)
    
    assert isinstance(result, NietzscheSignal)
    assert isinstance(result.scores, dict)
    assert len(result.scores) == 12  # All 12 axes
    assert isinstance(result.dominant_axes, list)
    assert isinstance(result.severity, float)
    assert isinstance(result.notes, list)
    assert result.morality_type in ["master", "slave", "mixed"]


def test_nietzsche_signal_fields_are_in_range():
    """Test that all NietzscheSignal fields are in valid ranges."""
    engine = NietzscheEngine()
    meta_input = MetaInput(text="Power, strength, dominance, and control!")
    
    result = engine.analyze(meta_input)
    
    # Check primary fields
    assert 0.0 <= result.will_to_power <= 1.0
    assert 0.0 <= result.eternal_return <= 1.0
    assert 0.0 <= result.transcendence <= 1.0
    assert 0.0 <= result.severity <= 1.0
    assert 0.0 <= result.score <= 1.0
    
    # Check all axis scores
    for axis, score in result.scores.items():
        assert 0.0 <= score <= 1.0, f"Axis {axis} score {score} out of range"


def test_dominant_axes_returns_top_3():
    """Test that dominant_axes returns top 3 axes."""
    engine = NietzscheEngine()
    meta_input = MetaInput(text="Power, strength, and dominance are everything!")
    
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
    engine = NietzscheEngine()
    
    # Test without Kindra
    meta_input_no_kindra = MetaInput(text="We will dominate the market.")
    result_no_kindra = engine.analyze(meta_input_no_kindra)
    
    # Test with Kindra (high power climate)
    kindra_high_power = KindraContext(
        layer1={
            "power_dynamics": 0.9,
            "dominance": 0.8,
            "hierarchy": 0.7
        },
        layer2={
            "conflict": 0.6
        },
        layer3={
            "archetypal_hero": 0.7
        }
    )
    meta_input_with_kindra = MetaInput(
        text="We will dominate the market.",
        kindra=kindra_high_power
    )
    result_with_kindra = engine.analyze(meta_input_with_kindra)
    
    # Kindra should boost will_to_power
    assert result_with_kindra.will_to_power > result_no_kindra.will_to_power
    
    # Test with Kindra (high ressentiment)
    kindra_high_ressentiment = KindraContext(
        layer1={
            "victimhood": 0.9,
            "grievance": 0.8,
            "resentment": 0.7
        },
        layer2={
            "victim_narrative": 0.8,
            "injustice_framing": 0.7
        },
        layer3={}
    )
    meta_input_ressentiment = MetaInput(
        text="It's so unfair.",
        kindra=kindra_high_ressentiment
    )
    result_ressentiment = engine.analyze(meta_input_ressentiment)
    
    # Should have high resentment score
    assert result_ressentiment.scores["resentment"] > 0.5


def test_kindra_mythic_intensity_boosts_transcendence():
    """Test that Kindra mythic intensity boosts transcendence."""
    engine = NietzscheEngine()
    
    # High mythic intensity
    kindra_mythic = KindraContext(
        layer1={},
        layer2={},
        layer3={
            "archetypal_hero": 0.9,
            "mythic_pattern": 0.8,
            "universal_theme": 0.9,
            "transcendence": 0.85
        }
    )
    
    meta_input = MetaInput(
        text="We embrace our destiny with strength and wisdom.",
        kindra=kindra_mythic
    )
    result = engine.analyze(meta_input)
    
    # Should have elevated transcendence
    assert result.transcendence > 0.4


# ============================================================================
# TW369 Drift Awareness Tests
# ============================================================================

def test_uses_tw369_drift_for_adjustments():
    """Test that TW369 drift influences the analysis."""
    engine = NietzscheEngine()
    text = "We will overcome all obstacles."
    
    # Low drift scenario
    tw_low_drift = TWState(metadata={"drift_metric": 0.1, "regime": "STABLE"})
    meta_input_low = MetaInput(text=text, tw_state=tw_low_drift)
    result_low = engine.analyze(meta_input_low)
    
    # High drift scenario
    tw_high_drift = TWState(metadata={"drift_metric": 0.9, "regime": "CRITICAL"})
    meta_input_high = MetaInput(text=text, tw_state=tw_high_drift)
    result_high = engine.analyze(meta_input_high)
    
    # High drift should boost will_to_power and dionysian
    assert result_high.will_to_power >= result_low.will_to_power
    assert result_high.scores["dionysian_force"] > result_low.scores["dionysian_force"]
    
    # Low drift should favor apollonian
    assert result_low.scores["apollonian_order"] >= result_high.scores["apollonian_order"]


def test_tw369_critical_regime_boosts_nihilism():
    """Test that CRITICAL regime boosts active nihilism."""
    engine = NietzscheEngine()
    
    tw_critical = TWState(metadata={"drift_metric": 0.8, "regime": "CRITICAL"})
    meta_input = MetaInput(
        text="We must tear down the old structures.",
        tw_state=tw_critical
    )
    result = engine.analyze(meta_input)
    
    # Critical regime should boost active nihilism
    assert result.scores["active_nihilism"] > 0.3


def test_tw369_transition_regime_boosts_transvaluation():
    """Test that TRANSITION regime boosts transvaluation."""
    engine = NietzscheEngine()
    
    tw_transition = TWState(metadata={"drift_metric": 0.5, "regime": "TRANSITION"})
    meta_input = MetaInput(
        text="We are redefining our values.",
        tw_state=tw_transition
    )
    result = engine.analyze(meta_input)
    
    # Transition regime should boost transvaluation
    assert result.scores["transvaluation"] >= 0.2


# ============================================================================
# Morality Type Classification Tests
# ============================================================================

def test_morality_type_classification_master():
    """Test master morality classification."""
    engine = NietzscheEngine()
    
    # Master morality text
    meta_input = MetaInput(
        text="We will dominate and conquer all obstacles with our superior strength and power. "
             "We lead, we command, we triumph through excellence."
    )
    result = engine.analyze(meta_input)
    
    assert result.morality_type == "master"
    assert result.will_to_power > 0.5


def test_morality_type_classification_slave():
    """Test slave morality classification."""
    engine = NietzscheEngine()
    
    # Slave morality text
    meta_input = MetaInput(
        text="It's so unfair. I'm the victim here. They don't deserve what they have. "
             "Why them and not me? I blame them for my situation. It's not fair."
    )
    result = engine.analyze(meta_input)
    
    assert result.morality_type == "slave"
    assert result.scores["resentment"] > 0.5


def test_morality_type_classification_mixed():
    """Test mixed morality classification."""
    engine = NietzscheEngine()
    
    # Mixed signals
    meta_input = MetaInput(
        text="We have power but also feel resentment. We lead but also blame others."
    )
    result = engine.analyze(meta_input)
    
    assert result.morality_type == "mixed"


def test_morality_type_with_kindra_power_climate():
    """Test that Kindra power_climate influences morality classification."""
    engine = NietzscheEngine()
    
    # High power climate should favor master
    kindra_power = KindraContext(
        layer1={"power_dynamics": 0.9, "dominance": 0.8},
        layer2={},
        layer3={}
    )
    
    meta_input = MetaInput(
        text="We will succeed.",
        kindra=kindra_power
    )
    result = engine.analyze(meta_input)
    
    # Should lean toward master with high power climate
    assert result.morality_type in ["master", "mixed"]


# ============================================================================
# Axis-Specific Tests
# ============================================================================

def test_will_to_power_detected():
    """Test will to power detection."""
    engine = NietzscheEngine()
    
    meta_input = MetaInput(
        text="We will dominate the market, lead with power, and conquer all obstacles. "
             "Our strength will triumph."
    )
    result = engine.analyze(meta_input)
    
    assert result.will_to_power > 0.5
    assert "will_to_power" in [ax[0] for ax in result.dominant_axes]


def test_resentment_detected():
    """Test resentment detection."""
    engine = NietzscheEngine()
    
    meta_input = MetaInput(
        text="It's so unfair. They don't deserve what they have. I'm the victim here. "
             "Why them and not me?"
    )
    result = engine.analyze(meta_input)
    
    assert result.scores["resentment"] > 0.5


def test_dionysian_vs_apollonian():
    """Test dionysian vs apollonian detection."""
    engine = NietzscheEngine()
    
    # Apollonian text
    meta_input_order = MetaInput(
        text="We need structure, order, and systematic organization. "
             "Harmony and balance are essential."
    )
    result_order = engine.analyze(meta_input_order)
    
    # Dionysian text
    meta_input_chaos = MetaInput(
        text="Wild chaos and primal passion! Embrace the frenzy and ecstasy of raw instinct!"
    )
    result_chaos = engine.analyze(meta_input_chaos)
    
    assert result_order.scores["apollonian_order"] > result_order.scores["dionysian_force"]
    assert result_chaos.scores["dionysian_force"] > result_chaos.scores["apollonian_order"]


def test_active_vs_passive_nihilism():
    """Test nihilism detection."""
    engine = NietzscheEngine()
    
    # Active nihilism
    meta_input_active = MetaInput(
        text="Tear down the old structures! Destroy and rebuild. "
             "Creative destruction is necessary."
    )
    result_active = engine.analyze(meta_input_active)
    
    # Passive nihilism
    meta_input_passive = MetaInput(
        text="Nothing matters anymore. Why bother? I'm just numb and indifferent to everything."
    )
    result_passive = engine.analyze(meta_input_passive)
    
    assert result_active.scores["active_nihilism"] > 0.4
    assert result_passive.scores["passive_nihilism"] > 0.4


def test_amor_fati_detection():
    """Test amor fati detection."""
    engine = NietzscheEngine()
    
    meta_input = MetaInput(
        text="I accept and embrace my fate. I love what is and wouldn't change a thing. "
             "It's perfect as is."
    )
    result = engine.analyze(meta_input)
    
    assert result.scores["amor_fati"] > 0.5


# ============================================================================
# Transcendence Tests
# ============================================================================

def test_transcendence_calculation():
    """Test transcendence (Übermensch) calculation."""
    engine = NietzscheEngine()
    
    # High transcendence text
    meta_input = MetaInput(
        text="We embrace life with power and joy, free from resentment, "
             "creating our own values beyond tradition."
    )
    result = engine.analyze(meta_input)
    
    # Should have elevated transcendence
    assert result.transcendence > 0.3


def test_transcendence_with_high_will_and_free_spirit():
    """Test that high will_to_power + free_spirit yields high transcendence."""
    engine = NietzscheEngine()
    
    meta_input = MetaInput(
        text="We dominate with power, think independently, question all traditions, "
             "and forge our own path with strength."
    )
    result = engine.analyze(meta_input)
    
    # Should have high transcendence
    assert result.transcendence > 0.4
    assert "Übermensch potential" in " ".join(result.notes)


# ============================================================================
# Backward Compatibility Tests
# ============================================================================

def test_backward_compatibility_wrapper():
    """Test that legacy analyze_meta() function still works."""
    text = "We must overcome and dominate our challenges with strength."
    
    result = analyze_meta(text)
    
    assert isinstance(result, MetaEngineResult)
    assert isinstance(result.scores, dict)
    assert len(result.scores) == 12
    assert isinstance(result.dominant_axes, list)
    assert isinstance(result.severity, float)
    assert isinstance(result.notes, list)


def test_backward_compatibility_with_tw_state():
    """Test legacy function with tw_state parameter."""
    text = "We will overcome all obstacles."
    tw_state = TWState(metadata={"drift_metric": 0.9, "regime": "CRITICAL"})
    
    result = analyze_meta(text, tw_state=tw_state)
    
    assert isinstance(result, MetaEngineResult)
    assert result.scores["will_to_power"] > 0.0


# ============================================================================
# Notes Generation Tests
# ============================================================================

def test_notes_generated():
    """Test that notes are generated."""
    engine = NietzscheEngine()
    
    meta_input = MetaInput(text="We must dominate with power!")
    result = engine.analyze(meta_input)
    
    assert len(result.notes) > 0
    assert all(isinstance(note, str) for note in result.notes)


def test_notes_include_morality_type():
    """Test that notes include morality type."""
    engine = NietzscheEngine()
    
    meta_input = MetaInput(text="We will dominate and conquer!")
    result = engine.analyze(meta_input)
    
    # Should have morality type in notes
    notes_text = " ".join(result.notes)
    assert "morality type" in notes_text.lower()


def test_notes_detect_contradictions():
    """Test that notes detect contradictions."""
    engine = NietzscheEngine()
    
    # Create contradictory text
    meta_input = MetaInput(
        text="We have immense power and strength to dominate, "
             "but it's unfair and we're victims who deserve better."
    )
    result = engine.analyze(meta_input)
    
    # Should detect tension
    notes_text = " ".join(result.notes)
    assert "tension" in notes_text.lower() or "contradiction" in notes_text.lower()


# ============================================================================
# Integration Tests
# ============================================================================

def test_full_integration_with_all_inputs():
    """Test full integration with Kindra + TW369 + archetypes."""
    engine = NietzscheEngine()
    
    kindra = KindraContext(
        layer1={"power_dynamics": 0.8, "dominance": 0.7},
        layer2={"conflict": 0.6},
        layer3={"archetypal_hero": 0.7, "mythic_pattern": 0.6}
    )
    
    tw_state = TWState(metadata={"drift_metric": 0.7, "regime": "CRITICAL"})
    
    archetype_scores = {"A03_WARRIOR": 0.8, "A10_SAGE": 0.3}
    
    meta_input = MetaInput(
        text="We will dominate and overcome all challenges with strength and wisdom.",
        kindra=kindra,
        tw_state=tw_state,
        archetype_scores=archetype_scores
    )
    
    result = engine.analyze(meta_input)
    
    # Should have high will_to_power (from text + kindra + tw369 + archetype)
    assert result.will_to_power > 0.6
    
    # Should have elevated transcendence (from mythic intensity)
    assert result.transcendence > 0.3
    
    # Should be master or mixed morality
    assert result.morality_type in ["master", "mixed"]
    
    # Should have valid structure
    assert len(result.scores) == 12
    assert len(result.dominant_axes) == 3
    assert len(result.notes) > 0
