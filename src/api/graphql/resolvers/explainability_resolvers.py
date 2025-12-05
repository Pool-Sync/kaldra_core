"""
GraphQL resolvers for KALDRA Explainability (v3.4 Phase 3).

Backend-only adapters for future API exposure.
"""
from typing import Optional
from src.explainability.explanation_generator import Explanation
from src.api.graphql.types.explainability_types import (
    ExplanationType,
    ExplanationConfidenceType,
    ComponentConfidenceType,
    DecisionStepType
)


def explanation_to_graphql(explanation: Explanation) -> dict:
    """
    Convert Explanation object to GraphQL-compatible dict.
    
    Args:
        explanation: Explanation instance
    
    Returns:
        Dictionary compatible with ExplanationType
    """
    result = {
        "summary": explanation.summary,
        "details": explanation.details,
        "raw_facts": explanation.raw_facts,
    }
    
    # Convert confidence if present
    if explanation.confidence:
        result["confidence"] = {
            "overall": explanation.confidence.overall,
            "components": [
                {
                    "name": comp.name,
                    "score": comp.score,
                    "reason": comp.reason,
                    "metadata": comp.metadata
                }
                for comp in explanation.confidence.components
            ],
            "trace": [
                {
                    "step": step.step,
                    "description": step.description,
                    "weight": step.weight,
                    "source": step.source,
                    "metadata": step.metadata
                }
                for step in explanation.confidence.trace
            ],
            "metadata": explanation.confidence.metadata
        }
    
    # Convert trace if present
    if explanation.trace:
        result["trace"] = [
            {
                "step": step.step,
                "description": step.description,
                "weight": step.weight,
                "source": step.source,
                "metadata": step.metadata if hasattr(step, 'metadata') else {}
            }
            for step in explanation.trace
        ]
    
    return result
