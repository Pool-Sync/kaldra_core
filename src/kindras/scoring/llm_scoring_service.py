"""
LLM Scoring Service.

High-level service for text-based Kindra scoring via LLM API.
"""

from __future__ import annotations

from typing import Dict, Any

from .llm_types import LLMScoringRequest, LLMScoringResponse
from .llm_client_base import LLMScoringClient
from .llm_dummy_client import DummyLLMScoringClient


class LLMScoringService:
    """
    High-level service that exposes a simple API:

        (layer, text, context) -> Kindra scores

    It delegates the actual scoring to an LLMScoringClient implementation.
    By default, it uses DummyLLMScoringClient (rule-backed).

    In the future, this can be configured to use a real LLM-based client
    without changing the call sites.
    """

    def __init__(self, client: LLMScoringClient | None = None) -> None:
        """
        Initialize scoring service.
        
        Args:
            client: Optional LLM scoring client. Defaults to DummyLLMScoringClient.
        """
        self._client = client or DummyLLMScoringClient()

    def score_layer(
        self,
        layer: int,
        text: str,
        context: Dict[str, Any],
        mode: str = "kindra",
        max_vectors: int | None = None,
    ) -> LLMScoringResponse:
        """
        Score a single Kindra layer using the configured LLM client.
        
        Args:
            layer: Kindra layer (1, 2, or 3)
            text: Raw text to analyze
            context: Context metadata
            mode: Prompt mode identifier
            max_vectors: Optional limit on number of vectors
            
        Returns:
            LLM scoring response with scores and metadata
        """
        request = LLMScoringRequest(
            layer=layer,
            text=text,
            context=context,
            mode=mode,
            max_vectors=max_vectors,
        )
        return self._client.score(request)

    def score_all_layers(
        self,
        text: str,
        context: Dict[str, Any],
        mode_prefix: str = "kindra_layer",
        max_vectors_per_layer: int | None = None,
    ) -> Dict[int, LLMScoringResponse]:
        """
        Convenience helper to score all three layers (1, 2, 3) at once.

        Args:
            text: Raw text to analyze
            context: Context metadata
            mode_prefix: Prefix for mode identifiers
            max_vectors_per_layer: Optional limit per layer
            
        Returns:
            {1: response_layer1, 2: response_layer2, 3: response_layer3}
        """
        results: Dict[int, LLMScoringResponse] = {}
        for layer in (1, 2, 3):
            mode = f"{mode_prefix}{layer}"
            results[layer] = self.score_layer(
                layer=layer,
                text=text,
                context=context,
                mode=mode,
                max_vectors=max_vectors_per_layer,
            )
        return results
