"""
Configuration loader utilities for TW369.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class PainleveConfig:
    """Painlevé solver configuration."""
    alpha: float = 0.0
    x_start: float = -5.0
    x_end: float = 5.0
    step_size: float = 0.01
    tolerance: float = 1e-5
    window_short: int = 5
    window_long: int = 20
    volatility_threshold: float = 0.5


def load_painleve_config(schema_dir: Optional[Path] = None) -> PainleveConfig:
    """
    Load Painlevé configuration from schema.
    
    Args:
        schema_dir: Optional schema directory path
        
    Returns:
        PainleveConfig object
    """
    if schema_dir is None:
        schema_dir = Path(__file__).parent.parent.parent / "schema" / "tw369"
    
    config_path = schema_dir / "painleve_config.json"
    
    if not config_path.exists():
        return PainleveConfig()
    
    with open(config_path, "r") as f:
        data = json.load(f)
    
    return PainleveConfig(**data)
