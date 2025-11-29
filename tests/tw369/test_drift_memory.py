"""
Tests for DriftState and DriftMemory.
"""

import pytest
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from tw369.drift_state import DriftState
from tw369.drift_memory import DriftMemory


def test_drift_state_serialization_roundtrip():
    """Test that DriftState can be serialized and deserialized."""
    state = DriftState(
        timestamp=1234567890.0,
        plane_values={"3": 0.3, "6": 0.5, "9": 0.2},
        drift_metric=0.42,
        painleve_coherence=0.85,
        regime="A07_RULER"
    )
    
    # to_dict / from_dict
    state_dict = state.to_dict()
    state_restored = DriftState.from_dict(state_dict)
    
    assert state_restored.timestamp == state.timestamp
    assert state_restored.plane_values == state.plane_values
    assert state_restored.drift_metric == state.drift_metric
    assert state_restored.regime == state.regime
    
    # to_json / from_json
    json_str = state.to_json()
    state_from_json = DriftState.from_json(json_str)
    
    assert state_from_json.timestamp == state.timestamp
    assert state_from_json.regime == state.regime


def test_memory_keeps_window_size():
    """Test that DriftMemory respects window size."""
    memory = DriftMemory(window_size=5)
    
    # Add 10 states
    for i in range(10):
        state = DriftState(
            timestamp=float(i),
            drift_metric=float(i) * 0.1,
            regime=f"STATE_{i}"
        )
        memory.append(state)
    
    history = memory.get_history()
    
    # Should only keep last 5
    assert len(history) == 5
    
    # Should be states 5-9
    assert history[0].regime == "STATE_5"
    assert history[-1].regime == "STATE_9"


def test_save_and_load_file():
    """Test saving and loading DriftMemory to/from file."""
    memory = DriftMemory(window_size=3)
    
    # Add some states
    for i in range(3):
        state = DriftState(
            timestamp=float(i),
            drift_metric=float(i) * 0.2,
            regime=f"A0{i+1}_TEST"
        )
        memory.append(state)
    
    # Save to temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "drift_memory.json"
        memory.save(path)
        
        # Load into new memory
        new_memory = DriftMemory()
        new_memory.load(path)
        
        # Verify
        assert new_memory.window_size == 3
        assert len(new_memory.get_history()) == 3
        assert new_memory.get_latest().regime == "A03_TEST"


def test_memory_volatility():
    """Test volatility calculation."""
    memory = DriftMemory(window_size=10)
    
    # Add states with varying drift
    drift_values = [0.1, 0.2, 0.15, 0.25, 0.18]
    for drift in drift_values:
        state = DriftState(drift_metric=drift)
        memory.append(state)
    
    volatility = memory.compute_volatility()
    
    # Should be non-zero
    assert volatility > 0.0
    
    # Should be reasonable (std dev of the values)
    mean = sum(drift_values) / len(drift_values)
    expected_std = (sum((x - mean) ** 2 for x in drift_values) / len(drift_values)) ** 0.5
    
    assert abs(volatility - expected_std) < 0.001


def test_memory_clear():
    """Test clearing memory."""
    memory = DriftMemory(window_size=5)
    
    for i in range(3):
        memory.append(DriftState(drift_metric=float(i)))
    
    assert len(memory.get_history()) == 3
    
    memory.clear()
    
    assert len(memory.get_history()) == 0
    assert memory.get_latest() is None
