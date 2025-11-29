"""
Test TW369 polarity modulation.

v2.7: Tests for modulate_state() method.
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.tw369.tw369_integration import TW369Integrator, TWState


def test_tw369_modulation_plane3():
    """Test modulation of Plane 3 (Cultural)."""
    integrator = TW369Integrator()
    
    # Initial state
    state = TWState(
        plane3_cultural_macro={"vec1": 1.0},
        plane6_semiotic_media={"vec2": 1.0},
        plane9_structural_systemic={"vec3": 1.0}
    )
    
    # High COLLECTIVE (Boosts Plane 3)
    polarity_scores = {"POL_INDIVIDUAL_COLLECTIVE": 1.0}
    
    mod_state = integrator.modulate_state(state, polarity_scores, intensity=0.5)
    
    # Plane 3 should increase
    # Factor = 1 + (1 * (2*1 - 1) * 0.5) = 1.5
    assert mod_state.plane3_cultural_macro["vec1"] == pytest.approx(1.5)
    
    # Others unchanged
    assert mod_state.plane6_semiotic_media["vec2"] == 1.0


def test_tw369_modulation_plane6():
    """Test modulation of Plane 6 (Tension)."""
    integrator = TW369Integrator()
    state = TWState(plane6_semiotic_media={"vec": 1.0})
    
    # High CHAOS (Boosts Plane 6)
    # POL_ORDER_CHAOS: -1 direction for Plane 6.
    # Score 0.0 (Chaos) -> Alignment -1 * (2*0 - 1) = 1.0 (Boost)
    polarity_scores = {"POL_ORDER_CHAOS": 0.0}
    
    mod_state = integrator.modulate_state(state, polarity_scores, intensity=0.5)
    
    # Factor = 1 + (1 * 0.5) = 1.5
    assert mod_state.plane6_semiotic_media["vec"] == pytest.approx(1.5)


def test_tw369_modulation_plane9():
    """Test modulation of Plane 9 (Structural)."""
    integrator = TW369Integrator()
    state = TWState(plane9_structural_systemic={"vec": 1.0})
    
    # High VOID (Suppresses Plane 9)
    # POL_MEANING_VOID: 1.0 direction.
    # Score 0.0 (Void) -> Alignment 1 * (2*0 - 1) = -1.0 (Suppress)
    polarity_scores = {"POL_MEANING_VOID": 0.0}
    
    mod_state = integrator.modulate_state(state, polarity_scores, intensity=0.5)
    
    # Factor = 1 + (-1 * 0.5) = 0.5
    assert mod_state.plane9_structural_systemic["vec"] == pytest.approx(0.5)


def test_tw369_modulation_empty():
    """Test with empty inputs."""
    integrator = TW369Integrator()
    state = TWState()
    mod_state = integrator.modulate_state(state, {})
    assert mod_state == state
