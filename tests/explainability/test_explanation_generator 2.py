"""
Unit tests for ExplanationGenerator.

Tests v3.4 Phase 1 explanation generation with LLM, template, and barebones fallback.
"""
import pytest
from unittest.mock import Mock, MagicMock
from src.explainability.explanation_generator import ExplanationGenerator, Explanation
from src.unification.states.unified_state import (
    UnifiedContext,
    GlobalContext,
    ArchetypeContext,
    DriftContext,
    MetaContext,
)
from src.common.unified_signal import MetaSignal


class TestExplanationGenerator:
    """Test suite for ExplanationGenerator."""
    
    def test_generate_basic_explanation(self):
        """Test that generator returns valid text explanation."""
        generator = ExplanationGenerator()
        
        # Create minimal context
        context = UnifiedContext(global_ctx=GlobalContext())
        
        # Generate explanation
        explanation = generator.generate(context)
        
        # Verify
        assert isinstance(explanation, Explanation)
        assert isinstance(explanation.summary, str)
        assert len(explanation.summary) > 0
        assert isinstance(explanation.details, dict)
        assert isinstance(explanation.raw_facts, dict)
    
    def test_generate_uses_llm_when_available(self):
        """Test that LLM is called when available."""
        # Mock LLM
        mock_llm = Mock()
        mock_llm.generate = Mock(return_value={
            "summary": "LLM generated summary",
            "details": {"key": "value"}
        })
        
        generator = ExplanationGenerator(llm=mock_llm)
        context = UnifiedContext(global_ctx=GlobalContext())
        
        # Generate
        explanation = generator.generate(context)
        
        # Verify LLM was called
        assert mock_llm.generate.called
        assert "LLM generated summary" in explanation.summary
    
    def test_generate_fallback_on_llm_error(self):
        """Test that generator falls back to template when LLM fails."""
        # Mock LLM that raises exception
        mock_llm = Mock()
        mock_llm.generate = Mock(side_effect=Exception("LLM API error"))
        
        generator = ExplanationGenerator(llm=mock_llm)
        context = UnifiedContext(global_ctx=GlobalContext())
        
        # Generate - should not raise exception
        explanation = generator.generate(context)
        
        # Verify fallback worked
        assert isinstance(explanation, Explanation)
        assert len(explanation.summary) > 0
        # Should be template-based, not LLM
        assert "LLM generated" not in explanation.summary
    
    def test_template_fallback_generates_required_sections(self):
        """Test that template fallback includes all required sections."""
        generator = ExplanationGenerator()  # No LLM
        
        # Create context with some data
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(
                polarity_scores={"order": 0.6, "chaos": 0.4}
            )
        )
        
        # Generate
        explanation = generator.generate(context)
        
        # Verify sections present
        assert "drivers" in explanation.details
        assert "archetypes" in explanation.details
        assert "polarities" in explanation.details
        assert "narrative" in explanation.details
    
    def test_explanation_has_summary_field(self):
        """Test that all explanations have a summary field."""
        generator = ExplanationGenerator()
        context = UnifiedContext(global_ctx=GlobalContext())
        
        explanation = generator.generate(context)
        
        assert hasattr(explanation, 'summary')
        assert isinstance(explanation.summary, str)
        assert len(explanation.summary) > 0
    
    def test_generator_extracts_archetype_data(self):
        """Test that generator extracts archetype data from context."""
        generator = ExplanationGenerator()
        
        # Create context with archetype data
        from src.archetypes.delta12_vector import Delta12Vector
        
        delta12 = Delta12Vector()
        delta12.hero = 0.8
        delta12.sage = 0.3
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(delta12=delta12)
        )
        
        # Explanation = generator.generate(context)
        
        # Verify archetypal data extracted
        facts = generator._extract_facts(context)
        assert "archetypes" in facts
        assert len(facts["archetypes"]) > 0
    
    def test_generator_extracts_polarity_data(self):
        """Test that generator extracts polarity data."""
        generator = ExplanationGenerator()
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(
                polarity_scores={"order": 0.7, "chaos": 0.3}
            )
        )
        
        # Extract facts
        facts = generator._extract_facts(context)
        
        # Verify
        assert "polarities" in facts
        assert facts["polarities"]["order"] == 0.7
        assert facts["polarities"]["chaos"] == 0.3
    
    def test_generator_extracts_journey_stage_if_present(self):
        """Test that generator extracts journey stage from CampbellEngine."""
        generator = ExplanationGenerator()
        
        # Create context with Campbell meta signal
        campbell_signal = MetaSignal(
            name="Campbell",
            score=0.75,
            label="Crossing the Threshold"
        )
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            meta_ctx=MetaContext(campbell=campbell_signal)
        )
        
        # Extract facts
        facts = generator._extract_facts(context)
        
        # Verify
        assert "journey_stage" in facts
        assert facts["journey_stage"] == "Crossing the Threshold"
    
    def test_generator_accepts_unifiedcontext_minimal(self):
        """Test that generator works with minimal UnifiedContext."""
        generator = ExplanationGenerator()
        
        # Minimal context (only global_ctx)
        context = UnifiedContext(global_ctx=GlobalContext())
        
        # Generate - should not raise exception
        explanation = generator.generate(context)
        
        # Verify barebones explanation works
        assert isinstance(explanation, Explanation)
        assert len(explanation.summary) > 0
    
    def test_graceful_degradation_on_invalid_signal(self):
        """Test that generator degrades gracefully on invalid/malformed context."""
        generator = ExplanationGenerator()
        
        # Invalid context (None archetype_ctx with nested access)
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=None  # Explicitly None
        )
        
        # Extract facts - should not crash
        facts = generator._extract_facts(context)
        
        # Generate - should not crash
        explanation = generator.generate(context)
        
        # Verify barebones fallback worked
        assert isinstance(explanation, Explanation)
        assert len(explanation.summary) > 0
        
        # Should still have basic structure
        assert "polarities" in facts
        assert "archetypes" in facts
