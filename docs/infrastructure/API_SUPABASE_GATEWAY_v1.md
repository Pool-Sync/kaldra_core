# KALDRA API Supabase Gateway v1

**Version:** v1  
**Date:** December 2025  
**Integration:** FastAPI ↔ Supabase

---

## Overview

The KALDRA API Gateway now exposes REST endpoints for signals and story events stored in Supabase. This provides external access to the KALDRA persistence layer.

---

## Architecture

```
Client (curl/browser/frontend)
    ↓
FastAPI Router
    ↓
SignalRepository / StoryEventRepository
    ↓
SupabaseClient
    ↓
Supabase PostgreSQL
```

---

## Endpoints

### Signals

#### `GET /signals`
List signals with optional filters.

**Query Parameters:**
- `domain` (optional): Filter by domain ("alpha", "geo", "product", "safeguard")
- `limit` (optional): Max results (default 20, max 100)

**Example:**
```bash
curl "http://localhost:8000/signals?domain=alpha&limit=10"
```

**Response:**
```json
[
  {
    "id": "uuid-here",
    "domain": "alpha",
    "title": "Signal title",
    "importance": 0.85,
    "created_at": "2025-12-06T..."
  }
]
```

#### `GET /signals/{signal_id}`
Get a specific signal by ID.

**Path Parameters:**
- `signal_id`: Signal UUID

**Example:**
```bash
curl "http://localhost:8000/signals/abc-123-uuid"
```

**Response:**
```json
{
  "id": "abc-123-uuid",
  "domain": "alpha",
  "title": "Signal title",
  "summary": "Description...",
  "importance": 0.85,
  "delta144_state": "threshold",
  "raw_payload": {...}
}
```

**Status Codes:**
- `200`: Success
- `404`: Signal not found
- `503`: Database error

---

### Story Events

#### `GET /story-events/by-signal/{signal_id}`
List story events for a specific signal.

**Path Parameters:**
- `signal_id`: Parent signal UUID

**Query Parameters:**
- `limit` (optional): Max results (default 50, max 200)

**Example:**
```bash
curl "http://localhost:8000/story-events/by-signal/abc-123?limit=20"
```

**Response:**
```json
[
  {
    "id": "event-uuid",
    "signal_id": "abc-123",
    "stream_id": "twitter",
    "text": "Event description",
    "delta144_state": "threshold",
    "polarities": {"order": 0.7, "chaos": 0.3},
    "created_at": "2025-12-06T..."
  }
]
```

#### `GET /story-events`
List story events with optional filters.

**Query Parameters:**
- `stream_id` (optional): Filter by stream
- `limit` (optional): Max results (default 50, max 200)

**Example:**
```bash
curl "http://localhost:8000/story-events?stream_id=nyt&limit=10"
```

---

### Health Checks

#### `GET /health`
Basic health check (existing).

**Response:**
```json
{"status": "ok"}
```

#### `GET /health/supabase`
Supabase connectivity check (new).

**Response (success):**
```json
{
  "status": "ok",
  "supabase_connected": true,
  "signals_sample_count": 5
}
```

**Response (error):**
```json
{
  "status": "error",
  "supabase_connected": false,
  "error": "Connection failed"
}
```

---

## Running Locally

### 1. Start the API

```bash
cd ~/Desktop/kaldra_core
export $(grep -v '^#' .env | xargs)
uvicorn kaldra_api.main:app --reload --port 8000
```

### 2. Access endpoints

- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Supabase health: http://localhost:8000/health/supabase
- Signals: http://localhost:8000/signals
- Events: http://localhost:8000/story-events

---

## Testing

### Run Tests

```bash
cd ~/Desktop/kaldra_core
export $(grep -v '^#' .env | xargs)
pytest tests/api -v
```

### Test Coverage

**Signals API:**
- ✅ List signals returns 200
- ✅ List with domain filter
- ✅ Get signal by ID (404 for not found)
- ✅ Supabase health check

**Story Events API:**
- ✅ List events by signal returns 200
- ✅ List all events
- ✅ Filter by stream
- ✅ Limit parameter respected

---

## curl Examples

### List all signals
```bash
curl "http://localhost:8000/signals"
```

### Filter signals by domain
```bash
curl "http://localhost:8000/signals?domain=alpha&limit=5"
```

### Get specific signal
```bash
curl "http://localhost:8000/signals/YOUR-UUID-HERE"
```

### Get events for a signal
```bash
curl "http://localhost:8000/story-events/by-signal/YOUR-SIGNAL-UUID"
```

### List events by stream
```bash
curl "http://localhost:8000/story-events?stream_id=twitter&limit=20"
```

### Check Supabase connectivity
```bash
curl "http://localhost:8000/health/supabase"
```

---

## Error Handling

### 404 Not Found
Signal ID doesn't exist in database.

```json
{
  "detail": "Signal not found"
}
```

### 503 Service Unavailable
Database connection or query error.

```json
{
  "detail": "Database error: Connection timeout"
}
```

---

## Dependencies

### Required
- FastAPI
- `SignalRepository` (src/data/repositories)
- `StoryEventRepository` (src/data/repositories)
- `SupabaseClient` (src/infrastructure)
- Environment variables configured in `.env`

### Optional
- `uvicorn` for local development

---

## Integration Points

### Frontend Dashboard
Can consume these endpoints to display:
- Signal timeline
- Story event narratives
- Real-time updates

### External Tools
- Analytics platforms
- Monitoring dashboards
- Data export tools

---

## Security Considerations

**Current Implementation:**
- No authentication (internal API)
- Read-only endpoints
- Uses SERVICE_ROLE_KEY (backend only)

**Production TODO:**
- Add API key authentication
- Rate limiting
- CORS configuration
- Request validation

---

## Next Steps (Phase 3.2)

1. Connect 4iam.ai Explorer to these endpoints
2. Add real-time WebSocket support
3. Implement pagination with cursors
4. Add filtering by date ranges
5. Create endpoints for analytics aggregations

---

## Files Modified

**Created:**
- `kaldra_api/routers/router_signals.py`
- `kaldra_api/routers/router_story_events.py`
- `tests/api/test_signals_api.py`
- `tests/api/test_story_events_api.py`
- `docs/infrastructure/API_SUPABASE_GATEWAY_v1.md`

**Modified:**
- `kaldra_api/dependencies.py` - Added repository getters
- `kaldra_api/main.py` - Registered routers + health check

---

**KALDRA API Gateway Phase 3.1 is complete!**

All signals and story events in Supabase are now accessible via REST API.
