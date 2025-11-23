"""
KALDRA API — Pydantic schemas for KALDRA Engine signals.
"""
from __future__ import annotations

from typing import Dict, List, Literal, Mapping

from pydantic import BaseModel, Field


TWRegime = Literal["STABLE", "ANOMALY"]


class KaldraSignalRequest(BaseModel):
    text: str = Field(..., description="Input text to be analyzed by KALDRA.")


class KindraDistributionItem(BaseModel):
    state_index: int
    prob: float


class KaldraSignalResponse(BaseModel):
    archetype: str
    delta_state: str
    tw_regime: TWRegime
    kindra_distribution: List[KindraDistributionItem]
    bias_score: float
    meta_modifiers: Mapping[str, List[float]]
    confidence: float
    explanation: str

    # Campos extras que o engine já retorna (não obrigatórios na UI)
    bias_label: str | None = None
    narrative_risk: float | None = None
