"""Tests for KALDRA-Alpha earnings analyzer."""

import pytest
import numpy as np
from unittest.mock import MagicMock

from src.apps.alpha.earnings_analyzer import (
    summarize_archetypes, 
    build_alpha_signal_payload
)
from src.apps.alpha.earnings_pipeline import EarningsPipelineResult

@pytest.fixture
def mock_result():
    # Create a mock result with a specific probability distribution
    # Index 0: 0.5, Index 1: 0.3, Index 2: 0.2, others 0
    probs = np.zeros(144)
    probs[0] = 0.5
    probs[1] = 0.3
    probs[2] = 0.2
    
    mock_signal = MagicMock()
    mock_signal.archetype_probs = probs
    mock_signal.tw_trigger = True
    mock_signal.epistemic.status = "CAUTION"
    
    return EarningsPipelineResult(
        story_id="story_123",
        ticker="AAPL",
        quarter="Q4 2024",
        raw_text="raw",
        cleaned_text="cleaned",
        embedding=np.zeros(10),
        signal=mock_signal,
        metadata={"provider": "test"}
    )

def test_summarize_archetypes_returns_top_k(mock_result):
    summary = summarize_archetypes(mock_result, top_k=3)
    
    assert len(summary["top_indices"]) == 3
    assert len(summary["top_probs"]) == 3
    
    # Check specific values
    assert summary["top_indices"][0] == 0
    assert summary["top_probs"][0] == 0.5
    
    # Entropy should be positive
    assert summary["entropy"] > 0.0

def test_build_alpha_signal_payload(mock_result):
    payload = build_alpha_signal_payload(mock_result)
    
    assert payload["ticker"] == "AAPL"
    assert payload["quarter"] == "Q4 2024"
    assert payload["tw_trigger"] is True
    assert payload["epistemic_status"] == "CAUTION"
    assert len(payload["top_archetypes"]) == 5  # Default top_k is 5
    assert payload["narrative_coherence"] is None
    assert payload["metadata"]["provider"] == "test"
