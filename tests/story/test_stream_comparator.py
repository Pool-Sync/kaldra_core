"""
Unit tests for StreamComparator.

Tests cover:
- Identical streams (low divergence)
- Completely different streams (high divergence)
- Partial overlap (mid divergence)
- Empty stream handling
- Basic note population
"""
import pytest
from src.story.stream_comparator import StreamComparator, StreamComparisonResult
from src.story.multi_stream_buffer import StreamWindow
from src.common.unified_signal import StoryEvent
import time


def create_event(
    event_id: str,
    stream_id: str,
    delta12: dict = None,
    polarity_scores: dict = None,
    delta144_state: str = None
) -> StoryEvent:
    """Helper to create a test event."""
    return StoryEvent(
        event_id=event_id,
        timestamp=time.time(),
        sequence_id=0,
        text="test",
        stream_id=stream_id,
        delta12=delta12,
        polarity_scores=polarity_scores,
        delta144_state=delta144_state
    )


class TestStreamComparator:
    """Test suite for StreamComparator."""
    
    def test_identical_streams_have_low_divergence(self):
        """Test that identical streams produce near-zero divergence."""
        comparator = StreamComparator()
        
        # Create identical events
        events_a = [
            create_event(
                "e1", "nyt",
                delta12={"hero": 0.8, "sage": 0.3},
                polarity_scores={"order": 0.7, "chaos": 0.2}
            ),
            create_event(
                "e2", "nyt",
                delta12={"hero": 0.7, "sage": 0.4},
                polarity_scores={"order": 0.6, "chaos": 0.3}
            )
        ]
        
        events_b = [
            create_event(
                "e3", "twitter",
                delta12={"hero": 0.8, "sage": 0.3},
                polarity_scores={"order": 0.7, "chaos": 0.2}
            ),
            create_event(
                "e4", "twitter",
                delta12={"hero": 0.7, "sage": 0.4},
                polarity_scores={"order": 0.6, "chaos": 0.3}
            )
        ]
        
        windows = [
            StreamWindow("nyt", events_a),
            StreamWindow("twitter", events_b)
        ]
        
        results = comparator.compare_windows(windows)
        
        assert len(results) == 1
        result = results[0]
        
        # Identical streams should have very low divergence
        assert result.overall_divergence < 0.1
        assert result.archetype_divergence < 0.1
        assert result.polarity_divergence < 0.1
    
    def test_completely_different_streams_have_high_divergence(self):
        """Test that completely different streams produce high divergence."""
        comparator = StreamComparator()
        
        # Stream A: high hero, low sage, high order
        events_a = [
            create_event(
                "e1", "nyt",
                delta12={"hero": 1.0, "sage": 0.0},
                polarity_scores={"order": 1.0, "chaos": 0.0}
            )
        ]
        
        # Stream B: low hero, high sage, high chaos (orthogonal)
        events_b = [
            create_event(
                "e2", "twitter",
                delta12={"hero": 0.0, "sage": 1.0},
                polarity_scores={"order": 0.0, "chaos": 1.0}
            )
        ]
        
        windows = [
            StreamWindow("nyt", events_a),
            StreamWindow("twitter", events_b)
        ]
        
        results = comparator.compare_windows(windows)
        
        assert len(results) == 1
        result = results[0]
        
        # Completely different streams should have high divergence
        assert result.overall_divergence > 0.5
        assert result.archetype_divergence > 0.5
        assert result.polarity_divergence > 0.5
    
    def test_partial_overlap_mid_divergence(self):
        """Test that partially overlapping streams have mid-range divergence."""
        comparator = StreamComparator()
        
        # Stream A: strong hero, weak sage
        events_a = [
            create_event(
                "e1", "nyt",
                delta12={"hero": 0.9, "sage": 0.1},
                polarity_scores={"order": 0.8, "chaos": 0.2}
            )
        ]
        
        # Stream B: balanced, different archetypes
        events_b = [
            create_event(
                "e2", "twitter",
                delta12={"rebel": 0.6, "sage": 0.4},
                polarity_scores={"order": 0.5, "chaos": 0.5}
            )
        ]
        
        windows = [
            StreamWindow("nyt", events_a),
            StreamWindow("twitter", events_b)
        ]
        
        results = comparator.compare_windows(windows)
        
        assert len(results) == 1
        result = results[0]
        
        # Different but not completely orthogonal
        assert 0.2 < result.overall_divergence < 0.95
    
    def test_empty_streams_handled_gracefully(self):
        """Test that empty streams don't cause errors."""
        comparator = StreamComparator()
        
        # Both empty
        windows_both_empty = [
            StreamWindow("nyt", []),
            StreamWindow("twitter", [])
        ]
        
        results = comparator.compare_windows(windows_both_empty)
        assert len(results) == 1
        assert results[0].overall_divergence == 0.0
        assert "warning" in results[0].notes
        
        # One empty
        events = [
            create_event(
                "e1", "nyt",
                delta12={"hero": 0.5},
                polarity_scores={"order": 0.5}
            )
        ]
        
        windows_one_empty = [
            StreamWindow("nyt", events),
            StreamWindow("twitter", [])
        ]
        
        results = comparator.compare_windows(windows_one_empty)
        assert len(results) == 1
        assert results[0].overall_divergence == 1.0  # Maximum divergence
        assert "warning" in results[0].notes
    
    def test_notes_field_populated_with_basic_info(self):
        """Test that notes field contains relevant information."""
        comparator = StreamComparator()
        
        events_a = [
            create_event(
                "e1", "nyt",
                delta12={"hero": 0.5},
                polarity_scores={"order": 0.5}
            )
        ]
        
        events_b = [
            create_event(
                "e2", "twitter",
                delta12={"sage": 0.5},
                polarity_scores={"chaos": 0.5}
            )
        ]
        
        windows = [
            StreamWindow("nyt", events_a),
            StreamWindow("twitter", events_b)
        ]
        
        results = comparator.compare_windows(windows)
        
        assert len(results) == 1
        result = results[0]
        
        # Should have note about stage divergence not being implemented
        assert "stage_divergence" in result.notes
        assert result.stage_divergence == 0.0
    
    def test_multiple_streams_all_pairs_compared(self):
        """Test that all pairs are compared when multiple streams."""
        comparator = StreamComparator()
        
        events_a = [create_event("e1", "nyt", delta12={"hero": 0.5})]
        events_b = [create_event("e2", "twitter", delta12={"sage": 0.5})]
        events_c = [create_event("e3", "reddit", delta12={"rebel": 0.5})]
        
        windows = [
            StreamWindow("nyt", events_a),
            StreamWindow("twitter", events_b),
            StreamWindow("reddit", events_c)
        ]
        
        results = comparator.compare_windows(windows)
        
        # Should have 3 comparisons: (nyt,twitter), (nyt,reddit), (twitter,reddit)
        assert len(results) == 3
        
        pairs = {(r.stream_a, r.stream_b) for r in results}
        expected_pairs = {
            ("nyt", "twitter"),
            ("nyt", "reddit"),
            ("twitter", "reddit")
        }
        assert pairs == expected_pairs
    
    def test_delta144_state_included_in_archetype_profile(self):
        """Test that delta144_state is included in archetype aggregation."""
        comparator = StreamComparator()
        
        events_a = [
            create_event("e1", "nyt", delta144_state="threshold"),
            create_event("e2", "nyt", delta144_state="threshold")
        ]
        
        events_b = [
            create_event("e3", "twitter", delta144_state="resurrection"),
            create_event("e4", "twitter", delta144_state="resurrection")
        ]
        
        windows = [
            StreamWindow("nyt", events_a),
            StreamWindow("twitter", events_b)
        ]
        
        results = comparator.compare_windows(windows)
        
        assert len(results) == 1
        # Different delta144 states should contribute to divergence
        assert results[0].archetype_divergence > 0.5
    
    def test_no_streams_returns_empty_list(self):
        """Test that comparing zero streams returns empty list."""
        comparator = StreamComparator()
        results = comparator.compare_windows([])
        assert results == []
    
    def test_single_stream_returns_empty_list(self):
        """Test that a single stream has no pairs to compare."""
        comparator = StreamComparator()
        
        events = [create_event("e1", "nyt", delta12={"hero": 0.5})]
        windows = [StreamWindow("nyt", events)]
        
        results = comparator.compare_windows(windows)
        assert results == []
