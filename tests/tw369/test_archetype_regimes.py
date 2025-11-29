"""
Tests for archetype regimes integration.
"""

import pytest
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from archetypes.delta12_vector import Delta12Vector, ARCHETYPE_IDS


def test_load_regime_for_known_archetype():
    """Test loading regime configuration for known archetype."""
    schema_path = Path(__file__).parent.parent.parent / "schema" / "tw369" / "archetype_regimes.json"
    
    if not schema_path.exists():
        pytest.skip("archetype_regimes.json not found")
    
    with open(schema_path, "r") as f:
        regimes = json.load(f)
    
    # Test known archetype
    ruler_regime = regimes.get("A07_RULER")
    
    assert ruler_regime is not None
    assert "preferred_plane" in ruler_regime
    assert "drift_tolerance" in ruler_regime
    assert ruler_regime["preferred_plane"] in ["3", "6", "9"]


def test_default_regime_for_unknown_archetype():
    """Test fallback for unknown archetype."""
    schema_path = Path(__file__).parent.parent.parent / "schema" / "tw369" / "archetype_regimes.json"
    
    if not schema_path.exists():
        pytest.skip("archetype_regimes.json not found")
    
    with open(schema_path, "r") as f:
        regimes = json.load(f)
    
    # Unknown archetype should not exist
    unknown_regime = regimes.get("A99_UNKNOWN")
    
    assert unknown_regime is None, "Unknown archetype should not have regime"


def test_delta12_vector_creation():
    """Test Delta12Vector creation and normalization."""
    # Create from dict
    values = {arch_id: 0.1 if i < 5 else 0.0 for i, arch_id in enumerate(ARCHETYPE_IDS)}
    delta12 = Delta12Vector(values=values)
    
    # Normalize
    delta12.normalize()
    
    # Sum should be 1.0
    total = sum(delta12.values.values())
    assert abs(total - 1.0) < 1e-6


def test_delta12_dominant():
    """Test dominant archetype selection."""
    values = {arch_id: 0.05 for arch_id in ARCHETYPE_IDS}
    values["A07_RULER"] = 0.5
    
    delta12 = Delta12Vector(values=values)
    delta12.normalize()
    
    dominant_id, dominant_prob = delta12.dominant()
    
    assert dominant_id == "A07_RULER"
    assert dominant_prob > 0.3  # Should be highest after normalization


def test_delta12_from_list():
    """Test creating Delta12Vector from list."""
    values_list = [0.1] * 12
    delta12 = Delta12Vector.from_list(values_list)
    
    assert len(delta12.values) == 12
    assert all(v == 0.1 for v in delta12.values.values())


def test_delta12_to_list():
    """Test converting Delta12Vector to list."""
    values = {arch_id: float(i) / 12 for i, arch_id in enumerate(ARCHETYPE_IDS)}
    delta12 = Delta12Vector(values=values)
    
    values_list = delta12.to_list()
    
    assert len(values_list) == 12
    assert values_list[0] == 0.0  # A01_INNOCENT
    assert values_list[6] == 6.0 / 12  # A07_RULER
