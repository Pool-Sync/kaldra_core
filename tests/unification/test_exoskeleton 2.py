"""
Exoskeleton Layer Integration Tests.

Comprehensive test suite covering:
- PresetManager (presets)
- ProfileManager (profiles)
- PresetRouter (preset + profile resolution)
- Integration between all components
"""

import os
import json
import pytest

from src.unification.exoskeleton import (
    PresetManager,
    PresetConfig,
    ProfileManager,
    UserProfile,
    PresetRouter,
    PresetResolvedConfig,
)


# ============================================================================
# PRESET LOADING TESTS
# ============================================================================

def test_preset_loading_default_presets_exist():
    """Test that all default presets exist and are valid."""
    mgr = PresetManager()
    presets = mgr.list_presets()
    
    # 4 fundamental presets
    for name in ["alpha", "geo", "safeguard", "product"]:
        assert name in presets
        preset = presets[name]
        assert isinstance(preset, PresetConfig)
        assert preset.name == name
        assert preset.mode in ["signal", "full", "story", "safety-first", "exploratory"]
        assert isinstance(preset.emphasis, list)
        assert isinstance(preset.thresholds, dict)


def test_preset_loading_structure_consistency():
    """Test that all presets have consistent structure."""
    mgr = PresetManager()
    presets = mgr.list_presets()
    
    for name, preset in presets.items():
        # All presets must have these fields
        assert preset.name
        assert preset.description
        assert preset.mode
        assert len(preset.emphasis) > 0
        assert "risk" in preset.thresholds
        assert preset.output_format
        assert isinstance(preset.metadata, dict)


# ============================================================================
# PROFILE MANAGEMENT TESTS
# ============================================================================

def test_profile_creation_and_retrieval(tmp_path):
    """Test profile creation and retrieval flow."""
    storage = tmp_path / "profiles"
    mgr = ProfileManager(storage_dir=str(storage))
    
    mgr.create_profile("user_123", {
        "preferred_preset": "geo",
        "risk_tolerance": 0.8
    })
    profile = mgr.get_profile("user_123")
    
    assert isinstance(profile, UserProfile)
    assert profile.user_id == "user_123"
    assert profile.preferred_preset == "geo"
    assert profile.risk_tolerance == 0.8


def test_profile_update(tmp_path):
    """Test profile update functionality."""
    storage = tmp_path / "profiles"
    mgr = ProfileManager(storage_dir=str(storage))
    
    mgr.create_profile("user_123")
    mgr.update_profile("user_123", {
        "risk_tolerance": 0.9,
        "output_format": "markdown"
    })
    
    profile = mgr.get_profile("user_123")
    assert profile.risk_tolerance == 0.9
    assert profile.output_format == "markdown"


def test_profile_persistence_across_managers(tmp_path):
    """Test that profiles persist across ProfileManager instances."""
    storage = tmp_path / "profiles"
    
    # Create with first manager
    mgr1 = ProfileManager(storage_dir=str(storage))
    mgr1.create_profile("user_persist", {"risk_tolerance": 0.85})
    
    # Retrieve with second manager
    mgr2 = ProfileManager(storage_dir=str(storage))
    profile = mgr2.get_profile("user_persist")
    
    assert profile is not None
    assert profile.risk_tolerance == 0.85


# ============================================================================
# PRESET ROUTER BASIC TESTS
# ============================================================================

def test_preset_router_resolve_preset_without_profile():
    """Test basic preset resolution without profile override."""
    router = PresetRouter()
    resolved = router.resolve_preset("alpha")
    
    assert isinstance(resolved, PresetResolvedConfig)
    assert resolved.name == "alpha"
    assert resolved.mode == "full"
    assert "risk" in resolved.thresholds
    assert isinstance(resolved.emphasis, dict)
    assert len(resolved.emphasis) > 0


def test_preset_router_all_presets_resolvable():
    """Test that all default presets can be resolved."""
    router = PresetRouter()
    
    for preset_name in ["alpha", "geo", "safeguard", "product"]:
        resolved = router.resolve_preset(preset_name)
        assert resolved.name == preset_name
        assert isinstance(resolved, PresetResolvedConfig)


# ============================================================================
# PRESET + PROFILE MERGING TESTS
# ============================================================================

def test_preset_router_merges_profile_risk_and_output(tmp_path):
    """Test that profile overrides preset risk and output format."""
    storage = tmp_path / "profiles"
    profile_mgr = ProfileManager(storage_dir=str(storage))
    profile_mgr.create_profile(
        "user_1",
        {"risk_tolerance": 0.95, "output_format": "markdown"}
    )
    
    preset_router = PresetRouter(profile_manager=profile_mgr)
    resolved = preset_router.resolve_preset("geo", user_id="user_1")
    
    # Risk from profile
    assert resolved.thresholds["risk"] == 0.95
    # Output format overridden by profile
    assert resolved.output_format == "markdown"
    # Depth in metadata
    assert "depth" in resolved.metadata


def test_preset_router_profile_depth_in_metadata(tmp_path):
    """Test that profile depth is added to metadata."""
    storage = tmp_path / "profiles"
    profile_mgr = ProfileManager(storage_dir=str(storage))
    profile_mgr.create_profile("user_deep", {"depth": "exploratory"})
    
    preset_router = PresetRouter(profile_manager=profile_mgr)
    resolved = preset_router.resolve_preset("alpha", user_id="user_deep")
    
    assert resolved.metadata["depth"] == "exploratory"
    assert resolved.metadata["user_id"] == "user_deep"


def test_preset_router_custom_preferences_merged(tmp_path):
    """Test that custom profile preferences are merged into metadata."""
    storage = tmp_path / "profiles"
    profile_mgr = ProfileManager(storage_dir=str(storage))
    profile_mgr.create_profile("user_custom")
    profile_mgr.update_profile("user_custom", {
        "custom_field": "custom_value",
        "favorite_domains": ["finance", "geo"]
    })
    
    preset_router = PresetRouter(profile_manager=profile_mgr)
    resolved = preset_router.resolve_preset("product", user_id="user_custom")
    
    assert "user_preferences" in resolved.metadata
    assert resolved.metadata["user_preferences"]["custom_field"] == "custom_value"


# ============================================================================
# INTEGRATION SCENARIOS
# ============================================================================

def test_full_flow_preset_to_profile_to_resolution(tmp_path):
    """Test complete flow: load preset → create profile → resolve."""
    storage = tmp_path / "profiles"
    
    # 1. Verify preset exists
    preset_mgr = PresetManager()
    alpha_preset = preset_mgr.get_preset("alpha")
    assert alpha_preset.name == "alpha"
    
    # 2. Create user profile
    profile_mgr = ProfileManager(storage_dir=str(storage))
    profile_mgr.create_profile("analyst_001", {
        "preferred_preset": "alpha",
        "risk_tolerance": 0.75,
        "depth": "deep"
    })
    
    # 3. Resolve with router
    router = PresetRouter(
        preset_manager=preset_mgr,
        profile_manager=profile_mgr
    )
    resolved = router.resolve_preset("alpha", user_id="analyst_001")
    
    # 4. Verify merged config
    assert resolved.name == "alpha"
    assert resolved.thresholds["risk"] == 0.75  # From profile
    assert resolved.metadata["depth"] == "deep"  # From profile
    assert resolved.mode == "full"  # From preset


def test_different_users_different_configs(tmp_path):
    """Test that different users get different resolved configs."""
    storage = tmp_path / "profiles"
    profile_mgr = ProfileManager(storage_dir=str(storage))
    
    # User 1: Conservative
    profile_mgr.create_profile("conservative", {"risk_tolerance": 0.2})
    
    # User 2: Aggressive
    profile_mgr.create_profile("aggressive", {"risk_tolerance": 0.9})
    
    router = PresetRouter(profile_manager=profile_mgr)
    
    config_conservative = router.resolve_preset("alpha", user_id="conservative")
    config_aggressive = router.resolve_preset("alpha", user_id="aggressive")
    
    assert config_conservative.thresholds["risk"] == 0.2
    assert config_aggressive.thresholds["risk"] == 0.9


def test_preset_switch_maintains_profile(tmp_path):
    """Test that switching presets maintains profile overrides."""
    storage = tmp_path / "profiles"
    profile_mgr = ProfileManager(storage_dir=str(storage))
    profile_mgr.create_profile("switcher", {
        "risk_tolerance": 0.6,
        "output_format": "detailed"
    })
    
    router = PresetRouter(profile_manager=profile_mgr)
    
    # Try different presets with same profile
    for preset_name in ["alpha", "geo", "product"]:
        resolved = router.resolve_preset(preset_name, user_id="switcher")
        assert resolved.thresholds["risk"] == 0.6
        assert resolved.output_format == "detailed"


# ============================================================================
# EDGE CASES AND VALIDATION
# ============================================================================

def test_nonexistent_preset_raises_error():
    """Test that requesting invalid preset raises KeyError."""
    router = PresetRouter()
    
    with pytest.raises(KeyError):
        router.resolve_preset("invalid_preset_name")


def test_nonexistent_profile_uses_preset_only():
    """Test that nonexistent profile falls back to preset-only config."""
    router = PresetRouter()
    resolved = router.resolve_preset("geo", user_id="nonexistent_user")
    
    # Should use original preset values
    assert resolved.name == "geo"
    assert resolved.thresholds["risk"] == 0.40  # Original geo preset value
    assert "user_id" not in resolved.metadata


def test_emphasis_list_converted_to_weighted_dict():
    """Test that emphasis list is properly converted to weighted dict."""
    router = PresetRouter()
    resolved = router.resolve_preset("alpha")
    
    assert isinstance(resolved.emphasis, dict)
    # All items should have default weight 1.0
    for key, weight in resolved.emphasis.items():
        assert weight == 1.0
    
    # Verify expected emphasis items from alpha preset
    assert "kindra.layer1" in resolved.emphasis
    assert "meta.nietzsche" in resolved.emphasis


def test_get_default_config():
    """Test getting default configuration (alpha preset)."""
    router = PresetRouter()
    config = router.get_default_config()
    
    assert config.name == "alpha"
    assert config.mode == "full"
    assert isinstance(config, PresetResolvedConfig)
