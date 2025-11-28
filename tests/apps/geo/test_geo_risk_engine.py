"""Tests for KALDRA-GEO risk engine."""

import pytest
from unittest.mock import MagicMock, patch

from src.apps.geo.geo_risk_engine import GeoRiskEngine, GeoRiskEngineConfig
from src.apps.geo.geo_signals import GeoSignal


def test_geo_risk_engine_analyze_text_returns_geo_signal():
    """Test that analyze_text returns a valid GeoSignal."""
    engine = GeoRiskEngine(config=GeoRiskEngineConfig(d_ctx=16))
    
    result = engine.analyze_text(
        text="Geopolitical tensions rising in the region",
        region="APAC",
        source="news"
    )
    
    assert isinstance(result, GeoSignal)
    assert result.domain == "GEO"
    assert result.extras["region"] == "APAC"
    assert result.extras["source"] == "news"
    assert result.risk_level in ["low", "medium", "high", "critical"]


def test_geo_risk_engine_handles_empty_text():
    """Test that empty text raises ValueError."""
    engine = GeoRiskEngine()
    
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        engine.analyze_text("")
    
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        engine.analyze_text("   ")


def test_geo_risk_engine_uses_fallback_embeddings():
    """Test that engine uses fallback embeddings by default."""
    engine = GeoRiskEngine(config=GeoRiskEngineConfig(d_ctx=16))
    
    # This should work without SentenceTransformers installed
    result = engine.analyze_text("Test geopolitical text")
    
    assert isinstance(result, GeoSignal)
    assert len(result.top_archetypes) > 0
