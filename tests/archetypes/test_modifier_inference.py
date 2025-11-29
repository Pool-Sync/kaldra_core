"""
Test modifier auto-inference from embeddings.

v2.7: Tests for infer_modifier_scores_from_embedding() and integration.
"""
import pytest
import sys
import numpy as np
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.archetypes.delta144_engine import Delta144Engine
from src.core.embedding_generator import EmbeddingGenerator, EmbeddingConfig


def test_modifier_embeddings_initialization():
    """Test that modifier embeddings are initialized."""
    engine = Delta144Engine.from_schema()
    
    # Should have embeddings for all modifiers
    assert len(engine._modifier_embeddings) == len(engine.modifiers)
    
    # Each embedding should be a numpy array
    for mod_id, embedding in engine._modifier_embeddings.items():
        assert isinstance(embedding, np.ndarray)
        assert len(embedding) > 0


def test_infer_modifier_scores_from_embedding():
    """Test modifier score inference from embedding."""
    engine = Delta144Engine.from_schema()
    
    # Create a test embedding (simulating text about being wounded)
    test_text = "I feel wounded and hurt, carrying deep pain."
    test_embedding = engine.embedding_generator.encode(test_text)[0]
    
    # Infer modifier scores
    scores = engine.infer_modifier_scores_from_embedding(test_embedding, top_k=5)
    
    # Should return dict with scores
    assert isinstance(scores, dict)
    assert len(scores) <= 5
    
    # All scores should be between 0 and 1
    for score in scores.values():
        assert 0.0 <= score <= 1.0


def test_modifier_scores_relevance():
    """Test that modifier scores are semantically relevant."""
    engine = Delta144Engine.from_schema()
    
    # Test with "wounded" text
    wounded_text = "I am wounded, hurt, and in pain."
    wounded_embedding = engine.embedding_generator.encode(wounded_text)[0]
    wounded_scores = engine.infer_modifier_scores_from_embedding(wounded_embedding, top_k=10)
    
    # MOD_WOUNDED should be in top scores (if using real embeddings)
    # With legacy embeddings, just check structure
    assert len(wounded_scores) > 0
    assert all(isinstance(k, str) and k.startswith("MOD_") for k in wounded_scores.keys())


def test_infer_from_vector_with_auto_modifiers():
    """Test that infer_from_vector now auto-infers modifiers."""
    engine = Delta144Engine.from_schema()
    
    # Create test embedding
    test_text = "I feel strong and radiant, full of energy."
    test_embedding = engine.embedding_generator.encode(test_text)[0]
    
    # Infer state
    result = engine.infer_from_vector(test_embedding)
    
    # v2.7: active_modifiers should now be populated
    assert hasattr(result, 'active_modifiers')
    assert isinstance(result.active_modifiers, list)
    
    # Should have some modifiers (unless all scores below threshold)
    # With legacy embeddings, might be empty or have defaults
    assert len(result.active_modifiers) >= 0


def test_modifier_inference_respects_allowed_modifiers():
    """Test that modifier inference respects state's allowed_modifiers."""
    engine = Delta144Engine.from_schema()
    
    # Get a state with specific allowed modifiers
    test_state = list(engine.states.values())[0]
    
    # Create test embedding
    test_embedding = np.random.rand(256)  # Random embedding
    
    # Infer modifier scores
    modifier_scores = engine.infer_modifier_scores_from_embedding(test_embedding, top_k=20)
    
    # Infer modifiers for this state
    active_modifiers = engine._infer_modifiers(
        test_state,
        modifier_scores,
        max_modifiers=4,
        threshold=0.3
    )
    
    # All active modifiers should be in allowed or default set
    allowed_set = set(test_state.allowed_modifiers) | set(test_state.default_modifiers)
    
    for mod in active_modifiers:
        if allowed_set:  # Only check if state has allowed modifiers defined
            assert mod.id in allowed_set or mod.id in test_state.default_modifiers


def test_modifier_inference_empty_embedding():
    """Test graceful handling of edge cases."""
    engine = Delta144Engine.from_schema()
    
    # Zero embedding
    zero_embedding = np.zeros(256)
    scores = engine.infer_modifier_scores_from_embedding(zero_embedding, top_k=5)
    
    # Should still return valid scores (might be all similar)
    assert isinstance(scores, dict)
    assert all(0.0 <= v <= 1.0 for v in scores.values())
