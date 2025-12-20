"""
Response schemas for API v3.1.
"""

from typing import Any

from pydantic import BaseModel, Field


class AnalyzeV31Response(BaseModel):
    """Response schema for v3.1 analyze endpoint with enhanced signal format."""

    # Core metadata
    version: str = Field(default="3.1", description="API version")
    request_id: str = Field(..., description="Unique request identifier")
    timestamp: float = Field(..., description="Unix timestamp")
    mode: str = Field(..., description="Execution mode")
    degraded: bool = Field(default=False, description="Degraded mode flag")

    # Enhanced v3.1 fields
    preset_used: str | None = Field(None, description="Preset used for analysis")
    preset_config: dict[str, Any] | None = Field(None, description="Resolved preset configuration")

    # Signal outputs
    meta: dict[str, Any] | None = Field(None, description="Meta engines (Nietzsche, Aurelius, Campbell)")
    kindra: dict[str, Any] | None = Field(None, description="Kindra 3×48 vector analysis")
    archetypes: dict[str, Any] | None = Field(None, description="Archetypal analysis (Δ144)")
    drift: dict[str, Any] | None = Field(None, description="Drift and TW369 analysis")
    risk: dict[str, Any] | None = Field(None, description="Risk assessment")
    story: dict[str, Any] | None = Field(None, description="Story arc analysis")

    # Legacy compatibility
    input: dict[str, Any] | None = Field(None, description="Input context")
    summary: dict[str, Any] | None = Field(None, description="Analysis summary")

    class Config:
        schema_extra = {
            "example": {
                "version": "3.1",
                "request_id": "abc-123",
                "timestamp": 1701234567.89,
                "mode": "full",
                "degraded": False,
                "preset_used": "alpha",
                "preset_config": {
                    "mode": "full",
                    "emphasis": {"kindra.layer1": 1.0},
                    "thresholds": {"risk": 0.75},
                },
                "meta": {
                    "nietzsche": {"will_to_power": 0.75},
                    "aurelius": {"stoic_acceptance": 0.82},
                    "campbell": {"journey_stage": "ordeal"},
                },
                "kindra": {
                    "layer1": {"E01": 0.23, "E02": 0.45},
                    "tw_plane_distribution": {"3": 0.33, "6": 0.34, "9": 0.33},
                },
            }
        }


class ProfileResponse(BaseModel):
    """Response schema for profile endpoints."""

    user_id: str
    preferred_preset: str = "alpha"
    risk_tolerance: float = 0.5
    output_format: str = "json"
    depth: str = "standard"
    preferences: dict[str, Any] = {}


class PresetsResponse(BaseModel):
    """Response schema for presets listing."""

    presets: dict[str, dict[str, Any]] = Field(..., description="Available presets with configurations")

    class Config:
        schema_extra = {
            "example": {
                "presets": {
                    "alpha": {
                        "name": "alpha",
                        "description": "Financial analysis",
                        "mode": "full",
                        "emphasis": ["kindra.layer1", "meta.nietzsche"],
                    }
                }
            }
        }
