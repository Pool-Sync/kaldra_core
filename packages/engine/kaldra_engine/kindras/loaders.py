"""
Loaders for Kindra 3x48 vectors and mappings.
"""
import json
import os
from typing import Dict, Any, List

# Base path for schema files
SCHEMA_BASE_PATH = os.path.join(os.getcwd(), "schema", "kindras")

def _get_vector_file_path(layer: int) -> str:
    """Get path for vector definition file."""
    filenames = {
        1: "kindra_vectors_layer1_cultural_macro_48.json",
        2: "kindra_vectors_layer2_semiotic_media_48.json",
        3: "kindra_vectors_layer3_structural_systemic_48.json"
    }
    return os.path.join(SCHEMA_BASE_PATH, filenames[layer])

def _get_map_file_path(layer: int) -> str:
    """Get path for mapping file."""
    filenames = {
        1: "kindra_layer1_to_delta144_map.json",
        2: "kindra_layer2_to_delta144_map.json",
        3: "kindra_layer3_to_delta144_map.json"
    }
    return os.path.join(SCHEMA_BASE_PATH, filenames[layer])

def load_layer_vectors(layer: int) -> Dict[str, Dict[str, Any]]:
    """
    Load vector definitions for a specific layer.
    
    Returns:
        Dict mapping vector_id -> vector_definition_dict
    """
    path = _get_vector_file_path(layer)
    if not os.path.exists(path):
        # Fallback for testing or if file missing
        print(f"Warning: Vector file not found at {path}")
        return {}
        
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Convert list to dict keyed by id
    return {item['id']: item for item in data}

def load_layer_mapping(layer: int) -> Dict[str, Any]:
    """
    Load Kindra->Delta144 mapping for a specific layer.
    
    Returns:
        Dict mapping vector_id -> mapping_info
    """
    path = _get_map_file_path(layer)
    if not os.path.exists(path):
        print(f"Warning: Map file not found at {path}")
        return {}
        
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Convert list to dict keyed by kindra_vector_id if it's a list
    # The map file format might be a list of objects or a dict.
    # Based on previous context, it's likely a list of objects like:
    # [{"kindra_vector_id": "...", "delta144_targets": [...]}, ...]
    
    if isinstance(data, list):
        mapping = {}
        for item in data:
            # Handle different possible key names based on schema evolution
            key = item.get('kindra_vector_id') or item.get('id')
            if key:
                mapping[key] = item
        return mapping
    
    return data
