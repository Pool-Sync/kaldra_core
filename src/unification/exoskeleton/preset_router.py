"""
Preset Router for Exoskeleton Layer.

Resolves (preset + user profile) into executable pipeline configuration.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from .presets import PresetManager, PresetConfig
from .profiles import ProfileManager, UserProfile


@dataclass
class PresetResolvedConfig:
    """
    Represents preset merged with user preferences, ready for pipeline execution.

    This is the final configuration after resolving:
    - Base preset configuration
    - User profile overrides
    - Merged thresholds and emphasis weights

    Attributes:
        name: Preset identifier
        mode: Execution mode
        emphasis: Stage/engine weighting
        thresholds: Risk, confidence limits
        output_format: Response format
        metadata: Additional configuration
    """

    name: str
    mode: str
    emphasis: Dict[str, float] = field(default_factory=dict)
    thresholds: Dict[str, float] = field(default_factory=dict)
    output_format: str = "json"
    metadata: Dict[str, Any] = field(default_factory=dict)


class PresetRouter:
    """
    Routes analysis requests through preset + profile resolution.

    Merges preset configuration with user profile preferences to create
    a final resolved configuration for pipeline execution.
    """

    def __init__(
        self,
        preset_manager: Optional[PresetManager] = None,
        profile_manager: Optional[ProfileManager] = None
    ):
        """
        Initialize PresetRouter.

        Args:
            preset_manager: Manager for presets (creates default if None)
            profile_manager: Manager for profiles (creates default if None)
        """
        self.preset_manager = preset_manager or PresetManager()
        self.profile_manager = profile_manager or ProfileManager()

    def resolve_preset(
        self,
        preset_name: str,
        user_id: Optional[str] = None
    ) -> PresetResolvedConfig:
        """
        Resolve preset + user profile into final configuration.

        Args:
            preset_name: Preset identifier to load
            user_id: Optional user ID to load profile

        Returns:
            PresetResolvedConfig with merged configuration

        Raises:
            KeyError: If preset not found
        """
        # 1. Load base preset
        preset: PresetConfig = self.preset_manager.get_preset(preset_name)

        # 2. Load user profile (optional)
        profile: Optional[UserProfile] = None
        if user_id:
            profile = self.profile_manager.get_profile(user_id)

        # 3. Build base configuration from preset
        mode = preset.mode
        output_format = preset.output_format
        thresholds = dict(preset.thresholds)
        
        # Convert emphasis list to dict with default weight of 1.0
        emphasis = {key: 1.0 for key in preset.emphasis}
        
        metadata = dict(preset.metadata)

        # 4. Apply profile overrides if available
        if profile:
            # Override risk threshold with user's risk tolerance
            if profile.risk_tolerance is not None:
                thresholds["risk"] = profile.risk_tolerance

            # Override output format if user has preference
            if profile.output_format and profile.output_format != "json":
                output_format = profile.output_format

            # Add depth preference to metadata
            metadata["depth"] = profile.depth
            metadata["user_id"] = profile.user_id

            # Merge custom preferences
            if profile.preferences:
                metadata["user_preferences"] = profile.preferences

        return PresetResolvedConfig(
            name=preset_name,
            mode=mode,
            emphasis=emphasis,
            thresholds=thresholds,
            output_format=output_format,
            metadata=metadata,
        )

    def get_default_config(self) -> PresetResolvedConfig:
        """
        Get default configuration (alpha preset, no profile).

        Returns:
            Default PresetResolvedConfig
        """
        return self.resolve_preset("alpha")
