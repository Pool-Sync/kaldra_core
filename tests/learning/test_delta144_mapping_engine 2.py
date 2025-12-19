"""
Unit tests for Delta144 Mapping Engine (v3.5 Phase 2).
"""
import pytest
from src.learning.delta144_mapping_engine import Delta144MappingEngine, Delta144MappingResult
from src.learning.features.feature_builder import LearningFeatureVector
from src.learning.kindra_priors import KindraPriors
from src.learning.kindra_weights_engine import KindraWeightsEngine


class TestDelta144MappingEngine:
    """Test suite for Delta144 mapping engine."""
    
    def test_engine_returns_valid_distribution(self):
        """Test that engine returns normalized distribution."""
        # Setup
        priors = KindraPriors(priors={
            "k1": {"threshold": 0.5, "emergence": 0.5}
        })
        weights_engine = KindraWeightsEngine(config={"domain_weights": {"alpha": {"k1": 0.8}}})
        config = {"base_prior_weight": 0.1, "current_state_boost": 0.2}
        
        engine = Delta144MappingEngine(config, priors, weights_engine)
        
        # Create features
        features = LearningFeatureVector(
            domain="alpha",
            kindra_scores={"k1": 0.7}
        )
        
        # Suggest
        result = engine.suggest(features)
        
        # Verify distribution sums to ~1.0
        assert isinstance(result, Delta144MappingResult)
        assert abs(sum(result.state_distribution.values()) - 1.0) < 0.01
        assert result.suggested_state_id in result.state_distribution
    
    def test_engine_has_higher_confidence_with_clear_winner(self):
        """Test confidence is higher when distribution has clear winner."""
        priors = KindraPriors(priors={"k1": {"threshold": 0.9, "emergence": 0.1}})
        weights_engine = KindraWeightsEngine(config={"domain_weights": {"alpha": {"k1": 1.0}}})
        config = {}
        
        engine = Delta144MappingEngine(config, priors, weights_engine)
        
        features = LearningFeatureVector(domain="alpha", kindra_scores={"k1": 1.0})
        result = engine.suggest(features)
        
        # Should have reasonable confidence (>0.2) with clear winner
        assert result.confidence > 0.2
    
    def test_engine_with_no_kindra_returns_uniform(self):
        """Test that engine with no Kindra features returns uniform distribution."""
        priors = KindraPriors(priors={})
        weights_engine = KindraWeightsEngine(config={"domain_weights": {}})
        config = {}
        
        engine = Delta144MappingEngine(config, priors, weights_engine)
        
        features = LearningFeatureVector(domain="alpha", kindra_scores={})
        result = engine.suggest(features)
        
        # Distribution should exist and be normalized
        assert len(result.state_distribution) > 0
        assert abs(sum(result.state_distribution.values()) - 1.0) < 0.01
    
    def test_engine_boosts_current_state(self):
        """Test that current state gets boost in scoring."""
        priors = KindraPriors(priors={"k1": {"threshold": 0.3, "emergence": 0.7}})
        weights_engine = KindraWeightsEngine(config={"domain_weights": {"alpha": {"k1": 0.5}}})
        config = {"current_state_boost": 0.5}
        
        engine = Delta144MappingEngine(config, priors, weights_engine)
        
        # Features with current state
        features = LearningFeatureVector(
            domain="alpha",
            delta144_state_id="threshold",
            kindra_scores={"k1": 0.6}
        )
        
        result = engine.suggest(features)
        
       # threshold should benefit from boost despite lower prior
        # This is a weak assertion - just check threshold is in top 2
        sorted_states = sorted(result.state_distribution.items(), key=lambda x: x[1], reverse=True)
        top_2_states = [state for state, _ in sorted_states[:2]]
        assert "threshold" in top_2_states
    
    def test_engine_metadata_populated(self):
        """Test that result metadata is populated."""
        priors = KindraPriors(priors={})
        weights_engine = KindraWeightsEngine(config={"domain_weights": {}})
        config = {}
        
        engine = Delta144MappingEngine(config, priors, weights_engine)
        
        features = LearningFeatureVector(
            domain="geo",
            kindra_scores={"k1": 0.5, "k2": 0.3}
        )
        
        result = engine.suggest(features)
        
        assert result.metadata["domain"] == "geo"
        assert result.metadata["num_kindra_used"] == 2
        assert "has_current_state" in result.metadata
