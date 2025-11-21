# Integration Guide — 4IAM.AI

## 1. Objective

Guide for integrating the 4IAM.AI Dashboard with backend services, Visual Engine, and Design System.

**Status**: Integration specification — implementation TODO

## 2. Architecture Overview

```
┌─────────────────────────────────────────────┐
│         4IAM.AI Dashboard (Frontend)        │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  Pages   │  │Components│  │ Templates│ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘ │
│       │             │             │        │
│  ┌────┴─────────────┴─────────────┴─────┐ │
│  │      Design System + Visual Engine   │ │
│  └────────────────┬─────────────────────┘ │
└───────────────────┼───────────────────────┘
                    │
           ┌────────┴────────┐
           │   API Gateway   │
           └────────┬────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
┌───┴───┐     ┌────┴────┐    ┌────┴────┐
│ Alpha │     │   GEO   │    │ Product │
└───────┘     └─────────┘    └─────────┘
```

## 3. Backend API Integration

### API Gateway
**Base URL**: `http://localhost:8000/api/v1` (development)  
**Location**: `kaldra_api/`

### Authentication
```typescript
// TODO: Implement authentication
interface AuthConfig {
  apiKey?: string;
  bearerToken?: string;
  refreshToken?: string;
}
```

### API Client Setup
```typescript
// lib/api/client.ts (TODO: Create)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchAPI(endpoint: string, options?: RequestInit) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      // TODO: Add authentication headers
      ...options?.headers,
    },
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }
  
  return response.json();
}
```

### API Endpoints

#### Signals
```typescript
// GET /signals - List all signals
// GET /signals/{id} - Get signal details
// GET /signals/product/{product} - Filter by product
// POST /signals/search - Search signals

interface Signal {
  id: string;
  product: 'alpha' | 'geo' | 'product' | 'safeguard';
  title: string;
  content: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  timestamp: string;
  metadata: Record<string, any>;
}
```

#### Insights
```typescript
// GET /insights - List all insights
// GET /insights/{id} - Get insight details
// GET /insights/category/{category} - Filter by category
// POST /insights/search - Search insights

interface Insight {
  id: string;
  title: string;
  summary: string;
  content: string;
  category: string;
  product: string;
  publishedAt: string;
  author: string;
  tags: string[];
}
```

#### Products (Alpha, GEO, Product, Safeguard)
```typescript
// GET /alpha/dashboard - Alpha dashboard data
// GET /geo/dashboard - GEO dashboard data
// GET /product/dashboard - Product dashboard data
// GET /safeguard/dashboard - Safeguard dashboard data
```

## 4. Visual Engine Integration

### Template Usage
```typescript
// Import templates from visual_engine
import AlphaTemplate from '@/visual_engine/templates/alpha_template';
import GeoTemplate from '@/visual_engine/templates/geo_template';
import ProductTemplate from '@/visual_engine/templates/product_template';
import SafeguardTemplate from '@/visual_engine/templates/safeguard_template';
import DashboardTemplate from '@/visual_engine/templates/dashboard_template';
import ExplorerTemplate from '@/visual_engine/templates/kaldra_explorer_template';

// Use in pages
export default function AlphaPage() {
  return <AlphaTemplate data={data} />;
}
```

### Chart Components
```typescript
// Import charts from visual_engine
import Delta144Grid from '@/visual_engine/charts/delta144_grid';
import TW369Wave from '@/visual_engine/charts/tw369_wave';
import DriftMap from '@/visual_engine/charts/drift_map';
import KindraGlyphRenderer from '@/visual_engine/charts/kindra_glyph_renderer';

// Use in templates or pages
<Delta144Grid data={archetypeData} />
<TW369Wave data={waveData} />
```

## 5. Design System Integration

### Token Usage
```typescript
// Import design tokens
import colors from '@/design_system/tokens/colors.json';
import typography from '@/design_system/tokens/typography.json';
import spacing from '@/design_system/tokens/spacing.json';

// Tokens are also available via Tailwind CSS classes
// configured in tailwind.config.js
```

### Component Library
```typescript
// Import design system components
import { Button } from '@/design_system/components/button';
import { Card } from '@/design_system/components/card';
import { Input } from '@/design_system/components/input';

// Use in pages
<Button variant="primary">Click me</Button>
<Card>Content</Card>
```

## 6. Data Fetching Patterns

### Server Components (Recommended)
```typescript
// app/signals/page.tsx
export default async function SignalsPage() {
  const signals = await fetchAPI('/signals');
  
  return <SignalsList signals={signals} />;
}
```

### Client Components (for interactivity)
```typescript
'use client';

import { useState, useEffect } from 'react';

export default function SignalsFeed() {
  const [signals, setSignals] = useState([]);
  
  useEffect(() => {
    fetchAPI('/signals').then(setSignals);
  }, []);
  
  return <div>{/* Render signals */}</div>;
}
```

### Real-time Updates (Future)
```typescript
// TODO: Implement WebSocket connection
const ws = new WebSocket('ws://localhost:8000/ws/signals');

ws.onmessage = (event) => {
  const signal = JSON.parse(event.data);
  // Update UI with new signal
};
```

## 7. State Management

### Options
1. **React Context** - For simple global state
2. **Zustand** - For medium complexity
3. **Redux Toolkit** - For complex state management

### Recommendation
Start with React Context, migrate to Zustand if needed.

```typescript
// TODO: Create context for user preferences
// contexts/preferences.tsx
```

## 8. Environment Variables

### Required Variables
```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_ENV=development

# Optional
NEXT_PUBLIC_ANALYTICS_ID=
NEXT_PUBLIC_SENTRY_DSN=
```

## 9. Development Workflow

### Setup
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run with backend
# Terminal 1: Start backend (kaldra_api)
cd ../kaldra_api
python -m uvicorn main:app --reload

# Terminal 2: Start frontend
npm run dev
```

### Testing Integration
```bash
# Test API connection
curl http://localhost:8000/api/v1/health

# Test frontend
open http://localhost:3000
```

## 10. Deployment

### Build
```bash
npm run build
npm start
```

### Environment-specific Configuration
- **Development**: Local API, debug mode
- **Staging**: Staging API, analytics enabled
- **Production**: Production API, optimizations enabled

## 11. TODO

- [ ] Create API client library
- [ ] Implement authentication flow
- [ ] Set up error handling
- [ ] Add request caching
- [ ] Implement retry logic
- [ ] Add loading states
- [ ] Create error boundaries
- [ ] Set up analytics
- [ ] Configure monitoring
- [ ] Add performance tracking
- [ ] Implement WebSocket connection
- [ ] Create state management solution
- [ ] Add request interceptors
- [ ] Implement request queuing
- [ ] Add offline support (future)
