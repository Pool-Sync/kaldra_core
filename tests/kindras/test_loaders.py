"""
Tests for Kindra Loaders (Layer 1, 2, 3)
"""

import pytest
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from kindras.layer1_cultural_macro_loader import Layer1Loader
from kindras.layer2_semiotic_media_loader import Layer2Loader
from kindras.layer3_structural_systemic_loader import Layer3Loader


class TestLayer1Loader:
    def test_loader_initialization(self):
        """Test that Layer 1 loader initializes correctly."""
        loader = Layer1Loader("schema/kindras/kindra_vectors_layer1_cultural_macro_48.json")
        assert loader is not None
        assert len(loader.vectors) == 48
    
    def test_get_vector(self):
        """Test retrieving a specific vector."""
        loader = Layer1Loader("schema/kindras/kindra_vectors_layer1_cultural_macro_48.json")
        vector = loader.get_vector("E01")
        assert vector is not None
        assert vector.id == "E01"
        assert vector.layer == "L1_CULTURAL_MACRO"
        assert vector.tw_plane == "3"
    
    def test_get_by_domain(self):
        """Test filtering vectors by domain."""
        loader = Layer1Loader("schema/kindras/kindra_vectors_layer1_cultural_macro_48.json")
        expressive_vectors = loader.get_by_domain("EXPRESSIVE")
        assert len(expressive_vectors) == 8  # E01-E08


class TestLayer2Loader:
    def test_loader_initialization(self):
        """Test that Layer 2 loader initializes correctly."""
        loader = Layer2Loader("schema/kindras/kindra_vectors_layer2_semiotic_media_48.json")
        assert loader is not None
        assert len(loader.vectors) == 48
    
    def test_get_vector(self):
        """Test retrieving a specific vector."""
        loader = Layer2Loader("schema/kindras/kindra_vectors_layer2_semiotic_media_48.json")
        vector = loader.get_vector("E01")
        assert vector is not None
        assert vector.layer == "L2_SEMIOTIC_MEDIA"
        assert vector.tw_plane == "6"


class TestLayer3Loader:
    def test_loader_initialization(self):
        """Test that Layer 3 loader initializes correctly."""
        loader = Layer3Loader("schema/kindras/kindra_vectors_layer3_structural_systemic_48.json")
        assert loader is not None
        assert len(loader.vectors) == 48
    
    def test_get_vector(self):
        """Test retrieving a specific vector."""
        loader = Layer3Loader("schema/kindras/kindra_vectors_layer3_structural_systemic_48.json")
        vector = loader.get_vector("E01")
        assert vector is not None
        assert vector.layer == "L3_STRUCTURAL_SYSTEMIC"
        assert vector.tw_plane == "9"
