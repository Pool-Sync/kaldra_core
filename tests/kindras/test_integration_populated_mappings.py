"""
Integration test for Kindra 3×48 system with populated Δ144 mappings.

Tests:
- All 3 layers load correctly
- Mappings are populated
- Sequential application (L1 → L2 → L3)
- Combined effects on Δ144 distribution
- Boost/suppress logic works correctly
"""

import pytest
from src.kindras.layer1_cultural_macro_loader import Layer1Loader
from src.kindras.layer2_semiotic_media_loader import Layer2Loader
from src.kindras.layer3_structural_systemic_loader import Layer3Loader
from src.kindras.layer1_cultural_macro_scoring import Layer1Scorer
from src.kindras.layer2_semiotic_media_scoring import Layer2Scorer
from src.kindras.layer3_structural_systemic_scoring import Layer3Scorer
from src.kindras.layer1_delta144_bridge import Layer1Delta144Bridge
from src.kindras.layer2_delta144_bridge import Layer2Delta144Bridge
from src.kindras.layer3_delta144_bridge import Layer3Delta144Bridge


class TestKindraIntegration:
    """Integration tests for complete Kindra 3×48 system."""

    def test_all_mappings_populated(self):
        """Verify all 144 mappings are populated."""
        l1_bridge = Layer1Delta144Bridge("schema/kindras/kindra_layer1_to_delta144_map.json")
        l2_bridge = Layer2Delta144Bridge("schema/kindras/kindra_layer2_to_delta144_map.json")
        l3_bridge = Layer3Delta144Bridge("schema/kindras/kindra_layer3_to_delta144_map.json")

        # Check Layer 1
        assert len(l1_bridge.mapping) == 48
        for entry in l1_bridge.mapping.values():
            assert len(entry["boost"]) >= 2, f"Layer 1 {entry['id']} has < 2 boost"
            assert len(entry["suppress"]) >= 2, f"Layer 1 {entry['id']} has < 2 suppress"

        # Check Layer 2
        assert len(l2_bridge.mapping) == 48
        for entry in l2_bridge.mapping.values():
            assert len(entry["boost"]) >= 2, f"Layer 2 {entry['id']} has < 2 boost"
            assert len(entry["suppress"]) >= 2, f"Layer 2 {entry['id']} has < 2 suppress"

        # Check Layer 3
        assert len(l3_bridge.mapping) == 48
        for entry in l3_bridge.mapping.values():
            assert len(entry["boost"]) >= 2, f"Layer 3 {entry['id']} has < 2 boost"
            assert len(entry["suppress"]) >= 2, f"Layer 3 {entry['id']} has < 2 suppress"

        print("✅ All 144 mappings populated with 2+ boost/suppress")

    def test_sequential_layer_application(self):
        """Test sequential application of all 3 layers."""
        # Initialize loaders
        l1_loader = Layer1Loader("schema/kindras/kindra_vectors_layer1_cultural_macro_48.json")
        l2_loader = Layer2Loader("schema/kindras/kindra_vectors_layer2_semiotic_media_48.json")
        l3_loader = Layer3Loader("schema/kindras/kindra_vectors_layer3_structural_systemic_48.json")

        # Initialize scorers
        l1_scorer = Layer1Scorer()
        l2_scorer = Layer2Scorer()
        l3_scorer = Layer3Scorer()

        # Initialize bridges
        l1_bridge = Layer1Delta144Bridge("schema/kindras/kindra_layer1_to_delta144_map.json")
        l2_bridge = Layer2Delta144Bridge("schema/kindras/kindra_layer2_to_delta144_map.json")
        l3_bridge = Layer3Delta144Bridge("schema/kindras/kindra_layer3_to_delta144_map.json")

        # Base Δ144 distribution (using archetype names)
        archetypes = [
            "Innocent", "Orphan", "Hero", "Caregiver", "Explorer", "Rebel",
            "Lover", "Creator", "Jester", "Sage", "Magician", "Ruler",
            "Everyman", "Outlaw", "Trickster", "Judge", "Guardian", "Hermit"
        ]
        base_dist = {arch: 1.0 for arch in archetypes}

        # Context with overrides for testing
        context = {
            "layer1_overrides": {"E01": 0.5, "S09": -0.3},
            "layer2_overrides": {"E01": 0.4, "S09": 0.2},
            "layer3_overrides": {"E01": 0.6, "S09": -0.4}
        }

        # Layer 1 application
        l1_scores = l1_scorer.score(context, l1_loader.get_all_vectors())
        dist_after_l1 = l1_bridge.apply(base_dist, l1_scores)

        # Layer 2 application
        l2_scores = l2_scorer.score(context, l2_loader.get_all_vectors())
        dist_after_l2 = l2_bridge.apply(dist_after_l1, l2_scores)

        # Layer 3 application
        l3_scores = l3_scorer.score(context, l3_loader.get_all_vectors())
        dist_after_l3 = l3_bridge.apply(dist_after_l2, l3_scores)

        # Validate distributions
        assert len(dist_after_l1) == len(archetypes)
        assert len(dist_after_l2) == len(archetypes)
        assert len(dist_after_l3) == len(archetypes)

        # All values should be non-negative
        assert all(v >= 0 for v in dist_after_l1.values())
        assert all(v >= 0 for v in dist_after_l2.values())
        assert all(v >= 0 for v in dist_after_l3.values())

        # Distribution should change from base
        assert dist_after_l1 != base_dist, "Layer 1 had no effect"
        assert dist_after_l2 != dist_after_l1, "Layer 2 had no effect"
        assert dist_after_l3 != dist_after_l2, "Layer 3 had no effect"

        print("✅ Sequential layer application works correctly")

    def test_boost_suppress_effects(self):
        """Test that boost/suppress logic actually affects distribution."""
        # Test Layer 1 E01 mapping
        l1_bridge = Layer1Delta144Bridge("schema/kindras/kindra_layer1_to_delta144_map.json")

        # Get E01 mapping (should boost Lover, Jester; suppress Sage, Hermit)
        e01_mapping = l1_bridge.mapping["E01"]
        assert "Lover" in e01_mapping["boost"]
        assert "Jester" in e01_mapping["boost"]
        assert "Sage" in e01_mapping["suppress"]
        assert "Hermit" in e01_mapping["suppress"]

        # Create simple distribution
        base_dist = {
            "Lover": 1.0,
            "Jester": 1.0,
            "Sage": 1.0,
            "Hermit": 1.0,
            "Hero": 1.0
        }

        # Apply positive score for E01
        scores = {"E01": 0.5}
        adjusted = l1_bridge.apply(base_dist, scores)

        # Boosted archetypes should increase
        assert adjusted["Lover"] > base_dist["Lover"], "Lover not boosted"
        assert adjusted["Jester"] > base_dist["Jester"], "Jester not boosted"

        # Suppressed archetypes should decrease
        assert adjusted["Sage"] < base_dist["Sage"], "Sage not suppressed"
        assert adjusted["Hermit"] < base_dist["Hermit"], "Hermit not suppressed"

        # Unaffected archetype should stay same
        assert adjusted["Hero"] == base_dist["Hero"], "Hero affected unexpectedly"

        print("✅ Boost/suppress logic works correctly")

    def test_negative_score_inversion(self):
        """Test that negative scores invert boost/suppress."""
        l1_bridge = Layer1Delta144Bridge("schema/kindras/kindra_layer1_to_delta144_map.json")

        base_dist = {
            "Lover": 1.0,
            "Jester": 1.0,
            "Sage": 1.0,
            "Hermit": 1.0
        }

        # Apply negative score for E01 (should invert: suppress Lover/Jester, boost Sage/Hermit)
        scores = {"E01": -0.5}
        adjusted = l1_bridge.apply(base_dist, scores)

        # Originally boosted should now be suppressed
        assert adjusted["Lover"] < base_dist["Lover"], "Lover not suppressed with negative score"
        assert adjusted["Jester"] < base_dist["Jester"], "Jester not suppressed with negative score"

        # Originally suppressed should now be boosted
        assert adjusted["Sage"] > base_dist["Sage"], "Sage not boosted with negative score"
        assert adjusted["Hermit"] > base_dist["Hermit"], "Hermit not boosted with negative score"

        print("✅ Negative score inversion works correctly")

    def test_combined_layer_effects(self):
        """Test combined effects of all 3 layers on same archetypes."""
        l1_bridge = Layer1Delta144Bridge("schema/kindras/kindra_layer1_to_delta144_map.json")
        l2_bridge = Layer2Delta144Bridge("schema/kindras/kindra_layer2_to_delta144_map.json")
        l3_bridge = Layer3Delta144Bridge("schema/kindras/kindra_layer3_to_delta144_map.json")

        # Start with uniform distribution using real archetype names
        archetypes = [
            "Innocent", "Orphan", "Hero", "Caregiver", "Explorer", "Rebel",
            "Lover", "Creator", "Jester", "Sage", "Magician", "Ruler"
        ]
        base_dist = {arch: 1.0 for arch in archetypes}

        # Apply same vector across all layers with different scores
        l1_scores = {"E01": 0.3}
        l2_scores = {"E01": 0.4}
        l3_scores = {"E01": 0.5}

        dist_l1 = l1_bridge.apply(base_dist, l1_scores)
        dist_l2 = l2_bridge.apply(dist_l1, l2_scores)
        dist_l3 = l3_bridge.apply(dist_l2, l3_scores)

        # Final distribution should have different values from base
        # Check that at least some values changed
        changes = sum(1 for k in dist_l3 if dist_l3[k] != base_dist[k])
        assert changes > 0, "No changes detected in distribution"

        print("✅ Combined layer effects work correctly")

    def test_all_vectors_have_valid_archetypes(self):
        """Verify all boost/suppress entries reference valid archetypes."""
        valid_archetypes = {
            "Innocent", "Orphan", "Hero", "Caregiver", "Explorer", "Rebel",
            "Lover", "Creator", "Jester", "Sage", "Magician", "Ruler",
            "Everyman", "Outlaw", "Trickster", "Judge", "Guardian", "Hermit"
        }

        for layer_num, path in enumerate([
            "schema/kindras/kindra_layer1_to_delta144_map.json",
            "schema/kindras/kindra_layer2_to_delta144_map.json",
            "schema/kindras/kindra_layer3_to_delta144_map.json"
        ], 1):
            if layer_num == 1:
                bridge = Layer1Delta144Bridge(path)
            elif layer_num == 2:
                bridge = Layer2Delta144Bridge(path)
            else:
                bridge = Layer3Delta144Bridge(path)

            for entry in bridge.mapping.values():
                for archetype in entry["boost"]:
                    assert archetype in valid_archetypes, \
                        f"Layer {layer_num} {entry['id']} has invalid boost: {archetype}"
                for archetype in entry["suppress"]:
                    assert archetype in valid_archetypes, \
                        f"Layer {layer_num} {entry['id']} has invalid suppress: {archetype}"

        print("✅ All archetypes are valid")


if __name__ == "__main__":
    # Run tests
    test = TestKindraIntegration()
    
    print("\n" + "="*60)
    print("KINDRA 3×48 INTEGRATION TESTS")
    print("="*60 + "\n")
    
    test.test_all_mappings_populated()
    test.test_sequential_layer_application()
    test.test_boost_suppress_effects()
    test.test_negative_score_inversion()
    test.test_combined_layer_effects()
    test.test_all_vectors_have_valid_archetypes()
    
    print("\n" + "="*60)
    print("✅ ALL INTEGRATION TESTS PASSED")
    print("="*60)
