"""
Story event record model for Supabase.
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class StoryEventRecord:
    """
    Narrative event associated with a signal.
    
    Attributes:
        id: Unique identifier
        created_at: Creation timestamp
        signal_id: Parent signal ID
        stream_id: Stream identifier (nyt, twitter, etc.)
        text: Event text content
        delta144_state: Delta144 state for this event
        polarities: Polarity scores dict
        meta: Additional metadata
    """
    id: str
    created_at: Optional[datetime]
    signal_id: str
    
    stream_id: Optional[str] = None
    text: Optional[str] = None
    
    delta144_state: Optional[str] = None
    polarities: Optional[Dict[str, float]] = None
    meta: Optional[Dict[str, Any]] = None
