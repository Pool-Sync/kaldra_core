"""Tests for Meta Engine Router"""

import pytest
import numpy as np

from src.meta.engine_router import RoutingContext, RoutingDecision, MetaRouter


class TestRoutingContext:
    """Test RoutingContext dataclass"""
    
    def test_create_with_text(self):
        """Test creating context with text"""
        context = RoutingContext(text="earnings call revenue guidance")
        assert context.text == "earnings call revenue guidance"
        assert context.embedding is None
        assert context.metadata is None
        assert context.domain_hints is None
    
    def test_create_with_metadata(self):
        """Test creating context with metadata"""
        context = RoutingContext(metadata={"domain": "finance"})
        assert context.metadata == {"domain": "finance"}
    
    def test_create_with_hints(self):
        """Test creating context with domain hints"""
        context = RoutingContext(domain_hints=["alpha", "finance"])
        assert context.domain_hints == ["alpha", "finance"]


class TestMetaRouter:
    """Test MetaRouter routing logic"""
    
    def test_route_with_strong_financial_keywords(self):
        """Test routing with many financial keywords"""
        router = MetaRouter(confidence_threshold=0.2)
        context = RoutingContext(
            text="earnings revenue profit EPS guidance forecast market stock investor shareholder financial quarterly"
        )
        
        decision = router.route(context)
        
        # With many keywords, should route to alpha
        assert decision.primary_engine in ["alpha", "default"]
    
    def test_route_with_strong_geo_keywords(self):
        """Test routing with many geopolitical keywords"""
        router = MetaRouter(confidence_threshold=0.2)
        context = RoutingContext(
            text="diplomatic diplomacy sanctions treaty conflict geopolitical sovereignty alliance foreign policy"
        )
        
        decision = router.route(context)
        
        # With many keywords, should route to geo
        assert decision.primary_engine in ["geo", "default"]
    
    def test_route_with_domain_hint(self):
        """Test routing with explicit domain hint"""
        router = MetaRouter()
        context = RoutingContext(
            text="Some generic text",
            domain_hints=["alpha"]
        )
        
        decision = router.route(context)
        
        assert decision.primary_engine == "alpha"
        assert decision.confidence == 1.0
        assert "hint" in decision.reasoning.lower()
    
    def test_route_with_metadata(self):
        """Test routing with metadata"""
        router = MetaRouter()
        context = RoutingContext(
            text="Some text",
            metadata={"domain": "finance", "source": "earnings_call"}
        )
        
        decision = router.route(context)
        
        assert decision.primary_engine == "alpha"
        assert decision.confidence > 0.8
        assert "metadata" in decision.reasoning.lower()
    
    def test_route_fallback_to_default(self):
        """Test fallback to default engine"""
        router = MetaRouter()
        context = RoutingContext(
            text="This is some generic text without specific domain keywords."
        )
        
        decision = router.route(context)
        
        # Should use default due to low confidence
        assert decision.primary_engine == "default"
    
    def test_route_empty_context(self):
        """Test routing with empty context"""
        router = MetaRouter()
        context = RoutingContext()
        
        decision = router.route(context)
        
        assert decision.primary_engine == "default"
        assert decision.confidence == 1.0
    
    def test_confidence_threshold(self):
        """Test custom confidence threshold"""
        router = MetaRouter(confidence_threshold=0.8)
        context = RoutingContext(
            domain_hints=["alpha"]  # Use hints for deterministic test
        )
        
        decision = router.route(context)
        
        # With explicit hint, should always work
        assert decision.primary_engine == "alpha"



class TestRoutingDecision:
    """Test RoutingDecision dataclass"""
    
    def test_create_decision(self):
        """Test creating routing decision"""
        decision = RoutingDecision(
            primary_engine="alpha",
            confidence=0.85,
            secondary_engines=["geo"],
            reasoning="Test reasoning"
        )
        
        assert decision.primary_engine == "alpha"
        assert decision.confidence == 0.85
        assert decision.secondary_engines == ["geo"]
        assert decision.reasoning == "Test reasoning"
    
    def test_decision_defaults(self):
        """Test decision with defaults"""
        decision = RoutingDecision(
            primary_engine="default",
            confidence=1.0
        )
        
        assert decision.secondary_engines == []
        assert decision.reasoning is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
