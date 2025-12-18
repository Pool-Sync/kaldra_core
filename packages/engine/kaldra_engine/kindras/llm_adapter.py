"""
LLM Adapter for Kindra scoring.
"""
from typing import Dict, Any, Optional
import re

class KindraLLMScorer:
    """
    Wrapper for LLM scoring of Kindra vectors.
    Implementation uses heuristic keyword matching for v3.1.
    """

    def score_vector(self, text: str, vector_def: Dict[str, Any]) -> float:
        """
        Return a heuristic score [0, 1] for the vector based on text.
        
        Args:
            text: Input text to analyze
            vector_def: Vector definition dictionary containing 'keywords', 'short_name', etc.
            
        Returns:
            Float score between 0.0 and 1.0
        """
        text_lower = text.lower()
        score = 0.0
        
        # 1. Check for direct mention of ID or short name (strong signal)
        if vector_def.get('id', '').lower() in text_lower:
            score += 0.3
        if vector_def.get('short_name', '').lower() in text_lower:
            score += 0.2
            
        # 2. Check keywords/examples
        # Assuming vector_def has 'examples' or 'keywords' list
        keywords = vector_def.get('examples', []) + vector_def.get('keywords', [])
        
        matches = 0
        for kw in keywords:
            if kw.lower() in text_lower:
                matches += 1
        
        # Simple saturation curve
        if matches > 0:
            score += 0.1 + (0.1 * min(matches, 5))
            
        # 3. Base score for existence
        score += 0.1
        
        return min(1.0, score)
