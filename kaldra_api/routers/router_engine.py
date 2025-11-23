"""
KALDRA API — Engine router.

Exposes HTTP endpoints that wrap the KALDRA Master Engine V2.
"""
from __future__ import annotations

import logging
import numpy as np
from fastapi import APIRouter, HTTPException, Depends

from ..dependencies import get_master_engine
from src.core.kaldra_master_engine import KaldraMasterEngineV2
from src.bias import compute_bias_score_from_text, classify_bias
from ..schemas.signal import KaldraSignalRequest, KaldraSignalResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/kaldra/signal",
    response_model=KaldraSignalResponse,
    summary="Generate a KALDRA signal from input text.",
)
def generate_signal(
    payload: KaldraSignalRequest,
    engine: KaldraMasterEngineV2 = Depends(get_master_engine)
) -> KaldraSignalResponse:
    """
    Call the KALDRA Master Engine V2 and return a structured signal.
    
    This endpoint now uses the real Master Engine V2, which orchestrates:
    - Delta144 (archetype inference)
    - Kindra Cultural Modulation
    - TW-Painlevé Oracle (anomaly detection)
    - Epistemic Limiter (confidence gating)
    """
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Input text must not be empty.")

    logger.info("KALDRA signal request received", extra={"text_len": len(text)})

    # Calculate bias score and label
    bias_score = 0.0
    bias_label = None
    try:
        bias_result = compute_bias_score_from_text(text)
        bias_score = float(bias_result["bias_score"])
        bias_label = classify_bias(bias_score)
    except Exception:
        # If bias calculation fails, continue with defaults
        pass

    try:
        # Simulate embedding generation (in prod, use a real encoder)
        # For now, use a simple hash-based deterministic vector
        embedding = _text_to_embedding(text)
        
        # Call Master Engine V2
        signal = engine.infer_from_embedding(embedding)
        
        # Extract top archetype
        top_idx = int(np.argmax(signal.archetype_probs))
        top_prob = float(signal.archetype_probs[top_idx])
        
        # Extract Delta144 state information
        delta = signal.delta_state or {}
        archetype_id = delta.get("archetype", {}).get("id", f"STATE_{top_idx:03d}")
        state_id = delta.get("state", {}).get("id", "INFERRED")
        
        # Prepare Kindra distribution (top 5 states)
        probs = signal.archetype_probs
        top_indices = probs.argsort()[-5:][::-1]
        kindra_distribution = [
            {"state_index": int(i), "prob": float(probs[i])}
            for i in top_indices
        ]
        
        # Calculate narrative risk (heuristic v0.1)
        # 40% bias, 30% TW, 30% low epistemic confidence
        conf = signal.epistemic.confidence or 0.0
        tw_factor = 1.0 if signal.tw_trigger else 0.0
        narrative_risk = (
            0.4 * bias_score +
            0.3 * tw_factor +
            0.3 * (1.0 - conf)
        )
        narrative_risk = max(0.0, min(1.0, float(narrative_risk)))
        
        logger.info(
            "KALDRA signal generated",
            extra={
                "top_idx": top_idx,
                "archetype_id": archetype_id,
                "confidence": conf,
                "tw_trigger": signal.tw_trigger,
                "bias_score": bias_score,
                "narrative_risk": narrative_risk,
            },
        )
        
        # Map to response schema
        return KaldraSignalResponse(
            archetype=archetype_id,
            delta_state=state_id,
            tw_regime="ANOMALY" if signal.tw_trigger else "STABLE",
            kindra_distribution=kindra_distribution,
            bias_score=bias_score,
            meta_modifiers={},
            confidence=float(signal.epistemic.confidence) if signal.epistemic.confidence is not None else 0.0,
            explanation=f"Master Engine V2: {signal.epistemic.status}",
            bias_label=bias_label,
            narrative_risk=narrative_risk,
        )
        
    except Exception as exc:
        logger.exception("KALDRA Master Engine error")
        raise HTTPException(
            status_code=500, detail=f"KALDRA Master Engine error: {exc}"
        ) from exc


def _text_to_embedding(text: str, d_ctx: int = 256) -> np.ndarray:
    """
    Placeholder: Convert text to embedding vector.
    In production, use a real sentence encoder (e.g., SentenceTransformers).
    """
    seed = sum(ord(c) for c in text) % (2**32)
    rng = np.random.RandomState(seed)
    return rng.randn(d_ctx)

