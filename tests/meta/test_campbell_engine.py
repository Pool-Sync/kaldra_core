"""
Tests for CampbellEngine - Hero's Journey detection.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from meta.campbell import CampbellEngine, HERO_JOURNEY_STAGES
from meta.meta_engine_base import MetaSignal


def test_campbell_engine_basic():
    """Test that CampbellEngine runs without error."""
    engine = CampbellEngine()
    
    # Minimal signal
    signal = {
        "delta144": None,
        "drift_history": [],
        "tw_state": None
    }
    
    result = engine.run(signal)
    
    assert isinstance(result, MetaSignal)
    assert result.name == "campbell"
    assert 0.0 <= result.score <= 1.0
    assert result.label in HERO_JOURNEY_STAGES


def test_campbell_12_stages_defined():
    """Test that all 12 stages are defined."""
    assert len(HERO_JOURNEY_STAGES) == 12
    assert "ordinary_world" in HERO_JOURNEY_STAGES
    assert "ordeal" in HERO_JOURNEY_STAGES
    assert "return_with_elixir" in HERO_JOURNEY_STAGES


def test_campbell_ordeal_detection():
    """Test ordeal detection with high drift and low coherence."""
    engine = CampbellEngine()
    
    # Mock drift history indicating crisis
    class MockDriftState:
        drift_metric = 0.9
        painleve_coherence = 0.2
        regime = "crisis"
    
    signal = {
        "delta144": None,
        "drift_history": [MockDriftState(), MockDriftState()],
        "tw_state": None
    }
    
    result = engine.run(signal)
    
    # Should detect crisis-related stage
    assert result.label in ["ordeal", "approach_to_cave", "tests_allies_enemies"]


def test_campbell_ordinary_world_detection():
    """Test ordinary world detection with low drift."""
    engine = CampbellEngine()
    
    # Mock drift history indicating stability
    class MockDriftState:
        drift_metric = 0.1
        painleve_coherence = 0.8
        regime = "stable"
    
    signal = {
        "delta144": None,
        "drift_history": [MockDriftState(), MockDriftState(), MockDriftState()],
        "tw_state": None
    }
    
    result = engine.run(signal)
    
    # Should detect stable/beginning stages
    assert result.label in ["ordinary_world", "return_with_elixir"]


def test_campbell_fail_safe():
    """Test that engine fails safely on bad input."""
    engine = CampbellEngine()
    
    # Invalid signal
    signal = {"invalid": "data"}
    
    result = engine.run(signal)
    
    # Should return valid MetaSignal even on error
    assert isinstance(result, MetaSignal)
    assert result.label in HERO_JOURNEY_STAGES
