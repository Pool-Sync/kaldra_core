"""
StoryStage for KALDRA v3.2 Pipeline.

Integrates Story Engine components to build/update StoryContext from pipeline events.

Responsibilities:
1. Build StoryEvent from UnifiedContext
2. Update StoryBuffer with sliding window
3. Build Timeline, Arc, Coherence via Story Engine
4. Populate StoryContext in UnifiedContext
5. Preserve metadata (e.g., delta144_timeline)
"""
from dataclasses import dataclass
from typing import Optional
import logging
from time import time

from ..states.unified_state import UnifiedContext, StoryContext
from src.story.story_buffer import StoryBuffer, StoryEvent, StoryBufferConfig
from src.story.timeline_builder import TimelineBuilder
from src.story.arc_detector import ArcDetector
from src.story.coherence_scorer import CoherenceScorer

logger = logging.getLogger(__name__)


@dataclass
class StoryStageConfig:
    """
    Configuration for StoryStage.
    
    Attributes:
        max_events: Maximum events in buffer (older events evicted)
        window_size: Number of recent events to analyze
        enable_coherence: Whether to compute coherence score (adds latency)
    """
    max_events: int = 1000
    window_size: int = 200
    enable_coherence: bool = True


class StoryStage:
    """
    Story and narrative analysis pipeline stage (v3.2).
    
    Integrates Story Engine to build temporal narrative context:
    - StoryBuffer: Maintains sliding window of events
    - TimelineBuilder: Constructs temporal event sequence
    - ArcDetector: Identifies narrative arc and journey stages
    - CoherenceScorer: Measures narrative consistency
    
    Populates StoryContext for consumption by CampbellEngine v3.2 temporal.
    """
    
    def __init__(self, config: Optional[StoryStageConfig] = None):
        """
        Initialize story stage.
        
        Args:
            config: StoryStage configuration (defaults to StoryStageConfig())
        """
        self.config = config or StoryStageConfig()
        
        # Initialize Story Engine components
        buffer_config = StoryBufferConfig(max_events=self.config.max_events)
        self._buffer = StoryBuffer(buffer_config)
        self._timeline_builder = TimelineBuilder()
        self._arc_detector = ArcDetector()
        if self.config.enable_coherence:
            self._coherence_scorer = CoherenceScorer()
        else:
            self._coherence_scorer = None
        
        logger.info(f"StoryStage initialized: max_events={self.config.max_events}, window_size={self.config.window_size}")
    
    def run(self, context: UnifiedContext) -> UnifiedContext:
        """
        Execute story stage: build/update StoryContext from current signal + history.
        
        Flow:
        1. Build StoryEvent from context
        2. Add to StoryBuffer
        3. Get sliding window of events
        4. Build Timeline, Arc, Coherence via Story Engine
        5. Populate StoryContext
        6. Preserve existing metadata (e.g., delta144_timeline)
        
        Args:
            context: Unified context from previous pipeline stages
            
        Returns:
            Updated context with populated story_ctx
        """
        # Skip if signal mode (fast path)
        if context.global_ctx and context.global_ctx.mode == "signal":
            logger.debug("StoryStage: skipped (signal mode)")
            return context
        
        logger.info("StoryStage: executing narrative analysis")
        
        try:
            # 1. Build event from current context
            event = self._build_event_from_context(context)
            
            # 2. Add to buffer (maintains max_events limit)
            self._buffer.add_event(event)
            
            # 3. Get sliding window of recent events
            events_window = self._buffer.get_window(self.config.window_size)
            
            # 4. Build Story Engine components
            timeline = self._timeline_builder.build(events_window)
            arc = self._arc_detector.detect(events_window, timeline)
            
            # Compute coherence if enabled
            coherence_value = 0.0
            if self.config.enable_coherence and self._coherence_scorer:
                coherence = self._coherence_scorer.score(events_window, timeline, arc)
                # coherence is CoherenceScore object with .overall attribute
                if hasattr(coherence, 'overall'):
                    coherence_value = coherence.overall
                elif isinstance(coherence, (int, float)):
                    coherence_value = float(coherence)
                else:
                    coherence_value = 0.0
            
            # 5. Build StoryContext
            story_ctx = StoryContext(
                events=events_window,
                arc=arc,
                timeline=timeline,
                coherence=coherence_value,
                metadata={}
            )
            
            # 6. Preserve existing metadata (e.g., delta144_timeline from other stages)
            if context.story_ctx and context.story_ctx.metadata:
                story_ctx.metadata.update(context.story_ctx.metadata)
            
            # Update context
            context.story_ctx = story_ctx
            
            logger.info(f"StoryStage: processed {len(events_window)} events, arc={arc.dominant_stage if arc else 'None'}")
            
        except Exception as e:
            logger.error(f"StoryStage failed: {e}", exc_info=True)
            if context.global_ctx:
                context.global_ctx.degraded = True
            
            # Create minimal StoryContext on error (graceful degradation)
            context.story_ctx = StoryContext()
        
        return context
    
    def _build_event_from_context(self, context: UnifiedContext) -> StoryEvent:
        """
        Build StoryEvent from UnifiedContext.
        
        Extracts:
        - Timestamp from global_ctx
        - Text from input_ctx
        - Archetype data from archetype_ctx
        - Polarities from archetype_ctx
        - Metadata from global_ctx
        
        Args:
            context: Unified context
            
        Returns:
            StoryEvent ready for StoryBuffer
        """
        # Extract timestamp
        timestamp = context.global_ctx.timestamp if context.global_ctx else time()
        
        # Extract text
        text = ""
        if context.input_ctx:
            text = context.input_ctx.text or ""
        
        # Extract archetype data
        archetype_id = None
        archetype_scores = {}
        if context.archetype_ctx:
            if context.archetype_ctx.delta144_state:
                # delta144_state is StateInferenceResult with state_id and weights
                archetype_id = getattr(context.archetype_ctx.delta144_state, 'state_id', None)
                weights = getattr(context.archetype_ctx.delta144_state, 'weights', {})
                archetype_scores = weights if weights else {}
            elif context.archetype_ctx.delta12:
                # Fallback to delta12 primary archetype
                archetype_id = getattr(context.archetype_ctx.delta12, 'primary_archetype', None)
        
        # Extract polarities
        polarities = {}
        if context.archetype_ctx and context.archetype_ctx.polarity_scores:
            polarities = context.archetype_ctx.polarity_scores
        
        # Build metadata
        metadata = {}
        if context.global_ctx:
            metadata = {
                "request_id": context.global_ctx.request_id,
                "mode": context.global_ctx.mode
            }
        
        return StoryEvent(
            timestamp=timestamp,
            text=text,
            archetype_id=archetype_id,
            archetype_scores=archetype_scores,
            polarities=polarities,
            metadata=metadata
        )
