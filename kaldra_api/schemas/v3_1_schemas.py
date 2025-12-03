"""
Request schemas for API v3.1.
"""

from typing import Optional
from pydantic import BaseModel, Field


class AnalyzeV31Request(BaseModel):
    """Request schema for v3.1 analyze endpoint."""
    
    text: str = Field(
        ...,
        min_length=1,
        max_length=50000,
        description="Text to analyze"
    )
    preset: Optional[str] = Field(
        None,
        description="Preset name: alpha, geo, safeguard, or product"
    )
    profile_id: Optional[str] = Field(
        None,
        description="User profile ID for personalized analysis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "text": "Market volatility increased amid geopolitical tensions...",
                "preset": "alpha",
                "profile_id": "user_123"
            }
        }


class ProfileUpdateRequest(BaseModel):
    """Request schema for profile updates."""
    
    preferred_preset: Optional[str] = Field(
        None,
        description="Default preset: alpha, geo, safeguard, or product"
    )
    risk_tolerance: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Risk tolerance level [0.0, 1.0]"
    )
    output_format: Optional[str] = Field(
        None,
        description="Preferred output format"
    )
    depth: Optional[str] = Field(
        None,
        description="Analysis depth: fast, standard, deep, or exploratory"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "preferred_preset": "geo",
                "risk_tolerance": 0.7,
                "depth": "deep"
            }
        }
