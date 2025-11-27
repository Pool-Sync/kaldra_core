"""Domain-level analysis utilities for KALDRA-Alpha earnings results."""

from typing import Dict, Any, List
import numpy as np

from src.apps.alpha.earnings_pipeline import EarningsPipelineResult

def summarize_archetypes(result: EarningsPipelineResult, top_k: int = 3) -> Dict[str, Any]:
    """
    Summarize archetype distribution at the earnings-call level.
    Returns:
      {
        "top_indices": [int, ...],
        "top_probs": [float, ...],
        "entropy": float,
      }
    """
    signal = result.signal
    if not hasattr(signal, "archetype_probs"):
        return {"top_indices": [], "top_probs": [], "entropy": 0.0}
        
    probs = np.array(signal.archetype_probs)
    
    # Top K
    top_indices = probs.argsort()[-top_k:][::-1]
    top_probs = probs[top_indices]
    
    # Entropy
    # Avoid log(0)
    safe_probs = np.maximum(probs, 1e-10)
    entropy = -np.sum(safe_probs * np.log(safe_probs))
    
    return {
        "top_indices": [int(i) for i in top_indices],
        "top_probs": [float(p) for p in top_probs],
        "entropy": float(entropy)
    }


def build_alpha_signal_payload(result: EarningsPipelineResult) -> Dict[str, Any]:
    """
    Build a compact JSON-ready payload for Alpha dashboards.
    Should not depend on any web framework.
    """
    summary = summarize_archetypes(result, top_k=5)
    
    # Extract signal attributes safely
    signal = result.signal
    tw_trigger = getattr(signal, "tw_trigger", False)
    epistemic_status = "UNKNOWN"
    if hasattr(signal, "epistemic") and hasattr(signal.epistemic, "status"):
        epistemic_status = signal.epistemic.status
        
    return {
        "ticker": result.ticker,
        "quarter": result.quarter,
        "top_archetypes": [
            {"index": idx, "probability": prob} 
            for idx, prob in zip(summary["top_indices"], summary["top_probs"])
        ],
        "entropy": summary["entropy"],
        "tw_trigger": tw_trigger,
        "epistemic_status": epistemic_status,
        "narrative_coherence": None, # Placeholder for Story Aggregation
        "metadata": result.metadata
    }
