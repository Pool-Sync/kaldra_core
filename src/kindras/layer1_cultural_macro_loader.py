import json
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class KindraVectorL1:
    id: str
    layer: str
    domain: str
    tw_plane: str
    scale_type: str
    scale_direction: str
    weight: float
    short_name: str
    objective_definition: str
    examples: List[str]
    narrative_role: str

class Layer1Loader:
    """
    Responsible for loading and validating Layer 1 (Cultural Macro) vectors.
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.vectors: Dict[str, KindraVectorL1] = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Kindra Layer 1 file not found: {self.file_path}")
            
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for item in data:
            vector = KindraVectorL1(
                id=item['id'],
                layer=item['layer'],
                domain=item['domain'],
                tw_plane=item['tw_plane'],
                scale_type=item.get('scale_type', 'spectrum'),
                scale_direction=item.get('scale_direction', ''),
                weight=item.get('weight', 1.0),
                short_name=item['short_name'],
                objective_definition=item['objective_definition'],
                examples=item.get('examples', []),
                narrative_role=item.get('narrative_role', '')
            )
            self.vectors[vector.id] = vector

    def get_vector(self, vector_id: str) -> Optional[KindraVectorL1]:
        return self.vectors.get(vector_id)

    def get_all_vectors(self) -> List[KindraVectorL1]:
        return list(self.vectors.values())

    def get_by_domain(self, domain: str) -> List[KindraVectorL1]:
        return [v for v in self.vectors.values() if v.domain == domain]
