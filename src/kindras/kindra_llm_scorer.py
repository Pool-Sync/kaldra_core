"""
Kindra LLM-Based Scoring Engine.

Replaces rule-based scoring with contextual LLM inference while maintaining
full compatibility with Δ144, TW369, and all existing components.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
import math
from .scoring.llm_client_base import LLMClientBase


class KindraLLMScorer:
    """
    LLM-based Kindra scoring engine.
    
    Input:
        - text: raw input text (str)
        - context: dict with metadata (country, sector, domain, channel, etc.)
        - vectors: dict of vector definitions (from schema)
    
    Output:
        - dict {vector_id: score (-1.0 to 1.0)}

    Requirements (Engine Upgrade 1.pdf):
        - Clamp scores to [-1, 1]
        - Compatible with Δ144 + TW369
        - Deterministic fallback (rule-based)
        - Same shape as current rule-based scorer
    """

    def __init__(self, llm_client: Optional[LLMClientBase] = None, rule_fallback=None):
        """
        Initialize LLM scorer.
        
        Args:
            llm_client: Optional LLM client implementing LLMClientBase
            rule_fallback: Optional rule-based scorer for fallback
        """
        self.llm = llm_client
        self.rule_fallback = rule_fallback

    def score(
        self, 
        text: str, 
        context: Dict[str, Any], 
        vectors: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Generate Kindra scores using LLM inference.
        
        Args:
            text: Raw input text to analyze
            context: Metadata dict (country, sector, domain, etc.)
            vectors: Vector definitions from schema
            
        Returns:
            Dict mapping vector_id to score in [-1, 1]
        """
        # 1. Se LLM indisponível → fallback
        if self.llm is None:
            if self.rule_fallback is not None:
                return self.rule_fallback.score(context, vectors)
            else:
                # Ultimate fallback: zeros
                return {k: 0.0 for k in vectors.keys()}

        # 2. Construir prompt (few-shot + contexto)
        prompt = self._build_prompt(text, context, vectors)

        # 3. Chamada LLM
        try:
            response = self.llm.generate(prompt)
        except Exception as e:
            # LLM error → fallback
            if self.rule_fallback is not None:
                return self.rule_fallback.score(context, vectors)
            else:
                return {k: 0.0 for k in vectors.keys()}

        # 4. Parsear saída LLM
        scores = self._parse_scores(response, vectors)

        # 5. Clamp final
        return {k: max(-1.0, min(1.0, v)) for k, v in scores.items()}

    def _build_prompt(
        self, 
        text: str, 
        context: Dict[str, Any], 
        vectors: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Construct LLM prompt with context and instructions.
        
        Args:
            text: Input text
            context: Context metadata
            vectors: Vector definitions
            
        Returns:
            Prompt dict for LLM
        """
        # Contextual prompt structure
        return {
            "instruction": "Score Kindra cultural vectors in [-1,1]. Do NOT add extra fields.",
            "context": context,
            "text": text,
            "vectors": list(vectors.keys()),
        }

    def _parse_scores(
        self, 
        llm_response: Any, 
        vectors: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Parse LLM response into score dict.
        
        Args:
            llm_response: Response from LLM (must have 'scores' key)
            vectors: Vector definitions
            
        Returns:
            Dict mapping vector_id to float score
        """
        # llm_response must return {vector_id: float}
        raw = llm_response.get("scores", {})
        parsed = {}
        
        for k in vectors.keys():
            v = raw.get(k, 0.0)
            try:
                parsed[k] = float(v)
            except (ValueError, TypeError):
                parsed[k] = 0.0
                
        return parsed
