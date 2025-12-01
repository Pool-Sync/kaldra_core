"""
Tests for Delta12Vector and compute_delta12.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from archetypes.delta12_vector import Delta12Vector, ARCHETYPE_IDS
from archetypes.delta144_engine import Delta144Engine


def test_delta12_normalizes_to_one():
    """Test that Delta12Vector normalizes to sum=1.0."""
    values = {arch_id: float(i) for i, arch_id in enumerate(ARCHETYPE_IDS)}
    delta12 = Delta12Vector(values=values)
    delta12.normalize()
    
    total = sum(delta12.values.values())
    assert abs(total - 1.0) < 1e-6, "Delta12 should normalize to 1.0"


def test_delta12_dominant_returns_expected_archetype():
    """Test dominant archetype selection."""
    values = {arch_id: 0.05 for arch_id in ARCHETYPE_IDS}
    values["A07_RULER"] = 0.6
    
    delta12 = Delta12Vector(values=values)
    delta12.normalize()
    
    dominant_id, dominant_prob = delta12.dominant()
    
    assert dominant_id == "A07_RULER"
    assert dominant_prob > 0.3  # Should be highest after normalization


def test_compute_delta12_runs():
    """Test that compute_delta12 runs without error."""
    engine = Delta144Engine.from_default_files(d_ctx=128)
    
    plane_scores = {"3": 0.2, "6": 0.6, "9": 0.2}
    profile_scores = {"EXPANSIVE": 0.1, "CONTRACTIVE": 0.7, "TRANSCENDENT": 0.2}
    
    delta12 = engine.compute_delta12(
        plane_scores=plane_scores,
        profile_scores=profile_scores
    )
    
    assert isinstance(delta12, Delta12Vector)
    assert len(delta12.values) == 12
    
    # Should be normalized
    total = sum(delta12.values.values())
    assert abs(total - 1.0) < 1e-6


def test_compute_delta12_plane_6_favors_ruler():
    """Test that high Plane 6 favors RULER archetype."""
    engine = Delta144Engine.from_default_files(d_ctx=128)
    
    plane_scores = {"3": 0.1, "6": 0.8, "9": 0.1}
    profile_scores = {"EXPANSIVE": 0.1, "CONTRACTIVE": 0.8, "TRANSCENDENT": 0.1}
    
    delta12 = engine.compute_delta12(
        plane_scores=plane_scores,
        profile_scores=profile_scores
    )
    
    # RULER should have high probability
    ruler_prob = delta12.values.get("A07_RULER", 0.0)
    assert ruler_prob > 0.15, "RULER should be favored with high Plane 6"


def test_delta12_top_k():
    """Test top_k method."""
    values = {arch_id: float(i) / 100 for i, arch_id in enumerate(ARCHETYPE_IDS)}
    delta12 = Delta12Vector(values=values)
    delta12.normalize()
    
    top_3 = delta12.top_k(k=3)
    
    assert len(top_3) == 3
    # Should be sorted descending
    assert top_3[0][1] >= top_3[1][1] >= top_3[2][1]
