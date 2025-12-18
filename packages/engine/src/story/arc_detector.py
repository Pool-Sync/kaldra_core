"""
Arc Detector implementation for KALDRA v3.2.

Detects Hero's Journey stages and narrative arcs.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .story_buffer import StoryEvent
from .timeline_builder import StoryTimeline

# Campbell's Hero's Journey Stages
JOURNEY_STAGES = [
    "ORDINARY_WORLD",
    "CALL_TO_ADVENTURE",
    "REFUSAL_OF_CALL",
    "MEETING_MENTOR",
    "CROSSING_THRESHOLD",
    "TESTS_ALLIES_ENEMIES",
    "APPROACH_INMOST_CAVE",
    "ORDEAL",
    "REWARD",
    "ROAD_BACK",
    "RESURRECTION",
    "RETURN_WITH_ELIXIR",
]

@dataclass
class StoryArc:
    """Detected narrative arc."""
    dominant_stage: str
    stage_scores: Dict[str, float]
    notes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ArcDetector:
    """
    Detects narrative structure and journey stages from events.
    """
    
    def __init__(self):
        # Keyword mappings for heuristic detection
        self.stage_keywords = {
            "ORDINARY_WORLD": ["normal", "routine", "status quo", "everyday", "calm"],
            "CALL_TO_ADVENTURE": ["opportunity", "challenge", "invitation", "threat", "message", "signal"],
            "REFUSAL_OF_CALL": ["hesitation", "fear", "doubt", "refuse", "ignore", "avoid"],
            "MEETING_MENTOR": ["guide", "teacher", "advice", "wisdom", "help", "mentor"],
            "CROSSING_THRESHOLD": ["commit", "enter", "start", "begin", "launch", "cross"],
            "TESTS_ALLIES_ENEMIES": ["test", "ally", "enemy", "friend", "foe", "struggle", "team"],
            "APPROACH_INMOST_CAVE": ["prepare", "plan", "approach", "danger", "deep"],
            "ORDEAL": ["crisis", "battle", "climax", "death", "failure", "peak", "confrontation"],
            "REWARD": ["success", "victory", "treasure", "gain", "achievement", "relief"],
            "ROAD_BACK": ["return", "leave", "escape", "pursuit"],
            "RESURRECTION": ["rebirth", "transform", "change", "final", "awakening"],
            "RETURN_WITH_ELIXIR": ["freedom", "solution", "heal", "knowledge", "gift", "end"]
        }
        
        # Archetype mappings (simplified)
        self.archetype_mappings = {
            "Hero": ["CALL_TO_ADVENTURE", "ORDEAL", "RESURRECTION"],
            "Mentor": ["MEETING_MENTOR"],
            "Shadow": ["ORDEAL", "TESTS_ALLIES_ENEMIES"],
            "Herald": ["CALL_TO_ADVENTURE"],
            "Threshold Guardian": ["CROSSING_THRESHOLD"],
            "Shapeshifter": ["TESTS_ALLIES_ENEMIES"],
            "Trickster": ["TESTS_ALLIES_ENEMIES"],
            "Ally": ["TESTS_ALLIES_ENEMIES"]
        }

    def detect(self, events: List[StoryEvent], timeline: Optional[StoryTimeline] = None) -> StoryArc:
        """
        Detect dominant journey stage from events.
        
        Snapshot-only detection using heuristics.
        
        Args:
            events: List of StoryEvents
            timeline: Optional pre-built timeline
            
        Returns:
            StoryArc object
        """
        if not events:
            return StoryArc(
                dominant_stage="ORDINARY_WORLD",
                stage_scores={s: 0.0 for s in JOURNEY_STAGES},
                notes=["No events provided"]
            )
            
        scores = {stage: 0.0 for stage in JOURNEY_STAGES}
        notes = []
        
        # Analyze events
        for event in events:
            text_lower = event.text.lower()
            
            # Keyword matching
            for stage, keywords in self.stage_keywords.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        scores[stage] += 1.0
            
            # Archetype matching
            if event.archetype_id:
                # Check if archetype maps to a stage
                # This assumes archetype_id might be "Mentor" or similar, 
                # or we map specific IDs (A01, etc.) to roles.
                # For Phase 1, we'll do a loose string check if ID contains role name
                for role, stages in self.archetype_mappings.items():
                    if role.lower() in event.archetype_id.lower():
                        for stage in stages:
                            scores[stage] += 2.0
                            
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            for stage in scores:
                scores[stage] /= total_score
        else:
            # Default if no signals found
            scores["ORDINARY_WORLD"] = 1.0
            notes.append("No strong narrative signals detected, defaulting to Ordinary World")
            
        # Find dominant stage
        dominant_stage = max(scores.items(), key=lambda x: x[1])[0]
        
        # Add notes
        notes.append(f"Dominant stage detected: {dominant_stage}")
        if timeline and timeline.metadata.get("has_cycle"):
            notes.append("Cyclical narrative pattern detected")
            
        return StoryArc(
            dominant_stage=dominant_stage,
            stage_scores=scores,
            notes=notes
        )
