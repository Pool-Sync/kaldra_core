"""
Tests for Polarity Loading and Kindra Hooks (v2.7).
"""
import pytest
from src.archetypes.polarity_mapping import extract_polarity_scores
from src.kindras.layer1_cultural_macro_scoring import KindraLayer1CulturalMacroScoring
from src.kindras.layer2_semiotic_media_scoring import KindraLayer2SemioticMediaScoring

def test_polarity_loading_structure():
    """Test that we can load/define polarities correctly."""
    # Since we don't have a direct loader file exposed in the prompt list, 
    # we verify the mapping logic which relies on the definitions.
    
    # Mock meta-results
    meta_results = {
        "nietzsche": {
            "scores": {"dionysian_force": 0.9, "apollonian_order": 0.1},
            "dominant_axes": ["dionysian_force"]
        },
        "aurelius": {
            "scores": {"control_dichotomy": 0.8},
            "alignment": 0.8
        }
    }
    
    scores = extract_polarity_scores(meta_results)
    assert "POL_ORDER_CHAOS" in scores
    # High Dionysian -> High Chaos (Low Order, so closer to 0.0)
    assert scores["POL_ORDER_CHAOS"] < 0.4

def test_kindra_layer1_hook():
    """Test Layer 1 adjustment with polarities."""
    scorer = KindraLayer1CulturalMacroScoring()
    
    base_scores = {"tradition_val": 0.5, "disruption_val": 0.5}
    
    # Case 1: High Chaos boosts disruption
    polarities_chaos = {"POL_ORDER_CHAOS": 0.9}
    adj_chaos = scorer.adjust_l1_with_polarities(base_scores, polarities_chaos)
    assert adj_chaos["disruption_val"] > 0.5
    assert adj_chaos["tradition_val"] == 0.5
    
    # Case 2: High Tradition boosts tradition
    polarities_trad = {"POL_TRADITION_INNOVATION": 0.1} # Low score = Tradition
    adj_trad = scorer.adjust_l1_with_polarities(base_scores, polarities_trad)
    assert adj_trad["tradition_val"] > 0.5

def test_kindra_layer2_hook():
    """Test Layer 2 adjustment with modifiers."""
    scorer = KindraLayer2SemioticMediaScoring()
    
    base_scores = {"aggressive_tone": 0.5, "calm_tone": 0.5}
    
    # Case: Aggressive modifier active
    modifiers = {"MOD_AGGRESSIVE": 0.8}
    adj = scorer.adjust_l2_with_modifiers(base_scores, modifiers)
    
    # Should boost 'aggressive_tone' because 'aggressive' is in the key
    assert adj["aggressive_tone"] > 0.5
    assert adj["calm_tone"] == 0.5
