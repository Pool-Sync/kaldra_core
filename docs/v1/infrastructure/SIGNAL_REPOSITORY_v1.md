# Signal Repository v1 - Documentation

**Version:** v1  
**Date:** December 2025  
**Location:** `src/data/repositories/signal_repository.py`

---

## Overview

`SignalRepository` is the **official high-level interface** for all signal operations in KALDRA. All pipeline components should use this repository instead of directly accessing the SupabaseClient.

---

## Architecture

```
KALDRA Pipeline
    ↓
SignalRepository (high-level)
    ↓
SupabaseClient (low-level REST)
    ↓
Supabase Database
```

---

## Usage

### Initialize

```python
from src.data.repositories.signal_repository import SignalRepository

repo = SignalRepository()  # Uses default SupabaseClient
```

### List Signals

```python
# Get all signals (limit 50)
signals = repo.list_signals()

# Filter by domain
alpha_signals = repo.list_signals(domain="alpha", limit=20)

# Check for errors
if "error" in signals:
    print(f"Error: {signals}")
else:
    for signal in signals:
        print(signal['title'])
```

### Get Signal by ID

```python
signal = repo.get_signal_by_id("some-uuid-here")

if isinstance(signal, list) and len(signal) > 0:
    print(signal[0]['title'])
```

### Create Signal

```python
import uuid

data = {
    "id": str(uuid.uuid4()),  # Optional - DB can generate
    "domain": "alpha",
    "title": "Breaking News Signal",
    "summary": "Important narrative event detected",
    "importance": 0.85,
    "confidence": 0.92,
    "delta144_state": "threshold",
    "dominant_archetype": "hero",
    "raw_payload": {
        "source": "kaldra_pipeline",
        "version": "3.4"
    }
}

result = repo.create_signal(data)

if "error" not in result:
    print("Signal created successfully")
```

### Upsert Signal

```python
data = {
    "id": "existing-uuid",
    "title": "Updated Title",
    "importance": 0.95
}

result = repo.upsert_signal(data)
```

### Delete Signal

```python
result = repo.delete_signal("signal-uuid")

if "error" not in result:
    print("Signal deleted")
```

---

## API Reference

### Methods

#### `list_signals(domain=None, limit=50)`
List signals with optional filtering.

**Args:**
- `domain` (str, optional): Filter by domain
- `limit` (int): Maximum results (default: 50)

**Returns:** List of signals or error dict

#### `get_signal_by_id(signal_id)`
Get a specific signal.

**Args:**
- `signal_id` (str): Signal UUID

**Returns:** List with signal or error dict

#### `create_signal(data)`
Create a new signal.

**Args:**
- `data` (dict): Signal data

**Returns:** Created signal or error dict

#### `upsert_signal(data)`
Insert or update a signal.

**Args:**
- `data` (dict): Signal data (must include `id` for update)

**Returns:** Upserted signal or error dict

#### `delete_signal(signal_id)`
Delete a signal.

**Args:**
- `signal_id` (str): Signal UUID

**Returns:** Success response or error dict

---

## Expected Fields

### Required
- `domain` (str): "alpha", "geo", "product", or "safeguard"
- `title` (str): Signal title

### Optional
- `id` (uuid): Auto-generated if not provided
- `summary` (str): Brief description
- `source_anchor` (str): Source identifier
- `source_url` (str): Source URL
- `delta144_state` (str): Delta144 state
- `dominant_archetype` (str): Primary archetype
- `dominant_polarity` (str): Primary polarity
- `tw_regime` (str): TW369 regime
- `journey_stage` (str): Hero's journey stage
- `importance` (float): 0-1
- `confidence` (float): 0-1
- `divergence` (float): 0-1
- `raw_payload` (jsonb): Full KALDRA output

---

## Testing

Run the test script:

```bash
cd ~/Desktop/kaldra_core
python3 -m src.scripts.test_signal_repository
```

Expected flow:
1. ✅ List existing signals
2. ✅ Create test signal
3. ✅ Retrieve by ID
4. ✅ Delete test signal

---

## Error Handling

All methods return structured responses. Always check for errors:

```python
result = repo.create_signal(data)

if "error" in result:
    print(f"Failed: {result['error']} - {result['message']}")
else:
    print("Success!")
```

---

## Integration with KALDRA Pipeline

This repository will be used by:
- Signal processing stages
- Story engine persistence
- Analytics aggregation
- Dashboard API endpoints
- Export/import utilities

---

## Next Steps

1. Test with real KALDRA signals
2. Add batch operations
3. Add query helpers (by state, by archetype, etc.)
4. Add statistics methods
