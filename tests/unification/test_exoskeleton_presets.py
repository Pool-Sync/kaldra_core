"""
Tests for Exoskeleton Presets System.
"""

import pytest
from src.unification.exoskeleton import PresetConfig, PresetManager


def test_presets_exist():
    """Test that all default presets exist and are valid."""
    mgr = PresetManager()
    
    for name in ["alpha", "geo", "safeguard", "product"]:
        assert mgr.has_preset(name), f"Preset {name} should exist"
        preset = mgr.get_preset(name)
        assert preset.name == name
        assert preset.mode in ["signal", "full", "story", "safety-first", "exploratory"]
        assert isinstance(preset.emphasis, list)
        assert isinstance(preset.thresholds, dict)
        assert isinstance(preset.metadata, dict)


def test_list_presets_returns_all():
    """Test that list_presets returns all default presets."""
    mgr = PresetManager()
    presets = mgr.list_presets()
    
    assert "alpha" in presets
    assert "geo" in presets
    assert "safeguard" in presets
    assert "product" in presets
    assert len(presets) >= 4


def test_preset_config_structure():
    """Test PresetConfig structure and required fields."""
    mgr = PresetManager()
    
    # Test alpha preset structure
    alpha = mgr.get_preset("alpha")
    assert alpha.name == "alpha"
    assert alpha.description is not None
    assert alpha.mode == "full"
    assert "kindra.layer1" in alpha.emphasis
    assert "risk" in alpha.thresholds
    assert "confidence_min" in alpha.thresholds
    assert alpha.output_format == "financial_brief"
    assert "domain" in alpha.metadata
    assert alpha.metadata["domain"] == "finance"


def test_get_preset_raises_for_invalid():
    """Test that get_preset raises KeyError for invalid preset."""
    mgr = PresetManager()
    
    with pytest.raises(KeyError, match="Preset not found"):
        mgr.get_preset("invalid_preset")


def test_preset_manager_with_custom_presets():
    """Test PresetManager with custom presets."""
    custom_preset = PresetConfig(
        name="custom",
        description="Custom test preset",
        mode="signal",
        emphasis=["test"],
        thresholds={"risk": 0.5},
    )
    
    mgr = PresetManager(extra_presets={"custom": custom_preset})
    
    assert mgr.has_preset("custom")
    assert mgr.has_preset("alpha")  # Default still exists
    
    retrieved = mgr.get_preset("custom")
    assert retrieved.name == "custom"
    assert retrieved.mode == "signal"


def test_preset_thresholds_are_valid():
    """Test that all preset thresholds are within valid ranges."""
    mgr = PresetManager()
    
    for name, preset in mgr.list_presets().items():
        # Thresholds should be between 0 and 1
        for threshold_name, value in preset.thresholds.items():
            assert 0.0 <= value <= 1.0, \
                f"Preset {name} threshold {threshold_name}={value} out of range [0, 1]"


def test_preset_emphasis_not_empty():
    """Test that all presets have at least one emphasis."""
    mgr = PresetManager()
    
    for name, preset in mgr.list_presets().items():
        assert len(preset.emphasis) > 0, \
            f"Preset {name} should have at least one emphasis"


def test_geo_preset_specifics():
    """Test geo preset specific configuration."""
    mgr = PresetManager()
    geo = mgr.get_preset("geo")
    
    assert geo.mode == "story"
    assert "kindra.tw_plane" in geo.emphasis
    assert "meta.aurelius" in geo.emphasis
    assert geo.metadata["domain"] == "geopolitics"


def test_safeguard_preset_specifics():
    """Test safeguard preset specific configuration."""
    mgr = PresetManager()
    safeguard = mgr.get_preset("safeguard")
    
    assert safeguard.mode == "safety-first"
    assert "safeguard" in safeguard.emphasis
    assert safeguard.thresholds["risk"] < 0.25  # Strict risk threshold
    assert safeguard.thresholds["confidence_min"] >= 0.70  # High confidence required


def test_product_preset_specifics():
    """Test product preset specific configuration."""
    mgr = PresetManager()
    product = mgr.get_preset("product")
    
    assert product.mode == "full"
    assert "kindra.layer2" in product.emphasis  # Brand messaging
    assert "meta.campbell" in product.emphasis  # Hero's Journey
    assert product.metadata["domain"] == "product"


def test_preset_manager_immutability():
    """Test that list_presets returns a copy, not reference."""
    mgr = PresetManager()
    
    presets1 = mgr.list_presets()
    presets2 = mgr.list_presets()
    
    # Modify one
    presets1["alpha"].name = "modified"
    
    # Other should be unchanged
    assert presets2["alpha"].name == "alpha"
