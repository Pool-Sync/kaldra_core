"""
Story module for KALDRA v3.2 Temporal Mind.

Provides temporal narrative analysis capabilities:
- StoryBuffer: Event storage with sliding window
- TimelineBuilder: Archetype transition tracking
- ArcDetector: Hero's Journey stage detection
- CoherenceScorer: Narrative consistency metrics
"""

from .story_buffer import StoryEvent, StoryBufferConfig, StoryBuffer
from .timeline_builder import ArchetypeTransition, StoryTimeline, TimelineBuilder
from .arc_detector import StoryArc, ArcDetector, JOURNEY_STAGES
from .coherence_scorer import CoherenceScore, CoherenceScorer

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
