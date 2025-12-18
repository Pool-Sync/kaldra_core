"""
Kindra Hybrid Scoring Engine.

Combines LLM and Rule-Based scoring with configurable mixing:
    score_final = clamp(alpha * score_llm + (1 - alpha) * score_rule)
"""

from __future__ import annotations
from typing import Dict, Any, Optional


class KindraHybridScorer:
    """
    Hybrid scorer combining LLM and Rule-Based scoring.
    
    Formula:
        score_final = alpha * score_llm + (1 - alpha) * score_rule
        
    Where alpha ∈ [0, 1]:
        - alpha = 0: Pure rule-based
        - alpha = 0.5: Equal mix
        - alpha = 1: Pure LLM
    
    Supports:
        - Global alpha (default for all layers)
        - Layer-specific alpha overrides
        - Automatic clamping to [-1, 1]
    """

    def __init__(
        self,
        llm_scorer,
        rule_scorer,
        alpha_global: float = 0.5,
        alpha_layers: Optional[Dict[str, float]] = None
    ):
        """
        Initialize hybrid scorer.
        
        Args:
            llm_scorer: LLM-based scorer instance
            rule_scorer: Rule-based scorer instance
            alpha_global: Default mixing ratio (0-1)
            alpha_layers: Layer-specific alpha overrides {layer: alpha}
        """
        self.llm_scorer = llm_scorer
        self.rule_scorer = rule_scorer
        self.alpha_global = float(alpha_global)
        self.alpha_layers = alpha_layers or {}

    def _clamp(self, v: float) -> float:
        """Clamp value to [-1, 1]."""
        return max(-1.0, min(1.0, v))

    def _resolve_alpha(self, layer: int) -> float:
        """
        Resolve alpha for specific layer.
        
        Args:
            layer: Layer number (1, 2, or 3)
            
        Returns:
            Alpha value for this layer
        """
        return float(self.alpha_layers.get(str(layer), self.alpha_global))

    def score(
        self,
        text: str,
        context: Dict[str, Any],
        vectors: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Generate hybrid scores mixing LLM and rule-based.
        
        Args:
            text: Input text to analyze
            context: Context metadata (must include 'kindra_layer')
            vectors: Vector definitions
            
        Returns:
            Dict mapping vector_id to hybrid score in [-1, 1]
        """
        # 1. Get LLM scores
        llm_scores = self.llm_scorer.score(text, context, vectors)

        # 2. Get Rule-Based scores
        rule_scores = self.rule_scorer.score(context, vectors)

        # 3. Determine layer and alpha
        layer = context.get("kindra_layer", 1)
        alpha = self._resolve_alpha(layer)

        # 4. Mix scores and clamp
        final_scores: Dict[str, float] = {}
        for vid in vectors.keys():
            llm_val = llm_scores.get(vid, 0.0)
            rule_val = rule_scores.get(vid, 0.0)
            
            # Hybrid mixing
            mixed = alpha * llm_val + (1.0 - alpha) * rule_val
            
            # Clamp to [-1, 1]
            final_scores[vid] = self._clamp(mixed)

        return final_scores
