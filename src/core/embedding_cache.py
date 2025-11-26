"""
Embedding Cache Layer for KALDRA Core v2.3

Provides caching infrastructure for embeddings to avoid redundant computation.
Supports in-memory and Redis-backed caching.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from typing import Dict, Optional, Sequence

import numpy as np


def _normalize_text_batch(texts: Sequence[str]) -> Sequence[str]:
    """
    Normalize a batch of texts into a consistent representation for hashing.
    """
    return [t.strip() for t in texts]


def make_embedding_cache_key(
    provider: str,
    model_name: str,
    texts: Sequence[str],
) -> str:
    """
    Build a deterministic cache key for a batch of texts.

    The same (provider, model, texts) tuple must always yield the same key.
    
    Args:
        provider: Embedding provider name (e.g., "sentence-transformers")
        model_name: Model identifier (e.g., "all-MiniLM-L6-v2")
        texts: Sequence of text strings to encode
    
    Returns:
        Deterministic cache key string
    """
    normalized = _normalize_text_batch(texts)
    joined = "\n".join(normalized).encode("utf-8")
    digest = sha256(joined).hexdigest()
    return f"{provider}:{model_name}:{digest}"


class BaseEmbeddingCache:
    """
    Abstract base class for embedding caches.

    Implementations must override:
      - get(key) -> Optional[np.ndarray]
      - set(key, value) -> None
    """

    def get(self, key: str) -> Optional[np.ndarray]:  # pragma: no cover - interface
        raise NotImplementedError

    def set(self, key: str, value: np.ndarray) -> None:  # pragma: no cover - interface
        raise NotImplementedError


@dataclass
class InMemoryEmbeddingCache(BaseEmbeddingCache):
    """
    Simple in-memory cache based on a Python dict.

    Suitable for:
      - local development
      - small-scale experiments
      - unit / integration tests
    """

    _store: Dict[str, np.ndarray] = field(default_factory=dict)

    def get(self, key: str) -> Optional[np.ndarray]:
        return self._store.get(key)

    def set(self, key: str, value: np.ndarray) -> None:
        # Store a copy to avoid external mutation.
        self._store[key] = np.array(value, copy=True)


@dataclass
class RedisEmbeddingCache(BaseEmbeddingCache):
    """
    Redis-backed cache for embeddings.

    This is an optional integration:
      - requires the `redis` package
      - requires a running Redis instance
    """

    client: "object"  # expected to be a redis.Redis-like client
    namespace: str = "kaldra:embeddings"

    def _full_key(self, key: str) -> str:
        return f"{self.namespace}:{key}"

    def get(self, key: str) -> Optional[np.ndarray]:
        full_key = self._full_key(key)
        raw = self.client.get(full_key)
        if raw is None:
            return None
        try:
            arr = np.frombuffer(raw, dtype=np.float32)
            return arr
        except Exception:
            # Corrupted or incompatible data; treat as cache miss.
            return None

    def set(self, key: str, value: np.ndarray) -> None:
        full_key = self._full_key(key)
        arr = np.asarray(value, dtype=np.float32)
        # Store raw bytes; caller is responsible for dim consistency.
        self.client.set(full_key, arr.tobytes())


def export_cache_to_disk(cache: InMemoryEmbeddingCache, path: str | Path) -> None:
    """
    Utility for debugging: export an InMemoryEmbeddingCache to disk as raw numpy arrays.

    Not used by core logic; safe helper for experiments.
    
    Args:
        cache: InMemoryEmbeddingCache instance to export
        path: File path for export
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("wb") as f:
        # Very simple, non-portable binary dump (for debugging only).
        for key, value in cache._store.items():
            key_bytes = key.encode("utf-8")
            f.write(len(key_bytes).to_bytes(4, "big"))
            f.write(key_bytes)
            arr = np.asarray(value, dtype=np.float32)
            f.write(len(arr).to_bytes(4, "big"))
            f.write(arr.tobytes())
