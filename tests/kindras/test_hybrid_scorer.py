"""
Unit tests for Kindra Hybrid Scoring.
"""

import pytest
from src.kindras.kindra_hybrid_scorer import KindraHybridScorer


class DummyLLMScorer:
    """Mock LLM scorer for testing."""
    
    def score(self, text, context, vectors):
        """Return all 1.0 scores."""
        return {k: 1.0 for k in vectors}


class DummyRuleScorer:
    """Mock rule-based scorer for testing."""
    
    def score(self, context, vectors):
        """Return all -1.0 scores."""
        return {k: -1.0 for k in vectors}


class TestKindraHybridScorer:
    def test_hybrid_mixing_global_alpha_05(self):
        """Test hybrid mixing with alpha=0.5 (equal mix)."""
        vectors = {"E01": {}, "T25": {}}
        scorer = KindraHybridScorer(
            DummyLLMScorer(),
            DummyRuleScorer(),
            alpha_global=0.5
        )
        
        out = scorer.score("text", {}, vectors)
        
        # 0.5 * 1.0 + 0.5 * (-1.0) = 0.0
        assert out["E01"] == 0.0
        assert out["T25"] == 0.0

    def test_hybrid_mixing_alpha_0(self):
        """Test hybrid mixing with alpha=0 (pure rule-based)."""
        vectors = {"E01": {}}
        scorer = KindraHybridScorer(
            DummyLLMScorer(),
            DummyRuleScorer(),
            alpha_global=0.0
        )
        
        out = scorer.score("text", {}, vectors)
        
        # 0.0 * 1.0 + 1.0 * (-1.0) = -1.0
        assert out["E01"] == -1.0

    def test_hybrid_mixing_alpha_1(self):
        """Test hybrid mixing with alpha=1 (pure LLM)."""
        vectors = {"E01": {}}
        scorer = KindraHybridScorer(
            DummyLLMScorer(),
            DummyRuleScorer(),
            alpha_global=1.0
        )
        
        out = scorer.score("text", {}, vectors)
        
        # 1.0 * 1.0 + 0.0 * (-1.0) = 1.0
        assert out["E01"] == 1.0

    def test_hybrid_mixing_layer_override(self):
        """Test layer-specific alpha override."""
        vectors = {"E01": {}}
        scorer = KindraHybridScorer(
            DummyLLMScorer(),
            DummyRuleScorer(),
            alpha_global=0.0,
            alpha_layers={"1": 1.0}
        )
        
        # Layer 1 should use alpha=1.0 (pure LLM)
        out = scorer.score("text", {"kindra_layer": 1}, vectors)
        assert out["E01"] == 1.0
        
        # Layer 2 should use alpha_global=0.0 (pure rule)
        out2 = scorer.score("text", {"kindra_layer": 2}, vectors)
        assert out2["E01"] == -1.0

    def test_hybrid_clamping(self):
        """Test that scores are clamped to [-1, 1]."""
        
        class ExtremeLLM:
            def score(self, text, context, vectors):
                return {k: 10.0 for k in vectors}
        
        class ExtremeRule:
            def score(self, context, vectors):
                return {k: -10.0 for k in vectors}
        
        vectors = {"E01": {}}
        scorer = KindraHybridScorer(
            ExtremeLLM(),
            ExtremeRule(),
            alpha_global=0.5
        )
        
        out = scorer.score("text", {}, vectors)
        
        # 0.5 * 10 + 0.5 * (-10) = 0, which is in range
        assert -1.0 <= out["E01"] <= 1.0

    def test_hybrid_multiple_vectors(self):
        """Test hybrid scoring with multiple vectors."""
        vectors = {"E01": {}, "T25": {}, "P17": {}}
        scorer = KindraHybridScorer(
            DummyLLMScorer(),
            DummyRuleScorer(),
            alpha_global=0.7
        )
        
        out = scorer.score("text", {}, vectors)
        
        # All vectors should be scored
        assert set(out.keys()) == {"E01", "T25", "P17"}
        
        # All should have same value: 0.7 * 1.0 + 0.3 * (-1.0) = 0.4
        expected = 0.7 * 1.0 + 0.3 * (-1.0)
        for v in out.values():
            assert abs(v - expected) < 1e-6
