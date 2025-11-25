import json
import os
from typing import Dict, List

class Layer2Delta144Bridge:
    """
    Connects Layer 2 (Semiotic / Media) vectors to Δ144 states.
    Uses the mapping file to adjust state probabilities based on vector scores.
    """

    def __init__(self, map_file_path: str):
        self.map_file_path = map_file_path
        self.mapping = self._load_mapping()

    def _load_mapping(self) -> Dict[str, Dict[str, List[str]]]:
        if not os.path.exists(self.map_file_path):
            raise FileNotFoundError(f"Mapping file not found: {self.map_file_path}")
        with open(self.map_file_path, 'r', encoding='utf-8') as f:
            mapping_list = json.load(f)
            # Convert list to dict indexed by vector ID
            return {entry["id"]: entry for entry in mapping_list}

    def apply(self, base_distribution: Dict[str, float], kindra_scores: Dict[str, float]) -> Dict[str, float]:
        """
        Adjusts the Δ144 distribution based on Kindra Layer 2 scores.
        Layer 2 typically has a higher impact factor due to media amplification/distortion.
        """
        adjusted = base_distribution.copy()
        
        # Layer 2 might have stronger amplification effects
        IMPACT_FACTOR = 0.25

        for vector_id, score in kindra_scores.items():
            if vector_id not in self.mapping:
                continue
            
            if score == 0:
                continue

            map_data = self.mapping[vector_id]
            boost_targets = map_data.get('boost', [])
            suppress_targets = map_data.get('suppress', [])

            effective_boost = boost_targets if score > 0 else suppress_targets
            effective_suppress = suppress_targets if score > 0 else boost_targets
            abs_score = abs(score)

            for target in effective_boost:
                if target in adjusted:
                    adjusted[target] *= (1 + (abs_score * IMPACT_FACTOR))
            
            for target in effective_suppress:
                if target in adjusted:
                    adjusted[target] *= (1 - (abs_score * IMPACT_FACTOR))
                    if adjusted[target] < 0:
                        adjusted[target] = 0.0

        return adjusted
