"""
Unit tests for MultiStreamBuffer.

Tests cover:
- Stream creation and event addition
- Per-stream and global limits
- Window retrieval
- Stream listing and clearing
"""
import pytest
import time
from src.story.multi_stream_buffer import MultiStreamBuffer, StreamWindow
from src.common.unified_signal import StoryEvent


def create_test_event(
    event_id: str,
    stream_id: str,
    timestamp: float = None,
    sequence_id: int = 0,
    text: str = "test"
) -> StoryEvent:
    """Helper to create a test StoryEvent."""
    return StoryEvent(
        event_id=event_id,
        timestamp=timestamp or time.time(),
        sequence_id=sequence_id,
        text=text,
        stream_id=stream_id
    )


class TestMultiStreamBuffer:
    """Test suite for MultiStreamBuffer."""
    
    def test_add_event_creates_streams(self):
        """Test that adding events creates separate streams."""
        buffer = MultiStreamBuffer()
        
        event1 = create_test_event("e1", "nyt", timestamp=1.0)
        event2 = create_test_event("e2", "twitter", timestamp=2.0)
        event3 = create_test_event("e3", "nyt", timestamp=3.0)
        
        buffer.add_event(event1)
        buffer.add_event(event2)
        buffer.add_event(event3)
        
        assert buffer.stream_count == 2
        assert set(buffer.list_streams()) == {"nyt", "twitter"}
        assert buffer.total_events == 3
    
    def test_default_stream_for_none(self):
        """Test that events with stream_id=None go to 'default'."""
        buffer = MultiStreamBuffer()
        
        event = create_test_event("e1", stream_id=None, timestamp=1.0)
        buffer.add_event(event)
        
        assert "default" in buffer.list_streams()
        assert buffer.total_events == 1
    
    def test_respects_max_events_per_stream(self):
        """Test that per-stream limit is enforced (FIFO)."""
        buffer = MultiStreamBuffer(max_events_per_stream=3)
        
        # Add 5 events to same stream
        for i in range(5):
            event = create_test_event(f"e{i}", "nyt", timestamp=float(i))
            buffer.add_event(event)
        
        # Should only have the last 3
        window = buffer.get_window("nyt", size=10)
        assert len(window.events) == 3
        assert window.events[0].event_id == "e2"
        assert window.events[-1].event_id == "e4"
    
    def test_respects_global_max_events(self):
        """Test that global limit is enforced across all streams."""
        buffer = MultiStreamBuffer(
            max_events_per_stream=10,
            global_max_events=5
        )
        
        # Add events to multiple streams
        for i in range(3):
            buffer.add_event(create_test_event(f"nyt{i}", "nyt", timestamp=float(i)))
        for i in range(3):
            buffer.add_event(create_test_event(f"twitter{i}", "twitter", timestamp=float(i + 10)))
        
        # Should have evicted oldest event(s) to stay at 5
        assert buffer.total_events == 5
    
    def test_get_window_returns_latest_events(self):
        """Test that get_window returns the most recent N events."""
        buffer = MultiStreamBuffer()
        
        # Add 5 events to a stream
        for i in range(5):
            event = create_test_event(f"e{i}", "nyt", timestamp=float(i), sequence_id=i)
            buffer.add_event(event)
        
        # Request window of size 3
        window = buffer.get_window("nyt", size=3)
        
        assert len(window.events) == 3
        assert window.stream_id == "nyt"
        assert window.events[0].sequence_id == 2
        assert window.events[-1].sequence_id == 4
    
    def test_get_window_handles_missing_stream(self):
        """Test that get_window returns empty for non-existent stream."""
        buffer = MultiStreamBuffer()
        window = buffer.get_window("nonexistent", size=10)
        
        assert window.stream_id == "nonexistent"
        assert len(window.events) == 0
    
    def test_get_window_returns_all_if_fewer_than_size(self):
        """Test that get_window returns all events if fewer than requested."""
        buffer = MultiStreamBuffer()
        
        buffer.add_event(create_test_event("e1", "nyt", timestamp=1.0))
        buffer.add_event(create_test_event("e2", "nyt", timestamp=2.0))
        
        window = buffer.get_window("nyt", size=10)
        assert len(window.events) == 2
    
    def test_get_all_windows(self):
        """Test that get_all_windows returns windows for all streams."""
        buffer = MultiStreamBuffer()
        
        buffer.add_event(create_test_event("e1", "nyt", timestamp=1.0))
        buffer.add_event(create_test_event("e2", "twitter", timestamp=2.0))
        buffer.add_event(create_test_event("e3", "nyt", timestamp=3.0))
        
        windows = buffer.get_all_windows(size=10)
        
        assert len(windows) == 2
        stream_ids = {w.stream_id for w in windows}
        assert stream_ids == {"nyt", "twitter"}
        
        # Find NYT window and verify it has 2 events
        nyt_window = next(w for w in windows if w.stream_id == "nyt")
        assert len(nyt_window.events) == 2
    
    def test_list_streams(self):
        """Test that list_streams returns all stream IDs."""
        buffer = MultiStreamBuffer()
        
        buffer.add_event(create_test_event("e1", "nyt", timestamp=1.0))
        buffer.add_event(create_test_event("e2", "twitter", timestamp=2.0))
        buffer.add_event(create_test_event("e3", "reddit", timestamp=3.0))
        
        streams = buffer.list_streams()
        assert set(streams) == {"nyt", "twitter", "reddit"}
    
    def test_clear_stream(self):
        """Test that clear_stream removes all events from a stream."""
        buffer = MultiStreamBuffer()
        
        buffer.add_event(create_test_event("e1", "nyt", timestamp=1.0))
        buffer.add_event(create_test_event("e2", "twitter", timestamp=2.0))
        buffer.add_event(create_test_event("e3", "nyt", timestamp=3.0))
        
        assert buffer.total_events == 3
        
        buffer.clear_stream("nyt")
        
        assert buffer.total_events == 1
        assert buffer.stream_count == 1
        assert "nyt" not in buffer.list_streams()
        assert "twitter" in buffer.list_streams()
    
    def test_clear_all(self):
        """Test that clear_all removes everything."""
        buffer = MultiStreamBuffer()
        
        buffer.add_event(create_test_event("e1", "nyt", timestamp=1.0))
        buffer.add_event(create_test_event("e2", "twitter", timestamp=2.0))
        
        buffer.clear_all()
        
        assert buffer.total_events == 0
        assert buffer.stream_count == 0
        assert len(buffer.list_streams()) == 0
    
    def test_empty_streams_handled_gracefully(self):
        """Test that operations on empty buffer don't fail."""
        buffer = MultiStreamBuffer()
        
        assert buffer.total_events == 0
        assert buffer.stream_count == 0
        assert buffer.list_streams() == []
        
        window = buffer.get_window("any", size=10)
        assert len(window.events) == 0
        
        windows = buffer.get_all_windows(size=10)
        assert len(windows) == 0
        
        buffer.clear_all()  # Should not raise
        assert buffer.total_events == 0
