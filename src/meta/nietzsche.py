"""
NietzscheEngine v3.1 - Nietzschean Analysis with Kindra 3×48 and TW369 Integration.

Analyzes text through 12 Nietzschean axes with semantic intelligence from Kindra
and temporal awareness from TW369.

12 Axes:
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

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Tuple
import re

# Import v3.1 state definitions
from src.unification.states.unified_state import KindraContext
from src.tw369.tw369_integration import TWState
from src.common.unified_signal import MetaSignal


# ============================================================================
# v3.1 Data Structures
# ============================================================================

@dataclass
class MetaInput:
    """
    Standard input for meta-engine analysis (v3.1).
    
    Attributes:
        text: Input text to analyze
        delta144_state: Optional current Δ144 state identifier
        archetype_scores: Optional archetype distribution scores
        kindra: Optional KindraContext with 3×48 vectors
        tw_state: Optional TWState for drift/regime awareness
        bias_score: Optional bias detection score
        polarity_scores: Optional polarity scores
        modifiers: Optional adjustment modifiers
    """
    text: str
    delta144_state: Optional[str] = None
    archetype_scores: Dict[str, float] = field(default_factory=dict)
    kindra: Optional[KindraContext] = None
    tw_state: Optional[TWState] = None
    bias_score: Optional[float] = None
    polarity_scores: Optional[Dict[str, float]] = None
    modifiers: Optional[Dict[str, float]] = None


@dataclass
class NietzscheSignal(MetaSignal):
    """
    Output signal from NietzscheEngine analysis (v3.1).
    
    Extends MetaSignal with Nietzschean-specific fields.
    
    Attributes:
        will_to_power: Drive for power/dominance [0, 1]
        morality_type: Classification as "master" | "slave" | "mixed"
        eternal_return: Cyclical pattern strength [0, 1]
        transcendence: Übermensch/transcendence markers [0, 1]
        scores: All 12 dimensional axis scores
        dominant_axes: Top 3 dominant axes with scores
        severity: Overall intensity/severity [0, 1]
        notes: Interpretive notes in English
    """
    will_to_power: float = 0.0
    morality_type: str = "mixed"
    eternal_return: float = 0.0
    transcendence: float = 0.0
    scores: Dict[str, float] = field(default_factory=dict)
    dominant_axes: List[Tuple[str, float]] = field(default_factory=list)
    severity: float = 0.0
    notes: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate ranges."""
        super().__post_init__()
        self.will_to_power = max(0.0, min(1.0, self.will_to_power))
        self.eternal_return = max(0.0, min(1.0, self.eternal_return))
        self.transcendence = max(0.0, min(1.0, self.transcendence))
        self.severity = max(0.0, min(1.0, self.severity))


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


# ============================================================================
# Keyword Patterns (Heuristic Foundation)
# ============================================================================

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


# ============================================================================
# NietzscheEngine v3.1
# ============================================================================

class NietzscheEngine:
    """
    Nietzschean analysis engine with Kindra 3×48 and TW369 integration.
    
    Analyzes text through 12 Nietzschean philosophical axes, enhanced by:
    - Kindra 3×48: Semantic intelligence from 144 cultural/semiotic vectors
    - TW369: Temporal drift and regime awareness
    """
    
    name = "nietzsche"
    
    def analyze(self, meta_input: MetaInput) -> NietzscheSignal:
        """
        Analyze text through Nietzschean lens.
        
        Args:
            meta_input: MetaInput with text and optional context
            
        Returns:
            NietzscheSignal with 12-dimensional analysis
        """
        text_lower = meta_input.text.lower()
        
        # Step 1: Calculate base profile from keywords
        profile = self._calculate_base_profile(text_lower)
        
        # Step 2: Adjust based on Kindra 3×48 (if available)
        if meta_input.kindra:
            kindra_sig = self._compute_kindra_signature(meta_input.kindra)
            profile = self._integrate_kindra(profile, kindra_sig)
        else:
            kindra_sig = {}
        
        # Step 3: Adjust based on TW369 (if available)
        if meta_input.tw_state:
            profile = self._apply_tw369_adjustments(profile, meta_input.tw_state)
        
        # Step 4: Adjust based on archetype scores (if available)
        if meta_input.archetype_scores:
            profile = self._adjust_for_archetypes(profile, meta_input.archetype_scores)
        
        # Step 5: Classify morality type
        morality_type = self._classify_morality_type(
            profile.will_to_power,
            profile.resentment,
            kindra_sig
        )
        
        # Step 6: Calculate transcendence
        transcendence = self._calculate_transcendence(profile, kindra_sig)
        
        # Step 7: Build result
        dominant = profile.dominant_axes(3)
        severity = profile.overall_severity()
        notes = self._generate_notes(profile, dominant, morality_type)
        
        return NietzscheSignal(
            name=self.name,
            score=severity,
            label=morality_type,
            details={
                "kindra_signature": kindra_sig,
                "tw369_applied": meta_input.tw_state is not None
            },
            will_to_power=profile.will_to_power,
            morality_type=morality_type,
            eternal_return=profile.eternal_return_acceptance,
            transcendence=transcendence,
            scores=profile.to_dict(),
            dominant_axes=dominant,
            severity=severity,
            notes=notes
        )
    
    def _calculate_base_profile(self, text_lower: str) -> NietzscheProfile:
        """Calculate base profile from keyword matching."""
        return NietzscheProfile(
            will_to_power=self._score_keywords(text_lower, WILL_TO_POWER_KEYWORDS),
            resentment=self._score_keywords(text_lower, RESENTMENT_KEYWORDS),
            life_affirmation=self._score_keywords(text_lower, LIFE_AFFIRMATION_KEYWORDS),
            life_negation=self._score_keywords(text_lower, LIFE_NEGATION_KEYWORDS),
            free_spirit=self._score_keywords(text_lower, FREE_SPIRIT_KEYWORDS),
            active_nihilism=self._score_keywords(text_lower, ACTIVE_NIHILISM_KEYWORDS),
            passive_nihilism=self._score_keywords(text_lower, PASSIVE_NIHILISM_KEYWORDS),
            eternal_return_acceptance=self._score_keywords(text_lower, ETERNAL_RETURN_KEYWORDS),
            transvaluation=self._score_keywords(text_lower, TRANSVALUATION_KEYWORDS),
            dionysian_force=self._score_keywords(text_lower, DIONYSIAN_KEYWORDS),
            apollonian_order=self._score_keywords(text_lower, APOLLONIAN_KEYWORDS),
            amor_fati=self._score_keywords(text_lower, AMOR_FATI_KEYWORDS),
        )
    
    def _compute_kindra_signature(self, kindra: KindraContext) -> Dict[str, float]:
        """
        Compute Nietzschean signature from Kindra 3×48 vectors.
        
        Extracts 4 key metrics:
        - power_climate: Cultural power dynamics (Layer 1)
        - ressentiment_index: Victim/blame patterns (Layers 1+2)
        - mythic_intensity: Archetypal resonance (Layer 3)
        - conflict_tension: Dialectical forces (Layer 2)
        
        Args:
            kindra: KindraContext with 3 layers of scores
            
        Returns:
            Dict with Nietzschean signature metrics
        """
        # Layer 1: Cultural/Macro - extract power dynamics
        power_vectors = ["power_dynamics", "dominance", "hierarchy", "authority", "control"]
        victim_vectors = ["victimhood", "grievance", "resentment", "blame", "unfairness"]
        
        power_climate = self._extract_vector_score(kindra.layer1, power_vectors)
        ressentiment_l1 = self._extract_vector_score(kindra.layer1, victim_vectors)
        
        # Layer 2: Semiotic/Media - extract conflict and narrative patterns
        conflict_vectors = ["conflict", "tension", "opposition", "struggle", "dialectic"]
        victim_narrative_vectors = ["victim_narrative", "injustice_framing", "blame_attribution"]
        
        conflict_tension = self._extract_vector_score(kindra.layer2, conflict_vectors)
        ressentiment_l2 = self._extract_vector_score(kindra.layer2, victim_narrative_vectors)
        
        # Layer 3: Structural/Systemic - extract archetypal depth
        mythic_vectors = ["archetypal_hero", "mythic_pattern", "universal_theme", "transcendence"]
        
        mythic_intensity = self._extract_vector_score(kindra.layer3, mythic_vectors)
        
        # Combine ressentiment from layers 1 and 2
        ressentiment_index = (ressentiment_l1 + ressentiment_l2) / 2.0
        
        return {
            "power_climate": power_climate,
            "ressentiment_index": ressentiment_index,
            "mythic_intensity": mythic_intensity,
            "conflict_tension": conflict_tension
        }
    
    def _extract_vector_score(self, layer_scores: Dict[str, float], vector_names: List[str]) -> float:
        """
        Extract average score for matching vectors in a layer.
        
        Uses fuzzy matching - if vector_name is substring of any key, include it.
        """
        matching_scores = []
        for vec_name in vector_names:
            for key, score in layer_scores.items():
                if vec_name.lower() in key.lower():
                    matching_scores.append(score)
        
        if not matching_scores:
            return 0.0
        
        return sum(matching_scores) / len(matching_scores)
    
    def _integrate_kindra(self, profile: NietzscheProfile, kindra_sig: Dict[str, float]) -> NietzscheProfile:
        """
        Integrate Kindra signature into Nietzschean profile.
        
        Adjusts base scores using Kindra-derived metrics.
        """
        # Power climate boosts will_to_power
        power_boost = kindra_sig.get("power_climate", 0.0) * 0.3
        profile.will_to_power = min(1.0, profile.will_to_power + power_boost)
        
        # Ressentiment index boosts resentment
        ressentiment_boost = kindra_sig.get("ressentiment_index", 0.0) * 0.4
        profile.resentment = min(1.0, profile.resentment + ressentiment_boost)
        
        # Mythic intensity boosts transcendence-related axes
        mythic_boost = kindra_sig.get("mythic_intensity", 0.0) * 0.2
        profile.eternal_return_acceptance = min(1.0, profile.eternal_return_acceptance + mythic_boost)
        profile.amor_fati = min(1.0, profile.amor_fati + mythic_boost)
        
        # Conflict tension boosts dionysian (chaos) over apollonian (order)
        conflict = kindra_sig.get("conflict_tension", 0.0)
        if conflict > 0.5:
            profile.dionysian_force = min(1.0, profile.dionysian_force + conflict * 0.2)
        else:
            profile.apollonian_order = min(1.0, profile.apollonian_order + (1.0 - conflict) * 0.15)
        
        return profile
    
    def _apply_tw369_adjustments(self, profile: NietzscheProfile, tw_state: TWState) -> NietzscheProfile:
        """
        Apply TW369 drift and regime adjustments.
        
        Rules:
        - High drift + critical regime → boost will_to_power, eternal_return
        - Low drift + stable regime → favor apollonian over dionysian
        - Transition regime → boost transvaluation
        """
        # Extract drift and regime
        drift = 0.0
        regime = "UNKNOWN"
        
        if tw_state.metadata:
            drift = tw_state.metadata.get("drift_metric", 0.0)
            regime = tw_state.metadata.get("regime", "UNKNOWN")
        
        # High drift scenarios
        if drift > 0.7:
            profile.will_to_power = min(1.0, profile.will_to_power + 0.15)
            profile.eternal_return_acceptance = min(1.0, profile.eternal_return_acceptance + 0.1)
            profile.dionysian_force = min(1.0, profile.dionysian_force + 0.15)
        
        # Low drift scenarios
        elif drift < 0.3:
            profile.apollonian_order = min(1.0, profile.apollonian_order + 0.1)
            profile.amor_fati = min(1.0, profile.amor_fati + 0.1)
        
        # Critical regime
        if regime == "CRITICAL":
            profile.active_nihilism = min(1.0, profile.active_nihilism + 0.2)
            profile.transvaluation = min(1.0, profile.transvaluation + 0.15)
        
        # Stable regime
        elif regime == "STABLE":
            profile.life_affirmation = min(1.0, profile.life_affirmation + 0.1)
        
        # Transition regime
        elif regime == "TRANSITION":
            profile.transvaluation = min(1.0, profile.transvaluation + 0.2)
        
        return profile
    
    def _adjust_for_archetypes(self, profile: NietzscheProfile, archetype_scores: Dict[str, float]) -> NietzscheProfile:
        """
        Adjust profile based on dominant archetypes.
        
        Maps archetype patterns to Nietzschean axes.
        """
        # Find dominant archetype
        if not archetype_scores:
            return profile
        
        dominant_arch = max(archetype_scores.items(), key=lambda x: x[1])[0]
        
        # WARRIOR, REBEL → boost will_to_power
        if "WARRIOR" in dominant_arch or "REBEL" in dominant_arch:
            profile.will_to_power = min(1.0, profile.will_to_power + 0.1)
        
        # ORPHAN → boost resentment
        if "ORPHAN" in dominant_arch:
            profile.resentment = min(1.0, profile.resentment + 0.15)
        
        # SAGE, MAGICIAN → boost free_spirit
        if "SAGE" in dominant_arch or "MAGICIAN" in dominant_arch:
            profile.free_spirit = min(1.0, profile.free_spirit + 0.1)
        
        # CREATOR → boost active_nihilism (creative destruction)
        if "CREATOR" in dominant_arch:
            profile.active_nihilism = min(1.0, profile.active_nihilism + 0.1)
        
        return profile
    
    def _classify_morality_type(
        self,
        will_to_power: float,
        resentment: float,
        kindra_sig: Dict[str, float]
    ) -> str:
        """
        Classify morality type as master/slave/mixed.
        
        Master: High will_to_power, low resentment, positive power_climate
        Slave: Low will_to_power, high resentment, negative power_climate
        Mixed: Intermediate or contradictory signals
        """
        power_climate = kindra_sig.get("power_climate", 0.5)
        
        # Master morality indicators
        master_score = will_to_power * 0.5 + (1.0 - resentment) * 0.3 + power_climate * 0.2
        
        # Slave morality indicators
        slave_score = resentment * 0.5 + (1.0 - will_to_power) * 0.3 + (1.0 - power_climate) * 0.2
        
        # Classification thresholds
        if master_score > 0.6 and master_score > slave_score * 1.3:
            return "master"
        elif slave_score > 0.6 and slave_score > master_score * 1.3:
            return "slave"
        else:
            return "mixed"
    
    def _calculate_transcendence(self, profile: NietzscheProfile, kindra_sig: Dict[str, float]) -> float:
        """
        Calculate transcendence (Übermensch markers).
        
        Combines:
        - High will_to_power
        - High life_affirmation
        - Low resentment
        - High free_spirit
        - Mythic intensity from Kindra
        """
        base_transcendence = (
            profile.will_to_power * 0.3 +
            profile.life_affirmation * 0.2 +
            (1.0 - profile.resentment) * 0.2 +
            profile.free_spirit * 0.2 +
            profile.amor_fati * 0.1
        )
        
        # Boost from Kindra mythic intensity
        mythic_boost = kindra_sig.get("mythic_intensity", 0.0) * 0.3
        
        transcendence = min(1.0, base_transcendence + mythic_boost)
        return transcendence
    
    def _score_keywords(self, text: str, keywords: List[str]) -> float:
        """Score text based on keyword presence."""
        count = sum(1 for kw in keywords if kw in text)
        # Normalize to [0, 1]
        return min(1.0, count / max(len(keywords) * 0.3, 1.0))
    
    def _generate_notes(
        self,
        profile: NietzscheProfile,
        dominant: List[Tuple[str, float]],
        morality_type: str
    ) -> List[str]:
        """Generate interpretive notes."""
        notes = []
        
        # Note on morality type
        notes.append(f"Morality type: {morality_type}")
        
        # Note on dominant axes
        if dominant:
            top_axis, top_score = dominant[0]
            notes.append(f"Dominant axis: {top_axis.replace('_', ' ')} ({top_score:.2f})")
        
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
        
        # Transcendence potential
        if profile.will_to_power > 0.7 and profile.free_spirit > 0.6:
            notes.append("Übermensch potential: High will to power and free spirit")
        
        return notes


# ============================================================================
# Backward Compatibility (v2.9 Legacy Support)
# ============================================================================

@dataclass
class MetaEngineResult:
    """Legacy result format for backward compatibility."""
    scores: Dict[str, float]
    dominant_axes: List[Tuple[str, float]]
    severity: float
    notes: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


def analyze_meta(
    text: str,
    *,
    delta12: Optional[Any] = None,
    delta144_state: Optional[str] = None,
    tw_state: Optional[Any] = None,
    bias_score: Optional[float] = None,
) -> MetaEngineResult:
    """
    Legacy wrapper for backward compatibility with v2.9.
    
    Args:
        text: Input text to analyze
        delta12: Optional Delta12Vector for archetype context
        delta144_state: Optional current Δ144 state
        tw_state: Optional TWState for drift context
        bias_score: Optional bias score
        
    Returns:
        MetaEngineResult with 12-dimensional analysis
    """
    # Convert to v3.1 format
    archetype_scores = {}
    if delta12 and hasattr(delta12, "to_dict"):
        archetype_scores = delta12.to_dict()
    
    meta_input = MetaInput(
        text=text,
        delta144_state=delta144_state,
        archetype_scores=archetype_scores,
        tw_state=tw_state,
        bias_score=bias_score
    )
    
    # Run v3.1 engine
    engine = NietzscheEngine()
    signal = engine.analyze(meta_input)
    
    # Convert back to legacy format
    return MetaEngineResult(
        scores=signal.scores,
        dominant_axes=signal.dominant_axes,
        severity=signal.severity,
        notes=signal.notes
    )
