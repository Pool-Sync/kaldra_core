"""
TW369 Temporal Coherence - Temporal drift analysis for KALDRA v2.6.

Extends TW369 with temporal aggregation capabilities for analyzing
drift evolution over narrative timelines.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import statistics

# Import from story module to avoid circular dependency
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class TemporalCoherence:
    """
    Temporal coherence analysis of drift over time.
    """
    drift_slope: float  # Linear regression slope
    drift_acceleration: float  # Second derivative
    drift_volatility: float  # Standard deviation
    regime_stability: float  # How stable the regime is (0-1)
    
    # Trajectory data
    drift_values: List[float]
    timestamps: List[float]
    
    # Regime info
    current_regime: Optional[str] = None
    regime_duration: float = 0.0  # Time in current regime


def compute_temporal_coherence(events: List[Any]) -> Optional[TemporalCoherence]:
    """
    Compute temporal coherence from event timeline.
    
    Args:
        events: List of StoryEvents with drift_state
        
    Returns:
        TemporalCoherence or None if insufficient data
    """
    # Extract drift values and timestamps
    drift_values = []
    timestamps = []
    
    for event in events:
        if hasattr(event, 'drift_state') and event.drift_state:
            drift = event.drift_state.get("drift_metric", 0.0)
            drift_values.append(drift)
            timestamps.append(event.timestamp)
    
    if len(drift_values) < 2:
        return None
    
    # Compute slope
    slope = compute_drift_slope(events)
    
    # Compute acceleration
    acceleration = compute_drift_acceleration(events)
    
    # Compute volatility
    volatility = statistics.stdev(drift_values) if len(drift_values) > 1 else 0.0
    
    # Compute regime stability
    stability = detect_regime_stability(events)
    
    # Detect current regime
    current_regime = None
    regime_duration = 0.0
    
    if events and hasattr(events[-1], 'tw_state') and events[-1].tw_state:
        current_regime = events[-1].tw_state.get("regime")
    
    # Compute regime duration (time in same regime)
    if current_regime:
        regime_start_time = timestamps[-1]
        for i in range(len(events) - 1, -1, -1):
            event = events[i]
            if hasattr(event, 'tw_state') and event.tw_state:
                regime = event.tw_state.get("regime")
                if regime == current_regime:
                    regime_start_time = event.timestamp
                else:
                    break
        regime_duration = timestamps[-1] - regime_start_time
    
    return TemporalCoherence(
        drift_slope=slope,
        drift_acceleration=acceleration,
        drift_volatility=volatility,
        regime_stability=stability,
        drift_values=drift_values,
        timestamps=timestamps,
        current_regime=current_regime,
        regime_duration=regime_duration
    )


def compute_drift_slope(events: List[Any]) -> float:
    """
    Compute drift slope via linear regression.
    
    Args:
        events: List of StoryEvents
        
    Returns:
        Slope (drift change per event)
    """
    drift_values = []
    
    for event in events:
        if hasattr(event, 'drift_state') and event.drift_state:
            drift = event.drift_state.get("drift_metric", 0.0)
            drift_values.append(drift)
    
    if len(drift_values) < 2:
        return 0.0
    
    # Linear regression
    n = len(drift_values)
    x = list(range(n))
    y = drift_values
    
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    
    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    
    slope = numerator / denominator if denominator != 0 else 0.0
    
    return slope


def compute_drift_acceleration(events: List[Any]) -> float:
    """
    Compute drift acceleration (second derivative).
    
    Args:
        events: List of StoryEvents
        
    Returns:
        Average acceleration
    """
    drift_values = []
    
    for event in events:
        if hasattr(event, 'drift_state') and event.drift_state:
            drift = event.drift_state.get("drift_metric", 0.0)
            drift_values.append(drift)
    
    if len(drift_values) < 3:
        return 0.0
    
    # Second derivative approximation
    accelerations = []
    for i in range(1, len(drift_values) - 1):
        accel = drift_values[i + 1] - 2 * drift_values[i] + drift_values[i - 1]
        accelerations.append(accel)
    
    return sum(accelerations) / len(accelerations) if accelerations else 0.0


def detect_regime_stability(events: List[Any]) -> float:
    """
    Detect regime stability (how often regime changes).
    
    Args:
        events: List of StoryEvents
        
    Returns:
        Stability score (0-1, higher = more stable)
    """
    if len(events) < 2:
        return 1.0
    
    # Track regime changes
    regimes = []
    
    for event in events:
        if hasattr(event, 'tw_state') and event.tw_state:
            regime = event.tw_state.get("regime")
            if regime:
                regimes.append(regime)
    
    if len(regimes) < 2:
        return 1.0
    
    # Count regime changes
    changes = 0
    for i in range(len(regimes) - 1):
        if regimes[i] != regimes[i + 1]:
            changes += 1
    
    # Stability = 1 - (change_rate)
    change_rate = changes / (len(regimes) - 1)
    stability = 1.0 - change_rate
    
    return stability
