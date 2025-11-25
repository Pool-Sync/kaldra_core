"""
Kindra Scoring Dispatcher.

High-level dispatcher that runs all three Kindra scoring layers.
"""

from typing import Dict, Any

from .layer1_cultural_macro_scoring import KindraLayer1CulturalMacroScoring
from .layer2_semiotic_media_scoring import KindraLayer2SemioticMediaScoring
from .layer3_structural_systemic_scoring import KindraLayer3StructuralSystemicScoring
from .kindra_llm_scorer import KindraLLMScorer
from .kindra_hybrid_scorer import KindraHybridScorer


class KindraScoringDispatcher:
    """
    High-level dispatcher that runs all three Kindra scoring layers.

    Usage:
        dispatcher = KindraScoringDispatcher()
        result = dispatcher.run_all(context, base_vectors)
    """

    def __init__(self, llm_client=None, scoring_mode="llm", hybrid_config=None) -> None:
        """
        Initialize all three layer scorers.
        
        Args:
            llm_client: Optional LLM client for LLM-based scoring
            scoring_mode: "llm", "rule_based", or "hybrid" (default: "llm")
            hybrid_config: Optional config dict for hybrid mode
        """
        self.layer1 = KindraLayer1CulturalMacroScoring()
        self.layer2 = KindraLayer2SemioticMediaScoring()
        self.layer3 = KindraLayer3StructuralSystemicScoring()
        
        # LLM scorer with fallback to rule-based
        self.scoring_mode = scoring_mode
        self.llm_scorer = KindraLLMScorer(
            llm_client=llm_client,
            rule_fallback=None  # Will use layer scorers as fallback
        )
        
        # Hybrid scorer (combines LLM + rule-based)
        if scoring_mode == "hybrid":
            config = hybrid_config or {}
            self.hybrid_scorer = KindraHybridScorer(
                llm_scorer=self.llm_scorer,
                rule_scorer=self.layer1,  # Use layer1 as rule fallback
                alpha_global=config.get("alpha_global", 0.5),
                alpha_layers=config.get("alpha_layers", {})
            )

    def run_all(
        self,
        context: Dict[str, Any],
        base_vectors: Dict[str, float] | None = None,
    ) -> Dict[str, Dict[str, float]]:
        """
        Run all 3 layer scorers and return a dict keyed by layer name.

        Args:
            context: Shared context for all layers.
            base_vectors: Optional baseline vector scores to start from.

        Returns:
            {
              "layer1": {vector_id: score, ...},
              "layer2": {...},
              "layer3": {...}
            }
        """
        base = base_vectors or {}
        return {
            "layer1": self.layer1.score(context, base),
            "layer2": self.layer2.score(context, base),
            "layer3": self.layer3.score(context, base),
        }
