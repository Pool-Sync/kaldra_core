"""
Kindra Layer 2 (Semiotic/Media) Rule-Based Scoring Engine.

Expanded coverage for media channels and tones.
"""

from __future__ import annotations

from typing import Dict, Any

from .rule_engine_base import KindraRuleEngineBase, clamp_score


class KindraLayer2SemioticMediaRules(KindraRuleEngineBase):
    """
    Rule-based scorer for Kindra Layer 2 (Semiotic / Media, Plane 6).

    Interprets:
    - Tone of media / discourse (sensational, analytical, neutral, opinionated, ...)
    - Journalistic style
    - Emotional sentiment + intensity
    - Media channels (social, TV, print, radio, podcast, blog, ...)
    """

    def score(self, context: Dict[str, Any], base_vectors: Dict[str, float] | None = None) -> Dict[str, float]:
        """Score Layer 2 vectors based on semiotic/media context."""
        scores: Dict[str, float] = dict(base_vectors) if base_vectors else {}

        tone = (context.get("media_tone") or "").lower()
        channel = (context.get("channel") or "").lower()
        sentiment = (context.get("sentiment") or "").lower()
        intensity = float(context.get("intensity", 0.0))

        # --- Tone-based rules ---

        if tone in {"sensational", "alarmist"}:
            scores["M12"] = clamp_score(scores.get("M12", 0.0) + 0.7)
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.3)

        elif tone in {"analytical", "neutral"}:
            scores["M12"] = clamp_score(scores.get("M12", 0.0) - 0.3)
            scores["T25"] = clamp_score(scores.get("T25", 0.0) + 0.2)

        elif tone in {"opinionated", "editorial"}:
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.2)
            scores["S09"] = clamp_score(scores.get("S09", 0.0) + 0.2)

        # --- Channel / medium modifiers (expanded) ---

        if channel in {"social", "twitter", "x", "tiktok", "instagram"}:
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.3)
            scores["R33"] = clamp_score(scores.get("R33", 0.0) - 0.1)

        elif channel in {"newspaper", "print"}:
            scores["M12"] = clamp_score(scores.get("M12", 0.0) - 0.1)

        elif channel in {"tv_news", "cable_news"}:
            scores["M12"] = clamp_score(scores.get("M12", 0.0) + 0.2)

        elif channel in {"radio"}:
            scores["M12"] = clamp_score(scores.get("M12", 0.0) + 0.1)

        elif channel in {"podcast"}:
            scores["T25"] = clamp_score(scores.get("T25", 0.0) + 0.2)
            if tone in {"opinionated", "sensational"}:
                scores["S09"] = clamp_score(scores.get("S09", 0.0) + 0.2)

        elif channel in {"blog"}:
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.1)

        # --- Sentiment & intensity ---

        intensity = max(0.0, min(1.0, intensity))

        if sentiment == "positive":
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.2 * intensity)
        elif sentiment == "negative":
            scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.2 * intensity)

        if intensity >= 0.7:
            scores["S09"] = clamp_score(scores.get("S09", 0.0) + 0.4)

        return scores
