"""
KALDRA API Tests — Narrative Risk Calculation
Tests narrative_risk calculation based on TW, bias, and confidence
"""
import pytest
from fastapi.testclient import TestClient
from kaldra_api.main import app

client = TestClient(app)


def test_narrative_risk_range():
    """Test that narrative_risk is in valid range [0, 1]"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Technology evolves rapidly"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Must have narrative_risk field
    assert "narrative_risk" in data
    
    # Must be a number
    assert isinstance(data["narrative_risk"], (int, float))
    
    # Must be in [0, 1] range
    assert 0.0 <= data["narrative_risk"] <= 1.0


def test_narrative_risk_high_bias():
    """Test that high bias increases narrative_risk"""
    # Low bias text
    response_low = client.post(
        "/engine/kaldra/signal",
        json={"text": "A simple observation about nature."}
    )
    
    # High bias text
    response_high = client.post(
        "/engine/kaldra/signal",
        json={"text": "THIS IS ABSOLUTELY THE WORST CATASTROPHE EVER!!!"}
    )
    
    data_low = response_low.json()
    data_high = response_high.json()
    
    # High bias should generally lead to higher narrative risk
    # (though other factors like confidence also play a role)
    assert data_high["bias_score"] > data_low["bias_score"]
    
    # narrative_risk should reflect this
    # Note: This is a heuristic test, may need adjustment
    if data_high["bias_score"] > 0.7:
        assert data_high["narrative_risk"] > 0.3


def test_narrative_risk_formula():
    """Test narrative_risk calculation formula (heuristic v0.1)"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Change brings uncertainty"}
    )
    
    data = response.json()
    
    # Extract components
    bias_score = data["bias_score"]
    confidence = data["confidence"]
    tw_regime = data["tw_regime"]
    narrative_risk = data["narrative_risk"]
    
    # Calculate expected risk using formula:
    # 40% bias + 30% TW + 30% (1 - confidence)
    tw_factor = 1.0 if tw_regime == "ANOMALY" else 0.0
    expected_risk = (
        0.4 * bias_score +
        0.3 * tw_factor +
        0.3 * (1.0 - confidence)
    )
    expected_risk = max(0.0, min(1.0, expected_risk))
    
    # Should match (with small floating point tolerance)
    assert abs(narrative_risk - expected_risk) < 0.01


def test_narrative_risk_tw_trigger():
    """Test that TW trigger affects narrative_risk"""
    # Note: TW trigger is hard to force in tests, so we just verify
    # that when it happens, it increases risk
    
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Volatility and instability"}
    )
    
    data = response.json()
    
    if data["tw_regime"] == "ANOMALY":
        # If TW triggered, narrative_risk should be elevated
        # (at least 30% contribution from TW factor)
        assert data["narrative_risk"] >= 0.3


def test_narrative_risk_confidence_impact():
    """Test that low confidence increases narrative_risk"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Ambiguous and uncertain situation"}
    )
    
    data = response.json()
    
    # Low confidence should contribute to higher risk
    if data["confidence"] < 0.3:
        # Low confidence contributes ~21% to risk (30% * 0.7)
        assert data["narrative_risk"] > 0.2


def test_narrative_risk_consistency():
    """Test that narrative_risk is consistent across multiple calls"""
    text = "Consistent test input"
    
    risks = []
    for _ in range(3):
        response = client.post(
            "/engine/kaldra/signal",
            json={"text": text}
        )
        data = response.json()
        risks.append(data["narrative_risk"])
    
    # All risks should be identical (deterministic)
    assert len(set(risks)) == 1
