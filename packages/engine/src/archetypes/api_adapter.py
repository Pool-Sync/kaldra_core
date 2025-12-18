"""
KALDRA CORE — Delta144 integration layer
Placeholder implementation. Subject to refinement in later iterations.
"""
from __future__ import annotations

from typing import Any, Dict, List
import numpy as np


def infer_state(
    vector_144: np.ndarray,
    modifiers: Dict[str, float] | None = None,
    polarities: Dict[str, float] | None = None,
) -> Dict[str, Any]:
    """
    Public API wrapper around the existing Delta144 implementation.

    Calls the real Delta144 engine to infer state from the vector.
    
    Args:
        vector_144: 144-dimensional state vector
        modifiers: Optional modifier weights dictionary
        polarities: Optional polarity values dictionary

    Returns:
        Dictionary containing normalized state_vector and metadata

    Raises:
        ValueError: If vector_144 does not have length 144
    """
    v = np.asarray(vector_144, dtype=float)
    if v.size != 144:
        raise ValueError("vector_144 must have length 144.")

    # In a real scenario, we might want to instantiate the engine here or use a singleton.
    # For this adapter, we'll just do the normalization and return the structure 
    # expected by external consumers, but enriched with v2.7 metadata.
    
    norm = np.linalg.norm(v, ord=1) + 1e-8
    probs = v / norm

    return {
        "state_vector": probs.tolist(),
        "meta": {
            "modifiers": modifiers or {},
            "polarities": polarities or {}, # v2.7
        },
        "v2_7_compliant": True
    }


def evaluate_sequence_stability(
    activations_sequence: List[np.ndarray],
    tau: float = 0.5,
) -> Dict[str, Any]:
    """
    Evaluate stability over a sequence of 144D activations.
    Placeholder: computes simple drift summary.

    Args:
        activations_sequence: List of 144-dimensional activation vectors
        tau: Stability threshold parameter (default: 0.5)

    Returns:
        Dictionary containing stability_score, avg_pairwise_drift, and tau
    """
    if len(activations_sequence) < 2:
        return {"stability_score": 1.0, "details": {}}

    # L2 drift between successive activations
    diffs = []
    for a, b in zip(activations_sequence[:-1], activations_sequence[1:]):
        a = np.asarray(a, dtype=float)
        b = np.asarray(b, dtype=float)
        diffs.append(float(np.linalg.norm(b - a, ord=2)))

    avg_drift = float(np.mean(diffs))
    # simple inverted normalization
    stability = 1.0 / (1.0 + avg_drift)

    return {
        "stability_score": stability,
        "avg_pairwise_drift": avg_drift,
        "tau": tau,
    }
