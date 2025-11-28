"""Tests for KALDRA-Product Kindra mapping."""

import pytest
from unittest.mock import MagicMock
import numpy as np

from src.apps.product.product_kindra_mapping import (
    ProductNarrativeInput,
    ProductKindraMapping,
    map_text_to_product_kindra
)
from src.core.kaldra_master_engine import KaldraMasterEngineV2


def test_map_text_to_product_kindra_basic():
    """Test basic product Kindra mapping."""
    engine = KaldraMasterEngineV2(d_ctx=16)
    
    mapping = map_text_to_product_kindra(
        text="This product is amazing and exceeded expectations",
        engine=engine,
        product_id="PROD-123",
        category="electronics"
    )
    
    assert isinstance(mapping, ProductKindraMapping)
    assert mapping.domain == "PRODUCT"
    assert len(mapping.archetype_top_indices) > 0


def test_map_text_to_product_kindra_empty_text():
    """Test that empty text raises ValueError."""
    engine = KaldraMasterEngineV2(d_ctx=16)
    
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        map_text_to_product_kindra("", engine)
    
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        map_text_to_product_kindra("   ", engine)


def test_product_kindra_mapping_structure():
    """Test that ProductKindraMapping has expected structure."""
    engine = KaldraMasterEngineV2(d_ctx=16)
    
    mapping = map_text_to_product_kindra(
        text="Great customer service experience",
        engine=engine
    )
    
    assert hasattr(mapping, "kindra_layer1")
    assert hasattr(mapping, "kindra_layer2")
    assert hasattr(mapping, "kindra_layer3")
    assert hasattr(mapping, "dominant_vectors")
    assert hasattr(mapping, "archetype_top_indices")
    assert isinstance(mapping.kindra_layer1, dict)
