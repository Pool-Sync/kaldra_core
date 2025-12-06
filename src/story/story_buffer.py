"""
Story Buffer implementation for KALDRA v3.2.

Handles temporal event storage with sliding window capabilities.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Iterator
from datetime import datetime
import collections


@dataclass
class StoryEvent:
    """
    Single narrative event in the story buffer.
    """
    timestamp: datetime
    text: str
    archetype_id: Optional[str] = None        # Δ144 / Δ12 ID
    archetype_scores: Dict[str, float] = field(default_factory=dict)
    polarities: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)  # domain-specific (symbol, region, etc.)


@dataclass
class StoryBufferConfig:
    """Configuration for StoryBuffer."""
    max_events: int = 1000        # target capacity
    window_size: int = 200        # sliding window default


class StoryBuffer:
    """
    Persistent in-memory buffer for story events.
    
    Manages a sequence of StoryEvents with automatic eviction
    when capacity is reached.
    """
    
    def __init__(self, config: Optional[StoryBufferConfig] = None):
        self.config = config or StoryBufferConfig()
        # Use deque for efficient appends and pops from both ends if needed,
        # though we mainly append and popleft (FIFO).
        # However, random access is O(n) for deque in Python < 3.5, but O(1) for ends.
        # For random access by index, a list is better, but eviction is O(n).
        # Given max_events is ~1000, list overhead for eviction (pop(0)) is negligible.
        # Let's use a list for simplicity and O(1) random access, or a deque if we strictly enforce maxlen.
        # We'll use a list to support easy slicing and indexing.
        self._events: List[StoryEvent] = []

    def add_event(self, event: StoryEvent) -> None:
        """
        Append event and enforce max_events (drop oldest).
        
        Args:
            event: StoryEvent to add
        """
        self._events.append(event)
        
        # Enforce capacity
        if len(self._events) > self.config.max_events:
            # Remove oldest events to fit
            excess = len(self._events) - self.config.max_events
            self._events = self._events[excess:]

    def get_events(self) -> List[StoryEvent]:
        """
        Return all events ordered by timestamp (ascending).
        
        Returns:
            List of StoryEvent
        """
        # Assuming events are added in chronological order.
        # If strict sorting is needed, we could sort here, but for now we assume append order.
        return list(self._events)

    def get_window(self, size: Optional[int] = None) -> List[StoryEvent]:
        """
        Return last N events (sliding window).
        
        Args:
            size: Size of window. Defaults to config.window_size.
            
        Returns:
            List of StoryEvent in the window
        """
        window_size = size if size is not None else self.config.window_size
        if not self._events:
            return []
            
        return self._events[-window_size:]

    def get_event_by_index(self, idx: int) -> Optional[StoryEvent]:
        """
        Get event by index (0 is oldest).
        
        Args:
            idx: Index to retrieve
            
        Returns:
            StoryEvent or None if out of bounds
        """
        try:
            return self._events[idx]
        except IndexError:
            return None

    def iter_events(self) -> Iterator[StoryEvent]:
        """
        Iterate over all events.
        
        Yields:
            StoryEvent
        """
        yield from self._events

    def clear(self) -> None:
        """Reset buffer."""
        self._events.clear()

    def __len__(self) -> int:
        return len(self._events)
