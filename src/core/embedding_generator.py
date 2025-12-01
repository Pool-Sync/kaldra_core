"""
Embedding Generator for KALDRA Core v2.3

Unified embedding generation with support for multiple providers:
- Sentence Transformers (primary)
- OpenAI (via requests or client injection)
- Cohere (skeleton via client injection)
- Legacy (deterministic simulation)
- Custom (via callback)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Sequence, Union
import os
import json
import requests
import numpy as np

from src.core.embedding_cache import (
    BaseEmbeddingCache,
    InMemoryEmbeddingCache,
    make_embedding_cache_key,
)
from src.core.hardening.retries import with_retries
from src.core.hardening.circuit_breaker import circuit_breaker
from src.core.hardening.fallbacks import safe_fallback
from src.core.hardening.timeouts import with_timeout

# Optional import for sentence-transformers.
try:  # pragma: no cover - import guard
    from sentence_transformers import SentenceTransformer  # type: ignore
except ImportError:  # pragma: no cover - import guard
    SentenceTransformer = None  # type: ignore[assignment]


TextLike = Union[str, Sequence[str]]


@dataclass
class EmbeddingConfig:
    """
    Configuration for EmbeddingGenerator.

    provider:
      - "sentence-transformers"
      - "openai"
      - "cohere"
      - "legacy" (deterministic simulation)
      - "custom"

    model_name:
      - e.g. "all-MiniLM-L6-v2" for ST
      - e.g. "text-embedding-3-small" for OpenAI
    """

    provider: str = "sentence-transformers"
    model_name: str = "all-MiniLM-L6-v2"
    normalize: bool = True
    batch_size: int = 16
    device: Optional[str] = None
    dim: Optional[int] = None  # expected output dimension (optional)
    api_key: Optional[str] = None # For OpenAI/Cohere


class EmbeddingGenerator:
    """
    Unified embedding generator for KALDRA Core.

    Responsibilities:
      - Load / manage embedding backends
      - Normalize text input
      - Apply caching when configured
      - Return np.ndarray[float32] with shape (N, D)
    """

    def __init__(
        self,
        config: Optional[EmbeddingConfig] = None,
        cache: Optional[BaseEmbeddingCache] = None,
        openai_client: Any = None,
        cohere_client: Any = None,
        custom_encoder: Optional[Callable[[Sequence[str]], np.ndarray]] = None,
    ) -> None:
        self.config = config or EmbeddingConfig()
        self.cache = cache or InMemoryEmbeddingCache()
        self.openai_client = openai_client
        self.cohere_client = cohere_client
        self.custom_encoder = custom_encoder

        self._st_model: Any = None  # lazy-loaded sentence-transformers model

    # --------------------
    # Public API
    # --------------------
    def encode(self, texts: TextLike) -> np.ndarray:
        """
        Encode a single string or a batch of strings into embeddings.

        Returns:
            np.ndarray with shape (N, D), dtype=float32
        """
        batch = self._normalize_input(texts)

        # Try cache first (batch-level key).
        cache_key = make_embedding_cache_key(
            provider=self.config.provider,
            model_name=self.config.model_name,
            texts=batch,
        )
        if self.cache is not None:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached

        # Compute embeddings based on provider.
        if self.config.provider == "sentence-transformers":
            embeddings = self._encode_sentence_transformers(batch)
        elif self.config.provider == "openai":
            embeddings = self._encode_openai(batch)
        elif self.config.provider == "cohere":
            embeddings = self._encode_cohere(batch)
        elif self.config.provider == "legacy":
            embeddings = self._encode_legacy(batch)
        elif self.config.provider == "custom":
            embeddings = self._encode_custom(batch)
        else:
            raise ValueError(f"Unknown embedding provider: {self.config.provider}")

        embeddings = self._postprocess(embeddings)

        # Store in cache.
        if self.cache is not None:
            self.cache.set(cache_key, embeddings)

        return embeddings

    # --------------------
    # Internal helpers
    # --------------------
    def _normalize_input(self, texts: TextLike) -> List[str]:
        if isinstance(texts, str):
            batch = [texts]
        else:
            batch = list(texts)

        return [t.strip() for t in batch]

    def _ensure_dim(self, arr: np.ndarray) -> np.ndarray:
        """
        Ensure array is 2D (N, D).
        """
        if arr.ndim == 1:
            arr = arr[None, :]
        if arr.dtype != np.float32:
            arr = arr.astype(np.float32)
        return arr

    def _normalize_l2(self, arr: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(arr, axis=1, keepdims=True)
        norms = np.where(norms == 0.0, 1.0, norms)
        return arr / norms

    def _postprocess(self, arr: np.ndarray) -> np.ndarray:
        arr = self._ensure_dim(arr)
        if self.config.normalize:
            arr = self._normalize_l2(arr)

        # Respect config.dim if provided.
        if self.config.dim is not None and arr.shape[1] != self.config.dim:
            # Soft assertion: do not crash, but log shape mismatch in the future.
            # For now, we just return the raw array.
            pass
        return arr

    # --------------------
    # Provider-specific encoders
    # --------------------
    def _encode_sentence_transformers(self, texts: Sequence[str]) -> np.ndarray:
        if SentenceTransformer is None:
            raise RuntimeError(
                "sentence-transformers is not installed. "
                "Install via `pip install sentence-transformers`."
            )

        if self._st_model is None:
            # Lazy initialization.
            if self.config.device is not None:
                self._st_model = SentenceTransformer(self.config.model_name, device=self.config.device)
            else:
                self._st_model = SentenceTransformer(self.config.model_name)

        # sentence-transformers already supports batching internally.
        emb = self._st_model.encode(
            list(texts),
            batch_size=self.config.batch_size,
            convert_to_numpy=True,
            normalize_embeddings=False,
        )
        return np.asarray(emb, dtype=np.float32)

    @circuit_breaker(name="openai_embeddings", fail_threshold=3, reset_time=60)
    @with_retries(max_attempts=3, backoff=1.0)
    @with_timeout(seconds=10)
    def _encode_openai(self, texts: Sequence[str]) -> np.ndarray:
        """
        OpenAI embeddings via requests or injected client.
        """
        # 1. Use injected client if available
        if self.openai_client is not None:
            response = self.openai_client.embeddings.create(
                model=self.config.model_name,
                input=list(texts),
            )
            vectors = [np.array(item.embedding, dtype=np.float32) for item in response.data]
            return np.vstack(vectors)

        # 2. Use requests if API key is provided
        if self.config.api_key:
            url = "https://api.openai.com/v1/embeddings"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key}"
            }
            payload = {
                "model": self.config.model_name,
                "input": list(texts)
            }
            
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=10)
                response.raise_for_status()
                data = response.json()
                vectors = [np.array(item["embedding"], dtype=np.float32) for item in data["data"]]
                return np.vstack(vectors)
            except Exception as e:
                print(f"OpenAI Embedding Error: {e}")
                # Fallback to legacy if configured or raise? 
                # For now, let's raise to be explicit about failure in REAL mode.
                raise RuntimeError(f"OpenAI API failed: {e}")

        raise RuntimeError(
            "OpenAI provider selected but no client injected and no API key in config."
        )

    @circuit_breaker(name="cohere_embeddings", fail_threshold=3, reset_time=60)
    @with_retries(max_attempts=3, backoff=1.0)
    @with_timeout(seconds=10)
    def _encode_cohere(self, texts: Sequence[str]) -> np.ndarray:
        """
        Skeleton for Cohere embeddings.
        """
        if self.cohere_client is None:
            raise RuntimeError(
                "cohere_client is not configured. "
                "Pass a Cohere client instance to EmbeddingGenerator(cohere_client=...)."
            )

        resp = self.cohere_client.embed(
            texts=list(texts),
            model=self.config.model_name,
        )
        # Adjust depending on actual API; here we assume `resp.embeddings`.
        vectors = [np.array(vec, dtype=np.float32) for vec in resp.embeddings]
        return np.vstack(vectors)

    def _encode_legacy(self, texts: Sequence[str]) -> np.ndarray:
        """
        Deterministic simulation based on text hash.
        Used for testing and fallback.
        """
        dim = self.config.dim or 256
        vectors = []
        for text in texts:
            # Seed based on text content
            seed = sum(ord(c) for c in text) % (2**32)
            rng = np.random.RandomState(seed)
            
            # Generate random vector
            vec = rng.randn(dim)
            vectors.append(vec)
            
        return np.vstack(vectors).astype(np.float32)

    def _encode_custom(self, texts: Sequence[str]) -> np.ndarray:
        """
        Custom encoder integration.
        """
        if self.custom_encoder is None:
            raise RuntimeError(
                "custom_encoder is not configured. "
                "Pass a callable to EmbeddingGenerator(custom_encoder=...)."
            )

        arr = self.custom_encoder(list(texts))
        return np.asarray(arr, dtype=np.float32)
