"""
KALDRA API Tests — Kindra Distribution
Tests that kindra_distribution returns top-5 states correctly
"""
import pytest
from fastapi.testclient import TestClient
from kaldra_api.main import app

client = TestClient(app)


def test_kindra_distribution_structure():
    """Test that kindra_distribution has correct structure"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Artificial intelligence is transforming society"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Must contain kindra_distribution
    assert "kindra_distribution" in data
    
    # Must be a list
    assert isinstance(data["kindra_distribution"], list)
    
    # Must have exactly 5 items (top-5)
    assert len(data["kindra_distribution"]) == 5


def test_kindra_distribution_item_format():
    """Test that each item has correct format"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Technology advances rapidly"}
    )
    
    data = response.json()
    distribution = data["kindra_distribution"]
    
    for item in distribution:
        # Each item must be a dict
        assert isinstance(item, dict)
        
        # Must have state_index and prob
        assert "state_index" in item
        assert "prob" in item
        
        # state_index must be int
        assert isinstance(item["state_index"], int)
        assert 0 <= item["state_index"] < 144
        
        # prob must be float > 0
        assert isinstance(item["prob"], (int, float))
        assert item["prob"] > 0


def test_kindra_distribution_sorted():
    """Test that distribution is sorted by probability (descending)"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Innovation drives progress"}
    )
    
    data = response.json()
    distribution = data["kindra_distribution"]
    
    # Extract probabilities
    probs = [item["prob"] for item in distribution]
    
    # Should be sorted in descending order
    assert probs == sorted(probs, reverse=True)


def test_kindra_distribution_probabilities_valid():
    """Test that all probabilities are valid"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Change is constant"}
    )
    
    data = response.json()
    distribution = data["kindra_distribution"]
    
    for item in distribution:
        prob = item["prob"]
        
        # Probability must be in [0, 1]
        assert 0.0 <= prob <= 1.0
        
        # Probability must be positive (top-5 should never be 0)
        assert prob > 0


def test_kindra_distribution_unique_states():
    """Test that state_index values are unique"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Evolution of ideas"}
    )
    
    data = response.json()
    distribution = data["kindra_distribution"]
    
    # Extract state indices
    indices = [item["state_index"] for item in distribution]
    
    # All indices should be unique
    assert len(indices) == len(set(indices))
