"""
Profile API endpoints for v3.1.
"""

from fastapi import APIRouter, HTTPException, Path
from ..schemas.v3_1_schemas import ProfileUpdateRequest
from ..schemas.v3_1_responses import ProfileResponse

# Import from Exoskeleton layer
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from src.unification.exoskeleton import ProfileManager, UserProfile

router = APIRouter()
profile_manager = ProfileManager()


@router.get("/profile/{user_id}", response_model=ProfileResponse)
def get_profile(user_id: str = Path(..., description="User ID")):
    """
    Retrieve user profile by ID.
    
    Returns the user's analysis preferences including:
    - Preferred preset
    - Risk tolerance
    - Output format preferences
    - Analysis depth setting
    """
    profile = profile_manager.get_profile(user_id)
    
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile not found for user: {user_id}")
    
    return ProfileResponse(
        user_id=profile.user_id,
        preferred_preset=profile.preferred_preset,
        risk_tolerance=profile.risk_tolerance,
        output_format=profile.output_format,
        depth=profile.depth,
        preferences=profile.preferences
    )


@router.put("/profile/{user_id}", response_model=ProfileResponse)
def update_profile(
    user_id: str = Path(..., description="User ID"),
    update: ProfileUpdateRequest = None
):
    """
    Create or update user profile.
    
    Supports partial updates - only provided fields will be updated.
    If profile doesn't exist, it will be created with provided values.
    """
    try:
        # Build update dict from request
        update_dict = {}
        if update.preferred_preset is not None:
            update_dict["preferred_preset"] = update.preferred_preset
        if update.risk_tolerance is not None:
            update_dict["risk_tolerance"] = update.risk_tolerance
        if update.output_format is not None:
            update_dict["output_format"] = update.output_format
        if update.depth is not None:
            update_dict["depth"] = update.depth
        
        # Update or create profile
        updated_profile = profile_manager.update_profile(user_id, update_dict)
        
        return ProfileResponse(
            user_id=updated_profile.user_id,
            preferred_preset=updated_profile.preferred_preset,
            risk_tolerance=updated_profile.risk_tolerance,
            output_format=updated_profile.output_format,
            depth=updated_profile.depth,
            preferences=updated_profile.preferences
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update profile: {str(e)}")
