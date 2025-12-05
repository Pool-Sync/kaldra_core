"""
Unit tests for Markdown output (v3.4 Phase 3).
"""
import pytest
from src.explainability.explanation_generator import ExplanationGenerator, Explanation
from src.explainability.explanation_output import ExplanationMarkdownRenderer
from src.unification.states.unified_state import UnifiedContext, GlobalContext, ArchetypeContext


class TestExplanationMarkdownOutput:
    """Test suite for Markdown rendering."""
    
    def test_markdown_renderer_basic(self):
        """Test basic Markdown rendering."""
        generator = ExplanationGenerator()
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(polarity_scores={"order": 0.7})
        )
        
        explanation = generator.generate(context)
        markdown = explanation.to_markdown()
        
        # Verify output
        assert isinstance(markdown, str)
        assert len(markdown) > 0
        assert "Explanation" in markdown or "explanation" in markdown.lower()
    
    def test_markdown_includes_summary_and_confidence(self):
        """Test that Markdown includes summary and confidence."""
        generator = ExplanationGenerator()
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(polarity_scores={"order": 0.7})
        )
        
        explanation = generator.generate(context)
        markdown = explanation.to_markdown(variant="default")
        
        # Check for summary
        assert explanation.summary in markdown or "summary" in markdown.lower()
        
        # Check for confidence
        if explanation.confidence:
            assert "confidence" in markdown.lower() or "Confidence" in markdown
    
    def test_markdown_handles_missing_confidence(self):
        """Test that Markdown works without confidence."""
        # Create explanation without confidence
        explanation = Explanation(
            summary="Test summary",
            details={"test": "data"},
            raw_facts={}
        )
        
        # Should not crash
        markdown = explanation.to_markdown()
        
        assert isinstance(markdown, str)
        assert "Test summary" in markdown
