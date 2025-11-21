"""
KALDRA API — Engine router.

Exposes HTTP endpoints that wrap the KALDRA CORE engine.
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from kaldra_core.kaldra_engine import generate_kaldra_signal

from ..schemas.signal import KaldraSignalRequest, KaldraSignalResponse

router = APIRouter(
    prefix="/engine",
    tags=["engine"],
)


@router.post(
    "/kaldra/signal",
    response_model=KaldraSignalResponse,
    summary="Generate a KALDRA signal from input text.",
)
def generate_signal(payload: KaldraSignalRequest) -> KaldraSignalResponse:
    """
    Call the KALDRA CORE engine and wrap its result in a typed response model.
    """
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Input text must not be empty.")

    try:
        raw: Dict[str, Any] = generate_kaldra_signal(text)
    except Exception as exc:  # noqa: BLE001
        # In produção: logar exception, aqui só devolvemos erro genérico.
        raise HTTPException(
            status_code=500, detail=f"KALDRA engine error: {exc}"
        ) from exc

    # Normalizar saída mínima esperada
    return KaldraSignalResponse(
        archetype=str(raw.get("archetype", "UNSPECIFIED")),
        delta_state=str(raw.get("delta_state", "GENERIC")),
        tw_regime=str(raw.get("tw_regime", "STABLE")),  # type: ignore[arg-type]
        kindra_distribution=raw.get("kindra_distribution", {}),
        bias_score=float(raw.get("bias_score", 0.0)),
        meta_modifiers=raw.get("meta_modifiers", {}),
        confidence=float(raw.get("confidence", 0.0)),
        explanation=str(raw.get("explanation", "")),
        bias_label=raw.get("bias_label"),
        narrative_risk=raw.get("narrative_risk"),
    )
