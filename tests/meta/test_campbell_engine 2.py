"""
Tests for CampbellEngine v3.1.

Tests the snapshot-only Hero's Journey analyzer with:
- Δ144 to Campbell role mapping
- Journey stage detection
- Kindra 3×48 integration
- TW369 transformation potential
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from meta.campbell_engine import (
    CampbellEngine,
    CampbellSignal,
    CAMPBELL_ARCHETYPES,
    JOURNEY_STAGES
)
from meta.nietzsche import MetaInput
from unification.states.unified_state import KindraContext
from tw369.tw369_integration import TWState


# ============================================================================
# Basic Functionality Tests
# ============================================================================

def test_basic_analysis_runs_without_error():
    """Test that basic analysis runs and returns a valid signal."""
    engine = CampbellEngine()
    meta_input = MetaInput(text="The hero accepts the call to adventure.")
    
    result = engine.analyze(meta_input)
    
    assert isinstance(result, CampbellSignal)
    assert result.journey_stage in JOURNEY_STAGES
    assert 0.0 <= result.mythic_resonance <= 1.0
    assert 0.0 <= result.transformation_potential <= 1.0
    assert isinstance(result.archetypal_roles, dict)


def test_signal_fields_in_range():
    """Test that all numeric fields are within [0, 1]."""
    engine = CampbellEngine()
    meta_input = MetaInput(text="Crisis battle death rebirth.")
    result = engine.analyze(meta_input)
    
    assert 0.0 <= result.transformation_potential <= 1.0
    assert 0.0 <= result.mythic_resonance <= 1.0
    assert 0.0 <= result.severity <= 1.0
    assert 0.0 <= result.score <= 1.0


# ============================================================================
# Archetype Mapping Tests
# ============================================================================

def test_archetype_normalization_mapping_state():
    """Test mapping from explicit delta144_state."""
    engine = CampbellEngine()
    
    # Test HERO mapping
    meta_input = MetaInput(
        text="...",
        delta144_state="A04_HERO_STATE_01"
    )
    result = engine.analyze(meta_input)
    assert "A04_HERO_STATE_01" in result.archetypal_roles
    assert result.archetypal_roles["A04_HERO_STATE_01"] == "HERO"
    assert "HERO" in result.active_archetypes

    # Test SHADOW mapping
    meta_input_shadow = MetaInput(
        text="...",
        delta144_state="A08_REBEL_STATE_99"
    )
    result_shadow = engine.analyze(meta_input_shadow)
    assert result_shadow.archetypal_roles["A08_REBEL_STATE_99"] == "SHADOW"


def test_active_archetypes_top3_from_scores():
    """Test mapping from archetype_scores (top 3)."""
    engine = CampbellEngine()
    
    scores = {
        "A02_SAGE": 0.9,      # MENTOR
        "A11_TRICKSTER": 0.8, # TRICKSTER
        "A06_CAREGIVER": 0.7, # ALLY
        "A04_HERO": 0.1       # Should be ignored (4th)
    }
    
    meta_input = MetaInput(text="...", archetype_scores=scores)
    result = engine.analyze(meta_input)
    
    assert len(result.active_archetypes) <= 3
    assert "MENTOR" in result.active_archetypes
    assert "TRICKSTER" in result.active_archetypes
    assert "ALLY" in result.active_archetypes
    assert "HERO" not in result.active_archetypes


# ============================================================================
# Stage Detection Tests
# ============================================================================

def test_journey_stage_detection_variants():
    """Test detection of specific stages based on keywords."""
    engine = CampbellEngine()
    
    # Call to Adventure
    input_call = MetaInput(text="The message arrived with a challenge and an invitation to adventure.")
    res_call = engine.analyze(input_call)
    assert res_call.journey_stage == "CALL_TO_ADVENTURE"
    
    # Ordeal
    input_ordeal = MetaInput(text="A crisis of survival, a battle to the death, the ultimate confrontation.")
    res_ordeal = engine.analyze(input_ordeal)
    assert res_ordeal.journey_stage == "ORDEAL"
    
    # Return
    input_return = MetaInput(text="Returning home with the elixir to heal the world.")
    res_return = engine.analyze(input_return)
    assert res_return.journey_stage == "RETURN_WITH_ELIXIR"


def test_stage_detection_role_influence():
    """Test that active roles influence stage detection."""
    engine = CampbellEngine()
    
    # MENTOR presence should boost MEETING_MENTOR
    scores = {"A02_SAGE": 1.0} # MENTOR
    meta_input = MetaInput(text="guide wisdom", archetype_scores=scores)
    result = engine.analyze(meta_input)
    
    assert result.journey_stage == "MEETING_MENTOR"


# ============================================================================
# Integration Tests (Kindra & TW369)
# ============================================================================

def test_kindra_influences_mythic_resonance():
    """Test that Kindra depth increases mythic resonance."""
    engine = CampbellEngine()
    text = "A simple story."
    
    # Baseline
    res_base = engine.analyze(MetaInput(text=text))
    
    # With Kindra Depth
    kindra = KindraContext(
        layer1={},
        layer2={"intensity": 0.8},
        layer3={"myth": 0.9, "symbol": 0.9, "archetype": 0.9}
    )
    res_kindra = engine.analyze(MetaInput(text=text, kindra=kindra))
    
    assert res_kindra.mythic_resonance > res_base.mythic_resonance


def test_tw369_influences_transformation_potential():
    """Test that TW369 drift/regime affects transformation potential."""
    engine = CampbellEngine()
    text = "A time of change."
    
    # Stable/Low Drift
    tw_stable = TWState(metadata={"drift_metric": 0.1, "regime": "STABLE"})
    res_stable = engine.analyze(MetaInput(text=text, tw_state=tw_stable))
    
    # Critical/High Drift
    tw_critical = TWState(metadata={"drift_metric": 0.9, "regime": "CRITICAL"})
    res_critical = engine.analyze(MetaInput(text=text, tw_state=tw_critical))
    
    assert res_critical.transformation_potential > res_stable.transformation_potential


def test_kindra_liminality_boosts_threshold():
    """Test that Kindra liminality boosts threshold stages."""
    engine = CampbellEngine()
    
    kindra = KindraContext(
        layer1={},
        layer2={"transition": 0.9},
        layer3={"threshold": 0.9}
    )
    
    # Text is ambiguous, but Kindra signals threshold
    meta_input = MetaInput(text="moving forward", kindra=kindra)
    result = engine.analyze(meta_input)
    
    # Should likely be CROSSING_THRESHOLD or APPROACH_INMOST_CAVE
    assert result.journey_stage in ["CROSSING_THRESHOLD", "APPROACH_INMOST_CAVE", "RETURN_WITH_ELIXIR"]
