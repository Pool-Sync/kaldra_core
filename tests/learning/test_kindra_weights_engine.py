"""
Unit tests for Kindra Weights Engine (v3.5 Phase 2).
"""
import pytest
from src.learning.kindra_weights_engine import KindraWeightsEngine, KindraWeightVector
from src.learning.features.feature_builder import LearningFeatureVector


class TestKindraWeightsEngine:
    """Test suite for Kindra weights engine."""
    
    def test_get_weights_for_domain(self):
        """Test getting weights for specific domain."""
        config = {
            "domain_weights": {
                "alpha": {"k1": 0.8, "k2": 0.5},
                "geo": {"k1": 0.3, "k3": 0.7}
            }
        }
        
        engine = KindraWeightsEngine(config)
        weights = engine.get_weights("alpha")
        
        assert weights.domain == "alpha"
        assert weights.weights["k1"] == 0.8
        assert weights.weights["k2"] == 0.5
    
    def test_get_weights_unknown_domain_returns_empty(self):
        """Test that unknown domain returns empty weights."""
        config = {"domain_weights": {"alpha": {"k1": 1.0}}}
        
        engine = KindraWeightsEngine(config)
        weights = engine.get_weights("unknown")
        
        assert weights.domain == "unknown"
        assert weights.weights == {}
    
    def test_update_from_observations_stub(self):
        """Test update_from_observations (stub in Phase 2)."""
        config = {"domain_weights": {}}
        engine = KindraWeightsEngine(config)
        
        observations = [
            LearningFeatureVector(domain="alpha", kindra_scores={"k1": 0.5})
        ]
        
        # Should not crash (stub implementation)
        engine.update_from_observations(observations)
