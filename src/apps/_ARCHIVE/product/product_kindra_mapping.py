"""Product/brand narrative analysis using Kindra mappings."""

from dataclasses import dataclass, field
from typing import Optional, Any
import logging

import numpy as np

from src.core.kaldra_master_engine import KaldraMasterEngineV2
from kaldra_data.transformation.embedding_router import EmbeddingRouter, EmbeddingRouterConfig

logger = logging.getLogger(__name__)


@dataclass
class ProductNarrativeInput:
    """Input for product narrative analysis."""
    text: str
    product_id: Optional[str] = None
    category: Optional[str] = None
    channel: Optional[str] = None  # "review", "social", "support", etc.
    metadata: Optional[dict] = None


@dataclass
class ProductKindraMapping:
    """Product-specific Kindra layer mappings."""
    kindra_layer1: dict = field(default_factory=dict)  # Cultural macro vectors
    kindra_layer2: dict = field(default_factory=dict)  # Narrative modulation
    kindra_layer3: dict = field(default_factory=dict)  # Fine-grained adjustments
    dominant_vectors: list = field(default_factory=list)
    archetype_top_indices: list = field(default_factory=list)
    domain: str = "PRODUCT"


def map_text_to_product_kindra(
    text: str,
    engine: KaldraMasterEngineV2,
    product_id: Optional[str] = None,
    category: Optional[str] = None,
) -> ProductKindraMapping:
    """
    Map text to product-specific Kindra layers.
    
    Args:
        text: Input text (review, feedback, etc.)
        engine: KaldraMasterEngineV2 instance
        product_id: Product identifier
        category: Product category
    
    Returns:
        ProductKindraMapping with Kindra layer information
    
    Raises:
        ValueError: If text is empty
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty")
    
    # 1. Generate embedding using fallback provider
    router_config = EmbeddingRouterConfig(
        provider="fallback",
        dim=engine.d_ctx,
        use_fallback=True
    )
    router = EmbeddingRouter(config=router_config)
    
    embedding_array = router.get_embedding(text.strip())
    if embedding_array.ndim > 1:
        embedding_array = embedding_array[0]
    
    # 2. Infer signal
    signal = engine.infer_from_embedding(embedding_array)
    
    # 3. Extract archetype information
    if hasattr(signal, "archetype_probs"):
        probs = np.array(signal.archetype_probs)
        top_indices = probs.argsort()[-5:][::-1]
        archetype_top_indices = [int(idx) for idx in top_indices]
    else:
        archetype_top_indices = []
    
    # 4. Extract Kindra layers (if available in signal)
    # TODO: Once KaldraSignal exposes Kindra metadata directly, extract here
    # For now, use placeholders based on archetype distribution
    
    kindra_layer1 = {}
    kindra_layer2 = {}
    kindra_layer3 = {}
    dominant_vectors = []
    
    # Placeholder logic: map top archetypes to cultural vectors
    if archetype_top_indices:
        # This is a simplified mapping; real implementation would use
        # the actual Kindra scoring system
        kindra_layer1 = {
            f"vector_{i}": float(probs[i]) 
            for i in archetype_top_indices[:3]
        }
        dominant_vectors = [f"vector_{archetype_top_indices[0]}"]
    
    logger.info(
        f"Product Kindra mapping complete: product_id={product_id}, "
        f"top_archetypes={archetype_top_indices[:3]}"
    )
    
    return ProductKindraMapping(
        kindra_layer1=kindra_layer1,
        kindra_layer2=kindra_layer2,
        kindra_layer3=kindra_layer3,
        dominant_vectors=dominant_vectors,
        archetype_top_indices=archetype_top_indices,
        domain="PRODUCT"
    )
