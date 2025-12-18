"""
Safeguard Stage for KALDRA v3.0 Pipeline.

Handles:
- Tau output phase
- Safeguard risk evaluation
- Risk consolidation
"""
from typing import Optional
import logging

from ..states.unified_state import UnifiedContext, RiskContext
from ..registry import ModuleRegistry

logger = logging.getLogger(__name__)


class SafeguardStage:
    """
    Safety and risk mitigation stage.
    
    Responsibilities:
    1. Tau output phase (epistemic check)
    2. Safeguard risk evaluation
    3. Risk consolidation
    """
    
    def __init__(self, registry: ModuleRegistry):
        """
        Initialize safeguard stage.
        
        Args:
            registry: Module registry with loaded engines
        """
        self.registry = registry
        self.tau_layer = registry.get("tau")
        self.safeguard = registry.get("safeguard")
    
    def execute(self, context: UnifiedContext) -> UnifiedContext:
        """
        Execute safeguard stage.
        
        Args:
            context: Unified context
            
        Returns:
            Updated context with safety analysis results
        """
        logger.info("Safeguard stage: executing safety checks")
        
        try:
            # 1. Tau output phase
            tau_output = self.tau_layer.compute_tau_output_phase(
                drift_trajectory=context.drift_ctx.drift_state if context.drift_ctx else None,
                meta_signals=context.meta_ctx if context.meta_ctx else None,
                story_signal=context.story_ctx if context.story_ctx else None
            )
            
            # 2. Safeguard evaluation
            safeguard_result = self.safeguard.evaluate(
                tau_state=tau_output,
                drift_state=context.drift_ctx.drift_state.to_dict() if context.drift_ctx and context.drift_ctx.drift_state else {},
                polarities=context.archetype_ctx.polarity_scores if context.archetype_ctx else {},
                meta=context.meta_ctx.to_dict() if context.meta_ctx else {},
                journey_state=context.story_ctx
            )
            
            # Create risk context
            risk_ctx = RiskContext(
                tau_output=tau_output,
                safeguard=safeguard_result,
                final_risk=safeguard_result.final_risk,
                risk_score=safeguard_result.risk_score
            )
            
            context.risk_ctx = risk_ctx
            
            logger.info(f"Safeguard stage complete: risk={safeguard_result.final_risk}, score={safeguard_result.risk_score:.3f}")
            
        except Exception as e:
            logger.error(f"Safeguard stage failed: {e}")
            context.global_ctx.degraded = True
            # Create minimal risk context
            context.risk_ctx = RiskContext()
        
        return context
