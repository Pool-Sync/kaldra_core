"""
Story module for KALDRA v3.2 Temporal Mind.

Provides temporal narrative analysis capabilities:
- StoryBuffer: Event storage with sliding window
- TimelineBuilder: Archetype transition tracking
- ArcDetector: Hero's Journey stage detection
- CoherenceScorer: Narrative consistency metrics
"""

from .arc_detector import JOURNEY_STAGES, ArcDetector, StoryArc
from .coherence_scorer import CoherenceScore, CoherenceScorer
from .story_buffer import StoryBuffer, StoryBufferConfig, StoryEvent
from .timeline_builder import ArchetypeTransition, StoryTimeline, TimelineBuilder

__all__ = [
    # Story Buffer
    "StoryEvent",
    "StoryBufferConfig",
    "StoryBuffer",
    # Timeline Builder
    "ArchetypeTransition",
    "StoryTimeline",
    "TimelineBuilder",
    # Arc Detector
    "StoryArc",
    "ArcDetector",
    "JOURNEY_STAGES",
    # Coherence Scorer
    "CoherenceScore",
    "CoherenceScorer",
]
