"""
Core Stage for KALDRA v3.0 Pipeline.

Handles:
- Kindra 3×48 scoring
- Δ12 projection
- Δ144 state inference
- TW369 drift calculation
"""
from typing import Optional
import logging

from ..states.unified_state import (
    UnifiedContext,
    ArchetypeContext,
    DriftContext,
    KindraContext
)
from ..registry import ModuleRegistry
from src.kindras.kindra_engine import KindraEngine

logger = logging.getLogger(__name__)


class CoreStage:
    """
    Core archetypal and drift analysis stage.
    
    Responsibilities:
    1. Kindra 3×48 scoring
    2. Δ12 projection
    3. Δ144 state inference
    4. TW369 drift calculation
    """
    
    def __init__(self, registry: ModuleRegistry):
        """
        Initialize core stage.
        
        Args:
            registry: Module registry with loaded engines
        """
        self.registry = registry
        self.delta144 = registry.get("archetypes")
        # Initialize KindraEngine
        # In a full DI system, this might come from registry too, but for now we instantiate directly
        # or check registry.
        self.kindra_engine = registry.get("kindra") or KindraEngine()
    
    def execute(self, context: UnifiedContext) -> UnifiedContext:
        """
        Execute core stage.
        
        Args:
            context: Unified context
            
        Returns:
            Updated context with core analysis results
        """
        if not context.input_ctx or context.input_ctx.embedding is None:
            logger.warning("No embedding available, skipping core stage")
            return context
        
        logger.info("Core stage: executing archetypal analysis")
        
        try:
            embedding = context.input_ctx.embedding
            
            # Get Tau modifiers if available
            tau_modifiers = None
            if context.input_ctx.tau_input:
                tau_modifiers = context.input_ctx.tau_input.tau_modifiers
            
            # 1. Δ144 inference (includes Kindra, Δ12, and polarities)
            delta144_result = self.delta144.infer_from_vector(
                embedding,
                tau_modifiers=tau_modifiers
            )
            
            # 2. Compute Δ12 from plane scores (simplified for now)
            delta12 = self.delta144.compute_delta12(
                plane_scores={"3": 0.33, "6": 0.33, "9": 0.34},
                profile_scores={"EXPANSIVE": 0.33, "CONTRACTIVE": 0.33, "TRANSCENDENT": 0.34}
            )
            
            # Create archetype context
            archetype_ctx = ArchetypeContext(
                delta12=delta12,
                delta144_state=delta144_result,
                polarity_scores=delta144_result.polarity_scores
            )
            
            context.archetype_ctx = archetype_ctx
            
            # Create drift context (placeholder - TW369 integration in future)
            drift_ctx = DriftContext(
                regime=delta144_result.state.archetype_id,
                drift_metric=0.0
            )
            
            context.drift_ctx = drift_ctx
            
            # 3. Kindra 3x48 Scoring (with graceful degradation)
            context = self._run_kindra(context)
            
            logger.info(f"Core stage complete: archetype={delta144_result.archetype.label}, state={delta144_result.state.label}")
            
        except Exception as e:
            logger.error(f"Core stage failed: {e}")
            context.global_ctx.degraded = True
        
        return context
    
    def _run_kindra(self, context: UnifiedContext) -> UnifiedContext:
        """
        Execute KindraEngine and populate context.kindra_ctx.
        Implements graceful degradation - does not break pipeline on error.
        """
        # Skip if Kindra already populated (e.g., reuse scenario)
        if context.kindra_ctx is not None:
            return context
        
        try:
            text = context.input_ctx.text if context.input_ctx else ""
            embedding = context.input_ctx.embedding if context.input_ctx else None
            
            # Extract archetype data if available
            delta144_state = None
            archetype_scores = None
            if context.archetype_ctx:
                if hasattr(context.archetype_ctx, 'delta144_state') and context.archetype_ctx.delta144_state:
                    # Try to get state.id, fallback to string representation
                    d_state = context.archetype_ctx.delta144_state
                    delta144_state = getattr(d_state, 'id', str(d_state)) if d_state else None
                
                if hasattr(context.archetype_ctx, 'delta12') and context.archetype_ctx.delta12:
                    archetype_scores = getattr(context.archetype_ctx.delta12, 'scores', None)
            
            # Execute Kindra engine
            kindra_ctx = self.kindra_engine.score_all_layers(
                text=text,
                embedding=embedding,
                delta144_state=delta144_state,
                archetype_scores=archetype_scores
            )
            
            context.kindra_ctx = kindra_ctx
            logger.info(f"Kindra scoring complete: {kindra_ctx.get_total_vectors()} vectors")
            
        except Exception as e:
            # Graceful degradation - log but don't break pipeline
            self._warn_kindra_failure(e)
            context.kindra_ctx = None
            # Don't set global degraded flag for Kindra failures - it's supplementary
        
        return context
    
    def _warn_kindra_failure(self, exc: Exception):
        """Log Kindra engine failure with warning level."""
        logger.warning(f"KindraEngine failed (graceful degradation): {exc}")
