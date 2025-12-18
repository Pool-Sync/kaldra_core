"""
Timeline Builder implementation for KALDRA v3.2.

Constructs narrative timelines and tracks archetype transitions.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .story_buffer import StoryEvent


@dataclass
class ArchetypeTransition:
    """Record of a transition between two archetypes."""
    from_id: str
    to_id: str
    count: int = 1


@dataclass
class StoryTimeline:
    """Aggregated timeline of events and transitions."""
    events: List[StoryEvent]
    archetype_transitions: List[ArchetypeTransition] = field(default_factory=list)
    transition_counts: Dict[str, int] = field(default_factory=dict)  # "A01->A04": 3
    metadata: Dict[str, Any] = field(default_factory=dict)


class TimelineBuilder:
    """
    Builds StoryTimelines from sequences of StoryEvents.
    """
    
    def build(self, events: List[StoryEvent]) -> StoryTimeline:
        """
        Build a timeline from ordered StoryEvents.
        
        Tracks archetype transitions and detects simple patterns.
        
        Args:
            events: List of StoryEvent objects (assumed sorted)
            
        Returns:
            StoryTimeline object
        """
        # Ensure events are sorted by timestamp
        sorted_events = sorted(events, key=lambda e: e.timestamp)
        
        transitions: List[ArchetypeTransition] = []
        transition_counts: Dict[str, int] = {}
        
        # Track transitions
        last_archetype = None
        
        for event in sorted_events:
            current_archetype = event.archetype_id
            
            if current_archetype and last_archetype and current_archetype != last_archetype:
                # Register transition
                key = f"{last_archetype}->{current_archetype}"
                transition_counts[key] = transition_counts.get(key, 0) + 1
                
                # Add to list (simplified: we don't store every instance object, 
                # but we could. For now, let's store unique transitions or just counts)
                # The spec says "List[ArchetypeTransition]", implying we might want 
                # a list of all transitions or unique ones. 
                # Let's store unique transitions with counts in the list for now, 
                # matching the transition_counts dict.
                
            if current_archetype:
                last_archetype = current_archetype
        
        # Populate archetype_transitions list from counts
        for key, count in transition_counts.items():
            from_id, to_id = key.split("->")
            transitions.append(ArchetypeTransition(from_id, to_id, count))
            
        # Metadata analysis
        metadata = {}
        
        # Simple cycle detection (e.g. A->B->A)
        # This is a heuristic check for now
        has_cycle = False
        for key in transition_counts:
            from_id, to_id = key.split("->")
            reverse_key = f"{to_id}->{from_id}"
            if reverse_key in transition_counts:
                has_cycle = True
                break
        
        metadata["has_cycle"] = has_cycle
        
        # Dominant transition
        if transition_counts:
            dominant = max(transition_counts.items(), key=lambda x: x[1])
            metadata["dominant_transition"] = dominant[0]
            
        return StoryTimeline(
            events=sorted_events,
            archetype_transitions=transitions,
            transition_counts=transition_counts,
            metadata=metadata
        )
