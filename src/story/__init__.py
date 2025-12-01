"""
Story module initialization.
"""

from .story_buffer import StoryBuffer, StoryEvent
from .story_aggregator import (
    StoryAggregation,
    MotionVector,
    InflectionPoint,
    DriftTrajectory,
    ArcProgression,
    aggregate_story,
    compute_narrative_motion,
    detect_inflection_points,
    detect_arc_progression,
)
from .narrative_arc import (
    NarrativeArc,
    CAMPBELL_STAGES,
    analyze_arc,
    predict_next_stage,
    compute_tension,
)
from .archetypal_timeline import (
    ArchetypalTimeline,
    TimelinePoint,
    ArchetypalLoop,
    build_timeline,
    compute_shift_magnitude,
    compute_trajectory_curvature,
    detect_archetypal_loops,
)

__all__ = [
    "StoryBuffer",
    "StoryEvent",
    "StoryAggregation",
    "MotionVector",
    "InflectionPoint",
    "DriftTrajectory",
    "ArcProgression",
    "aggregate_story",
    "compute_narrative_motion",
    "detect_inflection_points",
    "detect_arc_progression",
    "NarrativeArc",
    "CAMPBELL_STAGES",
    "analyze_arc",
    "predict_next_stage",
    "compute_tension",
    "ArchetypalTimeline",
    "TimelinePoint",
    "ArchetypalLoop",
    "build_timeline",
    "compute_shift_magnitude",
    "compute_trajectory_curvature",
    "detect_archetypal_loops",
]
