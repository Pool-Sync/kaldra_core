"""
Tests for Story Events API endpoints.
"""
import uuid
from fastapi.testclient import TestClient
from kaldra_api.main import app


client = TestClient(app)


def test_list_events_by_signal_returns_200():
    """Test listing events by signal ID returns 200."""
    # Use a fake signal ID - endpoint should return empty list, not error
    fake_signal_id = str(uuid.uuid4())
    response = client.get(f"/story-events/by-signal/{fake_signal_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_list_all_events_returns_200():
    """Test listing all events returns 200."""
    response = client.get("/story-events?limit=10")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_list_events_with_stream_filter():
    """Test filtering events by stream ID."""
    response = client.get("/story-events?stream_id=test-stream&limit=5")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_list_events_respects_limit():
    """Test that limit parameter is respected."""
    response = client.get("/story-events?limit=1")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    # Should have at most 1 event
    assert len(data) <= 1
