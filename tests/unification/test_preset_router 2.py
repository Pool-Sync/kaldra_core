"""
Tests for PresetRouter Integration.
"""

import pytest
import tempfile
from src.unification.exoskeleton import (
    PresetRouter,
    PresetResolvedConfig,
    PresetManager,
    ProfileManager,
)


def test_resolve_preset_basic():
    """Test basic preset resolution without profile."""
    router = PresetRouter()
    cfg = router.resolve_preset("alpha")
    
    assert cfg.name == "alpha"
    assert cfg.mode == "full"
    assert "kindra.layer1" in cfg.emphasis
    assert "meta.nietzsche" in cfg.emphasis
    assert cfg.thresholds["risk"] == 0.30
    assert cfg.thresholds["confidence_min"] == 0.60
    assert cfg.output_format == "financial_brief"


def test_resolve_all_presets():
    """Test that all default presets can be resolved."""
    router = PresetRouter()
    
    for preset_name in ["alpha", "geo", "safeguard", "product"]:
        cfg = router.resolve_preset(preset_name)
        assert cfg.name == preset_name
        assert isinstance(cfg.emphasis, dict)
        assert isinstance(cfg.thresholds, dict)


def test_resolve_nonexistent_preset():
    """Test that resolving invalid preset raises KeyError."""
    router = PresetRouter()
    
    with pytest.raises(KeyError):
        router.resolve_preset("invalid_preset")


def test_profile_overrides_risk_tolerance(tmp_path):
    """Test that user profile overrides risk threshold."""
    storage = tmp_path / "profiles"
    pm = ProfileManager(storage_dir=str(storage))
    pm.create_profile("user_1", {"risk_tolerance": 0.9})
    
    router = PresetRouter(profile_manager=pm)
    cfg = router.resolve_preset("geo", user_id="user_1")
    
    assert cfg.thresholds["risk"] == 0.9


def test_profile_overrides_output_format(tmp_path):
    """Test that user profile overrides output format."""
    storage = tmp_path / "profiles"
    pm = ProfileManager(storage_dir=str(storage))
    pm.create_profile("user_1", {"output_format": "custom_brief"})
    
    router = PresetRouter(profile_manager=pm)
    cfg = router.resolve_preset("alpha", user_id="user_1")
    
    assert cfg.output_format == "custom_brief"


def test_profile_adds_metadata(tmp_path):
    """Test that profile adds depth and user_id to metadata."""
    storage = tmp_path / "profiles"
    pm = ProfileManager(storage_dir=str(storage))
    pm.create_profile("user_1", {"depth": "exploratory"})
    
    router = PresetRouter(profile_manager=pm)
    cfg = router.resolve_preset("product", user_id="user_1")
    
    assert cfg.metadata["depth"] == "exploratory"
    assert cfg.metadata["user_id"] == "user_1"


def test_profile_custom_preferences_in_metadata(tmp_path):
    """Test that custom preferences are added to metadata."""
    storage = tmp_path / "profiles"
    pm = ProfileManager(storage_dir=str(storage))
    pm.create_profile("user_1")
    pm.update_profile("user_1", {
        "custom_field": "value",
        "favorite_domains": ["finance", "geo"]
    })
    
    router = PresetRouter(profile_manager=pm)
    cfg = router.resolve_preset("alpha", user_id="user_1")
    
    assert "user_preferences" in cfg.metadata
    assert cfg.metadata["user_preferences"]["custom_field"] == "value"


def test_resolve_without_profile():
    """Test resolution when user_id is None."""
    router = PresetRouter()
    cfg = router.resolve_preset("alpha", user_id=None)
    
    assert cfg.name == "alpha"
    assert "user_id" not in cfg.metadata


def test_resolve_with_nonexistent_profile():
    """Test resolution when profile doesn't exist (should use preset only)."""
    router = PresetRouter()
    cfg = router.resolve_preset("geo", user_id="nonexistent_user")
    
    # Should still work, just without profile overrides
    assert cfg.name == "geo"
    assert cfg.thresholds["risk"] == 0.40  # Original preset value


def test_emphasis_converted_to_dict():
    """Test that emphasis list is converted to weighted dict."""
    router = PresetRouter()
    cfg = router.resolve_preset("alpha")
    
    assert isinstance(cfg.emphasis, dict)
    # All emphasis items should have weight 1.0 by default
    for key, weight in cfg.emphasis.items():
        assert weight == 1.0


def test_get_default_config():
    """Test getting default configuration."""
    router = PresetRouter()
    cfg = router.get_default_config()
    
    assert cfg.name == "alpha"
    assert cfg.mode == "full"


def test_preset_resolved_config_structure():
    """Test PresetResolvedConfig dataclass structure."""
    cfg = PresetResolvedConfig(
        name="test",
        mode="full",
        emphasis={"stage1": 1.0},
        thresholds={"risk": 0.5},
        output_format="json",
        metadata={"key": "value"}
    )
    
    assert cfg.name == "test"
    assert cfg.mode == "full"
    assert cfg.emphasis["stage1"] == 1.0
    assert cfg.thresholds["risk"] == 0.5
    assert cfg.output_format == "json"
    assert cfg.metadata["key"] == "value"


def test_multiple_profile_overrides(tmp_path):
    """Test multiple profile settings override preset."""
    storage = tmp_path / "profiles"
    pm = ProfileManager(storage_dir=str(storage))
    pm.create_profile("power_user", {
        "risk_tolerance": 0.8,
        "output_format": "detailed_report",
        "depth": "deep"
    })
    
    router = PresetRouter(profile_manager=pm)
    cfg = router.resolve_preset("safeguard", user_id="power_user")
    
    assert cfg.thresholds["risk"] == 0.8
    assert cfg.output_format == "detailed_report"
    assert cfg.metadata["depth"] == "deep"
    assert cfg.metadata["user_id"] == "power_user"


def test_geo_preset_specifics():
    """Test geo preset specific configuration."""
    router = PresetRouter()
    cfg = router.resolve_preset("geo")
    
    assert cfg.mode == "story"
    assert "kindra.tw_plane" in cfg.emphasis
    assert "meta.aurelius" in cfg.emphasis


def test_safeguard_preset_specifics():
    """Test safeguard preset specific configuration."""
    router = PresetRouter()
    cfg = router.resolve_preset("safeguard")
    
    assert cfg.mode == "safety-first"
    assert "safeguard" in cfg.emphasis
    assert cfg.thresholds["risk"] == 0.20  # Strict
    assert cfg.thresholds["confidence_min"] == 0.70  # High
