import json
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class KindraVectorL3:
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

class Layer3Loader:
    """
    Responsible for loading and validating Layer 3 (Structural / Systemic) vectors.
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.vectors: Dict[str, KindraVectorL3] = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Kindra Layer 3 file not found: {self.file_path}")
            
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for item in data:
            vector = KindraVectorL3(
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

    def get_vector(self, vector_id: str) -> Optional[KindraVectorL3]:
        return self.vectors.get(vector_id)

    def get_all_vectors(self) -> List[KindraVectorL3]:
        return list(self.vectors.values())

    def get_by_domain(self, domain: str) -> List[KindraVectorL3]:
        return [v for v in self.vectors.values() if v.domain == domain]
