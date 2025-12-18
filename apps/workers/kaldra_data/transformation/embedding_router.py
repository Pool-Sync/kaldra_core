"""
Embedding Router for KALDRA Data Lab

Connects cleaned text from Data Lab to the Embedding Generator,
providing a standardized interface for the full pipeline:
INGEST → CLEAN → PREP → EMBEDDING → MASTER ENGINE
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import List, Optional, Sequence, Union

import numpy as np

# Optional import for embedding generator
try:
    from src.core.embedding_generator import EmbeddingConfig, EmbeddingGenerator
except ImportError:
    EmbeddingGenerator = None  # type: ignore[assignment, misc]
    EmbeddingConfig = None  # type: ignore[assignment, misc]


TextLike = Union[str, Sequence[str]]


@dataclass
class EmbeddingRouterConfig:
    """
    Configuration for EmbeddingRouter.
    
    provider: "sentence-transformers" | "openai" | "cohere" | "custom" | "fallback"
    model_name: Model identifier for the provider
    dim: Expected embedding dimension
    use_fallback: If True, use deterministic fallback when provider fails
    """
    provider: str = "sentence-transformers"
    model_name: str = "all-MiniLM-L6-v2"
    dim: int = 384
    use_fallback: bool = True
    normalize: bool = True
    batch_size: int = 16


class EmbeddingRouter:
    """
    Router between Data Lab and Embedding Generator.
    
    Responsibilities:
    - Receive cleaned text from Data Lab
    - Route to appropriate embedding provider
    - Handle failures with deterministic fallback
    - Return embeddings ready for Master Engine
    """
    
    def __init__(self, config: Optional[EmbeddingRouterConfig] = None):
        self.config = config or EmbeddingRouterConfig()
        self._generator: Optional[object] = None
        
        # Try to initialize generator if available
        if EmbeddingGenerator is not None and self.config.provider != "fallback":
            try:
                emb_config = EmbeddingConfig(
                    provider=self.config.provider,
                    model_name=self.config.model_name,
                    normalize=self.config.normalize,
                    batch_size=self.config.batch_size,
                    dim=self.config.dim,
                )
                self._generator = EmbeddingGenerator(config=emb_config)
            except Exception as e:
                if not self.config.use_fallback:
                    raise
                # Fallback will be used
                self._generator = None
    
    def get_embedding(self, texts: TextLike) -> np.ndarray:
        """
        Get embeddings for text(s).
        
        Args:
            texts: Single string or list of strings
        
        Returns:
            np.ndarray with shape (N, D), dtype=float32
        """
        # Normalize input
        if isinstance(texts, str):
            batch = [texts]
        else:
            batch = list(texts)
        
        # Try generator first
        if self._generator is not None:
            try:
                return self._generator.encode(batch)
            except Exception as e:
                if not self.config.use_fallback:
                    raise
                # Fall through to fallback
        
        # Fallback: deterministic SHA256-based embeddings
        return self._fallback_embedding(batch)
    
    def _fallback_embedding(self, texts: Sequence[str]) -> np.ndarray:
        """
        Deterministic fallback embedding based on SHA256 hash.
        
        This ensures the pipeline never crashes due to missing dependencies.
        The embeddings are deterministic (same text → same embedding) but
        not semantically meaningful.
        
        Args:
            texts: List of strings
        
        Returns:
            np.ndarray with shape (len(texts), dim), dtype=float32
        """
        embeddings = []
        
        for text in texts:
            # Hash text to get deterministic seed
            hash_digest = sha256(text.encode('utf-8')).hexdigest()
            seed = int(hash_digest[:16], 16) % (2**32)
            
            # Generate deterministic vector
            rng = np.random.RandomState(seed)
            vec = rng.randn(self.config.dim).astype(np.float32)
            
            # Normalize if configured
            if self.config.normalize:
                norm = np.linalg.norm(vec)
                if norm > 0:
                    vec = vec / norm
            
            embeddings.append(vec)
        
        return np.vstack(embeddings)
    
    def get_embedding_batch(
        self,
        texts: Sequence[str],
        batch_size: Optional[int] = None,
    ) -> np.ndarray:
        """
        Get embeddings for a large batch of texts, processing in chunks.
        
        Args:
            texts: List of strings
            batch_size: Chunk size (default: from config)
        
        Returns:
            np.ndarray with shape (len(texts), dim), dtype=float32
        """
        batch_size = batch_size or self.config.batch_size
        
        if len(texts) <= batch_size:
            return self.get_embedding(texts)
        
        # Process in chunks
        embeddings = []
        for i in range(0, len(texts), batch_size):
            chunk = texts[i:i + batch_size]
            chunk_emb = self.get_embedding(chunk)
            embeddings.append(chunk_emb)
        
        return np.vstack(embeddings)


def make_default_router() -> EmbeddingRouter:
    """
    Factory function for creating a default EmbeddingRouter.
    
    Returns:
        EmbeddingRouter with default configuration
    """
    return EmbeddingRouter()
