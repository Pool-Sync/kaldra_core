# KALDRA Explorer - Technical Overview

## Introduction

The **KALDRA Explorer** is the internal workstation for the 4IAM.AI platform. It serves as the unified interface for navigating, filtering, and analyzing signals across all KALDRA domains:

- **KALDRA Alpha** - Earnings and financial signals
- **KALDRA GEO** - Geopolitical events and trends
- **KALDRA Product** - Brand, consumer, and cultural signals
- **KALDRA Safeguard** - Toxic narratives and misinformation detection

## Architecture

### Directory Structure

```
app/(explorer)/explorer/
├── page.tsx                     # Main Explorer page
├── layout.tsx                   # Base layout
├── components/
│   ├── ExplorerSidebar.tsx      # Domain filters and navigation
│   ├── ExplorerTimeline.tsx     # Visual timeline with TW regime indicators
│   ├── ExplorerList.tsx         # Signal card list
│   └── ExplorerDetails.tsx      # Signal detail modal
└── lib/
    ├── explorer.types.ts        # TypeScript type definitions
    ├── explorer.mock.ts         # Mock data (development only)
    └── explorer.utils.ts        # Utility functions

app/hooks/
└── useExplorer.ts               # React hook for Explorer state management
```

### Data Flow

```
┌─────────────────┐
│  Explorer Page  │
└────────┬────────┘
         │
         ├─► useExplorer Hook
         │   ├─► Mock Data (current)
         │   └─► API Gateway (future)
         │
         ├─► ExplorerSidebar (filters)
         ├─► ExplorerTimeline (visualization)
         ├─► ExplorerList (signal cards)
         └─► ExplorerDetails (modal)
```

## Core Types

### ExplorerSignal

The fundamental data structure representing a KALDRA signal:

```typescript
interface ExplorerSignal {
  id: string;                    // Unique signal identifier
  source: ExplorerSource;        // 'alpha' | 'geo' | 'product' | 'safeguard'
  title: string;                 // Signal headline
  summary: string;               // Detailed description
  archetype_id: string;          // Δ144 archetype reference
  delta144_state: string;        // Current Δ144 state
  kindra_vector: string;         // Kindra classification
  tw_regime: TWRegime;           // 'STABLE' | 'TURBULENT' | 'CRITICAL'
  confidence: number;            // 0.0 - 1.0
  timestamp: string;             // ISO 8601 format
}
```

### ExplorerFilters

Filter criteria for signal queries:

```typescript
interface ExplorerFilters {
  source?: ExplorerSource | 'all';
  regime?: TWRegime | 'all';
  dateFrom?: string;
  dateTo?: string;
  minConfidence?: number;
}
```

### ExplorerTimelinePoint

Aggregated timeline data:

```typescript
interface ExplorerTimelinePoint {
  timestamp: string;             // Date (YYYY-MM-DD)
  regime: TWRegime;              // Dominant regime for the day
  count: number;                 // Number of signals
  signals: ExplorerSignal[];     // All signals for this point
}
```

## Components

### ExplorerSidebar

**Purpose**: Domain filtering and navigation

**Features**:
- Filter by KALDRA domain (Alpha, GEO, Product, Safeguard)
- "All Signals" view
- Signal count per domain
- Dark/light mode support

**Props**:
```typescript
{
  filters: ExplorerFilters;
  onFilterChange: (filters: ExplorerFilters) => void;
  stats: ExplorerStats;
}
```

### ExplorerTimeline

**Purpose**: Visual timeline of signal distribution

**Features**:
- Chronological signal visualization
- Color-coded by TW regime:
  - 🟢 Green = STABLE
  - 🟡 Yellow = TURBULENT
  - 🔴 Red = CRITICAL
- Hover for details
- Click to filter by date

**Props**:
```typescript
{
  timeline: ExplorerTimelinePoint[];
  onPointClick?: (point: ExplorerTimelinePoint) => void;
}
```

### ExplorerList

**Purpose**: Display signals as interactive cards

**Features**:
- Scrollable signal list
- Click to view details
- Shows key metadata (regime, confidence, Δ144 state)
- Visual regime indicator
- Timestamp formatting

**Props**:
```typescript
{
  signals: ExplorerSignal[];
  onSignalClick: (signal: ExplorerSignal) => void;
  selectedSignalId?: string | null;
}
```

### ExplorerDetails

**Purpose**: Full signal detail modal

**Features**:
- Modal overlay
- Complete signal metadata
- Formatted timestamps
- Close on backdrop click or button
- Responsive design

**Props**:
```typescript
{
  signal: ExplorerSignal | null;
  onClose: () => void;
}
```

## Hooks

### useExplorer

**Purpose**: Centralized state management for Explorer

**Returns**:
```typescript
{
  // Data
  signals: ExplorerSignal[];
  timeline: ExplorerTimelinePoint[];
  stats: ExplorerStats;
  selectedSignal: ExplorerSignal | null;
  
  // Filters
  filters: ExplorerFilters;
  setFilters: (filters: ExplorerFilters) => void;
  
  // Selection
  selectedSignalId: string | null;
  setSelectedSignalId: (id: string | null) => void;
  
  // Actions
  clearFilters: () => void;
  clearSelection: () => void;
}
```

**Current Implementation**: Uses mock data from `explorer.mock.ts`

**Future Implementation**: Will call API Gateway endpoints

## Utility Functions

### filterSignals

Filters signals based on criteria (source, regime, date range, confidence)

### sortSignalsByTime

Sorts signals chronologically (newest first)

### generateTimeline

Groups signals by date and determines dominant regime

### calculateStats

Computes aggregate statistics (total, by source, by regime, avg confidence)

### getRegimeColor

Returns RGB color for TW regime visualization

### getSourceLabel

Returns human-readable label for KALDRA domain

### formatTimestamp

Formats ISO timestamp for display

## Mock Data

### Current Implementation

The Explorer currently uses **20 realistic mock signals** distributed across all domains:

- **5 Alpha signals** - Earnings from NVDA, TSLA, META, JPM, AAPL
- **5 GEO signals** - US-China tech, EU AI Act, OPEC+, India infrastructure, Taiwan
- **5 Product signals** - Nike, Ozempic, Shein, Liquid Death, luxury resale
- **5 Safeguard signals** - Deepfakes, crypto scams, health misinfo, financial doom, synthetic identity

### Mock Data Structure

Located in `explorer.mock.ts`:

```typescript
export const explorerMockSignals: ExplorerSignal[] = [
  {
    id: 'alpha_001',
    source: 'alpha',
    title: 'NVDA Q4 Earnings Beat - AI Demand Surge',
    summary: '...',
    archetype_id: 'ARC_001',
    delta144_state: 'Δ_089',
    kindra_vector: 'K_EXPANSION_HIGH',
    tw_regime: 'TURBULENT',
    confidence: 0.92,
    timestamp: '2025-11-20T14:30:00Z'
  },
  // ... 19 more signals
];
```

## Future API Integration

### Transition Plan

**Phase 1: Mock Data (Current)**
- All data from `explorer.mock.ts`
- No external dependencies
- Instant response times
- Perfect for development and UI testing

**Phase 2: API Gateway Integration (Future)**

Replace mock calls in `useExplorer` hook:

```typescript
// Current (Mock)
const allSignals = useMemo(() => getAllMockSignals(), []);

// Future (API)
const { data: allSignals } = useQuery({
  queryKey: ['explorer-signals'],
  queryFn: () => apiClient.get('/kaldra/explorer/signals')
});
```

### API Endpoints (Future)

The Explorer will consume these API Gateway endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/kaldra/explorer/signals` | GET | Fetch all signals with optional filters |
| `/kaldra/explorer/signals/:id` | GET | Fetch single signal by ID |
| `/kaldra/explorer/timeline` | GET | Get timeline aggregation |
| `/kaldra/explorer/stats` | GET | Get aggregate statistics |

### Query Parameters (Future)

```
GET /kaldra/explorer/signals?source=alpha&regime=CRITICAL&limit=50
```

Parameters:
- `source` - Filter by domain (alpha, geo, product, safeguard)
- `regime` - Filter by TW regime (STABLE, TURBULENT, CRITICAL)
- `dateFrom` - ISO timestamp
- `dateTo` - ISO timestamp
- `minConfidence` - Float 0.0-1.0
- `limit` - Max results
- `offset` - Pagination

## Integration with KALDRA Engine

### Data Pipeline (Future)

```
┌──────────────────┐
│  KALDRA Engine   │
│  - Alpha         │
│  - GEO           │
│  - Product       │
│  - Safeguard     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  API Gateway     │
│  /explorer/*     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  useExplorer     │
│  Hook            │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Explorer UI     │
└──────────────────┘
```

### Signal Enrichment

Each signal will include:

1. **Δ144 Classification** - Archetype and state from Δ144 system
2. **TW369 Regime** - Tracy-Widom regime classification
3. **Kindra Vector** - Cultural/narrative vector
4. **Confidence Score** - ML model confidence
5. **Metadata** - Source, timestamp, identifiers

## TW369 Integration

### Regime Classification

The Explorer visualizes **Tracy-Widom (TW) regimes** which indicate market/narrative stability:

- **STABLE** (Green) - Normal conditions, low volatility
- **TURBULENT** (Yellow) - Elevated uncertainty, moderate volatility
- **CRITICAL** (Red) - Extreme conditions, high volatility

### Visual Indicators

TW regimes are shown via:
- Timeline point colors
- Signal card indicators
- Detail modal badges
- Stats dashboard

## Δ144 Integration

### Archetype System

Each signal is classified into one of **144 archetypal states** representing:
- Cultural narratives
- Market conditions
- Geopolitical postures
- Brand positioning

### Display

Δ144 data shown in:
- Signal cards (`delta144_state`)
- Detail modal (`archetype_id`, `delta144_state`)
- Future: Δ144 Grid visualization

## Performance Considerations

### Current (Mock)

- Instant load times
- All filtering client-side
- No network latency
- Perfect for development

### Future (API)

**Optimizations to implement**:

1. **Pagination** - Load signals in batches
2. **Caching** - React Query with stale-while-revalidate
3. **Debouncing** - Delay filter API calls
4. **Virtual Scrolling** - Render only visible signals
5. **Prefetching** - Load next page in background

## Styling & Theming

### Design System

The Explorer uses the 4IAM.AI design system:

- **Colors**: Tailwind CSS palette
- **Typography**: System fonts
- **Spacing**: Tailwind spacing scale
- **Dark Mode**: Automatic via `dark:` classes

### Responsive Design

- **Desktop**: Sidebar + main content
- **Tablet**: Collapsible sidebar
- **Mobile**: Full-width, hamburger menu (future)

## Testing Strategy

### Unit Tests (Future)

- `explorer.utils.ts` - Filter, sort, timeline generation
- `useExplorer.ts` - Hook state management
- Component rendering

### Integration Tests (Future)

- Filter interactions
- Timeline navigation
- Signal selection
- Modal open/close

### E2E Tests (Future)

- Full user flows
- Cross-domain filtering
- Detail view navigation

## Deployment

### Current Status

- ✅ Fully functional with mock data
- ✅ No external dependencies
- ✅ Ready for local development
- ✅ No authentication required

### Production Readiness

**Before production deployment**:

1. ✅ Replace mocks with API calls
2. ✅ Implement authentication
3. ✅ Add error handling
4. ✅ Implement loading states
5. ✅ Add pagination
6. ✅ Optimize performance
7. ✅ Add analytics tracking

## Maintenance

### Adding New Signals (Mock)

Edit `explorer.mock.ts`:

```typescript
export const explorerMockSignals: ExplorerSignal[] = [
  // ... existing signals
  {
    id: 'new_signal_001',
    source: 'alpha',
    title: 'New Signal Title',
    // ... other fields
  }
];
```

### Adding New Filters

1. Update `ExplorerFilters` type in `explorer.types.ts`
2. Add filter UI to `ExplorerSidebar`
3. Update `filterSignals` in `explorer.utils.ts`
4. Update `useExplorer` hook state

### Customizing Components

All components are standalone and can be modified independently:

- Sidebar: Change filter options
- Timeline: Adjust visualization
- List: Modify card layout
- Details: Add/remove fields

## Troubleshooting

### Common Issues

**Issue**: Signals not displaying
- Check `explorerMockSignals` array is populated
- Verify filters aren't excluding all signals

**Issue**: Timeline empty
- Ensure signals have valid timestamps
- Check `generateTimeline` function

**Issue**: Detail modal not opening
- Verify `setSelectedSignalId` is called
- Check signal ID exists in mock data

## Future Enhancements

### Planned Features

1. **Export Functionality** - Download signals as CSV/JSON
2. **Advanced Filters** - Multi-select, date ranges, confidence sliders
3. **Signal Comparison** - Side-by-side signal analysis
4. **Bookmarking** - Save favorite signals
5. **Notifications** - Alert on new CRITICAL signals
6. **Search** - Full-text signal search
7. **Visualizations** - Δ144 grid, Kindra maps, drift charts
8. **Collaboration** - Share signals, add notes

### Integration Roadmap

1. **Phase 1**: Mock data (✅ Complete)
2. **Phase 2**: API Gateway integration
3. **Phase 3**: Real-time updates (WebSocket)
4. **Phase 4**: Advanced visualizations
5. **Phase 5**: Collaborative features

## Conclusion

The KALDRA Explorer provides a unified, intuitive interface for navigating signals across all KALDRA domains. Its modular architecture, comprehensive type system, and clean separation of concerns make it easy to maintain and extend.

The current mock implementation allows for rapid frontend development and testing, while the planned API integration will seamlessly connect to the KALDRA Engine backend.

---

**Last Updated**: 2025-11-21  
**Version**: 1.0.0  
**Status**: Mock Implementation Complete
