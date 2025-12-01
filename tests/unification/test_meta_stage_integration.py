"""
Integration tests for MetaStage (v3.1).

Verifies:
- Integration of Nietzsche, Aurelius, and Campbell engines
- MetaInput construction from UnifiedContext
- Graceful degradation on engine failure
- MetaContext population
"""

import pytest
from unittest.mock import MagicMock, patch
from src.unification.pipeline.meta_stage import MetaStage
from src.unification.states.unified_state import (
    UnifiedContext, InputContext, ArchetypeContext, MetaContext, KindraContext, DriftContext
)
from src.tw369.tw369_integration import TWState

# Import Signals
from src.meta.nietzsche import NietzscheSignal
from src.meta.aurelius import AureliusSignal
from src.meta.campbell_engine import CampbellSignal


@pytest.fixture
def mock_context():
    """Create a populated UnifiedContext for testing."""
    ctx = UnifiedContext()
    ctx.input_ctx = InputContext(text="The hero faces a crisis of morality.")
    
    # Mock Archetype Context
    ctx.archetype_ctx = ArchetypeContext()
    # Mock delta12 with scores attribute
    mock_delta12 = MagicMock()
    mock_delta12.scores = {"A04_HERO": 0.8, "A08_REBEL": 0.2}
    ctx.archetype_ctx.delta12 = mock_delta12
    
    # Mock delta144_state with id
    mock_state = MagicMock()
    mock_state.id = "A04_HERO_STATE_01"
    ctx.archetype_ctx.delta144_state = mock_state
    
    ctx.archetype_ctx.polarity_scores = {"positive": 0.6}
    ctx.archetype_ctx.modifier_scores = {"intensity": 1.2}

    # Mock Kindra Context
    ctx.kindra_ctx = KindraContext(
        layer1={"order": 0.5},
        layer2={"intensity": 0.8},
        layer3={"myth": 0.9}
    )
    
    # Mock Drift Context (which contains TWState)
    tw_state = TWState(metadata={"drift_metric": 0.5, "regime": "STABLE"})
    ctx.drift_ctx = DriftContext(
        tw_state=tw_state,
        drift_state=MagicMock(),
        regime="STABLE",
        drift_metric=0.5
    )
    
    return ctx


def test_meta_stage_runs_without_error(mock_context):
    """Test that MetaStage executes without crashing."""
    mock_registry = MagicMock()
    mock_registry.get.return_value = None # Trigger fallback to real engines
    stage = MetaStage(registry=mock_registry)
    result_ctx = stage.execute(mock_context)
    
    assert isinstance(result_ctx, UnifiedContext)
    assert isinstance(result_ctx.meta_ctx, MetaContext)


def test_meta_stage_populates_all_three_signals(mock_context):
    """Test that all three engines produce signals."""
    mock_registry = MagicMock()
    mock_registry.get.return_value = None
    stage = MetaStage(registry=mock_registry)
    result_ctx = stage.execute(mock_context)
    
    meta = result_ctx.meta_ctx
    
    # Nietzsche
    assert meta.nietzsche is not None
    assert isinstance(meta.nietzsche, NietzscheSignal)
    assert meta.nietzsche.name == "nietzsche"
    
    # Aurelius
    assert meta.aurelius is not None
    assert isinstance(meta.aurelius, AureliusSignal)
    assert meta.aurelius.name == "aurelius"
    
    # Campbell
    assert meta.campbell is not None
    assert isinstance(meta.campbell, CampbellSignal)
    assert meta.campbell.name == "campbell"


def test_degradation_when_one_engine_fails(mock_context):
    """Test that stage continues if one engine raises an exception."""
    mock_registry = MagicMock()
    mock_registry.get.return_value = None
    stage = MetaStage(registry=mock_registry)
    
    # Mock NietzscheEngine to fail
    with patch("src.meta.nietzsche.NietzscheEngine.analyze", side_effect=Exception("Boom")):
        result_ctx = stage.execute(mock_context)
        
        # Nietzsche should be None (failed)
        assert result_ctx.meta_ctx.nietzsche is None
        
        # Others should still work
        assert result_ctx.meta_ctx.aurelius is not None
        assert result_ctx.meta_ctx.campbell is not None


def test_meta_stage_integrates_with_unified_context(mock_context):
    """Test that inputs from UnifiedContext are correctly passed to engines."""
    mock_registry = MagicMock()
    mock_registry.get.return_value = None
    stage = MetaStage(registry=mock_registry)
    
    # Spy on CampbellEngine to check input
    with patch("src.meta.campbell_engine.CampbellEngine.analyze") as mock_analyze:
        # Setup return value so it doesn't crash
        mock_analyze.return_value = CampbellSignal(journey_stage="ORDEAL")
        
        stage.execute(mock_context)
        
        # Check arguments passed to analyze
        args, _ = mock_analyze.call_args
        meta_input = args[0]
        
        assert meta_input.text == "The hero faces a crisis of morality."
        assert meta_input.delta144_state == "A04_HERO_STATE_01"
        assert meta_input.kindra is not None
        assert meta_input.tw_state is not None


def test_meta_stage_returns_meta_context_instance(mock_context):
    """Verify the type of the returned context."""
    mock_registry = MagicMock()
    mock_registry.get.return_value = None
    stage = MetaStage(registry=mock_registry)
    result = stage.execute(mock_context)
    assert isinstance(result.meta_ctx, MetaContext)
