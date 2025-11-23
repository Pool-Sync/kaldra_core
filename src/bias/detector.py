"""
KALDRA CORE — Bias detector (placeholder).
"""
from __future__ import annotations

from typing import Any, Dict



BIAS_KEYWORDS = {
    "always", "never", "worst", "best", "hate", "stupid", 
    "absolute", "undeniable", "disaster", "miracle", "impossible",
    "everyone", "nobody", "obvious", "clearly", "refuse"
}

def compute_bias_score_from_text(text: str) -> Dict[str, Any]:
    """
    Bias detector based on heuristics and keyword presence.
    
    Features:
    - Exclamation marks (intensity)
    - Upper-case ratio (shouting)
    - Text length (complexity)
    - Bias keywords (absolutism/emotion)

    Args:
        text: Input text to analyze for bias

    Returns:
        Dictionary containing:
            - bias_score: Numeric score in [0.0, 1.0]
            - features: Dictionary of extracted features
    """
    length = len(text)
    if length == 0:
        return {"bias_score": 0.0, "features": {"length": 0}}
        
    exclam = text.count("!")
    caps = sum(1 for ch in text if ch.isupper())
    
    # Keyword analysis
    text_lower = text.lower()
    keyword_hits = sum(1 for word in BIAS_KEYWORDS if word in text_lower)

    raw_score = 0.0
    
    # Heuristics weights
    raw_score += min(exclam / 5.0, 1.0) * 0.3        # Exclamations
    raw_score += min(caps / max(length, 1), 0.5) * 0.2 # Caps Lock
    raw_score += min(keyword_hits / 3.0, 1.0) * 0.4  # Keywords (Strongest signal)
    
    # Length penalty/boost (very short texts are often biased/snappy)
    if length < 50:
        raw_score += 0.1

    raw_score = max(0.0, min(1.0, raw_score))
    
    return {
        "bias_score": float(round(raw_score, 2)),
        "features": {
            "length": length,
            "exclamations": exclam,
            "upper_case_chars": caps,
            "keyword_hits": keyword_hits
        },
    }
