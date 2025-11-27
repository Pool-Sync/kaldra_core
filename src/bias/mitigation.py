"""
Bias Mitigation Module — KALDRA Bias Engine v1.0

Implements bias mitigation strategies:
- Correction (reduce extreme scores)
- Confidence shaping (adjust confidence based on bias)
- Flagging (identify high-bias content)
"""

from __future__ import annotations

from typing import Any, Dict, List


class BiasMitigation:
    """
    Bias mitigation for KALDRA Bias Engine v1.0.

    Provides strategies to handle detected bias:
      - Correction: Reduce extreme bias scores
      - Flagging: Identify dimensions exceeding thresholds
      - Confidence shaping: Adjust confidence based on bias levels

    Args:
        correction_factor: Multiplier for extreme scores (default: 0.85)
        flag_threshold: Threshold for flagging high bias (default: 0.8)
        extreme_threshold: Threshold for extreme correction (default: 0.7)

    Example:
        >>> mitigator = BiasMitigation()
        >>> bias_scores = {'toxicity': 0.9, 'political': 0.3, 'gender': 0.1, 'racial': 0.0}
        >>> result = mitigator.apply(bias_scores)
        >>> print(result['flags'])
        ['toxicity']
        >>> print(result['mitigated_scores']['toxicity'])
        0.765  # 0.9 * 0.85 = 0.765
    """

    def __init__(
        self,
        correction_factor: float = 0.85,
        flag_threshold: float = 0.8,
        extreme_threshold: float = 0.7,
    ) -> None:
        self.correction_factor = correction_factor
        self.flag_threshold = flag_threshold
        self.extreme_threshold = extreme_threshold

    def apply(self, bias_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Apply mitigation strategies to bias scores.

        Args:
            bias_scores: Multi-dimensional bias scores

        Returns:
            Dictionary containing:
                - mitigated_scores: Corrected bias scores
                - flags: List of dimensions exceeding flag_threshold
                - severity: Overall severity classification
        """
        mitigated = {}
        flags = []

        for dim, score in bias_scores.items():
            # Flag high-bias dimensions
            if score > self.flag_threshold:
                flags.append(dim)

            # Apply correction to extreme values
            if score > self.extreme_threshold:
                corrected = score * self.correction_factor
            else:
                corrected = score

            mitigated[dim] = corrected

        # Determine overall severity
        max_score = max(bias_scores.values()) if bias_scores else 0.0
        severity = self._classify_severity(max_score)

        return {
            "mitigated_scores": mitigated,
            "flags": flags,
            "severity": severity,
        }

    def shape_confidence(
        self, confidence: float, bias_scores: Dict[str, float]
    ) -> float:
        """
        Adjust confidence score based on detected bias.

        High bias reduces confidence in the result.

        Args:
            confidence: Original confidence score [0.0, 1.0]
            bias_scores: Multi-dimensional bias scores

        Returns:
            Adjusted confidence score [0.0, 1.0]

        Example:
            >>> mitigator = BiasMitigation()
            >>> confidence = 0.9
            >>> bias_scores = {'toxicity': 0.8, 'political': 0.2}
            >>> adjusted = mitigator.shape_confidence(confidence, bias_scores)
            >>> print(adjusted)
            0.72  # Reduced due to high toxicity
        """
        if not bias_scores:
            return confidence

        # Calculate average bias
        avg_bias = sum(bias_scores.values()) / len(bias_scores)

        # Reduce confidence proportionally to bias
        # High bias (0.8-1.0) reduces confidence by up to 20%
        reduction_factor = 1.0 - (avg_bias * 0.2)

        adjusted = confidence * reduction_factor
        return max(0.0, min(1.0, adjusted))

    def _classify_severity(self, max_score: float) -> str:
        """
        Classify overall bias severity.

        Args:
            max_score: Maximum bias score across all dimensions

        Returns:
            Severity label: "low", "medium", "high", or "critical"
        """
        if max_score < 0.3:
            return "low"
        elif max_score < 0.6:
            return "medium"
        elif max_score < 0.8:
            return "high"
        else:
            return "critical"

    def generate_recommendations(self, flags: List[str]) -> List[str]:
        """
        Generate mitigation recommendations based on flagged dimensions.

        Args:
            flags: List of flagged bias dimensions

        Returns:
            List of human-readable recommendations

        Example:
            >>> mitigator = BiasMitigation()
            >>> flags = ['toxicity', 'gender']
            >>> recommendations = mitigator.generate_recommendations(flags)
            >>> print(recommendations)
            ['Review content for toxic language', 'Check for gender bias or stereotyping']
        """
        recommendations = []

        if "toxicity" in flags:
            recommendations.append("Review content for toxic language")
        if "political" in flags:
            recommendations.append("Check for political bias or one-sided framing")
        if "gender" in flags:
            recommendations.append("Check for gender bias or stereotyping")
        if "racial" in flags:
            recommendations.append("Check for racial bias or stereotyping")

        if not recommendations:
            recommendations.append("No significant bias detected")

        return recommendations
