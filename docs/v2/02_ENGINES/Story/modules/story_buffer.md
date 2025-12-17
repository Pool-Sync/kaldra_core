# 📦 Story Buffer Module

> **Module**: `StoryBuffer`  
> **Engine**: [[../ENGINE_OVERVIEW|Story]]  
> **Path**: `src/story/story_buffer.py`  
> **Node ID**: `mod_story_buffer`

---

## What It Is

The `StoryBuffer` is the data container and memory management system for the Story engine. It holds the sequence of specific `StoryEvent` objects that make up the narrative timeline.

The buffer is more than just a list; it implements a **temporal window** concept. It can store a fixed number of recent events (short-term memory) or a specific time window (e.g., last 10 minutes).

`StoryEvent` objects are rich data structures. They contain the timestamp, the raw input text, the `KaldraSignal` output from that moment (embeddings, archetypes, drift), and metadata. This effectively snapshots the system's entire state at a point in time.

The buffer supports **multi-stream isolation**. Events can be tagged with a `stream_id`, allowing a single buffer instance to track multiple interlaced narratives (e.g., different characters or subplots) and query them independently.

It provides utility methods for analysis: retrieving vectors as numpy arrays (for efficient computation), slicing by time time, and finding nearest neighbors in time.

The sorting mechanism guarantees chronological integrity, crucial because events might arrive out of order in a distributed system (though KALDRA is currently synchronous).

It implements `Protocol` interfaces for serialization, allowing narrative histories to be saved to disk or sent over the API (e.g., for simple replay).

---

## How It Works

### Step-by-Step Mechanics

1. **Add Event**: `add_event(timestamp, signal, metadata)`
2. **Validation**: Check for duplicates and valid timestamp
3. **Storage**: Append to internal list
4. **Pruning**: If max_size exceeded, remove oldest events
5. **Retrieval**: `get_events(window)` returns sorted subset
6. **Vectorization**: `get_embedding_matrix()` returns (N, D) array

### Mermaid Diagram

```mermaid
flowchart LR
    INPUT[Add Event] --> VALID[Validate]
    VALID --> STORE[Store in List]
    STORE --> PRUNE[Prune Oldest]
    
    QUERY[Get Events] --> FILTER[Filter by Stream/Time]
    FILTER --> SORT[Sort Chronological]
    SORT --> RETURN[List[StoryEvent]]
```

---

## Data Structures

### StoryEvent
```python
@dataclass
class StoryEvent:
    event_id: str
    timestamp: float
    text: str
    signal: KaldraSignal  # Full system state
    stream_id: str
    metadata: Dict
```

---

## With What It Works

### Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| `KaldraSignal` | contains | Snapshot of state |
| `numpy` | uses | Vector operations |

---

## Public Surface

| Item | Type | Description |
|------|------|-------------|
| `StoryBuffer` | class | Main buffer |
| `add_event()` | method | Ingest new event |
| `get_ordered_events()` | method | Retrieve timeline |
| `get_embedding_matrix()` | method | Get matrix for math |
| `clear()` | method | Reset memory |

---

## Future Implementations

1. Persistent backing store (SQLite/Redis)
2. Semantic compression (merging similar events)
3. Distributed buffer synchronization

---

## Enhancements (Short/Medium Term)

1. Add specialized query filters (by archetype)
2. Implementation circular buffer optimization
3. Add serialization to JSON

---

## Research Track (Long Term)

1. Associative memory (retrieval by content)
2. Long-term semantic compression
3. "Dreaming" (replaying/consolidating memory)

---

## Known Limitations

1. In-memory only (lost on restart)
2. Linear memory growth without pruning
3. No built-in compression

---

## Testing

| Test File | Coverage | Notes |
|-----------|----------|-------|
| `tests/story/test_buffer.py` | ✅ Good | Part of 16 files |

---

## Next Steps

1. [ ] Add persistence
2. [ ] Add compression
3. [ ] Optimize memory usage

---

## Related

- [[../ENGINE_OVERVIEW]]
- [[story_aggregator]]
