"""
Integration tests for MultiStreamStage.

Tests v3.3 Phase 3 multi-stream integration with the unified pipeline.
"""
import pytest
import time
from src.unification.states.unified_state import (
    UnifiedContext,
    GlobalContext,
    InputContext,
    InputMetadata,
    StoryContext,
)
from src.common.unified_signal import StoryEvent
from src.unification.pipeline.multi_stream_stage import MultiStreamStage, MultiStreamStageConfig


def create_story_event(
    event_id: str,
    stream_id: str,
    delta12: dict = None,
    polarity_scores: dict = None,
    text: str = "test"
) -> StoryEvent:
    """Helper to create a test StoryEvent."""
    return StoryEvent(
        event_id=event_id,
        timestamp=time.time(),
        sequence_id=0,
        text=text,
        stream_id=stream_id,
        delta12=delta12,
        polarity_scores=polarity_scores
    )


class TestMultiStreamStageIntegration:
    """Integration test suite for MultiStreamStage."""
    
    def test_single_stream_no_regression(self):
        """Test that single-stream processing works (no regression)."""
        # Setup
        stage = MultiStreamStage()
        
        # Create context with single stream events
        events = [
            create_story_event("e1", "nyt", delta12={"hero": 0.8}),
            create_story_event("e2", "nyt", delta12={"hero": 0.7}),
            create_story_event("e3", "nyt", delta12={"hero": 0.9}),
        ]
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            story_ctx=StoryContext(events=events)
        )
        
        # Execute
        result = stage.run(context)
        
        # Verify
        assert result.multi_stream_ctx is not None
        assert result.multi_stream_ctx.active_streams == ["nyt"]
        assert len(result.multi_stream_ctx.pairwise_results) == 0  # Single stream = no pairs
        assert result.multi_stream_ctx.max_divergence == 0.0
        assert result.multi_stream_ctx.convergent is True
    
    def test_divergent_streams(self):
        """Test that divergent streams are detected."""
        # Setup
        stage = MultiStreamStage(MultiStreamStageConfig(divergence_threshold=0.7))
        
        # Create events from two divergent streams
        nyt_events = [
            create_story_event(
                f"nyt_{i}", "nyt",
                delta12={"hero": 0.9, "sage": 0.1},
                polarity_scores={"order": 0.8, "chaos": 0.2}
            )
            for i in range(5)
        ]
        
        twitter_events = [
            create_story_event(
                f"twitter_{i}", "twitter",
                delta12={"rebel": 0.8, "orphan": 0.3},
                polarity_scores={"order": 0.2, "chaos": 0.8}
            )
            for i in range(5)
        ]
        
        all_events = nyt_events + twitter_events
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            story_ctx=StoryContext(events=all_events)
        )
        
        # Execute
        result = stage.run(context)
        
        # Verify
        assert result.multi_stream_ctx is not None
        assert set(result.multi_stream_ctx.active_streams) == {"nyt", "twitter"}
        assert len(result.multi_stream_ctx.pairwise_results) == 1  # One pair: nyt vs twitter
        
        # Check divergence
        comparison = result.multi_stream_ctx.pairwise_results[0]
        assert comparison.stream_a in ["nyt", "twitter"]
        assert comparison.stream_b in ["nyt", "twitter"]
        assert comparison.overall_divergence > 0.5  # Should be divergent
        
        # Check max divergence
        assert result.multi_stream_ctx.max_divergence > 0.7
        assert result.multi_stream_ctx.convergent is False  # Not convergent
    
    def test_no_story_ctx(self):
        """Test that stage skips gracefully when no story_ctx."""
        # Setup
        stage = MultiStreamStage()
        
        # Create context without story_ctx
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            story_ctx=None
        )
        
        # Execute
        result = stage.run(context)
        
        # Verify - should skip and leave multi_stream_ctx as None
        assert result.multi_stream_ctx is None
    
    def test_empty_story_events(self):
        """Test that stage skips when story_ctx has no events."""
        # Setup
        stage = MultiStreamStage()
        
        # Create context with empty events
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            story_ctx=StoryContext(events=[])
        )
        
        # Execute
        result = stage.run(context)
        
        # Verify
        assert result.multi_stream_ctx is None
    
    def test_stage_disabled(self):
        """Test that stage does nothing when disabled."""
        # Setup
        stage = MultiStreamStage(MultiStreamStageConfig(enabled=False))
        
        # Create context with events
        events = [
            create_story_event("e1", "nyt", delta12={"hero": 0.8}),
            create_story_event("e2", "twitter", delta12={"rebel": 0.7}),
        ]
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            story_ctx=StoryContext(events=events)
        )
        
        # Execute
        result = stage.run(context)
        
        # Verify - should not populate multi_stream_ctx
        assert result.multi_stream_ctx is None
    
    def test_graceful_degradation(self):
        """Test that stage handles errors gracefully."""
        # Setup
        stage = MultiStreamStage()
        
        # Create context with MULTIPLE streams to trigger comparator
        events = [
            create_story_event("e1", "nyt", delta12={"hero": 0.8}),
            create_story_event("e2", "twitter", delta12={"rebel": 0.7}),  # Second stream
        ]
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            story_ctx=StoryContext(events=events)
        )
        
        # Monkeypatch comparator to raise exception
        def failing_compare(windows):
            raise ValueError("Simulated failure")
        
        stage._comparator.compare_windows = failing_compare
        
        # Execute - should not raise exception
        result = stage.run(context)
        
        # Verify - should handle gracefully, leaving multi_stream_ctx as None
        assert result.multi_stream_ctx is None
    
    def test_stream_id_fallback_to_default(self):
        """Test that events without stream_id get 'default' stream."""
        # Setup
        stage = MultiStreamStage()
        
        # Create events without explicit stream_id (None)
        events = [
            StoryEvent(
                event_id="e1",
                timestamp=time.time(),
                sequence_id=0,
                text="test",
                stream_id=None  # Explicitly None
            ),
            StoryEvent(
                event_id="e2",
                timestamp=time.time(),
                sequence_id=1,
                text="test",
                stream_id=None
            ),
        ]
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            story_ctx=StoryContext(events=events)
        )
        
        # Execute
        result = stage.run(context)
        
        # Verify - should use "default" stream
        assert result.multi_stream_ctx is not None
        assert result.multi_stream_ctx.active_streams == ["default"]
    
    def test_multiple_streams_all_pairs(self):
        """Test that all stream pairs are compared."""
        # Setup
        stage = MultiStreamStage()
        
        # Create events from 3 streams
        events = [
            create_story_event("e1", "nyt", delta12={"hero": 0.8}),
            create_story_event("e2", "twitter", delta12={"rebel": 0.7}),
            create_story_event("e3", "reddit", delta12={"sage": 0.6}),
        ]
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            story_ctx=StoryContext(events=events)
        )
        
        # Execute
        result = stage.run(context)
        
        # Verify - should have 3 pairs: (nyt,twitter), (nyt,reddit), (twitter,reddit)
        assert result.multi_stream_ctx is not None
        assert len(result.multi_stream_ctx.active_streams) == 3
        assert len(result.multi_stream_ctx.pairwise_results) == 3
        
        # Verify all pairs are present
        pairs = {
            (r.stream_a, r.stream_b)
            for r in result.multi_stream_ctx.pairwise_results
        }
        
        # Note: order in pairs doesn't matter for this test
        assert len(pairs) == 3
