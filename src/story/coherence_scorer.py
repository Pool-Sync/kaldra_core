"""
Coherence Scorer implementation for KALDRA v3.2.

Computes narrative consistency and coherence metrics.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from .story_buffer import StoryEvent
from .timeline_builder import StoryTimeline
from .arc_detector import StoryArc


@dataclass
class CoherenceScore:
    """Metrics for narrative coherence."""
    overall: float                         # [0, 1]
    archetype_consistency: float           # [0, 1]
    polarity_smoothness: float             # [0, 1]
    stage_alignment: float                 # [0, 1]
    notes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class CoherenceScorer:
    """
    Evaluates the coherence of a narrative sequence.
    """
    
    def score(
        self,
        events: List[StoryEvent],
        timeline: StoryTimeline,
        arc: StoryArc,
    ) -> CoherenceScore:
        """
        Compute basic temporal coherence scores.
        
        Args:
            events: List of StoryEvents
            timeline: StoryTimeline object
            arc: StoryArc object
            
        Returns:
            CoherenceScore object
        """
        if not events:
            return CoherenceScore(0.0, 0.0, 0.0, 0.0, ["No events to score"])
            
        notes = []
        
        # 1. Archetype Consistency
        # Measure how often we switch archetypes relative to total events
        # Fewer switches = higher consistency (simplistic heuristic)
        # Or: dominant archetype presence
        
        num_transitions = sum(timeline.transition_counts.values())
        if len(events) > 1:
            # Ratio of transitions to possible transitions (events - 1)
            # High transition ratio = low consistency (whipsawing)
            transition_ratio = num_transitions / (len(events) - 1)
            archetype_consistency = 1.0 - min(transition_ratio, 1.0)
        else:
            archetype_consistency = 1.0
            
        # 2. Polarity Smoothness
        # Measure abrupt flips in polarity (e.g. pos -> neg)
        # We'll look at a primary polarity key if available, or average
        polarity_flips = 0
        total_polarity_checks = 0
        
        # Assume "sentiment" or similar key in polarities
        primary_key = "sentiment" 
        
        last_val = None
        for event in events:
            if primary_key in event.polarities:
                val = event.polarities[primary_key]
                if last_val is not None:
                    # Check for sign flip
                    if (last_val > 0 and val < 0) or (last_val < 0 and val > 0):
                        polarity_flips += 1
                    total_polarity_checks += 1
                last_val = val
                
        if total_polarity_checks > 0:
            smoothness = 1.0 - (polarity_flips / total_polarity_checks)
        else:
            smoothness = 1.0  # Default if no polarity data
            notes.append("No polarity data found for smoothness check")
            
        # 3. Stage Alignment
        # Check if events align with dominant stage
        # This is tricky without per-event stage scoring in the buffer
        # For Phase 1, we'll use the arc confidence (score of dominant stage)
        dominant_score = arc.stage_scores.get(arc.dominant_stage, 0.0)
        stage_alignment = dominant_score
        
        # Overall Score
        # Weighted average
        overall = (
            (archetype_consistency * 0.4) +
            (smoothness * 0.3) +
            (stage_alignment * 0.3)
        )
        
        return CoherenceScore(
            overall=overall,
            archetype_consistency=archetype_consistency,
            polarity_smoothness=smoothness,
            stage_alignment=stage_alignment,
            notes=notes
        )
