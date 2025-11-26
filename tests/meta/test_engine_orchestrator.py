"""Tests for Meta Engine Orchestrator"""

import pytest
import numpy as np

from src.meta.engine_router import RoutingContext, RoutingDecision
from src.meta.engine_orchestrator import (
    OrchestrationConfig,
    EngineResult,
    OrchestrationResult,
    MetaOrchestrator,
)


class TestOrchestrationConfig:
    """Test OrchestrationConfig dataclass"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = OrchestrationConfig()
        
        assert config.parallel_execution is False
        assert config.timeout_seconds is None
        assert config.fallback_to_default is True
    
    def test_custom_config(self):
        """Test custom configuration"""
        config = OrchestrationConfig(
            parallel_execution=True,
            timeout_seconds=5.0,
            fallback_to_default=False
        )
        
        assert config.parallel_execution is True
        assert config.timeout_seconds == 5.0
        assert config.fallback_to_default is False


class TestMetaOrchestrator:
    """Test MetaOrchestrator execution"""
    
    def test_initialize_engines(self):
        """Test engine initialization"""
        orchestrator = MetaOrchestrator()
        
        assert "default" in orchestrator.engines
        assert "alpha" in orchestrator.engines
        assert "geo" in orchestrator.engines
        assert "product" in orchestrator.engines
        assert "safeguard" in orchestrator.engines
    
    def test_execute_with_default_engine(self):
        """Test execution with default engine"""
        orchestrator = MetaOrchestrator()
        embedding = np.random.randn(256).astype(np.float32)
        
        result = orchestrator.execute(embedding)
        
        assert result.primary_result.engine_name == "default"
        assert result.primary_result.success is True
        assert result.primary_result.signal is not None
        assert result.primary_result.execution_time > 0
        assert result.total_time > 0
    
    def test_execute_with_routing_context(self):
        """Test execution with routing context"""
        orchestrator = MetaOrchestrator()
        embedding = np.random.randn(256).astype(np.float32)
        context = RoutingContext(
            text="The company reported strong earnings with revenue growth."
        )
        
        result = orchestrator.execute(embedding, context=context)
        
        # Should route to alpha or default (if confidence too low)
        assert result.primary_result.engine_name in ["alpha", "default"]
        assert result.primary_result.success is True
        assert result.routing_decision is not None
    
    def test_execute_with_predefined_routing(self):
        """Test execution with predefined routing decision"""
        orchestrator = MetaOrchestrator()
        embedding = np.random.randn(256).astype(np.float32)
        decision = RoutingDecision(
            primary_engine="geo",
            confidence=0.9,
            reasoning="Test routing"
        )
        
        result = orchestrator.execute(embedding, routing_decision=decision)
        
        assert result.primary_result.engine_name == "geo"
        assert result.primary_result.success is True
        assert result.routing_decision.primary_engine == "geo"
    
    def test_execute_all_engine_variants(self):
        """Test execution with all engine variants"""
        orchestrator = MetaOrchestrator()
        embedding = np.random.randn(256).astype(np.float32)
        
        for engine_name in ["default", "alpha", "geo", "product", "safeguard"]:
            decision = RoutingDecision(
                primary_engine=engine_name,
                confidence=1.0
            )
            
            result = orchestrator.execute(embedding, routing_decision=decision)
            
            assert result.primary_result.engine_name == engine_name
            assert result.primary_result.success is True
            assert result.primary_result.signal is not None
    
    def test_execute_with_tw_window(self):
        """Test execution with TW window"""
        orchestrator = MetaOrchestrator()
        embedding = np.random.randn(256).astype(np.float32)
        tw_window = np.random.randn(10, 5).astype(np.float32)
        
        result = orchestrator.execute(embedding, tw_window=tw_window)
        
        assert result.primary_result.success is True
        assert result.primary_result.signal is not None
    
    def test_execute_with_invalid_engine(self):
        """Test execution with invalid engine name"""
        orchestrator = MetaOrchestrator()
        embedding = np.random.randn(256).astype(np.float32)
        decision = RoutingDecision(
            primary_engine="nonexistent",
            confidence=1.0
        )
        
        result = orchestrator.execute(embedding, routing_decision=decision)
        
        # Primary result should be fallback (default) since invalid engine failed
        assert result.primary_result.engine_name == "default"
        assert result.primary_result.success is True
        # Routing decision should still show the original intent
        assert result.routing_decision.primary_engine == "nonexistent"
    
    def test_fallback_to_default(self):
        """Test fallback to default engine on failure"""
        config = OrchestrationConfig(fallback_to_default=True)
        orchestrator = MetaOrchestrator(config=config)
        embedding = np.random.randn(256).astype(np.float32)
        
        # Try invalid engine
        decision = RoutingDecision(
            primary_engine="invalid",
            confidence=1.0
        )
        
        result = orchestrator.execute(embedding, routing_decision=decision)
        
        # Should fallback to default
        assert result.primary_result.engine_name == "default"
        assert result.primary_result.success is True
    
    def test_no_fallback(self):
        """Test no fallback when disabled"""
        config = OrchestrationConfig(fallback_to_default=False)
        orchestrator = MetaOrchestrator(config=config)
        embedding = np.random.randn(256).astype(np.float32)
        
        decision = RoutingDecision(
            primary_engine="invalid",
            confidence=1.0
        )
        
        result = orchestrator.execute(embedding, routing_decision=decision)
        
        # Should not fallback
        assert result.primary_result.engine_name == "invalid"
        assert result.primary_result.success is False
    
    def test_execution_timing(self):
        """Test execution timing is recorded"""
        orchestrator = MetaOrchestrator()
        embedding = np.random.randn(256).astype(np.float32)
        
        result = orchestrator.execute(embedding)
        
        assert result.primary_result.execution_time > 0
        assert result.total_time > 0
        assert result.total_time >= result.primary_result.execution_time
    
    def test_secondary_engines_execution(self):
        """Test execution of secondary engines"""
        orchestrator = MetaOrchestrator()
        embedding = np.random.randn(256).astype(np.float32)
        
        decision = RoutingDecision(
            primary_engine="alpha",
            confidence=0.8,
            secondary_engines=["geo"]
        )
        
        result = orchestrator.execute(embedding, routing_decision=decision)
        
        assert result.primary_result.engine_name == "alpha"
        assert len(result.secondary_results) == 1
        assert result.secondary_results[0].engine_name == "geo"
        assert result.secondary_results[0].success is True


class TestEngineResult:
    """Test EngineResult dataclass"""
    
    def test_successful_result(self):
        """Test successful engine result"""
        from src.core.kaldra_master_engine import KaldraSignal
        import numpy as np
        
        signal = KaldraSignal(
            archetype_probs=np.ones(144) / 144,
            tw_trigger=False,
            tw_stats=None,
            epistemic=None
        )
        
        result = EngineResult(
            engine_name="alpha",
            signal=signal,
            execution_time=0.5,
            success=True
        )
        
        assert result.engine_name == "alpha"
        assert result.signal is not None
        assert result.execution_time == 0.5
        assert result.success is True
        assert result.error is None
    
    def test_failed_result(self):
        """Test failed engine result"""
        result = EngineResult(
            engine_name="alpha",
            signal=None,
            execution_time=0.1,
            success=False,
            error="Test error"
        )
        
        assert result.success is False
        assert result.error == "Test error"
        assert result.signal is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
