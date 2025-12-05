# Signal Persistence v1 - Documentation

**Version:** v1  
**Date:** December 2025  
**Component:** SignalAdapter Integration

---

## Overview

All signals processed by KALDRA are now **automatically persisted** to Supabase via the `SignalRepository`. This happens transparently in the `SignalAdapter` after pipeline processing.

---

## Architecture

```
KALDRA Pipeline
    ↓
[Input Processing]
    ↓
[Kindra, Delta144, TW369, Story, etc.]
    ↓
SignalAdapter.to_signal()
    ├─ Generate signal dict
    └─ Persist to Supabase ← NEW
        ↓
    SignalRepository
        ↓
    SupabaseClient
        ↓
    Supabase Database
```

---

## When Signals Are Persisted

Signals are saved **after** the pipeline completes:
1. Pipeline processes the input through all stages
2. `SignalAdapter.to_signal()` generates the output
3. **Persistence happens** (new step)
4. Signal returned to caller

---

## Persisted Fields

### Required Fields
- `id` (UUID) - Auto-generated
- `domain` - Default "alpha" or from META_CTX
- `title` - First 100 chars of input text
- `summary` - First 500 chars of input text
- `raw_payload` (JSONB) - Full signal dict
- `created_at` - Timestamp (UTC)

### Extracted from Context
- `delta144_state` - From ARCHETYPE_CTX
- `dominant_archetype` - Max value from Delta12
- `dominant_polarity` - Max value from polarities
- `tw_regime` - From DRIFT_CTX
- `journey_stage` - From STORY_CTX
- `importance` - From META_CTX or default 0.5
- `confidence` - From summary or default 0.8

---

## Error Handling

**Critical Rule:** Persistence failures NEVER break the pipeline.

```python
try:
    # Persist signal
    result = repository.create_signal(payload)
    
    if "error" in result:
        logger.warning("Failed to persist signal")  # Log only
    
except Exception as e:
    logger.error(f"Unexpected error: {e}")  # Log only

# Pipeline continues regardless
return signal
```

If Supabase is down:
- ✅ API continues responding
- ✅ Signals still generated
- ❌ Database persistence skipped
- 📝 Errors logged

---

## Configuration

### Enable/Disable Persistence

```python
# Enabled (default)
adapter = SignalAdapter()

# Disabled
adapter = SignalAdapter(enable_persistence=False)

# Custom repository (for testing)
adapter = SignalAdapter(signal_repository=custom_repo)
```

### Environment Requirements

Persistence requires:
- `SUPABASE_URL` in `.env`
- `SUPABASE_SERVICE_ROLE_KEY` in `.env`
- `SignalRepository` importable

If any requirement fails:
- Persistence auto-disables
- Warning logged
- Pipeline continues normally

---

## Testing

### Unit Tests

Run integration tests:

```bash
cd ~/Desktop/kaldra_core
pytest tests/integration/test_signal_persistence.py -v
```

Tests include:
- ✅ Signal persisted successfully
- ✅ Persistence failure doesn't break pipeline
- ✅ Disabled persistence works
- ✅ All fields included in payload

### Manual Testing

1. Run KALDRA with a simple input
2. Check Supabase Table Editor
3. Verify signal appears in `signals` table
4. Check fields are populated

---

## Monitoring

### Logs

**Success:**
```
[INFO] SignalAdapter: Persistence enabled
[DEBUG] SignalAdapter: Signal persisted with ID: abc-123...
```

**Warning (non-fatal):**
```
[WARNING] SignalAdapter: Failed to persist signal: {error}
```

**Error (non-fatal):**
```
[ERROR] SignalAdapter: Unexpected error persisting signal: Exception(...)
```

---

## Future Enhancements

Possible improvements for v2:
- Batch persistence
- Retry logic
- Async persistence
- Metrics/analytics
- Signal deduplication
- Partial update support

---

## Backward Compatibility

✅ **Fully backward compatible**
- Existing code continues working
- No API changes
- Persistence is optional
- Graceful degradation

---

## Summary

**What changed:**
- `SignalAdapter` now has `__init__()` method
- Automatic persistence after signal generation
- Graceful error handling

**What stayed the same:**
- `to_signal()` return value
- `to_compact_signal()` behavior
- Public API contract

**Net effect:**
- Every KALDRA signal is now saved to Supabase
- Zero breaking changes
- Pipeline reliability unchanged
