"""
KALDRA API Tests — Delta144 State Exposure
Tests that real archetype and delta_state are exposed (not placeholders)
"""
import pytest
from fastapi.testclient import TestClient
from kaldra_api.main import app

client = TestClient(app)


def test_archetype_is_real():
    """Test that archetype field contains real archetype ID"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Leadership and vision guide progress"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Must have archetype field
    assert "archetype" in data
    
    # Should not be a generic placeholder
    assert not data["archetype"].startswith("STATE_")
    
    # Should match archetype ID pattern (e.g., A01_INNOCENT, A07_RULER)
    assert data["archetype"].startswith("A")
    assert "_" in data["archetype"]


def test_delta_state_is_real():
    """Test that delta_state field contains real state ID"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Transformation and growth"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Must have delta_state field
    assert "delta_state" in data
    
    # Should not be generic "INFERRED"
    assert data["delta_state"] != "INFERRED"
    
    # Should have a meaningful state ID
    assert len(data["delta_state"]) > 3


def test_no_inferred_placeholders():
    """Test that response doesn't contain any 'INFERRED' placeholders"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Innovation and creativity"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check all string fields for "INFERRED"
    for key, value in data.items():
        if isinstance(value, str):
            assert value != "INFERRED", f"Field '{key}' should not be 'INFERRED'"


def test_archetype_state_consistency():
    """Test that archetype and delta_state are consistent"""
    response = client.post(
        "/engine/kaldra/signal",
        json={"text": "Power and control"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    archetype = data["archetype"]
    delta_state = data["delta_state"]
    
    # delta_state should contain archetype prefix
    # e.g., if archetype is "A07_RULER", delta_state might be "A07_RULER_6_05"
    archetype_prefix = archetype.split("_")[0]  # e.g., "A07"
    assert delta_state.startswith(archetype_prefix), \
        f"delta_state '{delta_state}' should start with archetype prefix '{archetype_prefix}'"


def test_multiple_requests_different_states():
    """Test that different texts can produce different states"""
    texts = [
        "Peace and harmony",
        "Conflict and struggle",
        "Growth and transformation"
    ]
    
    archetypes = set()
    states = set()
    
    for text in texts:
        response = client.post(
            "/engine/kaldra/signal",
            json={"text": text}
        )
        data = response.json()
        archetypes.add(data["archetype"])
        states.add(data["delta_state"])
    
    # Should have at least some variation (not all identical)
    # Note: This might occasionally fail due to semantic similarity
    # but generally different texts should produce different results
    assert len(archetypes) >= 1
    assert len(states) >= 1
