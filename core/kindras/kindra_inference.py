"""
KALDRA CORE — Kindra inference engine (3×48).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from .normalization import l2_normalize, softmax
from .scoring import cosine_similarity

_VECTORS_CACHE: Dict[str, np.ndarray] | None = None


def _load_vectors() -> Dict[str, np.ndarray]:
    """
    Load Kindra vectors from vectors.json and cache them in memory.

    Returns:
        Dictionary mapping Kindra IDs to L2-normalized vectors
    """
    global _VECTORS_CACHE
    if _VECTORS_CACHE is not None:
        return _VECTORS_CACHE

    here = Path(__file__).resolve().parent
    data_path = here / "vectors.json"
    with data_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    mapping: Dict[str, np.ndarray] = {}
    for item in data.get("kindras", []):
        kid = item["id"]
        vec = np.asarray(item["vector"], dtype=float)
        mapping[kid] = l2_normalize(vec)

    _VECTORS_CACHE = mapping
    return mapping


def infer_kindra_distribution(input_vector: np.ndarray) -> Dict[str, Any]:
    """
    Compute a probability distribution over Kindras given an input vector.

    Args:
        input_vector: Input embedding or feature vector (any dimension)

    Returns:
        Dictionary containing:
            - distribution: {kindra_id: probability}
            - labels: [kindra_id, ...]
    """
    base = l2_normalize(input_vector)
    vectors = _load_vectors()

    if not vectors:
        return {"distribution": {}, "labels": []}

    scores: List[float] = []
    labels: List[str] = []

    for kid, kvec in vectors.items():
        labels.append(kid)
        scores.append(cosine_similarity(base, kvec))

    scores_arr = np.asarray(scores, dtype=float)
    probs = softmax(scores_arr)

    distribution = {label: float(p) for label, p in zip(labels, probs)}
    return {
        "distribution": distribution,
        "labels": labels,
    }
