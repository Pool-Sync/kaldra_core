"""
AureliusEngine-12 - 12-Dimensional Stoic Analysis.

Analyzes text through 12 Stoic axes:
1. perception_clarity - Clear, undistorted perception of reality
2. assent_to_reality - Acceptance of facts as they are
3. right_action - Focus on duty, responsibility, virtue
4. discipline_of_will - Consistency, commitment, self-control
5. emotional_regulation - Low reactivity, measured response
6. fate_acceptance - Acceptance of what cannot be controlled
7. control_dichotomy - Distinction between controllable/uncontrollable
8. premeditatio_malorum - Anticipation of difficulties
9. desire_restraint - Moderation, absence of excess
10. character_integrity - Concern with honor, values, coherence
11. self_mastery - Internal dominion, not moved by externals
12. serenity - Calm tone, absence of catastrophizing
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Tuple
import re


@dataclass
class AureliusProfile:
    """12-dimensional Stoic profile."""
    perception_clarity: float = 0.0
    assent_to_reality: float = 0.0
    right_action: float = 0.0
    discipline_of_will: float = 0.0
    emotional_regulation: float = 0.0
    fate_acceptance: float = 0.0
    control_dichotomy: float = 0.0
    premeditatio_malorum: float = 0.0
    desire_restraint: float = 0.0
    character_integrity: float = 0.0
    self_mastery: float = 0.0
    serenity: float = 0.0
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return asdict(self)
    
    def dominant_axes(self, top_k: int = 3) -> List[Tuple[str, float]]:
        """Get top K dominant axes."""
        scores = self.to_dict()
        sorted_axes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_axes[:top_k]
    
    def overall_stoic_alignment(self) -> float:
        """Calculate overall Stoic alignment [0, 1]."""
        scores = self.to_dict()
        return sum(scores.values()) / len(scores)


@dataclass
class MetaEngineResult:
    """Result from meta-engine analysis."""
    scores: Dict[str, float]
    dominant_axes: List[Tuple[str, float]]
    severity: float  # For Aurelius: stoic alignment intensity
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


# Keyword patterns for each axis
PERCEPTION_CLARITY_KEYWORDS = [
    "objectively", "factually", "precisely", "accurately", "clearly",
    "as it is", "without bias", "neutral", "observe", "examine"
]

ASSENT_TO_REALITY_KEYWORDS = [
    "this happened", "it is what it is", "accept", "acknowledge",
    "face the facts", "reality is", "the truth is", "recognize"
]

RIGHT_ACTION_KEYWORDS = [
    "duty", "responsibility", "obligation", "should", "must",
    "right thing", "virtue", "honor", "principle", "integrity"
]

DISCIPLINE_OF_WILL_KEYWORDS = [
    "consistent", "committed", "disciplined", "routine", "practice",
    "habit", "persevere", "steadfast", "resolute", "determined"
]

EMOTIONAL_REGULATION_KEYWORDS = [
    "calm", "composed", "measured", "balanced", "steady",
    "not reactive", "pause", "consider", "reflect", "rational"
]

FATE_ACCEPTANCE_KEYWORDS = [
    "accept fate", "meant to be", "destiny", "inevitable",
    "cannot change", "beyond control", "surrender to", "flow with"
]

CONTROL_DICHOTOMY_KEYWORDS = [
    "in my control", "not in my control", "up to me", "depends on me",
    "within my power", "outside my power", "can control", "cannot control"
]

PREMEDITATIO_MALORUM_KEYWORDS = [
    "if it fails", "worst case", "prepare for", "anticipate",
    "plan for difficulty", "expect obstacles", "ready for", "contingency"
]

DESIRE_RESTRAINT_KEYWORDS = [
    "moderate", "enough", "sufficient", "restrain", "limit",
    "not excessive", "measured", "temperate", "frugal", "simple"
]

CHARACTER_INTEGRITY_KEYWORDS = [
    "character", "values", "principles", "honor", "virtue",
    "moral", "ethical", "consistent with", "true to", "authentic"
]

SELF_MASTERY_KEYWORDS = [
    "self-control", "master myself", "inner strength", "discipline",
    "not swayed", "unmoved", "centered", "grounded", "sovereign"
]

SERENITY_KEYWORDS = [
    "peaceful", "tranquil", "serene", "calm", "quiet",
    "still", "equanimity", "untroubled", "at peace", "content"
]

# Anti-patterns (reduce scores)
EMOTIONAL_REACTIVITY_KEYWORDS = [
    "outraged", "furious", "devastated", "terrified", "panicked",
    "catastrophe", "disaster", "horrible", "terrible", "awful"
]

EXCESS_KEYWORDS = [
    "more and more", "never enough", "insatiable", "greedy",
    "excessive", "extreme", "unlimited", "boundless"
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
    Analyze text through 12 Stoic axes.
    
    Args:
        text: Input text to analyze
        delta12: Optional Delta12Vector for archetype context
        delta144_state: Optional current Δ144 state
        tw_state: Optional TWState for drift context
        bias_score: Optional bias score
        
    Returns:
        MetaEngineResult with 12-dimensional Stoic analysis
    """
    text_lower = text.lower()
    
    # Calculate each axis
    profile = AureliusProfile(
        perception_clarity=_score_keywords(text_lower, PERCEPTION_CLARITY_KEYWORDS),
        assent_to_reality=_score_keywords(text_lower, ASSENT_TO_REALITY_KEYWORDS),
        right_action=_score_keywords(text_lower, RIGHT_ACTION_KEYWORDS),
        discipline_of_will=_score_keywords(text_lower, DISCIPLINE_OF_WILL_KEYWORDS),
        emotional_regulation=_score_keywords(text_lower, EMOTIONAL_REGULATION_KEYWORDS),
        fate_acceptance=_score_keywords(text_lower, FATE_ACCEPTANCE_KEYWORDS),
        control_dichotomy=_score_keywords(text_lower, CONTROL_DICHOTOMY_KEYWORDS),
        premeditatio_malorum=_score_keywords(text_lower, PREMEDITATIO_MALORUM_KEYWORDS),
        desire_restraint=_score_keywords(text_lower, DESIRE_RESTRAINT_KEYWORDS),
        character_integrity=_score_keywords(text_lower, CHARACTER_INTEGRITY_KEYWORDS),
        self_mastery=_score_keywords(text_lower, SELF_MASTERY_KEYWORDS),
        serenity=_score_keywords(text_lower, SERENITY_KEYWORDS),
    )
    
    # Apply penalties for anti-patterns
    reactivity_penalty = _score_keywords(text_lower, EMOTIONAL_REACTIVITY_KEYWORDS)
    profile.emotional_regulation = max(0.0, profile.emotional_regulation - reactivity_penalty)
    profile.serenity = max(0.0, profile.serenity - reactivity_penalty * 0.5)
    
    excess_penalty = _score_keywords(text_lower, EXCESS_KEYWORDS)
    profile.desire_restraint = max(0.0, profile.desire_restraint - excess_penalty)
    
    # Adjust based on optional inputs
    if delta12:
        profile = _adjust_for_archetypes(profile, delta12)
    
    if tw_state:
        profile = _adjust_for_tw_state(profile, tw_state)
    
    if bias_score is not None:
        profile = _adjust_for_bias(profile, bias_score)
    
    # Build result
    dominant = profile.dominant_axes(3)
    alignment = profile.overall_stoic_alignment()
    notes = _generate_notes(profile, dominant, alignment)
    
    return MetaEngineResult(
        scores=profile.to_dict(),
        dominant_axes=dominant,
        severity=alignment,  # For Stoics, severity = alignment strength
        notes=notes
    )


def _score_keywords(text: str, keywords: List[str]) -> float:
    """Score text based on keyword presence."""
    count = sum(1 for kw in keywords if kw in text)
    # Normalize to [0, 1]
    return min(1.0, count / max(len(keywords) * 0.3, 1.0))


def _adjust_for_archetypes(profile: AureliusProfile, delta12: Any) -> AureliusProfile:
    """Adjust profile based on dominant archetypes."""
    if not hasattr(delta12, "dominant"):
        return profile
    
    dominant_id, _ = delta12.dominant()
    
    # RULER, SAGE → boost discipline, integrity
    if dominant_id in ["A07_RULER", "A10_SAGE"]:
        profile.discipline_of_will = min(1.0, profile.discipline_of_will + 0.1)
        profile.character_integrity = min(1.0, profile.character_integrity + 0.1)
    
    # CAREGIVER → boost right_action
    if dominant_id == "A04_CAREGIVER":
        profile.right_action = min(1.0, profile.right_action + 0.1)
    
    # ORPHAN, REBEL → reduce serenity, emotional_regulation
    if dominant_id in ["A02_ORPHAN", "A08_REBEL"]:
        profile.serenity = max(0.0, profile.serenity - 0.1)
        profile.emotional_regulation = max(0.0, profile.emotional_regulation - 0.1)
    
    return profile


def _adjust_for_tw_state(profile: AureliusProfile, tw_state: Any) -> AureliusProfile:
    """Adjust profile based on TW369 state."""
    if not hasattr(tw_state, "metadata") or not tw_state.metadata:
        return profile
    
    drift = tw_state.metadata.get("drift_metric", 0.0)
    
    # High drift → reduce serenity, emotional_regulation
    if drift > 0.7:
        profile.serenity = max(0.0, profile.serenity - 0.15)
        profile.emotional_regulation = max(0.0, profile.emotional_regulation - 0.1)
    
    # Low drift → boost serenity
    if drift < 0.3:
        profile.serenity = min(1.0, profile.serenity + 0.1)
    
    return profile


def _adjust_for_bias(profile: AureliusProfile, bias_score: float) -> AureliusProfile:
    """Adjust profile based on bias score."""
    # High bias → reduce perception_clarity, emotional_regulation
    if bias_score > 0.6:
        profile.perception_clarity = max(0.0, profile.perception_clarity - 0.2)
        profile.emotional_regulation = max(0.0, profile.emotional_regulation - 0.15)
    
    # Low bias → boost perception_clarity
    if bias_score < 0.3:
        profile.perception_clarity = min(1.0, profile.perception_clarity + 0.1)
    
    return profile


def _generate_notes(
    profile: AureliusProfile,
    dominant: List[Tuple[str, float]],
    alignment: float
) -> List[str]:
    """Generate interpretive notes."""
    notes = []
    
    # Note on dominant axes
    if dominant:
        top_axis, top_score = dominant[0]
        notes.append(f"Dominant: {top_axis.replace('_', ' ')} ({top_score:.2f})")
    
    # Overall alignment
    if alignment > 0.7:
        notes.append("High Stoic alignment: Strong discipline and regulation")
    elif alignment < 0.3:
        notes.append("Low Stoic alignment: Reactive or unregulated state")
    
    # Specific patterns
    if profile.perception_clarity > 0.7 and profile.emotional_regulation < 0.4:
        notes.append("Tension: High clarity but low emotional regulation")
    
    if profile.control_dichotomy > 0.6:
        notes.append("Strong control dichotomy awareness")
    
    if profile.premeditatio_malorum > 0.6:
        notes.append("Active negative visualization practice detected")
    
    if profile.serenity > 0.7 and profile.self_mastery > 0.7:
        notes.append("Exemplary Stoic state: High serenity and self-mastery")
    
    if profile.fate_acceptance > 0.7:
        notes.append("Strong fate acceptance: Amor fati alignment")
    
    return notes
