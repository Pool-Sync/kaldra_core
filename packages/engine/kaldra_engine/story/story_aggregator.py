"""
Story Aggregator - Temporal pattern detection for KALDRA v2.6.

Aggregates events from StoryBuffer and detects:
- Motion vectors between states
- Inflection points
- Arc progression
- Drift trajectories
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
import math

from .story_buffer import StoryBuffer, StoryEvent


@dataclass
class MotionVector:
    """
    Motion vector between two narrative states.
    
    Captures change in Δ12, Δ144, drift, and meta-scores.
    """
    from_event_id: str
    to_event_id: str
    time_delta: float  # seconds
    
    # Δ12 motion
    delta12_shift_magnitude: float  # Euclidean distance
    delta12_dominant_change: Optional[Tuple[str, str]] = None  # (from_archetype, to_archetype)
    
    # Δ144 motion
    delta144_transition: Optional[Tuple[str, str]] = None  # (from_state, to_state)
    
    # Drift motion
    drift_velocity: float = 0.0  # Change in drift per second
    drift_acceleration: float = 0.0  # Change in velocity
    
    # Meta-score deltas
    meta_deltas: Dict[str, float] = field(default_factory=dict)
    
    # Polarity deltas (v2.7)
    polarity_deltas: Dict[str, float] = field(default_factory=dict)


@dataclass
class InflectionPoint:
    """
    Detected inflection point in narrative.
    
    Marks significant changes in trajectory.
    """
    event_id: str
    sequence_id: int
    timestamp: float
    inflection_type: str  # "drift_peak", "archetype_shift", "stage_transition", "meta_inversion"
    magnitude: float  # Strength of inflection
    description: str


@dataclass
class DriftTrajectory:
    """
    Drift evolution over time.
    """
    drift_values: List[float]
    drift_slope: float  # Linear regression slope
    drift_acceleration: float  # Second derivative
    drift_volatility: float  # Standard deviation


@dataclass
class ArcProgression:
    """
    Campbell arc progression tracking.
    """
    current_stage: str
    stage_confidence: float
    arc_progress: float  # 0.0-1.0
    stage_history: List[Tuple[str, int]]  # (stage, sequence_id)


@dataclass
class StoryAggregation:
    """
    Complete aggregation of story timeline.
    """
    timeline: List[StoryEvent]
    motion_vectors: List[MotionVector]
    inflection_points: List[InflectionPoint]
    arc_progression: Optional[ArcProgression]
    drift_trajectory: Optional[DriftTrajectory]
    
    # Summary stats
    total_events: int
    time_span: float  # seconds
    narrative_oscillation_index: float = 0.0


def aggregate_story(buffer: StoryBuffer) -> StoryAggregation:
    """
    Aggregate complete story from buffer.
    
    Args:
        buffer: StoryBuffer with events
        
    Returns:
        StoryAggregation with all computed metrics
    """
    timeline = buffer.get_timeline()
    
    if len(timeline) == 0:
        return StoryAggregation(
            timeline=[],
            motion_vectors=[],
            inflection_points=[],
            arc_progression=None,
            drift_trajectory=None,
            total_events=0,
            time_span=0.0
        )
    
    # Compute motion vectors
    motion_vectors = _compute_motion_vectors(timeline)
    
    # Detect inflection points
    inflection_points = detect_inflection_points(timeline)
    
    # Track arc progression
    arc_progression = detect_arc_progression(buffer)
    
    # Compute drift trajectory
    drift_trajectory = _compute_drift_trajectory(timeline)
    
    # Compute narrative oscillation
    oscillation = _compute_narrative_oscillation(motion_vectors)
    
    # Time span
    time_span = timeline[-1].timestamp - timeline[0].timestamp if len(timeline) > 1 else 0.0
    
    return StoryAggregation(
        timeline=timeline,
        motion_vectors=motion_vectors,
        inflection_points=inflection_points,
        arc_progression=arc_progression,
        drift_trajectory=drift_trajectory,
        total_events=len(timeline),
        time_span=time_span,
        narrative_oscillation_index=oscillation
    )


def compute_narrative_motion(prev: StoryEvent, curr: StoryEvent) -> MotionVector:
    """
    Compute motion vector between two events.
    
    Args:
        prev: Previous event
        curr: Current event
        
    Returns:
        MotionVector capturing change
    """
    time_delta = curr.timestamp - prev.timestamp
    
    # Δ12 shift magnitude
    delta12_shift = 0.0
    delta12_dominant_change = None
    
    if prev.delta12 and curr.delta12:
        delta12_shift = _compute_delta12_distance(prev.delta12, curr.delta12)
        
        # Find dominant archetype change
        prev_dominant = max(prev.delta12.items(), key=lambda x: x[1])[0] if prev.delta12 else None
        curr_dominant = max(curr.delta12.items(), key=lambda x: x[1])[0] if curr.delta12 else None
        
        if prev_dominant and curr_dominant and prev_dominant != curr_dominant:
            delta12_dominant_change = (prev_dominant, curr_dominant)
    
    # Δ144 transition
    delta144_transition = None
    if prev.delta144_state and curr.delta144_state and prev.delta144_state != curr.delta144_state:
        delta144_transition = (prev.delta144_state, curr.delta144_state)
    
    # Drift velocity
    drift_velocity = 0.0
    if prev.drift_state and curr.drift_state:
        prev_drift = prev.drift_state.get("drift_metric", 0.0)
        curr_drift = curr.drift_state.get("drift_metric", 0.0)
        drift_velocity = (curr_drift - prev_drift) / time_delta if time_delta > 0 else 0.0
    
    # Meta-score deltas
    meta_deltas = {}
    if prev.meta_scores and curr.meta_scores:
        for engine in ["nietzsche", "aurelius", "campbell"]:
            if engine in prev.meta_scores and engine in curr.meta_scores:
                # Compute average delta across all scores
                prev_scores = prev.meta_scores[engine]
                curr_scores = curr.meta_scores[engine]
                
                if isinstance(prev_scores, dict) and isinstance(curr_scores, dict):
                    deltas = [curr_scores.get(k, 0) - prev_scores.get(k, 0) 
                             for k in set(prev_scores.keys()) & set(curr_scores.keys())]
                    if deltas:
                        meta_deltas[engine] = sum(deltas) / len(deltas)
    
    # Polarity deltas (v2.7)
    polarity_deltas = {}
    if prev.polarity_scores and curr.polarity_scores:
        all_pols = set(prev.polarity_scores.keys()) | set(curr.polarity_scores.keys())
        for pol_id in all_pols:
            val_prev = prev.polarity_scores.get(pol_id, 0.0)
            val_curr = curr.polarity_scores.get(pol_id, 0.0)
            diff = val_curr - val_prev
            if abs(diff) > 0.1:  # Only track significant changes
                polarity_deltas[pol_id] = diff
    
    return MotionVector(
        from_event_id=prev.event_id,
        to_event_id=curr.event_id,
        time_delta=time_delta,
        delta12_shift_magnitude=delta12_shift,
        delta12_dominant_change=delta12_dominant_change,
        delta144_transition=delta144_transition,
        drift_velocity=drift_velocity,
        meta_deltas=meta_deltas,
        polarity_deltas=polarity_deltas
    )


def detect_inflection_points(history: List[StoryEvent]) -> List[InflectionPoint]:
    """
    Detect inflection points in narrative history.
    
    Args:
        history: List of StoryEvents
        
    Returns:
        List of detected InflectionPoints
    """
    if len(history) < 2:
        return []
    
    inflections = []
    
    # Detect drift peaks
    for i in range(1, len(history) - 1):
        prev = history[i - 1]
        curr = history[i]
        next_event = history[i + 1]
        
        if not (prev.drift_state and curr.drift_state and next_event.drift_state):
            continue
        
        prev_drift = prev.drift_state.get("drift_metric", 0.0)
        curr_drift = curr.drift_state.get("drift_metric", 0.0)
        next_drift = next_event.drift_state.get("drift_metric", 0.0)
        
        # Peak detection (local maximum)
        if curr_drift > prev_drift and curr_drift > next_drift and curr_drift > 0.7:
            inflections.append(InflectionPoint(
                event_id=curr.event_id,
                sequence_id=curr.sequence_id,
                timestamp=curr.timestamp,
                inflection_type="drift_peak",
                magnitude=curr_drift,
                description=f"Drift peak at {curr_drift:.2f}"
            ))
    
    # Detect archetype regime changes
    for i in range(1, len(history)):
        prev = history[i - 1]
        curr = history[i]
        
        if prev.delta12 and curr.delta12:
            prev_dominant = max(prev.delta12.items(), key=lambda x: x[1])[0]
            curr_dominant = max(curr.delta12.items(), key=lambda x: x[1])[0]
            
            if prev_dominant != curr_dominant:
                shift_magnitude = _compute_delta12_distance(prev.delta12, curr.delta12)
                
                if shift_magnitude > 0.3:  # Significant shift
                    inflections.append(InflectionPoint(
                        event_id=curr.event_id,
                        sequence_id=curr.sequence_id,
                        timestamp=curr.timestamp,
                        inflection_type="archetype_shift",
                        magnitude=shift_magnitude,
                        description=f"Archetype shift: {prev_dominant} → {curr_dominant}"
                    ))
    
    # Detect Campbell stage transitions
    for i in range(1, len(history)):
        prev = history[i - 1]
        curr = history[i]
        
        if (prev.meta_scores and curr.meta_scores and 
            "campbell" in prev.meta_scores and "campbell" in curr.meta_scores):
            
            prev_stage = prev.meta_scores["campbell"].get("stage")
            curr_stage = curr.meta_scores["campbell"].get("stage")
            
            if prev_stage and curr_stage and prev_stage != curr_stage:
                inflections.append(InflectionPoint(
                    event_id=curr.event_id,
                    sequence_id=curr.sequence_id,
                    timestamp=curr.timestamp,
                    inflection_type="stage_transition",
                    magnitude=1.0,
                    description=f"Campbell stage: {prev_stage} → {curr_stage}"
                ))

    # Detect Polarity Inversions (v2.7)
    # e.g. High Order -> High Chaos (rapid flip)
    for i in range(1, len(history)):
        prev = history[i - 1]
        curr = history[i]
        
        if prev.polarity_scores and curr.polarity_scores:
            for pol_id, val_curr in curr.polarity_scores.items():
                val_prev = prev.polarity_scores.get(pol_id, 0.0)
                
                # Check for inversion: crossing 0.5 threshold with large magnitude
                # e.g. 0.8 -> 0.2 (diff -0.6)
                diff = val_curr - val_prev
                
                if abs(diff) > 0.6:
                    direction = "Rise" if diff > 0 else "Fall"
                    inflections.append(InflectionPoint(
                        event_id=curr.event_id,
                        sequence_id=curr.sequence_id,
                        timestamp=curr.timestamp,
                        inflection_type="polarity_inversion",
                        magnitude=abs(diff),
                        description=f"Polarity Inversion: {pol_id} {direction} ({val_prev:.2f} → {val_curr:.2f})"
                    ))
    
    return inflections


def detect_arc_progression(buffer: StoryBuffer) -> Optional[ArcProgression]:
    """
    Detect Campbell arc progression from buffer.
    
    Args:
        buffer: StoryBuffer with events
        
    Returns:
        ArcProgression or None if insufficient data
    """
    timeline = buffer.get_timeline()
    
    if len(timeline) == 0:
        return None
    
    # Extract Campbell stages from timeline
    stage_history = []
    current_stage = None
    stage_confidence = 0.0
    
    for event in timeline:
        if event.meta_scores and "campbell" in event.meta_scores:
            campbell = event.meta_scores["campbell"]
            stage = campbell.get("stage")
            confidence = campbell.get("confidence", 0.0)
            
            if stage:
                stage_history.append((stage, event.sequence_id))
                current_stage = stage
                stage_confidence = confidence
    
    if not current_stage:
        return None
    
    # Compute arc progress (simplified: based on stage index)
    campbell_stages = [
        "ordinary_world", "call_to_adventure", "refusal_of_the_call",
        "meeting_with_the_mentor", "crossing_the_threshold", "tests_allies_enemies",
        "approach_to_cave", "ordeal", "reward", "road_back", "resurrection", "return_with_elixir"
    ]
    
    try:
        stage_index = campbell_stages.index(current_stage)
        arc_progress = stage_index / (len(campbell_stages) - 1)
    except ValueError:
        arc_progress = 0.0
    
    return ArcProgression(
        current_stage=current_stage,
        stage_confidence=stage_confidence,
        arc_progress=arc_progress,
        stage_history=stage_history
    )


# Helper functions

def _compute_motion_vectors(timeline: List[StoryEvent]) -> List[MotionVector]:
    """Compute motion vectors for all consecutive event pairs."""
    vectors = []
    
    for i in range(len(timeline) - 1):
        vector = compute_narrative_motion(timeline[i], timeline[i + 1])
        vectors.append(vector)
    
    return vectors


def _compute_delta12_distance(delta12_a: Dict[str, float], delta12_b: Dict[str, float]) -> float:
    """Compute Euclidean distance between two Δ12 vectors."""
    all_keys = set(delta12_a.keys()) | set(delta12_b.keys())
    
    squared_diff = sum((delta12_a.get(k, 0.0) - delta12_b.get(k, 0.0)) ** 2 for k in all_keys)
    
    return math.sqrt(squared_diff)


def _compute_drift_trajectory(timeline: List[StoryEvent]) -> Optional[DriftTrajectory]:
    """Compute drift trajectory from timeline."""
    drift_values = []
    
    for event in timeline:
        if event.drift_state:
            drift = event.drift_state.get("drift_metric", 0.0)
            drift_values.append(drift)
    
    if len(drift_values) < 2:
        return None
    
    # Compute slope (linear regression)
    n = len(drift_values)
    x = list(range(n))
    y = drift_values
    
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    
    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    
    slope = numerator / denominator if denominator != 0 else 0.0
    
    # Compute acceleration (second derivative approximation)
    if len(drift_values) >= 3:
        accelerations = []
        for i in range(1, len(drift_values) - 1):
            accel = drift_values[i + 1] - 2 * drift_values[i] + drift_values[i - 1]
            accelerations.append(accel)
        acceleration = sum(accelerations) / len(accelerations) if accelerations else 0.0
    else:
        acceleration = 0.0
    
    # Compute volatility (standard deviation)
    variance = sum((v - y_mean) ** 2 for v in drift_values) / n
    volatility = math.sqrt(variance)
    
    return DriftTrajectory(
        drift_values=drift_values,
        drift_slope=slope,
        drift_acceleration=acceleration,
        drift_volatility=volatility
    )


def _compute_narrative_oscillation(motion_vectors: List[MotionVector]) -> float:
    """
    Compute narrative oscillation index.
    
    Measures how much the narrative "bounces" between states.
    """
    if len(motion_vectors) < 2:
        return 0.0
    
    # Count direction changes in drift velocity
    direction_changes = 0
    
    for i in range(len(motion_vectors) - 1):
        curr_velocity = motion_vectors[i].drift_velocity
        next_velocity = motion_vectors[i + 1].drift_velocity
        
        # Sign change indicates oscillation
        if (curr_velocity > 0 and next_velocity < 0) or (curr_velocity < 0 and next_velocity > 0):
            direction_changes += 1
    
    # Normalize by number of transitions
    oscillation_index = direction_changes / (len(motion_vectors) - 1) if len(motion_vectors) > 1 else 0.0
    
    return oscillation_index
