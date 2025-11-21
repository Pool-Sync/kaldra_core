"""
KALDRA API — Pydantic schemas for KALDRA Engine signals.
"""
from __future__ import annotations

from typing import Dict, List, Literal, Mapping

from pydantic import BaseModel, Field


TWRegime = Literal["STABLE", "CRITICAL", "UNSTABLE"]


class KaldraSignalRequest(BaseModel):
    text: str = Field(..., description="Input text to be analyzed by KALDRA.")


class KaldraSignalResponse(BaseModel):
    archetype: str
    delta_state: str
    tw_regime: TWRegime
    kindra_distribution: Mapping[str, float]
    bias_score: float
    meta_modifiers: Mapping[str, List[float]]
    confidence: float
    explanation: str

    # Campos extras que o engine já retorna (não obrigatórios na UI)
    bias_label: str | None = None
    narrative_risk: str | None = None
