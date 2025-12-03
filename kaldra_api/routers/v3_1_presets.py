"""
Presets API endpoints for v3.1.
"""

from fastapi import APIRouter, HTTPException
from ..schemas.v3_1_responses import PresetsResponse

# Import from Exoskeleton layer
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from src.unification.exoskeleton import PresetManager

router = APIRouter()


@router.get("/presets", response_model=PresetsResponse)
def list_presets():
    """
    List all available analysis presets.
    
    Returns all preset configurations including:
    - Description
    - Execution mode
    - Emphasis areas
    - Thresholds
    - Output format
    """
    try:
        manager = PresetManager()
        presets_dict = manager.list_presets()
        
        # Convert PresetConfig objects to dicts
        presets_response = {}
        for name, preset in presets_dict.items():
            presets_response[name] = {
                "name": preset.name,
                "description": preset.description,
                "mode": preset.mode,
                "emphasis": preset.emphasis,
                "thresholds": preset.thresholds,
                "output_format": preset.output_format,
                "metadata": preset.metadata
            }
        
        return {"presets": presets_response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load presets: {str(e)}")
