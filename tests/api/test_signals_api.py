"""
Tests for Signals API endpoints.
"""
import uuid
from fastapi.testclient import TestClient
from kaldra_api.main import app


client = TestClient(app)


def test_list_signals_returns_200():
    """Test that listing signals returns 200."""
    response = client.get("/signals?limit=5")
    assert response.status_code == 200
    
    # Response should be a list
    data = response.json()
    assert isinstance(data, list)


def test_list_signals_with_domain_filter():
    """Test filtering signals by domain."""
    response = client.get("/signals?domain=alpha&limit=10")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_get_signal_not_found():
    """Test getting a non-existent signal returns 404."""
    fake_id = str(uuid.uuid4())
    response = client.get(f"/signals/{fake_id}")
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_health_supabase():
    """Test Supabase health check endpoint."""
    response = client.get("/health/supabase")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    # Status can be "ok" or "error" depending on connection
