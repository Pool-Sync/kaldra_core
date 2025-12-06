"""
Exoskeleton Presets System.

Defines PresetConfig and PresetManager for domain-specific KALDRA analysis modes.
"""

import copy
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class PresetConfig:
    """
    PresetConfig defines how KALDRA should operate for a specific context.

    Attributes:
        name: Unique identifier for the preset
        description: Human-readable description
        mode: Execution mode (signal/full/story/safety-first/exploratory)
        emphasis: Modules/stages with higher weight
        thresholds: Risk, confidence, and other limits
        output_format: Response format type
        metadata: Auxiliary information for frontend/API
    """

    name: str
    description: str
    mode: str  # "signal", "full", "story", "safety-first", "exploratory"
    emphasis: List[str] = field(default_factory=list)
    thresholds: Dict[str, float] = field(default_factory=dict)
    output_format: str = "json"
    metadata: Dict[str, Any] = field(default_factory=dict)


# Default preset definitions
_DEFAULT_PRESETS: Dict[str, PresetConfig] = {
    "alpha": PresetConfig(
        name="alpha",
        description="Financial / earnings narrative analysis",
        mode="full",
        emphasis=[
            "kindra.layer1",         # Cultural/Macro
            "meta.nietzsche",        # Power dynamics
            "core.archetypes",       # Δ144
            "story",                 # When v3.2 arrives
        ],
        thresholds={
            "risk": 0.30,
            "confidence_min": 0.60,
        },
        output_format="financial_brief",
        metadata={
            "domain": "finance",
            "ui_layout": "alpha_dashboard_v1",
        },
    ),
    "geo": PresetConfig(
        name="geo",
        description="Geopolitical narrative and regime analysis",
        mode="story",
        emphasis=[
            "kindra.layer1",         # Geopolitics / macro
            "kindra.tw_plane",       # 3/6/9 distribution
            "meta.aurelius",         # Stoic lens for crisis & control
            "core.archetypes",
        ],
        thresholds={
            "risk": 0.40,
            "confidence_min": 0.55,
        },
        output_format="geopolitical_brief",
        metadata={
            "domain": "geopolitics",
            "ui_layout": "geo_dashboard_v1",
        },
    ),
    "safeguard": PresetConfig(
        name="safeguard",
        description="Safety-first narrative risk and mitigation",
        mode="safety-first",
        emphasis=[
            "safeguard",
            "tau",
            "bias",
            "kindra.layer2",      # Media/semiotic toxicity
        ],
        thresholds={
            "risk": 0.20,
            "confidence_min": 0.70,
        },
        output_format="safety_report",
        metadata={
            "domain": "safeguard",
            "ui_layout": "safeguard_dashboard_v1",
        },
    ),
    "product": PresetConfig(
        name="product",
        description="Brand / product narrative and market resonance",
        mode="full",
        emphasis=[
            "kindra.layer2",         # Semiotic/Media (brand messaging)
            "meta.campbell",         # Hero's Journey for brand
            "core.polarities",       # Brand tensions
            "core.archetypes",
        ],
        thresholds={
            "risk": 0.35,
            "confidence_min": 0.60,
        },
        output_format="brand_brief",
        metadata={
            "domain": "product",
            "ui_layout": "product_dashboard_v1",
        },
    ),
}


class PresetManager:
    """
    Manages Exoskeleton presets.

    Provides methods to retrieve and list available presets.
    Supports extension with custom presets.
    """

    def __init__(self, extra_presets: Optional[Dict[str, PresetConfig]] = None):
        """
        Initialize PresetManager.

        Args:
            extra_presets: Additional custom presets to merge with defaults
        """
        self._presets: Dict[str, PresetConfig] = dict(_DEFAULT_PRESETS)
        if extra_presets:
            self._presets.update(extra_presets)

    def get_preset(self, name: str) -> PresetConfig:
        """
        Retrieve a preset by name.

        Args:
            name: Preset identifier

        Returns:
            PresetConfig for the requested preset (deep copy)

        Raises:
            KeyError: If preset not found
        """
        if name not in self._presets:
            raise KeyError(f"Preset not found: {name}")
        return copy.deepcopy(self._presets[name])

    def list_presets(self) -> Dict[str, PresetConfig]:
        """
        List all available presets.

        Returns:
            Dictionary of preset name to PresetConfig (deep copies)
        """
        return {name: copy.deepcopy(config) for name, config in self._presets.items()}

    def has_preset(self, name: str) -> bool:
        """
        Check if a preset exists.

        Args:
            name: Preset identifier

        Returns:
            True if preset exists, False otherwise
        """
        return name in self._presets
