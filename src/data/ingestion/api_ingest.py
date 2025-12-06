"""
API Ingestion Module for KALDRA v3.3.

Handles ingestion of data from API sources (JSON).
"""
from typing import Dict, Any, Optional
from ..normalizer.structured_normalizer import StructuredNormalizer
from src.unification.states.unified_state import InputContext, InputMetadata

class APIIngest:
    """
    Ingests data from API sources.
    """
    
    def __init__(self):
        self.normalizer = StructuredNormalizer()
        
    def ingest(self, data: Dict[str, Any], source: str = "api", stream_id: Optional[str] = None) -> InputContext:
        """
        Ingest JSON data and return an InputContext.
        """
        normalized_data = self.normalizer.normalize_json(data)
        
        # Create a text representation for the 'text' field (required by InputContext)
        # In a real app, this might be a summary or a specific field extraction
        text_repr = str(normalized_data)
        
        metadata = InputMetadata(
            source=source,
            stream_id=stream_id,
            content_type="json",
            timestamp=None # Could extract from data if available
        )
        
        return InputContext(
            text=text_repr,
            metadata=metadata,
            structured=normalized_data
        )
