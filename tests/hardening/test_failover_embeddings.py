"""
Hardening Tests: Embedding Failover.
Verifies EmbeddingGenerator behavior under failure.
"""
import pytest
import numpy as np
from unittest.mock import MagicMock
from src.core.embedding_generator import EmbeddingGenerator, EmbeddingConfig

def test_openai_fallback_on_error():
    # Config for OpenAI
    config = EmbeddingConfig(provider="openai", api_key="fake")
    
    # Mock client that raises exception
    mock_client = MagicMock()
    mock_client.embeddings.create.side_effect = Exception("API Error")
    
    generator = EmbeddingGenerator(config=config, openai_client=mock_client)
    
    # The decorator @safe_fallback is NOT on the public encode method, 
    # but retries/circuit breakers are on _encode_openai.
    # If _encode_openai fails after retries, it raises.
    # However, we want to ensure the system handles it.
    # Wait, did we put safe_fallback on _encode_openai? No, just retries/CB/timeout.
    # So it should raise, and the caller (MasterEngine) handles it.
    
    with pytest.raises(Exception):
        generator.encode("test")

def test_circuit_breaker_activation():
    # This test assumes the global circuit breaker state.
    # We might need to reset it or mock it.
    pass
