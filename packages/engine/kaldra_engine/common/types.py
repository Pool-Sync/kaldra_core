from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class TWState:
    """
    Represents the state of the TW369 engine with inputs from all three Kindra layers.
    
    Attributes:
        plane3_cultural_macro: Layer 1 vector scores (Dict[vector_id, score])
        plane6_semiotic_media: Layer 2 vector scores
        plane9_structural_systemic: Layer 3 vector scores
        metadata: Additional context information
    """
    plane3_cultural_macro: Optional[Dict[str, float]] = None
    plane6_semiotic_media: Optional[Dict[str, float]] = None
    plane9_structural_systemic: Optional[Dict[str, float]] = None
    metadata: Optional[Dict[str, Any]] = None
