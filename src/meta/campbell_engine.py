"""
CampbellEngine v3.1 - Snapshot-only Hero's Journey Analysis.

Analyzes text through the lens of the Hero's Journey (Monomyth), mapping
Δ144 archetypes to Campbellian roles and detecting the current journey stage.

Integrations:
- Δ144: Normalized mapping to Campbell roles (Hero, Mentor, Shadow, etc.)
- Kindra 3×48: Mythic signature extraction (intensity, depth)
- TW369: Transformation potential estimation via drift/regime
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Tuple, Optional, TYPE_CHECKING

# Import shared types
from src.meta.types import MetaInput
from src.common.unified_signal import MetaSignal
from src.unification.states.unified_state import KindraContext
from src.tw369.tw369_integration import TWState

if TYPE_CHECKING:
    from src.unification.states.unified_state import DriftContext, StoryContext


# ============================================================================
# Constants & Mappings
# ============================================================================

# Strict mapping from Δ144 Archetypes to Campbell Roles
CAMPBELL_ARCHETYPES = {
    "A04_HERO": "HERO",
    "A02_SAGE": "MENTOR",
    "A07_RULER": "THRESHOLD_GUARDIAN",
    "A05_EXPLORER": "HERALD",
    "A03_MAGICIAN": "SHAPESHIFTER",
    "A08_REBEL": "SHADOW",
    "A06_CAREGIVER": "ALLY",
    "A11_TRICKSTER": "TRICKSTER",
    "A01_CREATOR": "CREATOR",  # Can function as a higher-order Mentor or God-figure
    "A09_LOVER": "LOVER",      # Often the "Goddess" or temptation
    "A10_INNOCENT": "INNOCENT", # Often the starting state
    "A12_ORACLE": "ORACLE"     # Special role, often Herald or Mentor variant
}

# The 12 Stages of the Hero's Journey
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
    "RETURN_WITH_ELIXIR"
]

# Keyword markers for stage detection (Heuristic Snapshot)
STAGE_KEYWORDS = {
    "ORDINARY_WORLD": ["normal", "routine", "everyday", "status quo", "boredom", "home", "safe"],
    "CALL_TO_ADVENTURE": ["message", "invitation", "threat", "disruption", "opportunity", "challenge", "summon"],
    "REFUSAL_OF_CALL": ["fear", "hesitation", "doubt", "refuse", "ignore", "avoid", "unsafe"],
    "MEETING_MENTOR": ["guide", "teacher", "advice", "training", "gift", "weapon", "wisdom", "elder"],
    "CROSSING_THRESHOLD": ["leave", "enter", "border", "gate", "unknown", "new world", "commitment"],
    "TESTS_ALLIES_ENEMIES": ["friend", "enemy", "test", "trial", "team", "rival", "learning"],
    "APPROACH_INMOST_CAVE": ["prepare", "plan", "danger", "darkness", "lair", "deep", "focus"],
    "ORDEAL": ["crisis", "death", "battle", "confrontation", "sacrifice", "survival", "climax"],
    "REWARD": ["treasure", "elixir", "knowledge", "power", "celebration", "relief", "gift"],
    "ROAD_BACK": ["chase", "escape", "return", "pursuit", "urgency", "consequence"],
    "RESURRECTION": ["rebirth", "transform", "final test", "purification", "mastery", "change"],
    "RETURN_WITH_ELIXIR": ["home", "share", "heal", "solution", "freedom", "master", "peace"]
}


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class CampbellSignal(MetaSignal):
    """
    Output signal from CampbellEngine analysis (v3.1+).
    
    Attributes:
        journey_stage: Detected stage (one of JOURNEY_STAGES)
        archetypal_roles: Mapping of Δ144 IDs to Campbell roles
        transformation_potential: [0, 1] Potential for growth/change
        mythic_resonance: [0, 1] Adherence to monomyth patterns
        active_archetypes: List of top active Campbell roles
        scores: Auxiliary scores (e.g., stage confidence)
        dominant_axes: Top detected stages or themes
        severity: Strength of the mythic pattern [0, 1]
        notes: Interpretive notes
        
        # v3.2: Temporal fields
        journey_sequence: Sequence of journey stages over time
        temporal_coherence: [0, 1] Narrative consistency over time
        arc_completeness: [0, 1] How complete the Hero's Journey is
        drift_coupling: [0, 1] Alignment between drift transitions and journey milestones
        delta144_alignment: [0, 1] Archetypal consistency across temporal progression
    """
    journey_stage: str = "ORDINARY_WORLD"
    archetypal_roles: Dict[str, str] = field(default_factory=dict)
    transformation_potential: float = 0.0
    mythic_resonance: float = 0.0
    active_archetypes: List[str] = field(default_factory=list)
    scores: Dict[str, float] = field(default_factory=dict)
    dominant_axes: List[Tuple[str, float]] = field(default_factory=list)
    severity: float = 0.0
    notes: List[str] = field(default_factory=list)
    name: str = "campbell"
    label: str = ""  # e.g., "incipient_hero", "trial_phase"
    score: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)
    
    # v3.2: Temporal fields (backward compatible defaults)
    journey_sequence: List[str] = field(default_factory=list)
    temporal_coherence: float = 0.0
    arc_completeness: float = 0.0
    drift_coupling: float = 0.0
    delta144_alignment: float = 0.0

    def __post_init__(self):
        super().__post_init__()
        # v3.1 clamps
        self.transformation_potential = max(0.0, min(1.0, self.transformation_potential))
        self.mythic_resonance = max(0.0, min(1.0, self.mythic_resonance))
        self.severity = max(0.0, min(1.0, self.severity))
        
        # v3.2 clamps
        self.temporal_coherence = max(0.0, min(1.0, self.temporal_coherence))
        self.arc_completeness = max(0.0, min(1.0, self.arc_completeness))
        self.drift_coupling = max(0.0, min(1.0, self.drift_coupling))
        self.delta144_alignment = max(0.0, min(1.0, self.delta144_alignment))


# ============================================================================
# CampbellEngine v3.1
# ============================================================================

class CampbellEngine:
    """
    CampbellEngine v3.2 — Snapshot + Temporal Hero's Journey analyzer.

    - Uses Δ144 for role mapping
    - Uses Kindra 3×48 for mythic resonance
    - Uses TW369 for transformation potential
    - Detects journey stage from text snapshot
    - v3.2: Temporal analysis with Story and Drift integration
    """
    
    name = "campbell"
    
    # ========================================================================
    # v3.2: Temporal Analysis Methods
    # ========================================================================
    
    def _infer_journey_sequence_from_story(
        self,
        story_ctx: Optional['StoryContext']
    ) -> List[str]:
        """
        Build journey sequence from StoryContext.
        
        Args:
            story_ctx: StoryContext with timeline/arc
            
        Returns:
            List of journey stages in temporal order (deduplicated)
        """
        if not story_ctx:
            return []
            
        sequence = []
        
        # Try to extract from arc.stage_scores if available
        if story_ctx.arc and hasattr(story_ctx.arc, 'stage_scores'):
            # Build sequence from stage_scores (sorted by score)
            stage_scores = story_ctx.arc.stage_scores
            if stage_scores:
                # Sort stages by score, take top stages
                sorted_stages = sorted(stage_scores.items(), key=lambda x: x[1], reverse=True)
                # Take stages with non-trivial scores
                for stage, score in sorted_stages:
                    if score > 0.1:  # Threshold for meaningful presence
                        sequence.append(stage)
        
        # TODO v3.3: Extract temporal sequence from timeline if available
        # if story_ctx.timeline and hasattr(story_ctx.timeline, 'events'):
        #     for event in story_ctx.timeline.events:
        #         if event.dominant_stage:
        #             sequence.append(event.dominant_stage)
        
        # Remove consecutive duplicates
        deduplicated = []
        prev = None
        for stage in sequence:
            if stage != prev:
                deduplicated.append(stage)
                prev = stage
                
        return deduplicated
    
    def _measure_transformation_arc(
        self,
        story_ctx: Optional['StoryContext'],
        delta144_timeline: Optional[List[Dict[str, Any]]]
    ) -> float:
        """
        Measure transformation arc completeness.
        
        Scoring:
        - 0.0-0.3: Stuck in early stages (ORDINARY_WORLD, REFUSAL)
        - 0.4-0.6: Reaches middle stages (ORDEAL, REWARD) but incomplete
        - 0.7-1.0: Full journey (ORDEAL → RESURRECTION → RETURN)
        
        Args:
            story_ctx: StoryContext with arc info
            delta144_timeline: Optional archetype evolution timeline
            
        Returns:
            Arc completeness score [0, 1]
        """
        base_score = 0.3
        
        # Extract dominant stage from arc
        if story_ctx and story_ctx.arc:
            dominant_stage = getattr(story_ctx.arc, 'dominant_stage', None)
            
            # Scoring by stage
            early_stages = ["ORDINARY_WORLD", "CALL_TO_ADVENTURE", "REFUSAL_OF_CALL"]
            middle_stages = ["ORDEAL", "REWARD", "APPROACH_INMOST_CAVE", "TESTS_ALLIES_ENEMIES"]
            late_stages = ["RESURRECTION", "RETURN_WITH_ELIXIR", "ROAD_BACK"]
            
            if dominant_stage in early_stages:
                base_score = 0.2
            elif dominant_stage in middle_stages:
                base_score = 0.5
            elif dominant_stage in late_stages:
                base_score = 0.9
        
        # Boost if Δ144 timeline shows archetype evolution
        if delta144_timeline and len(delta144_timeline) >= 2:
            # Check for progression from innocent/hero to sage/creator
            first_state = delta144_timeline[0].get('state_id', '')
            last_state = delta144_timeline[-1].get('state_id', '')
            
            # Heuristic: early archetypes → mature archetypes
            early_archetypes = ['A10_INNOCENT', 'A04_HERO']
            mature_archetypes = ['A02_SAGE', 'A01_CREATOR', 'A06_CAREGIVER']
            
            has_early = any(arch in first_state for arch in early_archetypes)
            has_mature = any(arch in last_state for arch in mature_archetypes)
            
            if has_early and has_mature:
                base_score += 0.15
            elif has_mature:
                base_score += 0.08
                
        return min(1.0, max(0.0, base_score))
    
    def _compute_temporal_coherence(
        self,
        story_ctx: Optional['StoryContext']
    ) -> float:
        """
        Compute temporal coherence of narrative.
        
        Uses StoryContext.coherence if available,
        else heuristic based on stage continuity.
        
        Args:
            story_ctx: StoryContext with coherence info
            
        Returns:
            Coherence score [0, 1]
        """
        if not story_ctx:
            return 0.0
            
        # Use coherence.overall if available
        if story_ctx.coherence and hasattr(story_ctx.coherence, 'overall'):
            return min(1.0, max(0.0, story_ctx.coherence.overall))
        
        # Fallback: check if coherence is a float directly
        if isinstance(story_ctx.coherence, (int, float)):
            return min(1.0, max(0.0, float(story_ctx.coherence)))
            
        # TODO v3.3: Implement stage sequence coherence checking
        # Penalize illogical jumps (e.g., CALL → RETURN without ORDEAL)
        
        return 0.5  # Default moderate coherence
    
    def _compute_drift_coupling(
        self,
        drift_ctx: Optional['DriftContext'],
        journey_sequence: List[str]
    ) -> float:
        """
        Measure alignment between drift turning points and journey milestones.
        
        Args:
            drift_ctx: DriftContext with turning_points
            journey_sequence: Journey stages in sequence
            
        Returns:
            Coupling score [0, 1]: proportion of turning points near critical stages
        """
        if not drift_ctx or not journey_sequence:
            return 0.0
            
        # Check if drift_ctx has turning_points
        turning_points = getattr(drift_ctx, 'turning_points', [])
        if not turning_points:
            return 0.0
            
        # Critical journey stages where drift should align
        critical_stages = ["ORDEAL", "RESURRECTION", "RETURN_WITH_ELIXIR", "CROSSING_THRESHOLD"]
        
        # Count how many turning points occur during critical stages
        # NOTE: This is a simplified heuristic; v3.3 should use actual timestamps
        aligned_count = 0
        
        # If any critical stage is in sequence, assume some coupling potential
        has_critical = any(stage in journey_sequence for stage in critical_stages)
        
        if has_critical and turning_points:
            # Simple heuristic: if we have turning points and critical stages present,
            # assume proportional alignment
            alignment_ratio = min(len(turning_points) / 3.0, 1.0)  # Normalize by expected ~3 major transitions
            aligned_count = alignment_ratio
            
        # TODO v3.3: Use actual timestamp matching between turning_points and story events
        
        coupling = aligned_count if has_critical else 0.0
        return min(1.0, max(0.0, coupling))
    
    def _compute_delta144_alignment(
        self,
        delta144_timeline: Optional[List[Dict[str, Any]]],
        journey_sequence: List[str]
    ) -> float:
        """
        Measure alignment between Δ144 archetypes and Campbell journey stages.
        
        Args:
            delta144_timeline: Timeline of archetype states
            journey_sequence: Journey stages
            
        Returns:
            Alignment score [0, 1]
        """
        if not delta144_timeline or not journey_sequence:
            return 0.0
            
        # Expected archetype-stage pairings (heuristic)
        expected_pairings = {
            "CALL_TO_ADVENTURE": ["A04_HERO", "A05_EXPLORER"],
            "MEETING_MENTOR": ["A02_SAGE", "A06_CAREGIVER"],
            "ORDEAL": ["A04_HERO", "A08_REBEL"],
            "RESURRECTION": ["A04_HERO", "A01_CREATOR"],
            "RETURN_WITH_ELIXIR": ["A02_SAGE", "A01_CREATOR", "A06_CAREGIVER"]
        }
        
        # Count matches
        matches = 0
        total_checks = 0
        
        for stage in journey_sequence:
            if stage in expected_pairings:
                expected_archetypes = expected_pairings[stage]
                total_checks += 1
                
                # Check if any delta144_timeline entry matches expected archetypes
                for entry in delta144_timeline:
                    state_id = entry.get('state_id', '')
                    if any(arch in state_id for arch in expected_archetypes):
                        matches += 1
                        break
        
        if total_checks == 0:
            return 0.5  # Default if no critical stages to check
            
        alignment = matches / total_checks
        return min(1.0, max(0.0, alignment))

    def analyze(self, meta_input: MetaInput) -> CampbellSignal:
        """
        Analyze text through the Hero's Journey lens.
        
        Args:
            meta_input: Standardized input containing text, archetypes, Kindra, TW.
            
        Returns:
            CampbellSignal with stage, roles, and resonance metrics.
        """
        text_lower = meta_input.text.lower()
        
        # 1. Map Archetypes (Δ144 → Campbell)
        archetypal_roles, active_archetypes = self._map_delta144_to_roles(
            meta_input.delta144_state,
            meta_input.archetype_scores
        )
        
        # 2. Compute Kindra Mythic Signature
        kindra_sig = self._compute_kindra_mythic_signature(meta_input.kindra)
        
        # 3. Detect Journey Stage (Snapshot)
        journey_stage, stage_conf = self._detect_journey_stage(
            text_lower,
            archetypal_roles,
            kindra_sig
        )
        
        # 4. Estimate Transformation Potential (TW369)
        trans_potential = self._estimate_transformation_potential(
            journey_stage,
            kindra_sig,
            meta_input.tw_state
        )
        
        # 5. Compute Mythic Resonance
        mythic_resonance = self._compute_mythic_resonance(
            journey_stage,
            stage_conf,
            archetypal_roles,
            kindra_sig
        )
        
        # 6. Build Scores and Notes
        scores, dominant_axes, notes, label, severity = self._build_scores_and_notes(
            journey_stage,
            stage_conf,
            active_archetypes,
            trans_potential,
            mythic_resonance
        )
        
        # v3.1: Build base signal (snapshot)
        signal = CampbellSignal(
            journey_stage=journey_stage,
            archetypal_roles=archetypal_roles,
            transformation_potential=trans_potential,
            mythic_resonance=mythic_resonance,
            active_archetypes=active_archetypes,
            scores=scores,
            dominant_axes=dominant_axes,
            severity=severity,
            notes=notes,
            label=label,
            score=mythic_resonance, # Base MetaSignal score
            details={
                "kindra_signature": kindra_sig,
                "stage_confidence": stage_conf,
                "tw369_applied": meta_input.tw_state is not None
            }
        )
        
        # v3.2: Temporal enrichment (additive, gracefully degrades)
        try:
            drift_ctx = getattr(meta_input, 'drift_ctx', None)
            story_ctx = getattr(meta_input, 'story_ctx', None)
            
            # Early exit if no temporal contexts
            if not drift_ctx and not story_ctx:
                return signal
                
            # Extract Δ144 timeline if present
            delta144_timeline = None
            if story_ctx and story_ctx.metadata:
                delta144_timeline = story_ctx.metadata.get("delta144_timeline")
            
            # (a) Journey sequence
            if story_ctx:
                signal.journey_sequence = self._infer_journey_sequence_from_story(story_ctx)
            
            # (b) Temporal coherence
            if story_ctx:
                signal.temporal_coherence = self._compute_temporal_coherence(story_ctx)
            
            # (c) Arc completeness
            if story_ctx or delta144_timeline:
                signal.arc_completeness = self._measure_transformation_arc(
                    story_ctx=story_ctx,
                    delta144_timeline=delta144_timeline
                )
            
            # (d) Drift coupling
            if drift_ctx and signal.journey_sequence:
                signal.drift_coupling = self._compute_drift_coupling(
                    drift_ctx=drift_ctx,
                    journey_sequence=signal.journey_sequence
                )
            
            # (e) Δ144 alignment
            if delta144_timeline and signal.journey_sequence:
                signal.delta144_alignment = self._compute_delta144_alignment(
                    delta144_timeline=delta144_timeline,
                    journey_sequence=signal.journey_sequence
                )
            
            # Update details with temporal flags
            signal.details["temporal_enrichment_applied"] = True
            signal.details["story_ctx_present"] = story_ctx is not None
            signal.details["drift_ctx_present"] = drift_ctx is not None
            
        except Exception as e:
            # Log but don't fail - graceful degradation
            import logging
            logging.warning(f"CampbellEngine temporal enrichment failed: {e}")
            signal.details["temporal_enrichment_error"] = str(e)
        
        return signal


    def _map_delta144_to_roles(
        self,
        delta144_state: Optional[str],
        archetype_scores: Dict[str, float]
    ) -> Tuple[Dict[str, str], List[str]]:
        """
        Map Δ144 archetypes to Campbell roles.
        
        Returns:
            archetypal_roles: {id_Δ144: "HERO"/"MENTOR"/...}
            active_archetypes: List of top active Campbell roles
        """
        roles_map = {}
        active_list = []
        
        # 1. Check explicit state first
        if delta144_state:
            # Extract base ID (e.g., "A04_HERO" from "A04_HERO_STATE_XX")
            for base_id, role in CAMPBELL_ARCHETYPES.items():
                if base_id in delta144_state:
                    roles_map[delta144_state] = role
                    active_list.append(role)
                    break
        
        # 2. Check scores if state didn't yield or to supplement
        if archetype_scores:
            # Sort by score descending
            sorted_archs = sorted(archetype_scores.items(), key=lambda x: x[1], reverse=True)
            
            for arch_id, score in sorted_archs[:3]: # Take top 3
                # Match against CAMPBELL_ARCHETYPES keys
                # arch_id might be full ID or just prefix, assume standard keys for now
                matched_role = None
                for base_id, role in CAMPBELL_ARCHETYPES.items():
                    if base_id in arch_id:
                        matched_role = role
                        roles_map[arch_id] = role
                        break
                
                if matched_role and matched_role not in active_list:
                    active_list.append(matched_role)
        
        # Fallback if nothing found
        if not active_list:
            active_list = ["HERO"] # Default assumption for the protagonist
            
        return roles_map, active_list[:3]

    def _compute_kindra_mythic_signature(
        self,
        kindra: Optional[KindraContext]
    ) -> Dict[str, float]:
        """
        Extract mythic metrics from Kindra 3×48.
        
        Metrics:
        - narrative_intensity (Layer 2): Conflict, climax, urgency
        - archetypal_depth (Layer 3): Symbolism, meaning
        - worldbuilding_clarity (Layer 1): Coherence, order
        - liminality_factor (Layer 2+3): Transition, threshold
        """
        if not kindra:
            return {
                "narrative_intensity": 0.0,
                "archetypal_depth": 0.0,
                "worldbuilding_clarity": 0.0,
                "liminality_factor": 0.0
            }
            
        # Helper to extract average score for keywords
        def get_score(layer: Dict[str, float], keywords: List[str]) -> float:
            matches = []
            for k, v in layer.items():
                if any(kw in k.lower() for kw in keywords):
                    matches.append(v)
            return sum(matches) / len(matches) if matches else 0.0

        # Layer 1: Cultural/Macro
        world_clarity = get_score(kindra.layer1, ["order", "structure", "system", "law", "tradition"])
        
        # Layer 2: Semiotic/Media
        intensity = get_score(kindra.layer2, ["intensity", "conflict", "urgency", "passion", "climax"])
        liminality_l2 = get_score(kindra.layer2, ["transition", "change", "flux", "uncertainty"])
        
        # Layer 3: Structural/Systemic
        depth = get_score(kindra.layer3, ["myth", "symbol", "meaning", "archetype", "transcendence"])
        liminality_l3 = get_score(kindra.layer3, ["threshold", "transformation", "boundary"])
        
        return {
            "narrative_intensity": intensity,
            "archetypal_depth": depth,
            "worldbuilding_clarity": world_clarity,
            "liminality_factor": (liminality_l2 + liminality_l3) / 2
        }

    def _detect_journey_stage(
        self,
        text: str,
        roles: Dict[str, str],
        kindra_sig: Dict[str, float]
    ) -> Tuple[str, float]:
        """
        Detect the current journey stage based on text keywords and signals.
        Returns (stage_name, confidence).
        """
        stage_scores = {stage: 0.0 for stage in JOURNEY_STAGES}
        
        # 1. Keyword Scoring
        for stage, keywords in STAGE_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in text)
            if count > 0:
                # Normalize count impact
                stage_scores[stage] += min(1.0, count * 0.2)
        
        # 2. Role Influence
        active_roles = list(roles.values())
        if "MENTOR" in active_roles:
            stage_scores["MEETING_MENTOR"] += 0.4
            stage_scores["CALL_TO_ADVENTURE"] += 0.2
        if "THRESHOLD_GUARDIAN" in active_roles:
            stage_scores["CROSSING_THRESHOLD"] += 0.4
        if "SHADOW" in active_roles:
            stage_scores["ORDEAL"] += 0.3
            stage_scores["RESURRECTION"] += 0.3
        if "ALLY" in active_roles:
            stage_scores["TESTS_ALLIES_ENEMIES"] += 0.3
            
        # 3. Kindra Influence
        # High intensity -> Ordeal/Resurrection
        if kindra_sig["narrative_intensity"] > 0.6:
            stage_scores["ORDEAL"] += 0.3
            stage_scores["RESURRECTION"] += 0.2
            stage_scores["ROAD_BACK"] += 0.2
            
        # High liminality -> Thresholds
        if kindra_sig["liminality_factor"] > 0.6:
            stage_scores["CROSSING_THRESHOLD"] += 0.3
            stage_scores["APPROACH_INMOST_CAVE"] += 0.2
            stage_scores["RETURN_WITH_ELIXIR"] += 0.2
            
        # High world clarity -> Ordinary World / Return
        if kindra_sig["worldbuilding_clarity"] > 0.7:
            stage_scores["ORDINARY_WORLD"] += 0.3
            stage_scores["RETURN_WITH_ELIXIR"] += 0.2

        # Select best stage
        best_stage = max(stage_scores.items(), key=lambda x: x[1])
        
        # If no signal detected, default to Ordinary World with low confidence
        if best_stage[1] == 0.0:
            return "ORDINARY_WORLD", 0.1
            
        # Normalize confidence roughly to [0, 1]
        confidence = min(1.0, best_stage[1])
        return best_stage[0], confidence

    def _estimate_transformation_potential(
        self,
        journey_stage: str,
        kindra_sig: Dict[str, float],
        tw_state: Optional[TWState]
    ) -> float:
        """
        Estimate potential for transformation based on stage, drift, and depth.
        """
        base_potential = 0.3
        
        # Stage Baseline
        high_potential_stages = ["ORDEAL", "REWARD", "RESURRECTION", "APPROACH_INMOST_CAVE"]
        low_potential_stages = ["ORDINARY_WORLD", "REFUSAL_OF_CALL"]
        
        if journey_stage in high_potential_stages:
            base_potential = 0.7
        elif journey_stage in low_potential_stages:
            base_potential = 0.2
        else:
            base_potential = 0.5
            
        # Kindra Adjustments
        # Depth implies meaningful change
        base_potential += kindra_sig["archetypal_depth"] * 0.2
        
        # TW369 Adjustments
        if tw_state and tw_state.metadata:
            drift = tw_state.metadata.get("drift_metric", 0.0)
            regime = tw_state.metadata.get("regime", "UNKNOWN")
            
            # High drift + Critical/Transition = High transformation potential
            if drift > 0.6:
                base_potential += 0.15
            
            if regime in ["CRITICAL", "TRANSITION"]:
                base_potential += 0.15
            elif regime == "STABLE" and journey_stage in low_potential_stages:
                # Stable + Ordinary World = Stagnation
                base_potential -= 0.1
                
        return min(1.0, max(0.0, base_potential))

    def _compute_mythic_resonance(
        self,
        journey_stage: str,
        stage_conf: float,
        roles: Dict[str, str],
        kindra_sig: Dict[str, float]
    ) -> float:
        """
        Measure how 'monomythic' the snapshot is.
        """
        resonance = 0.0
        
        # 1. Confidence in the stage detection
        resonance += stage_conf * 0.4
        
        # 2. Presence of key roles
        if roles:
            resonance += 0.2
            if "HERO" in roles.values():
                resonance += 0.1
                
        # 3. Kindra Depth & Intensity
        resonance += kindra_sig["archetypal_depth"] * 0.2
        resonance += kindra_sig["narrative_intensity"] * 0.1
        
        return min(1.0, resonance)

    def _build_scores_and_notes(
        self,
        journey_stage: str,
        stage_conf: float,
        active_archetypes: List[str],
        trans_potential: float,
        mythic_resonance: float
    ) -> Tuple[Dict[str, float], List[Tuple[str, float]], List[str], str, float]:
        """
        Construct auxiliary scores, notes, and labels.
        """
        scores = {
            "stage_confidence": stage_conf,
            "transformation_potential": trans_potential,
            "mythic_resonance": mythic_resonance
        }
        
        dominant_axes = [(journey_stage, stage_conf)]
        
        # Severity is essentially the strength of the mythic pattern here
        severity = mythic_resonance
        
        # Label generation
        label = journey_stage.lower()
        if active_archetypes:
            label += f" ({active_archetypes[0].lower()})"
            
        # Notes generation
        notes = []
        notes.append(f"Stage: {journey_stage.replace('_', ' ')} (Conf: {stage_conf:.2f})")
        
        if active_archetypes:
            notes.append(f"Active Roles: {', '.join(active_archetypes)}")
            
        if trans_potential > 0.7:
            notes.append("High transformation potential detected.")
        elif trans_potential < 0.3:
            notes.append("Low transformation potential; static state.")
            
        if mythic_resonance > 0.7:
            notes.append("Strong mythic resonance.")
            
        return scores, dominant_axes, notes, label, severity
