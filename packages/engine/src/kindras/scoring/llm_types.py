"""
LLM Scoring API Types.

Defines the request/response contract for internal LLM-based Kindra scoring.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class LLMScoringRequest:
    """
    Represents a request to the internal LLM scoring API.

    This is an abstract contract, independent of any specific provider (OpenAI, etc.).
    """
    layer: int  # 1, 2, or 3 (Kindra layer)
    text: str   # raw text to be analyzed
    context: Dict[str, Any]  # metadata: country, sector, channel, etc.
    mode: str = "kindra"     # hint for prompt variant (e.g. 'kindra_layer1_v1')
    max_vectors: Optional[int] = None  # optional: limit number of vectors to score


@dataclass
class LLMScoringResponse:
    """
    Represents the output of the internal LLM scoring API.

    All scores MUST be clamped to [-1.0, 1.0] before returning.
    """
    scores: Dict[str, float]          # vector_id -> score in [-1.0, 1.0]
    metadata: Dict[str, Any]          # model, prompt_version, latency, etc.
    error: Optional[str] = None       # optional error description
