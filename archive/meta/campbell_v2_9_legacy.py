"""
CampbellEngine - Hero's Journey Analysis (12 Stages).

Analyzes KALDRA signals through Joseph Campbell's monomyth framework,
detecting which stage of the Hero's Journey the narrative is in.
"""

from typing import Dict, Any, List, Tuple
from .meta_engine_base import MetaEngineBase, MetaSignal


# The 12 canonical stages of the Hero's Journey
HERO_JOURNEY_STAGES = [
    "ordinary_world",          # 1. Mundo comum
    "call_to_adventure",       # 2. Chamado à aventura
    "refusal_of_the_call",     # 3. Recusa do chamado
    "meeting_with_the_mentor", # 4. Encontro com o mentor
    "crossing_the_threshold",  # 5. Travessia do primeiro limiar
    "tests_allies_enemies",    # 6. Testes, aliados e inimigos
    "approach_to_cave",        # 7. Aproximação da caverna secreta
    "ordeal",                  # 8. Provação suprema
    "reward",                  # 9. Recompensa (apoderar-se da espada)
    "road_back",               # 10. Caminho de volta
    "resurrection",            # 11. Ressurreição
    "return_with_elixir"       # 12. Retorno com o elixir
]


class CampbellEngine(MetaEngineBase):
    """
    Meta-engine analyzing signals through Campbell's Hero's Journey.
    
    Maps drift patterns, archetype transitions, and coherence to the 12 stages
    of the monomyth.
    """
    
    name = "campbell"
    
    def run(self, signal: Dict[str, Any]) -> MetaSignal:
        """
        Detect current Hero's Journey stage from KALDRA signal.
        
        Uses:
        - Δ144: Current archetype + state
        - DriftMemory: Recent history of drift states
        - TWState: Current drift metric, coherence
        - Painlevé coherence: Structural stability
        """
        try:
            # Extract components
            delta144 = signal.get("delta144")
            drift_history = signal.get("drift_history", [])
            tw_state = signal.get("tw_state")
            
            # Detect stage
            stage_index, confidence = self._detect_stage(delta144, drift_history, tw_state)
            stage_label = HERO_JOURNEY_STAGES[stage_index]
            
            details = {
                "stage_index": stage_index,
                "stage_name": stage_label,
                "confidence": confidence,
                "drift_pattern": self._analyze_drift_pattern(drift_history),
                "archetype_context": self._get_archetype_context(delta144),
            }
            
            return MetaSignal(
                name=self.name,
                score=confidence,
                label=stage_label,
                details=details
            )
            
        except Exception as e:
            # Fail-safe: return ordinary_world with low confidence
            return MetaSignal(
                name=self.name,
                score=0.3,
                label="ordinary_world",
                details={"error": str(e)}
            )
    
    def _detect_stage(
        self,
        delta144: Any,
        drift_history: List,
        tw_state: Any
    ) -> Tuple[int, float]:
        """
        Detect which of the 12 stages best matches current state.
        
        Returns:
            (stage_index, confidence) where stage_index ∈ [0, 11]
        """
        # Calculate features for stage detection
        drift_level = self._get_drift_level(drift_history, tw_state)
        drift_trend = self._get_drift_trend(drift_history)
        coherence = self._get_coherence(drift_history, tw_state)
        archetype_type = self._get_archetype_type(delta144)
        regime_change = self._detect_regime_change(drift_history)
        
        # Score each stage
        stage_scores = []
        
        # Stage 1: Ordinary World
        stage_scores.append(self._score_ordinary_world(drift_level, drift_trend, coherence, archetype_type))
        
        # Stage 2: Call to Adventure
        stage_scores.append(self._score_call_to_adventure(drift_level, drift_trend, archetype_type))
        
        # Stage 3: Refusal of the Call
        stage_scores.append(self._score_refusal(drift_level, archetype_type, coherence))
        
        # Stage 4: Meeting with the Mentor
        stage_scores.append(self._score_mentor(drift_level, archetype_type, coherence))
        
        # Stage 5: Crossing the Threshold
        stage_scores.append(self._score_threshold(drift_level, regime_change, archetype_type))
        
        # Stage 6: Tests, Allies, Enemies
        stage_scores.append(self._score_tests(drift_level, drift_trend, coherence))
        
        # Stage 7: Approach to the Cave
        stage_scores.append(self._score_approach(drift_level, drift_trend, archetype_type))
        
        # Stage 8: Ordeal
        stage_scores.append(self._score_ordeal(drift_level, coherence, archetype_type))
        
        # Stage 9: Reward
        stage_scores.append(self._score_reward(drift_level, drift_trend, archetype_type, coherence))
        
        # Stage 10: Road Back
        stage_scores.append(self._score_road_back(drift_level, drift_trend, archetype_type))
        
        # Stage 11: Resurrection
        stage_scores.append(self._score_resurrection(drift_level, coherence, archetype_type))
        
        # Stage 12: Return with Elixir
        stage_scores.append(self._score_return(drift_level, coherence, archetype_type))
        
        # Find best match
        best_index = stage_scores.index(max(stage_scores))
        confidence = stage_scores[best_index]
        
        return best_index, confidence
    
    # ========== Stage Scoring Functions ==========
    
    def _score_ordinary_world(self, drift_level: str, drift_trend: str, coherence: float, arch_type: str) -> float:
        """Stage 1: Low drift, stable, neutral archetypes."""
        score = 0.3
        if drift_level == "low":
            score += 0.3
        if drift_trend == "stable":
            score += 0.2
        if coherence > 0.7:
            score += 0.1
        if arch_type in ["neutral", "caregiver"]:
            score += 0.1
        return min(1.0, score)
    
    def _score_call_to_adventure(self, drift_level: str, drift_trend: str, arch_type: str) -> float:
        """Stage 2: Rising drift, action archetypes emerging."""
        score = 0.2
        if drift_trend == "increasing":
            score += 0.4
        if drift_level in ["low", "medium"]:
            score += 0.2
        if arch_type in ["action", "seeker"]:
            score += 0.2
        return min(1.0, score)
    
    def _score_refusal(self, drift_level: str, arch_type: str, coherence: float) -> float:
        """Stage 3: High tension but defensive archetypes."""
        score = 0.2
        if drift_level in ["medium", "high"]:
            score += 0.3
        if arch_type in ["defensive", "caregiver"]:
            score += 0.3
        if coherence > 0.5:
            score += 0.2
        return min(1.0, score)
    
    def _score_mentor(self, drift_level: str, arch_type: str, coherence: float) -> float:
        """Stage 4: Wisdom archetypes, moderate drift, high coherence."""
        score = 0.2
        if arch_type in ["wisdom", "sage"]:
            score += 0.4
        if drift_level == "medium":
            score += 0.2
        if coherence > 0.7:
            score += 0.2
        return min(1.0, score)
    
    def _score_threshold(self, drift_level: str, regime_change: bool, arch_type: str) -> float:
        """Stage 5: Clear regime change, rising drift."""
        score = 0.2
        if regime_change:
            score += 0.4
        if drift_level in ["medium", "high"]:
            score += 0.2
        if arch_type in ["action", "rebel"]:
            score += 0.2
        return min(1.0, score)
    
    def _score_tests(self, drift_level: str, drift_trend: str, coherence: float) -> float:
        """Stage 6: Oscillating drift, moderate coherence."""
        score = 0.2
        if drift_level == "medium":
            score += 0.3
        if drift_trend == "oscillating":
            score += 0.3
        if 0.4 < coherence < 0.7:
            score += 0.2
        return min(1.0, score)
    
    def _score_approach(self, drift_level: str, drift_trend: str, arch_type: str) -> float:
        """Stage 7: Rising drift, preparation mode."""
        score = 0.2
        if drift_trend == "increasing":
            score += 0.3
        if drift_level in ["medium", "high"]:
            score += 0.2
        if arch_type in ["action", "strategic"]:
            score += 0.3
        return min(1.0, score)
    
    def _score_ordeal(self, drift_level: str, coherence: float, arch_type: str) -> float:
        """Stage 8: Peak drift, low coherence, crisis archetypes."""
        score = 0.2
        if drift_level == "high":
            score += 0.4
        if coherence < 0.4:
            score += 0.2
        if arch_type in ["action", "rebel", "orphan"]:
            score += 0.2
        return min(1.0, score)
    
    def _score_reward(self, drift_level: str, drift_trend: str, arch_type: str, coherence: float) -> float:
        """Stage 9: Falling drift after peak, constructive archetypes."""
        score = 0.2
        if drift_trend == "decreasing":
            score += 0.3
        if arch_type in ["creator", "wisdom", "strategic"]:
            score += 0.3
        if coherence > 0.5:
            score += 0.2
        return min(1.0, score)
    
    def _score_road_back(self, drift_level: str, drift_trend: str, arch_type: str) -> float:
        """Stage 10: Stabilizing drift, structural archetypes."""
        score = 0.2
        if drift_trend in ["decreasing", "stable"]:
            score += 0.3
        if drift_level in ["medium", "low"]:
            score += 0.2
        if arch_type in ["strategic", "caregiver"]:
            score += 0.3
        return min(1.0, score)
    
    def _score_resurrection(self, drift_level: str, coherence: float, arch_type: str) -> float:
        """Stage 11: Transformative peak, transcendent archetypes."""
        score = 0.2
        if drift_level in ["medium", "high"]:
            score += 0.2
        if coherence > 0.6:
            score += 0.3
        if arch_type in ["wisdom", "transcendent"]:
            score += 0.3
        return min(1.0, score)
    
    def _score_return(self, drift_level: str, coherence: float, arch_type: str) -> float:
        """Stage 12: Low drift, high coherence, integrative archetypes."""
        score = 0.2
        if drift_level == "low":
            score += 0.3
        if coherence > 0.7:
            score += 0.3
        if arch_type in ["wisdom", "creator", "caregiver"]:
            score += 0.2
        return min(1.0, score)
    
    # ========== Helper Functions ==========
    
    def _get_drift_level(self, drift_history: List, tw_state: Any) -> str:
        """Classify current drift as low/medium/high."""
        current_drift = 0.0
        
        if drift_history and len(drift_history) > 0:
            current_drift = drift_history[-1].drift_metric
        elif tw_state and hasattr(tw_state, "metadata") and tw_state.metadata:
            current_drift = tw_state.metadata.get("drift_metric", 0.0)
        
        if current_drift < 0.3:
            return "low"
        elif current_drift < 0.7:
            return "medium"
        else:
            return "high"
    
    def _get_drift_trend(self, drift_history: List) -> str:
        """Detect drift trend: increasing/decreasing/stable/oscillating."""
        if len(drift_history) < 3:
            return "stable"
        
        recent = [state.drift_metric for state in drift_history[-5:]]
        
        # Check for oscillation (high variance)
        mean = sum(recent) / len(recent)
        variance = sum((x - mean) ** 2 for x in recent) / len(recent)
        
        if variance > 0.1:
            return "oscillating"
        
        # Check trend
        if recent[-1] > recent[0] * 1.2:
            return "increasing"
        elif recent[-1] < recent[0] * 0.8:
            return "decreasing"
        else:
            return "stable"
    
    def _get_coherence(self, drift_history: List, tw_state: Any) -> float:
        """Get Painlevé coherence score."""
        if drift_history and len(drift_history) > 0:
            return drift_history[-1].painleve_coherence
        return 0.5  # Neutral default
    
    def _get_archetype_type(self, delta144: Any) -> str:
        """Classify dominant archetype into categories."""
        if not delta144 or not hasattr(delta144, "archetype"):
            return "neutral"
        
        arch_id = delta144.archetype.id if hasattr(delta144.archetype, "id") else ""
        
        # Action archetypes
        if arch_id in ["A03_WARRIOR", "A08_REBEL", "A12_CREATOR"]:
            return "action"
        
        # Wisdom archetypes
        if arch_id in ["A10_SAGE", "A09_MAGICIAN"]:
            return "wisdom"
        
        # Strategic archetypes
        if arch_id in ["A07_RULER"]:
            return "strategic"
        
        # Caregiver archetypes
        if arch_id in ["A04_CAREGIVER", "A06_LOVER"]:
            return "caregiver"
        
        # Seeker archetypes
        if arch_id in ["A05_SEEKER", "A11_JESTER"]:
            return "seeker"
        
        # Defensive/vulnerable
        if arch_id in ["A02_ORPHAN", "A01_INNOCENT"]:
            return "defensive"
        
        return "neutral"
    
    def _detect_regime_change(self, drift_history: List) -> bool:
        """Detect if there was a recent regime change."""
        if len(drift_history) < 2:
            return False
        
        # Check if regime changed in last 3 states
        recent_regimes = [state.regime for state in drift_history[-3:]]
        return len(set(recent_regimes)) > 1
    
    def _analyze_drift_pattern(self, drift_history: List) -> Dict[str, Any]:
        """Analyze drift history pattern."""
        if not drift_history:
            return {"length": 0, "pattern": "unknown"}
        
        return {
            "length": len(drift_history),
            "current": drift_history[-1].drift_metric if drift_history else 0.0,
            "trend": self._get_drift_trend(drift_history),
            "volatility": self._calculate_volatility([s.drift_metric for s in drift_history[-5:]]),
        }
    
    def _get_archetype_context(self, delta144: Any) -> Dict[str, Any]:
        """Get archetype context from Δ144."""
        if not delta144:
            return {}
        
        context = {}
        if hasattr(delta144, "archetype") and delta144.archetype:
            context["archetype_id"] = delta144.archetype.id if hasattr(delta144.archetype, "id") else "unknown"
            context["archetype_label"] = delta144.archetype.label if hasattr(delta144.archetype, "label") else "unknown"
        
        if hasattr(delta144, "state") and delta144.state:
            context["state_profile"] = delta144.state.profile if hasattr(delta144.state, "profile") else "unknown"
        
        return context
    
    def _calculate_volatility(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if not values or len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
