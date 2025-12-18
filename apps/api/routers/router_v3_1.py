"""
Main router for API v3.1 endpoints.

Aggregates all v3.1 sub-routers:
- Analyze (preset + profile aware)
- Presets management
- Profile management
"""

from fastapi import APIRouter
from . import v3_1_analyze, v3_1_presets, v3_1_profile

# Create main v3.1 router
router = APIRouter(
    prefix="/v3.1",
    tags=["v3.1"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)

# Include sub-routers
router.include_router(v3_1_analyze.router, tags=["analyze"])
router.include_router(v3_1_presets.router, tags=["presets"])
router.include_router(v3_1_profile.router, tags=["profiles"])
