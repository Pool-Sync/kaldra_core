"""
Unit tests for Signal Adapter (KALDRA v3.0).
"""
import pytest
import sys
sys.path.insert(0, '/Users/niki/Desktop/kaldra_core')

from src.unification.states.unified_state import UnifiedContext, GlobalContext
from src.unification.adapters.signal_adapter import SignalAdapter


def test_signal_adapter_basic():
    """Test basic signal conversion."""
    context = UnifiedContext()
    
    signal = SignalAdapter.to_signal(context)
    
    assert 'version' in signal
    assert signal['version'] == "3.0"
    assert 'request_id' in signal
    assert 'timestamp' in signal
    assert 'mode' in signal


def test_signal_adapter_with_data():
    """Test signal conversion with data."""
    context = UnifiedContext()
    context.global_ctx.mode = "full"
    
    signal = SignalAdapter.to_signal(context)
    
    assert signal['mode'] == "full"
    assert 'summary' in signal


def test_compact_signal():
    """Test compact signal format."""
    context = UnifiedContext()
    
    signal = SignalAdapter.to_compact_signal(context)
    
    assert 'version' in signal
    assert 'request_id' in signal
    assert 'degraded' in signal


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
