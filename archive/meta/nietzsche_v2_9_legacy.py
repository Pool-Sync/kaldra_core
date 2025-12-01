"""
NietzscheEngine-12 - 12-Dimensional Nietzschean Analysis.

Analyzes text through 12 Nietzschean axes:
1. will_to_power - Drive for dominance, creation, self-overcoming
2. resentment - Envy, victimization, reactive negativity
3. life_affirmation - Positive embrace of existence
4. life_negation - Rejection, exhaustion, world-weariness
5. free_spirit - Independence from tradition and convention
6. active_nihilism - Creative destruction, burning the old
7. passive_nihilism - Despair, apathy, giving up
8. eternal_return_acceptance - Radical acceptance of fate
9. transvaluation - Inversion of traditional values
10. dionysian_force - Chaos, excess, primal energy
11. apollonian_order - Form, harmony, rational structure
12. amor_fati - Loving acceptance of what is
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Tuple
import re


@dataclass
class NietzscheProfile:
    """12-dimensional Nietzschean profile."""
    will_to_power: float = 0.0
    resentment: float = 0.0
    life_affirmation: float = 0.0
    life_negation: float = 0.0
    free_spirit: float = 0.0
    active_nihilism: float = 0.0
    passive_nihilism: float = 0.0
    eternal_return_acceptance: float = 0.0
    transvaluation: float = 0.0
    dionysian_force: float = 0.0
    apollonian_order: float = 0.0
    amor_fati: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return asdict(self)
    
    def dominant_axes(self, top_k: int = 3) -> List[Tuple[str, float]]:
        """Get top K dominant axes."""
        scores = self.to_dict()
        sorted_axes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_axes[:top_k]
    
    def overall_severity(self) -> float:
        """Calculate overall intensity/severity."""
        scores = self.to_dict()
        # Use max of positive axes
        positive_axes = ["will_to_power", "life_affirmation", "free_spirit", 
                        "active_nihilism", "eternal_return_acceptance", 
                        "transvaluation", "dionysian_force", "amor_fati"]
        positive_max = max([scores[ax] for ax in positive_axes if ax in scores], default=0.0)
        
        # Use max of negative axes
        negative_axes = ["resentment", "life_negation", "passive_nihilism"]
        negative_max = max([scores[ax] for ax in negative_axes if ax in scores], default=0.0)
        
        return max(positive_max, negative_max)


@dataclass
class MetaEngineResult:
    """Result from meta-engine analysis."""
    scores: Dict[str, float]
    dominant_axes: List[Tuple[str, float]]
    severity: float
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


# Keyword patterns for each axis
WILL_TO_POWER_KEYWORDS = [
    "dominate", "power", "lead", "conquer", "overcome", "master", "control",
    "strength", "force", "command", "superior", "excel", "triumph", "victory"
]

RESENTMENT_KEYWORDS = [
    "unfair", "victim", "blame", "envy", "jealous", "deserve", "owe me",
    "they have", "not fair", "why them", "bitter", "grudge", "resent"
]

LIFE_AFFIRMATION_KEYWORDS = [
    "yes to life", "embrace", "celebrate", "joy", "vitality", "energy",
    "alive", "thrive", "flourish", "growth", "create", "build"
]

LIFE_NEGATION_KEYWORDS = [
    "exhausted", "tired of", "give up", "pointless", "meaningless", "empty",
    "void", "nothingness", "despair", "hopeless", "weary", "burden"
]

FREE_SPIRIT_KEYWORDS = [
    "independent", "think differently", "question", "rebel", "break free",
    "unconventional", "my own path", "reject tradition", "challenge"
]

ACTIVE_NIHILISM_KEYWORDS = [
    "destroy", "tear down", "burn", "demolish", "creative destruction",
    "break apart", "dismantle", "overthrow", "revolution"
]

PASSIVE_NIHILISM_KEYWORDS = [
    "nothing matters", "why bother", "apathy", "indifferent", "don't care",
    "numb", "detached", "resigned", "surrender"
]

ETERNAL_RETURN_KEYWORDS = [
    "do it again", "repeat", "cycle", "eternal", "forever", "again and again",
    "same path", "relive", "infinite loop"
]

TRANSVALUATION_KEYWORDS = [
    "weakness is strength", "invert", "reverse", "opposite", "revalue",
    "new values", "beyond good and evil", "redefine"
]

DIONYSIAN_KEYWORDS = [
    "chaos", "wild", "primal", "instinct", "passion", "ecstasy", "frenzy",
    "excess", "intoxication", "abandon", "raw"
]

APOLLONIAN_KEYWORDS = [
    "order", "structure", "form", "harmony", "balance", "rational", "measured",
    "controlled", "disciplined", "systematic", "organized"
]

AMOR_FATI_KEYWORDS = [
    "accept", "embrace fate", "love what is", "necessary", "meant to be",
    "grateful for", "wouldn't change", "perfect as is"
]


def analyze_meta(
    text: str,
    *,
    delta12: Optional[Any] = None,
    delta144_state: Optional[str] = None,
    tw_state: Optional[Any] = None,
    bias_score: Optional[float] = None,
) -> MetaEngineResult:
    """
    Analyze text through 12 Nietzschean axes.
    
    Args:
        text: Input text to analyze
        delta12: Optional Delta12Vector for archetype context
        delta144_state: Optional current Δ144 state
        tw_state: Optional TWState for drift context
        bias_score: Optional bias score
        
    Returns:
        MetaEngineResult with 12-dimensional analysis
    """
    text_lower = text.lower()
    
    # Calculate each axis
    profile = NietzscheProfile(
        will_to_power=_score_keywords(text_lower, WILL_TO_POWER_KEYWORDS),
        resentment=_score_keywords(text_lower, RESENTMENT_KEYWORDS),
        life_affirmation=_score_keywords(text_lower, LIFE_AFFIRMATION_KEYWORDS),
        life_negation=_score_keywords(text_lower, LIFE_NEGATION_KEYWORDS),
        free_spirit=_score_keywords(text_lower, FREE_SPIRIT_KEYWORDS),
        active_nihilism=_score_keywords(text_lower, ACTIVE_NIHILISM_KEYWORDS),
        passive_nihilism=_score_keywords(text_lower, PASSIVE_NIHILISM_KEYWORDS),
        eternal_return_acceptance=_score_keywords(text_lower, ETERNAL_RETURN_KEYWORDS),
        transvaluation=_score_keywords(text_lower, TRANSVALUATION_KEYWORDS),
        dionysian_force=_score_keywords(text_lower, DIONYSIAN_KEYWORDS),
        apollonian_order=_score_keywords(text_lower, APOLLONIAN_KEYWORDS),
        amor_fati=_score_keywords(text_lower, AMOR_FATI_KEYWORDS),
    )
    
    # Adjust based on optional inputs
    if delta12:
        profile = _adjust_for_archetypes(profile, delta12)
    
    if tw_state:
        profile = _adjust_for_tw_state(profile, tw_state)
    
    # Build result
    dominant = profile.dominant_axes(3)
    severity = profile.overall_severity()
    notes = _generate_notes(profile, dominant)
    
    return MetaEngineResult(
        scores=profile.to_dict(),
        dominant_axes=dominant,
        severity=severity,
        notes=notes
    )


def _score_keywords(text: str, keywords: List[str]) -> float:
    """Score text based on keyword presence."""
    count = sum(1 for kw in keywords if kw in text)
    # Normalize to [0, 1]
    return min(1.0, count / max(len(keywords) * 0.3, 1.0))


def _adjust_for_archetypes(profile: NietzscheProfile, delta12: Any) -> NietzscheProfile:
    """Adjust profile based on dominant archetypes."""
    if not hasattr(delta12, "dominant"):
        return profile
    
    dominant_id, _ = delta12.dominant()
    
    # WARRIOR, REBEL → boost will_to_power
    if dominant_id in ["A03_WARRIOR", "A08_REBEL"]:
        profile.will_to_power = min(1.0, profile.will_to_power + 0.1)
    
    # ORPHAN → boost resentment
    if dominant_id == "A02_ORPHAN":
        profile.resentment = min(1.0, profile.resentment + 0.15)
    
    # SAGE, MAGICIAN → boost free_spirit
    if dominant_id in ["A10_SAGE", "A09_MAGICIAN"]:
        profile.free_spirit = min(1.0, profile.free_spirit + 0.1)
    
    return profile


def _adjust_for_tw_state(profile: NietzscheProfile, tw_state: Any) -> NietzscheProfile:
    """Adjust profile based on TW369 state."""
    if not hasattr(tw_state, "metadata") or not tw_state.metadata:
        return profile
    
    drift = tw_state.metadata.get("drift_metric", 0.0)
    
    # High drift → boost dionysian
    if drift > 0.7:
        profile.dionysian_force = min(1.0, profile.dionysian_force + 0.15)
    
    # Low drift → boost apollonian
    if drift < 0.3:
        profile.apollonian_order = min(1.0, profile.apollonian_order + 0.1)
    
    return profile


def _generate_notes(profile: NietzscheProfile, dominant: List[Tuple[str, float]]) -> List[str]:
    """Generate interpretive notes."""
    notes = []
    
    # Note on dominant axes
    if dominant:
        top_axis, top_score = dominant[0]
        notes.append(f"Dominant: {top_axis.replace('_', ' ')} ({top_score:.2f})")
    
    # Contradictions
    if profile.will_to_power > 0.6 and profile.resentment > 0.5:
        notes.append("Tension: High will to power with significant resentment")
    
    if profile.life_affirmation > 0.6 and profile.life_negation > 0.5:
        notes.append("Contradiction: Strong life affirmation alongside negation")
    
    if profile.dionysian_force > 0.6 and profile.apollonian_order > 0.6:
        notes.append("Balance: High dionysian and apollonian forces")
    
    # Nihilism check
    if profile.active_nihilism > 0.5:
        notes.append("Active nihilism detected: Creative destruction mode")
    elif profile.passive_nihilism > 0.5:
        notes.append("Passive nihilism detected: Despair/resignation mode")
    
    # Amor fati
    if profile.amor_fati > 0.7:
        notes.append("Strong amor fati: Radical acceptance of fate")
    
    return notes
