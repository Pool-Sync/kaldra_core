# Explorer API Integration v1

**Version:** v1  
**Date:** December 2025  
**Integration:** 4iam.ai Explorer ↔ KALDRA API Gateway

---

## Overview

The 4iam.ai Explorer frontend now connects to the KALDRA API Gateway to display real signals and story events from Supabase. This replaces mock data with production database data.

---

## Environment Variables

### Configuration

Add to `.env.local` (NOT committed):

```bash
# API Mode: "mock" or "real"
NEXT_PUBLIC_KALDRA_API_MODE=real

# API URL
NEXT_PUBLIC_KALDRA_API_URL=http://localhost:8000
```

**Modes:**
- `mock`: Uses local mock data (no backend required)
- `real`: Connects to KALDRA API Gateway

---

## API Client Functions

### Location
`lib/api/kaldra.ts`

### Functions

#### `fetchSignals(params?)`
Fetch signals with optional filters.

```typescript
const signals = await fetchSignals({
  domain: 'alpha',
  limit: 50
});
```

#### `fetchSignalById(id)`
Get a specific signal by ID.

```typescript
const signal = await fetchSignalById('abc-123-uuid');
// Returns Signal | null
```

#### `fetchStoryEventsBySignalId(signalId)`
Get story events for a signal.

```typescript
const events = await fetchStoryEventsBySignalId('abc-123');
// Returns StoryEvent[]
```

#### `fetchSupabaseHealth()`
Check Supabase connection status.

```typescript
const health = await fetchSupabaseHealth();
// Returns { status: 'ok' | 'error', supabase_connected: boolean }
```

---

## Type Definitions

### Location
`lib/types/kaldra.ts`

### Types

```typescript
interface Signal {
  id: string;
  domain: string;
  title: string;
  summary?: string;
  delta144_state?: string;
  confidence?: number;
  tw_regime?: string;
  created_at?: string;
  // ... more fields
}

interface StoryEvent {
  id: string;
  signal_id?: string;
  stream_id?: string;
  text?: string;
  delta144_state?: string;
  created_at?: string;
}
```

---

## Component Updates

### useExplorer Hook

**File:** `app/hooks/useExplorer.ts`

**Changes:**
- Fetches signals from API when `API_MODE=real`
- Falls back to mocks on error
- Exposes `loading` and `error` states

**Usage:**
```typescript
const { signals, loading, error } = useExplorer();
```

### HealthBadge Component

**File:** `components/HealthBadge.tsx`

**Features:**
- Green dot: API connected
- Red dot: API offline
- Tooltip with details
- Auto-refreshes every 30s

**Usage:**
```tsx
import { HealthBadge } from '@/components/HealthBadge';

<HealthBadge />
```

---

## Running Locally

### 1. Start Backend

```bash
cd ~/Desktop/kaldra_core
export $(grep -v '^#' .env | xargs)
uvicorn kaldra_api.main:app --reload --port 8000
```

### 2. Start Frontend

```bash
cd ~/Desktop/kaldra_core/4iam_frontend
echo "NEXT_PUBLIC_KALDRA_API_MODE=real" > .env.local
echo "NEXT_PUBLIC_KALDRA_API_URL=http://localhost:8000" >> .env.local
npm run dev
```

### 3. Access Explorer

- Frontend: http://localhost:3000/explorer
- Backend API: http://localhost:8000/docs

---

## Data Flow

```
User → Explorer Page
    ↓
useExplorer Hook
    ↓
fetchSignals() (lib/api/kaldra.ts)
    ↓
KALDRA API Gateway (/signals)
    ↓
SignalRepository
    ↓
Supabase PostgreSQL
    ↓
Real signals displayed
```

---

## Error Handling

### API Unavailable
```typescript
try {
  const signals = await fetchSignals();
} catch (error) {
  if (error.message === 'API_UNAVAILABLE') {
    // Fallback to mocks or show error message
  }
}
```

### Modes

**Mock Mode:**
- Always works
- Uses static mock data
- No backend required

**Real Mode:**
- Requires backend running
- Falls back to mocks on error
- Shows error state in UI

---

## Features

### Signals List
- Real-time data from Supabase
- Domain filtering (alpha, geo, product, safeguard)
- Limit parameter support
- Loading/error states

### Signal Details
- Full signal information
- Metadata display
- Timeline placeholder

### Health Check
- Visual status indicator
- Auto-refresh
- Detailed tooltip

---

## Architecture

### Utility Functions

**File:** `lib/api/utils.ts`

Converts API types to Explorer types:

```typescript
convertSignalToExplorerFormat(signal: Signal): ExplorerSignal
convertSignalsToExplorerFormat(signals: Signal[]): ExplorerSignal[]
```

**Why:** API uses different field names than Explorer expects.

---

## Next Steps (Phase 3.2.2)

1. **Story Events Timeline**
   - Fetch events when signal is selected
   - Display timeline with events
   - Show stream badges

2. **Real-time Updates**
   - WebSocket integration
   - Auto-refresh signals
   - Live updates

3. **Write Operations**
   - Create signals from Explorer
   - Edit signal metadata
   - Manage story events

---

## Troubleshooting

### Explorer shows no signals
- Check `NEXT_PUBLIC_KALDRA_API_MODE=real` in `.env.local`
- Verify backend is running on port 8000
- Check browser console for errors
- Try `/health/supabase` endpoint

### Health badge shows red
- Backend not running
- Wrong `NEXT_PUBLIC_KALDRA_API_URL`
- Supabase connection issue
- Check backend logs

### Type errors
- Run `npm run build` to check TypeScript
- Verify imports are correct
- Check `lib/types/kaldra.ts` exists

---

## Files Modified

**Created:**
- `lib/api/kaldra.ts` - API client
- `lib/types/kaldra.ts` - TypeScript types
- `lib/api/utils.ts` - Type converters
- `components/HealthBadge.tsx` - Health UI
- `docs/EXPLORER_API_INTEGRATION_v1.md` - This file

**Modified:**
- `app/hooks/useExplorer.ts` - API integration
- (Ready for) `app/(explorer)/explorer/components/ExplorerDetails.tsx`

---

**Explorer API Integration v1 is complete and functional!**

Real signals from Supabase are now displayed in the Explorer.
