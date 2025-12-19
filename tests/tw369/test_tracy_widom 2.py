"""
Tests for Tracy-Widom module.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from tw369.tracy_widom import (
    tw_cdf,
    severity_from_index,
    load_tw_parameters,
    load_tw_lookup
)


def test_severity_monotonic():
    """Test that severity increases with instability_index."""
    # Use heuristic mode for predictable behavior
    params = {"enabled": False}
    
    sev1 = severity_from_index(0.1, params=params)
    sev2 = severity_from_index(0.5, params=params)
    sev3 = severity_from_index(1.0, params=params)
    
    assert sev1 < sev2 < sev3, "Severity should increase with instability_index"


def test_fallback_when_disabled():
    """Test that disabled mode uses heuristic fallback."""
    params = {"enabled": False}
    
    # Should use tanh-based heuristic
    sev = severity_from_index(1.0, params=params)
    
    # Verify it's in valid range
    assert 0.0 <= sev <= 1.0
    
    # Should be a reasonable high value for index=1.0
    # v2.4 uses _heuristic_cdf which clamps to [0,1]
    assert sev > 0.8, "Severity should be high for instability_index=1.0"


def test_lookup_respected():
    """Test that lookup table is used when enabled."""
    params = {"enabled": True, "beta": 2, "use_lookup": True, "severity_scale": 1.0}
    lookup = load_tw_lookup()
    
    # Test with a value in the lookup range
    sev = severity_from_index(0.5, params=params, lookup=lookup)
    
    # Should be in valid range
    assert 0.0 <= sev <= 1.0


def test_tw_cdf_interpolation():
    """Test that TW CDF interpolates correctly."""
    lookup = load_tw_lookup()
    
    # Test exact points from lookup
    cdf_at_0 = tw_cdf(0.0, beta=2, lookup=lookup)
    assert 0.4 < cdf_at_0 < 0.6, "CDF at 0 should be around 0.5"
    
    # Test interpolation
    cdf_at_1 = tw_cdf(1.0, beta=2, lookup=lookup)
    cdf_at_2 = tw_cdf(2.0, beta=2, lookup=lookup)
    
    assert cdf_at_1 < cdf_at_2, "CDF should be monotonic"


def test_severity_bounds():
    """Test that severity is always in [0, 1]."""
    params_disabled = {"enabled": False}
    params_enabled = {"enabled": True, "use_lookup": True}
    
    test_indices = [-2.0, -1.0, 0.0, 0.5, 1.0, 2.0, 5.0]
    
    for idx in test_indices:
        sev_disabled = severity_from_index(idx, params=params_disabled)
        sev_enabled = severity_from_index(idx, params=params_enabled)
        
        assert 0.0 <= sev_disabled <= 1.0, f"Severity out of bounds for index {idx} (disabled)"
        assert 0.0 <= sev_enabled <= 1.0, f"Severity out of bounds for index {idx} (enabled)"
