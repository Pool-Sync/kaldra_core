"""
Story event record model for Supabase.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


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
    created_at: datetime | None
    signal_id: str

    stream_id: str | None = None
    text: str | None = None

    delta144_state: str | None = None
    polarities: dict[str, float] | None = None
    meta: dict[str, Any] | None = None
