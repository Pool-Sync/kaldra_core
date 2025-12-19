"""
Unit tests for GraphQL types and adapters (v3.4 Phase 3).
"""
import pytest
from unittest.mock import Mock

# Check if graphene is available
try:
    import graphene
    GRAPHENE_AVAILABLE = True
except ImportError:
    GRAPHENE_AVAILABLE = False

pytestmark = pytest.mark.skipif(not GRAPHENE_AVAILABLE, reason="graphene not installed")

from src.explainability.explanation_generator import ExplanationGenerator, Explanation
from src.api.graphql.resolvers.explainability_resolvers import explanation_to_graphql
from src.unification.states.unified_state import UnifiedContext, GlobalContext, ArchetypeContext


class TestExplanationGraphQLOutput:
    """Test suite for GraphQL type mapping."""
    
    def test_graphql_types_mapping_from_explanation(self):
        """Test GraphQL type mapping from Explanation."""
        generator = ExplanationGenerator()
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(polarity_scores={"order": 0.7})
        )
        
        explanation = generator.generate(context)
        graphql_data = explanation_to_graphql(explanation)
        
        # Verify mapping
        assert "summary" in graphql_data
        assert graphql_data["summary"] == explanation.summary
        assert "details" in graphql_data
        assert "raw_facts" in graphql_data
    
    def test_graphql_confidence_optional(self):
        """Test that GraphQL handles optional confidence."""
        # Explanation without confidence
        explanation = Explanation(
            summary="Test",
            details={},
            raw_facts={}
        )
        
        graphql_data = explanation_to_graphql(explanation)
        
        # Should work without confidence
        assert "summary" in graphql_data
        assert graphql_data["summary"] == "Test"
    
    def test_graphql_trace_length_matches_explanation(self):
        """Test that GraphQL trace matches explanation trace."""
        generator = ExplanationGenerator()
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            archetype_ctx=ArchetypeContext(polarity_scores={"order": 0.7})
        )
        
        explanation = generator.generate(context)
        graphql_data = explanation_to_graphql(explanation)
        
        # If explanation has trace, GraphQL should too
        if explanation.trace:
            assert "trace" in graphql_data
            assert len(graphql_data["trace"]) == len(explanation.trace)
