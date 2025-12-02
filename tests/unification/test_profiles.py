"""
Tests for Exoskeleton Profiles System.
"""

import pytest
import os
import json
from src.unification.exoskeleton import UserProfile, ProfileManager


def test_user_profile_creation():
    """Test UserProfile dataclass creation with defaults."""
    profile = UserProfile(user_id="user_123")
    
    assert profile.user_id == "user_123"
    assert profile.preferred_preset == "alpha"
    assert profile.risk_tolerance == 0.5
    assert profile.output_format == "json"
    assert profile.depth == "standard"
    assert isinstance(profile.preferences, dict)


def test_user_profile_serialization():
    """Test UserProfile to_json and from_json."""
    original = UserProfile(
        user_id="user_123",
        preferred_preset="geo",
        risk_tolerance=0.7,
        output_format="brief",
        depth="deep",
        preferences={"custom_field": "value"}
    )
    
    # Serialize
    data = original.to_json()
    assert data["user_id"] == "user_123"
    assert data["preferred_preset"] == "geo"
    assert data["risk_tolerance"] == 0.7
    
    # Deserialize
    restored = UserProfile.from_json(data)
    assert restored.user_id == original.user_id
    assert restored.preferred_preset == original.preferred_preset
    assert restored.risk_tolerance == original.risk_tolerance
    assert restored.preferences == original.preferences


def test_create_and_get_profile(tmp_path):
    """Test creating and retrieving a profile."""
    storage = tmp_path / "profiles"
    mgr = ProfileManager(storage_dir=str(storage))
    
    # Create profile
    created = mgr.create_profile("user_1", {"preferred_preset": "geo"})
    assert created.user_id == "user_1"
    assert created.preferred_preset == "geo"
    
    # Retrieve profile
    retrieved = mgr.get_profile("user_1")
    assert retrieved is not None
    assert retrieved.user_id == "user_1"
    assert retrieved.preferred_preset == "geo"
    
    # Verify file exists
    assert os.path.exists(str(storage / "user_1.json"))


def test_get_nonexistent_profile(tmp_path):
    """Test getting a profile that doesn't exist."""
    storage = tmp_path / "profiles"
    mgr = ProfileManager(storage_dir=str(storage))
    
    profile = mgr.get_profile("nonexistent")
    assert profile is None


def test_update_profile(tmp_path):
    """Test updating an existing profile."""
    storage = tmp_path / "profiles"
    mgr = ProfileManager(storage_dir=str(storage))
    
    # Create profile
    mgr.create_profile("user_1")
    
    # Update
    updated = mgr.update_profile("user_1", {
        "risk_tolerance": 0.9,
        "depth": "exploratory"
    })
    
    assert updated.risk_tolerance == 0.9
    assert updated.depth == "exploratory"
    
    # Verify persisted
    retrieved = mgr.get_profile("user_1")
    assert retrieved.risk_tolerance == 0.9
    assert retrieved.depth == "exploratory"


def test_update_creates_if_not_exists(tmp_path):
    """Test that update creates profile if it doesn't exist."""
    storage = tmp_path / "profiles"
    mgr = ProfileManager(storage_dir=str(storage))
    
    updated = mgr.update_profile("new_user", {"preferred_preset": "product"})
    assert updated.user_id == "new_user"
    assert updated.preferred_preset == "product"
    
    # Verify persisted
    retrieved = mgr.get_profile("new_user")
    assert retrieved is not None


def test_update_custom_preferences(tmp_path):
    """Test updating custom preferences not in standard fields."""
    storage = tmp_path / "profiles"
    mgr = ProfileManager(storage_dir=str(storage))
    
    mgr.create_profile("user_1")
    mgr.update_profile("user_1", {
        "custom_field": "custom_value",
        "another_field": 42
    })
    
    profile = mgr.get_profile("user_1")
    assert profile.preferences["custom_field"] == "custom_value"
    assert profile.preferences["another_field"] == 42


def test_delete_profile(tmp_path):
    """Test deleting a profile."""
    storage = tmp_path / "profiles"
    mgr = ProfileManager(storage_dir=str(storage))
    
    # Create profile
    mgr.create_profile("user_1")
    assert mgr.get_profile("user_1") is not None
    
    # Delete
    result = mgr.delete_profile("user_1")
    assert result is True
    assert mgr.get_profile("user_1") is None
    
    # Delete non-existent
    result = mgr.delete_profile("user_1")
    assert result is False


def test_list_profiles(tmp_path):
    """Test listing all profiles."""
    storage = tmp_path / "profiles"
    mgr = ProfileManager(storage_dir=str(storage))
    
    # Create multiple profiles
    mgr.create_profile("user_1")
    mgr.create_profile("user_2")
    mgr.create_profile("user_3")
    
    profiles = mgr.list_profiles()
    assert len(profiles) == 3
    assert "user_1" in profiles
    assert "user_2" in profiles
    assert "user_3" in profiles


def test_profile_persistence(tmp_path):
    """Test that profiles persist across ProfileManager instances."""
    storage = tmp_path / "profiles"
    
    # Create profile with first manager
    mgr1 = ProfileManager(storage_dir=str(storage))
    mgr1.create_profile("user_persist", {"risk_tolerance": 0.8})
    
    # Retrieve with second manager
    mgr2 = ProfileManager(storage_dir=str(storage))
    profile = mgr2.get_profile("user_persist")
    
    assert profile is not None
    assert profile.risk_tolerance == 0.8


def test_risk_tolerance_range_validation():
    """Test that risk_tolerance accepts valid range."""
    profile = UserProfile(user_id="test", risk_tolerance=0.0)
    assert profile.risk_tolerance == 0.0
    
    profile = UserProfile(user_id="test", risk_tolerance=1.0)
    assert profile.risk_tolerance == 1.0
    
    profile = UserProfile(user_id="test", risk_tolerance=0.5)
    assert profile.risk_tolerance == 0.5


def test_depth_options():
    """Test that depth field accepts valid options."""
    for depth in ["fast", "standard", "deep", "exploratory"]:
        profile = UserProfile(user_id="test", depth=depth)
        assert profile.depth == depth


def test_multiple_preferences_update(tmp_path):
    """Test updating multiple preferences at once."""
    storage = tmp_path / "profiles"
    mgr = ProfileManager(storage_dir=str(storage))
    
    mgr.create_profile("user_1")
    mgr.update_profile("user_1", {
        "preferred_preset": "safeguard",
        "risk_tolerance": 0.2,
        "output_format": "safety_report",
        "depth": "deep"
    })
    
    profile = mgr.get_profile("user_1")
    assert profile.preferred_preset == "safeguard"
    assert profile.risk_tolerance == 0.2
    assert profile.output_format == "safety_report"
    assert profile.depth == "deep"
