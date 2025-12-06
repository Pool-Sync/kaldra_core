# KALDRA Supabase Client v1 - Documentation

**Version:** v1  
**Date:** December 2025  
**Location:** `src/infrastructure/supabase_client.py`

---

## Overview

The `SupabaseClient` class is the **official database interface** for all KALDRA modules. It provides a simple REST-based API for interacting with Supabase tables.

---

## Features

✅ **REST-based:** Uses standard HTTP methods  
✅ **Environment-driven:** Reads from `.env`  
✅ **Service role:** Uses SERVICE_ROLE_KEY for full access  
✅ **Error handling:** Returns structured error responses  
✅ **No dependencies:** Uses only Python stdlib (`urllib`)

---

## Usage

### Initialization

```python
from src.infrastructure.supabase_client import SupabaseClient

client = SupabaseClient()
```

### Fetch Records

```python
# Get all records
result = client.fetch("signals")

# With filters
result = client.fetch("signals", "select=*&domain=eq.alpha&limit=10")

# With specific columns
result = client.fetch("signals", "select=id,title,domain")
```

### Insert Record

```python
data = {
    "domain": "alpha",
    "title": "New Signal",
    "summary": "Test signal",
    "importance": 0.8
}

result = client.insert("signals", data)
```

### Upsert Record

```python
data = {
    "id": "some-uuid",
    "domain": "alpha",
    "title": "Updated Signal"
}

result = client.upsert("signals", data)
```

### Delete Record

```python
# Delete by ID
result = client.delete("signals", {"id": "some-uuid"})

# Delete by filter
result = client.delete("signals", {"domain": "alpha"})
```

---

## API Methods

### `fetch(table, params="select=*")`
Retrieve records from a table.

**Returns:** List of records or error dict

### `insert(table, data)`
Insert a new record.

**Returns:** Created record or error dict

### `upsert(table, data)`
Insert or update record (conflicts on `id`).

**Returns:** Upserted record or error dict

### `delete(table, match)`
Delete records matching filters.

**Returns:** Success response or error dict

---

## Error Handling

All methods return a dict. Check for `"error"` key:

```python
result = client.fetch("signals")

if "error" in result:
    print(f"Error: {result['error']} - {result['message']}")
else:
    # Success
    for signal in result:
        print(signal['title'])
```

---

## Environment Variables

Required in `.env`:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

---

## Testing

Run the test script:

```bash
cd /Users/niki/Desktop/kaldra_core
python3 -m src.scripts.test_kaldra_supabase_client
```

Expected output:
```
🔧 Testing KALDRA Supabase Client v1...
✅ Client initialized
→ URL: https://fyeyarxszwaeirtqqkmi.supabase.co

📊 Testing fetch on 'signals' table...
✅ Fetch successful
→ Returned 0 rows

👤 Testing fetch on 'profiles' table...
✅ Profiles fetch successful
→ Returned 0 profiles

🎉 KALDRA Supabase Client is working!
```

---

## Integration Points

This client will be used by:
- Signal processing pipeline
- Story engine persistence
- Profile management
- Analytics queries
- Dashboard backend

---

## Next Steps

1. Test the client with sample data
2. Integrate into signal processing
3. Add batch operations
4. Add transaction support
