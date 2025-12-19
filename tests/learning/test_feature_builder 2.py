"""
Unit tests for Feature Builder (v3.5 Phase 2).
"""
import pytest
from src.learning.features.feature_builder import LearningFeatureVector, build_from_unified_context
from src.unification.states.unified_state import (
    UnifiedContext,
    GlobalContext,
    ArchetypeContext,
    DriftContext,
    StoryContext
)


class TestFeatureBuilder:
    """Test suite for feature extraction."""
    
    def test_build_from_unified_context_complete(self):
        """Test feature extraction with complete context."""
        # Mock Delta144 state
        from unittest.mock import Mock
        mock_delta144 = Mock()
        mock_delta144.state_id = "threshold"
        
        # Mock Delta12
        mock_delta12 = Mock()
        mock_delta12.to_dict = Mock(return_value={"hero": 0.8, "sage": 0.3})
        
        # Create context
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(
                delta144_state=mock_delta144,
                delta12=mock_delta12,
                polarity_scores={"order": 0.7, "chaos": 0.3}
            ),
            drift_ctx=DriftContext(regime="STABLE"),
            story_ctx=StoryContext(coherence=0.85)
        )
        
        # Build features
        features = build_from_unified_context(context, "alpha")
        
        # Verify
        assert features.domain == "alpha"
        assert features.delta144_state_id == "threshold"
        assert features.delta12_scores == {"hero": 0.8, "sage": 0.3}
        assert features.polarity_scores == {"order": 0.7, "chaos": 0.3}
        assert features.tw_regime == "STABLE"
        assert features.coherence_score == 0.85
    
    def test_build_from_unified_context_partial(self):
        """Test feature extraction with partial context (missing TW, Story)."""
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(polarity_scores={"order": 0.6})
        )
        
        features = build_from_unified_context(context, "geo")
        
        # Verify
        assert features.domain == "geo"
        assert features.delta144_state_id is None
        assert features.tw_regime is None
        assert features.coherence_score is None
        assert features.polarity_scores == {"order": 0.6}
    
    def test_build_from_unified_context_different_domains(self):
        """Test feature extraction for different domains."""
        context = UnifiedContext(global_ctx=GlobalContext())
        
        for domain in ["alpha", "geo", "product", "safeguard"]:
            features = build_from_unified_context(context, domain)
            assert features.domain == domain
            assert isinstance(features, LearningFeatureVector)
