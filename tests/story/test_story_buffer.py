"""
Tests for StoryBuffer and StoryEvent.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from story.story_buffer import StoryBuffer, StoryEvent


def test_story_event_creation():
    """Test StoryEvent creation."""
    event = StoryEvent(
        event_id="test-123",
        timestamp=1234567890.0,
        sequence_id=0,
        text="Test event",
        delta12={"A01_INNOCENT": 0.5, "A02_ORPHAN": 0.3},
        delta144_state="A01_INNOCENT_1_01"
    )
    
    assert event.event_id == "test-123"
    assert event.text == "Test event"
    assert event.delta12["A01_INNOCENT"] == 0.5


def test_story_event_serialization():
    """Test StoryEvent to_dict/from_dict."""
    event = StoryEvent(
        event_id="test-456",
        timestamp=1234567890.0,
        sequence_id=1,
        text="Serialize me",
        meta_scores={"nietzsche": {"will_to_power": 0.8}}
    )
    
    # Serialize
    data = event.to_dict()
    assert data["event_id"] == "test-456"
    assert data["text"] == "Serialize me"
    
    # Deserialize
    restored = StoryEvent.from_dict(data)
    assert restored.event_id == event.event_id
    assert restored.text == event.text
    assert restored.meta_scores == event.meta_scores


def test_story_buffer_creation():
    """Test StoryBuffer initialization."""
    buffer = StoryBuffer(capacity=10)
    
    assert buffer.capacity == 10
    assert len(buffer) == 0


def test_story_buffer_add_event():
    """Test adding events to buffer."""
    buffer = StoryBuffer(capacity=5)
    
    event1 = buffer.add_event("First event", delta12={"A01_INNOCENT": 1.0})
    event2 = buffer.add_event("Second event", delta12={"A02_ORPHAN": 1.0})
    
    assert len(buffer) == 2
    assert event1.sequence_id == 0
    assert event2.sequence_id == 1
    assert event1.text == "First event"


def test_story_buffer_overflow():
    """Test buffer overflow (sliding window)."""
    buffer = StoryBuffer(capacity=3)
    
    # Add 5 events (capacity is 3)
    for i in range(5):
        buffer.add_event(f"Event {i}")
    
    # Should only have last 3
    assert len(buffer) == 3
    
    timeline = buffer.get_timeline()
    assert timeline[0].text == "Event 2"  # Oldest kept
    assert timeline[2].text == "Event 4"  # Newest


def test_story_buffer_get_recent():
    """Test get_recent() method."""
    buffer = StoryBuffer(capacity=10)
    
    for i in range(5):
        buffer.add_event(f"Event {i}")
    
    # Get 3 most recent (newest first)
    recent = buffer.get_recent(3)
    
    assert len(recent) == 3
    assert recent[0].text == "Event 4"  # Newest
    assert recent[1].text == "Event 3"
    assert recent[2].text == "Event 2"


def test_story_buffer_get_timeline():
    """Test get_timeline() method."""
    buffer = StoryBuffer(capacity=10)
    
    for i in range(4):
        buffer.add_event(f"Event {i}")
    
    # Get all events (oldest first)
    timeline = buffer.get_timeline()
    
    assert len(timeline) == 4
    assert timeline[0].text == "Event 0"  # Oldest
    assert timeline[3].text == "Event 3"  # Newest


def test_story_buffer_clear():
    """Test clear() method."""
    buffer = StoryBuffer(capacity=10)
    
    for i in range(5):
        buffer.add_event(f"Event {i}")
    
    assert len(buffer) == 5
    
    buffer.clear()
    
    assert len(buffer) == 0
    assert buffer._sequence_counter == 0


def test_story_buffer_serialization():
    """Test buffer to_dict/from_dict."""
    buffer = StoryBuffer(capacity=5)
    
    buffer.add_event("Event 1", delta12={"A01_INNOCENT": 0.7})
    buffer.add_event("Event 2", delta12={"A02_ORPHAN": 0.6})
    
    # Serialize
    data = buffer.to_dict()
    assert data["capacity"] == 5
    assert len(data["events"]) == 2
    
    # Deserialize
    restored = StoryBuffer.from_dict(data)
    assert restored.capacity == 5
    assert len(restored) == 2
    assert restored.get_timeline()[0].text == "Event 1"
    assert restored.get_timeline()[1].text == "Event 2"


def test_story_buffer_with_full_kaldra_signal():
    """Test buffer with complete KALDRA signal."""
    buffer = StoryBuffer(capacity=12)
    
    event = buffer.add_event(
        text="Complete signal test",
        delta12={"A01_INNOCENT": 0.3, "A07_RULER": 0.4, "A10_SAGE": 0.3},
        delta144_state="A07_RULER_6_05",
        kindra={"layer1": [0.1] * 48},
        meta_scores={
            "nietzsche": {"will_to_power": 0.7, "amor_fati": 0.5},
            "aurelius": {"serenity": 0.6, "discipline_of_will": 0.7},
            "campbell": {"stage": "tests", "confidence": 0.65}
        },
        drift_state={"drift_metric": 0.45},
        tw_state={"severity": 0.52, "plane": "6"}
    )
    
    assert event.delta12["A07_RULER"] == 0.4
    assert event.meta_scores["nietzsche"]["will_to_power"] == 0.7
    assert event.tw_state["plane"] == "6"
