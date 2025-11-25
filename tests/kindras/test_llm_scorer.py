"""
Unit tests for Kindra LLM-based scoring.
"""

import pytest
from src.kindras.kindra_llm_scorer import KindraLLMScorer


class DummyLLM:
    """Mock LLM client for testing."""
    
    def generate(self, prompt):
        """Return mock scores."""
        return {"scores": {"E01": 0.8, "T25": -0.1}}


class DummyRuleFallback:
    """Mock rule-based fallback."""
    
    def score(self, context, vectors):
        """Return fallback scores."""
        return {k: 0.5 for k in vectors.keys()}


class TestKindraLLMScorer:
    def test_llm_scorer_basic(self):
        """Test basic LLM scoring functionality."""
        scorer = KindraLLMScorer(llm_client=DummyLLM(), rule_fallback=None)
        vectors = {"E01": {}, "T25": {}}
        context = {"country": "BR", "sector": "Tech"}
        
        out = scorer.score("texto de teste", context, vectors)
        
        assert out["E01"] == 0.8
        assert out["T25"] == -0.1

    def test_llm_scorer_clamp(self):
        """Test score clamping to [-1, 1]."""
        
        class ExtremeScoreLLM:
            def generate(self, prompt):
                return {"scores": {"E01": 5.0, "T25": -3.0}}
        
        scorer = KindraLLMScorer(llm_client=ExtremeScoreLLM(), rule_fallback=None)
        vectors = {"E01": {}, "T25": {}}
        context = {"country": "US"}
        
        out = scorer.score("test text", context, vectors)
        
        # Should be clamped to [-1, 1]
        assert out["E01"] == 1.0
        assert out["T25"] == -1.0

    def test_llm_scorer_fallback_when_no_llm(self):
        """Test fallback to rule-based when LLM unavailable."""
        fallback = DummyRuleFallback()
        scorer = KindraLLMScorer(llm_client=None, rule_fallback=fallback)
        vectors = {"E01": {}, "T25": {}, "P17": {}}
        context = {"country": "BR"}
        
        out = scorer.score("texto", context, vectors)
        
        # Should use fallback
        assert out["E01"] == 0.5
        assert out["T25"] == 0.5
        assert out["P17"] == 0.5

    def test_llm_scorer_fallback_on_error(self):
        """Test fallback when LLM raises error."""
        
        class ErrorLLM:
            def generate(self, prompt):
                raise Exception("LLM error")
        
        fallback = DummyRuleFallback()
        scorer = KindraLLMScorer(llm_client=ErrorLLM(), rule_fallback=fallback)
        vectors = {"E01": {}, "T25": {}}
        context = {"country": "US"}
        
        out = scorer.score("test", context, vectors)
        
        # Should fallback
        assert out["E01"] == 0.5
        assert out["T25"] == 0.5

    def test_llm_scorer_parse_scores(self):
        """Test score parsing from LLM response."""
        scorer = KindraLLMScorer(llm_client=DummyLLM(), rule_fallback=None)
        vectors = {"E01": {}, "T25": {}, "P17": {}}
        
        response = {"scores": {"E01": 0.8, "T25": -0.1}}
        parsed = scorer._parse_scores(response, vectors)
        
        assert parsed["E01"] == 0.8
        assert parsed["T25"] == -0.1
        assert parsed["P17"] == 0.0  # Missing vector gets 0.0

    def test_llm_scorer_output_format_compatibility(self):
        """Test that output format matches rule-based scorer."""
        scorer = KindraLLMScorer(llm_client=DummyLLM(), rule_fallback=None)
        vectors = {"E01": {}, "T25": {}}
        context = {"country": "BR"}
        
        out = scorer.score("texto", context, vectors)
        
        # Check output format
        assert isinstance(out, dict)
        assert set(out.keys()) == set(vectors.keys())
        assert all(isinstance(v, float) for v in out.values())
        assert all(-1.0 <= v <= 1.0 for v in out.values())
