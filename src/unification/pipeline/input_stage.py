"""
Input Stage for KALDRA v3.0 Pipeline.

Handles:
- Bias detection
- Tau input phase (epistemic risk assessment)
- Embedding generation
"""
from typing import Optional
import logging
import numpy as np

from ..states.unified_state import UnifiedContext, InputContext
from ..registry import ModuleRegistry

logger = logging.getLogger(__name__)


class InputStage:
    """
    Input processing stage.
    
    Responsibilities:
    1. Bias detection
    2. Tau input phase (epistemic risk)
    3. Embedding generation
    """
    
    def __init__(self, registry: ModuleRegistry):
        """
        Initialize input stage.
        
        Args:
            registry: Module registry with loaded engines
        """
        self.registry = registry
        self.bias_detector = registry.get("bias")
        self.tau_layer = registry.get("tau")
        self.embedding_gen = registry.get("embeddings")
    
    def execute(self, context: UnifiedContext) -> UnifiedContext:
        """
        Execute input stage.
        
        Args:
            context: Unified context
            
        Returns:
            Updated context with input processing results
        """
        text = context.input_ctx.text if context.input_ctx else ""
        
        if not text:
            logger.warning("No input text provided")
            return context
        
        logger.info(f"Input stage: processing text (length={len(text)})")
        
        try:
            # 1. Bias detection
            bias_result = self.bias_detector.detect(text)
            bias_score = bias_result.get("score", 0.0) if isinstance(bias_result, dict) else 0.0
            
            # 2. Generate embedding
            embedding = self.embedding_gen.encode(text)[0]
            
            # 3. Tau input phase
            tau_input = self.tau_layer.compute_tau_input_phase(
                text=text,
                bias_score=bias_score,
                embedding=embedding
            )
            
            # Create input context
            input_ctx = InputContext(
                text=text,
                embedding=embedding,
                bias_score=bias_score,
                tau_input=tau_input
            )
            
            context.input_ctx = input_ctx
            
            logger.info(f"Input stage complete: bias={bias_score:.3f}, tau_risk={tau_input.tau_risk}")
            
        except Exception as e:
            logger.error(f"Input stage failed: {e}")
            context.global_ctx.degraded = True
            # Create minimal input context
            context.input_ctx = InputContext(text=text)
        
        return context
