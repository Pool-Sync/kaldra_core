"""
Heuristic Bias Provider.

Built-in keyword and feature-based bias detection.
"""

from typing import Dict
from .base import BiasProvider


BIAS_KEYWORDS = {
    "always", "never", "worst", "best", "hate", "stupid",
    "absolute", "undeniable", "disaster", "miracle", "impossible",
    "everyone", "nobody", "obvious", "clearly", "refuse"
}


class HeuristicProvider(BiasProvider):
    """
    Heuristic bias detection using keywords and text features.
    
    Features:
    - Exclamation marks (intensity)
    - Upper-case ratio (shouting)
    - Text length (complexity)
    - Bias keywords (absolutism/emotion)
    """
    
    def detect(self, text: str) -> Dict[str, float]:
        """
        Detect bias using heuristics.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with bias scores
        """
        length = len(text)
        if length == 0:
            return {
                "toxicity": 0.0,
                "political": 0.0,
                "gender": 0.0,
                "racial": 0.0
            }
        
        exclam = text.count("!")
        caps = sum(1 for ch in text if ch.isupper())
        
        # Keyword analysis
        text_lower = text.lower()
        keyword_hits = sum(1 for word in BIAS_KEYWORDS if word in text_lower)
        
        raw_score = 0.0
        
        # Heuristics weights
        raw_score += min(exclam / 5.0, 1.0) * 0.3  # Exclamations
        raw_score += min(caps / max(length, 1), 0.5) * 0.2  # Caps Lock
        raw_score += min(keyword_hits / 3.0, 1.0) * 0.4  # Keywords (Strongest signal)
        
        # Length penalty/boost (very short texts are often biased/snappy)
        if length < 50:
            raw_score += 0.1
        
        raw_score = max(0.0, min(1.0, raw_score))
        
        # Map heuristic score to dimensions
        return {
            "toxicity": raw_score,
            "political": raw_score * 0.3,  # Lower weight for political
            "gender": raw_score * 0.2,  # Lower weight for gender
            "racial": raw_score * 0.2,  # Lower weight for racial
        }
