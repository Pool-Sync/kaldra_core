"""
TW369 Integration Module for Kindra 3x48

This module integrates the three Kindra layers (L1, L2, L3) into the TW369 engine,
mapping them to planes 3, 6, and 9 respectively.

Implements temporal drift calculation based on tension gradients between planes.
"""

from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
import math


@dataclass
class TWState:
    """
    Represents the state of the TW369 engine with inputs from all three Kindra layers.
    
    Attributes:
        plane3_cultural_macro: Layer 1 vector scores (Dict[vector_id, score])
        plane6_semiotic_media: Layer 2 vector scores
        plane9_structural_systemic: Layer 3 vector scores
        metadata: Additional context information
    """
    plane3_cultural_macro: Optional[Dict[str, float]] = None
    plane6_semiotic_media: Optional[Dict[str, float]] = None
    plane9_structural_systemic: Optional[Dict[str, float]] = None
    metadata: Optional[Dict[str, Any]] = None


class TW369Integrator:
    """
    Integrates Kindra layers into the TW369 temporal evolution engine.
    
    Implements drift calculation based on:
    - Tension gradients between planes (3→6→9→3)
    - Tracy-Widom severity factors
    - Eigenvalue-based instability indices
    """
    
    def __init__(self):
        # State-to-plane mapping for Δ144 states
        # This is a simplified mapping - can be refined with actual Δ144 structure
        self._state_plane_mapping = self._initialize_state_plane_mapping()
    
    def _initialize_state_plane_mapping(self) -> Dict[str, str]:
        """
        Initialize mapping of Δ144 states to TW planes.
        
        Simplified heuristic:
        - Plane 3 (Cultural/Surface): Emotional, relational archetypes
        - Plane 6 (Semiotic/Tension): Transformative, symbolic archetypes
        - Plane 9 (Structural/Deep): Authority, wisdom archetypes
        """
        mapping = {}
        
        # Plane 3 archetypes (surface, emotional)
        plane3_archetypes = ["Lover", "Jester", "Innocent", "Caregiver", "Everyman"]
        
        # Plane 6 archetypes (tension, transformation)
        plane6_archetypes = ["Hero", "Outlaw", "Magician", "Creator", "Explorer", "Trickster"]
        
        # Plane 9 archetypes (structure, authority)
        plane9_archetypes = ["Ruler", "Sage", "Judge", "Guardian", "Hermit"]
        
        for arch in plane3_archetypes:
            mapping[arch] = "3"
        for arch in plane6_archetypes:
            mapping[arch] = "6"
        for arch in plane9_archetypes:
            mapping[arch] = "9"
        
        # Default for any unmapped states
        return mapping
    
    def create_state(
        self,
        layer1_scores: Optional[Dict[str, float]] = None,
        layer2_scores: Optional[Dict[str, float]] = None,
        layer3_scores: Optional[Dict[str, float]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TWState:
        """
        Creates a TWState object from Kindra layer scores.
        
        Args:
            layer1_scores: Cultural Macro scores (Plane 3)
            layer2_scores: Semiotic/Media scores (Plane 6)
            layer3_scores: Structural/Systemic scores (Plane 9)
            metadata: Additional context
            
        Returns:
            TWState object ready for temporal evolution
        """
        return TWState(
            plane3_cultural_macro=layer1_scores or {},
            plane6_semiotic_media=layer2_scores or {},
            plane9_structural_systemic=layer3_scores or {},
            metadata=metadata or {}
        )
    
    def _compute_plane_tension(self, tw_state: TWState) -> Dict[str, float]:
        """
        Compute tension level for each plane based on vector scores.
        
        Tension is derived from:
        - Magnitude of vector scores (energy)
        - Variance of scores (instability)
        
        Args:
            tw_state: Current TW state
            
        Returns:
            Dict with tension values for planes '3', '6', '9'
        """
        def calc_tension(scores: Dict[str, float]) -> float:
            if not scores:
                return 0.0
            
            values = list(scores.values())
            # Energy: mean absolute value
            energy = sum(abs(v) for v in values) / len(values)
            
            # Instability: variance
            mean_val = sum(values) / len(values)
            variance = sum((v - mean_val) ** 2 for v in values) / len(values)
            instability = math.sqrt(variance)
            
            # Combined tension (weighted)
            tension = 0.6 * energy + 0.4 * instability
            return float(tension)
        
        t3 = calc_tension(tw_state.plane3_cultural_macro or {})
        t6 = calc_tension(tw_state.plane6_semiotic_media or {})
        t9 = calc_tension(tw_state.plane9_structural_systemic or {})
        
        return {"3": t3, "6": t6, "9": t9}
    
    def _compute_severity_factor(self, tw_state: TWState) -> float:
        """
        Compute global severity factor based on overall system tension.
        
        Uses Tracy-Widom-inspired normalization to map tension to [0, 1].
        
        Args:
            tw_state: Current TW state
            
        Returns:
            Severity factor in range [0, 1]
        """
        tensions = self._compute_plane_tension(tw_state)
        
        # Global instability index (mean tension)
        mean_tension = (tensions["3"] + tensions["6"] + tensions["9"]) / 3.0
        
        # Tracy-Widom-like normalization using exponential decay
        # Maps [0, ∞) → [0, 1)
        severity = 1.0 - math.exp(-mean_tension)
        
        return float(max(0.0, min(1.0, severity)))
    
    def compute_drift(self, tw_state: TWState) -> Dict[str, float]:
        """
        Computes the temporal drift based on the TW state.
        
        Drift represents energy/symbolic flow between planes:
        - plane3_to_6: Surface → Tension (cultural forces creating tension)
        - plane6_to_9: Tension → Structure (tension crystallizing into structure)
        - plane9_to_3: Structure → Surface (structure manifesting at surface)
        
        Drift values are in range approximately [-1.0, 1.0]:
        - Positive: flow from source to target plane
        - Negative: resistance/backflow
        
        Args:
            tw_state: Current TW state with all plane inputs
            
        Returns:
            Dict mapping drift dimensions to values
        """
        # Compute tensions for each plane
        tensions = self._compute_plane_tension(tw_state)
        t3, t6, t9 = tensions["3"], tensions["6"], tensions["9"]
        
        # Compute global severity factor
        severity = self._compute_severity_factor(tw_state)
        
        # Calculate tension gradients (difference drives flow)
        g_3_6 = t6 - t3  # Gradient from plane 3 to 6
        g_6_9 = t9 - t6  # Gradient from plane 6 to 9
        g_9_3 = t3 - t9  # Gradient from plane 9 to 3 (feedback loop)
        
        # Normalization factor to keep drift in reasonable range
        # Use max to avoid division by zero
        k = max(1.0, abs(g_3_6) + abs(g_6_9) + abs(g_9_3))
        
        # Compute normalized drift with severity modulation
        drift = {
            "plane3_to_6": (g_3_6 / k) * severity,
            "plane6_to_9": (g_6_9 / k) * severity,
            "plane9_to_3": (g_9_3 / k) * severity,
        }
        
        return drift
    
    def evolve(
        self,
        tw_state: TWState,
        delta144_distribution: Dict[str, float],
        time_steps: int = 1,
        step_size: float = 1.0
    ) -> Dict[str, float]:
        """
        Evolves the Δ144 distribution over time using TW369 dynamics.
        
        Applies drift incrementally to modulate archetype probabilities based on
        which plane they belong to.
        
        Args:
            tw_state: Current TW state
            delta144_distribution: Current archetype distribution
            time_steps: Number of discrete time steps to evolve
            step_size: Size of each time step (default: 1.0)
            
        Returns:
            Evolved Δ144 distribution
        """
        current_dist = delta144_distribution.copy()
        
        for _ in range(max(1, time_steps)):
            # Compute current drift
            drift = self.compute_drift(tw_state)
            
            # Convert drift to multiplicative factors per plane
            # Positive drift into a plane increases its states
            # Drift is scaled by step_size and dampened by 0.5 for stability
            factors = {
                "3": 1.0 + drift["plane9_to_3"] * 0.5 * step_size,  # Feedback from 9→3
                "6": 1.0 + drift["plane3_to_6"] * 0.5 * step_size,  # Flow from 3→6
                "9": 1.0 + drift["plane6_to_9"] * 0.5 * step_size,  # Flow from 6→9
            }
            
            # Clamp factors to prevent negative values
            for plane in factors:
                factors[plane] = max(0.1, factors[plane])  # Minimum 0.1 to avoid collapse
            
            # Apply factors to distribution based on state-plane mapping
            new_dist = {}
            for state_id, value in current_dist.items():
                # Get plane for this state (default to plane 6 if unmapped)
                plane = self._state_plane_mapping.get(state_id, "6")
                factor = factors.get(plane, 1.0)
                
                # Apply factor
                new_val = max(0.0, float(value) * factor)
                new_dist[state_id] = new_val
            
            # Normalize distribution to maintain probability sum
            total = sum(new_dist.values())
            if total > 0:
                for state_id in new_dist:
                    new_dist[state_id] /= total
            
            current_dist = new_dist
        
        return current_dist
    
    def load_config(self, path="schema/tw369/tw369_default_config.json"):
        """
        Load TW369 engine configuration from file.
        
        Validates configuration against tw369_config_schema.json and
        stores it for runtime use.
        
        Args:
            path: Path to configuration JSON file
            
        Returns:
            Validated configuration dict
            
        Raises:
            jsonschema.ValidationError: If config is invalid
            FileNotFoundError: If config file doesn't exist
        """
        from .config_loader import TW369ConfigLoader
        
        loader = TW369ConfigLoader()
        self.config = loader.load(path)
        return self.config


