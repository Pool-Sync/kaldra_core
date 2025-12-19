"""
Delta12Vector - Explicit representation of base archetypal layer.

Represents the 12-dimensional probability distribution over fundamental archetypes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional


# 12 fundamental archetypes
ARCHETYPE_IDS = [
    "A01_INNOCENT",
    "A02_ORPHAN",
    "A03_WARRIOR",
    "A04_CAREGIVER",
    "A05_SEEKER",
    "A06_LOVER",
    "A07_RULER",
    "A08_REBEL",
    "A09_MAGICIAN",
    "A10_SAGE",
    "A11_JESTER",
    "A12_CREATOR",
]


@dataclass
class Delta12Vector:
    """
    12-dimensional probability distribution over archetypes.
    
    Represents Δ12 - the base archetypal layer.
    
    Attributes:
        values: Dictionary mapping archetype_id to probability
    """
    
    values: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize with zeros if empty."""
        if not self.values:
            self.values = {arch_id: 0.0 for arch_id in ARCHETYPE_IDS}
    
    def normalize(self) -> Delta12Vector:
        """
        Normalize to probability simplex (sum = 1.0).
        
        Returns:
            Normalized Delta12Vector
        """
        total = sum(self.values.values())
        
        if total == 0:
            # Uniform distribution if all zeros
            uniform_val = 1.0 / len(ARCHETYPE_IDS)
            self.values = {arch_id: uniform_val for arch_id in ARCHETYPE_IDS}
        else:
            self.values = {k: v / total for k, v in self.values.items()}
        
        return self
    
    def dominant(self) -> Tuple[str, float]:
        """
        Get dominant archetype.
        
        Returns:
            Tuple of (archetype_id, probability)
        """
        if not self.values:
            return ("UNKNOWN", 0.0)
        
        max_arch = max(self.values.items(), key=lambda x: x[1])
        return max_arch
    
    def top_k(self, k: int = 3) -> List[Tuple[str, float]]:
        """
        Get top-k archetypes by probability.
        
        Args:
            k: Number of top archetypes to return
            
        Returns:
            List of (archetype_id, probability) tuples, sorted descending
        """
        sorted_items = sorted(self.values.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:k]
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return self.values.copy()
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> Delta12Vector:
        """Create from dictionary."""
        return cls(values=data)

    def modulate(self, polarity_scores: Dict[str, float], intensity: float = 0.5) -> Delta12Vector:
        """
        v2.7: Modulate archetype probabilities based on polarity scores.
        
        Args:
            polarity_scores: Dict of {polarity_id: score (0.0-1.0)}
            intensity: Modulation strength (0.0-1.0)
            
        Returns:
            Self (modified in-place)
        """
        if not polarity_scores:
            return self
            
        new_values = self.values.copy()
        
        for arch_id, mapping in ARCHETYPE_POLARITY_MAP.items():
            if arch_id not in new_values:
                continue
                
            # Calculate modulation factor for this archetype
            factor = 1.0
            for pol_id, direction in mapping.items():
                if pol_id in polarity_scores:
                    score = polarity_scores[pol_id]
                    # Score 0.0 -> -1.0 effect, Score 1.0 -> +1.0 effect
                    # Normalized input score is 0..1.
                    # If direction is +1 (aligned with high score):
                    #   High score (1.0) -> Boost
                    #   Low score (0.0) -> Suppress
                    # If direction is -1 (aligned with low score):
                    #   Low score (0.0) -> Boost
                    #   High score (1.0) -> Suppress
                    
                    # Alignment: 1.0 if perfectly aligned, -1.0 if opposed
                    # score=1, dir=1 -> align=1
                    # score=0, dir=1 -> align=-1
                    # score=1, dir=-1 -> align=-1
                    # score=0, dir=-1 -> align=1
                    
                    # Formula: alignment = direction * (2 * score - 1)
                    alignment = direction * (2.0 * score - 1.0)
                    
                    # Apply intensity
                    factor += alignment * intensity
            
            # Apply factor (clamped to non-negative)
            new_values[arch_id] *= max(0.0, factor)
            
        self.values = new_values
        return self.normalize()



    
    @classmethod
    def from_list(cls, values: List[float]) -> Delta12Vector:
        """
        Create from list of 12 values.
        
        Args:
            values: List of 12 probabilities (in archetype order)
            
        Returns:
            Delta12Vector
        """
        if len(values) != 12:
            raise ValueError(f"Expected 12 values, got {len(values)}")
        
        return cls(values=dict(zip(ARCHETYPE_IDS, values)))
    
    def to_list(self) -> List[float]:
        """Convert to list of 12 values (in archetype order)."""
        return [self.values.get(arch_id, 0.0) for arch_id in ARCHETYPE_IDS]
    
    def __repr__(self) -> str:
        dominant_id, dominant_prob = self.dominant()
        return f"Delta12Vector(dominant={dominant_id}, prob={dominant_prob:.3f})"


def apply_meta_to_delta12(
    delta12: "Delta12Vector",
    nietzsche_scores: Optional[Dict[str, float]] = None,
    aurelius_scores: Optional[Dict[str, float]] = None,
    epsilon: float = 0.1
) -> "Delta12Vector":
    """
    Apply meta-signal adjustments to Delta12Vector.
    
    Makes small perturbations based on Nietzsche and Aurelius meta-scores,
    then re-normalizes to maintain probability distribution.
    
    Args:
        delta12: Original Delta12Vector
        nietzsche_scores: Nietzsche 12-axis scores (optional)
        aurelius_scores: Aurelius 12-axis scores (optional)
        epsilon: Maximum adjustment magnitude (default: 0.1)
        
    Returns:
        Adjusted and re-normalized Delta12Vector
        
    Example:
        >>> adjusted = apply_meta_to_delta12(
        ...     delta12,
        ...     nietzsche_scores={"will_to_power": 0.8, "dionysian_force": 0.6},
        ...     aurelius_scores={"serenity": 0.7, "discipline_of_will": 0.65}
        ... )
    """
    if nietzsche_scores is None and aurelius_scores is None:
        return delta12  # No adjustment
    
    # Copy current values
    adjusted_values = delta12.values.copy()
    
    # Nietzsche adjustments
    if nietzsche_scores:
        will_to_power = nietzsche_scores.get("will_to_power", 0.0)
        dionysian = nietzsche_scores.get("dionysian_force", 0.0)
        resentment = nietzsche_scores.get("resentment", 0.0)
        passive_nihilism = nietzsche_scores.get("passive_nihilism", 0.0)
        
        # High will to power → boost WARRIOR, REBEL, CREATOR
        if will_to_power > 0.6:
            boost = min(epsilon, (will_to_power - 0.6) * 0.25)
            adjusted_values["A03_WARRIOR"] = min(1.0, adjusted_values.get("A03_WARRIOR", 0.0) + boost)
            adjusted_values["A08_REBEL"] = min(1.0, adjusted_values.get("A08_REBEL", 0.0) + boost * 0.8)
            adjusted_values["A12_CREATOR"] = min(1.0, adjusted_values.get("A12_CREATOR", 0.0) + boost * 0.6)
        
        # High dionysian → boost chaotic archetypes
        if dionysian > 0.6:
            boost = min(epsilon * 0.5, (dionysian - 0.6) * 0.2)
            adjusted_values["A08_REBEL"] = min(1.0, adjusted_values.get("A08_REBEL", 0.0) + boost)
            adjusted_values["A11_JESTER"] = min(1.0, adjusted_values.get("A11_JESTER", 0.0) + boost * 0.7)
        
        # High resentment/passive nihilism → boost ORPHAN
        if resentment > 0.6 or passive_nihilism > 0.6:
            boost = min(epsilon * 0.5, max(resentment, passive_nihilism) * 0.15)
            adjusted_values["A02_ORPHAN"] = min(1.0, adjusted_values.get("A02_ORPHAN", 0.0) + boost)
    
    # Aurelius adjustments
    if aurelius_scores:
        serenity = aurelius_scores.get("serenity", 0.0)
        discipline = aurelius_scores.get("discipline_of_will", 0.0)
        control_dichotomy = aurelius_scores.get("control_dichotomy", 0.0)
        
        # High Stoic alignment → boost SAGE, RULER, CAREGIVER
        stoic_alignment = (serenity + discipline + control_dichotomy) / 3.0
        if stoic_alignment > 0.6:
            boost = min(epsilon, (stoic_alignment - 0.6) * 0.25)
            adjusted_values["A10_SAGE"] = min(1.0, adjusted_values.get("A10_SAGE", 0.0) + boost)
            adjusted_values["A07_RULER"] = min(1.0, adjusted_values.get("A07_RULER", 0.0) + boost * 0.7)
            adjusted_values["A04_CAREGIVER"] = min(1.0, adjusted_values.get("A04_CAREGIVER", 0.0) + boost * 0.5)
    
    # Re-normalize to sum to 1.0
    total = sum(adjusted_values.values())
    if total > 0:
        normalized_values = {k: v / total for k, v in adjusted_values.items()}
    else:
        # If all values are zero after adjustments, distribute uniformly
        normalized_values = {arch_id: 1.0 / len(ARCHETYPE_IDS) for arch_id in ARCHETYPE_IDS}
    
    return Delta12Vector(values=normalized_values)

# v2.7: Mapping of Archetypes to Polarities
# Format: {ArchetypeID: {PolarityID: Direction (+1 or -1)}}
ARCHETYPE_POLARITY_MAP = {
    "A01_INNOCENT": {
        "POL_ORDER_CHAOS": 1.0,      # Craves Order/Safety
        "POL_SAFETY_DANGER": 1.0,    # Craves Safety
        "POL_TRUST_SUSPICION": 1.0,  # Trusting
    },
    "A02_ORPHAN": {
        "POL_BELONGING_ALIENATION": -1.0, # Feels Alienation (low Belonging)
        "POL_REALISM_IDEALISM": 1.0,      # Realist
        "POL_SAFETY_DANGER": -1.0,        # Feels Danger
    },
    "A03_WARRIOR": {
        "POL_DOMINANCE_SERVICE": 1.0,     # Dominance/Win
        "POL_COURAGE_FEAR": 1.0,          # Courage
        "POL_ACTION_PASSIVITY": 1.0,      # Action
    },
    "A04_CAREGIVER": {
        "POL_DOMINANCE_SERVICE": -1.0,    # Service
        "POL_INDIVIDUAL_COLLECTIVE": -1.0,# Collective/Other-focus
        "POL_EMPATHY_APATHY": 1.0,        # Empathy
    },
    "A05_SEEKER": {
        "POL_STABILITY_VOLATILITY": -1.0, # Volatility/Change
        "POL_AUTONOMY_DEPENDENCE": 1.0,   # Autonomy
        "POL_KNOWN_UNKNOWN": -1.0,        # Seeks Unknown
    },
    "A06_LOVER": {
        "POL_INTIMACY_ISOLATION": 1.0,    # Intimacy
        "POL_INDIVIDUAL_COLLECTIVE": -1.0,# Connection
        "POL_PASSION_APATHY": 1.0,        # Passion
    },
    "A07_RULER": {
        "POL_ORDER_CHAOS": 1.0,           # Order
        "POL_HIERARCHY_NETWORK": 1.0,     # Hierarchy
        "POL_CONTROL_SURRENDER": 1.0,     # Control
    },
    "A08_REBEL": {
        "POL_ORDER_CHAOS": -1.0,          # Chaos/Disruption
        "POL_LIBERTY_OPPRESSION": 1.0,    # Liberty
        "POL_TRADITION_INNOVATION": -1.0, # Innovation/Break Tradition
    },
    "A09_MAGICIAN": {
        "POL_TRANSFORMATION_STASIS": 1.0, # Transformation
        "POL_RATIONAL_MYTHIC": -1.0,      # Mythic/Magic
        "POL_VISIBLE_INVISIBLE": -1.0,    # Invisible/Hidden laws
    },
    "A10_SAGE": {
        "POL_TRUTH_ILLUSION": 1.0,        # Truth
        "POL_RATIONAL_MYTHIC": 1.0,       # Rational/Logos
        "POL_KNOWLEDGE_IGNORANCE": 1.0,   # Knowledge
    },
    "A11_JESTER": {
        "POL_SERIOUSNESS_HUMOR": -1.0,    # Humor
        "POL_MEANING_VOID": -1.0,         # Play with Void/Absurd
        "POL_STRUCTURE_FLOW": -1.0,       # Flow/Spontaneity
    },
    "A12_CREATOR": {
        "POL_CREATION_DESTRUCTION": 1.0,  # Creation
        "POL_STRUCTURE_FLOW": 1.0,        # Structure (giving form)
        "POL_IMAGINATION_REALITY": 1.0,   # Imagination
    },
}
