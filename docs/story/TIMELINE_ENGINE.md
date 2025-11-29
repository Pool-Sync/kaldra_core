# Timeline Engine - Archetypal Evolution Tracking

**Component**: ArchetypalTimeline  
**Version**: v2.6.0

---

## Overview

The Timeline Engine tracks Δ12/Δ144 evolution over time, computing motion metrics, detecting patterns, and identifying archetypal loops.

---

## ArchetypalTimeline Structure

```python
@dataclass
class ArchetypalTimeline:
    points: List[TimelinePoint]
    
    # Metrics
    total_shifts: int                    # Dominant archetype changes
    average_shift_magnitude: float       # Average Δ12 distance
    trajectory_curvature: float          # Path "curvedness" (0-1)
    archetype_persistence_score: float   # Stability (0-1)
    
    # Patterns
    loops: List[ArchetypalLoop]
```

### TimelinePoint

```python
@dataclass
class TimelinePoint:
    sequence_id: int
    timestamp: float
    delta12_dominant: str        # e.g., "A03_WARRIOR"
    delta12_probability: float
    delta144_state: str          # e.g., "A03_WARRIOR_3_05"
    drift_level: float
```

---

## API

### Build Timeline

```python
from story import build_timeline

timeline = build_timeline(buffer)

print(f"Total shifts: {timeline.total_shifts}")
print(f"Curvature: {timeline.trajectory_curvature:.2f}")
print(f"Persistence: {timeline.archetype_persistence_score:.2f}")
```

### Compute Shift Magnitude

```python
from story import compute_shift_magnitude

magnitude = compute_shift_magnitude(
    prev_delta12={"A01_INNOCENT": 0.7, "A02_ORPHAN": 0.3},
    curr_delta12={"A03_WARRIOR": 0.8, "A01_INNOCENT": 0.2}
)
# Returns Euclidean distance
```

### Compute Trajectory Curvature

```python
from story import compute_trajectory_curvature

curvature = compute_trajectory_curvature(events)
# 0.0 = straight line (no direction changes)
# 1.0 = maximum curvature (constant direction changes)
```

### Detect Loops

```python
from story import detect_archetypal_loops

loops = detect_archetypal_loops(timeline)

for loop in loops:
    print(f"Archetype: {loop.archetype}")
    print(f"Occurrences: {loop.loop_count}")
    print(f"Avg duration: {loop.average_duration:.1f} events")
```

---

## Metrics Explained

### 1. Total Shifts

Number of times the dominant archetype changes.

**Example**:
```
A01_INNOCENT → A03_WARRIOR → A03_WARRIOR → A07_RULER
```
Total shifts: 2 (INNOCENT→WARRIOR, WARRIOR→RULER)

### 2. Average Shift Magnitude

Average Euclidean distance in Δ12 space between consecutive events.

**Interpretation**:
- **< 0.2**: Gradual evolution
- **0.2-0.5**: Moderate changes
- **> 0.5**: Dramatic shifts

### 3. Trajectory Curvature

Measures how "curved" the archetypal path is.

**Computation**:
- Compute angle between consecutive motion vectors
- Average absolute angles
- Normalize to [0, 1]

**Interpretation**:
- **< 0.3**: Linear progression
- **0.3-0.7**: Moderate oscillation
- **> 0.7**: Highly non-linear, chaotic

### 4. Archetype Persistence Score

How long archetypes remain dominant.

**Computation**:
```python
persistence = max_consecutive_same_archetype / total_events
```

**Interpretation**:
- **> 0.7**: Very stable
- **0.4-0.7**: Moderate stability
- **< 0.4**: Highly volatile

---

## Loop Detection

A loop occurs when the same archetype appears 3+ times.

### ArchetypalLoop

```python
@dataclass
class ArchetypalLoop:
    start_sequence: int
    end_sequence: int
    archetype: str
    loop_count: int           # Number of occurrences
    average_duration: float   # Events between occurrences
```

### Example

```
Timeline: INNOCENT → WARRIOR → INNOCENT → SAGE → INNOCENT
```

Loop detected:
- Archetype: A01_INNOCENT
- Loop count: 3
- Average duration: 2 events

**Interpretation**: Character keeps returning to innocence/naivety despite growth attempts.

---

## Visualization Example

```
Timeline (12 events):

Seq  Archetype       Drift   Δ144 State
───────────────────────────────────────────
0    A01_INNOCENT    0.2     A01_INNOCENT_1_01
1    A01_INNOCENT    0.25    A01_INNOCENT_1_02
2    A03_WARRIOR     0.45    A03_WARRIOR_3_05  ← Shift
3    A03_WARRIOR     0.52    A03_WARRIOR_3_06
4    A03_WARRIOR     0.48    A03_WARRIOR_3_05
5    A07_RULER       0.35    A07_RULER_6_05    ← Shift
6    A07_RULER       0.3     A07_RULER_6_04
7    A10_SAGE        0.25    A10_SAGE_9_10     ← Shift
8    A10_SAGE        0.22    A10_SAGE_9_09
9    A10_SAGE        0.2     A10_SAGE_9_08
10   A10_SAGE        0.18    A10_SAGE_9_07
11   A10_SAGE        0.15    A10_SAGE_9_06

Metrics:
- Total shifts: 3
- Avg shift magnitude: 0.42
- Trajectory curvature: 0.35 (moderate)
- Persistence: 0.42 (SAGE stayed for 5 events)
```

---

## Integration with Drift

Timeline tracks drift alongside archetypes:

```python
for point in timeline.points:
    print(f"{point.delta12_dominant}: drift={point.drift_level:.2f}")
```

**Pattern Detection**:
- High drift + archetype shift = Crisis moment
- Low drift + stable archetype = Equilibrium
- Rising drift + no shift = Building tension

---

## Use Cases

### 1. Character Development Tracking

```python
timeline = build_timeline(character_buffer)

if timeline.total_shifts > 5:
    print("Character shows significant growth")
elif timeline.archetype_persistence_score > 0.8:
    print("Character is static/unchanging")
```

### 2. Narrative Complexity Analysis

```python
if timeline.trajectory_curvature > 0.7:
    print("Highly non-linear, complex narrative")
elif timeline.trajectory_curvature < 0.3:
    print("Linear, straightforward progression")
```

### 3. Loop Detection for Themes

```python
loops = detect_archetypal_loops(timeline)

for loop in loops:
    if loop.loop_count >= 3:
        print(f"Recurring theme: {loop.archetype}")
```

---

## Future Enhancements

- 3D trajectory visualization
- Attractor basin detection
- Phase transition analysis
- Multi-character timeline comparison
- Temporal clustering (k-means on trajectories)

---

**See Also**:
- [Story Engine Spec](./STORY_ENGINE_SPEC.md)
- [Story Buffer](./STORY_BUFFER.md)
- [Narrative Archetypes Guide](../guides/NARRATIVE_ARCHETYPES_HERO_JOURNEY_DRIFT.md)
