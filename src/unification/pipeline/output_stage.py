"""
Output Stage for KALDRA v3.0 Pipeline.

Handles:
- Final signal assembly
- Signal adapter application
- API response formatting
"""
from typing import Optional, Dict, Any
import logging

from ..states.unified_state import UnifiedContext
from ..registry import ModuleRegistry

logger = logging.getLogger(__name__)


class OutputStage:
    """
    Output assembly and formatting stage.
    
    Responsibilities:
    1. Assemble final signal from all contexts
    2. Apply signal adapter
    3. Format for API response
    """
    
    def __init__(self, registry: ModuleRegistry):
        """
        Initialize output stage.
        
        Args:
            registry: Module registry with loaded engines
        """
        self.registry = registry
    
    def execute(self, context: UnifiedContext) -> UnifiedContext:
        """
        Execute output stage.
        
        Args:
            context: Unified context
            
        Returns:
            Final unified context ready for output
        """
        logger.info("Output stage: assembling final signal")
        
        try:
            # Calculate confidence score
            confidence = self._calculate_confidence(context)
            
            # Add summary metadata
            if not hasattr(context.global_ctx, 'summary'):
                context.global_ctx.__dict__['summary'] = {
                    'confidence': confidence,
                    'routing': context.global_ctx.mode,
                    'degraded': context.global_ctx.degraded
                }
            
            logger.info(f"Output stage complete: confidence={confidence:.3f}, degraded={context.global_ctx.degraded}")
            
        except Exception as e:
            logger.error(f"Output stage failed: {e}")
            context.global_ctx.degraded = True
        
        return context
    
    def _calculate_confidence(self, context: UnifiedContext) -> float:
        """
        Calculate overall confidence score.
        
        Args:
            context: Unified context
            
        Returns:
            Confidence score [0.0, 1.0]
        """
        # Start with base confidence
        confidence = 1.0
        
        # Reduce confidence if degraded
        if context.global_ctx.degraded:
            confidence *= 0.5
        
        # Reduce confidence based on Tau risk
        if context.input_ctx and context.input_ctx.tau_input:
            tau_score = context.input_ctx.tau_input.tau_score
            confidence *= tau_score
        
        # Reduce confidence based on Safeguard risk
        if context.risk_ctx and context.risk_ctx.risk_score:
            risk_penalty = 1.0 - (context.risk_ctx.risk_score * 0.3)
            confidence *= risk_penalty
        
        return max(0.0, min(1.0, confidence))
