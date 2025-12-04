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
import uuid
from time import time

from ..states.unified_state import UnifiedContext, StoryContext
from src.common.unified_signal import StoryEvent  # Use unified_signal StoryEvent (has stream_id)
from src.story.story_buffer import StoryBuffer, StoryBufferConfig
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
        - stream_id from input_ctx.metadata (v3.3 Phase 3)
        
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
        
        # v3.3 Phase 3: Extract stream_id from InputMetadata
        stream_id = None
        if context.input_ctx and hasattr(context.input_ctx, 'metadata'):
            metadata_obj = context.input_ctx.metadata
            if hasattr(metadata_obj, 'stream_id'):
                stream_id = metadata_obj.stream_id
        
        # Extract archetype data (for delta12 and delta144 fields)
        delta12 = None
        delta144_state = None
        kindra = None
        meta_scores = None
        drift_state = None
        tw_state = None
        
        if context.archetype_ctx:
            if context.archetype_ctx.delta12:
                # Convert Delta12Vector to dict
                delta12 = context.archetype_ctx.delta12.to_dict() if hasattr(context.archetype_ctx.delta12, 'to_dict') else {}
            
            if context.archetype_ctx.delta144_state:
                # Extract state_id from StateInferenceResult
                state_id = getattr(context.archetype_ctx.delta144_state, 'state_id', None)
                delta144_state = state_id
        
        # Extract meta scores
        if context.meta_ctx:
            meta_scores = {}
            if context.meta_ctx.nietzsche:
                meta_scores['nietzsche'] = context.meta_ctx.nietzsche.score
            if context.meta_ctx.aurelius:
                meta_scores['aurelius'] = context.meta_ctx.aurelius.score
            if context.meta_ctx.campbell:
                 meta_scores['campbell'] = context.meta_ctx.campbell.score
        
        # Extract TW369 state
        if context.drift_ctx:
            if context.drift_ctx.drift_state:
                drift_state = context.drift_ctx.drift_state.to_dict() if hasattr(context.drift_ctx.drift_state, 'to_dict') else {}
            if context.drift_ctx.tw_state:
                tw_state = context.drift_ctx.tw_state.to_dict() if hasattr(context.drift_ctx.tw_state, 'to_dict') else {}
        
        # Extract polarities
        polarity_scores = {}
        if context.archetype_ctx and context.archetype_ctx.polarity_scores:
            polarity_scores = context.archetype_ctx.polarity_scores
        
        # Build metadata
        metadata = {}
        if context.global_ctx:
            metadata = {
                "request_id": context.global_ctx.request_id,
                "mode": context.global_ctx.mode
            }
        
        # Generate event_id and sequence_id
        event_id = str(uuid.uuid4())
        sequence_id = len(self._buffer._events) if hasattr(self._buffer, '_events') else 0
        
        # Create StoryEvent using unified_signal.StoryEvent signature
        return StoryEvent(
            event_id=event_id,
            timestamp=timestamp,
            sequence_id=sequence_id,
            text=text,
            delta12=delta12,
            delta144_state=delta144_state,
            kindra=kindra,
            meta_scores=meta_scores,
            drift_state=drift_state,
            tw_state=tw_state,
            polarity_scores=polarity_scores,
            stream_id=stream_id,  # v3.3 Phase 3: propagate stream_id
            metadata=metadata
        )
