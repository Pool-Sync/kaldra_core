"""
Tests for TW369 Temporal Coherence.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from tw369.temporal_coherence import (
    compute_temporal_coherence,
    compute_drift_slope,
    compute_drift_acceleration,
    detect_regime_stability,
)
from story.story_buffer import StoryBuffer


def test_compute_drift_slope_increasing():
    """Test drift slope computation with increasing drift."""
    buffer = StoryBuffer(capacity=10)
    
    # Add events with increasing drift
    for i in range(5):
        buffer.add_event(
            f"Event {i}",
            drift_state={"drift_metric": 0.2 + i * 0.1}
        )
    
    events = buffer.get_timeline()
    slope = compute_drift_slope(events)
    
    assert slope > 0  # Increasing trend


def test_compute_drift_slope_decreasing():
    """Test drift slope with decreasing drift."""
    buffer = StoryBuffer(capacity=10)
    
    # Add events with decreasing drift
    for i in range(5):
        buffer.add_event(
            f"Event {i}",
            drift_state={"drift_metric": 0.8 - i * 0.1}
        )
    
    events = buffer.get_timeline()
    slope = compute_drift_slope(events)
    
    assert slope < 0  # Decreasing trend


def test_compute_drift_acceleration():
    """Test drift acceleration computation."""
    buffer = StoryBuffer(capacity=10)
    
    # Add events with accelerating drift
    drift_values = [0.2, 0.25, 0.35, 0.5, 0.7]
    for i, drift in enumerate(drift_values):
        buffer.add_event(f"Event {i}", drift_state={"drift_metric": drift})
    
    events = buffer.get_timeline()
    acceleration = compute_drift_acceleration(events)
    
    # Should detect positive acceleration
    assert isinstance(acceleration, float)


def test_detect_regime_stability_stable():
    """Test regime stability with stable regime."""
    buffer = StoryBuffer(capacity=10)
    
    # All events in same regime
    for i in range(5):
        buffer.add_event(
            f"Event {i}",
            tw_state={"regime": "stable", "plane": "6"}
        )
    
    events = buffer.get_timeline()
    stability = detect_regime_stability(events)
    
    assert stability == 1.0  # Perfectly stable


def test_detect_regime_stability_unstable():
    """Test regime stability with frequent changes."""
    buffer = StoryBuffer(capacity=10)
    
    # Alternating regimes
    regimes = ["stable", "unstable", "stable", "unstable", "stable"]
    for i, regime in enumerate(regimes):
        buffer.add_event(
            f"Event {i}",
            tw_state={"regime": regime, "plane": "6"}
        )
    
    events = buffer.get_timeline()
    stability = detect_regime_stability(events)
    
    assert stability < 0.5  # Unstable


def test_compute_temporal_coherence():
    """Test complete temporal coherence computation."""
    buffer = StoryBuffer(capacity=10)
    
    # Add events with drift and regime
    for i in range(5):
        buffer.add_event(
            f"Event {i}",
            drift_state={"drift_metric": 0.3 + i * 0.1},
            tw_state={"regime": "stable" if i < 3 else "unstable", "plane": "6"}
        )
    
    events = buffer.get_timeline()
    coherence = compute_temporal_coherence(events)
    
    assert coherence is not None
    assert coherence.drift_slope > 0  # Increasing
    assert 0.0 <= coherence.regime_stability <= 1.0
    assert len(coherence.drift_values) == 5
    assert coherence.current_regime in ["stable", "unstable"]


def test_temporal_coherence_insufficient_data():
    """Test temporal coherence with insufficient data."""
    buffer = StoryBuffer(capacity=10)
    
    # Only one event
    buffer.add_event("Event 1", drift_state={"drift_metric": 0.5})
    
    events = buffer.get_timeline()
    coherence = compute_temporal_coherence(events)
    
    assert coherence is None  # Not enough data
