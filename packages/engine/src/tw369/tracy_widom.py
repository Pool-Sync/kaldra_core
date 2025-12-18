"""
Tracy-Widom Module for TW369 Engine.

Provides real Tracy-Widom statistics for severity calculation,
replacing heuristic tanh approximation.
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np


def load_tw_lookup(schema_dir: Optional[Path] = None) -> Dict:
    """Load Tracy-Widom lookup table from schema."""
    if schema_dir is None:
        schema_dir = Path(__file__).parent.parent.parent / "schema" / "tw369"
    
    lookup_path = schema_dir / "tracy_widom_lookup.json"
    
    if not lookup_path.exists():
        return {}
    
    with open(lookup_path, "r") as f:
        return json.load(f)


def load_tw_parameters(schema_dir: Optional[Path] = None) -> Dict:
    """Load Tracy-Widom parameters from schema."""
    if schema_dir is None:
        schema_dir = Path(__file__).parent.parent.parent / "schema" / "tw369"
    
    params_path = schema_dir / "tw_parameters.json"
    
    if not params_path.exists():
        return {"enabled": False, "beta": 2, "use_lookup": True, "severity_scale": 1.0}
    
    with open(params_path, "r") as f:
        return json.load(f)


def tw_cdf(x: float, beta: int = 2, lookup: Optional[Dict] = None) -> float:
    """
    Compute Tracy-Widom CDF at x using lookup table with linear interpolation.
    
    Args:
        x: Input value
        beta: Ensemble type (1, 2, or 4)
        lookup: Preloaded lookup table (optional)
        
    Returns:
        CDF value in [0, 1]
    """
    if lookup is None:
        lookup = load_tw_lookup()
    
    beta_key = f"beta_{beta}"
    
    if beta_key not in lookup:
        # Fallback to heuristic if lookup not available
        return _heuristic_cdf(x)
    
    x_vals = lookup[beta_key]["x"]
    cdf_vals = lookup[beta_key]["cdf"]
    
    # Linear interpolation
    return float(np.interp(x, x_vals, cdf_vals))


def _heuristic_cdf(x: float) -> float:
    """
    Heuristic CDF approximation (legacy fallback).
    Maps x to [0, 1] using tanh-based transformation.
    """
    # Approximate CDF using tanh (legacy v2.3 behavior)
    # Ensure output is always in [0, 1]
    return max(0.0, min(1.0, 0.5 * (1.0 + math.tanh(x / 2.0))))


def severity_from_index(
    instability_index: float,
    params: Optional[Dict] = None,
    lookup: Optional[Dict] = None
) -> float:
    """
    Compute severity factor from instability index.
    
    Args:
        instability_index: Measure of system instability
        params: TW parameters (optional, will load from schema if None)
        lookup: TW lookup table (optional, will load from schema if None)
        
    Returns:
        Severity in [0, 1]
    """
    if params is None:
        params = load_tw_parameters()
    
    enabled = params.get("enabled", False)
    beta = params.get("beta", 2)
    use_lookup = params.get("use_lookup", True)
    severity_scale = params.get("severity_scale", 1.0)
    
    if not enabled:
        # Legacy heuristic (v2.3 behavior)
        return _heuristic_cdf(instability_index * 2.0)
    
    if use_lookup:
        # Use TW lookup table
        if lookup is None:
            lookup = load_tw_lookup()
        
        # Map instability_index to x-scale (normalize)
        x = instability_index * severity_scale
        
        # Get CDF value
        cdf_value = tw_cdf(x, beta=beta, lookup=lookup)
        
        return float(cdf_value)
    else:
        # Use heuristic even if enabled (for testing)
        return _heuristic_cdf(instability_index * severity_scale)
