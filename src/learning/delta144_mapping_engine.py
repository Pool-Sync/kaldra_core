"""
Delta144 Learned Mapping Engine (v3.5 Phase 2).

Provides learned Kindra→Δ144 mappings with domain-specific adjustments.
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class Delta144MappingResult:
    """
    Result from learned mapping engine.
    
    Attributes:
        suggested_state_id: Recommended Δ144 state
        state_distribution: Probability distribution over states
        confidence: Confidence score [0,1]
        metadata: Additional information
    """
    suggested_state_id: Optional[str] = None
    state_distribution: Dict[str, float] = field(default_factory=dict)
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class Delta144MappingEngine:
    """
    Learned mapping engine for Kindra→Δ144.
    
    Combines:
    - Kindra priors (base mappings)
    - Learned weights (domain-specific)
    - Current context features
    
    Example:
        >>> engine = Delta144MappingEngine(config, priors, weights_engine)
        >>> result = engine.suggest(features)
        >>> print(result.suggested_state_id)
    """
    
    def __init__(self, config: Dict[str, Any], priors: Any, weights_engine: Any):
        """
        Initialize mapping engine.
        
        Args:
            config: Configuration dictionary
            priors: KindraPriors instance
            weights_engine: KindraWeightsEngine instance
        """
        self.config = config
        self.priors = priors
        self.weights_engine = weights_engine
        logger.info("Delta144MappingEngine initialized")
    
    
    def suggest(self, features: Any) -> Delta144MappingResult:
        """
        Suggest Δ144 state from features.
        
        Uses heuristic formula:
        score[state] = bias_prior[state] + Σ(kindra_score * kindra_weight * prior_k_to_state)
                       + λ * indicator(state == current_state)
        
        Args:
            features: LearningFeatureVector instance
        
        Returns:
            Delta144MappingResult with suggestion
        """
        logger.info(f"Suggesting Δ144 state for domain: {features.domain}")
        
        # Get domain weights
        domain_weights = self.weights_engine.get_weights(features.domain)
        
        # Initialize state scores
        state_scores = {}
        
        # Get all possible states (from priors or default set)
        possible_states = self._get_possible_states(features)
        
        for state in possible_states:
            # Base prior score
            score = self.config.get("base_prior_weight", 0.1)
            
            # Add Kindra contributions
            for kindra_id, kindra_score in features.kindra_scores.items():
                # Get weight for this Kindra in this domain
                kindra_weight = domain_weights.weights.get(kindra_id, 0.5)
                
                # Get prior mapping kindra -> state
                kindra_prior = self.priors.get_prior(kindra_id)
                prior_to_state = kindra_prior.get(state, 0.0)
                
                # Add contribution
                score += kindra_score * kindra_weight * prior_to_state
            
            # Bias toward current state if available
            if features.delta144_state_id == state:
                current_state_boost = self.config.get("current_state_boost", 0.2)
                score += current_state_boost
            
            state_scores[state] = score
        
        # Normalize to distribution
        distribution = self._normalize_distribution(state_scores)
        
        # Get suggested state (argmax)
        suggested_state = max(distribution.items(), key=lambda x: x[1])[0] if distribution else None
        
        # Compute confidence
        confidence = self._compute_confidence(distribution, features)
        
        return Delta144MappingResult(
            suggested_state_id=suggested_state,
            state_distribution=distribution,
            confidence=confidence,
            metadata={
                "domain": features.domain,
                "num_kindra_used": len(features.kindra_scores),
                "has_current_state": features.delta144_state_id is not None
            }
        )
    
    def _get_possible_states(self, features: Any) -> list:
        """Get list of possible Delta144 states."""
        # Default KALDRA Delta144 states
        return [
            "threshold",
            "emergence",
            "integration",
            "transformation",
            "return",
            "call"
        ]
    
    def _normalize_distribution(self, scores: Dict[str, float]) -> Dict[str, float]:
        """Normalize scores to probability distribution."""
        if not scores:
            return {}
        
        total = sum(scores.values())
        if total == 0:
            # Uniform distribution
            n = len(scores)
            return {state: 1.0/n for state in scores}
        
        return {state: score/total for state, score in scores.items()}
    
    def _compute_confidence(self, distribution: Dict[str, float], features: Any) -> float:
        """
        Compute confidence in suggestion.
        
        Higher confidence when:
        - Clear winner in distribution
        - More Kindra features available
        - Richer context
        """
        if not distribution:
            return 0.0
        
        # Entropy-based confidence (lower entropy = higher confidence)
        import math
        entropy = -sum(p * math.log(p + 1e-10) for p in distribution.values())
        max_entropy = math.log(len(distribution))
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 1.0
        
        # Confidence from distribution clarity
        confidence_from_dist = 1.0 - normalized_entropy
        
        # Boost from feature richness
        feature_richness = min(len(features.kindra_scores) / 10.0, 1.0)  # Normalize to [0,1]
        
        # Combined confidence
        confidence = 0.7 * confidence_from_dist + 0.3 * feature_richness
        
        return min(max(confidence, 0.0), 1.0)  # Clamp to [0,1]

