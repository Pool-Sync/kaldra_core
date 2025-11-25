"""
Integration tests for TW369 drift mathematics implementation.

Tests the complete drift calculation and temporal evolution functionality.
"""

import math
import pytest
from src.tw369.tw369_integration import TW369Integrator, TWState


class TestTW369DriftMathematics:
    """Test suite for TW369 drift mathematics (Modelo A)."""
    
    def test_compute_drift_with_empty_state(self):
        """Test drift computation with empty TWState."""
        integrator = TW369Integrator()
        tw_state = TWState()
        
        drift = integrator.compute_drift(tw_state)
        
        # Should return valid drift structure
        assert "plane3_to_6" in drift
        assert "plane6_to_9" in drift
        assert "plane9_to_3" in drift
        
        # All values should be 0 for empty state
        assert drift["plane3_to_6"] == 0.0
        assert drift["plane6_to_9"] == 0.0
        assert drift["plane9_to_3"] == 0.0
    
    def test_compute_drift_with_scores(self):
        """Test drift computation with actual scores."""
        integrator = TW369Integrator()
        tw_state = TWState(
            plane3_cultural_macro={"E01": 0.5, "S09": -0.3},
            plane6_semiotic_media={"E01": 0.4, "S09": 0.2},
            plane9_structural_systemic={"E01": 0.6, "S09": -0.4}
        )
        
        drift = integrator.compute_drift(tw_state)
        
        # Drift values should be in reasonable range
        assert -1.0 <= drift["plane3_to_6"] <= 1.0
        assert -1.0 <= drift["plane6_to_9"] <= 1.0
        assert -1.0 <= drift["plane9_to_3"] <= 1.0
        
        # At least one drift should be non-zero
        assert any(abs(v) > 0 for v in drift.values())
    
    def test_plane_tension_calculation(self):
        """Test internal plane tension calculation."""
        integrator = TW369Integrator()
        tw_state = TWState(
            plane3_cultural_macro={"E01": 0.8, "S09": 0.6},
            plane6_semiotic_media={"E01": 0.2, "S09": 0.1},
            plane9_structural_systemic={"E01": 0.5, "S09": 0.5}
        )
        
        tensions = integrator._compute_plane_tension(tw_state)
        
        # Should have all three planes
        assert "3" in tensions
        assert "6" in tensions
        assert "9" in tensions
        
        # All tensions should be non-negative
        assert tensions["3"] >= 0
        assert tensions["6"] >= 0
        assert tensions["9"] >= 0
        
        # Plane 3 should have higher tension (higher scores)
        assert tensions["3"] > tensions["6"]
    
    def test_severity_factor_calculation(self):
        """Test severity factor computation."""
        integrator = TW369Integrator()
        
        # Low tension state
        low_state = TWState(
            plane3_cultural_macro={"E01": 0.1},
            plane6_semiotic_media={"E01": 0.1},
            plane9_structural_systemic={"E01": 0.1}
        )
        
        # High tension state
        high_state = TWState(
            plane3_cultural_macro={"E01": 0.9, "S09": 0.8, "P17": 0.7},
            plane6_semiotic_media={"E01": 0.9, "S09": 0.8, "P17": 0.7},
            plane9_structural_systemic={"E01": 0.9, "S09": 0.8, "P17": 0.7}
        )
        
        low_severity = integrator._compute_severity_factor(low_state)
        high_severity = integrator._compute_severity_factor(high_state)
        
        # Severity should be in [0, 1]
        assert 0.0 <= low_severity <= 1.0
        assert 0.0 <= high_severity <= 1.0
        
        # High tension should have higher severity
        assert high_severity > low_severity
    
    def test_evolve_maintains_distribution_sum(self):
        """Test that evolve() maintains probability distribution sum."""
        integrator = TW369Integrator()
        tw_state = TWState(
            plane3_cultural_macro={"E01": 0.5},
            plane6_semiotic_media={"E01": 0.3},
            plane9_structural_systemic={"E01": 0.7}
        )
        
        # Create initial distribution
        initial_dist = {
            "Lover": 0.2,
            "Hero": 0.3,
            "Sage": 0.5
        }
        
        # Evolve
        evolved = integrator.evolve(tw_state, initial_dist, time_steps=5)
        
        # Sum should still be ~1.0
        total = sum(evolved.values())
        assert abs(total - 1.0) < 0.01
    
    def test_evolve_changes_distribution(self):
        """Test that evolve() actually changes the distribution."""
        integrator = TW369Integrator()
        tw_state = TWState(
            plane3_cultural_macro={"E01": 0.8, "S09": 0.6},
            plane6_semiotic_media={"E01": 0.2, "S09": 0.1},
            plane9_structural_systemic={"E01": 0.5, "S09": 0.5}
        )
        
        initial_dist = {
            "Lover": 0.33,
            "Hero": 0.33,
            "Sage": 0.34
        }
        
        # Evolve with multiple steps
        evolved = integrator.evolve(tw_state, initial_dist, time_steps=10)
        
        # Distribution should change
        changes = sum(1 for k in evolved if abs(evolved[k] - initial_dist[k]) > 0.01)
        assert changes > 0, "Distribution should change after evolution"
    
    def test_evolve_with_step_size(self):
        """Test evolve() with different step sizes."""
        integrator = TW369Integrator()
        tw_state = TWState(
            plane3_cultural_macro={"E01": 0.7},
            plane6_semiotic_media={"E01": 0.3},
            plane9_structural_systemic={"E01": 0.5}
        )
        
        initial_dist = {"Lover": 0.5, "Hero": 0.3, "Sage": 0.2}
        
        # Small step size
        evolved_small = integrator.evolve(tw_state, initial_dist, time_steps=1, step_size=0.1)
        
        # Large step size
        evolved_large = integrator.evolve(tw_state, initial_dist, time_steps=1, step_size=2.0)
        
        # Larger step size should cause bigger changes
        change_small = sum(abs(evolved_small[k] - initial_dist[k]) for k in initial_dist)
        change_large = sum(abs(evolved_large[k] - initial_dist[k]) for k in initial_dist)
        
        assert change_large > change_small
    
    def test_state_plane_mapping(self):
        """Test that state-plane mapping is initialized correctly."""
        integrator = TW369Integrator()
        
        # Check that mapping exists
        assert hasattr(integrator, '_state_plane_mapping')
        assert isinstance(integrator._state_plane_mapping, dict)
        
        # Check some expected mappings
        assert integrator._state_plane_mapping.get("Lover") == "3"  # Plane 3
        assert integrator._state_plane_mapping.get("Hero") == "6"   # Plane 6
        assert integrator._state_plane_mapping.get("Sage") == "9"   # Plane 9
    
    def test_drift_gradient_direction(self):
        """Test that drift gradients point in expected direction."""
        integrator = TW369Integrator()
        
        # Create state with clear gradient: Plane 3 low, Plane 6 high, Plane 9 medium
        tw_state = TWState(
            plane3_cultural_macro={"E01": 0.1},
            plane6_semiotic_media={"E01": 0.9, "S09": 0.8},
            plane9_structural_systemic={"E01": 0.5}
        )
        
        drift = integrator.compute_drift(tw_state)
        
        # Plane 3→6: Should be positive (6 has higher tension)
        assert drift["plane3_to_6"] > 0
        
        # Plane 6→9: Should be negative (6 has higher tension than 9)
        assert drift["plane6_to_9"] < 0
    
    def test_evolve_stability(self):
        """Test that evolve() doesn't produce NaN or inf values."""
        integrator = TW369Integrator()
        tw_state = TWState(
            plane3_cultural_macro={"E01": 1.0, "S09": -1.0},
            plane6_semiotic_media={"E01": 0.5},
            plane9_structural_systemic={"E01": 0.0}
        )
        
        initial_dist = {"Lover": 0.5, "Hero": 0.3, "Sage": 0.2}
        
        # Evolve many steps
        evolved = integrator.evolve(tw_state, initial_dist, time_steps=100, step_size=1.0)
        
        # Check for numerical stability
        for value in evolved.values():
            assert not math.isnan(value), "Distribution contains NaN"
            assert not math.isinf(value), "Distribution contains inf"
            assert value >= 0, "Distribution contains negative values"


if __name__ == "__main__":
    import math
    
    # Run tests
    test = TestTW369DriftMathematics()
    
    print("\n" + "="*60)
    print("TW369 DRIFT MATHEMATICS TESTS")
    print("="*60 + "\n")
    
    test.test_compute_drift_with_empty_state()
    print("✅ Empty state drift")
    
    test.test_compute_drift_with_scores()
    print("✅ Drift with scores")
    
    test.test_plane_tension_calculation()
    print("✅ Plane tension calculation")
    
    test.test_severity_factor_calculation()
    print("✅ Severity factor calculation")
    
    test.test_evolve_maintains_distribution_sum()
    print("✅ Distribution sum maintained")
    
    test.test_evolve_changes_distribution()
    print("✅ Distribution changes")
    
    test.test_evolve_with_step_size()
    print("✅ Step size effects")
    
    test.test_state_plane_mapping()
    print("✅ State-plane mapping")
    
    test.test_drift_gradient_direction()
    print("✅ Drift gradient direction")
    
    test.test_evolve_stability()
    print("✅ Numerical stability")
    
    print("\n" + "="*60)
    print("✅ ALL TW369 DRIFT TESTS PASSED")
    print("="*60)
