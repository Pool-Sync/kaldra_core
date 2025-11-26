"""
Usage Examples for KALDRA Embedding Generation & Cache Layer

This module demonstrates how to use the new embedding infrastructure.
"""

import numpy as np

from src.core.embedding_cache import InMemoryEmbeddingCache, make_embedding_cache_key
from src.core.embedding_generator import EmbeddingConfig, EmbeddingGenerator


def example_1_basic_usage():
    """
    Example 1: Basic usage with default Sentence Transformers
    
    NOTE: Requires sentence-transformers to be installed:
          pip install sentence-transformers
    """
    print("=" * 60)
    print("Example 1: Basic Sentence Transformers Usage")
    print("=" * 60)
    
    # Create generator with default config
    generator = EmbeddingGenerator()
    
    # Encode single text
    text = "The company reported strong earnings growth."
    embedding = generator.encode(text)
    
    print(f"Input: {text}")
    print(f"Embedding shape: {embedding.shape}")
    print(f"Embedding dtype: {embedding.dtype}")
    print(f"First 5 values: {embedding[0, :5]}")
    print()


def example_2_batch_encoding():
    """
    Example 2: Batch encoding with caching
    """
    print("=" * 60)
    print("Example 2: Batch Encoding with Cache")
    print("=" * 60)
    
    # Create generator with explicit cache
    cache = InMemoryEmbeddingCache()
    generator = EmbeddingGenerator(cache=cache)
    
    # Encode batch
    texts = [
        "Financial markets showed strong performance.",
        "Geopolitical tensions escalated in the region.",
        "User experience improvements drove engagement.",
    ]
    
    # First call - computes embeddings
    embeddings_1 = generator.encode(texts)
    print(f"First call - computed {len(texts)} embeddings")
    print(f"Shape: {embeddings_1.shape}")
    
    # Second call - uses cache
    embeddings_2 = generator.encode(texts)
    print(f"Second call - retrieved from cache")
    print(f"Results identical: {np.allclose(embeddings_1, embeddings_2)}")
    print(f"Cache size: {len(cache._store)} entries")
    print()


def example_3_custom_config():
    """
    Example 3: Custom configuration
    """
    print("=" * 60)
    print("Example 3: Custom Configuration")
    print("=" * 60)
    
    # Custom config with specific model and settings
    config = EmbeddingConfig(
        provider="sentence-transformers",
        model_name="all-MiniLM-L6-v2",
        normalize=True,
        batch_size=8,
        dim=384,  # Expected dimension for this model
    )
    
    generator = EmbeddingGenerator(config=config)
    
    text = "Custom configuration example"
    embedding = generator.encode(text)
    
    print(f"Model: {config.model_name}")
    print(f"Normalize: {config.normalize}")
    print(f"Output shape: {embedding.shape}")
    print(f"L2 norm: {np.linalg.norm(embedding[0]):.4f}")  # Should be ~1.0 if normalized
    print()


def example_4_custom_encoder():
    """
    Example 4: Custom encoder (no external dependencies)
    """
    print("=" * 60)
    print("Example 4: Custom Encoder (Deterministic)")
    print("=" * 60)
    
    # Define custom encoder (simple hash-based for demo)
    def custom_hash_encoder(texts):
        """Simple deterministic encoder for testing"""
        embeddings = []
        for text in texts:
            # Use hash to create deterministic vector
            hash_val = hash(text)
            np.random.seed(abs(hash_val) % (2**32))
            vec = np.random.randn(128).astype(np.float32)
            embeddings.append(vec)
        return np.vstack(embeddings)
    
    # Create generator with custom encoder
    config = EmbeddingConfig(provider="custom", dim=128)
    generator = EmbeddingGenerator(
        config=config,
        custom_encoder=custom_hash_encoder
    )
    
    texts = ["Test text 1", "Test text 2"]
    embeddings = generator.encode(texts)
    
    print(f"Custom encoder used")
    print(f"Output shape: {embeddings.shape}")
    print(f"Deterministic: {np.allclose(embeddings, generator.encode(texts))}")
    print()


def example_5_cache_key_generation():
    """
    Example 5: Understanding cache keys
    """
    print("=" * 60)
    print("Example 5: Cache Key Generation")
    print("=" * 60)
    
    texts_1 = ["Hello world", "Goodbye world"]
    texts_2 = ["Hello world", "Goodbye world"]  # Same content
    texts_3 = ["Goodbye world", "Hello world"]  # Different order
    
    key_1 = make_embedding_cache_key("st", "model-v1", texts_1)
    key_2 = make_embedding_cache_key("st", "model-v1", texts_2)
    key_3 = make_embedding_cache_key("st", "model-v1", texts_3)
    
    print(f"Key 1: {key_1[:50]}...")
    print(f"Key 2: {key_2[:50]}...")
    print(f"Key 3: {key_3[:50]}...")
    print()
    print(f"Same content → same key: {key_1 == key_2}")
    print(f"Different order → different key: {key_1 != key_3}")
    print()


def example_6_openai_skeleton():
    """
    Example 6: OpenAI provider skeleton (requires client injection)
    """
    print("=" * 60)
    print("Example 6: OpenAI Provider (Skeleton)")
    print("=" * 60)
    
    # This would require an actual OpenAI client
    # from openai import OpenAI
    # client = OpenAI(api_key="...")
    
    config = EmbeddingConfig(
        provider="openai",
        model_name="text-embedding-3-small"
    )
    
    # generator = EmbeddingGenerator(config=config, openai_client=client)
    # embeddings = generator.encode("Example text")
    
    print("OpenAI provider requires:")
    print("  1. Install: pip install openai")
    print("  2. Create client: client = OpenAI(api_key='...')")
    print("  3. Pass to generator: EmbeddingGenerator(openai_client=client)")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("KALDRA Embedding Generator - Usage Examples")
    print("=" * 60 + "\n")
    
    # Run examples that don't require sentence-transformers
    example_4_custom_encoder()
    example_5_cache_key_generation()
    example_6_openai_skeleton()
    
    # These require sentence-transformers to be installed
    # Uncomment if you have it installed:
    # example_1_basic_usage()
    # example_2_batch_encoding()
    # example_3_custom_config()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)
