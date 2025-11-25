"""
Dummy LLM Scoring Client.

Rule-backed implementation for testing and API contract validation.
Does not call any real LLM - uses existing rule-based scoring engine.
"""

from __future__ import annotations

from typing import Dict, Any
import time

from .llm_types import LLMScoringRequest, LLMScoringResponse
from .llm_client_base import LLMScoringClient, clamp_score
from .dispatcher import KindraScoringDispatcher


class DummyLLMScoringClient(LLMScoringClient):
    """
    Dummy implementation of LLMScoringClient.

    Instead of calling a real LLM, it uses the existing rule-based Kindra scoring
    engine as a backend. This is intended for:
    - End-to-end integration tests
    - API contract validation
    - Local development without external dependencies
    """

    def __init__(self) -> None:
        """Initialize with rule-based dispatcher."""
        self._dispatcher = KindraScoringDispatcher()

    def _pick_layer_scores(self, layer: int, context: Dict[str, Any]) -> Dict[str, float]:
        """
        Runs the rule-based dispatcher and extracts scores for a specific layer.
        
        Args:
            layer: Kindra layer (1, 2, or 3)
            context: Context metadata
            
        Returns:
            Dictionary of vector scores for the specified layer
        """
        result = self._dispatcher.run_all(context, base_vectors={})

        if layer == 1:
            return result.get("layer1", {})
        if layer == 2:
            return result.get("layer2", {})
        if layer == 3:
            return result.get("layer3", {})
        # fallback: unknown layer -> empty
        return {}

    def score(self, request: LLMScoringRequest) -> LLMScoringResponse:
        """
        Compute scores using rule-based backend.
        
        Note: Currently ignores request.text and only uses context.
        This is a dummy implementation for testing the API contract.
        """
        start = time.time()

        # For now, ignore request.text in this dummy implementation.
        # Only context is used via the rule-based engine.
        raw_scores = self._pick_layer_scores(request.layer, request.context)

        # Clamp all scores
        clamped_scores: Dict[str, float] = {
            k: clamp_score(v) for k, v in raw_scores.items()
        }

        if request.max_vectors is not None and request.max_vectors > 0:
            # Keep only the first N vectors (arbitrary but deterministic order)
            items = list(clamped_scores.items())[: request.max_vectors]
            clamped_scores = dict(items)

        latency_ms = int((time.time() - start) * 1000)

        return LLMScoringResponse(
            scores=clamped_scores,
            metadata={
                "backend": "dummy_rule_based",
                "mode": request.mode,
                "layer": request.layer,
                "latency_ms": latency_ms,
            },
            error=None,
        )
