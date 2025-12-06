"""
Ensemble Embedder for KALDRA v3.3.

Combines embeddings from multiple modalities (text, structured data, etc.).
"""
from typing import List, Dict, Any, Optional, Union
import numpy as np
import json

class EnsembleEmbedder:
    """
    Generates and merges embeddings from different data sources.
    """
    
    def __init__(self, embedding_dim: int = 768):
        self.embedding_dim = embedding_dim
        
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for text.
        
        STUB: Returns a random vector for Phase 1.
        In production, this would call a transformer model.
        """
        # Deterministic "random" vector based on text length for testing stability
        seed = len(text)
        rng = np.random.default_rng(seed)
        return rng.standard_normal(self.embedding_dim)
        
    def embed_structured(self, data: Dict[str, Any]) -> np.ndarray:
        """
        Generate embedding for structured data.
        
        Strategy: Flatten to JSON string and embed as text.
        """
        text_repr = json.dumps(data, sort_keys=True)
        return self.embed_text(text_repr)
        
    def merge_embeddings(self, embeddings: List[np.ndarray], weights: Optional[List[float]] = None) -> np.ndarray:
        """
        Merge multiple embeddings into a single vector.
        
        Args:
            embeddings: List of numpy arrays (must be same shape)
            weights: Optional list of weights. If None, uses uniform weighting (mean).
            
        Returns:
            Merged numpy array.
        """
        if not embeddings:
            return np.zeros(self.embedding_dim)
            
        if weights is None:
            # Simple mean
            return np.mean(embeddings, axis=0)
            
        if len(weights) != len(embeddings):
            raise ValueError("Length of weights must match length of embeddings")
            
        # Normalize weights
        total_weight = sum(weights)
        if total_weight == 0:
            norm_weights = [1.0 / len(weights)] * len(weights)
        else:
            norm_weights = [w / total_weight for w in weights]
            
        # Weighted sum
        merged = np.zeros_like(embeddings[0])
        for emb, w in zip(embeddings, norm_weights):
            merged += emb * w
            
        return merged
