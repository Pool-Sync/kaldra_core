# KALDRA Full Pipeline Smoke Test v1

**Version:** v1  
**Date:** December 2025  
**Script:** `src/scripts/test_full_pipeline.py`

---

## Overview

This script performs an end-to-end smoke test of the KALDRA → Supabase persistence layer:

1. **Creates a test signal** via `SignalRepository`
2. **Creates multiple story events** linked to that signal via `StoryEventRepository`
3. **Reads the events back** from Supabase to validate persistence
4. **Cleans up all test data** (events → signal)

It validates that:

- Environment variables are correctly configured
- Supabase is reachable and responsive
- Both repositories work as expected
- Foreign key relations between `signals` and `story_events` are consistent
- Cascade operations work properly

---

## How to Run

From the project root:

```bash
cd ~/Desktop/kaldra_core
export $(grep -v '^#' .env | xargs)
python3 -m src.scripts.test_full_pipeline
```

---

## Expected Output

Successful execution shows:

```
🧪 Testing FULL KALDRA → Supabase pipeline (signals + story_events)...

🔧 Checking environment variables...
✅ Environment configured
   URL: https://your-project.supabase.co...

🧱 Initializing repositories...
✅ SignalRepository initialized
✅ StoryEventRepository initialized

➕ Creating test signal...
   ID: abc-123-...
✅ Signal created successfully
   Title: Full pipeline test signal

🧩 Creating story events linked to signal...
✅ Story events created successfully
   Count: 3 events

🔍 Validating: fetching story events by signal_id...
✅ Retrieved 3 story events for signal_id=abc-123...
✅ Event count matches!

📝 Sample event:
   Text: Hero receives the call to adventure.
   State: threshold
   Stream: test-stream-console

🎉 FULL PIPELINE TEST PASSED — signal + story_events persisted successfully!

🧹 Cleaning up test data...
✅ Story events deleted
✅ Signal deleted

✨ Test complete!
```

---

## What Gets Tested

### 1. Environment Configuration
- `SUPABASE_URL` exists
- `SUPABASE_SERVICE_ROLE_KEY` exists
- Variables are loadable

### 2. Repository Initialization
- `SignalRepository` can be instantiated
- `StoryEventRepository` can be instantiated
- SupabaseClient connects successfully

### 3. Signal Persistence
- Create signal with full payload
- Signal ID is preserved
- All fields are stored correctly

### 4. Story Events Persistence
- Bulk create multiple events
- Events link to parent signal via FK
- All event fields stored correctly

### 5. Query Operations
- Fetch events by `signal_id`
- Results match expected count
- Data integrity maintained

### 6. Cleanup Operations
- Delete events by signal (cascade)
- Delete signal
- No orphaned data left

---

## Error Scenarios

### Missing Environment Variables
```
❌ Environment variable not found: SUPABASE_URL
💡 Make sure to load .env: export $(grep -v '^#' .env | xargs)
```

**Fix:** Load environment variables or check `.env` file

### Supabase Connection Failed
```
❌ Initialization error: Failed to initialize SupabaseClient
```

**Fix:** Check Supabase URL and keys, verify network connectivity

### Signal Creation Failed
```
❌ Failed to create signal: {'error': 500, 'message': '...'}
```

**Fix:** Check table schema, verify permissions

### Event Count Mismatch
```
⚠️  WARNING: Expected 3 events, got 2
```

**Fix:** Check bulk insert, verify FK constraints

---

## Test Data

### Signal
```python
{
    "id": "<uuid>",
    "domain": "alpha",
    "title": "Full pipeline test signal",
    "summary": "Signal created by test_full_pipeline.py...",
    "importance": 0.9,
    "confidence": 0.85,
    "delta144_state": "threshold",
    "dominant_archetype": "hero",
    "dominant_polarity": "order",
    "tw_regime": "STABLE",
    "journey_stage": "call_to_adventure"
}
```

### Story Events (3)
1. **Call to Adventure** - threshold state, order-dominant
2. **Refusal of Call** - tension state, chaos-dominant
3. **Meeting Mentor** - emergence state, order-dominant

---

## Integration Points

This test validates the entire persistence stack:

```
test_full_pipeline.py
    ↓
SignalRepository
    ↓
SupabaseClient (signals table)
    ↓
StoryEventRepository
    ↓
SupabaseClient (story_events table)
    ↓
Supabase PostgreSQL
```

---

## Cleanup Guarantee

The script **always** attempts cleanup in a `finally` block:

- Events deleted first (FK dependency)
- Signal deleted second
- Errors logged but don't fail the test
- No test data left in database

---

## Use Cases

### Pre-Deployment Validation
Run before deploying to verify Supabase integration

### Environment Setup Check
Validate new environment has correct configuration

### CI/CD Integration
Include in automated test suite

### Debugging
Manually verify persistence layer is working

---

## Requirements

- Python 3.7+
- `.env` file with valid Supabase credentials
- Internet connection to Supabase
- Tables `signals` and `story_events` exist in Supabase

---

## Limitations

- **Not a unit test** - requires real Supabase connection
- **Network dependent** - fails if Supabase is unreachable
- **Manual execution** - not part of pytest suite
- **Destructive** - creates and deletes real database records

---

## Next Steps

After successful test:

1. ✅ Persistence layer is working
2. ✅ Ready for KALDRA pipeline integration
3. ✅ Can safely persist production signals
4. ✅ Story events will be captured automatically

---

## Troubleshooting

### Test hangs
- Check network connection
- Verify Supabase is not rate-limiting
- Check firewall rules

### Cleanup fails
- Manually delete test data from Supabase dashboard
- Check cascade delete is enabled on FK

### Events not found
- Verify FK constraint exists
- Check `signal_id` matches
- Validate bulk insert worked

---

**This test confirms the complete KALDRA → Supabase persistence pipeline is operational!**
