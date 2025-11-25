"""
LLM to TWState Service.

High-level service that converts text + context directly into TWState for TW369.
"""

from __future__ import annotations

from typing import Dict, Any

from src.tw369.tw369_integration import TWState
from .llm_scoring_service import LLMScoringService


class LLMToTWStateService:
    """
    High-level service that converts raw text + context into a TWState instance
    using the internal LLM scoring API (currently backed by rule-based dummy client).

    Mapping:
        Layer 1 -> Plane 3 (Cultural Macro)
        Layer 2 -> Plane 6 (Semiotic / Media)
        Layer 3 -> Plane 9 (Structural / Systemic)
    """

    def __init__(self, scoring_service: LLMScoringService | None = None) -> None:
        """
        Initialize TWState service.
        
        Args:
            scoring_service: Optional LLM scoring service. Defaults to new instance.
        """
        self._scoring_service = scoring_service or LLMScoringService()

    def build_twstate_from_text(
        self,
        text: str,
        context: Dict[str, Any],
        max_vectors_per_layer: int | None = None,
    ) -> TWState:
        """
        Run LLM scoring for all three layers and map them into a TWState.
        
        Args:
            text: Raw text to analyze
            context: Context metadata
            max_vectors_per_layer: Optional limit per layer
            
        Returns:
            TWState instance ready for TW369 engine
        """
        responses = self._scoring_service.score_all_layers(
            text=text,
            context=context,
            mode_prefix="kindra_layer",
            max_vectors_per_layer=max_vectors_per_layer,
        )

        layer1 = responses[1].scores
        layer2 = responses[2].scores
        layer3 = responses[3].scores

        return TWState(
            plane3_cultural_macro=layer1,
            plane6_semiotic_media=layer2,
            plane9_structural_systemic=layer3,
            metadata={
                "source": "llm_scoring_service",
                "context_snapshot": context,
                "layers_meta": {
                    1: responses[1].metadata,
                    2: responses[2].metadata,
                    3: responses[3].metadata,
                },
            },
        )
