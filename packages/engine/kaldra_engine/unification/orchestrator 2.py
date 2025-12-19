"""
Orchestrator for KALDRA v3.0 Pipeline.

Executes the complete pipeline by coordinating all stages.
"""
from typing import Dict, Any
import logging

from .states.unified_state import UnifiedContext, InputContext
from .states.unified_context import ContextManager
from .router import PipelineConfig, UnifiedRouter
from .registry import ModuleRegistry

# Import pipeline stages
from .pipeline.input_stage import InputStage
from .pipeline.core_stage import CoreStage
from .pipeline.meta_stage import MetaStage
from .pipeline.story_stage import StoryStage
from .pipeline.safeguard_stage import SafeguardStage
from .pipeline.output_stage import OutputStage

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """
    Pipeline orchestrator for KALDRA v3.0.
    
    Coordinates execution of all pipeline stages according to
    the routing configuration.
    
    Pipeline Flow:
    Input → Core → Meta → Story → Safeguard → Output
    """
    
    def __init__(self, registry: ModuleRegistry):
        """
        Initialize orchestrator.
        
        Args:
            registry: Module registry with loaded engines
        """
        self.registry = registry
        self.router = UnifiedRouter()
        
        # Initialize all stages
        self.stages = {
            "input": InputStage(registry),
            "core": CoreStage(registry),
            "meta": MetaStage(registry),
            "story": StoryStage(registry),
            "safeguard": SafeguardStage(registry),
            "output": OutputStage(registry)
        }
    
    def execute(
        self,
        input_text: str,
        mode: str = "full",
        context_dict: Dict[str, Any] = None
    ) -> UnifiedContext:
        """
        Execute the complete pipeline.
        
        Args:
            input_text: Text to analyze
            mode: Execution mode
            context_dict: Optional context dictionary
            
        Returns:
            Unified context with complete results
        """
        # 1. Route execution
        config = self.router.route(input_text, mode, context_dict or {})
        
        logger.info(f"Orchestrator: executing pipeline (mode={mode}, stages={len(config.stages)})")
        
        # 2. Create initial context
        context = ContextManager.create_context(input_text, mode=mode)
        context.input_ctx = InputContext(text=input_text)
        
        # 3. Execute stages in order
        for stage_name in config.stages:
            if stage_name not in self.stages:
                logger.warning(f"Unknown stage '{stage_name}', skipping")
                continue
            
            try:
                logger.debug(f"Executing stage: {stage_name}")
                stage = self.stages[stage_name]
                context = stage.execute(context)
                
            except Exception as e:
                logger.error(f"Stage '{stage_name}' failed: {e}")
                ContextManager.mark_degraded(context, f"Stage {stage_name} failed")
                # Continue with next stage (graceful degradation)
        
        logger.info(f"Orchestrator: pipeline complete (degraded={context.global_ctx.degraded})")
        
        return context
    
    def get_stage(self, name: str):
        """Get a specific stage."""
        return self.stages.get(name)
    
    def list_stages(self) -> list:
        """List all available stages."""
        return list(self.stages.keys())
