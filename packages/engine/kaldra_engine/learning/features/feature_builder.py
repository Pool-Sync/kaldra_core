"""
Feature Builder for learned mappings (v3.5 Phase 2).

Extracts features from UnifiedContext for learning.
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class LearningFeatureVector:
    """
    Feature vector for learned mapping.
    
    Attributes:
        domain: Domain identifier (alpha, geo, product, safeguard)
        delta144_state_id: Current Δ144 state (if available)
        delta12_scores: Delta12 archetype scores
        kindra_scores: Kindra scores (3×48)
        polarity_scores: Polarity scores
        tw_regime: TW369 regime (if available)
        coherence_score: Story coherence (if available)
        extras: Additional metadata
    """
    domain: str
    delta144_state_id: Optional[str] = None
    delta12_scores: Dict[str, float] = field(default_factory=dict)
    kindra_scores: Dict[str, float] = field(default_factory=dict)
    polarity_scores: Dict[str, float] = field(default_factory=dict)
    tw_regime: Optional[str] = None
    coherence_score: Optional[float] = None
    extras: Dict[str, Any] = field(default_factory=dict)


def build_from_unified_context(context: Any, domain: str) -> LearningFeatureVector:
    """
    Build feature vector from UnifiedContext.
    
    Args:
        context: UnifiedContext instance
        domain: Domain identifier
    
    Returns:
        LearningFeatureVector with extracted features
    """
    features = LearningFeatureVector(domain=domain)
    
    try:
        # Extract Δ144 state
        if hasattr(context, 'archetype_ctx') and context.archetype_ctx:
            if hasattr(context.archetype_ctx, 'delta144_state') and context.archetype_ctx.delta144_state:
                features.delta144_state_id = getattr(context.archetype_ctx.delta144_state, 'state_id', None)
            
            # Extract Delta12
            if hasattr(context.archetype_ctx, 'delta12') and context.archetype_ctx.delta12:
                delta12 = context.archetype_ctx.delta12
                if hasattr(delta12, 'to_dict'):
                    features.delta12_scores = delta12.to_dict()
            
            # Extract polarities
            if hasattr(context.archetype_ctx, 'polarity_scores'):
                features.polarity_scores = context.archetype_ctx.polarity_scores or {}
        
        # Extract Kindra (if available)
        if hasattr(context, 'kindra_ctx') and context.kindra_ctx:
            if hasattr(context.kindra_ctx, 'scores'):
                features.kindra_scores = context.kindra_ctx.scores or {}
        
        # Extract TW369 regime
        if hasattr(context, 'drift_ctx') and context.drift_ctx:
            if hasattr(context.drift_ctx, 'regime'):
                features.tw_regime = context.drift_ctx.regime
        
        # Extract story coherence
        if hasattr(context, 'story_ctx') and context.story_ctx:
            if hasattr(context.story_ctx, 'coherence'):
                features.coherence_score = context.story_ctx.coherence
    
    except Exception as e:
        logger.warning(f"Error extracting features: {e}")
    
    return features
