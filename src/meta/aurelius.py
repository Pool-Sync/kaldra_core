"""
AureliusEngine v3.1 - Stoic Analysis with Kindra 3×48 and TW369 Integration.

Analyzes text through 12 Stoic axes with semantic intelligence from Kindra
and temporal awareness from TW369, mapping to 4 Cardinal Virtues.

12 Axes:
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

4 Cardinal Virtues:
- Wisdom (Sophia)
- Courage (Andreia)
- Justice (Dikaiosyne)
- Temperance (Sophrosyne)
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Tuple

# Import v3.1 state definitions
from src.meta.nietzsche import MetaInput  # Reuse shared MetaInput
from src.unification.states.unified_state import KindraContext
from src.tw369.tw369_integration import TWState
from src.common.unified_signal import MetaSignal


# ============================================================================
# v3.1 Data Structures
# ============================================================================

@dataclass
class AureliusSignal(MetaSignal):
    """
    Output signal from AureliusEngine analysis (v3.1).
    
    Extends MetaSignal with Stoic-specific fields.
    
    Attributes:
        dichotomy_of_control: Controllable vs uncontrollable focus
        virtue_scores: 4 Cardinal Virtues (Wisdom, Courage, Justice, Temperance)
        memento_mori: Urgency/mortality awareness [0, 1]
        amor_fati: Active acceptance of fate [0, 1]
        scores: All 12 dimensional axis scores
        dominant_axes: Top 3 dominant axes with scores
        severity: Stoic alignment strength [0, 1]
        notes: Interpretive notes in English
    """
    dichotomy_of_control: Dict[str, float] = field(default_factory=dict)
    virtue_scores: Dict[str, float] = field(default_factory=dict)
    memento_mori: float = 0.0
    amor_fati: float = 0.0
    scores: Dict[str, float] = field(default_factory=dict)
    dominant_axes: List[Tuple[str, float]] = field(default_factory=list)
    severity: float = 0.0
    notes: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate ranges."""
        super().__post_init__()
        self.memento_mori = max(0.0, min(1.0, self.memento_mori))
        self.amor_fati = max(0.0, min(1.0, self.amor_fati))
        self.severity = max(0.0, min(1.0, self.severity))


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


# ============================================================================
# Keyword Patterns (Heuristic Foundation)
# ============================================================================

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


# ============================================================================
# AureliusEngine v3.1
# ============================================================================

class AureliusEngine:
    """
    Stoic analysis engine with Kindra 3×48 and TW369 integration.
    
    Analyzes text through 12 Stoic philosophical axes, enhanced by:
    - Kindra 3×48: Semantic intelligence from 144 cultural/semiotic vectors
    - TW369: Temporal drift and regime awareness
    - 4 Cardinal Virtues: Wisdom, Courage, Justice, Temperance
    """
    
    name = "aurelius"
    
    def analyze(self, meta_input: MetaInput) -> AureliusSignal:
        """
        Analyze text through Stoic lens.
        
        Args:
            meta_input: MetaInput with text and optional context
            
        Returns:
            AureliusSignal with 12-dimensional analysis + 4 virtues
        """
        text_lower = meta_input.text.lower()
        
        # Step 1: Calculate base profile from keywords
        profile = self._calculate_base_profile(text_lower)
        
        # Step 2: Compute Kindra signature (if available)
        kindra_sig = {}
        if meta_input.kindra:
            kindra_sig = self._compute_kindra_signature(meta_input.kindra)
        
        # Step 3: Adjust based on archetype scores (if available)
        if meta_input.archetype_scores:
            profile = self._adjust_for_archetypes(profile, meta_input.archetype_scores)
        
        # Step 4: Adjust based on bias score (if available)
        if meta_input.bias_score is not None:
            profile = self._adjust_for_bias(profile, meta_input.bias_score)
        
        # Step 5: Calculate 4 Cardinal Virtues
        virtue_scores = self._calculate_virtue_scores(profile, kindra_sig)
        
        # Step 6: Calculate dichotomy of control
        dichotomy = self._calculate_dichotomy_of_control(profile, kindra_sig)
        
        # Step 7: Calculate memento_mori and amor_fati
        memento_mori = self._calculate_memento_mori(profile, kindra_sig)
        amor_fati = self._calculate_amor_fati(profile, kindra_sig)
        
        # Step 8: Apply TW369 adjustments (if available)
        if meta_input.tw_state:
            virtue_scores, memento_mori, amor_fati = self._apply_tw369_adjustments(
                virtue_scores, memento_mori, amor_fati, meta_input.tw_state
            )
        
        # Step 9: Build result
        dominant = profile.dominant_axes(3)
        alignment = profile.overall_stoic_alignment()
        
        # Combine all scores for MetaSignal.scores
        all_scores = profile.to_dict()
        all_scores.update({
            "wisdom": virtue_scores["wisdom"],
            "courage": virtue_scores["courage"],
            "justice": virtue_scores["justice"],
            "temperance": virtue_scores["temperance"],
            "memento_mori": memento_mori,
            "amor_fati": amor_fati,
        })
        
        notes = self._generate_notes(profile, dominant, alignment, virtue_scores, dichotomy)
        
        return AureliusSignal(
            name=self.name,
            score=alignment,
            label=self._classify_stoic_posture(alignment, virtue_scores),
            details={
                "kindra_signature": kindra_sig,
                "tw369_applied": meta_input.tw_state is not None
            },
            dichotomy_of_control=dichotomy,
            virtue_scores=virtue_scores,
            memento_mori=memento_mori,
            amor_fati=amor_fati,
            scores=all_scores,
            dominant_axes=dominant,
            severity=alignment,
            notes=notes
        )
    
    def _calculate_base_profile(self, text_lower: str) -> AureliusProfile:
        """Calculate base profile from keyword matching."""
        profile = AureliusProfile(
            perception_clarity=self._score_keywords(text_lower, PERCEPTION_CLARITY_KEYWORDS),
            assent_to_reality=self._score_keywords(text_lower, ASSENT_TO_REALITY_KEYWORDS),
            right_action=self._score_keywords(text_lower, RIGHT_ACTION_KEYWORDS),
            discipline_of_will=self._score_keywords(text_lower, DISCIPLINE_OF_WILL_KEYWORDS),
            emotional_regulation=self._score_keywords(text_lower, EMOTIONAL_REGULATION_KEYWORDS),
            fate_acceptance=self._score_keywords(text_lower, FATE_ACCEPTANCE_KEYWORDS),
            control_dichotomy=self._score_keywords(text_lower, CONTROL_DICHOTOMY_KEYWORDS),
            premeditatio_malorum=self._score_keywords(text_lower, PREMEDITATIO_MALORUM_KEYWORDS),
            desire_restraint=self._score_keywords(text_lower, DESIRE_RESTRAINT_KEYWORDS),
            character_integrity=self._score_keywords(text_lower, CHARACTER_INTEGRITY_KEYWORDS),
            self_mastery=self._score_keywords(text_lower, SELF_MASTERY_KEYWORDS),
            serenity=self._score_keywords(text_lower, SERENITY_KEYWORDS),
        )
        
        # Apply penalties for anti-patterns
        reactivity_penalty = self._score_keywords(text_lower, EMOTIONAL_REACTIVITY_KEYWORDS)
        profile.emotional_regulation = max(0.0, profile.emotional_regulation - reactivity_penalty)
        profile.serenity = max(0.0, profile.serenity - reactivity_penalty * 0.5)
        
        excess_penalty = self._score_keywords(text_lower, EXCESS_KEYWORDS)
        profile.desire_restraint = max(0.0, profile.desire_restraint - excess_penalty)
        
        return profile
    
    def _compute_kindra_signature(self, kindra: KindraContext) -> Dict[str, float]:
        """
        Compute Stoic signature from Kindra 3×48 vectors.
        
        Extracts 4 key metrics:
        - control_focus: Focus on controllable vs external factors (Layers 1+2)
        - emotional_volatility: Emotional intensity vs serenity (Layer 2)
        - collective_responsibility: Duty/action focus (Layer 1)
        - existential_depth: Symbolic/existential density (Layer 3)
        
        Args:
            kindra: KindraContext with 3 layers of scores
            
        Returns:
            Dict with Stoic signature metrics
        """
        # Layer 1: Cultural/Macro - extract control and responsibility
        control_vectors = ["control", "agency", "autonomy", "self_determination"]
        external_vectors = ["external_forces", "fate", "destiny", "circumstances"]
        responsibility_vectors = ["duty", "responsibility", "obligation", "collective_action"]
        
        control_score = self._extract_vector_score(kindra.layer1, control_vectors)
        external_score = self._extract_vector_score(kindra.layer1, external_vectors)
        collective_responsibility = self._extract_vector_score(kindra.layer1, responsibility_vectors)
        
        # control_focus: positive if focused on controllable, negative if on external
        control_focus = control_score - external_score
        
        # Layer 2: Semiotic/Media - extract emotional patterns
        volatility_vectors = ["emotional_intensity", "reactivity", "passion", "urgency"]
        serenity_vectors = ["calm", "measured", "balanced", "equanimity"]
        
        volatility_score = self._extract_vector_score(kindra.layer2, volatility_vectors)
        serenity_score = self._extract_vector_score(kindra.layer2, serenity_vectors)
        
        emotional_volatility = volatility_score - serenity_score
        
        # Layer 3: Structural/Systemic - extract existential depth
        existential_vectors = ["mortality", "meaning", "purpose", "transcendence", "existential"]
        
        existential_depth = self._extract_vector_score(kindra.layer3, existential_vectors)
        
        return {
            "control_focus": control_focus,
            "emotional_volatility": emotional_volatility,
            "collective_responsibility": collective_responsibility,
            "existential_depth": existential_depth
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
    
    def _calculate_virtue_scores(
        self,
        profile: AureliusProfile,
        kindra_sig: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calculate 4 Cardinal Virtues from 12 axes + Kindra.
        
        Wisdom (Sophia): perception_clarity + assent_to_reality + control_dichotomy
        Courage (Andreia): right_action + discipline_of_will + premeditatio_malorum
        Justice (Dikaiosyne): right_action + character_integrity + collective_responsibility
        Temperance (Sophrosyne): desire_restraint + emotional_regulation + serenity
        """
        # Wisdom: Clear perception and understanding of reality
        wisdom = (
            profile.perception_clarity * 0.4 +
            profile.assent_to_reality * 0.3 +
            profile.control_dichotomy * 0.3
        )
        
        # Courage: Action in face of difficulty
        courage = (
            profile.right_action * 0.4 +
            profile.discipline_of_will * 0.3 +
            profile.premeditatio_malorum * 0.3
        )
        
        # Justice: Right action toward others
        justice = (
            profile.right_action * 0.4 +
            profile.character_integrity * 0.3
        )
        # Boost from Kindra collective_responsibility
        if kindra_sig:
            collective_resp = kindra_sig.get("collective_responsibility", 0.0)
            justice += collective_resp * 0.3
        else:
            justice += 0.0  # No boost without Kindra
        
        justice = min(1.0, justice)
        
        # Temperance: Self-control and moderation
        temperance = (
            profile.desire_restraint * 0.4 +
            profile.emotional_regulation * 0.3 +
            profile.serenity * 0.3
        )
        
        # Adjust for Kindra emotional_volatility (reduces temperance)
        if kindra_sig:
            volatility = kindra_sig.get("emotional_volatility", 0.0)
            if volatility > 0:
                temperance = max(0.0, temperance - volatility * 0.2)
        
        return {
            "wisdom": min(1.0, wisdom),
            "courage": min(1.0, courage),
            "justice": min(1.0, justice),
            "temperance": min(1.0, temperance)
        }
    
    def _calculate_dichotomy_of_control(
        self,
        profile: AureliusProfile,
        kindra_sig: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Calculate dichotomy of control: controllable vs uncontrollable focus.
        """
        # Base from control_dichotomy axis
        base_dichotomy = profile.control_dichotomy
        
        # Adjust from Kindra control_focus
        control_focus = kindra_sig.get("control_focus", 0.0) if kindra_sig else 0.0
        
        # Positive control_focus → more controllable
        # Negative control_focus → more uncontrollable
        controllable = min(1.0, max(0.0, base_dichotomy + control_focus * 0.3))
        uncontrollable = min(1.0, max(0.0, base_dichotomy - control_focus * 0.3))
        
        # Normalize so they make sense together
        total = controllable + uncontrollable
        if total > 0:
            controllable = controllable / total
            uncontrollable = uncontrollable / total
        
        return {
            "controllable": controllable,
            "not_controllable": uncontrollable
        }
    
    def _calculate_memento_mori(
        self,
        profile: AureliusProfile,
        kindra_sig: Dict[str, float]
    ) -> float:
        """
        Calculate memento_mori (urgency/mortality awareness).
        
        Based on:
        - premeditatio_malorum (anticipation of difficulties)
        - existential_depth from Kindra
        """
        base_memento = profile.premeditatio_malorum * 0.6
        
        # Boost from Kindra existential depth
        if kindra_sig:
            existential = kindra_sig.get("existential_depth", 0.0)
            base_memento += existential * 0.4
        
        return min(1.0, base_memento)
    
    def _calculate_amor_fati(
        self,
        profile: AureliusProfile,
        kindra_sig: Dict[str, float]
    ) -> float:
        """
        Calculate amor_fati (active acceptance of fate).
        
        Based on:
        - fate_acceptance
        - assent_to_reality
        - serenity
        """
        amor_fati = (
            profile.fate_acceptance * 0.5 +
            profile.assent_to_reality * 0.3 +
            profile.serenity * 0.2
        )
        
        return min(1.0, amor_fati)
    
    def _apply_tw369_adjustments(
        self,
        virtue_scores: Dict[str, float],
        memento_mori: float,
        amor_fati: float,
        tw_state: TWState
    ) -> Tuple[Dict[str, float], float, float]:
        """
        Apply TW369 drift and regime adjustments.
        
        Rules:
        - High drift + CRITICAL regime → increase memento_mori (urgency)
        - High drift → require more courage/temperance
        - STABLE regime → balanced virtues
        - TRANSITION regime → increase amor_fati (acceptance of change)
        """
        # Extract drift and regime
        drift = 0.0
        regime = "UNKNOWN"
        
        if tw_state.metadata:
            drift = tw_state.metadata.get("drift_metric", 0.0)
            regime = tw_state.metadata.get("regime", "UNKNOWN")
        
        # High drift scenarios
        if drift > 0.7:
            # Increase memento_mori (urgency in crisis)
            memento_mori = min(1.0, memento_mori + 0.2)
            
            # Require more courage and temperance
            virtue_scores["courage"] = min(1.0, virtue_scores["courage"] + 0.1)
            virtue_scores["temperance"] = min(1.0, virtue_scores["temperance"] + 0.1)
        
        # CRITICAL regime
        if regime == "CRITICAL":
            memento_mori = min(1.0, memento_mori + 0.15)
            virtue_scores["courage"] = min(1.0, virtue_scores["courage"] + 0.15)
        
        # TRANSITION regime
        elif regime == "TRANSITION":
            amor_fati = min(1.0, amor_fati + 0.2)
        
        # STABLE regime
        elif regime == "STABLE":
            # Slight boost to all virtues (balanced state)
            for virtue in virtue_scores:
                virtue_scores[virtue] = min(1.0, virtue_scores[virtue] + 0.05)
        
        return virtue_scores, memento_mori, amor_fati
    
    def _adjust_for_archetypes(
        self,
        profile: AureliusProfile,
        archetype_scores: Dict[str, float]
    ) -> AureliusProfile:
        """
        Adjust profile based on dominant archetypes.
        """
        if not archetype_scores:
            return profile
        
        dominant_arch = max(archetype_scores.items(), key=lambda x: x[1])[0]
        
        # RULER, SAGE → boost discipline, integrity
        if "RULER" in dominant_arch or "SAGE" in dominant_arch:
            profile.discipline_of_will = min(1.0, profile.discipline_of_will + 0.1)
            profile.character_integrity = min(1.0, profile.character_integrity + 0.1)
        
        # CAREGIVER → boost right_action
        if "CAREGIVER" in dominant_arch:
            profile.right_action = min(1.0, profile.right_action + 0.1)
        
        # ORPHAN, REBEL → reduce serenity, emotional_regulation
        if "ORPHAN" in dominant_arch or "REBEL" in dominant_arch:
            profile.serenity = max(0.0, profile.serenity - 0.1)
            profile.emotional_regulation = max(0.0, profile.emotional_regulation - 0.1)
        
        return profile
    
    def _adjust_for_bias(self, profile: AureliusProfile, bias_score: float) -> AureliusProfile:
        """Adjust profile based on bias score."""
        # High bias → reduce perception_clarity, emotional_regulation
        if bias_score > 0.6:
            profile.perception_clarity = max(0.0, profile.perception_clarity - 0.2)
            profile.emotional_regulation = max(0.0, profile.emotional_regulation - 0.15)
        
        # Low bias → boost perception_clarity
        if bias_score < 0.3:
            profile.perception_clarity = min(1.0, profile.perception_clarity + 0.1)
        
        return profile
    
    def _classify_stoic_posture(self, alignment: float, virtue_scores: Dict[str, float]) -> str:
        """
        Classify overall Stoic posture.
        
        Returns: "exemplary_stoic" | "stoic" | "mixed" | "non_stoic"
        """
        avg_virtue = sum(virtue_scores.values()) / len(virtue_scores)
        
        if alignment > 0.7 and avg_virtue > 0.7:
            return "exemplary_stoic"
        elif alignment > 0.5 and avg_virtue > 0.5:
            return "stoic"
        elif alignment > 0.3:
            return "mixed"
        else:
            return "non_stoic"
    
    def _score_keywords(self, text: str, keywords: List[str]) -> float:
        """Score text based on keyword presence."""
        count = sum(1 for kw in keywords if kw in text)
        # Normalize to [0, 1]
        return min(1.0, count / max(len(keywords) * 0.3, 1.0))
    
    def _generate_notes(
        self,
        profile: AureliusProfile,
        dominant: List[Tuple[str, float]],
        alignment: float,
        virtue_scores: Dict[str, float],
        dichotomy: Dict[str, float]
    ) -> List[str]:
        """Generate interpretive notes."""
        notes = []
        
        # Note on Stoic posture
        posture = self._classify_stoic_posture(alignment, virtue_scores)
        notes.append(f"Stoic posture: {posture.replace('_', ' ')}")
        
        # Note on dominant axes
        if dominant:
            top_axis, top_score = dominant[0]
            notes.append(f"Dominant axis: {top_axis.replace('_', ' ')} ({top_score:.2f})")
        
        # Overall alignment
        if alignment > 0.7:
            notes.append("High Stoic alignment: Strong discipline and regulation")
        elif alignment < 0.3:
            notes.append("Low Stoic alignment: Reactive or unregulated state")
        
        # Virtue analysis
        top_virtue = max(virtue_scores.items(), key=lambda x: x[1])
        notes.append(f"Strongest virtue: {top_virtue[0]} ({top_virtue[1]:.2f})")
        
        # Control dichotomy
        if dichotomy["controllable"] > 0.6:
            notes.append("Strong focus on controllable factors")
        elif dichotomy["not_controllable"] > 0.6:
            notes.append("High focus on uncontrollable external factors")
        
        # Specific patterns
        if profile.perception_clarity > 0.7 and profile.emotional_regulation < 0.4:
            notes.append("Tension: High clarity but low emotional regulation")
        
        if profile.premeditatio_malorum > 0.6:
            notes.append("Active negative visualization practice detected")
        
        if profile.serenity > 0.7 and profile.self_mastery > 0.7:
            notes.append("Exemplary Stoic state: High serenity and self-mastery")
        
        if profile.fate_acceptance > 0.7:
            notes.append("Strong fate acceptance: Amor fati alignment")
        
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
        MetaEngineResult with 12-dimensional Stoic analysis
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
    engine = AureliusEngine()
    signal = engine.analyze(meta_input)
    
    # Convert back to legacy format
    return MetaEngineResult(
        scores=signal.scores,
        dominant_axes=signal.dominant_axes,
        severity=signal.severity,
        notes=signal.notes
    )
