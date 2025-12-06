# Multi-Stream Narratives - v3.3 Phase 2

**Status:** ✅ IMPLEMENTED (Backend Only)  
**Version:** KALDRA v3.3 Phase 2  
**Date:** December 2025

---

## Overview

The Multi-Stream Narratives feature enables KALDRA to track, buffer, and compare narrative evolution across **multiple parallel sources** (e.g., NYT, Twitter, Reddit). This allows analysis of how different media streams tell the same story differently—or diverge into separate narratives.

### Key Capabilities

- **Per-Stream Buffering**: Maintain separate FIFO buffers for each stream
- **Windowed Access**: Retrieve recent events from any stream
- **Cross-Stream Comparison**: Measure divergence in archetypal patterns and polarities
- **Future-Ready**: Reserved infrastructure for StoryArc-level comparison

### What This Phase Does NOT Include

> [!IMPORTANT]
> Phase 2 is **backend-only**. The following are reserved for future phases:
> - API exposure via SignalAdapter
> - Automatic `stream_id` population in StoryStage
> - Multi-stream MetaStage integration
> - StoryArc divergence metrics

---

## Data Structures

### StoryEvent (Extended)

Located in: [unified_signal.py](file:///Users/niki/Desktop/kaldra_core/src/common/unified_signal.py)

```python
@dataclass
class StoryEvent:
    event_id: str
    timestamp: float
    sequence_id: int
    text: str
    
    # Core KALDRA components
    delta12: Optional[Dict[str, float]] = None
    delta144_state: Optional[str] = None
    polarity_scores: Optional[Dict[str, float]] = None
    
    # v3.3 Phase 2 — Multi-Stream Narratives
    stream_id: Optional[str] = None  # e.g., "nyt", "twitter", "report_42"
    
    # ... other fields ...
```

**Backward Compatibility**: The `stream_id` field defaults to `None`. Existing code that doesn't set it will use `"default"` as the stream ID.

### StreamWindow

Located in: [multi_stream_buffer.py](file:///Users/niki/Desktop/kaldra_core/src/story/multi_stream_buffer.py)

```python
@dataclass
class StreamWindow:
    stream_id: str
    events: List[StoryEvent]
```

A snapshot of recent events from a single stream.

### StreamComparisonResult

Located in: [stream_comparator.py](file:///Users/niki/Desktop/kaldra_core/src/story/stream_comparator.py)

```python
@dataclass
class StreamComparisonResult:
    stream_a: str
    stream_b: str
    archetype_divergence: float      # [0,1]
    polarity_divergence: float       # [0,1]
    stage_divergence: float          # [0,1] (FUTURE)
    overall_divergence: float        # [0,1]
    notes: Dict[str, str]
```

Result of comparing two streams. Divergence scores range from `0.0` (identical) to `1.0` (completely different).

---

## MultiStreamBuffer

### Purpose

Manages separate FIFO buffers for multiple narrative streams, with configurable per-stream and global limits.

### API

#### Initialization

```python
from src.story.multi_stream_buffer import MultiStreamBuffer

buffer = MultiStreamBuffer(
    max_events_per_stream=500,  # FIFO limit per stream
    global_max_events=5000       # Total events across all streams
)
```

#### Adding Events

```python
from src.common.unified_signal import StoryEvent

event = StoryEvent(
    event_id="evt_001",
    timestamp=time.time(),
    sequence_id=1,
    text="Breaking: New policy announced",
    stream_id="nyt",
    delta12={"hero": 0.65, "sage": 0.42},
    polarity_scores={"order": 0.71, "chaos": 0.29}
)

buffer.add_event(event)
```

#### Retrieving Windows

```python
# Get last 50 events from NYT
nyt_window = buffer.get_window("nyt", size=50)
print(f"NYT has {len(nyt_window.events)} events")

# Get windows for all streams
all_windows = buffer.get_all_windows(size=50)
for window in all_windows:
    print(f"{window.stream_id}: {len(window.events)} events")
```

#### Stream Management

```python
# List all active streams
streams = buffer.list_streams()
print(f"Active streams: {streams}")

# Clear a specific stream
buffer.clear_stream("twitter")

# Clear everything
buffer.clear_all()
```

### Limits and Eviction

- **Per-Stream Limit**: When a stream exceeds `max_events_per_stream`, the oldest event in that stream is removed (FIFO).
- **Global Limit**: When total events exceed `global_max_events`, the oldest event **across all streams** is removed.

---

## StreamComparator

### Purpose

Compares narrative evolution across different streams by measuring divergence in archetypal patterns and polarities.

### API

#### Basic Usage

```python
from src.story.stream_comparator import StreamComparator

comparator = StreamComparator()

# Get windows from buffer
windows = buffer.get_all_windows(size=100)

# Compare all pairs
results = comparator.compare_windows(windows)

for result in results:
    print(f"{result.stream_a} vs {result.stream_b}:")
    print(f"  Archetype Divergence: {result.archetype_divergence:.2f}")
    print(f"  Polarity Divergence:  {result.polarity_divergence:.2f}")
    print(f"  Overall Divergence:   {result.overall_divergence:.2f}")
```

### Divergence Metrics

#### Archetype Divergence

Measures how different the archetypal profiles are between two streams:

- Aggregates `delta12` scores (average per archetype)
- Aggregates `delta144_state` frequencies
- Computes cosine divergence between profile vectors

#### Polarity Divergence

Measures how different the polarity patterns are:

- Aggregates `polarity_scores` (average per polarity)
- Computes cosine divergence

#### Overall Divergence

Weighted average of component divergences:

```
overall = 0.5 * archetype_divergence + 0.5 * polarity_divergence
```

> [!NOTE]
> **Future Enhancement**: When StoryArc integration is complete, `stage_divergence` will be added with a weight of ~0.33 each.

#### Interpretation

- **0.0 - 0.2**: Streams are very similar (convergent narratives)
- **0.2 - 0.5**: Moderate divergence (different emphasis)
- **0.5 - 0.8**: High divergence (conflicting narratives)
- **0.8 - 1.0**: Completely different (orthogonal narratives)

---

## Example: Multi-Stream Analysis

```python
import time
from src.story.multi_stream_buffer import MultiStreamBuffer
from src.story.stream_comparator import StreamComparator
from src.common.unified_signal import StoryEvent

# Initialize buffer
buffer = MultiStreamBuffer(max_events_per_stream=100)

# Simulate events from different streams
# NYT: High "order", hero archetype
for i in range(10):
    buffer.add_event(StoryEvent(
        event_id=f"nyt_{i}",
        timestamp=time.time() + i,
        sequence_id=i,
        text=f"NYT story {i}",
        stream_id="nyt",
        delta12={"hero": 0.8, "sage": 0.3},
        polarity_scores={"order": 0.75, "chaos": 0.25}
    ))

# Twitter: High "chaos", rebel archetype
for i in range(10):
    buffer.add_event(StoryEvent(
        event_id=f"twitter_{i}",
        timestamp=time.time() + i,
        sequence_id=i,
        text=f"Twitter story {i}",
        stream_id="twitter",
        delta12={"rebel": 0.7, "orphan": 0.4},
        polarity_scores={"order": 0.2, "chaos": 0.8}
    ))

# Compare streams
comparator = StreamComparator()
windows = buffer.get_all_windows(size=50)
results = comparator.compare_windows(windows)

for result in results:
    print(f"\n{result.stream_a} vs {result.stream_b}")
    print(f"  Archetype: {result.archetype_divergence:.2f}")
    print(f"  Polarity:  {result.polarity_divergence:.2f}")
    print(f"  Overall:   {result.overall_divergence:.2f}")
    
    if result.overall_divergence > 0.7:
        print("  ⚠️  Highly divergent narratives!")
```

**Expected Output:**

```
nyt vs twitter
  Archetype: 0.85
  Polarity:  0.82
  Overall:   0.84
  ⚠️  Highly divergent narratives!
```

---

## Backward Compatibility

### No Breaking Changes

All modifications are **additive** and **backward compatible**:

1. **StoryEvent.stream_id**: Optional field, defaults to `None`
2. **Existing Code**: Continues to work without modification
3. **Default Stream**: Events without `stream_id` are assigned to `"default"`

### Migration Path

To start using multi-stream features:

1. **Set `stream_id`** when creating `StoryEvent`:
   ```python
   event = StoryEvent(..., stream_id="nyt")
   ```

2. **Use `MultiStreamBuffer`** instead of manual event lists

3. **Compare streams** with `StreamComparator`

> [!TIP]
> You can gradually migrate by setting `stream_id` only for new events. Old events will coexist in the `"default"` stream.

---

## Testing

### Unit Tests

- [test_multi_stream_buffer.py](file:///Users/niki/Desktop/kaldra_core/tests/story/test_multi_stream_buffer.py): 13 tests covering buffer operations
- [test_stream_comparator.py](file:///Users/niki/Desktop/kaldra_core/tests/story/test_stream_comparator.py): 11 tests covering divergence calculations

### Running Tests

```bash
# Run all multi-stream tests
pytest tests/story/test_multi_stream_buffer.py tests/story/test_stream_comparator.py -v

# Run with coverage
pytest tests/story/test_multi_stream_buffer.py tests/story/test_stream_comparator.py --cov=src/story
```

---

## Future Work

The following features are **marked but not implemented** in Phase 2:

### 1. Automatic `stream_id` Population

**Goal**: StoryStage automatically populates `stream_id` from `InputMetadata.stream_id`.

**Location**: `src/unification/stages/story_stage.py`

**Changes**:
```python
# In StoryStage._build_event_from_context()
event = StoryEvent(
    ...,
    stream_id=input_ctx.metadata.stream_id  # Auto-populate
)
```

### 2. Multi-Stream Pipeline Integration

**Goal**: Create a `MultiStreamStage` that processes `input_ctx_list` in parallel.

**Location**: New file `src/unification/stages/multi_stream_stage.py`

**Features**:
- Process multiple InputContext objects
- Populate `StoryContext` with cross-stream comparison results
- Expose via `UnifiedOutput`

### 3. StoryArc Divergence

**Goal**: Compare journey stages (Campbell's Hero's Journey) across streams.

**Dependencies**: Requires `StoryArc` to be stream-aware

**Metric**: Measure how far apart streams are in their narrative journey (e.g., one stream in "Crossing the Threshold", another in "Return")

### 4. Signal Adapter Exposure

**Goal**: Expose multi-stream metrics in the API.

**Location**: `src/api/signal_adapter.py`

**Proposed Signals**:
```json
{
  "multi_stream": {
    "active_streams": ["nyt", "twitter", "reddit"],
    "pairwise_divergence": {
      "nyt_vs_twitter": 0.84,
      "nyt_vs_reddit": 0.62,
      "twitter_vs_reddit": 0.51
    },
    "max_divergence": 0.84,
    "convergent": false
  }
}
```

### 5. Performance Optimization

**Goal**: Parallelize stream comparison for large numbers of streams.

**Approach**: Use multiprocessing or asyncio for `compare_windows()` when comparing 10+ streams.

---

## Limitations

### Current Phase (2)

- No automatic `stream_id` assignment (must be set manually)
- No API exposure (backend only)
- `stage_divergence` always returns `0.0` (reserved for future)
- No MetaContext integration

### Design Constraints

- **Memory**: With `global_max_events=5000`, expect ~5-10 MB memory usage (depending on event metadata)
- **Performance**: Comparison is O(N²) in number of streams. For 100+ streams, consider sampling or parallelization.

---

## Related Documentation

- [KALDRA v3.3 Roadmap](file:///Users/niki/Desktop/kaldra_core/docs/roadmaps/KALDRA_V3_3_MULTI_STREAM.md)
- [Multi-Modal Input (Phase 1)](file:///Users/niki/Desktop/kaldra_core/docs/multistream/MULTIMODAL_INPUT_v3_3_PHASE_1.md)
- [Story Engine Primitives (v3.2)](file:///Users/niki/Desktop/kaldra_core/docs/story/STORY_ENGINE_PRIMITIVES_v3_2.md)
- [TW369 Topological Deepening](file:///Users/niki/Desktop/kaldra_core/docs/tw369/TW369_TOPOLOGICAL_DEEPENING_v3_2.md)

---

## Summary

Multi-Stream Narratives (Phase 2) provides the **foundational infrastructure** for tracking and comparing narrative evolution across multiple parallel sources. With `MultiStreamBuffer` and `StreamComparator`, KALDRA can now:

- ✅ Buffer events from multiple streams
- ✅ Retrieve windowed snapshots per stream
- ✅ Measure archetypal and polarity divergence
- ✅ Identify convergent vs. conflicting narratives

Future phases will integrate this into the pipeline, expose it via the API, and add StoryArc-level comparison.
