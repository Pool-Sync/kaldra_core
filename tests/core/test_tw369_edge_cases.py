import pytest
import numpy as np
from src.tw369.tw369_integration import TW369Integrator, TWState

@pytest.fixture
def integrator():
    return TW369Integrator()

def test_tw369_zero_state(integrator):
    """Test drift calculation with all-zero state."""
    state = TWState(
        plane3_cultural_macro={},
        plane6_semiotic_media={},
        plane9_structural_systemic={}
    )
    drift = integrator.compute_drift(state)
    
    # Should handle zero state without errors
    assert isinstance(drift, dict)
    assert len(drift) > 0
    for val in drift.values():
        assert not np.isnan(val)
        assert not np.isinf(val)

def test_tw369_extreme_values(integrator):
    """Test drift calculation with boundary plane values."""
    state = TWState(
        plane3_cultural_macro={"E01": 1.0, "E02": 1.0},
        plane6_semiotic_media={"S01": -1.0},
        plane9_structural_systemic={"T01": 1.0}
    )
    drift = integrator.compute_drift(state)
    
    # Should handle extreme values gracefully
    assert isinstance(drift, dict)
    for val in drift.values():
        assert not np.isnan(val)
        assert not np.isinf(val)

def test_tw369_mixed_state(integrator):
    """Test drift with mixed positive/negative values."""
    state = TWState(
        plane3_cultural_macro={"E01": 0.5, "E02": -0.3},
        plane6_semiotic_media={"S01": 0.7},
        plane9_structural_systemic={"T01": 0.1, "T02": -0.2}
    )
    drift = integrator.compute_drift(state)
    
    assert isinstance(drift, dict)
    # Drift values should be bounded
    for val in drift.values():
        assert -10.0 <= val <= 10.0
