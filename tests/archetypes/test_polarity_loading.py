"""
Test polarity loading functionality.

v2.7: Tests for load_polarities() and Polarity dataclass.
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.archetypes.delta144_engine import load_polarities, Polarity
from src.config import POLARITIES_FILE


def test_polarity_dataclass():
    """Test Polarity dataclass creation."""
    pol = Polarity(
        id="POL_LIGHT_SHADOW",
        label="Luz ↔ Sombra",
        description="Polaridade fundamental do psiquismo.",
        dimension="existential",
        tw_alignment=["3", "6", "9"]
    )
    
    assert pol.id == "POL_LIGHT_SHADOW"
    assert pol.label == "Luz ↔ Sombra"
    assert pol.dimension == "existential"
    assert len(pol.tw_alignment) == 3


def test_load_polarities_from_schema():
    """Test loading polarities from schema file."""
    polarities = load_polarities(POLARITIES_FILE)
    
    # Should load 48 polarities (updated count from schema)
    assert len(polarities) == 48
    
    # Check some known polarities exist
    assert "POL_LIGHT_SHADOW" in polarities
    assert "POL_ORDER_CHAOS" in polarities
    assert "POL_EXPANSION_CONTRACTION" in polarities
    
    # Verify structure
    pol = polarities["POL_LIGHT_SHADOW"]
    assert isinstance(pol, Polarity)
    assert pol.id == "POL_LIGHT_SHADOW"
    assert pol.dimension == "existential"
    assert isinstance(pol.tw_alignment, list)


def test_load_polarities_missing_file():
    """Test graceful handling of missing file."""
    fake_path = Path("/nonexistent/polarities.json")
    polarities = load_polarities(fake_path)
    
    # Should return empty dict, not crash
    assert polarities == {}


def test_polarity_dimensions():
    """Test that polarities have correct dimensions."""
    polarities = load_polarities(POLARITIES_FILE)
    
    dimensions = set(p.dimension for p in polarities.values())
    
    # Should have multiple dimensions
    assert len(dimensions) > 5
    
    # Check some expected dimensions
    expected_dims = {"existential", "structure", "energy", "cognition", "affect"}
    assert expected_dims.issubset(dimensions)


def test_polarity_tw_alignment():
    """Test that polarities have TW alignment."""
    polarities = load_polarities(POLARITIES_FILE)
    
    # All polarities should have tw_alignment
    for pol in polarities.values():
        assert isinstance(pol.tw_alignment, list)
        assert len(pol.tw_alignment) > 0
        
        # All alignments should be valid TW planes
        for plane in pol.tw_alignment:
            assert plane in ["3", "6", "9"]


def test_polarity_count_by_dimension():
    """Test polarity distribution across dimensions."""
    polarities = load_polarities(POLARITIES_FILE)
    
    dim_counts = {}
    for pol in polarities.values():
        dim_counts[pol.dimension] = dim_counts.get(pol.dimension, 0) + 1
    
    # Should have polarities in multiple dimensions
    assert len(dim_counts) >= 9
    
    # Each dimension should have at least one polarity
    for count in dim_counts.values():
        assert count > 0
