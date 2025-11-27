"""
Bias Scoring Module — KALDRA Bias Engine v1.0

Multi-dimensional bias scoring across:
- Toxicity
- Political bias
- Gender bias
- Racial bias
"""

from __future__ import annotations

from typing import Dict


class BiasScoring:
    """
    Multi-dimensional bias scoring for KALDRA Bias Engine v1.0.

    Computes normalized scores across 4 dimensions:
      - toxicity: Harmful, aggressive, or toxic language
      - political: Political leaning or bias
      - gender: Gender-based bias or stereotyping
      - racial: Race-based bias or stereotyping

    All scores are normalized to [0.0, 1.0] range.

    Example:
        >>> scorer = BiasScoring()
        >>> raw_scores = {'toxicity': 0.8, 'political': 0.3, 'gender': 0.1, 'racial': 0.0}
        >>> normalized = scorer.compute(raw_scores)
        >>> print(normalized)
        {'toxicity': 0.8, 'political': 0.3, 'gender': 0.1, 'racial': 0.0}

        >>> # Handles missing dimensions
        >>> partial_scores = {'toxicity': 0.5}
        >>> normalized = scorer.compute(partial_scores)
        >>> print(normalized)
        {'toxicity': 0.5, 'political': 0.0, 'gender': 0.0, 'racial': 0.0}
    """

    DIMENSIONS = ["toxicity", "political", "gender", "racial"]

    def compute(self, raw_scores: Dict[str, float]) -> Dict[str, float]:
        """
        Compute normalized multi-dimensional bias scores.

        Args:
            raw_scores: Dictionary with raw bias scores (may be incomplete)

        Returns:
            Dictionary with all 4 dimensions, normalized to [0.0, 1.0]
        """
        output = {}
        for dim in self.DIMENSIONS:
            v = float(raw_scores.get(dim, 0.0))
            # Clamp to [0.0, 1.0]
            output[dim] = max(0.0, min(1.0, v))
        return output

    def aggregate(self, scores: Dict[str, float], weights: Dict[str, float] = None) -> float:
        """
        Compute weighted aggregate bias score.

        Args:
            scores: Multi-dimensional bias scores
            weights: Optional weights for each dimension (default: equal weights)

        Returns:
            Aggregate bias score in [0.0, 1.0]

        Example:
            >>> scorer = BiasScoring()
            >>> scores = {'toxicity': 0.8, 'political': 0.3, 'gender': 0.1, 'racial': 0.0}
            >>> aggregate = scorer.aggregate(scores)
            >>> print(aggregate)  # (0.8 + 0.3 + 0.1 + 0.0) / 4 = 0.3

            >>> # Custom weights
            >>> weights = {'toxicity': 0.5, 'political': 0.2, 'gender': 0.15, 'racial': 0.15}
            >>> aggregate = scorer.aggregate(scores, weights)
        """
        if weights is None:
            # Equal weights
            weights = {dim: 1.0 / len(self.DIMENSIONS) for dim in self.DIMENSIONS}

        # Normalize weights to sum to 1.0
        total_weight = sum(weights.values())
        if total_weight == 0:
            return 0.0

        normalized_weights = {k: v / total_weight for k, v in weights.items()}

        # Compute weighted sum
        aggregate = 0.0
        for dim in self.DIMENSIONS:
            score = scores.get(dim, 0.0)
            weight = normalized_weights.get(dim, 0.0)
            aggregate += score * weight

        return max(0.0, min(1.0, aggregate))


# ============================================================================
# BACKWARD COMPATIBILITY: Preserve existing classification function
# ============================================================================


def classify_bias(score: float) -> str:
    """
    Classify a bias score in [0, 1] into coarse labels.

    Args:
        score: Bias score in range [0.0, 1.0]

    Returns:
        Classification label: "neutral", "negative", "positive", or "extreme"

    Note:
        This function is preserved for backward compatibility.
        New code should use BiasScoring class for multi-dimensional analysis.
    """
    if score < 0.3:
        return "neutral"
    if score < 0.6:
        return "negative"
    if score < 0.8:
        return "positive"
    return "extreme"
