"""Tests for KALDRA-Alpha earnings pipeline."""

import pytest
import numpy as np
from unittest.mock import MagicMock, patch

from src.apps.alpha.earnings_pipeline import (
    run_earnings_pipeline, 
    EarningsSource, 
    EarningsPipelineResult
)
from src.core.kaldra_master_engine import KaldraMasterEngineV2

@pytest.fixture
def mock_engine():
    engine = MagicMock(spec=KaldraMasterEngineV2)
    engine.d_ctx = 16  # Small dim for testing
    
    # Mock signal response
    mock_signal = MagicMock()
    mock_signal.archetype_probs = np.ones(144) / 144.0
    mock_signal.tw_trigger = False
    mock_signal.epistemic.status = "CONFIDENT"
    mock_signal.epistemic.confidence = 0.95
    
    engine.infer_from_embedding.return_value = mock_signal
    return engine

@patch("src.apps.alpha.earnings_pipeline.load_earnings_text")
def test_run_earnings_pipeline_fallback(mock_load, mock_engine):
    # Setup
    mock_load.return_value = "  META Q1 Earnings Call...  "
    source = EarningsSource(source_type="text", path_or_url="dummy.txt", ticker="META", quarter="Q1 2025")
    
    # Run with fallback embeddings (deterministic)
    result = run_earnings_pipeline(
        source=source, 
        engine=mock_engine, 
        embedding_dim=16,
        use_fallback_embeddings=True
    )
    
    # Assertions
    assert isinstance(result, EarningsPipelineResult)
    assert result.ticker == "META"
    assert result.quarter == "Q1 2025"
    assert result.cleaned_text == "META Q1 Earnings Call..."
    
    # Check embedding shape
    assert result.embedding.shape == (16,)
    
    # Check engine call
    mock_engine.infer_from_embedding.assert_called_once()
    
    # Check metadata
    assert result.metadata["provider"] == "fallback"
    assert result.metadata["embedding_dim"] == 16
    assert result.metadata["epistemic_status"] == "CONFIDENT"

@patch("src.apps.alpha.earnings_pipeline.load_earnings_text")
def test_run_earnings_pipeline_empty_text_error(mock_load, mock_engine):
    mock_load.return_value = "   "  # Empty after normalization
    source = EarningsSource(source_type="text", path_or_url="dummy.txt")
    
    with pytest.raises(ValueError, match="Earnings text is empty"):
        run_earnings_pipeline(source, mock_engine)
