"""
Request Models for KALDRA API Input Validation.

Defines Pydantic models for critical endpoints to ensure data integrity.
Gracefully handles environments where Pydantic is not installed.
"""

from __future__ import annotations
from typing import Optional, List, Any

try:
    from pydantic import BaseModel, Field, validator
except ImportError:  # pragma: no cover
    # Dummy BaseModel if Pydantic is missing
    class BaseModel:  # type: ignore
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        
        def dict(self):
            return self.__dict__

    def Field(*args, **kwargs):
        return None
        
    def validator(*args, **kwargs):
        return lambda x: x


class EngineInferenceRequest(BaseModel):
    """
    Validation model for Master Engine inference requests.
    Mirrors the structure expected by router_engine.
    """
    text: str = Field(..., min_length=1, description="Input text for analysis")
    embedding: Optional[List[float]] = Field(None, description="Optional pre-computed embedding")
    
    # Optional metadata fields that might be passed
    metadata: Optional[dict] = Field(default_factory=dict)


class AlphaAnalyzeRequest(BaseModel):
    """
    Validation model for Alpha engine analysis requests.
    """
    ticker: str = Field(..., min_length=1, max_length=10, description="Asset ticker symbol")
    context: str = Field(..., min_length=10, description="Contextual text for analysis")
    time_horizon: Optional[str] = Field("1w", description="Analysis time horizon")
