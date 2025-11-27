"""
KALDRA Data Lab → Embedding → Master Engine Pipeline Example

This example demonstrates the complete flow:
1. Data Lab: Clean and prepare text
2. Embedding Generator: Convert text to vectors
3. Master Engine: Interpret narrative signals

This is a simplified example showing the integration points.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import numpy as np

# Data Lab imports (using fallback if modules don't exist)
try:
    from kaldra_data.transformation import EmbeddingRouter, EmbeddingRouterConfig
except ImportError:
    print("⚠️  kaldra_data not available, using mock")
    EmbeddingRouter = None  # type: ignore

# Core imports
from src.core.kaldra_master_engine import KaldraMasterEngineV2


def example_1_basic_pipeline():
    """
    Example 1: Basic pipeline with fallback embeddings
    
    This works even without sentence-transformers installed.
    """
    print("=" * 70)
    print("Example 1: Basic Pipeline (Fallback Embeddings)")
    print("=" * 70)
    
    # Step 1: Simulated Data Lab output (cleaned text)
    cleaned_text = "The company reported strong earnings growth with revenue up 15%."
    
    # Step 2: Get embedding via router (uses fallback if ST not available)
    if EmbeddingRouter is not None:
        router = EmbeddingRouter(
            EmbeddingRouterConfig(
                provider="fallback",  # Force fallback for demo
                dim=256,
            )
        )
        embedding = router.get_embedding(cleaned_text)
    else:
        # Mock embedding if router not available
        embedding = np.random.randn(1, 256).astype(np.float32)
    
    print(f"Text: {cleaned_text}")
    print(f"Embedding shape: {embedding.shape}")
    print(f"Embedding dtype: {embedding.dtype}")
    
    # Step 3: Run Master Engine
    engine = KaldraMasterEngineV2(d_ctx=embedding.shape[1])
    signal = engine.infer_from_embedding(embedding[0])
    
    print(f"\nMaster Engine Output:")
    print(f"  Max probability: {signal.archetype_probs.max():.4f}")
    print(f"  Max archetype index: {signal.archetype_probs.argmax()}")
    print(f"  Has delta state: {signal.delta_state is not None}")
    print()


def example_2_sentence_transformers():
    """
    Example 2: Pipeline with Sentence Transformers
    
    Requires: pip install sentence-transformers
    """
    print("=" * 70)
    print("Example 2: Pipeline with Sentence Transformers")
    print("=" * 70)
    
    if EmbeddingRouter is None:
        print("⚠️  EmbeddingRouter not available, skipping")
        return
    
    # Step 1: Simulated Data Lab output
    texts = [
        "Financial markets showed strong performance this quarter.",
        "Geopolitical tensions escalated in the region.",
        "User experience improvements drove higher engagement.",
    ]
    
    # Step 2: Get embeddings via router
    try:
        router = EmbeddingRouter(
            EmbeddingRouterConfig(
                provider="sentence-transformers",
                model_name="all-MiniLM-L6-v2",
                dim=384,
            )
        )
        embeddings = router.get_embedding(texts)
        print(f"✅ Sentence Transformers embeddings generated")
    except Exception as e:
        print(f"⚠️  Sentence Transformers not available: {e}")
        print(f"   Using fallback...")
        router = EmbeddingRouter(
            EmbeddingRouterConfig(provider="fallback", dim=384)
        )
        embeddings = router.get_embedding(texts)
    
    print(f"Embeddings shape: {embeddings.shape}")
    
    # Step 3: Run Master Engine on each
    engine = KaldraMasterEngineV2(d_ctx=embeddings.shape[1])
    
    for i, text in enumerate(texts):
        signal = engine.infer_from_embedding(embeddings[i])
        print(f"\nText {i+1}: {text[:50]}...")
        print(f"  Max prob: {signal.archetype_probs.max():.4f}")
    print()


def example_3_batch_processing():
    """
    Example 3: Batch processing with chunking
    """
    print("=" * 70)
    print("Example 3: Batch Processing")
    print("=" * 70)
    
    if EmbeddingRouter is None:
        print("⚠️  EmbeddingRouter not available, skipping")
        return
    
    # Simulate large batch from Data Lab
    texts = [f"Sample text number {i} for batch processing." for i in range(50)]
    
    # Process in batches
    router = EmbeddingRouter(
        EmbeddingRouterConfig(
            provider="fallback",
            dim=256,
            batch_size=10,
        )
    )
    
    embeddings = router.get_embedding_batch(texts, batch_size=10)
    
    print(f"Processed {len(texts)} texts")
    print(f"Embeddings shape: {embeddings.shape}")
    
    # Run Master Engine on first few
    engine = KaldraMasterEngineV2(d_ctx=embeddings.shape[1])
    
    for i in range(min(3, len(texts))):
        signal = engine.infer_from_embedding(embeddings[i])
        print(f"\nText {i+1}: {texts[i]}")
        print(f"  Max archetype: {signal.archetype_probs.argmax()}")
    print()


def example_4_full_pipeline_simulation():
    """
    Example 4: Complete pipeline simulation
    
    Simulates: PDF → Clean → Embed → Engine
    """
    print("=" * 70)
    print("Example 4: Full Pipeline Simulation")
    print("=" * 70)
    
    # Step 1: Simulated PDF ingestion (Data Lab)
    raw_text = """
    META PLATFORMS Q1 2025 EARNINGS CALL
    
    Revenue: $36.5B (+15% YoY)
    Net Income: $12.4B
    Daily Active Users: 2.1B
    
    CEO Mark Zuckerberg discussed AI investments and Reality Labs progress.
    CFO highlighted strong advertising revenue growth across all regions.
    """
    
    # Step 2: Simulated cleaning (Data Lab preprocessing)
    cleaned_text = raw_text.strip().replace("\n    ", " ")
    
    print(f"Original text length: {len(raw_text)} chars")
    print(f"Cleaned text length: {len(cleaned_text)} chars")
    
    # Step 3: Embedding
    if EmbeddingRouter is not None:
        router = EmbeddingRouter(
            EmbeddingRouterConfig(provider="fallback", dim=384)
        )
        embedding = router.get_embedding(cleaned_text)
    else:
        embedding = np.random.randn(1, 384).astype(np.float32)
    
    print(f"Embedding shape: {embedding.shape}")
    
    # Step 4: Master Engine
    engine = KaldraMasterEngineV2(d_ctx=embedding.shape[1])
    signal = engine.infer_from_embedding(embedding[0])
    
    print(f"\nKALDRA Signal:")
    print(f"  Top 3 archetypes:")
    top_3 = np.argsort(signal.archetype_probs)[-3:][::-1]
    for idx in top_3:
        print(f"    Archetype {idx}: {signal.archetype_probs[idx]:.4f}")
    print(f"  Has delta state: {signal.delta_state is not None}")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("KALDRA Data Lab → Embedding → Master Engine Pipeline")
    print("=" * 70 + "\n")
    
    # Run all examples
    example_1_basic_pipeline()
    example_2_sentence_transformers()
    example_3_batch_processing()
    example_4_full_pipeline_simulation()
    
    print("=" * 70)
    print("All examples completed!")
    print("=" * 70)
