"""
Unit tests for Protobuf adapters (v3.4 Phase 3).
"""
import pytest
from src.explainability.explanation_generator import ExplanationGenerator, Explanation
from src.explainability.proto.explanation_adapters import (
    explanation_to_proto,
    explanation_from_proto
)
from src.unification.states.unified_state import UnifiedContext, GlobalContext, ArchetypeContext


class TestExplanationProtobufOutput:
    """Test suite for Protobuf conversion."""
    
    def test_explanation_to_proto_and_back_roundtrip(self):
        """Test roundtrip: Explanation -> Proto -> Dict."""
        generator = ExplanationGenerator()
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(polarity_scores={"order": 0.7})
        )
        
        explanation = generator.generate(context)
        
        # Convert to proto
        proto_msg = explanation_to_proto(explanation)
        
        # Convert back
        result_dict = explanation_from_proto(proto_msg)
        
        # Verify roundtrip
        assert result_dict["summary"] == explanation.summary
        assert "details" in result_dict
        assert "raw_facts" in result_dict
    
    def test_proto_handles_missing_confidence_and_trace(self):
        """Test protobuf without confidence/trace."""
        explanation = Explanation(
            summary="Test summary",
            details={"key": "value"},
            raw_facts={"fact": "data"}
        )
        
        # Should not crash
        proto_msg = explanation_to_proto(explanation)
        result_dict = explanation_from_proto(proto_msg)
        
        assert result_dict["summary"] == "Test summary"
        assert "details" in result_dict
    
    def test_proto_metadata_serialization(self):
        """Test metadata serialization through protobuf."""
        generator = ExplanationGenerator()
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(polarity_scores={"order": 0.7})
        )
        
        explanation = generator.generate(context)
        
        # Convert to proto and back
        proto_msg = explanation_to_proto(explanation)
        result_dict = explanation_from_proto(proto_msg)
        
        # If original had confidence with metadata, check it persisted
        if explanation.confidence and explanation.confidence.metadata:
            assert "confidence" in result_dict
