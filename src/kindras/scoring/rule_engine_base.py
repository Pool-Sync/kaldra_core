"""
Base classes and utilities for Kindra rule-based scoring.

Provides abstract base class and clamp helper for all scoring engines.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Any


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


class KindraRuleEngineBase(ABC):
    """
    Abstract base class for Kindra rule-based scoring.
    Concrete engines implement score() for a given layer.
    """

    @abstractmethod
    def score(self, context: Dict[str, Any], base_vectors: Dict[str, float] | None = None) -> Dict[str, float]:
        """
        Compute scores for a set of Kindra vectors given a context.

        Args:
            context: Arbitrary metadata (country, sector, media_tone, etc.).
            base_vectors: Optional baseline scores per vector_id.

        Returns:
            Dict[vector_id, score] with values in [-1.0, 1.0].
        """
        raise NotImplementedError
