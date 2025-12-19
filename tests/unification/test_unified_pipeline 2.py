"""
Unit tests for Pipeline Stages (KALDRA v3.0).
"""
import pytest
import sys
sys.path.insert(0, '/Users/niki/Desktop/kaldra_core')

from src.unification.registry import ModuleRegistry
from src.unification.kernel import UnifiedKernel
from src.unification.states.unified_state import UnifiedContext, InputContext
from src.unification.pipeline.input_stage import InputStage
from src.unification.pipeline.core_stage import CoreStage
from src.unification.pipeline.output_stage import OutputStage


def test_input_stage():
    """Test input stage execution."""
    kernel = UnifiedKernel()
    stage = InputStage(kernel.registry)
    
    context = UnifiedContext()
    context.input_ctx = InputContext(text="Test input")
    
    result = stage.execute(context)
    
    assert result.input_ctx is not None
    # Note: May be degraded due to circuit breaker
    assert result.input_ctx.text == "Test input"


def test_core_stage():
    """Test core stage execution."""
    kernel = UnifiedKernel()
    stage = CoreStage(kernel.registry)
    
    context = UnifiedContext()
    # Core stage needs embedding from input stage
    # Will skip if no embedding available
    
    result = stage.execute(context)
    
    # Should handle gracefully even without input
    assert result is not None


def test_output_stage():
    """Test output stage execution."""
    kernel = UnifiedKernel()
    stage = OutputStage(kernel.registry)
    
    context = UnifiedContext()
    
    result = stage.execute(context)
    
    assert result is not None
    assert hasattr(result.global_ctx, 'summary') or result.global_ctx.__dict__.get('summary')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
