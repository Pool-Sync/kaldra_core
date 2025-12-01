# KALDRA v2.6 Story Engine Specification

**Version**: 2.6.0  
**Codename**: The Narrative Spine  
**Status**: Complete

---

## Overview

The KALDRA Story Engine transforms KALDRA from a single-shot signal analyzer into a **temporal narrative intelligence system** with memory, pattern detection, and predictive capabilities.

### Key Capabilities

- **Narrative Memory**: Persistent buffer of recent events (default: 12)
- **Motion Tracking**: Δ12/Δ144 evolution over time
- **Arc Detection**: Campbell's Hero's Journey progression
- **Inflection Prediction**: Detect narrative turning points
- **Drift Trajectories**: TW369 temporal analysis
- **Polarity Oscillations (v2.7)**: Track 46-dimensional tension shifts and inversions

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Story Engine v2.6                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │
│  │ StoryBuffer  │───▶│ Aggregator   │───▶│ Timeline │ │
│  │ (Memory)     │    │ (Patterns)   │    │ (Δ12/144)│ │
│  └──────────────┘    └──────────────┘    └──────────┘ │
│         │                    │                   │      │
│         ▼                    ▼                   ▼      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │
│  │ NarrativeArc │    │ TW369        │    │ Story    │ │
│  │ (Campbell)   │    │ Temporal     │    │ Signal   │ │
│  └──────────────┘    └──────────────┘    └──────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Components

### 1. StoryBuffer

**Purpose**: Sliding window memory for narrative events

**Capacity**: Default 12 events (configurable)

**Features**:
- FIFO buffer with overflow handling
- Full serialization (to_dict/from_dict)
- Timestamp tracking
- Complete KALDRA signal storage

**API**:
```python
from story import StoryBuffer

buffer = StoryBuffer(capacity=12)
event = buffer.add_event(
    text="...",
    delta12={...},
    delta144_state="...",
    meta_scores={...},
    drift_state={...}
)
```

### 2. StoryAggregator

**Purpose**: Detect temporal patterns and compute motion vectors

**Metrics**:
- **Motion Vectors**: Δ12 shift magnitude, drift velocity, meta-score deltas
- **Inflection Points**: Drift peaks, archetype shifts, stage transitions, polarity inversions
- **Arc Progression**: Campbell stage tracking
- **Drift Trajectory**: Slope, acceleration, volatility
- **Polarity Deltas**: Magnitude of change in 46 polarity axes

**API**:
```python
from story import aggregate_story

aggregation = aggregate_story(buffer)
# aggregation.motion_vectors
# aggregation.inflection_points
# aggregation.drift_trajectory
```

### 3. NarrativeArc Engine

**Purpose**: Campbell-based arc detection and prediction

**Hybrid Model**:
- Campbell 12 stages (macro-arc)
- Δ144 microstates
- TW369 drift dynamics
- Meta-engine alignment (Nietzsche/Aurelius)

**Output**:
```python
from story import analyze_arc

arc = analyze_arc(buffer)
# arc.current_stage = "tests_allies_enemies"
# arc.arc_progress = 0.42
# arc.predicted_next_stage = "approach_to_cave"
# arc.tension_trend = +0.14
```

### 4. ArchetypalTimeline

**Purpose**: Track Δ12/Δ144 evolution with motion metrics

**Metrics**:
- Total archetype shifts
- Average shift magnitude
- Trajectory curvature
- Archetype persistence score
- Loop detection

**API**:
```python
from story import build_timeline

timeline = build_timeline(buffer)
# timeline.total_shifts
# timeline.trajectory_curvature
# timeline.loops
```

### 5. TW369 Temporal Coherence

**Purpose**: Drift analysis over time

**Metrics**:
- Drift slope (linear regression)
- Drift acceleration (2nd derivative)
- Drift volatility (std dev)
- Regime stability

**API**:
```python
from tw369.temporal_coherence import compute_temporal_coherence

coherence = compute_temporal_coherence(events)
# coherence.drift_slope
# coherence.drift_acceleration
# coherence.regime_stability
```

---

## StorySignal Output Format

Extended KALDRA signal with `story` block:

```json
{
  "signal_id": "uuid",
  "timestamp": 1234567890.0,
  "delta12": {...},
  "delta144": {...},
  "meta": {...},
  "tw369": {...},
  "story": {
    "narrative_stage": "tests_allies_enemies",
    "arc_progress": 0.42,
    "timeline": [...],
    "inflection_points": [...],
    "motion_vectors": [...],
    "drift_trajectory": {
      "drift_slope": 0.05,
      "drift_acceleration": 0.02,
      "drift_volatility": 0.12
    },
    "predicted_next_stage": "approach_to_cave",
    "tension_trend": +0.14,
    "transition_likelihood": 0.65
  }
}
```

---

## Usage Example

```python
from story import StoryBuffer, aggregate_story, analyze_arc, build_timeline

# Initialize buffer
buffer = StoryBuffer(capacity=12)

# Add events over time
for signal in narrative_stream:
    buffer.add_event(
        text=signal.text,
        delta12=signal.delta12.to_dict(),
        delta144_state=signal.delta144_state,
        meta_scores=signal.meta,
        drift_state=signal.drift_state.to_dict()
    )
    
    # Analyze narrative
    aggregation = aggregate_story(buffer)
    arc = analyze_arc(buffer)
    timeline = build_timeline(buffer)
    
    print(f"Stage: {arc.current_stage}")
    print(f"Progress: {arc.arc_progress:.2f}")
    print(f"Inflections: {len(aggregation.inflection_points)}")
```

---

## Integration with KALDRA Pipeline

Story Engine is **opt-in** and **non-breaking**:

1. **Disabled by default**: No impact on existing behavior
2. **Feature flag**: Enable via `story_mode=true` query parameter
3. **Backward compatible**: All v2.5 functionality preserved

---

## Performance

- **Lightweight**: In-memory buffer only
- **Fast**: O(n) aggregation where n = buffer size (typically 12)
- **Scalable**: Stateless per-request (buffer can be persisted externally)

---

## Limitations

- In-memory only (no persistence layer yet)
- Single narrative timeline (no multi-document merging)
- Keyword-based heuristics (no LLM-powered analysis yet)

---

## Future Enhancements

- Redis/Postgres persistence
- Cross-narrative merging
- Real-time WebSocket streaming
- LLM-powered arc prediction
- Topological narrative manifolds

---

**See Also**:
- [Story Buffer](./STORY_BUFFER.md)
- [Narrative Arc Engine](./NARRATIVE_ARC_ENGINE.md)
- [Timeline Engine](./TIMELINE_ENGINE.md)
- [Story Signal Format](./STORY_SIGNAL_FORMAT.md)
