"""
Tests for CoherenceScorer.
"""

import pytest
from datetime import datetime
from src.story.story_buffer import StoryEvent
from src.story.timeline_builder import StoryTimeline, ArchetypeTransition
from src.story.arc_detector import StoryArc
from src.story.coherence_scorer import CoherenceScorer


class TestCoherenceScorer:
    
    def test_high_coherence(self):
        """Test scoring a coherent narrative."""
        # Consistent archetypes, smooth polarity
        events = [
            StoryEvent(datetime.now(), "Good start", archetype_id="Hero", polarities={"sentiment": 0.5}),
            StoryEvent(datetime.now(), "Better middle", archetype_id="Hero", polarities={"sentiment": 0.6}),
            StoryEvent(datetime.now(), "Great end", archetype_id="Hero", polarities={"sentiment": 0.7})
        ]
        
        # Mock timeline with no transitions (Hero -> Hero -> Hero)
        timeline = StoryTimeline(events, archetype_transitions=[], transition_counts={})
        
        # Mock arc with high confidence
        arc = StoryArc("ORDINARY_WORLD", {"ORDINARY_WORLD": 0.9})
        
        scorer = CoherenceScorer()
        score = scorer.score(events, timeline, arc)
        
        assert score.archetype_consistency == 1.0  # No transitions
        assert score.polarity_smoothness == 1.0    # No sign flips
        assert score.stage_alignment == 0.9
        assert score.overall > 0.8

    def test_low_coherence(self):
        """Test scoring an incoherent narrative."""
        # Whipsaw archetypes, flipping polarity
        events = [
            StoryEvent(datetime.now(), "Good", archetype_id="Hero", polarities={"sentiment": 0.8}),
            StoryEvent(datetime.now(), "Bad", archetype_id="Shadow", polarities={"sentiment": -0.8}),
            StoryEvent(datetime.now(), "Good again", archetype_id="Hero", polarities={"sentiment": 0.8})
        ]
        
        # Transitions: Hero->Shadow, Shadow->Hero
        timeline = StoryTimeline(events, 
                               archetype_transitions=[
                                   ArchetypeTransition("Hero", "Shadow", 1),
                                   ArchetypeTransition("Shadow", "Hero", 1)
                               ], 
                               transition_counts={"Hero->Shadow": 1, "Shadow->Hero": 1})
        
        # Low confidence arc
        arc = StoryArc("ORDEAL", {"ORDEAL": 0.3})
        
        scorer = CoherenceScorer()
        score = scorer.score(events, timeline, arc)
        
        # 2 transitions / 2 possible = 1.0 ratio -> 0.0 consistency
        assert score.archetype_consistency == 0.0
        
        # 2 flips / 2 checks -> 0.0 smoothness
        assert score.polarity_smoothness == 0.0
        
        assert score.stage_alignment == 0.3
        assert score.overall < 0.5

    def test_empty_events(self):
        """Test scoring empty events."""
        scorer = CoherenceScorer()
        score = scorer.score([], StoryTimeline([]), StoryArc("None", {}))
        
        assert score.overall == 0.0
        assert "No events" in score.notes[0]
