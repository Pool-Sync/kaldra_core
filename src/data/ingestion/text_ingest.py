"""
Text Ingestion Module for KALDRA v3.3.

Handles ingestion of raw text, potentially detecting structured patterns.
"""
from typing import Optional
import json
from ..normalizer.structured_normalizer import StructuredNormalizer
from src.unification.states.unified_state import InputContext, InputMetadata

class TextIngest:
    """
    Ingests raw text.
    """
    
    def __init__(self):
        self.normalizer = StructuredNormalizer()
        
    def ingest(self, text: str, source: str = "text_input", stream_id: Optional[str] = None) -> InputContext:
        """
        Ingest text and return an InputContext.
        
        Attempts to detect if text is actually JSON.
        """
        structured_data = None
        content_type = "text"
        
        # Simple heuristic to detect JSON
        text_stripped = text.strip()
        if (text_stripped.startswith("{") and text_stripped.endswith("}")) or \
           (text_stripped.startswith("[") and text_stripped.endswith("]")):
            try:
                data = json.loads(text)
                structured_data = self.normalizer.normalize_generic(data)
                content_type = "json" if isinstance(data, dict) else "list"
            except json.JSONDecodeError:
                pass
                
        metadata = InputMetadata(
            source=source,
            stream_id=stream_id,
            content_type=content_type
        )
        
        return InputContext(
            text=text,
            metadata=metadata,
            structured=structured_data
        )
