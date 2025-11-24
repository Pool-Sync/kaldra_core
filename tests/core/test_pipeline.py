"""
Tests for KALDRA Engine Pipeline
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from core.kaldra_engine_pipeline import KALDRAEnginePipeline


class TestKALDRAEnginePipeline:
    def test_pipeline_initialization(self):
        """Test that pipeline initializes all components."""
        pipeline = KALDRAEnginePipeline(schema_base_path="schema/kindras")
        
        assert pipeline.l1_loader is not None
        assert pipeline.l2_loader is not None
        assert pipeline.l3_loader is not None
        assert pipeline.l1_scorer is not None
        assert pipeline.l2_scorer is not None
        assert pipeline.l3_scorer is not None
        assert pipeline.l1_bridge is not None
        assert pipeline.l2_bridge is not None
        assert pipeline.l3_bridge is not None
        assert pipeline.tw369 is not None
    
    def test_pipeline_process(self):
        """Test complete pipeline execution."""
        pipeline = KALDRAEnginePipeline(schema_base_path="schema/kindras")
        
        # Create a simple base Δ144 distribution
        base_delta144 = {f"STATE_{i:03d}": 1.0 for i in range(144)}
        
        # Create context with some overrides
        context = {
            "layer1_overrides": {"E01": 0.5},
            "layer2_overrides": {"S09": 0.3},
            "layer3_overrides": {"P17": -0.2},
        }
        
        # Run pipeline
        result = pipeline.process(base_delta144, context, evolve_steps=0)
        
        # Verify result structure
        assert "final_distribution" in result
        assert "layer1_scores" in result
        assert "layer2_scores" in result
        assert "layer3_scores" in result
        assert "intermediate_distributions" in result
        assert "tw_state" in result
        
        # Verify scores
        assert result["layer1_scores"]["E01"] == 0.5
        assert result["layer2_scores"]["S09"] == 0.3
        assert result["layer3_scores"]["P17"] == -0.2
        
        # Verify intermediate distributions exist
        assert "base" in result["intermediate_distributions"]
        assert "after_layer1" in result["intermediate_distributions"]
        assert "after_layer2" in result["intermediate_distributions"]
        assert "after_layer3" in result["intermediate_distributions"]
    
    def test_pipeline_with_evolution(self):
        """Test pipeline with TW369 evolution."""
        pipeline = KALDRAEnginePipeline(schema_base_path="schema/kindras")
        
        base_delta144 = {f"STATE_{i:03d}": 1.0 for i in range(144)}
        context = {}
        
        # Run with evolution
        result = pipeline.process(base_delta144, context, evolve_steps=5)
        
        assert result["final_distribution"] is not None
        # Evolution is currently a placeholder, so distribution should be unchanged
        # This test validates the interface works
