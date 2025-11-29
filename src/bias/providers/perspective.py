"""
Perspective API Bias Provider.

Integration with Google Perspective API for toxicity detection.
"""

import requests
from typing import Dict, Optional
from .base import BiasProvider


class PerspectiveProvider(BiasProvider):
    """
    Bias detection using Google Perspective API.
    
    Requires PERSPECTIVE_API_KEY to be configured.
    """
    
    def __init__(self, api_key: str, timeout: int = 10):
        """
        Initialize Perspective provider.
        
        Args:
            api_key: Google Perspective API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.api_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    
    def detect(self, text: str) -> Dict[str, float]:
        """
        Detect bias using Perspective API.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with bias scores
        """
        if not text.strip():
            return {
                "toxicity": 0.0,
                "political": 0.0,
                "gender": 0.0,
                "racial": 0.0
            }
        
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "THREAT": {}
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            scores = data.get("attributeScores", {})
            
            # Extract scores
            toxicity = self._extract_score(scores, "TOXICITY")
            identity_attack = self._extract_score(scores, "IDENTITY_ATTACK")
            insult = self._extract_score(scores, "INSULT")
            
            return {
                "toxicity": toxicity,
                "political": insult * 0.5,  # Approximate mapping
                "gender": identity_attack,
                "racial": identity_attack,
            }
            
        except Exception as e:
            print(f"Perspective API Error: {e}")
            # Return zeros on failure - caller can fallback to heuristic
            return {
                "toxicity": 0.0,
                "political": 0.0,
                "gender": 0.0,
                "racial": 0.0
            }
    
    def _extract_score(self, scores: dict, attribute: str) -> float:
        """Extract score from Perspective API response."""
        try:
            return float(scores[attribute]["summaryScore"]["value"])
        except (KeyError, TypeError, ValueError):
            return 0.0
