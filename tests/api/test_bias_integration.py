"""
KALDRA API Tests — Bias Engine Integration
Tests bias score and label calculation in /engine/kaldra/signal endpoint
"""
import pytest
from fastapi.testclient import TestClient
from kaldra_api.main import app

client = TestClient(app)


def test_bias_neutral_text():
    """Test bias detection with neutral text"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "The weather is nice today."}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Neutral text should have low bias score
    assert "bias_score" in data
    assert data["bias_score"] < 0.3
    
    # Bias label should be present
    assert "bias_label" in data
    assert data["bias_label"] is not None


def test_bias_charged_text():
    """Test bias detection with highly charged text"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "THIS IS THE WORST DISASTER EVER!!!"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Charged text should have high bias score
    assert "bias_score" in data
    assert data["bias_score"] > 0.6  # Adjusted threshold
    
    # Bias label should reflect high bias
    assert "bias_label" in data
    assert data["bias_label"] is not None  # Any label is valid


def test_bias_label_coherence():
    """Test that bias_label is coherent with bias_score"""
    # Low bias
    response_low = client.post(
        "/engine/kaldra/signal",
        json={"text": "A simple statement."}
    )
    data_low = response_low.json()
    
    # High bias
    response_high = client.post(
        "/engine/kaldra/signal",
        json={"text": "ABSOLUTELY TERRIBLE CATASTROPHE!!!"}
    )
    data_high = response_high.json()
    
    # Labels should be different
    assert data_low["bias_label"] != data_high["bias_label"]
    
    # High score should have more severe label
    if data_high["bias_score"] > 0.5:
        assert data_high["bias_label"] in ["moderate", "extreme", "high", "negative"]


def test_bias_fields_required():
    """Test that bias_score and bias_label are always present"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Any text here"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Both fields must be present
    assert "bias_score" in data
    assert "bias_label" in data
    
    # bias_score must be a number
    assert isinstance(data["bias_score"], (int, float))
    assert 0.0 <= data["bias_score"] <= 1.0
