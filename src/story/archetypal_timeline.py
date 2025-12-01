"""
Archetypal Timeline Engine - Δ12/Δ144 evolution tracking for KALDRA v2.6.

Tracks archetypal evolution over time with motion metrics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import math

from .story_buffer import StoryBuffer, StoryEvent


@dataclass
class TimelinePoint:
    """Single point in archetypal timeline."""
    sequence_id: int
    timestamp: float
    delta12_dominant: str
    delta12_probability: float
    delta144_state: str
    drift_level: float


@dataclass
class ArchetypalLoop:
    """Detected loop in archetypal progression."""
    start_sequence: int
    end_sequence: int
    archetype: str
    loop_count: int
    average_duration: float  # Average time per loop


@dataclass
class ArchetypalTimeline:
    """
    Complete archetypal timeline with metrics.
    """
    points: List[TimelinePoint]
    
    # Metrics
    total_shifts: int  # Number of dominant archetype changes
    average_shift_magnitude: float
    trajectory_curvature: float  # How "curved" the path is
    archetype_persistence_score: float  # How stable archetypes are
    
    # Detected patterns
    loops: List[ArchetypalLoop] = field(default_factory=list)


def build_timeline(buffer: StoryBuffer) -> ArchetypalTimeline:
    """
    Build archetypal timeline from buffer.
    
    Args:
        buffer: StoryBuffer with events
        
    Returns:
        ArchetypalTimeline with complete analysis
    """
    timeline_events = buffer.get_timeline()
    
    if len(timeline_events) == 0:
        return ArchetypalTimeline(
            points=[],
            total_shifts=0,
            average_shift_magnitude=0.0,
            trajectory_curvature=0.0,
            archetype_persistence_score=0.0
        )
    
    # Build timeline points
    points = []
    for event in timeline_events:
        point = _event_to_timeline_point(event)
        if point:
            points.append(point)
    
    # Compute metrics
    total_shifts = _count_archetype_shifts(points)
    avg_shift_magnitude = _compute_average_shift_magnitude(timeline_events)
    curvature = compute_trajectory_curvature(timeline_events)
    persistence = _compute_persistence_score(points)
    
    # Detect loops
    loops = detect_archetypal_loops(ArchetypalTimeline(
        points=points,
        total_shifts=total_shifts,
        average_shift_magnitude=avg_shift_magnitude,
        trajectory_curvature=curvature,
        archetype_persistence_score=persistence
    ))
    
    return ArchetypalTimeline(
        points=points,
        total_shifts=total_shifts,
        average_shift_magnitude=avg_shift_magnitude,
        trajectory_curvature=curvature,
        archetype_persistence_score=persistence,
        loops=loops
    )


def compute_shift_magnitude(prev: Dict[str, float], curr: Dict[str, float]) -> float:
    """
    Compute Δ12 shift magnitude between two vectors.
    
    Args:
        prev: Previous Δ12 vector
        curr: Current Δ12 vector
        
    Returns:
        Euclidean distance
    """
    all_keys = set(prev.keys()) | set(curr.keys())
    
    squared_diff = sum((curr.get(k, 0.0) - prev.get(k, 0.0)) ** 2 for k in all_keys)
    
    return math.sqrt(squared_diff)


def compute_trajectory_curvature(events: List[StoryEvent]) -> float:
    """
    Compute trajectory curvature in Δ12 space.
    
    Measures how "curved" the archetypal path is.
    High curvature = lots of direction changes.
    
    Args:
        events: List of StoryEvents
        
    Returns:
        Curvature metric (0.0-1.0)
    """
    if len(events) < 3:
        return 0.0
    
    # Compute angles between consecutive motion vectors
    angles = []
    
    for i in range(len(events) - 2):
        if not (events[i].delta12 and events[i+1].delta12 and events[i+2].delta12):
            continue
        
        # Vectors: v1 = (i → i+1), v2 = (i+1 → i+2)
        v1 = _delta12_to_vector(events[i].delta12, events[i+1].delta12)
        v2 = _delta12_to_vector(events[i+1].delta12, events[i+2].delta12)
        
        # Compute angle between vectors
        angle = _vector_angle(v1, v2)
        angles.append(angle)
    
    if not angles:
        return 0.0
    
    # Average absolute angle (normalized to 0-1)
    avg_angle = sum(abs(a) for a in angles) / len(angles)
    curvature = avg_angle / math.pi  # Normalize to [0, 1]
    
    return min(1.0, curvature)


def detect_archetypal_loops(timeline: ArchetypalTimeline) -> List[ArchetypalLoop]:
    """
    Detect loops in archetypal progression.
    
    A loop is when the same dominant archetype appears multiple times
    with similar patterns.
    
    Args:
        timeline: ArchetypalTimeline
        
    Returns:
        List of detected loops
    """
    if len(timeline.points) < 4:
        return []
    
    loops = []
    
    # Track archetype occurrences
    archetype_occurrences: Dict[str, List[int]] = {}
    
    for point in timeline.points:
        arch = point.delta12_dominant
        if arch not in archetype_occurrences:
            archetype_occurrences[arch] = []
        archetype_occurrences[arch].append(point.sequence_id)
    
    # Detect loops (archetype appears 3+ times)
    for archetype, sequences in archetype_occurrences.items():
        if len(sequences) >= 3:
            # Compute average duration between occurrences
            durations = []
            for i in range(len(sequences) - 1):
                duration = sequences[i+1] - sequences[i]
                durations.append(duration)
            
            avg_duration = sum(durations) / len(durations) if durations else 0.0
            
            loops.append(ArchetypalLoop(
                start_sequence=sequences[0],
                end_sequence=sequences[-1],
                archetype=archetype,
                loop_count=len(sequences),
                average_duration=avg_duration
            ))
    
    return loops


# Helper functions

def _event_to_timeline_point(event: StoryEvent) -> Optional[TimelinePoint]:
    """Convert StoryEvent to TimelinePoint."""
    if not event.delta12:
        return None
    
    # Find dominant archetype
    dominant_arch = max(event.delta12.items(), key=lambda x: x[1])
    
    # Get drift level
    drift_level = 0.0
    if event.drift_state:
        drift_level = event.drift_state.get("drift_metric", 0.0)
    
    return TimelinePoint(
        sequence_id=event.sequence_id,
        timestamp=event.timestamp,
        delta12_dominant=dominant_arch[0],
        delta12_probability=dominant_arch[1],
        delta144_state=event.delta144_state or "UNKNOWN",
        drift_level=drift_level
    )


def _count_archetype_shifts(points: List[TimelinePoint]) -> int:
    """Count number of dominant archetype changes."""
    if len(points) < 2:
        return 0
    
    shifts = 0
    for i in range(len(points) - 1):
        if points[i].delta12_dominant != points[i+1].delta12_dominant:
            shifts += 1
    
    return shifts


def _compute_average_shift_magnitude(events: List[StoryEvent]) -> float:
    """Compute average Δ12 shift magnitude across timeline."""
    if len(events) < 2:
        return 0.0
    
    magnitudes = []
    
    for i in range(len(events) - 1):
        if events[i].delta12 and events[i+1].delta12:
            mag = compute_shift_magnitude(events[i].delta12, events[i+1].delta12)
            magnitudes.append(mag)
    
    return sum(magnitudes) / len(magnitudes) if magnitudes else 0.0


def _compute_persistence_score(points: List[TimelinePoint]) -> float:
    """
    Compute archetype persistence score.
    
    Higher score = archetypes stay stable longer.
    """
    if len(points) < 2:
        return 1.0
    
    # Count consecutive same-archetype sequences
    max_consecutive = 1
    current_consecutive = 1
    
    for i in range(len(points) - 1):
        if points[i].delta12_dominant == points[i+1].delta12_dominant:
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            current_consecutive = 1
    
    # Normalize by timeline length
    persistence = max_consecutive / len(points)
    
    return persistence


def _delta12_to_vector(delta12_a: Dict[str, float], delta12_b: Dict[str, float]) -> List[float]:
    """Convert Δ12 transition to vector."""
    all_keys = sorted(set(delta12_a.keys()) | set(delta12_b.keys()))
    
    vector = [delta12_b.get(k, 0.0) - delta12_a.get(k, 0.0) for k in all_keys]
    
    return vector


def _vector_angle(v1: List[float], v2: List[float]) -> float:
    """Compute angle between two vectors."""
    if len(v1) != len(v2):
        return 0.0
    
    # Dot product
    dot = sum(a * b for a, b in zip(v1, v2))
    
    # Magnitudes
    mag1 = math.sqrt(sum(a ** 2 for a in v1))
    mag2 = math.sqrt(sum(b ** 2 for b in v2))
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    # Cosine of angle
    cos_angle = dot / (mag1 * mag2)
    cos_angle = max(-1.0, min(1.0, cos_angle))  # Clamp to valid range
    
    # Angle in radians
    angle = math.acos(cos_angle)
    
    return angle
