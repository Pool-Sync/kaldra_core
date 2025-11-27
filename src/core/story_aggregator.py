"""
Story-level aggregation utilities for KALDRA Core.

This module does NOT depend on internal engine implementation details.
It only consumes a minimal protocol-compatible view of KaldraSignal-like
objects (see StoryTurnSignal below).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from collections import Counter

import numpy as np


@dataclass
class StoryTurnSignal:
    """
    Minimal view over a KALDRA signal for story-level aggregation.

    This is intentionally light and protocol-based. Any object with
    these attributes can be adapted:

      - archetype_probs: np.ndarray shape (144,) or similar
      - delta_state: Optional[dict] with at least an 'id' key (if available)
      - tw_trigger: Optional[bool]
      - tw_stats: Optional[dict] (may contain 'severity' or similar)
      - epistemic: Optional[object] with a 'status' attribute

    This dataclass is used for internal normalization only and does not
    change engine behavior.
    """

    archetype_probs: np.ndarray
    delta_state: Optional[Dict[str, Any]] = None
    tw_trigger: Optional[bool] = None
    tw_stats: Optional[Dict[str, Any]] = None
    epistemic_status: Optional[str] = None

    @classmethod
    def from_signal(cls, signal: Any) -> "StoryTurnSignal":
        """
        Build from a KaldraSignal-like object.

        This method should be robust to missing attributes.
        """
        probs = getattr(signal, "archetype_probs", None)
        if probs is None:
            raise ValueError("Signal is missing 'archetype_probs'.")

        probs_np = np.asarray(probs, dtype=np.float32)
        if probs_np.ndim != 1:
            probs_np = probs_np.reshape(-1)

        delta_state = getattr(signal, "delta_state", None)
        tw_trigger = getattr(signal, "tw_trigger", None)
        tw_stats = getattr(signal, "tw_stats", None)
        epistemic = getattr(signal, "epistemic", None)
        epistemic_status = getattr(epistemic, "status", None) if epistemic is not None else None

        return cls(
            archetype_probs=probs_np,
            delta_state=delta_state,
            tw_trigger=bool(tw_trigger) if tw_trigger is not None else None,
            tw_stats=tw_stats,
            epistemic_status=epistemic_status,
        )


class StoryAggregator:
    """
    Aggregates multiple KALDRA turn-level signals into a story-level
    representation compatible with schema/story/story_schema.json.
    """

    def __init__(self, top_k_archetypes: int = 3) -> None:
        self.top_k_archetypes = top_k_archetypes

    # -------------------------
    # Public API
    # -------------------------

    def aggregate(
        self,
        story_id: str,
        turns: Sequence[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Aggregate a sequence of turns into a story-level object.

        Each turn is expected to be a dict with at least:
          - 'turn_index': int
          - 'timestamp': str (ISO datetime)
          - 'role': str
          - 'text': str
          - 'signal': KaldraSignal-like object (or already a StoryTurnSignal)

        Returns:
            dict compatible with schema/story/story_schema.json (subset).
        """
        # Normalize and collect StoryTurnSignal instances.
        normalized_turns: List[Tuple[Dict[str, Any], StoryTurnSignal]] = []
        for t in turns:
            signal_obj = t.get("signal")
            if isinstance(signal_obj, StoryTurnSignal):
                sts = signal_obj
            else:
                sts = StoryTurnSignal.from_signal(signal_obj)
            normalized_turns.append((t, sts))

        # Build per-turn summaries and Δ144 evolution.
        turn_summaries: List[Dict[str, Any]] = []
        delta_evolution: List[Dict[str, Any]] = []
        archetype_indices: List[int] = []
        coherence_trace: List[Dict[str, Any]] = []

        for t, sts in normalized_turns:
            probs = sts.archetype_probs
            top_idx = int(np.argmax(probs))
            top_prob = float(probs[top_idx])
            archetype_indices.append(top_idx)

            delta_state_id = None
            if isinstance(sts.delta_state, dict):
                delta_state_id = sts.delta_state.get("id") or sts.delta_state.get("state_id")

            tw_severity = None
            if isinstance(sts.tw_stats, dict):
                tw_severity = sts.tw_stats.get("severity")

            signal_summary = {
                "archetype_top_index": top_idx,
                "archetype_top_prob": top_prob,
                "delta_state_id": delta_state_id,
                "tw_trigger": sts.tw_trigger,
                "tw_severity": tw_severity,
                "epistemic_status": sts.epistemic_status,
            }

            turn_summaries.append(
                {
                    "turn_id": t.get("turn_id"),
                    "turn_index": int(t["turn_index"]),
                    "timestamp": t["timestamp"],
                    "role": t["role"],
                    "text": t["text"],
                    "metadata": t.get("metadata", {}),
                    "signal_summary": signal_summary,
                }
            )

            if delta_state_id is not None:
                delta_evolution.append(
                    {
                        "turn_index": int(t["turn_index"]),
                        "delta_state_id": delta_state_id,
                        "profile": sts.delta_state.get("profile") if isinstance(sts.delta_state, dict) else None,
                    }
                )

            # Simple placeholder coherence: higher if top archetype is stable.
            coherence_trace.append(
                {
                    "turn_index": int(t["turn_index"]),
                    "coherence": top_prob
                }
            )

        # Compute aggregate coherence and dominant archetypes.
        narrative_coherence = self._compute_coherence(archetype_indices, coherence_trace)
        dominant_archetypes = self._compute_dominant_archetypes(archetype_indices)

        story_obj: Dict[str, Any] = {
            "story_id": story_id,
            "turns": turn_summaries,
            "delta144_evolution": delta_evolution,
            "narrative_coherence": narrative_coherence,
            "dominant_archetypes": dominant_archetypes,
            "coherence_trace": coherence_trace,
            "metadata": {},
        }
        return story_obj

    # -------------------------
    # Internal helpers
    # -------------------------

    def _compute_dominant_archetypes(self, indices: Sequence[int]) -> List[int]:
        if not indices:
            return []
        counter = Counter(indices)
        most_common = counter.most_common(self.top_k_archetypes)
        return [idx for idx, _ in most_common]

    def _compute_coherence(
        self,
        indices: Sequence[int],
        coherence_trace: Sequence[Dict[str, Any]],
    ) -> float:
        """
        Placeholder coherence metric v1.0.

        Combines:
          - Stability of dominant archetype across turns
          - Average of per-turn top probabilities (if available)
        """
        if not indices:
            return 0.0

        # Archetype stability: fraction of turns where archetype matches previous.
        matches = 0
        for i in range(1, len(indices)):
            if indices[i] == indices[i - 1]:
                matches += 1
        stability = matches / max(1, len(indices) - 1)

        # Average coherence from trace.
        if coherence_trace:
            avg_conf = float(
                sum(float(item.get("coherence", 0.0)) for item in coherence_trace)
                / max(1, len(coherence_trace))
            )
        else:
            avg_conf = 0.0

        # Simple blend.
        return float(max(0.0, min(1.0, 0.5 * stability + 0.5 * avg_conf)))
