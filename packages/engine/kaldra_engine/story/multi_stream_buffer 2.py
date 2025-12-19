"""
Multi-Stream Buffer for KALDRA v3.3 Phase 2.

Maintains separate buffers of StoryEvents for different streams (e.g., NYT, Twitter)
and provides windowed access for cross-stream comparison.
"""
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from src.common.unified_signal import StoryEvent


@dataclass
class StreamWindow:
    """
    A window of events from a single stream.
    
    Attributes:
        stream_id: Identifier for the stream (e.g., "nyt", "twitter")
        events: List of StoryEvents in this window
    """
    stream_id: str
    events: List[StoryEvent]


class MultiStreamBuffer:
    """
    Manages separate event buffers for multiple narrative streams.
    
    Features:
    - Per-stream FIFO buffers with configurable limits
    - Global event limit across all streams
    - Windowed access for comparison
    
    Example:
        >>> buffer = MultiStreamBuffer(max_events_per_stream=100)
        >>> buffer.add_event(event1)  # event1.stream_id = "nyt"
        >>> buffer.add_event(event2)  # event2.stream_id = "twitter"
        >>> window = buffer.get_window("nyt", size=10)
        >>> all_windows = buffer.get_all_windows(size=10)
    """
    
    def __init__(
        self,
        max_events_per_stream: int = 500,
        global_max_events: int = 5000
    ):
        """
        Initialize the multi-stream buffer.
        
        Args:
            max_events_per_stream: Maximum events to keep per stream (FIFO)
            global_max_events: Maximum total events across all streams
        """
        self._max_events_per_stream = max_events_per_stream
        self._global_max_events = global_max_events
        self._streams: Dict[str, deque[StoryEvent]] = {}
        self._total_events = 0
    
    def add_event(self, event: StoryEvent) -> None:
        """
        Add an event to the appropriate stream buffer.
        
        Args:
            event: StoryEvent to add. If stream_id is None, uses "default"
        """
        stream_id = event.stream_id or "default"
        
        # Create stream buffer if it doesn't exist
        if stream_id not in self._streams:
            self._streams[stream_id] = deque()
        
        # Add event to stream buffer
        stream_buffer = self._streams[stream_id]
        stream_buffer.append(event)
        self._total_events += 1
        
        # Enforce per-stream limit
        if len(stream_buffer) > self._max_events_per_stream:
            stream_buffer.popleft()
            self._total_events -= 1
        
        # Enforce global limit (remove oldest events from oldest streams)
        while self._total_events > self._global_max_events:
            self._evict_oldest_event()
    
    def _evict_oldest_event(self) -> None:
        """
        Remove the oldest event across all streams.
        Strategy: Find the stream with the oldest event and remove it.
        """
        oldest_stream = None
        oldest_timestamp = float('inf')
        
        for stream_id, buffer in self._streams.items():
            if buffer and buffer[0].timestamp < oldest_timestamp:
                oldest_timestamp = buffer[0].timestamp
                oldest_stream = stream_id
        
        if oldest_stream:
            self._streams[oldest_stream].popleft()
            self._total_events -= 1
            
            # Clean up empty streams
            if not self._streams[oldest_stream]:
                del self._streams[oldest_stream]
    
    def get_window(self, stream_id: str, size: int) -> StreamWindow:
        """
        Get the latest N events from a specific stream.
        
        Args:
            stream_id: Stream identifier
            size: Number of events to retrieve (returns fewer if not available)
        
        Returns:
            StreamWindow with the requested events
        """
        if stream_id not in self._streams:
            return StreamWindow(stream_id=stream_id, events=[])
        
        buffer = self._streams[stream_id]
        # Get last N events (or all if fewer than N)
        events = list(buffer)[-size:] if size < len(buffer) else list(buffer)
        
        return StreamWindow(stream_id=stream_id, events=events)
    
    def get_all_windows(self, size: int) -> List[StreamWindow]:
        """
        Get windows for all known streams.
        
        Args:
            size: Window size for each stream
        
        Returns:
            List of StreamWindow objects, one per stream
        """
        return [
            self.get_window(stream_id, size)
            for stream_id in self._streams.keys()
        ]
    
    def list_streams(self) -> List[str]:
        """
        Get list of all known stream IDs.
        
        Returns:
            List of stream identifiers
        """
        return list(self._streams.keys())
    
    def clear_stream(self, stream_id: str) -> None:
        """
        Clear all events from a specific stream.
        
        Args:
            stream_id: Stream to clear
        """
        if stream_id in self._streams:
            count = len(self._streams[stream_id])
            del self._streams[stream_id]
            self._total_events -= count
    
    def clear_all(self) -> None:
        """Clear all streams and reset counters."""
        self._streams.clear()
        self._total_events = 0
    
    @property
    def total_events(self) -> int:
        """Get total number of events across all streams."""
        return self._total_events
    
    @property
    def stream_count(self) -> int:
        """Get number of active streams."""
        return len(self._streams)
