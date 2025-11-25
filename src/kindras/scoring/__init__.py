"""
Kindra Scoring Engine (Rule-Based, Sprint 1.3).

This package contains:
- Base scoring utilities and clamp helper
- Layer 1 / 2 / 3 rule-based engines
- High-level dispatcher
- Adapter to TWState (TW369)
"""

from .dispatcher import KindraScoringDispatcher
from .twstate_adapter import build_twstate_from_context

# Import cosine_similarity from parent module for backward compatibility
import sys
from pathlib import Path
parent_path = str(Path(__file__).parent.parent)
if parent_path not in sys.path:
    sys.path.insert(0, parent_path)

try:
    from ..scoring import cosine_similarity
except ImportError:
    # Fallback if scoring.py doesn't exist
    import numpy as np
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        a = np.asarray(a, dtype=float)
        b = np.asarray(b, dtype=float)
        num = float(np.dot(a, b))
        denom = float(np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)
        return num / denom

__all__ = [
    "KindraScoringDispatcher",
    "build_twstate_from_context",
    "cosine_similarity",
]
