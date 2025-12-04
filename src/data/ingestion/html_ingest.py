"""
HTML Ingestion Module for KALDRA v3.3.

Handles ingestion of data from HTML sources, specifically tables.
"""
from typing import Dict, Any, List, Optional
from ..normalizer.structured_normalizer import StructuredNormalizer
from src.unification.states.unified_state import InputContext, InputMetadata

class HTMLIngest:
    """
    Ingests data from HTML sources.
    """
    
    def __init__(self):
        self.normalizer = StructuredNormalizer()
        
    def ingest_table(self, rows: List[Dict[str, Any]], source: str = "html_table", stream_id: Optional[str] = None) -> InputContext:
        """
        Ingest a parsed HTML table (list of dicts) and return an InputContext.
        """
        normalized_data = self.normalizer.normalize_table(rows)
        
        # Create text representation
        text_repr = f"Table with {len(rows)} rows."
        
        metadata = InputMetadata(
            source=source,
            stream_id=stream_id,
            content_type="table"
        )
        
        return InputContext(
            text=text_repr,
            metadata=metadata,
            structured=normalized_data
        )
