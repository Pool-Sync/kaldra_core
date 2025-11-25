"""
TW369 Schema Migration Utilities

Provides forward-compatible loading of drift parameters with migration support.
"""

import json
from pathlib import Path
from typing import Any, Dict

from .schema_registry import get_drift_parameters_path


def load_drift_parameters(profile: str = "default") -> Dict[str, Any]:
    """
    Helper to load a named drift parameter profile.

    This is a forward-compatible point for future migrations:
    - today, it simply loads the JSON at the registered path;
    - tomorrow, it can apply transformations if versions diverge.
    
    Args:
        profile: Parameter profile name (default, conservative_v1, exploratory_v1)
        
    Returns:
        Drift parameters dictionary
        
    Raises:
        ValueError: If profile is unknown
        FileNotFoundError: If parameter file doesn't exist
    """
    path = get_drift_parameters_path(profile)
    return json.loads(Path(path).read_text())
