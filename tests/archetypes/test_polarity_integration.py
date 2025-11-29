"""
Test polarity integration in Delta144Engine.

v2.7: Tests for passing polarity_scores to infer_state().
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.archetypes.delta144_engine import Delta144Engine


def test_infer_state_with_polarity_scores():
    """Test infer_state accepts and returns polarity scores."""
    engine = Delta144Engine.from_schema()
    
    # Mock inputs
    archetype_id = "A07_RULER"
    plane_scores = {"3": 0.2, "6": 0.6, "9": 0.2}
    profile_scores = {"EXPANSIVE": 0.1, "CONTRACTIVE": 0.7, "TRANSCENDENT": 0.2}
    polarity_scores = {"POL_ORDER_CHAOS": 0.9, "POL_LIGHT_SHADOW": 0.8}
    
    result = engine.infer_state(
        archetype_id=archetype_id,
        plane_scores=plane_scores,
        profile_scores=profile_scores,
        polarity_scores=polarity_scores
    )
    
    # Check result contains polarity scores
    assert result.polarity_scores == polarity_scores
    assert result.polarity_scores["POL_ORDER_CHAOS"] == 0.9
    
    # Check to_dict serialization
    data = result.to_dict()
    assert "polarity_scores" in data
    assert data["polarity_scores"] == polarity_scores


def test_infer_state_without_polarity_scores():
    """Test infer_state works without polarity scores (backward compatibility)."""
    engine = Delta144Engine.from_schema()
    
    # Mock inputs
    archetype_id = "A07_RULER"
    plane_scores = {"3": 0.2, "6": 0.6, "9": 0.2}
    profile_scores = {"EXPANSIVE": 0.1, "CONTRACTIVE": 0.7, "TRANSCENDENT": 0.2}
    
    result = engine.infer_state(
        archetype_id=archetype_id,
        plane_scores=plane_scores,
        profile_scores=profile_scores
    )
    
    # Check result has empty polarity scores
    assert result.polarity_scores == {}
    
    # Check to_dict serialization
    data = result.to_dict()
    assert "polarity_scores" in data
    assert data["polarity_scores"] == {}
