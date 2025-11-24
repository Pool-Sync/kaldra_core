"""
Tests for Kindra Scorers and Bridges
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from kindras.layer1_cultural_macro_loader import Layer1Loader
from kindras.layer1_cultural_macro_scoring import Layer1Scorer
from kindras.layer1_delta144_bridge import Layer1Delta144Bridge


class TestScorers:
    def test_layer1_scorer(self):
        """Test Layer 1 scorer with override context."""
        loader = Layer1Loader("schema/kindras/kindra_vectors_layer1_cultural_macro_48.json")
        scorer = Layer1Scorer()
        
        context = {
            "layer1_overrides": {
                "E01": 0.8,
                "S09": -0.5
            }
        }
        
        scores = scorer.score(context, loader.get_all_vectors())
        assert len(scores) == 48
        assert scores["E01"] == 0.8
        assert scores["S09"] == -0.5
        assert scores["E02"] == 0.0  # Default


class TestBridges:
    def test_layer1_bridge_boost(self):
        """Test Layer 1 bridge boost logic."""
        bridge = Layer1Delta144Bridge("schema/kindras/kindra_layer1_to_delta144_map.json")
        
        base_dist = {
            "STATE_A": 1.0,
            "STATE_B": 1.0,
        }
        
        # Manually set a mapping for testing
        bridge.mapping["E01"] = {
            "boost": ["STATE_A"],
            "suppress": ["STATE_B"]
        }
        
        kindra_scores = {"E01": 1.0}  # Full positive score
        
        adjusted = bridge.apply(base_dist, kindra_scores)
        
        # STATE_A should be boosted
        assert adjusted["STATE_A"] > base_dist["STATE_A"]
        # STATE_B should be suppressed
        assert adjusted["STATE_B"] < base_dist["STATE_B"]
    
    def test_layer1_bridge_negative_score(self):
        """Test Layer 1 bridge with negative score (inversion)."""
        bridge = Layer1Delta144Bridge("schema/kindras/kindra_layer1_to_delta144_map.json")
        
        base_dist = {
            "STATE_A": 1.0,
            "STATE_B": 1.0,
        }
        
        bridge.mapping["E01"] = {
            "boost": ["STATE_A"],
            "suppress": ["STATE_B"]
        }
        
        kindra_scores = {"E01": -1.0}  # Negative score inverts logic
        
        adjusted = bridge.apply(base_dist, kindra_scores)
        
        # With negative score, boost/suppress are inverted
        # STATE_B (suppress list) gets boosted
        assert adjusted["STATE_B"] > base_dist["STATE_B"]
        # STATE_A (boost list) gets suppressed
        assert adjusted["STATE_A"] < base_dist["STATE_A"]
