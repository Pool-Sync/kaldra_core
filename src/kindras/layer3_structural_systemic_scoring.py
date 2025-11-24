from typing import Dict, Any, List
from .layer3_structural_systemic_loader import KindraVectorL3

class Layer3Scorer:
    """
    Calculates the intensity of Layer 3 (Structural / Systemic) vectors based on structural context.
    """

    def __init__(self):
        pass

    def score(self, context: Dict[str, Any], vectors: List[KindraVectorL3]) -> Dict[str, float]:
        """
        Computes a normalized score for each vector based on structural/systemic context.

        Args:
            context: Dictionary containing structural data (e.g., {'regime_type': 'democracy'}).
            vectors: List of loaded KindraVectorL3 objects.

        Returns:
            Dict[str, float]: Mapping of vector_id -> score.
        """
        scores: Dict[str, float] = {}
        
        overrides = context.get('layer3_overrides', {})

        for vector in vectors:
            if vector.id in overrides:
                scores[vector.id] = float(overrides[vector.id])
            else:
                # Default baseline
                scores[vector.id] = 0.0
                
        return scores
