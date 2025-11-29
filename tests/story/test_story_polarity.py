"""
Test Story Engine polarity integration.

v2.7: Tests for polarity tracking in StoryBuffer and StoryAggregator.
"""
import pytest
import sys
from pathlib import Path
import time

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.story.story_buffer import StoryBuffer
from src.story.story_aggregator import aggregate_story, compute_narrative_motion


def test_story_buffer_polarity_storage():
    """Test storing polarity scores in StoryBuffer."""
    buffer = StoryBuffer()
    
    scores = {"POL_ORDER_CHAOS": 0.8}
    event = buffer.add_event("Test text", polarity_scores=scores)
    
    assert event.polarity_scores == scores
    assert event.polarity_scores["POL_ORDER_CHAOS"] == 0.8


def test_motion_vector_polarity_deltas():
    """Test calculating polarity deltas in motion vectors."""
    buffer = StoryBuffer()
    
    # Event 1: High Order
    buffer.add_event("Event 1", polarity_scores={"POL_ORDER_CHAOS": 0.9})
    time.sleep(0.01) # Ensure timestamp diff
    
    # Event 2: Low Order (Chaos)
    buffer.add_event("Event 2", polarity_scores={"POL_ORDER_CHAOS": 0.2})
    
    timeline = buffer.get_timeline()
    motion = compute_narrative_motion(timeline[0], timeline[1])
    
    assert "POL_ORDER_CHAOS" in motion.polarity_deltas
    # Delta should be approx -0.7
    assert motion.polarity_deltas["POL_ORDER_CHAOS"] == pytest.approx(-0.7)


def test_inflection_point_polarity_inversion():
    """Test detecting polarity inversion inflection points."""
    buffer = StoryBuffer()
    
    # Event 1: High Order
    buffer.add_event("Event 1", polarity_scores={"POL_ORDER_CHAOS": 0.9})
    
    # Event 2: Low Order (Chaos) - massive flip
    buffer.add_event("Event 2", polarity_scores={"POL_ORDER_CHAOS": 0.1})
    
    aggregation = aggregate_story(buffer)
    
    # Should detect inflection point
    inflections = aggregation.inflection_points
    polarity_inflections = [i for i in inflections if i.inflection_type == "polarity_inversion"]
    
    assert len(polarity_inflections) > 0
    assert "POL_ORDER_CHAOS" in polarity_inflections[0].description
    assert polarity_inflections[0].magnitude == pytest.approx(0.8)
