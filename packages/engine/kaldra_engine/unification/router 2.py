"""
Router for KALDRA v3.0 Pipeline.

Intelligent routing based on execution mode and context.
"""
from typing import Dict, Any, List
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """
    Configuration for pipeline execution.
    
    Defines which stages to execute and in what order.
    """
    mode: str
    stages: List[str] = field(default_factory=list)
    skip_story: bool = False
    strict_safety: bool = False
    max_depth: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'mode': self.mode,
            'stages': self.stages,
            'skip_story': self.skip_story,
            'strict_safety': self.strict_safety,
            'max_depth': self.max_depth
        }


class UnifiedRouter:
    """
    Intelligent router for KALDRA v3.0 pipeline.
    
    Routes execution based on mode and context, determining:
    - Which stages to execute
    - Execution order
    - Safety constraints
    - Performance optimizations
    """
    
    # Standard pipeline stages
    ALL_STAGES = [
        "input",
        "core",
        "meta",
        "story",
        "safeguard",
        "output"
    ]
    
    def route(
        self,
        input_text: str,
        mode: str,
        context: Dict[str, Any]
    ) -> PipelineConfig:
        """
        Route execution based on mode and context.
        
        Args:
            input_text: Input text
            mode: Execution mode
            context: Additional context
            
        Returns:
            Pipeline configuration
        """
        logger.info(f"Routing: mode={mode}")
        
        if mode == "signal":
            return self._route_signal_mode()
        elif mode == "story":
            return self._route_story_mode()
        elif mode == "full":
            return self._route_full_mode()
        elif mode == "safety-first":
            return self._route_safety_first_mode()
        elif mode == "exploratory":
            return self._route_exploratory_mode()
        else:
            logger.warning(f"Unknown mode '{mode}', defaulting to 'full'")
            return self._route_full_mode()
    
    def _route_signal_mode(self) -> PipelineConfig:
        """
        Fast mode: Core pipeline only.
        
        Skips:
        - Story analysis (temporal)
        - Meta engines (philosophical)
        
        Optimized for speed.
        """
        return PipelineConfig(
            mode="signal",
            stages=["input", "core", "safeguard", "output"],
            skip_story=True
        )
    
    def _route_story_mode(self) -> PipelineConfig:
        """
        Story mode: Full temporal analysis.
        
        Emphasizes:
        - Story engine
        - Narrative arcs
        - Temporal coherence
        """
        return PipelineConfig(
            mode="story",
            stages=self.ALL_STAGES
        )
    
    def _route_full_mode(self) -> PipelineConfig:
        """
        Full mode: Complete analysis (default).
        
        Executes all stages.
        """
        return PipelineConfig(
            mode="full",
            stages=self.ALL_STAGES
        )
    
    def _route_safety_first_mode(self) -> PipelineConfig:
        """
        Safety-first mode: Strict safety checks.
        
        Emphasizes:
        - Tau layer
        - Safeguard engine
        - Risk mitigation
        """
        return PipelineConfig(
            mode="safety-first",
            stages=self.ALL_STAGES,
            strict_safety=True
        )
    
    def _route_exploratory_mode(self) -> PipelineConfig:
        """
        Exploratory mode: Maximum depth.
        
        Executes all stages with maximum detail.
        """
        return PipelineConfig(
            mode="exploratory",
            stages=self.ALL_STAGES,
            max_depth=True
        )
