"""
Unit tests for CampbellEngine Temporal v3.2.

Tests temporal analysis capabilities:
- Journey sequence inference from StoryContext
- Arc completeness measurement
- Temporal coherence scoring
- Drift coupling with turning points
- Δ144 alignment with journey stages
- Backward compatibility  with v3.1
"""

import pytest
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.meta.campbell_engine import CampbellEngine, CampbellSignal
from src.meta.types import MetaInput
from src.unification.states.unified_state import DriftContext, StoryContext, DriftPoint, TurningPoint


# Mock classes for testing
@dataclass
class MockStoryArc:
    """Mock StoryArc for testing."""
    dominant_stage: str
    stage_scores: Dict[str, float] = field(default_factory=dict)


@dataclass
class MockCoherenceScore:
    """Mock CoherenceScore for testing."""
    overall: float


class TestBackwardCompatibility:
    """Test that v3.2 maintains full v3.1 compatibility."""
    
    def test_analyze_without_temporal_contexts(self):
        """MetaInput without story_ctx/drift_ctx should work identically to v3.1."""
        engine = CampbellEngine()
        
        # v3.1-style input
        meta_input = MetaInput(
            text="A young hero receives a mysterious call to adventure.",
            delta144_state="A04_HERO",
            archetype_scores={"A04_HERO": 0.8}
        )
        
        signal = engine.analyze(meta_input)
        
        # Should have v3.1 fields
        assert signal.journey_stage in ["CALL_TO_ADVENTURE", "ORDINARY_WORLD", "MEETING_MENTOR"]
        assert signal.mythic_resonance >= 0.0
        assert signal.transformation_potential >= 0.0
        
        # v3.2 temporal fields should be defaults
        assert signal.journey_sequence == []
        assert signal.temporal_coherence == 0.0
        assert signal.arc_completeness == 0.0
        assert signal.drift_coupling == 0.0
        assert signal.delta144_alignment == 0.0
    
    def test_signal_fields_are_clamped(self):
        """All score fields should be clamped to [0, 1]."""
        engine = CampbellEngine()
        
        signal = CampbellSignal(
            journey_stage="ORDEAL",
            temporal_coherence=1.5,  # Over 1.0
            arc_completeness=-0.2,   # Below 0.0
        )
        
        # __post_init__ should clamp
        assert 0.0 <= signal.temporal_coherence <= 1.0
        assert 0.0 <= signal.arc_completeness <= 1.0


class TestJourneySequenceInference:
    """Test _infer_journey_sequence_from_story()."""
    
    def test_sequence_from_story_arc(self):
        """Should extract journey sequence from StoryContext.arc.stage_scores."""
        engine = CampbellEngine()
        
        # Create StoryContext with arc
        arc = MockStoryArc(
            dominant_stage="ORDEAL",
            stage_scores={
                "CALL_TO_ADVENTURE": 0.8,
                "MEETING_MENTOR": 0.6,
                "ORDEAL": 0.9,
                "ORDINARY_WORLD": 0.05  # Below threshold
            }
        )
        
        story_ctx = StoryContext(arc=arc)
        story_ctx.metadata = {}
        
        meta_input = MetaInput(
            text="Journey progression",
            story_ctx=story_ctx
        )
        
        signal = engine.analyze(meta_input)
        
        # Should have sequence with stages > 0.1 threshold
        assert len(signal.journey_sequence) > 0
        assert "ORDEAL" in signal.journey_sequence
        assert "CALL_TO_ADVENTURE" in signal.journey_sequence
        assert "ORDINARY_WORLD" not in signal.journey_sequence  # Below threshold
    
    def test_empty_sequence_without_story_ctx(self):
        """Should return empty sequence if no StoryContext."""
        engine = CampbellEngine()
        
        meta_input = MetaInput(text="No story context")
        signal = engine.analyze(meta_input)
        
        assert signal.journey_sequence == []


class TestArcCompleteness:
    """Test _measure_transformation_arc()."""
    
    def test_early_stage_low_completeness(self):
        """Early stages should have low arc_completeness."""
        engine = CampbellEngine()
        
        arc = MockStoryArc(
            dominant_stage="ORDINARY_WORLD",
            stage_scores={"ORDINARY_WORLD": 0.9}
        )
        
        story_ctx = StoryContext(arc=arc)
        story_ctx.metadata = {}
        
        meta_input = MetaInput(
            text="Stuck in ordinary world",
            story_ctx=story_ctx
        )
        
        signal = engine.analyze(meta_input)
        
        # Early stage = low completeness
        assert signal.arc_completeness < 0.4
    
    def test_late_stage_high_completeness(self):
        """Late stages should have high arc_completeness."""
        engine = CampbellEngine()
        
        arc = MockStoryArc(
            dominant_stage="RETURN_WITH_ELIXIR",
            stage_scores={"RETURN_WITH_ELIXIR": 0.9}
        )
        
        story_ctx = StoryContext(arc=arc, metadata={})
        
        meta_input = MetaInput(
            text="Hero returns transformed",
            story_ctx=story_ctx
        )
        
        signal = engine.analyze(meta_input)
        
        # Late stage = high completeness
        assert signal.arc_completeness > 0.7
    
    def test_delta144_evolution_boosts_completeness(self):
        """Δ144 archetype evolution should boost arc_completeness."""
        engine = CampbellEngine()
        
        arc = MockStoryArc(
            dominant_stage="RESURRECTION",
            stage_scores={"RESURRECTION": 0.8}
        )
        
        # Δ144 timeline showing evolution
        delta144_timeline = [
            {"t": 1000, "state_id": "A10_INNOCENT", "weight": 0.9},
            {"t": 2000, "state_id": "A04_HERO", "weight": 0.8},
            {"t": 3000, "state_id": "A02_SAGE", "weight": 0.85}
        ]
        
        story_ctx = StoryContext(
            arc=arc,
            metadata={"delta144_timeline": delta144_timeline}
        )
        
        meta_input = MetaInput(
            text="Complete transformation", 
            story_ctx=story_ctx
        )
        
        signal = engine.analyze(meta_input)
        
        # Should have boost from evolution
        assert signal.arc_completeness > 0.8


class TestTemporalCoherence:
    """Test _compute_temporal_coherence()."""
    
    def test_uses_coherence_score(self):
        """Should use StoryContext.coherence if available."""
        engine = CampbellEngine()
        
        coherence_obj = MockCoherenceScore(overall=0.85)
        story_ctx = StoryContext(coherence=coherence_obj, metadata={})  # Pass as object
        
        meta_input = MetaInput(
            text="Coherent narrative",
            story_ctx=story_ctx
        )
        
        signal = engine.analyze(meta_input)
        
        # Should use coherence.overall
        assert abs(signal.temporal_coherence - 0.85) < 0.01
    
    def test_uses_float_coherence(self):
        """Should handle coherence as direct float."""
        engine = CampbellEngine()
        
        story_ctx = StoryContext(coherence=0.72, metadata={})
        
        meta_input = MetaInput(
            text="Moderately coherent",
            story_ctx=story_ctx
        )
        
        signal = engine.analyze(meta_input)
        
        assert abs(signal.temporal_coherence - 0.72) < 0.01


class TestDriftCoupling:
    """Test _compute_drift_coupling()."""
    
    def test_coupling_with_aligned_turning_points(self):
        """Turning points during critical stages should yield high coupling."""
        engine = CampbellEngine()
        
        # DriftContext with turning points
        drift_ctx = DriftContext(
            regime="VOLATILE",
            drift_metric=0.7,
            turning_points=[
                TurningPoint(timestamp=1000.0, from_regime="STABLE", to_regime="VOLATILE", reason="spike"),
                TurningPoint(timestamp=2000.0, from_regime="VOLATILE", to_regime="CRITICAL", reason="escalation")
            ]
        )
        
        # StoryContext with critical stages
        arc = MockStoryArc(
            dominant_stage="ORDEAL",
            stage_scores={
                "ORDEAL": 0.9,
                "RESURRECTION": 0.7,
                "CROSSING_THRESHOLD": 0.6
            }
        )
        
        story_ctx = StoryContext(arc=arc, metadata={})
        
        meta_input = MetaInput(
            text="Crisis and transformation",
            drift_ctx=drift_ctx,
            story_ctx=story_ctx
        )
        
        signal = engine.analyze(meta_input)
        
        # Should detect alignment
        assert signal.drift_coupling > 0.3
    
    def test_no_coupling_without_critical_stages(self):
        """No critical stages should yield low coupling."""
        engine = CampbellEngine()
        
        drift_ctx = DriftContext(
            turning_points=[
                TurningPoint(timestamp=1000.0, from_regime="STABLE", to_regime="VOLATILE", reason="test")
            ]
        )
        
        # Only early stages
        arc = MockStoryArc(
            dominant_stage="ORDINARY_WORLD",
            stage_scores={"ORDINARY_WORLD": 0.9}
        )
        
        story_ctx = StoryContext(arc=arc, metadata={})
        
        meta_input = MetaInput(
            text="No critical stages",
            drift_ctx=drift_ctx,
            story_ctx=story_ctx
        )
        
        signal = engine.analyze(meta_input)
        
        # Low coupling without critical stages
        assert signal.drift_coupling < 0.3


class TestDelta144Alignment:
    """Test _compute_delta144_alignment()."""
    
    def test_alignment_with_matching_archetypes(self):
        """Matching archetypes should yield high alignment."""
        engine = CampbellEngine()
        
        # Δ144 timeline with expected archetypes
        delta144_timeline = [
            {"t": 1000, "state_id": "A04_HERO", "weight": 0.9},
            {"t": 2000, "state_id": "A02_SAGE", "weight": 0.8}
        ]
        
        # Journey sequence with matching expectations
        arc = MockStoryArc(
            dominant_stage="ORDEAL",
            stage_scores={
                "CALL_TO_ADVENTURE": 0.7,  # Expects HERO
                "ORDEAL": 0.9,              # Expects HERO/REBEL
                "RETURN_WITH_ELIXIR": 0.6   # Expects SAGE
            }
        )
        
        story_ctx = StoryContext(
            arc=arc,
            metadata={"delta144_timeline": delta144_timeline}
        )
        
        meta_input = MetaInput(
            text="Hero's journey with sage return",
            story_ctx=story_ctx
        )
        
        signal = engine.analyze(meta_input)
        
        # Should have good alignment
        assert signal.delta144_alignment > 0.4


class TestGracefulDegradation:
    """Test error handling and graceful degradation."""
    
    def test_partial_contexts_dont_break(self):
        """Only drift_ctx (no story_ctx) should not raise exception."""
        engine = CampbellEngine()
        
        drift_ctx = DriftContext(
            regime="STABLE",
            drift_metric=0.3
        )
        
        meta_input = MetaInput(
            text="Partial context",
            drift_ctx=drift_ctx
            # no story_ctx
        )
        
        # Should not raise
        signal = engine.analyze(meta_input)
        
        assert signal.journey_stage is not None
        # Drift coupling calculated even without journey_sequence
        assert isinstance(signal.drift_coupling, float)
    
    def test_malformed_story_ctx_logged_not_raised(self):
        """Malformed StoryContext should log warning but not crash."""
        engine = CampbellEngine()
        
        # Intentionally broken story_ctx
        story_ctx = StoryContext(metadata={})
        story_ctx.arc = "not_a_valid_arc"  # Wrong type
        
        meta_input = MetaInput(
            text="Broken context",
            story_ctx=story_ctx
        )
        
        # Should gracefully degrade
        signal = engine.analyze(meta_input)
        
        # Should still have basic signal
        assert signal.journey_stage is not None
        # Temporal fields should be defaults (degraded)
        assert isinstance(signal.temporal_coherence, float)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
