"""
Unit tests for Explanation Confidence (v3.4 Phase 2).

Tests confidence scoring and decision tracing for explanations.
"""
import pytest
from unittest.mock import Mock
from src.explainability.explanation_confidence import (
    ConfidenceEngine,
    ComponentConfidence,
    DecisionStep,
    ExplanationConfidence
)
from src.explainability.explanation_generator import ExplanationGenerator, Explanation
from src.unification.states.unified_state import (
    UnifiedContext,
    GlobalContext,
    ArchetypeContext,
    DriftContext,
    MetaContext,
    StoryContext,
    MultiStreamContext,
)
from src.common.unified_signal import MetaSignal


class TestExplanationConfidence:
    """Test suite for Explanation Confidence (Phase 2)."""
    
    def test_confidence_engine_basic_overall_score(self):
        """Test that confidence engine returns valid overall score."""
        engine = ConfidenceEngine()
        context = UnifiedContext(global_ctx=GlobalContext())
        
        confidence = engine.compute_from_context(context)
        
        # Verify
        assert isinstance(confidence, ExplanationConfidence)
        assert 0.0 <= confidence.overall <= 1.0
        assert isinstance(confidence.components, list)
        assert isinstance(confidence.trace, list)
    
    def test_component_confidence_includes_delta144_when_available(self):
        """Test that Delta144 component is detected when present."""
        engine = ConfidenceEngine()
        
        # Create mock delta144 state
        mock_delta144 = Mock()
        mock_delta144.state_id = "threshold"
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(delta144_state=mock_delta144)
        )
        
        confidence = engine.compute_from_context(context)
        
        # Verify delta144 component present
        component_names = [c.name for c in confidence.components]
        assert "delta144" in component_names
        
        # Get delta144 component
        delta144_comp = next(c for c in confidence.components if c.name == "delta144")
        assert delta144_comp.score > 0.5  # Should have high confidence
        assert "threshold" in delta144_comp.reason
    
    def test_component_confidence_includes_story_when_story_ctx_present(self):
        """Test that story component is detected when story context present."""
        engine = ConfidenceEngine()
        
        # Create mock story arc
        mock_arc = Mock()
        mock_arc.dominant_stage = "crossing_threshold"
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            story_ctx=StoryContext(arc=mock_arc, coherence=0.75)
        )
        
        confidence = engine.compute_from_context(context)
        
        # Verify story component present
        component_names = [c.name for c in confidence.components]
        assert "story" in component_names
    
    def test_component_confidence_penalizes_degraded_context(self):
        """Test that degraded context reduces overall confidence."""
        engine = ConfidenceEngine()
        
        # Normal context
        normal_ctx = UnifiedContext(
            global_ctx=GlobalContext(degraded=False),
            archetype_ctx=ArchetypeContext(polarity_scores={"order": 0.6})
        )
        
        # Degraded context
        degraded_ctx = UnifiedContext(
            global_ctx=GlobalContext(degraded=True),
            archetype_ctx=ArchetypeContext(polarity_scores={"order": 0.6})
        )
        
        normal_conf = engine.compute_from_context(normal_ctx)
        degraded_conf = engine.compute_from_context(degraded_ctx)
        
        # Degraded should have lower confidence
        assert degraded_conf.overall < normal_conf.overall
    
    def test_trace_contains_steps_for_available_components(self):
        """Test that decision trace includes steps for each component."""
        engine = ConfidenceEngine()
        
        # Create context with multiple components
        mock_delta144 = Mock()
        mock_delta144.state_id = "threshold"
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(
                delta144_state=mock_delta144,
                polarity_scores={"order": 0.7, "chaos": 0.3}
            )
        )
        
        confidence = engine.compute_from_context(context)
        
        # Verify trace has steps
        assert len(confidence.trace) > 0
        
        # Check for specific steps
        step_names = [s.step for s in confidence.trace]
        assert "delta144_evaluation" in step_names
        assert "polarity_balance" in step_names
    
    def test_explanation_generator_populates_confidence_field(self):
        """Test that ExplanationGenerator populates confidence."""
        generator = ExplanationGenerator()  # Default ConfidenceEngine
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(polarity_scores={"order": 0.6})
        )
        
        explanation = generator.generate(context)
        
        # Verify confidence populated
        assert explanation.confidence is not None
        assert isinstance(explanation.confidence, ExplanationConfidence)
        assert explanation.confidence.overall >= 0.0
        assert explanation.confidence.overall <= 1.0
        
        # Verify trace populated
        assert isinstance(explanation.trace, list)
        
        # Verify confidence in details
        assert "confidence" in explanation.details
        assert "overall" in explanation.details["confidence"]
    
    def test_explanation_generator_preserves_phase1_behavior_when_confidence_disabled(self):
        """Test Phase 1 behavior when confidence engine disabled."""
        generator = ExplanationGenerator(confidence_engine=None)
        
        context = UnifiedContext(global_ctx=GlobalContext())
        
        explanation = generator.generate(context)
        
        # Should still work, but no confidence
        assert isinstance(explanation, Explanation)
        assert explanation.summary is not None
        assert explanation.confidence is None  # No confidence when disabled
    
    def test_confidence_engine_handles_missing_context_fields_gracefully(self):
        """Test that confidence engine handles sparse context."""
        engine = ConfidenceEngine()
        
        # Minimal context (no archetype, story, drift, etc.)
        context = UnifiedContext(global_ctx=GlobalContext())
        
        # Should not crash
        confidence = engine.compute_from_context(context)
        
        # Should have minimal confidence
        assert isinstance(confidence, ExplanationConfidence)
        assert confidence.overall >= 0.0  # Should still be valid
        assert len(confidence.components) == 0  # No components available
    
    def test_overall_confidence_higher_when_more_components_present(self):
        """Test that richer context yields higher confidence."""
        engine = ConfidenceEngine()
        
        # Lean context
        lean_ctx = UnifiedContext(global_ctx=GlobalContext())
        
        # Rich context
        mock_delta144 = Mock()
        mock_delta144.state_id = "threshold"
        
        mock_arc = Mock()
        mock_arc.dominant_stage = "crossing_threshold"
        
        rich_ctx = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(
                delta144_state=mock_delta144,
                polarity_scores={"order": 0.7}
            ),
            story_ctx=StoryContext(arc=mock_arc, coherence=0.8),
            drift_ctx=DriftContext(regime="STABLE")
        )
        
        lean_conf = engine.compute_from_context(lean_ctx)
        rich_conf = engine.compute_from_context(rich_ctx)
        
        # Rich should have higher overall confidence
        assert rich_conf.overall > lean_conf.overall
    
    def test_trace_includes_explanation_mode_step_for_llm(self):
        """Test that trace includes explanation mode for LLM."""
        # Mock LLM
        mock_llm = Mock()
        mock_llm.generate = Mock(return_value={
            "summary": "LLM generated explanation",
            "details": {}
        })
        
        generator = ExplanationGenerator(llm=mock_llm)
        context = UnifiedContext(global_ctx=GlobalContext())
        
        explanation = generator.generate(context)
        
        # Check trace for explanation_mode step
        step_names = [s.step for s in explanation.trace]
        assert "explanation_mode" in step_names
        
        # Check that it mentions llm
        mode_step = next(s for s in explanation.trace if s.step == "explanation_mode")
        assert "llm" in mode_step.description.lower()
    
    def test_trace_includes_explanation_mode_step_for_template_fallback(self):
        """Test that trace includes template mode for template generation."""
        generator = ExplanationGenerator()  # No LLM
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(polarity_scores={"order": 0.6})
        )
        
        explanation = generator.generate(context)
        
        # Check trace for explanation_mode step
        step_names = [s.step for s in explanation.trace]
        assert "explanation_mode" in step_names
    
    def test_trace_includes_explanation_mode_step_for_barebones_fallback(self):
        """Test that trace works even with barebones explanation."""
        # Force barebones by giving broken LLM and templates
        mock_llm = Mock()
        mock_llm.generate = Mock(side_effect=Exception("LLM failed"))
        
        generator = ExplanationGenerator(llm=mock_llm, templates={})
        context = UnifiedContext(global_ctx=GlobalContext())
        
        explanation = generator.generate(context)
        
        # Should still have confidence and trace
        assert explanation.confidence is not None
        assert len(explanation.trace) > 0
        
        # Check for explanation_mode
        step_names = [s.step for s in explanation.trace]
        assert "explanation_mode" in step_names
