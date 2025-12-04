"""
Tests for TimelineBuilder.
"""

import pytest
from datetime import datetime, timedelta
from src.story.story_buffer import StoryEvent
from src.story.timeline_builder import TimelineBuilder


class TestTimelineBuilder:
    
    def test_build_transitions(self):
        """Test transition tracking."""
        base_time = datetime.now()
        events = [
            StoryEvent(base_time, "E1", archetype_id="Hero"),
            StoryEvent(base_time + timedelta(minutes=1), "E2", archetype_id="Shadow"),
            StoryEvent(base_time + timedelta(minutes=2), "E3", archetype_id="Hero"),
            StoryEvent(base_time + timedelta(minutes=3), "E4", archetype_id="Hero") # No transition
        ]
        
        builder = TimelineBuilder()
        timeline = builder.build(events)
        
        assert len(timeline.events) == 4
        
        # Check transitions
        # Hero -> Shadow
        # Shadow -> Hero
        # Hero -> Hero (not a transition in our logic, only changes)
        
        counts = timeline.transition_counts
        assert counts.get("Hero->Shadow") == 1
        assert counts.get("Shadow->Hero") == 1
        
        # Check transition objects
        assert len(timeline.archetype_transitions) == 2

    def test_cycle_detection(self):
        """Test simple cycle detection."""
        base_time = datetime.now()
        events = [
            StoryEvent(base_time, "E1", archetype_id="A"),
            StoryEvent(base_time + timedelta(minutes=1), "E2", archetype_id="B"),
            StoryEvent(base_time + timedelta(minutes=2), "E3", archetype_id="A")
        ]
        
        builder = TimelineBuilder()
        timeline = builder.build(events)
        
        assert timeline.metadata["has_cycle"] is True
        assert timeline.transition_counts["A->B"] == 1
        assert timeline.transition_counts["B->A"] == 1

    def test_dominant_transition(self):
        """Test dominant transition identification."""
        base_time = datetime.now()
        events = [
            StoryEvent(base_time, "E1", archetype_id="A"),
            StoryEvent(base_time + timedelta(minutes=1), "E2", archetype_id="B"),
            StoryEvent(base_time + timedelta(minutes=2), "E3", archetype_id="A"),
            StoryEvent(base_time + timedelta(minutes=3), "E4", archetype_id="B")
        ]
        # A->B (2 times), B->A (1 time)
        
        builder = TimelineBuilder()
        timeline = builder.build(events)
        
        assert timeline.metadata["dominant_transition"] == "A->B"
