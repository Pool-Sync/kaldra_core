# Story Buffer - Narrative Memory

**Component**: StoryBuffer  
**Version**: v2.6.0

---

## Overview

StoryBuffer is a sliding window memory system that maintains the last N narrative events, enabling temporal analysis and pattern detection.

---

## Design

### Sliding Window

- **Capacity**: Default 12 events (one full Campbell cycle)
- **Overflow**: FIFO - oldest events automatically removed
- **Persistence**: Full serialization support

### StoryEvent Structure

```python
@dataclass
class StoryEvent:
    event_id: str              # UUID
    timestamp: float           # Unix timestamp
    sequence_id: int           # Sequential counter
    text: str                  # Input text
    
    # KALDRA components
    delta12: Dict[str, float]  # Δ12 vector
    delta144_state: str        # Δ144 state ID
    kindra: Dict[str, Any]     # Kindra scores
    meta_scores: Dict[str, Any]  # Nietzsche/Aurelius/Campbell
    drift_state: Dict[str, Any]  # DriftState
    tw_state: Dict[str, Any]     # TWState
    
    metadata: Dict[str, Any]   # Optional metadata
```

---

## API

### Initialization

```python
from story import StoryBuffer

buffer = StoryBuffer(capacity=12)
```

### Adding Events

```python
event = buffer.add_event(
    text="The hero crosses the threshold into the unknown.",
    delta12={"A03_WARRIOR": 0.6, "A05_SEEKER": 0.3},
    delta144_state="A03_WARRIOR_3_05",
    meta_scores={
        "campbell": {"stage": "crossing_the_threshold", "confidence": 0.75}
    },
    drift_state={"drift_metric": 0.52}
)
```

### Retrieving Events

```python
# Get 3 most recent (newest first)
recent = buffer.get_recent(3)

# Get complete timeline (oldest first)
timeline = buffer.get_timeline()

# Get buffer size
count = len(buffer)
```

### Serialization

```python
# Save buffer
data = buffer.to_dict()
save_to_file(data)

# Restore buffer
buffer = StoryBuffer.from_dict(data)
```

### Clearing

```python
buffer.clear()  # Remove all events
```

---

## Memory Management

### Overflow Behavior

When capacity is reached, oldest event is automatically removed:

```python
buffer = StoryBuffer(capacity=3)

buffer.add_event("Event 1")  # [E1]
buffer.add_event("Event 2")  # [E1, E2]
buffer.add_event("Event 3")  # [E1, E2, E3]
buffer.add_event("Event 4")  # [E2, E3, E4]  ← E1 removed
```

### Capacity Guidelines

- **12 events**: One full Campbell cycle (recommended default)
- **24 events**: Two cycles for pattern detection
- **6 events**: Minimal for arc detection

---

## Schema

See `schema/story/story_event.schema.json` for complete JSON schema.

---

## Performance

- **Time Complexity**: O(1) for add, O(n) for retrieval
- **Space Complexity**: O(capacity × event_size)
- **Typical Memory**: ~50KB for 12 events with full KALDRA signals

---

## Example: Complete Workflow

```python
from story import StoryBuffer

# Initialize
buffer = StoryBuffer(capacity=12)

# Process narrative stream
for text_chunk in narrative:
    # Run KALDRA pipeline
    signal = kaldra.analyze(text_chunk)
    
    # Add to buffer
    buffer.add_event(
        text=text_chunk,
        delta12=signal.delta12.to_dict(),
        delta144_state=signal.delta144_state,
        meta_scores=signal.meta,
        drift_state=signal.drift_state.to_dict(),
        tw_state=signal.tw_state.to_dict()
    )
    
    # Analyze when buffer has enough events
    if len(buffer) >= 3:
        from story import aggregate_story
        aggregation = aggregate_story(buffer)
        print(f"Inflections: {len(aggregation.inflection_points)}")
```

---

## Thread Safety

**Not thread-safe**. Use external synchronization for concurrent access.

---

## Persistence

### Save/Load Example

```python
import json

# Save
with open("story_buffer.json", "w") as f:
    json.dump(buffer.to_dict(), f)

# Load
with open("story_buffer.json", "r") as f:
    data = json.load(f)
    buffer = StoryBuffer.from_dict(data)
```

---

## Future Enhancements

- Redis backend for distributed memory
- Compression for large buffers
- Event pruning strategies (keep only inflection points)
- Multi-buffer support (parallel narratives)

---

**See Also**:
- [Story Engine Spec](./STORY_ENGINE_SPEC.md)
- [Story Aggregator](./STORY_ENGINE_SPEC.md#2-storyaggregator)
