# Story Event Persistence v1 - Documentation

**Version:** v1  
**Date:** December 2025  
**Integration:** Story Events → Supabase

---

## Overview

Narrative events generated during KALDRA processing are now automatically persisted to the `story_events` table in Supabase. This extends the signal persistence pattern to capture the temporal narrative structure.

---

## Architecture

```
KALDRA Pipeline
    ↓
[Story Processing]
    ↓
SignalAdapter.to_signal()
    ├─ Generate & persist signal
    └─ Persist story events ← NEW
        ↓
    StoryEventRepository
        ↓
    SupabaseClient
        ↓
    Supabase Database (story_events table)
```

---

## When Events Are Persisted

Story events are saved **after** the signal is persisted:
1. Pipeline processes input
2. `SignalAdapter` generates signal
3. Signal persisted to `signals` table
4. **Story events extracted and persisted** (new step)
5. Signal returned to caller

---

## Table Schema

### story_events

| Column | Type | Description |
|--------|------|-------------|
| `id` | uuid | Primary key |
| `created_at` | timestamptz | Auto timestamp |
| `signal_id` | uuid | Parent signal (FK) |
| `stream_id` | text | Stream identifier |
| `text` | text | Event description |
| `delta144_state` | text | State at event time |
| `polarities` | jsonb | Polarity scores |
| `meta` | jsonb | Additional metadata |

---

## Event Extraction

Events are extracted from `UnifiedContext.story_ctx.events`. Each event can be:
- **Dict**: `{"text": "...", "stream_id": "...", ...}`
- **Object**: With attributes like `.text`, `.stream_id`

### Extracted Fields

```python
{
    "signal_id": "<parent-signal-uuid>",
    "stream_id": ev.get("stream_id") or ev.stream_id,
    "text": ev.get("text") or ev.get("description"),
    "delta144_state": ev.get("delta144_state") or ev.get("state"),
    "polarities": ev.get("polarities"),
    "meta": {
        "stage": ev.get("stage"),
        "kind": ev.get("kind"),
        "source": "kaldra_pipeline"
    }
}
```

---

## Error Handling

**Critical Rule:** Story events persistence failures NEVER break the pipeline.

```python
try:
    # Extract & persist events
    events = extract_story_events(context, signal_id)
    repository.bulk_create_events(events)
    
except Exception as e:
    logger.error(f"Story events persistence failed: {e}")
    # Pipeline continues

# Signal still returned
return signal
```

---

## Configuration

### Enable/Disable

```python
# Both enabled (default)
adapter = SignalAdapter()

# Signals only
adapter = SignalAdapter(enable_story_events_persistence=False)

# All persistence disabled
adapter = SignalAdapter(enable_persistence=False)

# Custom repositories (testing)
adapter = SignalAdapter(
    signal_repository=signal_repo,
    story_event_repository=event_repo
)
```

### Requirements

Story events persistence requires:
- ✅ Signal persistence enabled (`enable_persistence=True`)
- ✅ `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` in `.env`
- ✅ `StoryEventRepository` importable

If any requirement fails:
- Story events persistence auto-disables
- Warning logged
- Pipeline continues normally

---

## Repository Operations

### List Events

```python
repo = StoryEventRepository()

# All events
events = repo.list_events(limit=50)

# By signal
events = repo.list_events(signal_id="uuid-here")

# By stream
events = repo.list_events(stream_id="nyt")
```

### Create Events

```python
# Single event
event = repo.create_event({
    "signal_id": "uuid",
    "text": "Event description",
    "stream_id": "twitter"
})

# Bulk create
events = repo.bulk_create_events([
    {"text": "Event 1"},
    {"text": "Event 2"},
    {"text": "Event 3"}
])
```

### Delete Events

```python
# By ID
repo.delete_event("event-uuid")

# By parent signal
repo.delete_by_signal("signal-uuid")
```

---

## Testing

### Repository Test

```bash
cd ~/Desktop/kaldra_core
python3 -m src.scripts.test_story_event_repository
```

Expected output:
- ✅ Repository initialized
- ✅ List existing events
- ✅ Create test event
- ✅ Bulk create events
- ✅ Delete test event

### Integration Tests

```bash
pytest tests/integration/test_story_event_persistence.py -v
```

Tests:
- ✅ Events persisted when context has events
- ✅ Persistence failure doesn't break pipeline
- ✅ Disabled persistence works
- ✅ No events when context empty
- ✅ Events linked to parent signal

---

## Monitoring

### Logs

**Success:**
```
[INFO] SignalAdapter: Story events persistence enabled
[DEBUG] SignalAdapter: Persisted 3 story events
```

**No Events:**
```
[DEBUG] SignalAdapter: No story events to persist
```

**Warning (non-fatal):**
```
[WARNING] SignalAdapter: Failed to persist story events: {error}
```

**Error (non-fatal):**
```
[ERROR] SignalAdapter: Unexpected error persisting story events: Exception(...)
```

---

## Use Cases

### Timeline Reconstruction
Query events by signal to rebuild narrative timeline

### Multi-Stream Analysis
Compare events across different streams (Twitter, NYT, etc.)

### State Transitions
Track delta144 state changes over time

### Narrative Coherence
Analyze polarities and stages across events

---

## Future Enhancements (v2+)

- Event deduplication
- Temporal clustering
- Stream divergence metrics
- Automatic timeline generation
- Event importance scoring
- Cascade deletion options

---

## Backward Compatibility

✅ **Fully backward compatible**
- Existing code works unchanged
- Persistence is optional
- Graceful degradation
- No API changes

---

## Summary

**What changed:**
- `SignalAdapter` now extracts and persists story events
- `StoryEventRepository` provides CRUD operations
- Automatic linking to parent signals

**What stayed the same:**
- Signal generation unchanged
- Return values unchanged
- Pipeline reliability unchanged

**Net effect:**
- Complete narrative history in database
- Zero breaking changes
- Robust error handling
