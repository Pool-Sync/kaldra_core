"""
Tau Risk Model.

Calculates the Tau Score based on various risk features.
"""
import math
from typing import Dict, Any

class TauRiskModel:
    """
    Mathematical model for calculating epistemic reliability (Tau Score).
    
    Formula:
        TauScore = sigmoid(baseline - weighted_sum(risk_features))
    """
    
    def __init__(self):
        # Base confidence level (adjusted for higher sensitivity)
        self.baseline = 3.0 
        
        # Weights for different risk factors (higher weight = more impact on score reduction)
        self.weights = {
            "bias_score": 2.5,
            "polarity_extremity": 2.0,
            "semantic_entropy": 1.0,
            "tw_severity": 1.5,
            "drift_instability": 2.0,
            "meta_inversions": 3.0
        }

    def calculate_score(self, features: Dict[str, float]) -> float:
        """
        Calculate Tau Score from a dictionary of normalized risk features [0.0, 1.0].
        
        Returns:
            float: Tau Score [0.0, 1.0]
        """
        risk_sum = 0.0
        
        for feature, value in features.items():
            weight = self.weights.get(feature, 1.0)
            risk_sum += value * weight
            
        # Sigmoid function: 1 / (1 + exp(-x))
        # We want high risk -> low score.
        # So we do: score = sigmoid(baseline - risk_sum)
        # If risk is 0, score -> sigmoid(5) ~= 0.99
        # If risk is high (e.g. sum=10), score -> sigmoid(-5) ~= 0.006
        
        logit = self.baseline - risk_sum
        score = 1.0 / (1.0 + math.exp(-logit))
        
        return score

    def classify_risk(self, score: float) -> str:
        """Classify Tau Score into risk categories."""
        if score >= 0.8:
            return "LOW"
        elif score >= 0.5:
            return "MID"
        elif score >= 0.2:
            return "HIGH"
        else:
            return "CRITICAL"
