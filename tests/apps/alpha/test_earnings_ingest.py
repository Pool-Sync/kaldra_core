"""Tests for KALDRA-Alpha earnings ingestion."""

import pytest
from unittest.mock import patch, MagicMock
from src.apps.alpha.earnings_ingest import (
    EarningsSource, 
    load_earnings_text, 
    normalize_earnings_text
)

def test_normalize_earnings_text_basic():
    raw = " META Q1 2025 \n\n Revenue up 15% \n"
    out = normalize_earnings_text(raw)
    assert "META Q1 2025" in out
    assert "Revenue up 15%" in out
    assert "\n" not in out
    assert "  " not in out  # No double spaces

def test_normalize_earnings_text_empty():
    assert normalize_earnings_text("") == ""
    assert normalize_earnings_text(None) == ""

def test_load_earnings_text_unsupported_type():
    source = EarningsSource(source_type="hologram", path_or_url="void")
    with pytest.raises(ValueError, match="Unsupported source type"):
        load_earnings_text(source)

@patch("src.apps.alpha.earnings_ingest.load_text")
def test_load_earnings_text_dispatch(mock_load_text):
    mock_load_text.return_value = "Mock Content"
    source = EarningsSource(source_type="text", path_or_url="dummy.txt")
    
    content = load_earnings_text(source)
    
    assert content == "Mock Content"
    mock_load_text.assert_called_once_with("dummy.txt")
