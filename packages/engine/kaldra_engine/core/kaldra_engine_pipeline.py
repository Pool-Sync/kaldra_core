"""
KALDRA Engine Pipeline

Orchestrates the complete flow:
1. Load Kindra vectors (L1, L2, L3)
2. Score vectors based on context
3. Apply bridges to Δ144 distribution
4. Integrate with TW369 for temporal evolution
"""

import os
from typing import Dict, Any, Optional

# Kindra Loaders
from kindras.layer1_cultural_macro_loader import Layer1Loader
from kindras.layer2_semiotic_media_loader import Layer2Loader
from kindras.layer3_structural_systemic_loader import Layer3Loader

# Kindra Scorers
from kindras.layer1_cultural_macro_scoring import Layer1Scorer
from kindras.layer2_semiotic_media_scoring import Layer2Scorer
from kindras.layer3_structural_systemic_scoring import Layer3Scorer

# Kindra Bridges
from kindras.layer1_delta144_bridge import Layer1Delta144Bridge
from kindras.layer2_delta144_bridge import Layer2Delta144Bridge
from kindras.layer3_delta144_bridge import Layer3Delta144Bridge

# TW369
from tw369.tw369_integration import TW369Integrator


class KALDRAEnginePipeline:
    """
    Main orchestrator for the KALDRA engine with full Kindra 3x48 integration.
    """
    
    def __init__(self, schema_base_path: str = "schema/kindras"):
        """
        Initialize the pipeline with all necessary components.
        
        Args:
            schema_base_path: Base path to Kindra schema files
        """
        self.schema_base = schema_base_path
        
        # Initialize Loaders
        self.l1_loader = Layer1Loader(
            os.path.join(schema_base_path, "kindra_vectors_layer1_cultural_macro_48.json")
        )
        self.l2_loader = Layer2Loader(
            os.path.join(schema_base_path, "kindra_vectors_layer2_semiotic_media_48.json")
        )
        self.l3_loader = Layer3Loader(
            os.path.join(schema_base_path, "kindra_vectors_layer3_structural_systemic_48.json")
        )
        
        # Initialize Scorers
        self.l1_scorer = Layer1Scorer()
        self.l2_scorer = Layer2Scorer()
        self.l3_scorer = Layer3Scorer()
        
        # Initialize Bridges
        self.l1_bridge = Layer1Delta144Bridge(
            os.path.join(schema_base_path, "kindra_layer1_to_delta144_map.json")
        )
        self.l2_bridge = Layer2Delta144Bridge(
            os.path.join(schema_base_path, "kindra_layer2_to_delta144_map.json")
        )
        self.l3_bridge = Layer3Delta144Bridge(
            os.path.join(schema_base_path, "kindra_layer3_to_delta144_map.json")
        )
        
        # Initialize TW369 Integrator
        self.tw369 = TW369Integrator()
    
    def process(
        self,
        base_delta144: Dict[str, float],
        context: Dict[str, Any],
        evolve_steps: int = 0
    ) -> Dict[str, Any]:
        """
        Execute the complete KALDRA pipeline.
        
        Args:
            base_delta144: Initial Δ144 distribution {state_id: probability}
            context: Context dictionary with cultural/media/structural data
            evolve_steps: Number of TW369 evolution steps (0 = no evolution)
            
        Returns:
            Dict containing:
                - final_distribution: Final Δ144 after all transformations
                - layer1_scores: L1 vector scores
                - layer2_scores: L2 vector scores
                - layer3_scores: L3 vector scores
                - intermediate_distributions: Dict of distributions at each stage
        """
        
        # Step 1: Score all Kindra layers
        l1_scores = self.l1_scorer.score(context, self.l1_loader.get_all_vectors())
        l2_scores = self.l2_scorer.score(context, self.l2_loader.get_all_vectors())
        l3_scores = self.l3_scorer.score(context, self.l3_loader.get_all_vectors())
        
        # Step 2: Apply Layer 1 (Cultural Macro)
        dist_after_l1 = self.l1_bridge.apply(base_delta144, l1_scores)
        
        # Step 3: Apply Layer 2 (Semiotic/Media)
        dist_after_l2 = self.l2_bridge.apply(dist_after_l1, l2_scores)
        
        # Step 4: Apply Layer 3 (Structural/Systemic)
        dist_after_l3 = self.l3_bridge.apply(dist_after_l2, l3_scores)
        
        # Step 5: TW369 Integration and Evolution
        tw_state = self.tw369.create_state(
            layer1_scores=l1_scores,
            layer2_scores=l2_scores,
            layer3_scores=l3_scores,
            metadata=context
        )
        
        final_distribution = dist_after_l3
        if evolve_steps > 0:
            final_distribution = self.tw369.evolve(tw_state, dist_after_l3, evolve_steps)
        
        # Return complete results
        return {
            "final_distribution": final_distribution,
            "layer1_scores": l1_scores,
            "layer2_scores": l2_scores,
            "layer3_scores": l3_scores,
            "intermediate_distributions": {
                "base": base_delta144,
                "after_layer1": dist_after_l1,
                "after_layer2": dist_after_l2,
                "after_layer3": dist_after_l3,
            },
            "tw_state": tw_state
        }
