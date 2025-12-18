"""
KALDRA Bias Engine v1.0

Multi-provider bias detection, scoring, and mitigation.
"""

from .detector import BiasDetector, compute_bias_score_from_text
from .mitigation import BiasMitigation
from .scoring import BiasScoring, classify_bias

__all__ = [
    # New v1.0 classes
    "BiasDetector",
    "BiasScoring",
    "BiasMitigation",
    # Legacy functions (backward compatibility)
    "compute_bias_score_from_text",
    "classify_bias",
]
