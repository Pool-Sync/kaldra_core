"""
Structured Data Normalizer for KALDRA v3.3.

Normalizes various structured data formats (JSON, tables, etc.) into a consistent dictionary format.
"""
from typing import Dict, Any, List, Union
import json

class StructuredNormalizer:
    """
    Normalizes structured data inputs.
    """
    
    def normalize_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize a JSON object.
        
        Currently a pass-through, but allows for future schema validation or transformation.
        """
        return data
        
    def normalize_table(self, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Normalize a list of rows (table) into a structured format.
        
        Returns:
            Dict with 'type': 'table', 'rows': rows, 'count': len(rows)
        """
        return {
            "type": "table",
            "rows": rows,
            "count": len(rows)
        }
        
    def normalize_generic(self, data: Any) -> Dict[str, Any]:
        """
        Normalize generic data.
        
        Attempts to detect type and normalize accordingly.
        """
        if isinstance(data, dict):
            return self.normalize_json(data)
        elif isinstance(data, list):
            # Check if it looks like a table (list of dicts)
            if data and isinstance(data[0], dict):
                return self.normalize_table(data)
            else:
                return {"type": "list", "items": data}
        else:
            return {"type": "value", "value": data}
