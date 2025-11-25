"""
Runtime validation helpers for TW369 engine.

Provides optional schema validation for TWState and config dicts.
Falls back to basic structural validation when jsonschema is unavailable.
"""

import json
from pathlib import Path
from typing import Any, Dict

try:
    import jsonschema  # type: ignore
    HAS_JSONSCHEMA = True
except ImportError:  # pragma: no cover
    HAS_JSONSCHEMA = False


SCHEMA_DIR = Path("schema") / "tw369"


def _load_json(path: Path) -> Dict[str, Any]:
    """Load JSON file."""
    return json.loads(path.read_text())


def validate_tw_state_dict(data: Dict[str, Any]) -> None:
    """
    Runtime validation helper for TWState-like dicts.

    - If jsonschema is available and tw_state_schema.json exists, validate against it.
    - Otherwise, perform minimal structural checks and raise ValueError on failure.
    
    Args:
        data: Dictionary to validate as TWState
        
    Raises:
        ValueError: If validation fails
        jsonschema.ValidationError: If schema validation fails (when jsonschema available)
    """
    schema_path = SCHEMA_DIR / "tw_state_schema.json"

    if HAS_JSONSCHEMA and schema_path.exists():
        schema = _load_json(schema_path)
        jsonschema.validate(data, schema)  # type: ignore[attr-defined]
        return

    # Fallback: minimal structural validation (no external dependency).
    required_keys = {
        "plane3_cultural_macro",
        "plane6_semiotic_media",
        "plane9_structural_systemic",
    }
    missing = required_keys - set(data.keys())
    if missing:
        raise ValueError(f"TWState missing required keys: {sorted(missing)}")


def validate_tw369_config_dict(cfg: Dict[str, Any]) -> None:
    """
    Runtime validation helper for TW369 engine config dicts.

    - If jsonschema is available and tw369_config_schema.json exists, validate against it.
    - Otherwise, perform minimal structural checks and raise ValueError on failure.
    
    Args:
        cfg: Dictionary to validate as TW369 config
        
    Raises:
        ValueError: If validation fails
        jsonschema.ValidationError: If schema validation fails (when jsonschema available)
    """
    schema_path = SCHEMA_DIR / "tw369_config_schema.json"

    if HAS_JSONSCHEMA and schema_path.exists():
        schema = _load_json(schema_path)
        jsonschema.validate(cfg, schema)  # type: ignore[attr-defined]
        return

    # Fallback: minimal structural validation.
    for key in ("enabled", "max_time_steps", "default_step_size"):
        if key not in cfg:
            raise ValueError(f"TW369 config missing required key: {key}")
