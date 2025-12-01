"""
Hardening Tests: LLM Failover.
Verifies that KindraLLMScorer falls back gracefully when LLM fails.
"""
import pytest
from unittest.mock import MagicMock
from src.kindras.kindra_llm_scorer import KindraLLMScorer

def test_llm_failure_fallback():
    # Mock a failing LLM client
    mock_llm = MagicMock()
    mock_llm.generate.side_effect = Exception("LLM Service Unavailable")
    
    # Mock a fallback scorer
    mock_fallback = MagicMock()
    mock_fallback.score.return_value = {"V01": 0.5}
    
    scorer = KindraLLMScorer(llm_client=mock_llm, rule_fallback=mock_fallback)
    
    context = {"country": "US"}
    vectors = {"V01": "Definition"}
    
    # Should not raise exception, but return fallback
    scores = scorer.score("test text", context, vectors)
    
    assert scores == {"V01": 0.5}
    mock_fallback.score.assert_called_once()

def test_llm_timeout_fallback():
    # Mock a timeout (simulated by side effect or just ensuring decorator works)
    # Since we can't easily simulate real time.sleep in a synchronous mock without slowing tests,
    # we rely on the Exception raised by the timeout decorator.
    
    from src.core.hardening.timeouts import TimeoutError
    
    mock_llm = MagicMock()
    mock_llm.generate.side_effect = TimeoutError("Timed out")
    
    mock_fallback = MagicMock()
    mock_fallback.score.return_value = {"V01": 0.1}
    
    scorer = KindraLLMScorer(llm_client=mock_llm, rule_fallback=mock_fallback)
    
    scores = scorer.score("test text", {}, {"V01": "Def"})
    assert scores == {"V01": 0.1}
