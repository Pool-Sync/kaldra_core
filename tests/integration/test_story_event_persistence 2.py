"""
Integration tests for story events persistence.
"""
import pytest
from typing import Any, Dict, List
from src.unification.adapters.signal_adapter import SignalAdapter
from src.unification.states.unified_state import (
    UnifiedContext,
    GlobalContext,
    InputContext,
    StoryContext
)


class FakeStoryEventRepository:
    """Fake repository for testing."""
    
    def __init__(self) -> None:
        self.created_events: List[Dict[str, Any]] = []
        self.should_fail = False
    
    def create_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate event creation."""
        if self.should_fail:
            return {"error": 500, "message": "Simulated failure"}
        
        self.created_events.append(data)
        return data
    
    def bulk_create_events(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate bulk creation."""
        if self.should_fail:
            return {"error": 500, "message": "Simulated failure"}
        
        self.created_events.extend(events)
        return events


class FakeSignalRepository:
    """Fake signal repository."""
    
    def __init__(self) -> None:
        self.created = []
    
    def create_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self.created.append(data)
        return [data]  # Return as list like Supabase does


class TestStoryEventPersistence:
    """Test suite for story events persistence."""
    
    def test_story_events_persisted_when_context_has_events(self):
        """Test events are persisted when context has story events."""
        signal_repo = FakeSignalRepository()
        event_repo = FakeStoryEventRepository()
        
        adapter = SignalAdapter(
            signal_repository=signal_repo,
            story_event_repository=event_repo,
            enable_persistence=True,
            enable_story_events_persistence=True
        )
        
        # Create context with events
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="Test", bias_score=0.5)
        )
        story_ctx = StoryContext()
        story_ctx.events = [
            {"text": "First event", "stream_id": "test-stream"},
            {"text": "Second event", "stream_id": "test-stream"}
        ]
        context.story_ctx = story_ctx
        
        # Directly test persistence method
        adapter._persist_story_events(context, "test-signal-id")
        
        # Verify events were persisted
        assert len(event_repo.created_events) == 2
        assert event_repo.created_events[0]["text"] == "First event"
    
    def test_story_events_persistence_failure_does_not_break_pipeline(self):
        """Test that persistence failures don't break pipeline."""
        event_repo = FakeStoryEventRepository()
        event_repo.should_fail = True
        
        adapter = SignalAdapter(
            story_event_repository=event_repo,
            enable_persistence=False,
            enable_story_events_persistence=True
        )
        
        context = UnifiedContext(global_ctx=GlobalContext())
        story_ctx = StoryContext()
        story_ctx.events = [{"text": "Test"}]
        context.story_ctx = story_ctx
        
        # Should not raise exception
        adapter._persist_story_events(context, None)
        # Test passes if no exception raised
    
    def test_story_events_persistence_disabled(self):
        """Test with story events persistence disabled."""
        event_repo = FakeStoryEventRepository()
        
        adapter = SignalAdapter(
            story_event_repository=event_repo,
            enable_persistence=False,
            enable_story_events_persistence=False
        )
        
        context = UnifiedContext(global_ctx=GlobalContext())
        story_ctx = StoryContext()
        story_ctx.events = [{"text": "Test"}]
        context.story_ctx = story_ctx
        
        adapter._persist_story_events(context, None)
        
        # No events should be persisted
        assert len(event_repo.created_events) == 0
    
    def test_no_events_when_context_empty(self):
        """Test no persistence when context has no events."""
        event_repo = FakeStoryEventRepository()
        
        adapter = SignalAdapter(
            story_event_repository=event_repo,
            enable_persistence=False,
            enable_story_events_persistence=True
        )
        
        context = UnifiedContext(global_ctx=GlobalContext())
        
        adapter._persist_story_events(context, None)
        
        # No events should be created
        assert len(event_repo.created_events) == 0
    
    def test_story_events_linked_to_signal(self):
        """Test that story events are linked to parent signal."""
        signal_repo = FakeSignalRepository()
        event_repo = FakeStoryEventRepository()
        
        adapter = SignalAdapter(
            signal_repository=signal_repo,
            story_event_repository=event_repo,
            enable_persistence=True,  # Must be True for story events
            enable_story_events_persistence=True
        )
        
        context = UnifiedContext(global_ctx=GlobalContext())
        story_ctx = StoryContext()
        story_ctx.events = [{"text": "Linked"}]
        context.story_ctx = story_ctx
        
        adapter._persist_story_events(context, "my-signal-id")
        
        # Check signal_id was set
        assert len(event_repo.created_events) == 1
        assert event_repo.created_events[0]["signal_id"] == "my-signal-id"
