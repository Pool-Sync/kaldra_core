"""
Test Delta12Vector polarity modulation.

v2.7: Tests for modulate() method.
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.archetypes.delta12_vector import Delta12Vector, ARCHETYPE_IDS


def test_delta12_modulation_boost():
    """Test that modulation boosts aligned archetypes."""
    # Start with uniform distribution
    vec = Delta12Vector().normalize()
    initial_prob = vec.values["A03_WARRIOR"]
    
    # Apply high COURAGE (Warrior aligned)
    polarity_scores = {"POL_COURAGE_FEAR": 1.0}
    vec.modulate(polarity_scores, intensity=0.5)
    
    # Warrior should increase
    assert vec.values["A03_WARRIOR"] > initial_prob


def test_delta12_modulation_suppress():
    """Test that modulation suppresses opposed archetypes."""
    vec = Delta12Vector().normalize()
    initial_prob = vec.values["A01_INNOCENT"]
    
    # Apply high CHAOS (Innocent wants Order)
    # POL_ORDER_CHAOS: 1.0 = Order, 0.0 = Chaos
    # Innocent has +1 alignment with Order.
    # If we pass 0.0 (Chaos), alignment = 1 * (2*0 - 1) = -1.
    # Factor = 1 + (-1 * 0.5) = 0.5. Should decrease.
    polarity_scores = {"POL_ORDER_CHAOS": 0.0}
    vec.modulate(polarity_scores, intensity=0.5)
    
    assert vec.values["A01_INNOCENT"] < initial_prob


def test_delta12_modulation_mixed():
    """Test mixed modulation effects."""
    vec = Delta12Vector().normalize()
    
    # High Order (Boosts Ruler, Innocent)
    # High Liberty (Boosts Rebel)
    polarity_scores = {
        "POL_ORDER_CHAOS": 1.0,
        "POL_LIBERTY_OPPRESSION": 1.0
    }
    
    vec.modulate(polarity_scores, intensity=0.5)
    
    # Ruler (Order+) should be high
    # Rebel (Order-, Liberty+) -> Conflict.
    # Order alignment: -1 * (2*1 - 1) = -1
    # Liberty alignment: 1 * (2*1 - 1) = 1
    # Net factor: 1 + (-0.5) + (0.5) = 1.0. Should stay roughly same (relative to others)
    
    assert vec.values["A07_RULER"] > vec.values["A08_REBEL"]


def test_delta12_modulation_normalization():
    """Test that vector remains normalized after modulation."""
    vec = Delta12Vector().normalize()
    polarity_scores = {"POL_COURAGE_FEAR": 1.0}
    vec.modulate(polarity_scores)
    
    total = sum(vec.values.values())
    assert total == pytest.approx(1.0)
