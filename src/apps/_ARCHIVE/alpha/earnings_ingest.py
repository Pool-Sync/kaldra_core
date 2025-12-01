"""Ingestion utilities for KALDRA-Alpha earnings data."""

from dataclasses import dataclass
from typing import Optional

# Import Data Lab ingestion modules
try:
    from kaldra_data.ingestion.pdf_ingest import load_pdf
except ImportError:
    load_pdf = None

try:
    from kaldra_data.ingestion.html_ingest import load_html
except ImportError:
    load_html = None

try:
    from kaldra_data.ingestion.text_ingest import load_text
except ImportError:
    load_text = None


@dataclass
class EarningsSource:
    """Defines a source for earnings call data."""
    source_type: str  # "pdf" | "html" | "text"
    path_or_url: str
    ticker: Optional[str] = None
    quarter: Optional[str] = None  # "Q1 2025" etc.


def load_earnings_text(source: EarningsSource) -> str:
    """
    Load raw earnings call text from the given source.
    Uses KALDRA Data Lab ingestion modules.
    """
    if source.source_type == "pdf":
        if load_pdf is None:
            raise RuntimeError("PDF ingestion module not available.")
        return load_pdf(source.path_or_url)
    
    elif source.source_type == "html":
        if load_html is None:
            raise RuntimeError("HTML ingestion module not available.")
        return load_html(source.path_or_url)
    
    elif source.source_type == "text":
        if load_text is None:
            raise RuntimeError("Text ingestion module not available.")
        return load_text(source.path_or_url)
    
    else:
        raise ValueError(f"Unsupported source type: {source.source_type}")


def normalize_earnings_text(raw: str) -> str:
    """
    Simple cleaning/normalization step for earnings drafts:
    - strip()
    - collapse whitespace
    - replace multiple newlines with single space
    """
    if not raw:
        return ""
        
    # Replace multiple newlines/tabs with space
    cleaned = " ".join(raw.split())
    return cleaned.strip()
