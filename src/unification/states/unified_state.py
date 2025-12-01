"""
Unified State Definitions for KALDRA v3.0.

Provides a consistent state representation across the entire pipeline.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
import time
import uuid
import numpy as np

# Import v2.9 state definitions
from src.common.unified_state import DriftState, TauState
from src.common.unified_signal import MetaSignal, SafeguardSignal, StoryEvent
from src.archetypes.delta12_vector import Delta12Vector


@dataclass
class GlobalContext:
    """
    Global context for the entire pipeline execution.
    """
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    mode: str = "full"  # "signal" | "story" | "full" | "safety-first" | "exploratory"
    version: str = "3.0"
    degraded: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class InputContext:
    """
    Context for input processing stage.
    """
    text: str
    embedding: Optional[np.ndarray] = None
    bias_score: float = 0.0
    tau_input: Optional[TauState] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        # Convert numpy array to list for JSON serialization
        if self.embedding is not None:
            data['embedding'] = self.embedding.tolist()
        if self.tau_input is not None:
            data['tau_input'] = self.tau_input.to_dict()
        return data


@dataclass
class ArchetypeContext:
    """
    Context for archetypal analysis.
    """
    delta12: Optional[Delta12Vector] = None
    delta144_state: Optional[Any] = None  # StateInferenceResult
    polarity_scores: Dict[str, float] = field(default_factory=dict)
    modifier_scores: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        data = {
            'delta12': self.delta12.to_dict() if self.delta12 else None,
            'delta144_state': self.delta144_state.to_dict() if self.delta144_state else None,
            'polarity_scores': self.polarity_scores,
            'modifier_scores': self.modifier_scores
        }
        return data


@dataclass
class DriftContext:
    """
    Context for drift and TW369 analysis.
    """
    tw_state: Optional[Any] = None  # TWState
    drift_state: Optional[DriftState] = None
    regime: str = "UNKNOWN"
    drift_metric: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'tw_state': self.tw_state.to_dict() if self.tw_state else None,
            'drift_state': self.drift_state.to_dict() if self.drift_state else None,
            'regime': self.regime,
            'drift_metric': self.drift_metric
        }


@dataclass
class MetaContext:
    """
    Context for meta-engine analysis.
    """
    nietzsche: Optional[MetaSignal] = None
    aurelius: Optional[MetaSignal] = None
    campbell: Optional[MetaSignal] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'nietzsche': asdict(self.nietzsche) if self.nietzsche else None,
            'aurelius': asdict(self.aurelius) if self.aurelius else None,
            'campbell': asdict(self.campbell) if self.campbell else None
        }


@dataclass
class StoryContext:
    """
    Context for story and narrative analysis.
    """
    events: List[StoryEvent] = field(default_factory=list)
    arc: Optional[Any] = None  # NarrativeArc
    timeline: Optional[Any] = None  # ArchetypalTimeline
    coherence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'events': [e.to_dict() for e in self.events],
            'arc': self.arc.to_dict() if self.arc and hasattr(self.arc, 'to_dict') else None,
            'timeline': self.timeline.to_dict() if self.timeline and hasattr(self.timeline, 'to_dict') else None,
            'coherence': self.coherence
        }


@dataclass
class RiskContext:
    """
    Context for risk and safety analysis.
    """
    tau_output: Optional[TauState] = None
    safeguard: Optional[SafeguardSignal] = None
    final_risk: str = "UNKNOWN"
    risk_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'tau_output': self.tau_output.to_dict() if self.tau_output else None,
            'safeguard': self.safeguard.to_dict() if self.safeguard else None,
            'final_risk': self.final_risk,
            'risk_score': self.risk_score
        }


@dataclass
class KindraLayerScores:
    """
    Container for 48 Kindra vectors in a specific layer.
    Example:
        scores = {"E01": 0.42, "E02": 0.76, ...}
    """
    scores: Dict[str, float] = field(default_factory=dict)
    avg_score: float = 0.0
    max_score: float = 0.0

    def to_json(self) -> Dict[str, Any]:
        return {
            "scores": self.scores,
            "avg_score": self.avg_score,
            "max_score": self.max_score,
        }


@dataclass
class KindraContext:
    """
    Represents 144 Kindra vectors (3×48) + aggregates.
    Single reference object for MetaStage, StoryStage, and OutputStage.
    """
    # 3 Kindra layers (each with 48 vectors)
    layer1: KindraLayerScores = field(default_factory=KindraLayerScores)
    layer2: KindraLayerScores = field(default_factory=KindraLayerScores)
    layer3: KindraLayerScores = field(default_factory=KindraLayerScores)

    # TW-plane distribution (3/6/9)
    tw_plane_distribution: Dict[int, float] = field(default_factory=dict)

    # Δ144 distribution derived from Kindra maps
    delta144_weights: Dict[str, float] = field(default_factory=dict)

    # Auxiliary metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_total_vectors(self) -> int:
        """
        Returns the total number of available Kindra vectors.
        Should always be 144 (3×48).
        """
        return (
            len(self.layer1.scores)
            + len(self.layer2.scores)
            + len(self.layer3.scores)
        )
    
    def get_top_vectors(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Returns the top n Kindra vectors considering all three layers combined.
        Result: list of dicts: [{"id": "...", "score": 0.87, "layer": 2}, ...]
        """
        all_vecs = []

        # Add Layer 1
        for vid, score in self.layer1.scores.items():
            all_vecs.append({"id": vid, "score": score, "layer": 1})

        # Add Layer 2
        for vid, score in self.layer2.scores.items():
            all_vecs.append({"id": vid, "score": score, "layer": 2})

        # Add Layer 3
        for vid, score in self.layer3.scores.items():
            all_vecs.append({"id": vid, "score": score, "layer": 3})

        # Sort by score desc
        all_vecs.sort(key=lambda x: x["score"], reverse=True)

        return all_vecs[:n]
    
    def to_json(self) -> Dict[str, Any]:
        return {
            "layer1": self.layer1.to_json(),
            "layer2": self.layer2.to_json(),
            "layer3": self.layer3.to_json(),
            "tw_plane_distribution": self.tw_plane_distribution,
            "delta144_weights": self.delta144_weights,
            "metadata": self.metadata,
        }
    
    @staticmethod
    def from_json(data: Dict[str, Any]) -> "KindraContext":
        return KindraContext(
            layer1=KindraLayerScores(**data.get("layer1", {})),
            layer2=KindraLayerScores(**data.get("layer2", {})),
            layer3=KindraLayerScores(**data.get("layer3", {})),
            tw_plane_distribution=data.get("tw_plane_distribution", {}),
            delta144_weights=data.get("delta144_weights", {}),
            metadata=data.get("metadata", {}),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Legacy compatibility method - use to_json() for new code."""
        return {
            'layer1': self.layer1.scores,
            'layer2': self.layer2.scores,
            'layer3': self.layer3.scores,
            'tw_plane_distribution': self.tw_plane_distribution,
            'delta144_weights': self.delta144_weights,
            'metadata': self.metadata
        }


@dataclass
class UnifiedContext:
    """
    Complete unified context for the entire pipeline.
    
    This is the central state object passed through all pipeline stages.
    """
    global_ctx: GlobalContext = field(default_factory=GlobalContext)
    input_ctx: Optional[InputContext] = None
    kindra_ctx: Optional[KindraContext] = None
    archetype_ctx: Optional[ArchetypeContext] = None
    drift_ctx: Optional[DriftContext] = None
    meta_ctx: Optional[MetaContext] = None
    story_ctx: Optional[StoryContext] = None
    risk_ctx: Optional[RiskContext] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert entire context to dictionary."""
        return {
            'global': self.global_ctx.to_dict(),
            'input': self.input_ctx.to_dict() if self.input_ctx else None,
            'kindra': self.kindra_ctx.to_dict() if self.kindra_ctx else None,
            'archetypes': self.archetype_ctx.to_dict() if self.archetype_ctx else None,
            'drift': self.drift_ctx.to_dict() if self.drift_ctx else None,
            'meta': self.meta_ctx.to_dict() if self.meta_ctx else None,
            'story': self.story_ctx.to_dict() if self.story_ctx else None,
            'risk': self.risk_ctx.to_dict() if self.risk_ctx else None
        }
