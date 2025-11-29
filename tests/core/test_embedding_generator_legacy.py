"""
Tests for EmbeddingGenerator Legacy Mode.
"""

import unittest
import numpy as np
from src.core.embedding_generator import EmbeddingGenerator, EmbeddingConfig

class TestEmbeddingGeneratorLegacy(unittest.TestCase):

    def test_legacy_mode_deterministic(self):
        """Test that legacy mode produces deterministic embeddings based on text."""
        config = EmbeddingConfig(provider="legacy", dim=128)
        generator = EmbeddingGenerator(config=config)
        
        text = "Test text"
        emb1 = generator.encode(text)
        emb2 = generator.encode(text)
        
        # Shape check
        self.assertEqual(emb1.shape, (1, 128))
        
        # Determinism check
        np.testing.assert_array_almost_equal(emb1, emb2)
        
        # Different text check
        emb3 = generator.encode("Different text")
        self.assertFalse(np.allclose(emb1, emb3))

    def test_legacy_mode_batch(self):
        """Test batch encoding in legacy mode."""
        config = EmbeddingConfig(provider="legacy", dim=64)
        generator = EmbeddingGenerator(config=config)
        
        texts = ["Text A", "Text B"]
        embs = generator.encode(texts)
        
        self.assertEqual(embs.shape, (2, 64))
        
        # Verify individual encoding matches batch
        emb_a = generator.encode("Text A")
        np.testing.assert_array_almost_equal(embs[0:1], emb_a)

if __name__ == "__main__":
    unittest.main()
