"""
Integration tests for CoreStage with KindraEngine (v3.1).
"""
import pytest
from unittest.mock import MagicMock, patch
import numpy as np

from src.unification.pipeline.core_stage import CoreStage
from src.unification.states.unified_state import (
    UnifiedContext, InputContext, KindraContext, ArchetypeContext
)
from src.kindras.kindra_engine import KindraEngine

@pytest.fixture
def mock_registry():
    registry = MagicMock()
    # Mock Archetypes engine (Delta144)
    mock_delta144 = MagicMock()
    mock_delta144.infer_from_vector.return_value = MagicMock(
        state=MagicMock(id="A04_HERO_STATE_01", archetype_id="A04_HERO"),
        archetype=MagicMock(label="Hero"),
        polarity_scores={}
    )
    mock_delta144.compute_delta12.return_value = MagicMock(scores={})
    registry.get.side_effect = lambda name: mock_delta144 if name == "archetypes" else None
    return registry

@pytest.fixture
def mock_context():
    ctx = UnifiedContext()
    ctx.input_ctx = InputContext(
        text="Heroic journey",
        embedding=np.zeros(1536) # Mock embedding
    )
    return ctx

def test_core_stage_integrates_kindra_engine(mock_registry, mock_context):
    """Test that CoreStage calls KindraEngine and populates context."""
    
    # Mock KindraEngine
    mock_kindra = MagicMock(spec=KindraEngine)
    expected_kindra_ctx = KindraContext(
        layer1={"L1_V1": 0.9},
        metadata={"engine": "MockKindra"}
    )
    mock_kindra.score_all_layers.return_value = expected_kindra_ctx
    
    # Store the mocks to avoid recursion
    mock_delta144 = mock_registry.get("archetypes")
    
    # Configure registry to return stored mocks
    def registry_get(name):
        if name == "archetypes":
            return mock_delta144
        if name == "kindra":
            return mock_kindra
        return None
    mock_registry.get.side_effect = registry_get
    
    # Initialize stage
    stage = CoreStage(registry=mock_registry)
    
    # Execute
    result_ctx = stage.execute(mock_context)
    
    # Verify KindraEngine was called
    mock_kindra.score_all_layers.assert_called_once()
    call_args = mock_kindra.score_all_layers.call_args
    assert call_args.kwargs['text'] == "Heroic journey"
    assert call_args.kwargs['embedding'] is not None
    
    # Verify Context Population
    assert result_ctx.kindra_ctx is not None
    assert result_ctx.kindra_ctx == expected_kindra_ctx
    assert result_ctx.kindra_ctx.layer1["L1_V1"] == 0.9

def test_core_stage_fallback_instantiation(mock_registry, mock_context):
    """Test that CoreStage instantiates KindraEngine if not in registry."""
    # Store the mock delta144 to avoid recursion
    mock_delta144 = mock_registry.get("archetypes")
    
    # Registry returns None for 'kindra'
    mock_registry.get.side_effect = lambda name: mock_delta144 if name == "archetypes" else None
    
    with patch('src.unification.pipeline.core_stage.KindraEngine') as MockKindraClass:
        stage = CoreStage(registry=mock_registry)
        
        # Verify it instantiated a new KindraEngine
        MockKindraClass.assert_called_once()
        assert stage.kindra_engine == MockKindraClass.return_value
