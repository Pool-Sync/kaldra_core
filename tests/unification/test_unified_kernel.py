"""
Unit tests for UnifiedKernel (KALDRA v3.0).
"""
import pytest
import sys
sys.path.insert(0, '/Users/niki/Desktop/kaldra_core')

from src.unification.kernel import UnifiedKernel
from src.unification.states.unified_state import UnifiedContext


def test_kernel_initialization():
    """Test kernel initialization."""
    kernel = UnifiedKernel()
    assert kernel.loaded == True
    assert len(kernel.list_modules()) == 5


def test_kernel_module_loading():
    """Test module loading."""
    kernel = UnifiedKernel()
    
    # Check all expected modules are loaded
    modules = kernel.list_modules()
    assert 'embeddings' in modules
    assert 'archetypes' in modules
    assert 'bias' in modules
    assert 'tau' in modules
    assert 'safeguard' in modules


def test_kernel_run_basic():
    """Test basic kernel run."""
    kernel = UnifiedKernel()
    result = kernel.run("Test input", mode="full")
    
    assert isinstance(result, UnifiedContext)
    assert result.global_ctx.mode == "full"
    assert result.global_ctx.version == "3.0"


def test_kernel_run_modes():
    """Test different execution modes."""
    kernel = UnifiedKernel()
    
    modes = ["signal", "story", "full", "safety-first", "exploratory"]
    
    for mode in modes:
        result = kernel.run("Test", mode=mode)
        assert result.global_ctx.mode == mode


def test_kernel_invalid_mode():
    """Test invalid mode raises error."""
    kernel = UnifiedKernel()
    
    with pytest.raises(ValueError):
        kernel.run("Test", mode="invalid_mode")


def test_kernel_get_module():
    """Test getting specific modules."""
    kernel = UnifiedKernel()
    
    embeddings = kernel.get_module("embeddings")
    assert embeddings is not None
    
    archetypes = kernel.get_module("archetypes")
    assert archetypes is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
