"""
Bias Detection Module — KALDRA Bias Engine v1.0

Multi-provider bias detection supporting:
- Perspective API (optional)
- Detoxify (optional)
- Custom classifier (injected)
- Heuristic fallback (built-in)
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional


# Optional imports with graceful degradation
try:
    # Perspective API would be imported here if available
    # from googleapiclient import discovery
    PERSPECTIVE_AVAILABLE = False
except ImportError:
    PERSPECTIVE_AVAILABLE = False

try:
    # Detoxify would be imported here if available
    # from detoxify import Detoxify
    DETOXIFY_AVAILABLE = False
except ImportError:
    DETOXIFY_AVAILABLE = False


BIAS_KEYWORDS = {
    "always", "never", "worst", "best", "hate", "stupid",
    "absolute", "undeniable", "disaster", "miracle", "impossible",
    "everyone", "nobody", "obvious", "clearly", "refuse"
}


class BiasDetector:
    """
    Unified bias detection wrapper for KALDRA Bias Engine v1.0.

    Supports multiple providers:
      - 'perspective': Google Perspective API (requires client)
      - 'detoxify': Detoxify model (requires model instance)
      - 'custom': Custom classifier function (requires callable)
      - 'heuristic': Built-in keyword/feature-based detection (default)

    Args:
        provider: Detection provider name
        perspective_client: Optional Perspective API client
        detoxify_model: Optional Detoxify model instance
        custom_fn: Optional custom detection function

    Example:
        >>> # Using heuristic detector (no dependencies)
        >>> detector = BiasDetector(provider="heuristic")
        >>> result = detector.detect("This is terrible!")
        >>> print(result)
        {'toxicity': 0.5, 'political': 0.0, 'gender': 0.0, 'racial': 0.0}

        >>> # Using custom detector
        >>> def my_detector(text):
        ...     return {'toxicity': 0.3}
        >>> detector = BiasDetector(provider="custom", custom_fn=my_detector)
        >>> result = detector.detect("Test text")
    """

    def __init__(
        self,
        provider: str = "heuristic",
        perspective_client: Optional[Any] = None,
        detoxify_model: Optional[Any] = None,
        custom_fn: Optional[Callable[[str], Dict[str, float]]] = None,
    ) -> None:
        self.provider = provider
        self.perspective_client = perspective_client
        self.detoxify_model = detoxify_model
        self.custom_fn = custom_fn

        # Validate provider configuration
        if provider == "perspective" and perspective_client is None:
            raise ValueError("perspective_client required for 'perspective' provider")
        if provider == "detoxify" and detoxify_model is None:
            raise ValueError("detoxify_model required for 'detoxify' provider")
        if provider == "custom" and custom_fn is None:
            raise ValueError("custom_fn required for 'custom' provider")

    def detect(self, text: str) -> Dict[str, float]:
        """
        Detect bias in text using configured provider.

        Args:
            text: Input text to analyze

        Returns:
            Dictionary with bias scores for each dimension:
                - toxicity: [0.0, 1.0]
                - political: [0.0, 1.0]
                - gender: [0.0, 1.0]
                - racial: [0.0, 1.0]
        """
        if self.provider == "perspective":
            return self._detect_perspective(text)
        elif self.provider == "detoxify":
            return self._detect_detoxify(text)
        elif self.provider == "custom":
            return self._detect_custom(text)
        elif self.provider == "heuristic":
            return self._detect_heuristic(text)
        else:
            # Fallback to heuristic for unknown providers
            return self._detect_heuristic(text)

    def _detect_perspective(self, text: str) -> Dict[str, float]:
        """
        Detect bias using Google Perspective API.

        Note: This is a skeleton implementation. Real integration would
        require API key and proper request formatting.
        """
        if self.perspective_client is None:
            return self._detect_heuristic(text)

        try:
            # Example API call structure (not functional without real client)
            # response = self.perspective_client.comments().analyze(
            #     body={
            #         'comment': {'text': text},
            #         'requestedAttributes': {
            #             'TOXICITY': {},
            #             'IDENTITY_ATTACK': {},
            #             'INSULT': {},
            #         }
            #     }
            # ).execute()
            #
            # return {
            #     'toxicity': response['attributeScores']['TOXICITY']['summaryScore']['value'],
            #     'political': 0.0,
            #     'gender': response['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value'],
            #     'racial': response['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value'],
            # }

            # Placeholder: call analyze method if client has it
            if hasattr(self.perspective_client, "analyze"):
                response = self.perspective_client.analyze(text)
                scores = response.get("scores", {})
                return {
                    "toxicity": float(scores.get("toxicity", 0.0)),
                    "political": float(scores.get("political", 0.0)),
                    "gender": float(scores.get("gender", 0.0)),
                    "racial": float(scores.get("racial", 0.0)),
                }
        except Exception:
            # Fallback on error
            pass

        return self._detect_heuristic(text)

    def _detect_detoxify(self, text: str) -> Dict[str, float]:
        """
        Detect bias using Detoxify model.

        Note: This is a skeleton implementation. Real integration would
        require the detoxify package installed.
        """
        if self.detoxify_model is None:
            return self._detect_heuristic(text)

        try:
            # Example usage (not functional without real model)
            # outputs = self.detoxify_model.predict(text)
            # return {
            #     'toxicity': outputs.get('toxicity', 0.0),
            #     'political': 0.0,
            #     'gender': outputs.get('identity_attack', 0.0),
            #     'racial': outputs.get('identity_attack', 0.0),
            # }

            # Placeholder: call predict method if model has it
            if hasattr(self.detoxify_model, "predict"):
                outputs = self.detoxify_model.predict(text)
                return {
                    "toxicity": float(outputs.get("toxicity", 0.0)),
                    "political": float(outputs.get("political", 0.0)),
                    "gender": float(outputs.get("gender", 0.0)),
                    "racial": float(outputs.get("racial", 0.0)),
                }
        except Exception:
            # Fallback on error
            pass

        return self._detect_heuristic(text)

    def _detect_custom(self, text: str) -> Dict[str, float]:
        """
        Detect bias using custom classifier function.

        Custom function should accept text and return dict with scores.
        """
        if self.custom_fn is None:
            return self._detect_heuristic(text)

        try:
            result = self.custom_fn(text)
            # Ensure all dimensions are present
            return {
                "toxicity": float(result.get("toxicity", 0.0)),
                "political": float(result.get("political", 0.0)),
                "gender": float(result.get("gender", 0.0)),
                "racial": float(result.get("racial", 0.0)),
            }
        except Exception:
            # Fallback on error
            return self._detect_heuristic(text)

    def _detect_heuristic(self, text: str) -> Dict[str, float]:
        """
        Built-in heuristic bias detection using keywords and text features.

        This is the fallback method that requires no external dependencies.
        """
        # Use existing heuristic function
        result = compute_bias_score_from_text(text)
        base_score = result["bias_score"]

        # Map heuristic score to dimensions
        # Simple mapping: higher bias score suggests higher toxicity
        return {
            "toxicity": base_score,
            "political": base_score * 0.3,  # Lower weight for political
            "gender": base_score * 0.2,  # Lower weight for gender
            "racial": base_score * 0.2,  # Lower weight for racial
        }


# ============================================================================
# BACKWARD COMPATIBILITY: Preserve existing heuristic function
# ============================================================================


def compute_bias_score_from_text(text: str) -> Dict[str, Any]:
    """
    Bias detector based on heuristics and keyword presence.

    Features:
    - Exclamation marks (intensity)
    - Upper-case ratio (shouting)
    - Text length (complexity)
    - Bias keywords (absolutism/emotion)

    Args:
        text: Input text to analyze for bias

    Returns:
        Dictionary containing:
            - bias_score: Numeric score in [0.0, 1.0]
            - features: Dictionary of extracted features

    Note:
        This function is preserved for backward compatibility.
        New code should use BiasDetector class.
    """
    length = len(text)
    if length == 0:
        return {"bias_score": 0.0, "features": {"length": 0}}

    exclam = text.count("!")
    caps = sum(1 for ch in text if ch.isupper())

    # Keyword analysis
    text_lower = text.lower()
    keyword_hits = sum(1 for word in BIAS_KEYWORDS if word in text_lower)

    raw_score = 0.0

    # Heuristics weights
    raw_score += min(exclam / 5.0, 1.0) * 0.3  # Exclamations
    raw_score += min(caps / max(length, 1), 0.5) * 0.2  # Caps Lock
    raw_score += min(keyword_hits / 3.0, 1.0) * 0.4  # Keywords (Strongest signal)

    # Length penalty/boost (very short texts are often biased/snappy)
    if length < 50:
        raw_score += 0.1

    raw_score = max(0.0, min(1.0, raw_score))

    return {
        "bias_score": float(round(raw_score, 2)),
        "features": {
            "length": length,
            "exclamations": exclam,
            "upper_case_chars": caps,
            "keyword_hits": keyword_hits,
        },
    }
