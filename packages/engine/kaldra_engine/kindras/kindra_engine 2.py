"""
KindraEngine v3.1 — 3×48 semantic/cultural engine.
"""
from typing import Dict, Any, List, Optional
import numpy as np

from src.unification.states.unified_state import KindraContext, KindraLayerScores
from src.kindras.loaders import (
    load_layer_vectors,
    load_layer_mapping
)
from src.kindras.llm_adapter import KindraLLMScorer

class KindraEngine:
    """
    KindraEngine v3.1 — 3×48 semantic/cultural engine.

    - Layer 1: Cultural/Macro (48)
    - Layer 2: Semiotic/Media (48)
    - Layer 3: Structural/Systemic (48)
    - Uses LLM scoring + embeddings + Kindra→Δ144 mapping normalized
    """

    def __init__(self, llm_scorer: Optional[KindraLLMScorer] = None):
        self.llm_scorer = llm_scorer or KindraLLMScorer()

        # Load vectors and maps
        self.layer1_vectors = load_layer_vectors(layer=1)
        self.layer2_vectors = load_layer_vectors(layer=2)
        self.layer3_vectors = load_layer_vectors(layer=3)

        self.layer1_map = load_layer_mapping(layer=1)
        self.layer2_map = load_layer_mapping(layer=2)
        self.layer3_map = load_layer_mapping(layer=3)

    def score_all_layers(
        self,
        text: str,
        embedding: Optional[np.ndarray] = None,
        delta144_state: Optional[str] = None,
        archetype_scores: Optional[Dict[str, float]] = None
    ) -> KindraContext:
        """
        Return KindraContext with 3×48 scores + TW-plane distribution + delta144_weights.
        """
        scores1 = self._score_layer(1, text, embedding, self.layer1_vectors, self.layer1_map)
        scores2 = self._score_layer(2, text, embedding, self.layer2_vectors, self.layer2_map)
        scores3 = self._score_layer(3, text, embedding, self.layer3_vectors, self.layer3_map)

        # Build KindraLayerScores objects
        layer1_obj = self._build_layer_scores(scores1)
        layer2_obj = self._build_layer_scores(scores2)
        layer3_obj = self._build_layer_scores(scores3)

        tw_dist = self._compute_tw_plane_distribution(layer1_obj, layer2_obj, layer3_obj)
        delta144_weights = self._aggregate_delta144_weights(scores1, scores2, scores3)

        return KindraContext(
            layer1=layer1_obj,
            layer2=layer2_obj,
            layer3=layer3_obj,
            tw_plane_distribution=tw_dist,
            delta144_weights=delta144_weights,
            metadata={"engine": "KindraEngine v3.1"}
        )
    
    def _build_layer_scores(self, scores: Dict[str, float]) -> KindraLayerScores:
        """Build KindraLayerScores from dict."""
        if not scores:
            return KindraLayerScores()
        
        avg = sum(scores.values()) / len(scores)
        max_val = max(scores.values())
        
        return KindraLayerScores(
            scores=scores,
            avg_score=avg,
            max_score=max_val
        )

    def _score_layer(
        self,
        layer: int,
        text: str,
        embedding: Optional[np.ndarray],
        vectors: Dict[str, Dict[str, Any]],
        layer_map: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Produce scores ∈ [0, 1] for the 48 vectors of a layer.
        """
        scores = {}
        for vid, vdef in vectors.items():
            # LLM/Heuristic Score
            raw_score = self.llm_scorer.score_vector(text, vdef)
            
            # TODO: Integrate embedding similarity if embedding is provided
            # For now, just use raw_score
            
            # Apply map boosts (if any logic requires it, e.g. based on global state)
            # Currently map is used for aggregation, but could influence score too.
            # We'll keep it simple for now.
            
            scores[vid] = raw_score
            
        return scores

    def _compute_tw_plane_distribution(
        self,
        l1: KindraLayerScores,
        l2: KindraLayerScores,
        l3: KindraLayerScores
    ) -> Dict[int, float]:
        """
        Calculate narrative energy distribution per 3/6/9 plane.
        """
        raw3 = l1.avg_score  # Layer 1 -> Plane 3 (Material/Cultural)
        raw6 = l2.avg_score  # Layer 2 -> Plane 6 (Relational/Media)
        raw9 = l3.avg_score  # Layer 3 -> Plane 9 (Abstract/Systemic)

        total = raw3 + raw6 + raw9 + 1e-8
        return {
            3: raw3 / total,
            6: raw6 / total,
            9: raw9 / total
        }

    def _aggregate_delta144_weights(
        self,
        l1: Dict[str, float],
        l2: Dict[str, float],
        l3: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Use normalized maps to accumulate weight on Delta144 states.
        """
        weights = {}
        
        def process_layer(scores, mapping):
            for vid, score in scores.items():
                if score <= 0: continue
                
                map_info = mapping.get(vid)
                if not map_info: continue
                
                # map_info is likely a dict with 'delta144_targets' or similar
                # Or based on schema: {"kindra_vector_id": "...", "delta144_targets": [{"id": "A01_CREATOR", "weight": 0.5}, ...]}
                targets = map_info.get('delta144_targets', [])
                
                for target in targets:
                    tid = target.get('id')
                    tweight = target.get('weight', 1.0)
                    
                    if tid:
                        weights[tid] = weights.get(tid, 0.0) + (score * tweight)

        process_layer(l1, self.layer1_map)
        process_layer(l2, self.layer2_map)
        process_layer(l3, self.layer3_map)
        
        # Normalize
        total = sum(weights.values())
        if total > 0:
            for k in weights:
                weights[k] /= total
                
        return weights
