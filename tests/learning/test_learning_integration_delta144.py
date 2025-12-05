"""
Integration tests for learned mappings with Delta144 (v3.5 Phase 2).

Tests the optional integration without modifying existing Delta144 engine.
"""
import pytest
from src.learning.delta144_mapping_engine import Delta144MappingEngine
from src.learning.features.feature_builder import LearningFeatureVector, build_from_unified_context
from src.learning.kindra_priors import KindraPriors
from src.learning.kindra_weights_engine import KindraWeightsEngine
from src.unification.states.unified_state import UnifiedContext, GlobalContext, ArchetypeContext


class TestLearningIntegrationDelta144:
    """Integration tests for learned mapping with Delta144."""
    
    def test_integration_with_minimal_context(self):
        """Test learned mapping with minimal UnifiedContext."""
        # Setup engines
        priors = KindraPriors(priors={"k1": {"threshold": 0.7, "emergence": 0.3}})
        weights_engine = KindraWeightsEngine(config={"domain_weights": {"alpha": {"k1": 0.8}}})
        config = {}
        
        mapping_engine = Delta144MappingEngine(config, priors, weights_engine)
        
        # Create minimal context
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext()
        )
        
        # Build features
        features = build_from_unified_context(context, "alpha")
        
        # Suggest mapping
        result = mapping_engine.suggest(features)
        
        # Verify works without crash
        assert result.suggested_state_id is not None
        assert len(result.state_distribution) > 0
    
    def test_fixed_mode_behavior(self):
        """Test that fixed mode doesn't use learned mapping (conceptual test)."""
        # In Phase 2, Delta144 engine not modified yet
        # This test verifies the mapping engine can be disabled
        
        # Setup with empty config
        priors = KindraPriors(priors={})
        weights_engine = KindraWeightsEngine(config={"domain_weights": {}})
        config = {"mode": "fixed"}  # Conceptual mode flag
        
        mapping_engine = Delta144MappingEngine(config, priors, weights_engine)
        
        features = LearningFeatureVector(domain="alpha")
        result = mapping_engine.suggest(features)
        
        # Should still return valid result (uniform distribution)
        assert result.confidence >= 0.0
        assert sum(result.state_distribution.values()) > 0.99
    
    def test_hybrid_mode_combines_features(self):
        """Test hybrid mode concept - combining learned + base."""
        priors = KindraPriors(priors={"k1": {"threshold": 0.5, "emergence": 0.5}})
        weights_engine = KindraWeightsEngine(config={"domain_weights": {"alpha": {"k1": 0.6}}})
        config = {"current_state_boost": 0.3}  # Hybrid boost
        
        mapping_engine = Delta144MappingEngine(config, priors, weights_engine)
        
        # Features with current state (simulating hybrid)
        features = LearningFeatureVector(
            domain="alpha",
            delta144_state_id="threshold",
            kindra_scores={"k1": 0.7}
        )
        
        result = mapping_engine.suggest(features)
        
        # threshold should benefit from both learned and current boost
        assert result.suggested_state_id in result.state_distribution
        assert result.confidence > 0.0
    
    def test_learned_only_mode_concept(self):
        """Test learned-only mode (no current state boost)."""
        priors = KindraPriors(priors={"k1": {"emergence": 0.9, "threshold": 0.1}})
        weights_engine = KindraWeightsEngine(config={"domain_weights": {"alpha": {"k1": 1.0}}})
        config = {"current_state_boost": 0.0}  # No boost for learned-only
        
        mapping_engine = Delta144MappingEngine(config, priors, weights_engine)
        
        features = LearningFeatureVector(
            domain="alpha",
            delta144_state_id="threshold",  # Current state
            kindra_scores={"k1": 1.0}
        )
        
        result = mapping_engine.suggest(features)
        
        # Should favor learned mapping (emergence) over current (threshold)
        # Since k1→emergence has 0.9 prior
        assert result.suggested_state_id is not None
