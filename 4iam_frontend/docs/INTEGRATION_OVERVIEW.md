# API Integration Overview — 4IAM.AI

## Current Status: MOCK MODE

The 4IAM.AI frontend is currently running in **MOCK MODE**, using local mock data instead of real API calls. This allows full development and testing of the UI without requiring the KALDRA API Gateway to be running.

---

## Architecture

```
┌─────────────────────────────────────────┐
│     4IAM.AI Frontend (Next.js)          │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   Pages (Alpha, GEO, etc.)       │  │
│  └──────────┬───────────────────────┘  │
│             │                           │
│  ┌──────────▼───────────────────────┐  │
│  │   React Hooks                    │  │
│  │   - useSignals()                 │  │
│  │   - useInsights()                │  │
│  │   - useExplorerFeed()            │  │
│  └──────────┬───────────────────────┘  │
│             │                           │
│  ┌──────────▼───────────────────────┐  │
│  │   API Client                     │  │
│  │   (Mock / Real switch)           │  │
│  └──────────┬───────────────────────┘  │
│             │                           │
│  ┌──────────▼───────────────────────┐  │
│  │   Mock Data (local)              │  │
│  │   OR                             │  │
│  │   Real API (future)              │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

## Files Created

### API Infrastructure

#### `app/lib/api/types.ts`
TypeScript interfaces for all KALDRA data structures:
- `Signal` - Real-time intelligence signals
- `Insight` - In-depth reports and analysis
- `ExplorerFeedItem` - Symbolic visualization data
- `ServiceKey` - Type for KALDRA services (alpha, geo, product, safeguard)
- `TWRegime` - Tracy-Widom regime types
- API response wrappers and error types

#### `app/lib/api/config.ts`
Configuration for API endpoints and settings:
- `API_ENDPOINTS` - Endpoint paths for each service
- `API_CONFIG` - Global API configuration
  - `useMocks: true` - **Currently in mock mode**
  - `baseUrl` - API Gateway URL (for future use)
  - Timeout and retry settings
- Service names and descriptions

#### `app/lib/api/mock_data.ts`
Comprehensive mock data for all services:
- **Alpha**: 5 signals, 1 insight (earnings intelligence)
- **GEO**: 4 signals, 1 insight (geopolitical intelligence)
- **Product**: 3 signals, 1 insight (product intelligence)
- **Safeguard**: 3 signals, 1 insight (risk intelligence)
- **Explorer**: 3 feed items (symbolic data)

Each signal includes:
- Title, summary, source
- Archetype ID (1-12)
- Δ144 state (1-144)
- Kindra vector
- TW regime (STABLE/TURBULENT/CRITICAL)
- Confidence score
- Priority level
- Entities and tags

#### `app/lib/api/client.ts`
Main API client with two implementations:
- **MockApiClient** (currently active) - Returns mock data with simulated network delay
- **RealApiClient** (future) - Will make real HTTP requests to KALDRA API Gateway

The client automatically switches based on `API_CONFIG.useMocks`.

### React Hooks

#### `app/hooks/useSignals.ts`
Hook for fetching signals from KALDRA services.
```tsx
const { signals, loading, error, refetch } = useSignals('alpha');
```

#### `app/hooks/useInsights.ts`
Hook for fetching insights from KALDRA services.
```tsx
const { insights, loading, error, refetch } = useInsights('geo');
```

#### `app/hooks/useExplorerFeed.ts`
Hook for fetching explorer feed data.
```tsx
const { feed, loading, error, refetch } = useExplorerFeed();
```

All hooks provide:
- Data array
- Loading state
- Error handling
- Refetch function

---

## Pages Updated

All pages now consume mock data via hooks:

1. **Dashboard** (`/dashboard`) - Unified view of all products with metrics
2. **Alpha** (`/alpha`) - Earnings intelligence signals and insights
3. **GEO** (`/geo`) - Geopolitical signals and insights
4. **Product** (`/product`) - Product intelligence signals and insights
5. **Safeguard** (`/safeguard`) - Risk intelligence signals and insights
6. **Signals** (`/signals`) - All signals with filtering by product
7. **Insights** (`/insights`) - All insights with filtering by product

Each page displays:
- Signal cards with metadata (archetype, Δ144 state, TW regime, confidence)
- Insight cards with author, read time, views
- Loading states
- Error handling
- Priority badges
- Entity tags

---

## How to Run

### Development Mode (Mock Data)

```bash
cd 4iam_frontend
npm run dev
```

Open http://localhost:3000

The app will run with mock data. No backend required.

### View Different Pages

- Dashboard: http://localhost:3000/dashboard
- Alpha: http://localhost:3000/alpha
- GEO: http://localhost:3000/geo
- Product: http://localhost:3000/product
- Safeguard: http://localhost:3000/safeguard
- Signals: http://localhost:3000/signals
- Insights: http://localhost:3000/insights

---

## Switching to Real API

When the KALDRA API Gateway is ready, follow these steps:

### 1. Update Configuration

Edit `app/lib/api/config.ts`:

```typescript
export const API_CONFIG = {
  baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  useMocks: false, // ← Change this to false
  // ... rest of config
};
```

### 2. Set Environment Variable

Create `.env.local`:

```bash
NEXT_PUBLIC_API_URL=https://api.kaldra.io/v1
```

### 3. Implement Real API Client

Edit `app/lib/api/client.ts` and implement the `RealApiClient` methods:

```typescript
async getSignals(source?: ServiceKey): Promise<ApiResponse<Signal[]>> {
  const endpoint = source 
    ? `${this.baseUrl}/signals?source=${source}` 
    : `${this.baseUrl}/signals`;
  
  const response = await fetch(endpoint);
  
  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }
  
  return response.json();
}
```

Repeat for all methods:
- `getSignalById()`
- `getInsights()`
- `getInsightById()`
- `getExplorerFeed()`

### 4. Test

```bash
npm run dev
```

The app will now fetch data from the real API Gateway.

---

## Adding a New Service

To add a new KALDRA service (e.g., `kaldra_meta`):

### 1. Update Types

Edit `app/lib/api/types.ts`:

```typescript
export type ServiceKey = 'alpha' | 'geo' | 'product' | 'safeguard' | 'meta';
```

### 2. Update Configuration

Edit `app/lib/api/config.ts`:

```typescript
export const API_ENDPOINTS: Record<ServiceKey, { basePath: string }> = {
  // ... existing services
  meta: { basePath: '/api/meta' },
};

export const SERVICE_NAMES: Record<ServiceKey, string> = {
  // ... existing services
  meta: 'KALDRA Meta',
};
```

### 3. Add Mock Data

Edit `app/lib/api/mock_data.ts`:

```typescript
export const mockMetaSignals: Signal[] = [
  // ... mock signals for meta service
];

// Update getMockSignals() function
export function getMockSignals(source: ServiceKey): Signal[] {
  switch (source) {
    // ... existing cases
    case 'meta':
      return mockMetaSignals;
  }
}
```

### 4. Create Page

Create `app/meta/page.tsx`:

```tsx
'use client';

import { useSignals } from '../hooks/useSignals';

export default function MetaPage() {
  const { signals, loading, error } = useSignals('meta');
  // ... render signals
}
```

---

## API Endpoint Contract

The real API Gateway should implement these endpoints:

### Signals

```
GET /api/v1/signals
GET /api/v1/signals?source=alpha
GET /api/v1/signals/{id}
```

Response format:
```json
{
  "data": [...],
  "timestamp": "2024-01-01T00:00:00Z",
  "source": "alpha"
}
```

### Insights

```
GET /api/v1/insights
GET /api/v1/insights?source=geo
GET /api/v1/insights/{id}
```

### Explorer Feed

```
GET /api/v1/explorer
GET /api/v1/explorer?source=product
```

---

## Error Handling

All hooks include error handling:

```tsx
const { signals, loading, error } = useSignals('alpha');

if (error) {
  return <div>Error: {error.message}</div>;
}
```

Errors are caught and displayed to the user.

---

## Future Enhancements

- [ ] Add authentication (JWT tokens)
- [ ] Implement request caching
- [ ] Add retry logic for failed requests
- [ ] Implement real-time updates (WebSocket)
- [ ] Add pagination for large datasets
- [ ] Implement search functionality
- [ ] Add request/response interceptors
- [ ] Create error boundary components
- [ ] Add analytics tracking
- [ ] Implement offline mode

---

## Summary

✅ **Complete API infrastructure created**
✅ **All pages integrated with mock data**
✅ **Ready to switch to real API**
✅ **No external dependencies required**
✅ **Fully functional in development mode**

The frontend is now fully functional with mock data and ready to connect to the KALDRA API Gateway when available.
