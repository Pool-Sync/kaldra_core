"""
Meta Stage for KALDRA v3.0 Pipeline.

Handles:
- Nietzsche Engine
- Aurelius Engine  
- Campbell Engine
- Polarity mapping
"""
from typing import Optional
import logging

from src.unification.states.unified_state import UnifiedContext, MetaContext
from src.unification.registry import ModuleRegistry
from src.meta.types import MetaInput

# Import Meta Engines
from src.meta.nietzsche import NietzscheEngine
from src.meta.aurelius import AureliusEngine
from src.meta.campbell_engine import CampbellEngine

logger = logging.getLogger(__name__)


class MetaStage:
    """
    Meta-engine philosophical analysis stage.
    
    Responsibilities:
    1. Nietzsche Engine (Will to Power, etc.)
    2. Aurelius Engine (Stoic analysis)
    3. Campbell Engine (Hero's Journey)
    4. Polarity mapping
    """
    
    def __init__(self, registry: ModuleRegistry):
        """
        Initialize meta stage.
        
        Args:
            registry: Module registry with loaded engines
        """
        self.registry = registry
        # Meta engines will be loaded in future phases
        self.meta_engines_available = False
    
    def execute(self, context: UnifiedContext) -> UnifiedContext:
        """
        Execute meta-analysis engines.
        
        Args:
            context: UnifiedContext with core analysis complete
            
        Returns:
            UnifiedContext with populated meta_ctx
        """
        logger.info("Meta stage: executing philosophical analysis")
        
        try:
            # Build MetaInput from UnifiedContext
            # Extract fields safely handling optional contexts
            delta144_state_id = None
            if context.archetype_ctx and context.archetype_ctx.delta144_state:
                # Assuming delta144_state object has 'id' attribute or is a string
                # If it's an object, we try to access .id, else str()
                d_state = context.archetype_ctx.delta144_state
                delta144_state_id = getattr(d_state, 'id', str(d_state)) if d_state else None

            archetype_scores = {}
            if context.archetype_ctx and context.archetype_ctx.delta12:
                # Assuming delta12 has .scores or .to_dict()
                if hasattr(context.archetype_ctx.delta12, 'scores'):
                    archetype_scores = context.archetype_ctx.delta12.scores
                elif hasattr(context.archetype_ctx.delta12, 'to_dict'):
                    archetype_scores = context.archetype_ctx.delta12.to_dict()
            
            tw_state = None
            if context.drift_ctx and context.drift_ctx.tw_state:
                tw_state = context.drift_ctx.tw_state

            polarities = {}
            modifiers = {}
            if context.archetype_ctx:
                polarities = context.archetype_ctx.polarity_scores
                modifiers = context.archetype_ctx.modifier_scores

            meta_input = MetaInput(
                text=context.input_ctx.text if context.input_ctx else "",
                delta144_state=delta144_state_id,
                archetype_scores=archetype_scores,
                kindra=context.kindra_ctx,
                tw_state=tw_state,
                polarity_scores=polarities,
                modifiers=modifiers
            )

            nietzsche_sig = None
            aurelius_sig = None
            campbell_sig = None

            # Execute NietzscheEngine
            try:
                if hasattr(self, "registry") and self.registry:
                     nietzsche_engine = self.registry.get("nietzsche")
                     if not nietzsche_engine: # Fallback if registry returns None
                         nietzsche_engine = NietzscheEngine()
                else:
                     nietzsche_engine = NietzscheEngine()
                     
                nietzsche_sig = nietzsche_engine.analyze(meta_input)
            except Exception as e:
                self._warn("NietzscheEngine failed", e)

            # Execute AureliusEngine
            try:
                if hasattr(self, "registry") and self.registry:
                    aurelius_engine = self.registry.get("aurelius")
                    if not aurelius_engine:
                        aurelius_engine = AureliusEngine()
                else:
                    aurelius_engine = AureliusEngine()
                    
                aurelius_sig = aurelius_engine.analyze(meta_input)
            except Exception as e:
                self._warn("AureliusEngine failed", e)

            # Execute CampbellEngine
            try:
                if hasattr(self, "registry") and self.registry:
                    campbell_engine = self.registry.get("campbell")
                    if not campbell_engine:
                        campbell_engine = CampbellEngine()
                else:
                    campbell_engine = CampbellEngine()

                campbell_sig = campbell_engine.analyze(meta_input)
            except Exception as e:
                self._warn("CampbellEngine failed", e)

            # Populate MetaContext
            context.meta_ctx = MetaContext(
                nietzsche=nietzsche_sig,
                aurelius=aurelius_sig,
                campbell=campbell_sig
            )
            
            logger.info("Meta stage complete")
            
        except Exception as e:
            logger.error(f"Meta stage failed: {e}")
            context.global_ctx.degraded = True
        
        return context

    def _warn(self, message, exception):
        print(f"[MetaStage Warning] {message}: {exception}")
