"""
Tests for StoryAggregator.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from story.story_buffer import StoryBuffer
from story.story_aggregator import (
    aggregate_story,
    compute_narrative_motion,
    detect_inflection_points,
    detect_arc_progression,
)


def test_compute_narrative_motion():
    """Test motion vector computation between two events."""
    buffer = StoryBuffer(capacity=10)
    
    event1 = buffer.add_event(
        "First event",
        delta12={"A01_INNOCENT": 0.7, "A02_ORPHAN": 0.3},
        delta144_state="A01_INNOCENT_1_01",
        drift_state={"drift_metric": 0.3}
    )
    
    event2 = buffer.add_event(
        "Second event",
        delta12={"A01_INNOCENT": 0.3, "A03_WARRIOR": 0.7},
        delta144_state="A03_WARRIOR_3_05",
        drift_state={"drift_metric": 0.6}
    )
    
    motion = compute_narrative_motion(event1, event2)
    
    assert motion.from_event_id == event1.event_id
    assert motion.to_event_id == event2.event_id
    assert motion.delta12_shift_magnitude > 0
    assert motion.delta144_transition == ("A01_INNOCENT_1_01", "A03_WARRIOR_3_05")
    assert motion.drift_velocity > 0  # Drift increased


def test_aggregate_story_empty_buffer():
    """Test aggregation with empty buffer."""
    buffer = StoryBuffer(capacity=10)
    
    aggregation = aggregate_story(buffer)
    
    assert aggregation.total_events == 0
    assert len(aggregation.motion_vectors) == 0
    assert len(aggregation.inflection_points) == 0


def test_aggregate_story_with_events():
    """Test aggregation with multiple events."""
    buffer = StoryBuffer(capacity=10)
    
    # Add 5 events
    for i in range(5):
        buffer.add_event(
            f"Event {i}",
            delta12={"A01_INNOCENT": 0.5 + i * 0.1},
            drift_state={"drift_metric": 0.2 + i * 0.15}
        )
    
    aggregation = aggregate_story(buffer)
    
    assert aggregation.total_events == 5
    assert len(aggregation.motion_vectors) == 4  # n-1 vectors
    assert aggregation.time_span > 0


def test_detect_inflection_points_drift_peak():
    """Test drift peak detection."""
    buffer = StoryBuffer(capacity=10)
    
    # Create drift peak pattern: 0.3 → 0.8 → 0.4
    buffer.add_event("Event 1", drift_state={"drift_metric": 0.3})
    buffer.add_event("Event 2", drift_state={"drift_metric": 0.8})  # Peak
    buffer.add_event("Event 3", drift_state={"drift_metric": 0.4})
    
    timeline = buffer.get_timeline()
    inflections = detect_inflection_points(timeline)
    
    # Should detect peak
    drift_peaks = [inf for inf in inflections if inf.inflection_type == "drift_peak"]
    assert len(drift_peaks) > 0
    assert drift_peaks[0].magnitude == 0.8


def test_detect_inflection_points_archetype_shift():
    """Test archetype shift detection."""
    buffer = StoryBuffer(capacity=10)
    
    buffer.add_event(
        "Event 1",
        delta12={"A01_INNOCENT": 0.9, "A02_ORPHAN": 0.1}
    )
    buffer.add_event(
        "Event 2",
        delta12={"A01_INNOCENT": 0.2, "A03_WARRIOR": 0.8}  # Major shift
    )
    buffer.add_event(
        "Event 3",
        delta12={"A03_WARRIOR": 0.85, "A01_INNOCENT": 0.15}
    )
    
    timeline = buffer.get_timeline()
    inflections = detect_inflection_points(timeline)
    
    # Should detect archetype shift (shift magnitude > 0.3)
    shifts = [inf for inf in inflections if inf.inflection_type == "archetype_shift"]
    assert len(shifts) >= 1  # At least one shift detected


def test_detect_arc_progression():
    """Test Campbell arc progression detection."""
    buffer = StoryBuffer(capacity=10)
    
    # Add events with Campbell stages
    buffer.add_event(
        "Event 1",
        meta_scores={
            "campbell": {"stage": "ordinary_world", "confidence": 0.8}
        }
    )
    buffer.add_event(
        "Event 2",
        meta_scores={
            "campbell": {"stage": "call_to_adventure", "confidence": 0.7}
        }
    )
    buffer.add_event(
        "Event 3",
        meta_scores={
            "campbell": {"stage": "tests_allies_enemies", "confidence": 0.75}
        }
    )
    
    arc = detect_arc_progression(buffer)
    
    assert arc is not None
    assert arc.current_stage == "tests_allies_enemies"
    assert arc.stage_confidence == 0.75
    assert 0.0 <= arc.arc_progress <= 1.0
    assert len(arc.stage_history) == 3


def test_drift_trajectory_computation():
    """Test drift trajectory analysis."""
    buffer = StoryBuffer(capacity=10)
    
    # Add events with increasing drift
    for i in range(5):
        buffer.add_event(
            f"Event {i}",
            drift_state={"drift_metric": 0.2 + i * 0.1}
        )
    
    aggregation = aggregate_story(buffer)
    
    assert aggregation.drift_trajectory is not None
    assert len(aggregation.drift_trajectory.drift_values) == 5
    assert aggregation.drift_trajectory.drift_slope > 0  # Increasing trend


def test_narrative_oscillation_index():
    """Test narrative oscillation computation."""
    buffer = StoryBuffer(capacity=10)
    
    # Create oscillating drift pattern
    drift_values = [0.3, 0.5, 0.4, 0.6, 0.45, 0.65]
    for i, drift in enumerate(drift_values):
        buffer.add_event(f"Event {i}", drift_state={"drift_metric": drift})
    
    aggregation = aggregate_story(buffer)
    
    # Should detect oscillations
    assert aggregation.narrative_oscillation_index >= 0.0


def test_meta_score_deltas():
    """Test meta-score delta computation."""
    buffer = StoryBuffer(capacity=10)
    
    event1 = buffer.add_event(
        "Event 1",
        meta_scores={
            "nietzsche": {"will_to_power": 0.5, "amor_fati": 0.4}
        }
    )
    
    event2 = buffer.add_event(
        "Event 2",
        meta_scores={
            "nietzsche": {"will_to_power": 0.8, "amor_fati": 0.6}
        }
    )
    
    motion = compute_narrative_motion(event1, event2)
    
    assert "nietzsche" in motion.meta_deltas
    assert motion.meta_deltas["nietzsche"] > 0  # Increased
