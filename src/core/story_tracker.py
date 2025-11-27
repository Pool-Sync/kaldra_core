"""
Story tracking and session management for KALDRA Core.

This module provides an in-memory StoryTracker that groups multiple
turn-level signals into stories and delegates aggregation to
StoryAggregator.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from src.core.story_aggregator import StoryAggregator, StoryTurnSignal


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class StoryTurn:
    story_id: str
    turn_index: int
    timestamp: str
    role: str
    text: str
    signal: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    turn_id: str = field(default_factory=lambda: uuid.uuid4().hex)


class StoryTracker:
    """
    In-memory story tracking for multi-turn narrative aggregation.

    This is intentionally minimal and can be replaced by a persistent or
    distributed implementation in future versions.
    """

    def __init__(self, aggregator: Optional[StoryAggregator] = None) -> None:
        self._stories: Dict[str, List[StoryTurn]] = {}
        self.aggregator = aggregator or StoryAggregator()

    # -------------------------
    # Story lifecycle
    # -------------------------

    def create_story(self, story_id: Optional[str] = None) -> str:
        """
        Create a new story. Returns the story_id.
        """
        sid = story_id or uuid.uuid4().hex
        if sid not in self._stories:
            self._stories[sid] = []
        return sid

    def add_turn(
        self,
        story_id: str,
        role: str,
        text: str,
        signal: Any,
        timestamp: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> StoryTurn:
        """
        Append a new turn to an existing story.

        Args:
            story_id: Existing story identifier (created via create_story()).
            role: Role label (e.g. 'user', 'assistant', 'system').
            text: Narrative text for this turn.
            signal: KaldraSignal-like object (or StoryTurnSignal).
            timestamp: Optional ISO string. If None, uses current UTC.
            metadata: Optional turn-level metadata.

        Returns:
            StoryTurn instance.
        """
        if story_id not in self._stories:
            raise KeyError(f"Unknown story_id: {story_id}")

        ts = timestamp or _now_iso()
        turns = self._stories[story_id]
        turn_index = len(turns)

        turn = StoryTurn(
            story_id=story_id,
            turn_index=turn_index,
            timestamp=ts,
            role=role,
            text=text,
            signal=signal,
            metadata=metadata or {},
        )
        turns.append(turn)
        return turn

    def get_story_turns(self, story_id: str) -> List[StoryTurn]:
        """
        Return the list of StoryTurn objects for a given story_id.
        """
        return list(self._stories.get(story_id, []))

    def aggregate_story(self, story_id: str) -> Dict[str, Any]:
        """
        Aggregate a story into a schema-compatible object via StoryAggregator.
        """
        if story_id not in self._stories:
            raise KeyError(f"Unknown story_id: {story_id}")

        turns = self._stories[story_id]
        turns_payload: List[Dict[str, Any]] = []
        for t in turns:
            turns_payload.append(
                {
                    "turn_id": t.turn_id,
                    "turn_index": t.turn_index,
                    "timestamp": t.timestamp,
                    "role": t.role,
                    "text": t.text,
                    "metadata": t.metadata,
                    "signal": t.signal,
                }
            )

        return self.aggregator.aggregate(story_id=story_id, turns=turns_payload)

    def reset_story(self, story_id: str) -> None:
        """
        Remove all turns from a story, keeping the story_id.
        """
        if story_id in self._stories:
            self._stories[story_id] = []

    def delete_story(self, story_id: str) -> None:
        """
        Delete a story entirely.
        """
        self._stories.pop(story_id, None)

    def list_story_ids(self) -> List[str]:
        """
        List all known story IDs.
        """
        return list(self._stories.keys())
