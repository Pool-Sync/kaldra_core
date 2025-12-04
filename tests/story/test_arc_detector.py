"""
Tests for ArcDetector.
"""

import pytest
from datetime import datetime
from src.story.story_buffer import StoryEvent
from src.story.arc_detector import ArcDetector, JOURNEY_STAGES


class TestArcDetector:
    
    def test_detect_ordinary_world(self):
        """Test detection of Ordinary World stage."""
        events = [
            StoryEvent(datetime.now(), "Everything is normal and routine today."),
            StoryEvent(datetime.now(), "Just another everyday status quo situation.")
        ]
        
        detector = ArcDetector()
        arc = detector.detect(events)
        
        assert arc.dominant_stage == "ORDINARY_WORLD"
        assert arc.stage_scores["ORDINARY_WORLD"] > 0.5

    def test_detect_ordeal_with_archetypes(self):
        """Test detection of Ordeal using keywords and archetypes."""
        events = [
            StoryEvent(datetime.now(), "A major crisis is unfolding.", archetype_id="Shadow"),
            StoryEvent(datetime.now(), "The battle for survival begins.", archetype_id="Hero")
        ]
        
        detector = ArcDetector()
        arc = detector.detect(events)
        
        assert arc.dominant_stage == "ORDEAL"
        # Hero maps to Ordeal, Shadow maps to Ordeal, keywords map to Ordeal
        assert arc.stage_scores["ORDEAL"] > arc.stage_scores["ORDINARY_WORLD"]

    def test_empty_events(self):
        """Test handling of empty event list."""
        detector = ArcDetector()
        arc = detector.detect([])
        
        assert arc.dominant_stage == "ORDINARY_WORLD"
        assert "No events" in arc.notes[0]

    def test_score_normalization(self):
        """Test that scores sum to 1.0."""
        events = [StoryEvent(datetime.now(), "Start the journey")]
        detector = ArcDetector()
        arc = detector.detect(events)
        
        total_score = sum(arc.stage_scores.values())
        assert abs(total_score - 1.0) < 0.001
