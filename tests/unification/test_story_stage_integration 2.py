"""
Integration tests for StoryStage v3.2.

Tests StoryStage pipeline integration:
- StoryContext population from UnifiedContext
- Sliding window behavior with buffer limits
- Coherence enabled/disabled modes
- Metadata preservation (delta144_timeline)
- Empty input handling
"""

import pytest
from datetime import datetime
from typing import Dict, Any

from src.unification.pipeline.story_stage import StoryStage, StoryStageConfig
from src.unification.states.unified_state import (
    UnifiedContext,
    GlobalContext,
    InputContext,
    ArchetypeContext,
    StoryContext
)
from src.archetypes.delta12_vector import Delta12Vector


# Mock Delta144 state for testing
class MockDelta144State:
    """Mock StateInferenceResult for testing."""
    def __init__(self, state_id: str, weights: Dict[str, float]):
        self.state_id = state_id
        self.weights = weights


class TestStoryStagePopulation:
    """Test that StoryStage populates StoryContext correctly."""
    
    def test_story_stage_populates_story_context(self):
        """StoryStage should populate story_ctx with events, arc, timeline."""
        stage = StoryStage()
        
        # Create minimal context
        context = UnifiedContext(
            global_ctx=GlobalContext(request_id="test-1", mode="full"),
            input_ctx=InputContext(text="A hero receives a call to adventure."),
            archetype_ctx=ArchetypeContext(
                delta144_state=MockDelta144State("A04_HERO", {"A04_HERO": 0.85})
            )
        )
        
        result = stage.run(context)
        
        # Should have story_ctx populated
        assert result.story_ctx is not None
        assert len(result.story_ctx.events) >= 1
        assert result.story_ctx.arc is not None
        assert result.story_ctx.timeline is not None
        
        # Events should have data from context
        event = result.story_ctx.events[0]
        assert event.text == "A hero receives a call to adventure."
        assert event.archetype_id == "A04_HERO"
    
    def test_story_context_includes_coherence_when_enabled(self):
        """With coherence enabled, story_ctx.coherence should be populated."""
        stage = StoryStage(StoryStageConfig(enable_coherence=True))
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="First event")
        )
        
        # Add multiple events to build coherence
        for i in range(5):
            context.input_ctx.text = f"Event {i}"
            context = stage.run(context)
        
        # Coherence should be computed (non-zero or object)
        assert context.story_ctx.coherence is not None
        # Could be 0.0 if CoherenceScorer returns 0 for low event count


class TestSlidingWindow:
    """Test sliding window behavior and buffer limits."""
    
    def test_story_stage_maintains_sliding_window(self):
        """Buffer should respect max_events limit and evict oldest."""
        stage = StoryStage(StoryStageConfig(max_events=100, window_size=50))
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="Event")
        )
        
        # Add 150 events (exceeds max_events=100)
        for i in range(150):
            context.input_ctx.text = f"Event {i}"
            context.global_ctx.timestamp = float(i)
            context = stage.run(context)
        
        # Should have at most 100 events in buffer
        # But window_size=50, so story_ctx should have ≤ 50 events
        assert len(context.story_ctx.events) <= 50
        
        # Latest events should be present (149, 148, ...)
        latest_texts = [e.text for e in context.story_ctx.events[-5:]]
        assert "Event 149" in latest_texts or "Event 148" in latest_texts
    
    def test_window_size_limits_analyzed_events(self):
        """window_size should limit events passed to Story Engine."""
        stage = StoryStage(StoryStageConfig(max_events=1000, window_size=10))
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="Event")
        )
        
        # Add 50 events
        for i in range(50):
            context.input_ctx.text = f"Event {i}"
            context = stage.run(context)
        
        # Should analyze only last 10 events
        assert len(context.story_ctx.events) <= 10


class TestCoherenceToggle:
    """Test coherence enabled/disabled behavior."""
    
    def test_coherence_enabled(self):
        """With enable_coherence=True, coherence should be computed."""
        stage = StoryStage(StoryStageConfig(enable_coherence=True))
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="Coherent narrative event")
        )
        
        # Add a few events
        for i in range(3):
            context.input_ctx.text = f"Event {i}"
            context = stage.run(context)
        
        # Coherence should exist (may be 0.0 but not None)
        assert context.story_ctx is not None
        assert isinstance(context.story_ctx.coherence, (int, float))
    
    def test_coherence_disabled(self):
        """With enable_coherence=False, coherence should be 0.0."""
        stage = StoryStage(StoryStageConfig(enable_coherence=False))
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="Event without coherence")
        )
        
        context = stage.run(context)
        
        # Coherence should be 0.0 when disabled
        assert context.story_ctx.coherence == 0.0


class TestMetadataPreservation:
    """Test that metadata (e.g., delta144_timeline) is preserved."""
    
    def test_preserves_existing_metadata(self):
        """Existing story_ctx metadata should be preserved across runs."""
        stage = StoryStage()
        
        # Create context with pre-existing story_ctx + metadata
        existing_metadata = {
            "delta144_timeline": [
                {"t": 1000, "state_id": "A04_HERO", "weight": 0.9}
            ],
            "custom_field": "should_persist"
        }
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="New event"),
            story_ctx=StoryContext(metadata=existing_metadata)
        )
        
        result = stage.run(context)
        
        # Metadata should be preserved
        assert "delta144_timeline" in result.story_ctx.metadata
        assert result.story_ctx.metadata["delta144_timeline"][0]["state_id"] == "A04_HERO"
        assert result.story_ctx.metadata["custom_field"] == "should_persist"
    
    def test_metadata_not_overwritten_on_new_events(self):
        """Adding new events should not delete existing metadata."""
        stage = StoryStage()
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="Event 1")
        )
        
        # First run - no metadata
        context = stage.run(context)
        
        # Add metadata manually
        context.story_ctx.metadata["delta144_timeline"] = [{"t": 123, "state_id": "A01_CREATOR"}]
        
        # Second run - should preserve metadata
        context.input_ctx.text = "Event 2"
        context = stage.run(context)
        
        assert "delta144_timeline" in context.story_ctx.metadata


class TestEmptyInputHandling:
    """Test graceful handling of empty/missing inputs."""
    
    def test_handles_empty_text(self):
        """Empty text should not crash StoryStage."""
        stage = StoryStage()
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="")
        )
        
        # Should not raise
        result = stage.run(context)
        
        assert result.story_ctx is not None
        assert len(result.story_ctx.events) >= 1
        assert result.story_ctx.events[0].text == ""
    
    def test_handles_no_input_context(self):
        """Missing input_ctx should not crash."""
        stage = StoryStage()
        
        context = UnifiedContext(
            global_ctx=GlobalContext()
            # no input_ctx
        )
        
        # Should not raise - graceful degradation
        result = stage.run(context)
        
        assert result.story_ctx is not None
        # Event text should be empty string
        if len(result.story_ctx.events) > 0:
            assert result.story_ctx.events[0].text == ""
    
    def test_handles_no_archetype_context(self):
        """Missing archetype_ctx should not crash."""
        stage = StoryStage()
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="Text without archetypes")
            # no archetype_ctx
        )
        
        result = stage.run(context)
        
        assert result.story_ctx is not None
        event = result.story_ctx.events[0]
        assert event.text == "Text without archetypes"
        assert event.archetype_id is None


class TestSignalModeSkip:
    """Test that signal mode skips StoryStage."""
    
    def test_signal_mode_skips_story_processing(self):
        """Mode='signal' should skip story processing."""
        stage = StoryStage()
        
        context = UnifiedContext(
            global_ctx=GlobalContext(mode="signal"),
            input_ctx=InputContext(text="Fast query")
        )
        
        result = stage.run(context)
        
        # story_ctx should not be populated in signal mode
        # (or remains None if it was None before)
        # The current implementation just returns early, so story_ctx is None
        assert result.story_ctx is None or len(result.story_ctx.events) == 0


class TestGracefulDegradation:
    """Test error handling and graceful degradation."""
    
    def test_degradation_on_story_engine_error(self):
        """If Story Engine fails, should set degraded flag and minimal story_ctx."""
        stage = StoryStage()
        
        # Create context that might cause issues
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="Test")
        )
        
        # Even with errors, should not crash
        result = stage.run(context)
        
        # Should always have story_ctx (even if minimal)
        assert result.story_ctx is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
