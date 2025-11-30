"""
Kindra Layer 1 (Cultural Macro) Scoring Engine.

Rule-based scorer for cultural macro-level context (Plane 3).
Interprets country, sector, and broad cultural patterns.
"""

from typing import Dict, Any

from .scoring_base import KindraScoringBase, clamp_score


class KindraLayer1CulturalMacroScoring(KindraScoringBase):
    """
    Rule-based scorer for Kindra Layer 1 (Cultural Macro, Plane 3).

    Interprets macro-level cultural context:
    - Country / region
    - Expressiveness vs restraint
    - Individualism vs collectivism
    - Hierarchy vs horizontal structures
    """

    def adjust_l1_with_polarities(self, scores: Dict[str, float], polarities: Dict[str, float]) -> Dict[str, float]:
        """
        Adjust Layer 1 scores based on active polarities (v2.7 Hook).
        
        If specific polarities are active (e.g., POL_ORDER_CHAOS), they can boost or suppress
        related cultural macro scores.
        """
        if not polarities:
            return scores
            
        adjusted = scores.copy()
        
        # Example logic: High Chaos (POL_ORDER_CHAOS > 0.7) boosts 'disruption' scores if present
        chaos_score = polarities.get("POL_ORDER_CHAOS", 0.5)
        if chaos_score > 0.7:
            for key in adjusted:
                if "disruption" in key or "change" in key:
                    adjusted[key] *= 1.1
                    
        # Example logic: High Tradition (POL_TRADITION_INNOVATION < 0.3) boosts 'stability'
        trad_score = polarities.get("POL_TRADITION_INNOVATION", 0.5)
        if trad_score < 0.3:
             for key in adjusted:
                if "tradition" in key or "stability" in key:
                    adjusted[key] *= 1.1
                    
        return adjusted

    def score(self, context: Dict[str, Any], vectors: Dict[str, float]) -> Dict[str, float]:
        """
        Score Layer 1 vectors based on cultural macro context.
        
        Args:
            context: Must contain 'country' and optionally 'sector'
            vectors: Baseline vector scores
            
        Returns:
            Updated vector scores in [-1.0, 1.0]
        """
        scores: Dict[str, float] = dict(vectors) if vectors else {}

        country = (context.get("country") or "").upper()
        sector = (context.get("sector") or "").lower()

        # --- Country-level baselines (examples) ---

        if country == "BR":
            # Brazil — high expressiveness, medium collectivism, lower formal hierarchy.
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.6)   # Expressiveness+
            scores["P17"] = clamp_score(scores.get("P17", 0.0) - 0.2)   # Hierarchy-
            scores["R33"] = clamp_score(scores.get("R33", 0.0) - 0.1)   # Risk aversion-

        elif country == "US":
            # US — medium-high individualism, higher risk tolerance, visible assertion.
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.3)   # Expressiveness+
            scores["R33"] = clamp_score(scores.get("R33", 0.0) - 0.3)   # Risk aversion-
            scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.1)   # Hierarchy+

        elif country == "JP":
            # Japan — lower overt expressiveness, high hierarchy, high social cohesion.
            scores["E01"] = clamp_score(scores.get("E01", 0.0) - 0.4)   # Expressiveness-
            scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.5)   # Hierarchy+
            scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.2)   # Risk aversion+

        elif country == "IN":
            # India — expressive, layered hierarchy, strong community fabric.
            scores["E01"] = clamp_score(scores.get("E01", 0.0) + 0.4)
            scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.3)
            scores["R33"] = clamp_score(scores.get("R33", 0.0) - 0.1)

        # --- Sector-level modifiers (macro cultural lens) ---

        if sector == "tech":
            # Tech culture: innovation bias, disruption narrative.
            scores["T25"] = clamp_score(scores.get("T25", 0.0) + 0.6)   # Innovation+
            scores["R33"] = clamp_score(scores.get("R33", 0.0) - 0.2)   # Risk aversion-

        elif sector in {"finance", "banking"}:
            # Finance: more risk-managed, hierarchy and control.
            scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.3)   # Risk aversion+
            scores["P17"] = clamp_score(scores.get("P17", 0.0) + 0.2)   # Hierarchy+

        elif sector in {"energy", "oil_gas"}:
            # Energy: long-term structural bets, high capital, slower change.
            scores["R33"] = clamp_score(scores.get("R33", 0.0) + 0.1)
            scores["T25"] = clamp_score(scores.get("T25", 0.0) - 0.1)

        return scores
