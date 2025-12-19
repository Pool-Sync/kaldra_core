"""
Analyze API endpoint for v3.1 with preset and profile support.
"""

from fastapi import APIRouter, HTTPException
from ..schemas.v3_1_schemas import AnalyzeV31Request
from ..schemas.v3_1_responses import AnalyzeV31Response
import logging

# Import from Exoskeleton and Unification layers
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from src.unification.exoskeleton import PresetRouter
from src.unification.adapters.unified_api import UnifiedKaldra

logger = logging.getLogger(__name__)

router = APIRouter()
preset_router = PresetRouter()


@router.post("/analyze", response_model=AnalyzeV31Response)
def analyze_v31(request: AnalyzeV31Request):
    """
    Execute KALDRA analysis with preset and profile support.
    
    This endpoint integrates the Exoskeleton Layer (presets + profiles)
    with the core KALDRA analysis pipeline.
    
    Flow:
    1. Load preset (if provided)
    2. Load profile (if provided)
    3. Merge via PresetRouter
    4. Execute analysis with resolved config
    5. Return enhanced v3.1 signal
    
    Args:
        request: AnalyzeV31Request with text, preset, and profile_id
        
    Returns:
        AnalyzeV31Response with enhanced signal format
    """
    try:
        # Determine preset to use
        preset_name = request.preset
        profile_id = request.profile_id
        
        # If no preset provided but profile exists, use profile's preferred preset
        if not preset_name and profile_id:
            try:
                profile = preset_router.profile_manager.get_profile(profile_id)
                if profile and profile.preferred_preset:
                    preset_name = profile.preferred_preset
                    logger.info(f"Using profile's preferred preset: {preset_name}")
            except Exception as e:
                logger.warning(f"Failed to load profile {profile_id}: {e}")
        
        # Default to alpha if no preset specified
        if not preset_name:
            preset_name = "alpha"
            logger.info("No preset specified, defaulting to 'alpha'")
        
        # Resolve preset + profile
        try:
            resolved_config = preset_router.resolve_preset(
                preset_name=preset_name,
                user_id=profile_id
            )
            logger.info(f"Resolved config: preset={resolved_config.name}, mode={resolved_config.mode}")
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Invalid preset: {preset_name}")
        except Exception as e:
            logger.error(f"Failed to resolve preset config: {e}")
            raise HTTPException(status_code=500, detail="Failed to resolve configuration")
        
        # Execute analysis
        try:
            kaldra = UnifiedKaldra()
            result = kaldra.analyze(
                text=request.text,
                mode=resolved_config.mode
            )
            
            # Enhance result with preset information
            if isinstance(result, dict):
                result["preset_used"] = resolved_config.name
                result["preset_config"] = {
                    "mode": resolved_config.mode,
                    "emphasis": resolved_config.emphasis,
                    "thresholds": resolved_config.thresholds,
                    "output_format": resolved_config.output_format
                }
                
                # Ensure version is set to 3.1
                result["version"] = "3.1"
            
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
