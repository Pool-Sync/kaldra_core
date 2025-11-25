"""
Kindra Layer 3 (Structural/Systemic) Scoring Engine.

Rule-based scorer for structural and systemic context (Plane 9).
Interprets institutional strength, power dynamics, and regulatory stability.
"""

from typing import Dict, Any

from .scoring_base import KindraScoringBase, clamp_score


class KindraLayer3StructuralSystemicScoring(KindraScoringBase):
    """
    Rule-based scorer for Kindra Layer 3 (Structural / Systemic, Plane 9).

    Interprets:
    - Institutional strength
    - Political power concentration
    - Regulatory stability vs volatility
    - Long-term structural constraints or tailwinds
    """

    def score(self, context: Dict[str, Any], vectors: Dict[str, float]) -> Dict[str, float]:
        """
        Score Layer 3 vectors based on structural/systemic context.
        
        Args:
            context: Must contain institutional_strength, power_concentration, regulatory_stability
            vectors: Baseline vector scores
            
        Returns:
            Updated vector scores in [-1.0, 1.0]
        """
        scores: Dict[str, float] = dict(vectors) if vectors else {}

        inst_strength = float(context.get("institutional_strength", 0.5))  # [0,1]
        power_conc = float(context.get("power_concentration", 0.5))        # [0,1]
        reg_stability = float(context.get("regulatory_stability", 0.5))    # [0,1]

        # Institutional strength → guardian / order archetypes via structural vectors.
        if inst_strength >= 0.7:
            scores["G21"] = clamp_score(scores.get("G21", 0.0) + 0.5)   # Guardian / order+
        elif inst_strength <= 0.3:
            scores["G21"] = clamp_score(scores.get("G21", 0.0) - 0.4)   # Weak institutions

        # Power concentration → ruler / control axis.
        if power_conc >= 0.7:
            scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.4)   # Hierarchy / control+
        elif power_conc <= 0.3:
            scores["P17"] = clamp_score(scores.get("P17", 0.0) - 0.3)   # Decentralization

        # Regulatory stability → structural risk vs predictability.
        if reg_stability >= 0.7:
            scores["R33"] = clamp_score(scores.get("R33", 0.0) - 0.3)   # Less structural risk
        elif reg_stability <= 0.3:
            scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.4)   # Structural risk+

        return scores
