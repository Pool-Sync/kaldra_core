"""
Kindra Layer 3 (Structural/Systemic) Rule-Based Scoring Engine.
"""

from __future__ import annotations

from typing import Dict, Any

from .rule_engine_base import KindraRuleEngineBase, clamp_score


class KindraLayer3StructuralSystemicRules(KindraRuleEngineBase):
    """
    Rule-based scorer for Kindra Layer 3 (Structural / Systemic, Plane 9).

    Interprets:
    - Institutional strength [0,1]
    - Political power concentration [0,1]
    - Regulatory stability vs volatility [0,1]
    - Long-term structural risk vs predictability
    """

    def score(self, context: Dict[str, Any], base_vectors: Dict[str, float] | None = None) -> Dict[str, float]:
        """Score Layer 3 vectors based on structural/systemic context."""
        scores: Dict[str, float] = dict(base_vectors) if base_vectors else {}

        inst_strength = float(context.get("institutional_strength", 0.5))
        power_conc = float(context.get("power_concentration", 0.5))
        reg_stability = float(context.get("regulatory_stability", 0.5))

        inst_strength = max(0.0, min(1.0, inst_strength))
        power_conc = max(0.0, min(1.0, power_conc))
        reg_stability = max(0.0, min(1.0, reg_stability))

        # Institutional strength → guardian / order axis
        if inst_strength >= 0.7:
            scores["G21"] = clamp_score(scores.get("G21", 0.0) + 0.5)
        elif inst_strength <= 0.3:
            scores["G21"] = clamp_score(scores.get("G21", 0.0) - 0.4)

        # Power concentration → ruler / control axis
        if power_conc >= 0.7:
            scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.4)
        elif power_conc <= 0.3:
            scores["P17"] = clamp_score(scores.get("P17", 0.0) - 0.3)

        # Regulatory stability → structural risk vs predictability
        if reg_stability >= 0.7:
            scores["R33"] = clamp_score(scores.get("R33", 0.0) - 0.3)
        elif reg_stability <= 0.3:
            scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.4)

        return scores
