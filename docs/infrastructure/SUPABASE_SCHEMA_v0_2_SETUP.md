# Supabase Core Schema v0.2 - Manual Setup Instructions

**Status:** ⏳ AWAITING MANUAL SQL EXECUTION  
**Date:** December 2025

---

## Migration File Created

Location: `supabase/migrations/0001_init_kaldra_core.sql`

This file contains SQL to create:
- `profiles` table
- `signals` table
- `story_events` table
- Performance indexes

---

## Manual Steps Required

### 1. Open Supabase Dashboard

Navigate to your project: `4iam-dashboard-prod`

### 2. Execute SQL Migration

1. Go to **SQL Editor**
2. Create a new script
3. Copy contents of `supabase/migrations/0001_init_kaldra_core.sql`
4. Paste into editor
5. Click **Run**

### 3. Verify Tables Created

Go to **Database → Table Editor**

You should see:
- ✅ `profiles`
- ✅ `signals`
- ✅ `story_events`

---

## Backend Integration

Once tables are created, these endpoints will work:

```bash
# List all signals
GET /api/signals

# List signals by domain
GET /api/signals?domain=alpha

# Get single signal
GET /api/signals/{signal_id}

# Get story events for signal
GET /api/signals/{signal_id}/events
```

---

## Models Created

Backend models aligned with schema:
- `src/domain/models/profile.py`
- `src/domain/models/signal_record.py`
- `src/domain/models/story_event_record.py`

---

## Repository Methods

Added to `SupabaseRepository`:
- `list_profiles()`
- `list_signals(domain, limit)`
- `get_signal(signal_id)`
- `list_story_events_for_signal(signal_id, limit)`

---

## Next Steps

After SQL execution:
1. Test endpoint: `GET /api/signals`
2. Populate with sample data
3. Connect to frontend dashboard
