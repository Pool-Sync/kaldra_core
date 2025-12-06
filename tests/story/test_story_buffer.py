"""
Tests for StoryBuffer.
"""

import pytest
from datetime import datetime, timedelta
from src.story.story_buffer import StoryBuffer, StoryBufferConfig, StoryEvent


class TestStoryBuffer:
    
    def test_add_event_respects_capacity(self):
        """Test that buffer respects max_events."""
        config = StoryBufferConfig(max_events=5)
        buffer = StoryBuffer(config)
        
        # Add 6 events
        for i in range(6):
            event = StoryEvent(
                timestamp=datetime.now(),
                text=f"Event {i}"
            )
            buffer.add_event(event)
            
        assert len(buffer) == 5
        # Should have dropped Event 0, so first should be Event 1
        assert buffer.get_events()[0].text == "Event 1"
        assert buffer.get_events()[-1].text == "Event 5"

    def test_get_window(self):
        """Test sliding window retrieval."""
        config = StoryBufferConfig(window_size=3)
        buffer = StoryBuffer(config)
        
        for i in range(5):
            buffer.add_event(StoryEvent(datetime.now(), f"Event {i}"))
            
        window = buffer.get_window()
        assert len(window) == 3
        assert window[0].text == "Event 2"
        assert window[-1].text == "Event 4"
        
        # Test custom window size
        small_window = buffer.get_window(size=2)
        assert len(small_window) == 2
        assert small_window[0].text == "Event 3"

    def test_get_event_by_index(self):
        """Test index access."""
        buffer = StoryBuffer()
        buffer.add_event(StoryEvent(datetime.now(), "First"))
        buffer.add_event(StoryEvent(datetime.now(), "Second"))
        
        assert buffer.get_event_by_index(0).text == "First"
        assert buffer.get_event_by_index(1).text == "Second"
        assert buffer.get_event_by_index(99) is None

    def test_clear(self):
        """Test clearing buffer."""
        buffer = StoryBuffer()
        buffer.add_event(StoryEvent(datetime.now(), "Test"))
        assert len(buffer) == 1
        buffer.clear()
        assert len(buffer) == 0
