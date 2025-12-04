"""
Tests for Ensemble Embedder.
"""
import pytest
import numpy as np
from src.embeddings.ensemble_embedder import EnsembleEmbedder

class TestEnsembleEmbedder:
    
    def test_embed_text(self):
        embedder = EnsembleEmbedder(embedding_dim=10)
        vec = embedder.embed_text("Test text")
        assert isinstance(vec, np.ndarray)
        assert vec.shape == (10,)
        
    def test_embed_structured(self):
        embedder = EnsembleEmbedder(embedding_dim=10)
        data = {"key": "value"}
        vec = embedder.embed_structured(data)
        assert vec.shape == (10,)
        
    def test_merge_embeddings_mean(self):
        embedder = EnsembleEmbedder(embedding_dim=2)
        v1 = np.array([1.0, 2.0])
        v2 = np.array([3.0, 4.0])
        
        merged = embedder.merge_embeddings([v1, v2])
        expected = np.array([2.0, 3.0])
        
        np.testing.assert_array_almost_equal(merged, expected)
        
    def test_merge_embeddings_weighted(self):
        embedder = EnsembleEmbedder(embedding_dim=2)
        v1 = np.array([1.0, 0.0])
        v2 = np.array([0.0, 1.0])
        weights = [0.8, 0.2]
        
        merged = embedder.merge_embeddings([v1, v2], weights=weights)
        expected = np.array([0.8, 0.2])
        
        np.testing.assert_array_almost_equal(merged, expected)
        
    def test_merge_empty(self):
        embedder = EnsembleEmbedder(embedding_dim=5)
        merged = embedder.merge_embeddings([])
        assert np.all(merged == 0)
        assert merged.shape == (5,)
