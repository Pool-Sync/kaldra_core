# Content Model — 4IAM.AI

## 1. Objective

Define the content structure and data models for the 4IAM.AI platform.

**Status**: Schema specification — implementation TODO

## 2. Core Content Types

### Signal
Real-time intelligence signals from KALDRA products.

```typescript
interface Signal {
  // Identity
  id: string;
  uuid: string;
  
  // Classification
  product: 'alpha' | 'geo' | 'product' | 'safeguard';
  category: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  
  // Content
  title: string;
  summary: string;
  content: string;
  
  // Metadata
  timestamp: string; // ISO 8601
  source: string;
  confidence: number; // 0-1
  
  // KALDRA Symbolic Data
  archetype?: string; // Δ144 archetype
  kindra?: string;
  tw369_score?: number;
  bias_vector?: number[];
  
  // Relationships
  relatedSignals?: string[]; // Signal IDs
  relatedInsights?: string[]; // Insight IDs
  entities?: Entity[];
  
  // User Interaction
  views: number;
  saved: boolean;
  notes?: string;
}
```

### Insight
In-depth intelligence reports and analysis.

```typescript
interface Insight {
  // Identity
  id: string;
  uuid: string;
  
  // Classification
  type: 'report' | 'analysis' | 'briefing' | 'forecast';
  category: string;
  product: string;
  
  // Content
  title: string;
  subtitle?: string;
  summary: string;
  content: string; // Markdown or rich text
  
  // Authorship
  author: string;
  contributors?: string[];
  publishedAt: string;
  updatedAt?: string;
  
  // Organization
  tags: string[];
  topics: string[];
  
  // Media
  coverImage?: string;
  attachments?: Attachment[];
  
  // KALDRA Analysis
  archetypes?: string[];
  kindras?: string[];
  symbolicSummary?: string;
  
  // Relationships
  relatedSignals?: string[];
  relatedInsights?: string[];
  references?: Reference[];
  
  // Metrics
  views: number;
  readTime: number; // minutes
  saved: boolean;
}
```

### Product Dashboard Data
Data structure for product-specific dashboards.

```typescript
interface ProductDashboard {
  product: 'alpha' | 'geo' | 'product' | 'safeguard';
  
  // Key Metrics
  metrics: {
    key: string;
    value: number | string;
    change?: number; // percentage
    trend?: 'up' | 'down' | 'stable';
  }[];
  
  // Recent Activity
  recentSignals: Signal[];
  recentInsights: Insight[];
  
  // Charts Data
  charts: {
    type: string;
    data: any;
    config?: any;
  }[];
  
  // Product-specific Data
  productData: any; // Varies by product
  
  // Timestamp
  lastUpdated: string;
}
```

### Entity
Entities mentioned in signals and insights.

```typescript
interface Entity {
  id: string;
  type: 'company' | 'person' | 'location' | 'event' | 'product' | 'other';
  name: string;
  description?: string;
  
  // Metadata
  metadata: Record<string, any>;
  
  // Relationships
  relatedEntities?: string[];
  
  // KALDRA Mapping
  archetype?: string;
  symbolicProfile?: any;
}
```

### Archetype (Δ144)
KALDRA symbolic archetype data.

```typescript
interface Archetype {
  id: string; // 1-12
  name: string;
  symbol: string;
  
  // Description
  description: string;
  traits: string[];
  
  // Δ144 Grid Position
  position: {
    x: number;
    y: number;
  };
  
  // Modifiers
  modifiers: string[];
  
  // Relationships
  polarities: {
    archetype: string;
    relationship: string;
  }[];
  
  // States (144 total)
  states: ArchetypeState[];
}

interface ArchetypeState {
  id: string; // 1-144
  archetype: string;
  modifier: string;
  description: string;
  keywords: string[];
}
```

### Kindra
KALDRA symbolic glyph/pattern.

```typescript
interface Kindra {
  id: string;
  name: string;
  glyph: string; // SVG or path data
  
  // Classification
  category: string;
  subcategory?: string;
  
  // Description
  meaning: string;
  interpretation: string;
  
  // Usage
  contexts: string[];
  examples: string[];
  
  // Relationships
  relatedKindras?: string[];
  relatedArchetypes?: string[];
}
```

## 3. User Data

### User Profile
```typescript
interface UserProfile {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  
  // Preferences
  preferences: {
    theme: 'light' | 'dark' | 'auto';
    defaultProduct?: string;
    notifications: NotificationSettings;
    dashboard: DashboardSettings;
  };
  
  // Activity
  savedSignals: string[];
  savedInsights: string[];
  recentViews: {
    type: 'signal' | 'insight' | 'page';
    id: string;
    timestamp: string;
  }[];
  
  // Access
  role: 'viewer' | 'analyst' | 'admin';
  permissions: string[];
}
```

### Notification Settings
```typescript
interface NotificationSettings {
  email: boolean;
  push: boolean;
  
  // Signal Alerts
  signalAlerts: {
    enabled: boolean;
    products: string[];
    priorities: string[];
  };
  
  // Insight Alerts
  insightAlerts: {
    enabled: boolean;
    categories: string[];
  };
}
```

### Dashboard Settings
```typescript
interface DashboardSettings {
  layout: 'grid' | 'list';
  widgets: {
    id: string;
    type: string;
    position: { x: number; y: number };
    size: { w: number; h: number };
    config: any;
  }[];
}
```

## 4. API Response Formats

### List Response
```typescript
interface ListResponse<T> {
  data: T[];
  pagination: {
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
  };
  filters?: Record<string, any>;
}
```

### Detail Response
```typescript
interface DetailResponse<T> {
  data: T;
  related?: {
    signals?: Signal[];
    insights?: Insight[];
    entities?: Entity[];
  };
}
```

### Error Response
```typescript
interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: any;
  };
  timestamp: string;
}
```

## 5. Content Relationships

```
Signal ←→ Insight (many-to-many)
Signal ←→ Entity (many-to-many)
Insight ←→ Entity (many-to-many)
Signal → Archetype (many-to-one)
Signal → Kindra (many-to-many)
Insight → Archetype (many-to-many)
Archetype ←→ Archetype (polarities)
Kindra ←→ Kindra (relationships)
```

## 6. Content Lifecycle

### Signal Lifecycle
1. **Created** - Signal generated by KALDRA product
2. **Published** - Signal available in feed
3. **Viewed** - User views signal
4. **Saved** - User saves signal
5. **Archived** - Signal moved to archive (after 90 days)

### Insight Lifecycle
1. **Draft** - Insight being written
2. **Review** - Insight under review
3. **Published** - Insight available to users
4. **Updated** - Insight content updated
5. **Archived** - Insight archived (manual)

## 7. Search & Filtering

### Search Fields
- Signals: title, summary, content, entities
- Insights: title, summary, content, tags, topics
- Entities: name, description

### Filter Options
- **Product**: alpha, geo, product, safeguard
- **Priority**: low, medium, high, critical (signals)
- **Category**: varies by content type
- **Date Range**: custom range
- **Archetype**: Δ144 archetypes
- **Tags**: user-defined tags

## 8. TODO

- [ ] Implement TypeScript interfaces
- [ ] Create Zod schemas for validation
- [ ] Set up database models
- [ ] Implement API endpoints
- [ ] Create mock data generators
- [ ] Add data migration scripts
- [ ] Implement search indexing
- [ ] Add content versioning
- [ ] Create content templates
- [ ] Implement content workflows
