"""
Story Buffer - Persistent narrative memory for KALDRA v2.6.

Maintains a sliding window of recent StoryEvents to enable temporal narrative analysis.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from collections import deque
import time
import uuid


@dataclass
class StoryEvent:
    """
    Single event in the narrative timeline.
    
    Captures complete KALDRA signal state at a moment in time.
    """
    event_id: str
    timestamp: float
    sequence_id: int
    text: str
    
    # Core KALDRA components
    delta12: Optional[Dict[str, float]] = None  # Delta12Vector as dict
    delta144_state: Optional[str] = None
    kindra: Optional[Dict[str, Any]] = None
    
    # Meta-engine scores (v2.5)
    meta_scores: Optional[Dict[str, Any]] = None  # Nietzsche/Aurelius/Campbell
    
    # TW369 state
    drift_state: Optional[Dict[str, Any]] = None  # DriftState as dict
    tw_state: Optional[Dict[str, Any]] = None  # TWState as dict
    
    # Polarity state (v2.7)
    polarity_scores: Optional[Dict[str, float]] = None
    
    # Optional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> StoryEvent:
        """Create from dictionary."""
        return cls(**data)


class StoryBuffer:
    """
    Sliding window buffer for narrative events.
    
    Maintains last N events for temporal analysis.
    Default capacity: 12 events (one full Campbell cycle).
    """
    
    def __init__(self, capacity: int = 12):
        """
        Initialize StoryBuffer.
        
        Args:
            capacity: Maximum number of events to store (default: 12)
        """
        self.capacity = capacity
        self._buffer: deque[StoryEvent] = deque(maxlen=capacity)
        self._sequence_counter = 0
    
    def add_event(
        self,
        text: str,
        delta12: Optional[Dict[str, float]] = None,
        delta144_state: Optional[str] = None,
        kindra: Optional[Dict[str, Any]] = None,
        meta_scores: Optional[Dict[str, Any]] = None,
        drift_state: Optional[Dict[str, Any]] = None,
        tw_state: Optional[Dict[str, Any]] = None,
        polarity_scores: Optional[Dict[str, float]] = None,  # v2.7
        metadata: Optional[Dict[str, Any]] = None
    ) -> StoryEvent:
        """
        Add new event to buffer.
        
        Args:
            text: Input text
            delta12: Delta12Vector as dict
            delta144_state: Current Δ144 state
            kindra: Kindra scores
            meta_scores: Meta-engine scores (Nietzsche/Aurelius/Campbell)
            drift_state: DriftState as dict
            tw_state: TWState as dict
            polarity_scores: Polarity scores (v2.7)
            metadata: Optional metadata
            
        Returns:
            Created StoryEvent
        """
        event = StoryEvent(
            event_id=str(uuid.uuid4()),
            timestamp=time.time(),
            sequence_id=self._sequence_counter,
            text=text,
            delta12=delta12,
            delta144_state=delta144_state,
            kindra=kindra,
            meta_scores=meta_scores,
            drift_state=drift_state,
            tw_state=tw_state,
            polarity_scores=polarity_scores,
            metadata=metadata or {}
        )
        
        self._buffer.append(event)
        self._sequence_counter += 1
        
        return event
    
    def get_recent(self, n: int) -> List[StoryEvent]:
        """
        Get N most recent events.
        
        Args:
            n: Number of events to retrieve
            
        Returns:
            List of recent events (newest first)
        """
        if n <= 0:
            return []
        
        # Return last n events, reversed (newest first)
        return list(reversed(list(self._buffer)[-n:]))
    
    def get_timeline(self) -> List[StoryEvent]:
        """
        Get complete timeline (all events in buffer).
        
        Returns:
            List of all events (oldest first)
        """
        return list(self._buffer)
    
    def clear(self):
        """Clear all events from buffer."""
        self._buffer.clear()
        self._sequence_counter = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize buffer to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "capacity": self.capacity,
            "sequence_counter": self._sequence_counter,
            "events": [event.to_dict() for event in self._buffer]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> StoryBuffer:
        """
        Deserialize buffer from dictionary.
        
        Args:
            data: Dictionary representation
            
        Returns:
            Reconstructed StoryBuffer
        """
        buffer = cls(capacity=data["capacity"])
        buffer._sequence_counter = data["sequence_counter"]
        
        for event_data in data["events"]:
            event = StoryEvent.from_dict(event_data)
            buffer._buffer.append(event)
        
        return buffer
    
    def __len__(self) -> int:
        """Get number of events in buffer."""
        return len(self._buffer)
    
    def __repr__(self) -> str:
        return f"StoryBuffer(capacity={self.capacity}, events={len(self._buffer)})"
