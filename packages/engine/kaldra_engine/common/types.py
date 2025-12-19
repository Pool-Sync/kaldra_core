from dataclasses import dataclass
from typing import Any


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

    plane3_cultural_macro: dict[str, float] | None = None
    plane6_semiotic_media: dict[str, float] | None = None
    plane9_structural_systemic: dict[str, float] | None = None
    metadata: dict[str, Any] | None = None
