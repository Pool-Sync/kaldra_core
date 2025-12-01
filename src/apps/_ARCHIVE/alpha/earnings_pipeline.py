"""End-to-end KALDRA-Alpha earnings pipeline (text → embedding → KaldraSignal)."""

from dataclasses import dataclass
from typing import Any, Dict, Optional
import logging

import numpy as np

from src.core.kaldra_master_engine import KaldraMasterEngineV2
from kaldra_data.transformation.embedding_router import EmbeddingRouter, EmbeddingRouterConfig
from src.apps.alpha.earnings_ingest import EarningsSource, load_earnings_text, normalize_earnings_text

logger = logging.getLogger(__name__)

@dataclass
class EarningsPipelineResult:
    """Result of the earnings analysis pipeline."""
    story_id: Optional[str]
    ticker: Optional[str]
    quarter: Optional[str]
    raw_text: str
    cleaned_text: str
    embedding: np.ndarray  # shape (D,) or (1, D)
    signal: Any  # KaldraSignal-like
    metadata: Dict[str, Any]


def run_earnings_pipeline(
    source: EarningsSource,
    engine: KaldraMasterEngineV2,
    embedding_dim: Optional[int] = None,
    use_fallback_embeddings: bool = True,
) -> EarningsPipelineResult:
    """
    Run full earnings pipeline:
    - Load + normalize text
    - Compute embeddings via EmbeddingRouter
    - Call KaldraMasterEngineV2.infer_from_embedding(...)
    - Return structured result
    """
    # 1. Load and normalize text
    try:
        raw_text = load_earnings_text(source)
    except Exception as e:
        logger.error(f"Failed to load earnings text: {e}")
        raise

    cleaned_text = normalize_earnings_text(raw_text)
    if not cleaned_text:
        raise ValueError("Earnings text is empty after normalization.")

    # 2. Configure Embedding Router
    # If use_fallback_embeddings is True, we force the fallback provider
    # Otherwise we use the default (SentenceTransformers) but allow fallback on error
    
    target_dim = embedding_dim or engine.d_ctx
    
    if use_fallback_embeddings:
        router_config = EmbeddingRouterConfig(
            provider="fallback",
            dim=target_dim,
            use_fallback=True
        )
    else:
        router_config = EmbeddingRouterConfig(
            provider="sentence-transformers",
            dim=target_dim,
            use_fallback=True
        )
        
    router = EmbeddingRouter(config=router_config)

    # 3. Generate Embedding
    # get_embedding returns np.ndarray with shape (N, D) where N is batch size
    # For single text, N=1, so we need to extract the first row
    embedding_array = router.get_embedding(cleaned_text)
    
    # Ensure 1D for engine (engine expects (D,))
    if embedding_array.ndim > 1:
        embedding_array = embedding_array[0]  # Get first row for single text

    # 4. Infer Signal
    signal = engine.infer_from_embedding(embedding_array)

    # 5. Construct Result
    metadata = {
        "provider": router.config.provider,
        "embedding_dim": embedding_array.shape[0],
        "tw_trigger": getattr(signal, "tw_trigger", False),
        "epistemic_status": getattr(signal.epistemic, "status", "UNKNOWN") if hasattr(signal, "epistemic") else "UNKNOWN"
    }

    return EarningsPipelineResult(
        story_id=None, # Placeholder for future Story Aggregation integration
        ticker=source.ticker,
        quarter=source.quarter,
        raw_text=raw_text,
        cleaned_text=cleaned_text,
        embedding=embedding_array,
        signal=signal,
        metadata=metadata
    )
