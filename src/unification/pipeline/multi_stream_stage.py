"""
MultiStreamStage for KALDRA v3.3 Phase 3 Pipeline.

Integrates multi-stream narrative comparison into the unified pipeline.
Populates MultiStreamContext with cross-stream divergence analysis.
"""
from dataclasses import dataclass
from typing import Optional
import logging

from ..states.unified_state import UnifiedContext, MultiStreamContext
from src.story.multi_stream_buffer import MultiStreamBuffer
from src.story.stream_comparator import StreamComparator

logger = logging.getLogger(__name__)


@dataclass
class MultiStreamStageConfig:
    """
    Configuration for MultiStreamStage.
    
    Attributes:
        window_size: Number of recent events per stream for comparison
        max_events_per_stream: Maximum events to keep per stream (FIFO)
        global_max_events: Maximum total events across all streams
        enabled: Whether multi-stream analysis is enabled
        divergence_threshold: Threshold for convergent/divergent classification
    """
    window_size: int = 50
    max_events_per_stream: int = 500
    global_max_events: int = 5000
    enabled: bool = True
    divergence_threshold: float = 0.7  # Above this = not convergent


class MultiStreamStage:
    """
    Multi-stream narrative comparison pipeline stage (v3.3 Phase 3).
    
    Analyzes narrative divergence across multiple streams (e.g., NYT vs Twitter).
    Uses MultiStreamBuffer and StreamComparator to measure how different sources
    tell the same story.
    
    Populates MultiStreamContext with:
    - Active streams list
    - Pairwise comparison results
    - Maximum divergence score
    - Convergence/divergence classification
    """
    
    def __init__(self, config: Optional[MultiStreamStageConfig] = None):
        """
        Initialize multi-stream stage.
        
        Args:
            config: MultiStreamStage configuration (defaults to MultiStreamStageConfig())
        """
        self.config = config or MultiStreamStageConfig()
        
        # Initialize multi-stream components
        self._buffer = MultiStreamBuffer(
            max_events_per_stream=self.config.max_events_per_stream,
            global_max_events=self.config.global_max_events,
        )
        self._comparator = StreamComparator()
        
        logger.info(f"MultiStreamStage initialized: window_size={self.config.window_size}, enabled={self.config.enabled}")
    
    def run(self, context: UnifiedContext) -> UnifiedContext:
        """
        Execute multi-stream stage: compare narratives across streams.
        
        Flow:
        1. Check if enabled and if story_ctx exists
        2. Feed events to MultiStreamBuffer (with stream_id)
        3. Get windows for each stream
        4. Compare streams using StreamComparator
        5. Populate MultiStreamContext
        6. Graceful degradation on errors
        
        Args:
            context: Unified context from previous pipeline stages
            
        Returns:
            Updated context with populated multi_stream_ctx
        """
        # Skip if disabled
        if not self.config.enabled:
            logger.debug("MultiStreamStage: skipped (disabled)")
            return context
        
        # Skip if no story context or events
        if not context.story_ctx or not context.story_ctx.events:
            logger.debug("MultiStreamStage: skipped (no story events)")
            return context
        
        logger.info("MultiStreamStage: executing cross-stream analysis")
        
        try:
            # 1. Feed events to buffer
            for event in context.story_ctx.events:
                # Ensure stream_id is set (fallback to "default")
                if not hasattr(event, 'stream_id') or event.stream_id is None:
                    event.stream_id = "default"
                
                self._buffer.add_event(event)
            
            # 2. Get windows for all streams
            windows = self._buffer.get_all_windows(size=self.config.window_size)
            
            # If no windows, skip
            if len(windows) == 0:
                logger.debug("MultiStreamStage: no streams to compare")
                return context
            
            # 3. Compare streams (if more than one)
            results = []
            if len(windows) > 1:
                results = self._comparator.compare_windows(windows)
            
            # 4. Extract active streams
            active_streams = [w.stream_id for w in windows]
            
            # 5. Calculate max divergence
            max_div = 0.0
            if results:
                max_div = max((r.overall_divergence for r in results), default=0.0)
            
            # 6. Determine convergence
            convergent = max_div < self.config.divergence_threshold
            
            # 7. Build MultiStreamContext
            ms_ctx = MultiStreamContext(
                active_streams=active_streams,
                pairwise_results=results,
                max_divergence=max_div,
                convergent=convergent,
                metadata={}
            )
            
            # 8. Attach to UnifiedContext
            context.multi_stream_ctx = ms_ctx
            
            logger.info(f"MultiStreamStage: analyzed {len(active_streams)} streams, max_div={max_div:.3f}, convergent={convergent}")
            
        except Exception as e:
            logger.warning(f"MultiStreamStage failed: {e}", exc_info=True)
            # Graceful degradation - don't mark global degraded (optional layer)
            # Leave multi_stream_ctx as None
        
        return context
