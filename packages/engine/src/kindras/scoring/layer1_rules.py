"""
Kindra Layer 1 (Cultural Macro) Rule-Based Scoring Engine.

Expanded coverage for countries and sectors.
"""

from __future__ import annotations

from typing import Dict, Any

from .rule_engine_base import KindraRuleEngineBase, clamp_score


class KindraLayer1CulturalMacroRules(KindraRuleEngineBase):
    """
    Rule-based scorer for Kindra Layer 1 (Cultural Macro, Plane 3).

    Interprets macro-level cultural context:
    - Country / region (BR, US, JP, IN, DE, FR, CN, ...)
    - Expressiveness vs restraint
    - Individualism vs collectivism
    - Hierarchy vs horizontal structures
    - Sector-level cultural biases (tech, finance, healthcare, retail, industrial, ...)
    """

    def score(self, context: Dict[str, Any], base_vectors: Dict[str, float] | None = None) -> Dict[str, float]:
        """Score Layer 1 vectors based on cultural macro context."""
        scores: Dict[str, float] = dict(base_vectors) if base_vectors else {}

        country = (context.get("country") or "").upper()
        sector = (context.get("sector") or "").lower()

        # --- Country-level baselines (expanded coverage) ---

        if country == "BR":
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.6)
            scores["P17"] = clamp_score(scores.get("P17", 0.0) - 0.2)
            scores["R33"] = clamp_score(scores.get("R33", 0.0) - 0.1)

        elif country == "US":
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.3)
            scores["R33"] = clamp_score(scores.get("R33", 0.0) - 0.3)
            scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.1)

        elif country == "JP":
            scores["E01"] = clamp_score(scores.get("E01", 0.0) - 0.4)
            scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.5)
            scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.2)

        elif country == "IN":
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.4)
            scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.3)
            scores["R33"] = clamp_score(scores.get("R33", 0.0) - 0.1)

        elif country == "DE":
            scores["E01"] = clamp_score(scores.get("E01", 0.0) - 0.2)
            scores["T25"] = clamp_score(scores.get("T25", 0.0) + 0.3)
            scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.2)

        elif country == "FR":
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.3)
            scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.1)
            scores["R33"] = clamp_score(scores.get("R33", 0.0) - 0.1)

        elif country == "CN":
            scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.6)
            scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.2)
            scores["E01"] = clamp_score(scores.get("E01", 0.0) - 0.2)

        # --- Sector-level modifiers (expanded coverage) ---

        if sector == "tech":
            scores["T25"] = clamp_score(scores.get("T25", 0.0) + 0.6)
            scores["R33"] = clamp_score(scores.get("R33", 0.0) - 0.2)

        elif sector in {"finance", "banking"}:
            scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.3)
            scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.2)

        elif sector in {"energy", "oil_gas"}:
            scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.1)
            scores["T25"] = clamp_score(scores.get("T25", 0.0) - 0.1)

        elif sector in {"healthcare", "pharma"}:
            scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.2)
            scores["G21"] = clamp_score(scores.get("G21", 0.0) + 0.2)

        elif sector in {"retail", "consumer"}:
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.2)
            scores["S09"] = clamp_score(scores.get("S09", 0.0) + 0.1)

        elif sector in {"industrial", "manufacturing"}:
            scores["T25"] = clamp_score(scores.get("T25", 0.0) + 0.2)
            scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.1)

        return scores
