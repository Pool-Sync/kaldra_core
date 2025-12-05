"""
GraphQL types for KALDRA Explainability (v3.4 Phase 3).

Backend-only types for future API exposure.

Note: This module provides type stubs without requiring graphene.
For production GraphQL use, install graphene: pip install graphene
"""

# Placeholder types for when graphene is not available
class ComponentConfidenceType:
    """Component confidence score (GraphQL type stub)."""
    pass


class DecisionStepType:
    """Single decision trace step (GraphQL type stub)."""
    pass


class ExplanationConfidenceType:
    """Confidence and trace information for an explanation (GraphQL type stub)."""
    pass


class ExplanationType:
    """Complete explanation with confidence and trace (GraphQL type stub)."""
    pass


# Try to import graphene and define real types if available
try:
    import graphene
    
    class ComponentConfidenceTypeReal(graphene.ObjectType):
        """Component confidence score."""
        name = graphene.String(required=True)
        score = graphene.Float(required=True)
        reason = graphene.String(required=True)
        metadata = graphene.JSONString()
    
    class DecisionStepTypeReal(graphene.ObjectType):
        """Single decision trace step."""
        step = graphene.String(required=True)
        description = graphene.String(required=True)
        weight = graphene.Float(required=True)
        source = graphene.String(required=True)
        metadata = graphene.JSONString()
    
    class ExplanationConfidenceTypeReal(graphene.ObjectType):
        """Confidence and trace information for an explanation."""
        overall = graphene.Float(required=True)
        components = graphene.List(ComponentConfidenceTypeReal)
        trace = graphene.List(DecisionStepTypeReal)
        metadata = graphene.JSONString()
    
    class ExplanationTypeReal(graphene.ObjectType):
        """Complete explanation with confidence and trace."""
        summary = graphene.String(required=True)
        details = graphene.JSONString()
        raw_facts = graphene.JSONString()
        confidence = graphene.Field(ExplanationConfidenceTypeReal)
        trace = graphene.List(DecisionStepTypeReal)
    
    # Use real types
    ComponentConfidenceType = ComponentConfidenceTypeReal
    DecisionStepType = DecisionStepTypeReal
    ExplanationConfidenceType = ExplanationConfidenceTypeReal
    ExplanationType = ExplanationTypeReal

except ImportError:
    # Graphene not available, use stubs (already defined above)
    pass
