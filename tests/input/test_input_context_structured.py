"""
Tests for Structured Data Ingestion and Normalization.
"""
import pytest
from src.data.normalizer.structured_normalizer import StructuredNormalizer
from src.data.ingestion.api_ingest import APIIngest
from src.data.ingestion.html_ingest import HTMLIngest
from src.data.ingestion.text_ingest import TextIngest
from src.unification.states.unified_state import InputContext

class TestStructuredNormalizer:
    
    def test_normalize_json(self):
        norm = StructuredNormalizer()
        data = {"key": "value", "nested": {"a": 1}}
        result = norm.normalize_json(data)
        assert result == data
        
    def test_normalize_table(self):
        norm = StructuredNormalizer()
        rows = [{"col1": "val1", "col2": 1}, {"col1": "val2", "col2": 2}]
        result = norm.normalize_table(rows)
        assert result["type"] == "table"
        assert result["count"] == 2
        assert result["rows"] == rows
        
    def test_normalize_generic(self):
        norm = StructuredNormalizer()
        assert norm.normalize_generic({"a": 1}) == {"a": 1}
        assert norm.normalize_generic([{"a": 1}])["type"] == "table"
        assert norm.normalize_generic([1, 2])["type"] == "list"
        assert norm.normalize_generic("string")["type"] == "value"


class TestIngestionModules:
    
    def test_api_ingest(self):
        ingestor = APIIngest()
        data = {"user": "test", "id": 123}
        ctx = ingestor.ingest(data, source="test_api")
        
        assert isinstance(ctx, InputContext)
        assert ctx.metadata.source == "test_api"
        assert ctx.metadata.content_type == "json"
        assert ctx.structured == data
        assert "user" in ctx.text or "test" in ctx.text
        
    def test_html_ingest(self):
        ingestor = HTMLIngest()
        rows = [{"header": "val"}]
        ctx = ingestor.ingest_table(rows, source="web_scrape")
        
        assert ctx.metadata.source == "web_scrape"
        assert ctx.metadata.content_type == "table"
        assert ctx.structured["type"] == "table"
        
    def test_text_ingest_json_detection(self):
        ingestor = TextIngest()
        json_text = '{"key": "value"}'
        ctx = ingestor.ingest(json_text)
        
        assert ctx.metadata.content_type == "json"
        assert ctx.structured == {"key": "value"}
        
    def test_text_ingest_plain_text(self):
        ingestor = TextIngest()
        plain_text = "Just some text"
        ctx = ingestor.ingest(plain_text)
        
        assert ctx.metadata.content_type == "text"
        assert ctx.structured is None
