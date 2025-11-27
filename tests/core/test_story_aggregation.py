import numpy as np

from src.core.story_aggregator import StoryAggregator, StoryTurnSignal
from src.core.story_tracker import StoryTracker


class DummySignal:
    """
    Minimal dummy signal for testing StoryAggregator/StoryTracker.

    Provides:
      - archetype_probs
      - delta_state (optional)
      - tw_trigger (optional)
      - tw_stats (optional)
      - epistemic (with status)
    """

    class _Epistemic:
        def __init__(self, status: str) -> None:
            self.status = status

    def __init__(
        self,
        probs: np.ndarray,
        delta_state: dict | None = None,
        tw_trigger: bool | None = None,
        tw_severity: float | None = None,
        epistemic_status: str | None = "OK",
    ) -> None:
        self.archetype_probs = probs
        self.delta_state = delta_state
        self.tw_trigger = tw_trigger
        self.tw_stats = {"severity": tw_severity} if tw_severity is not None else None
        self.epistemic = self._Epistemic(epistemic_status) if epistemic_status is not None else None


def test_story_aggregator_basic():
    agg = StoryAggregator(top_k_archetypes=2)

    # Two turns with different dominant archetypes.
    probs1 = np.zeros(144, dtype=np.float32)
    probs1[10] = 0.9
    probs2 = np.zeros(144, dtype=np.float32)
    probs2[20] = 0.8

    turns = [
        {
            "turn_index": 0,
            "timestamp": "2025-11-27T10:00:00Z",
            "role": "user",
            "text": "First turn.",
            "signal": DummySignal(probs1, delta_state={"id": "S10", "profile": "EXPANSIVE"}),
        },
        {
            "turn_index": 1,
            "timestamp": "2025-11-27T10:01:00Z",
            "role": "assistant",
            "text": "Second turn.",
            "signal": DummySignal(probs2, delta_state={"id": "S20", "profile": "CONTRACTIVE"}),
        },
    ]

    story = agg.aggregate(story_id="story-123", turns=turns)

    assert story["story_id"] == "story-123"
    assert len(story["turns"]) == 2
    assert len(story["delta144_evolution"]) == 2
    assert 0.0 <= story["narrative_coherence"] <= 1.0
    assert len(story["dominant_archetypes"]) <= 2
    assert story["dominant_archetypes"][0] in (10, 20)


def test_story_tracker_lifecycle():
    tracker = StoryTracker()

    sid = tracker.create_story()
    assert sid in tracker.list_story_ids()

    probs = np.zeros(144, dtype=np.float32)
    probs[5] = 1.0

    tracker.add_turn(
        story_id=sid,
        role="user",
        text="Hello there.",
        signal=DummySignal(probs),
        timestamp="2025-11-27T10:00:00Z",
    )

    tracker.add_turn(
        story_id=sid,
        role="assistant",
        text="Hi, how can I help?",
        signal=DummySignal(probs),
        timestamp="2025-11-27T10:00:05Z",
    )

    turns = tracker.get_story_turns(sid)
    assert len(turns) == 2

    story = tracker.aggregate_story(sid)
    assert story["story_id"] == sid
    assert len(story["turns"]) == 2
    assert "narrative_coherence" in story
    assert "dominant_archetypes" in story

    tracker.reset_story(sid)
    assert tracker.get_story_turns(sid) == []


def test_story_turn_signal_from_signal():
    probs = np.ones(144, dtype=np.float32) / 144.0
    signal = DummySignal(probs, delta_state={"id": "S42"})
    sts = StoryTurnSignal.from_signal(signal)

    assert isinstance(sts.archetype_probs, np.ndarray)
    assert sts.archetype_probs.shape[0] == 144
    assert sts.delta_state is not None
    assert sts.delta_state.get("id") == "S42"
