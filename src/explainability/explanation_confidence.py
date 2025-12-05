"""
Confidence and Decision Tracing for KALDRA Explainability v3.4 Phase 2.

Provides confidence scoring and decision trace capabilities for explanations.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class ComponentConfidence:
    """
    Confidence score for a specific component of the explanation.
    
    Attributes:
        name: Component identifier (e.g., "delta144", "story", "multistream")
        score: Confidence score [0,1]
        reason: Brief textual description of why this score
        metadata: Additional context
    """
    name: str
    score: float
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)


@dataclass
class DecisionStep:
    """
    Single step in the decision trace showing how explanation was built.
    
    Attributes:
        step: Step identifier (e.g., "delta144_evaluation")
        description: What happened in this step
        weight: Contribution to overall explanation [0,1]
        source: Origin of decision ("engine", "heuristic", "llm")
        metadata: Additional context
    """
    step: str
    description: str
    weight: float
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)


@dataclass
class ExplanationConfidence:
    """
    Complete confidence and trace information for an explanation.
    
    Attributes:
        overall: Overall confidence score [0,1]
        components: Per-component confidence scores
        trace: Sequential decision steps
        metadata: Additional metadata
    """
    overall: float
    components: List[ComponentConfidence] = field(default_factory=list)
    trace: List[DecisionStep] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "overall": self.overall,
            "components": [c.to_dict() for c in self.components],
            "trace": [t.to_dict() for t in self.trace],
            "metadata": self.metadata
        }


class ConfidenceEngine:
    """
    Computes confidence scores and decision traces for explanations.
    
    Uses heuristic-based scoring to assess explanation quality and
    generates decision traces showing the reasoning path.
    
    Example:
        >>> engine = ConfidenceEngine()
        >>> confidence = engine.compute_from_context(unified_context, explanation)
        >>> print(confidence.overall)
        0.75
    """
    
    def __init__(self):
        """Initialize confidence engine."""
        logger.info("ConfidenceEngine initialized")
    
    def compute_from_context(
        self,
        context: Any,
        explanation: Optional[Any] = None
    ) -> ExplanationConfidence:
        """
        Compute confidence and trace from UnifiedContext.
        
        Args:
            context: UnifiedContext from KALDRA pipeline
            explanation: Optional Explanation object (for mode detection)
        
        Returns:
            ExplanationConfidence with overall score, components, and trace
        """
        try:
            # Compute component confidences
            components = self._compute_component_confidences(context)
            
            # Build decision trace
            trace = self._build_trace_from_context(context, explanation)
            
            # Compute overall confidence
            overall = self._compute_overall_confidence(context, components)
            
            return ExplanationConfidence(
                overall=overall,
                components=components,
                trace=trace,
                metadata={}
            )
        
        except Exception as e:
            logger.warning(f"ConfidenceEngine failed: {e}")
            # Return minimal confidence on error
            return ExplanationConfidence(
                overall=0.3,
                components=[],
                trace=[],
                metadata={"error": str(e)}
            )
    
    def _compute_component_confidences(self, context: Any) -> List[ComponentConfidence]:
        """
        Compute confidence for each available component.
        
        Args:
            context: UnifiedContext
        
        Returns:
            List of ComponentConfidence objects
        """
        components = []
        
        # Delta144 component
        if hasattr(context, 'archetype_ctx') and context.archetype_ctx:
            if hasattr(context.archetype_ctx, 'delta144_state') and context.archetype_ctx.delta144_state:
                state_id = getattr(context.archetype_ctx.delta144_state, 'state_id', None)
                if state_id:
                    components.append(ComponentConfidence(
                        name="delta144",
                        score=0.8,
                        reason=f"Delta144 state '{state_id}' detected with clear archetypal pattern"
                    ))
        
        # Polarities component
        if hasattr(context, 'archetype_ctx') and context.archetype_ctx:
            if hasattr(context.archetype_ctx, 'polarity_scores') and context.archetype_ctx.polarity_scores:
                polarity_count = len(context.archetype_ctx.polarity_scores)
                if polarity_count > 0:
                    score = min(0.9, 0.6 + (polarity_count * 0.1))
                    components.append(ComponentConfidence(
                        name="polarities",
                        score=score,
                        reason=f"{polarity_count} polarity scores available"
                    ))
        
        # Story component
        if hasattr(context, 'story_ctx') and context.story_ctx:
            if hasattr(context.story_ctx, 'arc') and context.story_ctx.arc:
                coherence = getattr(context.story_ctx, 'coherence', 0.5)
                score = min(0.9, 0.5 + coherence * 0.4)
                components.append(ComponentConfidence(
                    name="story",
                    score=score,
                    reason=f"Story arc detected with coherence {coherence:.2f}"
                ))
        
        # TW369/Drift component
        if hasattr(context, 'drift_ctx') and context.drift_ctx:
            regime = getattr(context.drift_ctx, 'regime', None)
            if regime and regime != "UNKNOWN":
                components.append(ComponentConfidence(
                    name="tw369",
                    score=0.75,
                    reason=f"Drift regime '{regime}' identified"
                ))
        
        # Multi-stream component (v3.3)
        if hasattr(context, 'multi_stream_ctx') and context.multi_stream_ctx:
            if hasattr(context.multi_stream_ctx, 'pairwise_results'):
                num_comparisons = len(context.multi_stream_ctx.pairwise_results)
                if num_comparisons > 0:
                    score = min(0.85, 0.6 + (num_comparisons * 0.05))
                    components.append(ComponentConfidence(
                        name="multistream",
                        score=score,
                        reason=f"{num_comparisons} stream comparisons performed"
                    ))
        
        return components
    
    def _build_trace_from_context(
        self,
        context: Any,
        explanation: Optional[Any] = None
    ) -> List[DecisionStep]:
        """
        Build decision trace from context.
        
        Args:
            context: UnifiedContext
            explanation: Optional Explanation object
        
        Returns:
            List of DecisionStep objects
        """
        trace = []
        total_weight = 0.0
        
        # Delta144 evaluation step
        if hasattr(context, 'archetype_ctx') and context.archetype_ctx:
            if hasattr(context.archetype_ctx, 'delta144_state') and context.archetype_ctx.delta144_state:
                state_id = getattr(context.archetype_ctx.delta144_state, 'state_id', None)
                if state_id:
                    trace.append(DecisionStep(
                        step="delta144_evaluation",
                        description=f"Identified archetypal state: {state_id}",
                        weight=0.2,
                        source="engine"
                    ))
                    total_weight += 0.2
        
        # Polarity balance step
        if hasattr(context, 'archetype_ctx') and context.archetype_ctx:
            if hasattr(context.archetype_ctx, 'polarity_scores') and context.archetype_ctx.polarity_scores:
                polarities = context.archetype_ctx.polarity_scores
                dominant = max(polarities.items(), key=lambda x: x[1]) if polarities else None
                if dominant:
                    trace.append(DecisionStep(
                        step="polarity_balance",
                        description=f"Dominant polarity: {dominant[0]} ({dominant[1]:.2f})",
                        weight=0.15,
                        source="engine"
                    ))
                    total_weight += 0.15
        
        # Story arc step
        if hasattr(context, 'story_ctx') and context.story_ctx:
            if hasattr(context.story_ctx, 'arc') and context.story_ctx.arc:
                arc = context.story_ctx.arc
                stage = getattr(arc, 'dominant_stage', 'unknown')
                trace.append(DecisionStep(
                    step="story_arc",
                    description=f"Narrative arc stage: {stage}",
                    weight=0.2,
                    source="engine"
                ))
                total_weight += 0.2
        
        # Drift regime step
        if hasattr(context, 'drift_ctx') and context.drift_ctx:
            regime = getattr(context.drift_ctx, 'regime', None)
            if regime and regime != "UNKNOWN":
                trace.append(DecisionStep(
                    step="drift_regime",
                    description=f"Drift regime identified: {regime}",
                    weight=0.15,
                    source="engine"
                ))
                total_weight += 0.15
        
        # Multi-stream divergence step
        if hasattr(context, 'multi_stream_ctx') and context.multi_stream_ctx:
            max_div = getattr(context.multi_stream_ctx, 'max_divergence', None)
            if max_div is not None:
                convergent = "convergent" if max_div < 0.7 else "divergent"
                trace.append(DecisionStep(
                    step="multistream_divergence",
                    description=f"Multi-stream analysis: {convergent} (div={max_div:.2f})",
                    weight=0.15,
                    source="engine"
                ))
                total_weight += 0.15
        
        # Explanation mode step
        if explanation:
            mode = "barebones"
            if hasattr(explanation, 'details'):
                # Try to infer mode from explanation
                if "LLM" in explanation.summary:
                    mode = "llm"
                elif len(explanation.details) > 2:
                    mode = "template"
            
            trace.append(DecisionStep(
                step="explanation_mode",
                description=f"Explanation generated via {mode} mode",
                weight=0.15,
                source="explainability"
            ))
            total_weight += 0.15
        
        # Normalize weights if needed
        if total_weight > 1.0:
            for step in trace:
                step.weight = step.weight / total_weight
        
        return trace
    
    def _compute_overall_confidence(
        self,
        context: Any,
        components: List[ComponentConfidence]
    ) -> float:
        """
        Compute overall confidence score.
        
        Args:
            context: UnifiedContext
            components: List of component confidences
        
        Returns:
            Overall confidence [0,1]
        """
        # Start with base score
        overall = 0.5
        
        # Penalize if context is degraded
        if hasattr(context, 'global_ctx') and context.global_ctx:
            if getattr(context.global_ctx, 'degraded', False):
                overall -= 0.2
        
        # Boost based on number of components
        component_boost = len(components) * 0.08
        overall += component_boost
        
        # Average in component scores
        if components:
            avg_component_score = sum(c.score for c in components) / len(components)
            overall = (overall + avg_component_score) / 2
        
        # Clamp to [0,1]
        return max(0.0, min(1.0, overall))
