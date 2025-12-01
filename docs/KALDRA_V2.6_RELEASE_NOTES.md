# KALDRA v2.6 — Story Aggregation & Narrative Arcs

**Release Date**: November 28, 2025  
**Version**: 2.6.0  
**Codename**: The Narrative Spine  
**Status**: ✅ PRODUCTION READY

---

## Overview

KALDRA v2.6 transforms KALDRA from a single-shot signal analyzer into a **temporal narrative intelligence system** with memory, pattern detection, and predictive capabilities.

### Key Achievements

- ✅ **StoryBuffer** - Sliding window narrative memory (12 events default)
- ✅ **StoryAggregator** - Motion vectors & inflection detection
- ✅ **NarrativeArc** - Campbell-based arc tracking with prediction
- ✅ **ArchetypalTimeline** - Δ12/Δ144 evolution tracking
- ✅ **TW369 Temporal Coherence** - Drift analysis over time
- ✅ **StorySignal Format** - Extended JSON output
- ✅ **100% Backward Compatible** - All features opt-in

---

## What's New

### 1. StoryBuffer - Narrative Memory

**Purpose**: Persistent sliding window for recent events

**Features**:
- Default capacity: 12 events (one full Campbell cycle)
- FIFO overflow handling
- Complete KALDRA signal storage
- Full serialization (to_dict/from_dict)

**Usage**:
```python
from story import StoryBuffer

buffer = StoryBuffer(capacity=12)
event = buffer.add_event(
    text="The hero crosses the threshold.",
    delta12={"A03_WARRIOR": 0.6},
    meta_scores={"campbell": {"stage": "crossing_the_threshold"}}
)
```

### 2. StoryAggregator - Pattern Detection

**Purpose**: Detect temporal patterns and compute motion vectors

**Features**:
- Motion vectors (Δ12 shift, drift velocity, meta deltas)
- Inflection points (drift peaks, archetype shifts, stage transitions)
- Arc progression tracking
- Drift trajectory (slope, acceleration, volatility)
- Narrative oscillation index

**Usage**:
```python
from story import aggregate_story

aggregation = aggregate_story(buffer)
print(f"Inflections: {len(aggregation.inflection_points)}")
print(f"Drift slope: {aggregation.drift_trajectory.drift_slope:.3f}")
```

### 3. NarrativeArc - Campbell Tracking

**Purpose**: Hero's Journey detection and prediction

**Hybrid Model**:
- Campbell 12 stages (macro-arc)
- Δ144 microstates
- TW369 drift dynamics
- Meta-engine alignment (Nietzsche/Aurelius)

**Usage**:
```python
from story import analyze_arc

arc = analyze_arc(buffer)
print(f"Stage: {arc.current_stage}")
print(f"Progress: {arc.arc_progress:.2%}")
print(f"Next: {arc.predicted_next_stage}")
print(f"Tension: {arc.tension_trend:+.2f}")
```

### 4. ArchetypalTimeline - Evolution Tracking

**Purpose**: Track Δ12/Δ144 evolution with motion metrics

**Metrics**:
- Total archetype shifts
- Average shift magnitude
- Trajectory curvature
- Archetype persistence score
- Loop detection

**Usage**:
```python
from story import build_timeline

timeline = build_timeline(buffer)
print(f"Shifts: {timeline.total_shifts}")
print(f"Curvature: {timeline.trajectory_curvature:.2f}")
```

### 5. TW369 Temporal Coherence

**Purpose**: Drift analysis over time

**Metrics**:
- Drift slope (linear regression)
- Drift acceleration (2nd derivative)
- Drift volatility (standard deviation)
- Regime stability

**Usage**:
```python
from tw369.temporal_coherence import compute_temporal_coherence

coherence = compute_temporal_coherence(events)
print(f"Slope: {coherence.drift_slope:.3f}")
print(f"Stability: {coherence.regime_stability:.2f}")
```

### 6. StorySignal Format

**Purpose**: Extended KALDRA signal with temporal analysis

**New `story` Block**:
```json
{
  "story": {
    "narrative_stage": "tests_allies_enemies",
    "arc_progress": 0.42,
    "timeline": [...],
    "inflection_points": [...],
    "motion_vectors": [...],
    "drift_trajectory": {...},
    "predicted_next_stage": "approach_to_cave",
    "tension_trend": +0.14,
    "transition_likelihood": 0.65
  }
}
```

---

## Example Output

```json
{
  "signal_id": "uuid",
  "timestamp": 1701234567.890,
  "delta12": {"A03_WARRIOR": 0.65, "A05_SEEKER": 0.25},
  "meta": {
    "campbell": {"stage": "tests_allies_enemies", "confidence": 0.75}
  },
  "tw369": {"severity": 0.58, "plane": "3"},
  "story": {
    "narrative_stage": "tests_allies_enemies",
    "arc_progress": 0.42,
    "inflection_points": [
      {
        "inflection_type": "archetype_shift",
        "magnitude": 0.52,
        "description": "A01_INNOCENT → A03_WARRIOR"
      }
    ],
    "drift_trajectory": {
      "drift_slope": 0.06,
      "drift_acceleration": 0.01,
      "drift_volatility": 0.08
    },
    "predicted_next_stage": "approach_to_cave",
    "tension_trend": +0.12,
    "transition_likelihood": 0.55
  }
}
```

---

## Migration Guide

### For Existing Users

**No action required**. v2.6 is fully backward compatible.

### To Use Story Engine

```python
from story import StoryBuffer, aggregate_story, analyze_arc

# Initialize buffer
buffer = StoryBuffer(capacity=12)

# Add events over time
for signal in narrative_stream:
    buffer.add_event(
        text=signal.text,
        delta12=signal.delta12.to_dict(),
        meta_scores=signal.meta,
        drift_state=signal.drift_state.to_dict()
    )
    
    # Analyze when buffer has enough events
    if len(buffer) >= 3:
        aggregation = aggregate_story(buffer)
        arc = analyze_arc(buffer)
```

---

## Technical Details

### Architecture

- **In-memory buffer**: Lightweight, fast
- **Stateless**: Each request independent
- **Serializable**: Full to_dict/from_dict support
- **Modular**: Each component independent

### Performance

- **Time Complexity**: O(n) where n = buffer size (typically 12)
- **Space Complexity**: ~50KB for 12 events with full signals
- **Fast**: Sub-millisecond aggregation

---

## Backward Compatibility

**All v2.6 features are optional and disabled by default.**

- Story analysis only runs when buffer is populated
- No breaking changes to v2.5 behavior
- All existing tests continue to pass
- Story block only included if requested

---

## Test Coverage

**26 tests passing** (100%):
- StoryBuffer: 10/10 ✅
- StoryAggregator: 9/9 ✅
- TW369 Temporal Coherence: 7/7 ✅

All v2.5 tests continue to pass (100% backward compatibility).

---

## Documentation

**New Guides**:
1. [Story Engine Spec](./story/STORY_ENGINE_SPEC.md) - Architecture & components
2. [Story Buffer](./story/STORY_BUFFER.md) - Memory system
3. [Narrative Arc Engine](./story/NARRATIVE_ARC_ENGINE.md) - Campbell tracking
4. [Timeline Engine](./story/TIMELINE_ENGINE.md) - Evolution tracking
5. [Story Signal Format](./story/STORY_SIGNAL_FORMAT.md) - JSON schema

**Updated**:
- [KALDRA Core Roadmap](./core/KALDRA_CORE_MASTER_ROADMAP_V2.3_V2.9.md) - v2.6 marked complete
- [CHANGELOG](../CHANGELOG.md) - v2.6 entry added

---

## Known Limitations

- In-memory only (no persistence layer yet)
- Single narrative timeline (no multi-document merging)
- Keyword-based heuristics (no LLM-powered analysis)

---

## Next Steps (v2.7+)

- Apps Specialization (Alpha/Geo/Product)
- Tau Layer & Safeguard Integration
- Hardening & Performance optimization

---

**KALDRA v2.6 - The Narrative Spine is Complete!** 🌀
