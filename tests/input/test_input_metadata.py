"""
Tests for InputMetadata and InputContext backward compatibility.
"""
import pytest
from src.unification.states.unified_state import InputContext, InputMetadata

class TestInputMetadata:
    
    def test_metadata_defaults(self):
        """Test that InputMetadata initializes with correct defaults."""
        meta = InputMetadata()
        assert meta.source is None
        assert meta.stream_id is None
        assert meta.content_type == "text"
        assert meta.language == "en"
        assert meta.timestamp is None
        assert meta.extra == {}
        
    def test_metadata_custom_values(self):
        """Test initialization with custom values."""
        meta = InputMetadata(
            source="twitter",
            stream_id="stream-123",
            content_type="json",
            language="fr",
            timestamp=123456789.0,
            extra={"foo": "bar"}
        )
        assert meta.source == "twitter"
        assert meta.stream_id == "stream-123"
        assert meta.content_type == "json"
        assert meta.language == "fr"
        assert meta.timestamp == 123456789.0
        assert meta.extra == {"foo": "bar"}
        
    def test_to_dict(self):
        """Test serialization."""
        meta = InputMetadata(source="web")
        data = meta.to_dict()
        assert data["source"] == "web"
        assert data["content_type"] == "text"


class TestInputContextBackwardCompatibility:
    
    def test_init_with_metadata_dict(self):
        """Test initializing InputContext with a dict for metadata (v3.2 style)."""
        # Old style: metadata was a dict
        old_metadata = {
            "source": "legacy_api",
            "custom_field": "custom_value",
            "timestamp": 1000.0
        }
        
        ctx = InputContext(text="Legacy input", metadata=old_metadata)
        
        # Should be converted to InputMetadata
        assert isinstance(ctx.metadata, InputMetadata)
        assert ctx.metadata.source == "legacy_api"
        assert ctx.metadata.timestamp == 1000.0
        # Unknown fields go into 'extra'
        assert ctx.metadata.extra["custom_field"] == "custom_value"
        
    def test_init_with_input_metadata(self):
        """Test initializing InputContext with InputMetadata object (v3.3 style)."""
        meta = InputMetadata(source="new_api")
        ctx = InputContext(text="New input", metadata=meta)
        
        assert isinstance(ctx.metadata, InputMetadata)
        assert ctx.metadata.source == "new_api"
        
    def test_to_dict_serialization(self):
        """Test that to_dict produces expected structure."""
        meta = InputMetadata(source="test")
        ctx = InputContext(text="Test", metadata=meta)
        
        data = ctx.to_dict()
        assert data["text"] == "Test"
        assert data["metadata"]["source"] == "test"
        assert "structured" in data
