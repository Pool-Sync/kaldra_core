"""
Tests for KindraEngine v3.1.
"""
import pytest
from unittest.mock import MagicMock, patch
from src.kindras.kindra_engine import KindraEngine
from src.unification.states.unified_state import KindraContext

@pytest.fixture
def mock_loaders():
    with patch('src.kindras.kindra_engine.load_layer_vectors') as mock_load_vec, \
         patch('src.kindras.kindra_engine.load_layer_mapping') as mock_load_map:
        
        # Mock vectors
        mock_load_vec.side_effect = lambda layer: {
            f"L{layer}_V1": {"id": f"L{layer}_V1", "keywords": ["test"]},
            f"L{layer}_V2": {"id": f"L{layer}_V2", "keywords": ["sample"]}
        }
        
        # Mock maps
        mock_load_map.side_effect = lambda layer: {
            f"L{layer}_V1": {"delta144_targets": [{"id": "A01_CREATOR", "weight": 1.0}]},
            f"L{layer}_V2": {"delta144_targets": [{"id": "A04_HERO", "weight": 0.5}]}
        }
        
        yield mock_load_vec, mock_load_map

def test_score_all_layers_runs_without_error(mock_loaders):
    engine = KindraEngine()
    ctx = engine.score_all_layers("This is a test text")
    assert isinstance(ctx, KindraContext)
    assert ctx.metadata["engine"] == "KindraEngine v3.1"

def test_layer_scores_populated(mock_loaders):
    engine = KindraEngine()
    ctx = engine.score_all_layers("test")
    
    assert len(ctx.layer1.scores) == 2
    assert "L1_V1" in ctx.layer1.scores
    assert "L1_V2" in ctx.layer1.scores
    
    assert len(ctx.layer2.scores) == 2
    assert len(ctx.layer3.scores) == 2

def test_tw_plane_distribution_sums_to_one(mock_loaders):
    engine = KindraEngine()
    ctx = engine.score_all_layers("test")
    
    dist = ctx.tw_plane_distribution
    total = sum(dist.values())
    assert total == pytest.approx(1.0)
    assert 3 in dist
    assert 6 in dist
    assert 9 in dist

def test_delta144_weights_aggregation(mock_loaders):
    engine = KindraEngine()
    # "test" keyword triggers V1 (weight 1.0 to A01)
    # "sample" keyword triggers V2 (weight 0.5 to A04)
    # If we pass "test sample", both should trigger
    ctx = engine.score_all_layers("test sample")
    
    weights = ctx.delta144_weights
    assert "A01_CREATOR" in weights
    assert "A04_HERO" in weights
    
    # Check normalization
    total = sum(weights.values())
    assert total == pytest.approx(1.0)

def test_integration_with_core_stage_populates_kindra_context():
    # This requires mocking CoreStage dependencies
    pass 
