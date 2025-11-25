"""
LLM Scoring Client Base.

Defines the protocol and base classes for LLM-based scoring clients.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from .llm_types import LLMScoringRequest, LLMScoringResponse


def clamp_score(value: float) -> float:
    """
    Clamp helper to keep scores in [-1.0, 1.0].
    
    Args:
        value: Score value to clamp
        
    Returns:
        Clamped score in range [-1.0, 1.0]
    """
    if value > 1.0:
        return 1.0
    if value < -1.0:
        return -1.0
    return value


class LLMScoringError(RuntimeError):
    """
    Generic error raised by LLM scoring clients.
    """


class LLMScoringClient(Protocol):
    """
    Protocol for any LLM-based scoring backend.

    This is the internal API contract used by the KALDRA pipeline.
    Different implementations (rule-based, real LLM, hybrid) must adhere to it.
    """

    def score(self, request: LLMScoringRequest) -> LLMScoringResponse:
        """
        Compute Kindra vector scores from text + context.

        Implementations MUST:
        - clamp all scores to [-1.0, 1.0]
        - fill metadata with model/prompt identifiers when available
        - set error field OR raise LLMScoringError on failure
        """
        ...


class AbstractLLMScoringClient(ABC):
    """
    Optional abstract base class for concrete implementations.
    """

    @abstractmethod
    def score(self, request: LLMScoringRequest) -> LLMScoringResponse:
        """Compute Kindra vector scores from text + context."""
        raise NotImplementedError
