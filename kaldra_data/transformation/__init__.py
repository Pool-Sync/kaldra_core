"""
Transformation module for KALDRA Data Lab.

Handles embedding generation and other transformations.
"""

from kaldra_data.transformation.embedding_router import (
    EmbeddingRouter,
    EmbeddingRouterConfig,
    make_default_router,
)

__all__ = [
    "EmbeddingRouter",
    "EmbeddingRouterConfig",
    "make_default_router",
]
