"""
Tau Integration Helpers.

Functions to apply Tau modifiers to various system components.
"""
from typing import Dict, Any, List
import numpy as np
from .tau_state import TauState

def apply_tau_to_delta12(delta12: Dict[str, float], tau_state: TauState) -> Dict[str, float]:
    """
    Apply Tau smoothing to Delta12 vector.
    
    If Tau is low (high risk), the distribution is flattened (smoothed) to reduce
    archetypal certainty and extreme peaks.
    """
    smoothing_factor = tau_state.tau_modifiers.get("archetype_smoothing", 1.0)
    
    if smoothing_factor >= 0.99:
        return delta12
        
    # Apply temperature scaling / smoothing
    # New_prob = prob ^ factor / sum(prob ^ factor)
    # But here we want smoothing towards uniform distribution as factor decreases.
    # Let's use a simple interpolation between original and uniform.
    
    values = np.array(list(delta12.values()))
    keys = list(delta12.keys())
    
    uniform = np.ones_like(values) / len(values)
    
    # Interpolate: smoothed = factor * original + (1-factor) * uniform
    smoothed_values = (smoothing_factor * values) + ((1.0 - smoothing_factor) * uniform)
    
    # Re-normalize just in case
    smoothed_values /= smoothed_values.sum()
    
    return dict(zip(keys, smoothed_values))

def modulate_profile_scores(profile_scores: np.ndarray, tau_state: TauState) -> np.ndarray:
    """
    Modulate Delta144 profile scores (raw logits or probs).
    """
    smoothing_factor = tau_state.tau_modifiers.get("archetype_smoothing", 1.0)
    
    if smoothing_factor >= 0.99:
        return profile_scores
        
    # Simple dampening of variance
    mean = np.mean(profile_scores)
    dampened = mean + (profile_scores - mean) * smoothing_factor
    
    return dampened
