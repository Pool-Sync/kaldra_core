"""
Integration tests for signal persistence.

Tests that SignalAdapter correctly persists signals to repository.
"""
import pytest
from typing import Any, Dict, List
from src.unification.adapters.signal_adapter import SignalAdapter
from src.unification.states.unified_state import (
    UnifiedContext,
    GlobalContext,
    InputContext,
    ArchetypeContext,
    MetaContext
)


class FakeSignalRepository:
    """Fake repository for testing without database."""
    
    def __init__(self) -> None:
        self.created: List[Dict[str, Any]] = []
        self.should_fail = False
    
    def create_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate signal creation."""
        if self.should_fail:
            return {"error": 500, "message": "Simulated failure"}
        
        self.created.append(data)
        return data


class TestSignalPersistence:
    """Test suite for signal persistence."""
    
    def test_signal_adapter_persists_signal(self):
        """Test that adapter persists signal to repository."""
        repo = FakeSignalRepository()
        adapter = SignalAdapter(signal_repository=repo, enable_persistence=True)
        
        # Create minimal context
        context = UnifiedContext(
            global_ctx=GlobalContext(
                version="3.5",
                request_id="test-123",
                mode="full"
            ),
            input_ctx=InputContext(
                text="Test signal for persistence",
                bias_score=0.5
            ),
            meta_ctx=MetaContext()
        )
        
        # Process signal
        signal = adapter.to_signal(context)
        
        # Verify signal was persisted
        assert len(repo.created) == 1
        persisted = repo.created[0]
        
        assert "id" in persisted
        assert persisted["domain"] == "alpha"
        assert "Test signal" in persisted["title"]
        assert persisted["summary"] == context.input_ctx.text
        assert "created_at" in persisted
        assert "raw_payload" in persisted
    
    def test_signal_adapter_handles_persistence_failure(self):
        """Test that persistence failures don't break pipeline."""
        repo = FakeSignalRepository()
        repo.should_fail = True
        
        adapter = SignalAdapter(signal_repository=repo, enable_persistence=True)
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="Test", bias_score=0.5)
        )
        
        # Should not raise exception
        signal = adapter.to_signal(context)
        
        # Signal should still be generated
        assert signal is not None
        assert "version" in signal
    
    def test_signal_adapter_with_persistence_disabled(self):
        """Test adapter with persistence disabled."""
        repo = FakeSignalRepository()
        adapter = SignalAdapter(signal_repository=repo, enable_persistence=False)
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="Test", bias_score=0.5)
        )
        
        signal = adapter.to_signal(context)
        
        # No signals should be persisted
        assert len(repo.created) == 0
        
        # Signal should still be generated
        assert signal is not None
    
    def test_signal_payload_includes_all_fields(self):
        """Test that signal payload includes all expected fields."""
        repo = FakeSignalRepository()
        adapter = SignalAdapter(signal_repository=repo, enable_persistence=True)
        
        context = UnifiedContext(
            global_ctx=GlobalContext(),
            input_ctx=InputContext(text="Complete test signal", bias_score=0.7)
        )
        
        signal = adapter.to_signal(context)
        
        assert len(repo.created) == 1
        payload = repo.created[0]
        
        # Check required fields
        required_fields = ["id", "domain", "title", "raw_payload", "created_at"]
        for field in required_fields:
            assert field in payload, f"Missing field: {field}"
        
        # Check optional fields exist (may be None)
        optional_fields = [
            "delta144_state", "dominant_archetype", "dominant_polarity",
            "tw_regime", "journey_stage", "importance", "confidence"
        ]
        for field in optional_fields:
            assert field in payload, f"Missing optional field: {field}"
