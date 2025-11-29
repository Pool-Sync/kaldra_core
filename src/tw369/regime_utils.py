"""
Regime utilities for TW369 - Archetype regime mapping.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.archetypes.delta12_vector import Delta12Vector


DEFAULT_REGIME = {
    "preferred_plane": "6",
    "drift_tolerance": 0.5,
    "painleve_alpha": 0.0
}


def load_archetype_regimes(schema_dir: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    """
    Load archetype regime mappings from schema.
    
    Args:
        schema_dir: Optional schema directory path
        
    Returns:
        Dictionary mapping archetype_id to regime config
    """
    if schema_dir is None:
        schema_dir = Path(__file__).parent.parent.parent / "schema" / "tw369"
    
    regimes_path = schema_dir / "archetype_regimes.json"
    
    if not regimes_path.exists():
        return {}
    
    with open(regimes_path, "r") as f:
        return json.load(f)


def get_tw_regime_for_delta12(delta12: "Delta12Vector") -> Dict[str, Any]:
    """
    Get TW369 regime configuration for a Delta12 vector.
    
    Uses the dominant archetype to select regime parameters.
    
    Args:
        delta12: Delta12Vector with archetype probabilities
        
    Returns:
        Regime configuration dict
    """
    regimes = load_archetype_regimes()
    
    dominant_id, _ = delta12.dominant()
    
    return regimes.get(dominant_id, DEFAULT_REGIME.copy())


def get_painleve_alpha_for_archetype(archetype_id: str) -> float:
    """
    Get Painlevé alpha parameter for a specific archetype.
    
    Args:
        archetype_id: Archetype identifier (e.g., "A07_RULER")
        
    Returns:
        Alpha value for Painlevé solver
    """
    schema_dir = Path(__file__).parent.parent.parent / "schema" / "tw369"
    calibration_path = schema_dir / "regime_calibration.json"
    
    if not calibration_path.exists():
        return 0.0
    
    with open(calibration_path, "r") as f:
        calibration = json.load(f)
    
    regime = calibration.get(archetype_id, {})
    return float(regime.get("alpha", 0.0))


def adjust_tw_regime_with_meta(
    regime_config: Dict[str, Any],
    nietzsche_scores: Optional[Dict[str, float]] = None,
    aurelius_scores: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Adjust TW369 regime parameters based on meta-signals.
    
    Modifies noise_scale, drift_tolerance, and preferred_plane based on
    Nietzsche and Aurelius philosophical scores.
    
    Args:
        regime_config: Base TW369 regime configuration
        nietzsche_scores: Nietzsche 12-axis scores (optional)
        aurelius_scores: Aurelius 12-axis scores (optional)
        
    Returns:
        Adjusted regime configuration
        
    Example:
        >>> adjusted = adjust_tw_regime_with_meta(
        ...     regime_config,
        ...     nietzsche_scores={"active_nihilism": 0.8, "dionysian_force": 0.7},
        ...     aurelius_scores={"serenity": 0.75, "emotional_regulation": 0.68}
        ... )
    """
    if nietzsche_scores is None and aurelius_scores is None:
        return regime_config  # No adjustment
    
    # Copy config to avoid mutation
    adjusted = regime_config.copy()
    
    # Get current values with defaults
    noise_scale = adjusted.get("noise_scale", 1.0)
    drift_tolerance = adjusted.get("drift_tolerance", 0.5)
    preferred_plane = adjusted.get("preferred_plane", "6")
    
    # Nietzsche adjustments
    if nietzsche_scores:
        active_nihilism = nietzsche_scores.get("active_nihilism", 0.0)
        dionysian = nietzsche_scores.get("dionysian_force", 0.0)
        apollonian = nietzsche_scores.get("apollonian_order", 0.0)
        
        # High active nihilism → increase noise, decrease tolerance (more unstable)
        if active_nihilism > 0.6:
            noise_scale *= (1.0 + (active_nihilism - 0.6) * 0.5)  # Up to +20%
            drift_tolerance *= (1.0 - (active_nihilism - 0.6) * 0.3)  # Down to -12%
        
        # High dionysian → favor Plane 3 (action/expansion)
        if dionysian > 0.6:
            preferred_plane = "3"
            noise_scale *= (1.0 + (dionysian - 0.6) * 0.3)
        
        # High apollonian → favor Plane 6 (structure), reduce noise
        if apollonian > 0.6:
            preferred_plane = "6"
            noise_scale *= (1.0 - (apollonian - 0.6) * 0.2)
    
    # Aurelius adjustments
    if aurelius_scores:
        serenity = aurelius_scores.get("serenity", 0.0)
        emotional_regulation = aurelius_scores.get("emotional_regulation", 0.0)
        discipline = aurelius_scores.get("discipline_of_will", 0.0)
        
        # High Stoic alignment → reduce noise, increase stability
        stoic_alignment = (serenity + emotional_regulation + discipline) / 3.0
        if stoic_alignment > 0.6:
            noise_scale *= (1.0 - (stoic_alignment - 0.6) * 0.4)  # Down to -16%
            drift_tolerance *= (1.0 + (stoic_alignment - 0.6) * 0.2)  # Up to +8%
        
        # High discipline → favor Plane 6 (structure)
        if discipline > 0.65:
            preferred_plane = "6"
    
    # Apply adjustments
    adjusted["noise_scale"] = max(0.1, min(2.0, noise_scale))  # Clamp to reasonable range
    adjusted["drift_tolerance"] = max(0.1, min(1.0, drift_tolerance))
    adjusted["preferred_plane"] = preferred_plane
    
    return adjusted
