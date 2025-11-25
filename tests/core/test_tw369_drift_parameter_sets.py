"""
Tests for TW369 drift parameter sets.

Validates that all parameter profiles load correctly and have expected structure.
"""

import json
from pathlib import Path


PARAM_DIR = Path("schema") / "tw369"


def _load(name: str):
    """Load parameter file."""
    return json.loads((PARAM_DIR / name).read_text())


def test_default_drift_parameters_exist():
    """Test default drift parameters file exists and has required structure."""
    params = _load("drift_parameters.json")
    assert "tension_weights" in params
    assert "severity" in params
    assert "drift" in params
    assert "evolution" in params
    assert "planes" in params


def test_conservative_drift_parameters_exist():
    """Test conservative drift parameters file exists and has expected values."""
    params = _load("drift_parameters_conservative_v1.json")
    assert params.get("version") == "1.0-conservative"
    assert params["severity"]["bounds"]["max"] <= 0.9
    assert params["evolution"]["damping_factor"] == 0.35


def test_exploratory_drift_parameters_exist():
    """Test exploratory drift parameters file exists and has expected values."""
    params = _load("drift_parameters_exploratory_v1.json")
    assert params.get("version") == "1.0-exploratory"
    assert params["severity"]["bounds"]["max"] == 1.0
    assert params["evolution"]["damping_factor"] == 0.65
