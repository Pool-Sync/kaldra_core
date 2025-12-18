"""
TW369 Schema Registry

Provides access to schema and parameter file paths via versioned index.
"""

import json
from pathlib import Path
from typing import Any, Dict


SCHEMA_INDEX_PATH = Path("schema") / "tw369" / "schema_index.json"


def load_schema_index() -> Dict[str, Any]:
    """
    Load the schema index file.
    
    Returns:
        Schema index dictionary with paths and versions
    """
    return json.loads(SCHEMA_INDEX_PATH.read_text())


def get_drift_parameters_path(profile: str = "default") -> Path:
    """
    Get path to drift parameters file for a given profile.
    
    Args:
        profile: Parameter profile name (default, conservative_v1, exploratory_v1)
        
    Returns:
        Path to drift parameters JSON file
        
    Raises:
        ValueError: If profile is unknown
    """
    index = load_schema_index()
    params = index["drift_parameters"].get(profile)
    if not params:
        raise ValueError(f"Unknown drift profile: {profile}")
    return Path(params["path"])
