"""
Runtime validation tests for TW369 engine.

Tests runtime validation of TWState and config dicts.
"""

import pytest

from src.tw369.runtime_validation import (
    validate_tw_state_dict,
    validate_tw369_config_dict,
)


def test_validate_tw_state_dict_minimal_ok():
    """Test TWState validation with valid minimal data."""
    data = {
        "plane3_cultural_macro": {"E01": 0.5},
        "plane6_semiotic_media": {"E01": -0.2},
        "plane9_structural_systemic": {"E01": 0.1},
    }
    # Should not raise
    validate_tw_state_dict(data)


def test_validate_tw_state_dict_missing_key():
    """Test TWState validation fails with missing required key."""
    data = {
        "plane3_cultural_macro": {"E01": 0.5},
        "plane6_semiotic_media": {"E01": -0.2},
    }
    with pytest.raises(ValueError):
        validate_tw_state_dict(data)


def test_validate_tw369_config_dict_minimal_ok():
    """Test config validation with valid minimal data."""
    cfg = {
        "enabled": True,
        "max_time_steps": 10,
        "default_step_size": 1.0,
    }
    # Should not raise
    validate_tw369_config_dict(cfg)


def test_validate_tw369_config_dict_missing_key():
    """Test config validation fails with missing required key."""
    cfg = {
        "enabled": True,
        "default_step_size": 1.0,
    }
    with pytest.raises(ValueError):
        validate_tw369_config_dict(cfg)
