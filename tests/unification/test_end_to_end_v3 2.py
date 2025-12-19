"""
End-to-end integration tests for KALDRA v3.0.
"""
import pytest
import sys
sys.path.insert(0, '/Users/niki/Desktop/kaldra_core')

from src.unification.adapters.unified_api import UnifiedKaldra


def test_e2e_basic_analysis():
    """Test basic end-to-end analysis."""
    kaldra = UnifiedKaldra()
    
    result = kaldra.analyze("Test input text")
    
    assert 'version' in result
    assert result['version'] == "3.0"
    assert 'request_id' in result
    assert 'mode' in result


def test_e2e_different_modes():
    """Test all execution modes."""
    kaldra = UnifiedKaldra()
    
    modes = ["signal", "story", "full", "safety-first", "exploratory"]
    
    for mode in modes:
        result = kaldra.analyze("Test", mode=mode)
        assert result['mode'] == mode


def test_e2e_batch_processing():
    """Test batch processing."""
    kaldra = UnifiedKaldra()
    
    texts = ["Text 1", "Text 2", "Text 3"]
    results = kaldra.analyze_batch(texts)
    
    assert len(results) == 3
    for result in results:
        assert 'version' in result


def test_e2e_signal_structure():
    """Test signal structure completeness."""
    kaldra = UnifiedKaldra()
    
    result = kaldra.analyze("Complete test", mode="full")
    
    # Check all expected top-level keys
    expected_keys = ['version', 'request_id', 'timestamp', 'mode', 'summary']
    for key in expected_keys:
        assert key in result


def test_e2e_degraded_mode():
    """Test graceful degradation."""
    kaldra = UnifiedKaldra()
    
    # Even with failures, should return valid signal
    result = kaldra.analyze("Test")
    
    assert 'summary' in result
    assert 'degraded' in result['summary']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
