"""
Basic tests for API v3.1 presets endpoint.
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from kaldra_api.routers import v3_1_presets


def test_list_presets_returns_dict():
    """Test that list_presets returns a dictionary."""
    result = v3_1_presets.list_presets()
    
    assert isinstance(result, dict)
    assert "presets" in result
    assert isinstance(result["presets"], dict)


def test_list_presets_contains_all_four():
    """Test that all four default presets are returned."""
    result = v3_1_presets.list_presets()
    presets = result["presets"]
    
    assert "alpha" in presets
    assert "geo" in presets
    assert "safeguard" in presets
    assert "product" in presets


def test_preset_structure_valid():
    """Test that each preset has required fields."""
    result = v3_1_presets.list_presets()
    presets = result["presets"]
    
    for name, preset in presets.items():
        assert "name" in preset
        assert "description" in preset
        assert "mode" in preset
        assert "emphasis" in preset
        assert "thresholds" in preset
        assert "output_format" in preset
        assert preset["name"] == name


def test_alpha_preset_config():
    """Test alpha preset specific configuration."""
    result = v3_1_presets.list_presets()
    alpha = result["presets"]["alpha"]
    
    assert alpha["mode"] == "full"
    assert "kindra.layer1" in alpha["emphasis"]
    assert "risk" in alpha["thresholds"]
    assert alpha["output_format"] == "financial_brief"
