"""
User Profiles System for Exoskeleton Layer.

Provides persistent user preferences for KALDRA analysis modes.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import json
import os


@dataclass
class UserProfile:
    """
    Persistent user profile for KALDRA.
    Defines preferences that influence presets, output, and thresholds.

    Attributes:
        user_id: Unique user identifier
        preferred_preset: Default preset to use
        risk_tolerance: Risk acceptance level [0, 1]
        output_format: Preferred output format
        depth: Analysis depth mode
        preferences: Additional custom preferences
    """

    user_id: str
    preferred_preset: str = "alpha"
    risk_tolerance: float = 0.5  # [0, 1]
    output_format: str = "json"
    depth: str = "standard"  # "fast" | "standard" | "deep" | "exploratory"
    preferences: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> Dict[str, Any]:
        """Serialize profile to JSON-compatible dict."""
        return {
            "user_id": self.user_id,
            "preferred_preset": self.preferred_preset,
            "risk_tolerance": self.risk_tolerance,
            "output_format": self.output_format,
            "depth": self.depth,
            "preferences": self.preferences,
        }

    @staticmethod
    def from_json(data: Dict[str, Any]) -> "UserProfile":
        """Deserialize profile from JSON-compatible dict."""
        return UserProfile(
            user_id=data["user_id"],
            preferred_preset=data.get("preferred_preset", "alpha"),
            risk_tolerance=data.get("risk_tolerance", 0.5),
            output_format=data.get("output_format", "json"),
            depth=data.get("depth", "standard"),
            preferences=data.get("preferences", {}),
        )


class ProfileManager:
    """
    Manages persistent user profiles.
    
    Saves profiles as JSON files in a local directory.
    Can be replaced with database backend in future versions.
    """

    def __init__(self, storage_dir: str = "kaldra_profiles"):
        """
        Initialize ProfileManager.

        Args:
            storage_dir: Directory path for storing profile JSON files
        """
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def _path(self, user_id: str) -> str:
        """Get file path for a user's profile."""
        return os.path.join(self.storage_dir, f"{user_id}.json")

    def create_profile(
        self, user_id: str, preferences: Optional[Dict[str, Any]] = None
    ) -> UserProfile:
        """
        Create a new user profile.

        Args:
            user_id: Unique user identifier
            preferences: Optional initial preferences dict

        Returns:
            Created UserProfile
        """
        profile = UserProfile(user_id=user_id)

        if preferences:
            for k, v in preferences.items():
                if hasattr(profile, k):
                    setattr(profile, k, v)
                else:
                    profile.preferences[k] = v

        self.save_profile(profile)
        return profile

    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        Retrieve an existing user profile.

        Args:
            user_id: Unique user identifier

        Returns:
            UserProfile if exists, None otherwise
        """
        path = self._path(user_id)
        if not os.path.exists(path):
            return None

        with open(path, "r") as f:
            data = json.load(f)
        return UserProfile.from_json(data)

    def update_profile(self, user_id: str, preferences: Dict[str, Any]) -> UserProfile:
        """
        Update an existing profile or create if doesn't exist.

        Args:
            user_id: Unique user identifier
            preferences: Preferences dict to update

        Returns:
            Updated UserProfile
        """
        profile = self.get_profile(user_id)
        if profile is None:
            profile = UserProfile(user_id=user_id)

        for k, v in preferences.items():
            if hasattr(profile, k):
                setattr(profile, k, v)
            else:
                profile.preferences[k] = v

        self.save_profile(profile)
        return profile

    def save_profile(self, profile: UserProfile):
        """
        Save a profile to disk.

        Args:
            profile: UserProfile to save
        """
        path = self._path(profile.user_id)
        with open(path, "w") as f:
            json.dump(profile.to_json(), f, indent=4)

    def delete_profile(self, user_id: str) -> bool:
        """
        Delete a user profile.

        Args:
            user_id: Unique user identifier

        Returns:
            True if profile was deleted, False if didn't exist
        """
        path = self._path(user_id)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def list_profiles(self) -> list[str]:
        """
        List all user IDs with profiles.

        Returns:
            List of user IDs
        """
        if not os.path.exists(self.storage_dir):
            return []
        
        files = os.listdir(self.storage_dir)
        return [f.replace(".json", "") for f in files if f.endswith(".json")]
