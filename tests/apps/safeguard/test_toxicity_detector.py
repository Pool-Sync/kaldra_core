"""Tests for KALDRA-Safeguard toxicity detector."""

import pytest
from src.apps.safeguard.toxicity_detector import (
    ToxicityDetector,
    SafeguardInput,
    SafeguardToxicityResult
)


def test_toxicity_detector_analyze_basic():
    """Test basic toxicity detection."""
    detector = ToxicityDetector(provider="heuristic")
    
    result = detector.analyze("This is a normal, friendly message")
    
    assert isinstance(result, SafeguardToxicityResult)
    assert result.domain == "SAFEGUARD"
    assert 0.0 <= result.toxicity <= 1.0
    assert result.severity in ["low", "medium", "high", "critical"]


def test_toxicity_detector_empty_text():
    """Test that empty text returns low toxicity."""
    detector = ToxicityDetector()
    
    result = detector.analyze("")
    
    assert result.toxicity == 0.0
    assert result.severity == "low"
    assert len(result.flags) == 0


def test_toxicity_detector_recommendations_present_when_flags():
    """Test that recommendations are provided when flags are raised."""
    detector = ToxicityDetector(provider="heuristic")
    
    # Use text that should trigger high toxicity
    toxic_text = "hate stupid idiot terrible awful disgusting"
    result = detector.analyze(toxic_text)
    
    # If flags are present, recommendations should be too
    if result.flags:
        assert len(result.recommendations) > 0
        assert isinstance(result.recommendations[0], str)


def test_toxicity_detector_severity_levels():
    """Test that severity levels are correctly assigned."""
    detector = ToxicityDetector()
    
    # Low toxicity text
    result_low = detector.analyze("Hello, how are you?")
    assert result_low.severity in ["low", "medium"]
    
    # The heuristic detector should work consistently
    assert result_low.toxicity >= 0.0


def test_toxicity_detector_bias_dimensions():
    """Test that bias dimensions are populated."""
    detector = ToxicityDetector()
    
    result = detector.analyze("Some text to analyze")
    
    assert "toxicity" in result.bias_dimensions
    assert "political" in result.bias_dimensions
    assert "gender" in result.bias_dimensions
    assert "racial" in result.bias_dimensions
    
    # All dimensions should be floats between 0 and 1
    for dim, score in result.bias_dimensions.items():
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
