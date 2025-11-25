"""
Schema validation tests for TW369 engine.

Tests validate the structure and content of TW369 schema files.
Requires jsonschema package: pip install jsonschema
"""

import json
import pytest
from pathlib import Path

# Skip all tests if jsonschema not available
jsonschema = pytest.importorskip("jsonschema")

SCHEMA_DIR = Path("schema/tw369")


def load(name):
    """Load JSON file from schema directory."""
    return json.loads((SCHEMA_DIR / name).read_text())


def test_validate_tw_state_schema():
    """Test TWState schema with valid instance."""
    schema = load("tw_state_schema.json")
    instance = {
        "plane3_cultural_macro": {"E01": 0.5},
        "plane6_semiotic_media": {"E01": -0.2},
        "plane9_structural_systemic": {"E01": 0.1}
    }
    jsonschema.validate(instance, schema)


def test_validate_drift_params_schema_structure():
    """Test drift_parameters.json has required structure."""
    params = load("drift_parameters.json")
    assert "tension_weights" in params
    assert "severity" in params
    assert "drift" in params
    assert "evolution" in params
    assert "planes" in params


def test_validate_tw369_config_schema():
    """Test TW369 config schema with valid instance."""
    schema = load("tw369_config_schema.json")
    instance = {
        "enabled": True,
        "max_time_steps": 5,
        "default_step_size": 1.0
    }
    jsonschema.validate(instance, schema)


def test_drift_parameters_math_constants():
    """Verify mathematical constants in drift_parameters.json."""
    params = load("drift_parameters.json")
    
    # Tension weights
    assert params["tension_weights"]["energy_weight"] == 0.6
    assert params["tension_weights"]["instability_weight"] == 0.4
    
    # Severity
    assert params["severity"]["model"] == "exp_decay_tracy_widom_like"
    assert params["severity"]["formula"] == "severity = 1 - exp(-mean_tension)"
    
    # Evolution
    assert params["evolution"]["damping_factor"] == 0.5
    assert params["evolution"]["min_factor"] == 0.1
    assert params["evolution"]["step_size_default"] == 1.0


def test_tw_state_schema_required_fields():
    """Test that TWState schema enforces required fields."""
    schema = load("tw_state_schema.json")
    
    # Missing required field should fail
    invalid_instance = {
        "plane3_cultural_macro": {"E01": 0.5},
        "plane6_semiotic_media": {"E01": -0.2}
        # Missing plane9_structural_systemic
    }
    
    try:
        jsonschema.validate(invalid_instance, schema)
        assert False, "Should have raised validation error"
    except jsonschema.ValidationError:
        pass  # Expected


def test_config_schema_defaults():
    """Test config schema default values."""
    schema = load("tw369_config_schema.json")
    
    # Check defaults are documented
    assert schema["properties"]["enabled"]["default"] is True
    assert schema["properties"]["max_time_steps"]["default"] == 10
    assert schema["properties"]["default_step_size"]["default"] == 1.0
