"""
Kindra Layer 2 (Semiotic/Media) Scoring Engine.

Rule-based scorer for semiotic and media context (Plane 6).
Interprets tone, channel, sentiment, and media intensity.
"""

from typing import Dict, Any

from .scoring_base import KindraScoringBase, clamp_score


class KindraLayer2SemioticMediaScoring(KindraScoringBase):
    """
    Rule-based scorer for Kindra Layer 2 (Semiotic / Media, Plane 6).

    Interprets:
    - Tone of media / discourse
    - Journalistic style (sensational vs analytical)
    - Emotional intensity
    - Agenda-setting / repetition level
    """

    def score(self, context: Dict[str, Any], vectors: Dict[str, float]) -> Dict[str, float]:
        """
        Score Layer 2 vectors based on semiotic/media context.
        
        Args:
            context: Must contain media_tone, channel, sentiment, intensity
            vectors: Baseline vector scores
            
        Returns:
            Updated vector scores in [-1.0, 1.0]
        """
        scores: Dict[str, float] = dict(vectors) if vectors else {}

        tone = (context.get("media_tone") or "").lower()
        channel = (context.get("channel") or "").lower()
        sentiment = (context.get("sentiment") or "").lower()
        intensity = context.get("intensity", 0.0)  # expected in [0,1]

        # --- Tone-based rules ---

        if tone in {"sensational", "alarmist"}:
            scores["M12"] = clamp_score(scores.get("M12", 0.0) + 0.7)   # Media sensationalism+
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.3)   # Expressive charge+

        elif tone in {"analytical", "neutral"}:
            scores["M12"] = clamp_score(scores.get("M12", 0.0) - 0.3)   # Less sensational
            scores["T25"] = clamp_score(scores.get("T25", 0.0) + 0.2)   # Rational/technical+

        # --- Channel / medium modifiers ---

        if channel in {"social", "twitter", "x", "tiktok"}:
            # Faster, more emotional, more volatile narratives.
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.3)
            scores["R33"] = clamp_score(scores.get("R33", 0.0) - 0.1)

        elif channel in {"newspaper", "print"}:
            scores["M12"] = clamp_score(scores.get("M12", 0.0) - 0.1)

        elif channel in {"tv_news", "cable_news"}:
            scores["M12"] = clamp_score(scores.get("M12", 0.0) + 0.2)

        # --- Sentiment & intensity ---

        if sentiment == "positive":
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.2 * max(0.0, float(intensity)))
        elif sentiment == "negative":
            scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.2 * max(0.0, float(intensity)))

        # Agenda-setting proxy: if intensity is very high, amplify semiotic tension.
        if float(intensity) >= 0.7:
            scores["S09"] = clamp_score(scores.get("S09", 0.0) + 0.4)   # Semiotic tension+

        return scores
