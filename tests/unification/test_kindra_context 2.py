"""
Tests for KindraContext v3.1 structure and methods.
"""
import pytest
import json
from src.unification.states.unified_state import KindraContext, KindraLayerScores


def test_kindra_layer_scores_basic():
    """Test KindraLayerScores creation and attributes."""
    layer = KindraLayerScores(
        scores={"V1": 0.5, "V2": 0.8},
        avg_score=0.65,
        max_score=0.8
    )
    assert len(layer.scores) == 2
    assert layer.avg_score == 0.65
    assert layer.max_score == 0.8


def test_kindra_layer_scores_to_json():
    """Test KindraLayerScores JSON serialization."""
    layer = KindraLayerScores(
        scores={"V1": 0.5},
        avg_score=0.5,
        max_score=0.5
    )
    data = layer.to_json()
    assert data["scores"] == {"V1": 0.5}
    assert data["avg_score"] == 0.5
    assert data["max_score"] == 0.5


def test_total_vectors_is_144():
    """Test that get_total_vectors returns 144 for full context."""
    layer1 = KindraLayerScores(scores={f"L1_V{i}": 0.5 for i in range(48)})
    layer2 = KindraLayerScores(scores={f"L2_V{i}": 0.5 for i in range(48)})
    layer3 = KindraLayerScores(scores={f"L3_V{i}": 0.5 for i in range(48)})
    
    ctx = KindraContext(layer1=layer1, layer2=layer2, layer3=layer3)
    assert ctx.get_total_vectors() == 144


def test_get_top_vectors_returns_correct_length():
    """Test that get_top_vectors returns the correct number."""
    layer1 = KindraLayerScores(scores={"L1_V1": 0.9, "L1_V2": 0.5})
    layer2 = KindraLayerScores(scores={"L2_V1": 0.8, "L2_V2": 0.6})
    layer3 = KindraLayerScores(scores={"L3_V1": 0.7, "L3_V2": 0.4})
    
    ctx = KindraContext(layer1=layer1, layer2=layer2, layer3=layer3)
    top_3 = ctx.get_top_vectors(n=3)
    
    assert len(top_3) == 3
    assert top_3[0]["id"] == "L1_V1"
    assert top_3[0]["score"] == 0.9
    assert top_3[0]["layer"] == 1
    
    assert top_3[1]["id"] == "L2_V1"
    assert top_3[1]["score"] == 0.8
    
    assert top_3[2]["id"] == "L3_V1"
    assert top_3[2]["score"] == 0.7


def test_json_roundtrip_preserves_structure():
    """Test that to_json/from_json preserves structure."""
    layer1 = KindraLayerScores(
        scores={"L1_V1": 0.9},
        avg_score=0.9,
        max_score=0.9
    )
    layer2 = KindraLayerScores(scores={"L2_V1": 0.8})
    layer3 = KindraLayerScores(scores={"L3_V1": 0.7})
    
    original = KindraContext(
        layer1=layer1,
        layer2=layer2,
        layer3=layer3,
        tw_plane_distribution={3: 0.33, 6: 0.33, 9: 0.34},
        delta144_weights={"A01_CREATOR": 0.5},
        metadata={"engine": "test"}
    )
    
    # Serialize
    json_data = original.to_json()
    
    # Deserialize
    restored = KindraContext.from_json(json_data)
    
    # Verify
    assert restored.layer1.scores == original.layer1.scores
    assert restored.layer1.avg_score == original.layer1.avg_score
    assert restored.tw_plane_distribution == original.tw_plane_distribution
    assert restored.delta144_weights == original.delta144_weights
    assert restored.metadata == original.metadata


def test_tw_plane_distribution_present():
    """Test that TW plane distribution is properly stored."""
    ctx = KindraContext(
        tw_plane_distribution={3: 0.4, 6: 0.3, 9: 0.3}
    )
    assert sum(ctx.tw_plane_distribution.values()) == pytest.approx(1.0)
    assert 3 in ctx.tw_plane_distribution
    assert 6 in ctx.tw_plane_distribution
    assert 9 in ctx.tw_plane_distribution


def test_layers_have_48_entries_each():
    """Test that each layer can hold 48 vectors."""
    layer1_scores = {f"L1_V{i}": 0.5 for i in range(48)}
    layer2_scores = {f"L2_V{i}": 0.5 for i in range(48)}
    layer3_scores = {f"L3_V{i}": 0.5 for i in range(48)}
    
    layer1 = KindraLayerScores(scores=layer1_scores)
    layer2 = KindraLayerScores(scores=layer2_scores)
    layer3 = KindraLayerScores(scores=layer3_scores)
    
    assert len(layer1.scores) == 48
    assert len(layer2.scores) == 48
    assert len(layer3.scores) == 48
    
    ctx = KindraContext(layer1=layer1, layer2=layer2, layer3=layer3)
    assert ctx.get_total_vectors() == 144


def test_to_dict_legacy_compatibility():
    """Test that to_dict maintains backward compatibility."""
    layer1 = KindraLayerScores(scores={"V1": 0.5})
    ctx = KindraContext(layer1=layer1)
    
    data = ctx.to_dict()
    assert "layer1" in data
    assert data["layer1"] == {"V1": 0.5}  # Should be just the scores dict
