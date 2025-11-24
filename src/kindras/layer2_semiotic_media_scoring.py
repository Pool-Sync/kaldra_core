from typing import Dict, Any, List
from .layer2_semiotic_media_loader import KindraVectorL2

class Layer2Scorer:
    """
    Calculates the intensity of Layer 2 (Semiotic / Media) vectors based on media metrics and context.
    """

    def __init__(self):
        pass

    def score(self, context: Dict[str, Any], vectors: List[KindraVectorL2]) -> Dict[str, float]:
        """
        Computes a normalized score for each vector based on media context.

        Args:
            context: Dictionary containing media metrics (e.g., {'media_saturation': 'high'}).
            vectors: List of loaded KindraVectorL2 objects.

        Returns:
            Dict[str, float]: Mapping of vector_id -> score.
        """
        scores: Dict[str, float] = {}
        
        overrides = context.get('layer2_overrides', {})

        for vector in vectors:
            if vector.id in overrides:
                scores[vector.id] = float(overrides[vector.id])
            else:
                # Default baseline
                scores[vector.id] = 0.0
                
        return scores
