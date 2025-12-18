"""
Base classes and utilities for Kindra scoring.

Provides abstract base class and helper functions for all Kindra scorers.
"""

from typing import Dict, Any
from abc import ABC, abstractmethod


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


class KindraScoringBase(ABC):
    """
    Abstract base class for Kindra scoring.
    All concrete scorers must implement score().
    """

    @abstractmethod
    def score(self, context: Dict[str, Any], vectors: Dict[str, float]) -> Dict[str, float]:
        """
        Compute scores for a set of Kindra vectors given a context.

        Args:
            context: Arbitrary metadata (country, sector, channel, etc.).
            vectors: Dict of vector_id -> baseline score (may be empty or partial).

        Returns:
            Dict of vector_id -> score in [-1.0, 1.0].
        """
        raise NotImplementedError
