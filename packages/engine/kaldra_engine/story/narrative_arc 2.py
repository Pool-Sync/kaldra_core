"""
Narrative Arc Engine - Campbell-based arc tracking for KALDRA v2.6.

Combines Campbell's Hero's Journey with Δ144, TW369, and meta-engines
for hybrid narrative arc detection and prediction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple

from .story_buffer import StoryBuffer, StoryEvent


# Campbell's 12 canonical stages
CAMPBELL_STAGES = [
    "ordinary_world",
    "call_to_adventure",
    "refusal_of_the_call",
    "meeting_with_the_mentor",
    "crossing_the_threshold",
    "tests_allies_enemies",
    "approach_to_cave",
    "ordeal",
    "reward",
    "road_back",
    "resurrection",
    "return_with_elixir"
]


@dataclass
class NarrativeArc:
    """
    Complete narrative arc analysis.
    
    Combines Campbell stages with drift dynamics and meta-scores.
    """
    current_stage: str
    stage_confidence: float
    arc_progress: float  # 0.0-1.0
    transition_likelihood: float  # Probability of moving to next stage
    tension_trend: float  # +/- change in tension
    predicted_next_stage: str
    predicted_inflection_distance: int  # Events until next inflection
    
    # Supporting data
    stage_index: int
    drift_level: float
    meta_alignment: Dict[str, float]  # Nietzsche/Aurelius alignment


def analyze_arc(buffer: StoryBuffer) -> Optional[NarrativeArc]:
    """
    Analyze narrative arc from buffer.
    
    Args:
        buffer: StoryBuffer with events
        
    Returns:
        NarrativeArc or None if insufficient data
    """
    timeline = buffer.get_timeline()
    
    if len(timeline) == 0:
        return None
    
    # Get current event
    current_event = timeline[-1]
    
    # Extract Campbell stage
    current_stage = "ordinary_world"  # Default
    stage_confidence = 0.5
    
    if current_event.meta_scores and "campbell" in current_event.meta_scores:
        campbell = current_event.meta_scores["campbell"]
        current_stage = campbell.get("stage", "ordinary_world")
        stage_confidence = campbell.get("confidence", 0.5)
    
    # Get stage index
    try:
        stage_index = CAMPBELL_STAGES.index(current_stage)
    except ValueError:
        stage_index = 0
    
    # Compute arc progress
    arc_progress = stage_index / (len(CAMPBELL_STAGES) - 1)
    
    # Predict next stage
    predicted_next_stage = _predict_next_stage(current_stage, stage_index, timeline)
    
    # Compute transition likelihood
    transition_likelihood = _compute_transition_likelihood(timeline, current_stage)
    
    # Compute tension trend
    tension_trend = compute_tension(timeline)
    
    # Predict inflection distance
    inflection_distance = _predict_inflection_distance(timeline, current_stage)
    
    # Get drift level
    drift_level = 0.0
    if current_event.drift_state:
        drift_level = current_event.drift_state.get("drift_metric", 0.0)
    
    # Get meta alignment
    meta_alignment = _compute_meta_alignment(current_event)
    
    return NarrativeArc(
        current_stage=current_stage,
        stage_confidence=stage_confidence,
        arc_progress=arc_progress,
        transition_likelihood=transition_likelihood,
        tension_trend=tension_trend,
        predicted_next_stage=predicted_next_stage,
        predicted_inflection_distance=inflection_distance,
        stage_index=stage_index,
        drift_level=drift_level,
        meta_alignment=meta_alignment
    )


def predict_next_stage(current_arc: NarrativeArc, buffer: StoryBuffer) -> str:
    """
    Predict next Campbell stage.
    
    Args:
        current_arc: Current NarrativeArc
        buffer: StoryBuffer with events
        
    Returns:
        Predicted next stage name
    """
    # Simple progression: next stage in sequence
    next_index = current_arc.stage_index + 1
    
    if next_index >= len(CAMPBELL_STAGES):
        return current_arc.current_stage  # Stay at final stage
    
    return CAMPBELL_STAGES[next_index]


def compute_tension(events: List[StoryEvent]) -> float:
    """
    Compute narrative tension trend.
    
    Tension is a combination of:
    - Drift level
    - Nietzsche will_to_power / active_nihilism
    - Aurelius emotional_regulation (inverse)
    
    Args:
        events: List of StoryEvents
        
    Returns:
        Tension trend (+/- change)
    """
    if len(events) < 2:
        return 0.0
    
    # Compare last two events
    prev = events[-2]
    curr = events[-1]
    
    prev_tension = _compute_event_tension(prev)
    curr_tension = _compute_event_tension(curr)
    
    return curr_tension - prev_tension


# Helper functions

def _predict_next_stage(current_stage: str, stage_index: int, timeline: List[StoryEvent]) -> str:
    """Predict next stage based on current trajectory."""
    # Simple linear progression
    next_index = stage_index + 1
    
    if next_index >= len(CAMPBELL_STAGES):
        return current_stage  # Stay at final stage
    
    return CAMPBELL_STAGES[next_index]


def _compute_transition_likelihood(timeline: List[StoryEvent], current_stage: str) -> float:
    """
    Compute likelihood of transitioning to next stage.
    
    Based on:
    - Time in current stage
    - Drift acceleration
    - Meta-score changes
    """
    if len(timeline) < 2:
        return 0.5
    
    # Count events in current stage
    events_in_stage = 0
    for event in reversed(timeline):
        if event.meta_scores and "campbell" in event.meta_scores:
            stage = event.meta_scores["campbell"].get("stage")
            if stage == current_stage:
                events_in_stage += 1
            else:
                break
    
    # More events in stage → higher transition likelihood
    # Typical stage duration: 2-4 events
    if events_in_stage >= 4:
        likelihood = 0.8
    elif events_in_stage >= 3:
        likelihood = 0.6
    elif events_in_stage >= 2:
        likelihood = 0.4
    else:
        likelihood = 0.2
    
    return likelihood


def _predict_inflection_distance(timeline: List[StoryEvent], current_stage: str) -> int:
    """
    Predict number of events until next inflection.
    
    Based on typical stage durations and current trajectory.
    """
    # Typical stage duration: 2-4 events
    # Crisis stages (ordeal, approach) tend to be shorter
    
    crisis_stages = ["approach_to_cave", "ordeal", "resurrection"]
    
    if current_stage in crisis_stages:
        return 1  # Crisis stages transition quickly
    else:
        return 3  # Normal stages take longer


def _compute_event_tension(event: StoryEvent) -> float:
    """Compute tension level for a single event."""
    tension = 0.0
    
    # Drift contributes to tension
    if event.drift_state:
        drift = event.drift_state.get("drift_metric", 0.0)
        tension += drift * 0.4
    
    # Nietzsche scores contribute
    if event.meta_scores and "nietzsche" in event.meta_scores:
        nietzsche = event.meta_scores["nietzsche"]
        will_to_power = nietzsche.get("will_to_power", 0.0)
        active_nihilism = nietzsche.get("active_nihilism", 0.0)
        tension += (will_to_power + active_nihilism) * 0.3
    
    # Aurelius emotional_regulation reduces tension
    if event.meta_scores and "aurelius" in event.meta_scores:
        aurelius = event.meta_scores["aurelius"]
        regulation = aurelius.get("emotional_regulation", 0.5)
        tension -= (regulation - 0.5) * 0.3
    
    return max(0.0, min(1.0, tension))


def _compute_meta_alignment(event: StoryEvent) -> Dict[str, float]:
    """Compute meta-engine alignment scores."""
    alignment = {}
    
    if event.meta_scores:
        # Nietzsche: average of all scores
        if "nietzsche" in event.meta_scores:
            nietzsche = event.meta_scores["nietzsche"]
            if isinstance(nietzsche, dict):
                scores = [v for v in nietzsche.values() if isinstance(v, (int, float))]
                alignment["nietzsche"] = sum(scores) / len(scores) if scores else 0.0
        
        # Aurelius: use severity if available
        if "aurelius" in event.meta_scores:
            aurelius = event.meta_scores["aurelius"]
            if isinstance(aurelius, dict):
                # Look for severity or compute average
                if "severity" in aurelius:
                    alignment["aurelius"] = aurelius["severity"]
                else:
                    scores = [v for v in aurelius.values() if isinstance(v, (int, float))]
                    alignment["aurelius"] = sum(scores) / len(scores) if scores else 0.0
    
    return alignment
