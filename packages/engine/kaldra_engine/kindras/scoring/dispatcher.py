"""
Kindra Scoring Dispatcher.

Orchestrates all three layer scoring engines.
"""

from __future__ import annotations

from typing import Dict, Any

from .layer1_rules import KindraLayer1CulturalMacroRules
from .layer2_rules import KindraLayer2SemioticMediaRules
from .layer3_rules import KindraLayer3StructuralSystemicRules


class KindraScoringDispatcher:
    """
    High-level dispatcher that runs all three Kindra scoring layers.

    Usage:
        dispatcher = KindraScoringDispatcher()
        result = dispatcher.run_all(context, base_vectors)
    """

    def __init__(self) -> None:
        """Initialize all three layer scorers."""
        self.layer1 = KindraLayer1CulturalMacroRules()
        self.layer2 = KindraLayer2SemioticMediaRules()
        self.layer3 = KindraLayer3StructuralSystemicRules()

    def run_all(
        self,
        context: Dict[str, Any],
        base_vectors: Dict[str, float] | None = None,
    ) -> Dict[str, Dict[str, float]]:
        """
        Run all 3 layer scorers and return a dict keyed by layer name.

        Args:
            context: Shared context for all layers
            base_vectors: Optional baseline vector scores

        Returns:
            {
              "layer1": {vector_id: score, ...},
              "layer2": {...},
              "layer3": {...}
            }
        """
        base = base_vectors or {}
        return {
            "layer1": self.layer1.score(context, base),
            "layer2": self.layer2.score(context, base),
            "layer3": self.layer3.score(context, base),
        }
