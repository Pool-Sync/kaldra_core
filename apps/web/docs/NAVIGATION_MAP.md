# Navigation Map — 4IAM.AI

## Site Navigation Structure

```
Home (/)
│
├── Dashboard (/dashboard)
│   ├── Overview
│   ├── Recent Activity
│   ├── Quick Stats
│   └── Product Summaries
│       ├── Alpha Summary
│       ├── GEO Summary
│       ├── Product Summary
│       └── Safeguard Summary
│
├── Products
│   ├── Alpha (/alpha)
│   │   ├── Earnings Calendar
│   │   ├── Company Analysis
│   │   ├── Sector Trends
│   │   └── Signals Feed
│   │
│   ├── GEO (/geo)
│   │   ├── Regional Overview
│   │   ├── Risk Assessment
│   │   ├── Event Tracking
│   │   └── Signals Feed
│   │
│   ├── Product (/product)
│   │   ├── Market Analysis
│   │   ├── Product Trends
│   │   ├── Competitive Intelligence
│   │   └── Signals Feed
│   │
│   └── Safeguard (/safeguard)
│       ├── Risk Dashboard
│       ├── Alert Management
│       ├── Compliance Tracking
│       └── Signals Feed
│
├── Intelligence
│   ├── Signals (/signals)
│   │   ├── All Signals
│   │   ├── By Product
│   │   │   ├── Alpha Signals
│   │   │   ├── GEO Signals
│   │   │   ├── Product Signals
│   │   │   └── Safeguard Signals
│   │   ├── By Priority
│   │   └── Signal Detail (/signals/[id])
│   │
│   ├── Insights (/insights)
│   │   ├── All Insights
│   │   ├── By Category
│   │   │   ├── Reports
│   │   │   ├── Analysis
│   │   │   └── Briefings
│   │   ├── By Product
│   │   └── Insight Detail (/insights/[id])
│   │
│   └── Explorer (/explorer)
│       ├── Δ144 Grid
│       ├── TW369 Wave
│       ├── Kindra Glyphs
│       ├── Archetype Explorer
│       └── Symbolic Navigation
│
└── Settings (future)
    ├── Profile
    ├── Preferences
    ├── Notifications
    └── API Access
```

## Navigation Hierarchy

### Level 1: Global Navigation (Header)
- Home
- Dashboard
- Products (dropdown)
- Signals
- Insights
- Explorer

### Level 2: Product Navigation (Sidebar)
Visible when on product pages:
- Alpha
- GEO
- Product
- Safeguard

### Level 3: Contextual Navigation (Tabs/Sections)
Visible within specific pages:
- Product-specific sections
- Filtering options
- View toggles

## Quick Access Paths

### For Analysts
```
Home → Insights → [Category] → Insight Detail
Home → Explorer → [Visualization Type]
```

### For Executives
```
Home → Dashboard → Product Summary → Product Page
Home → Signals → [Priority Filter] → Signal Detail
```

### For Risk Managers
```
Home → Safeguard → Risk Dashboard
Home → Signals → Safeguard Signals → Signal Detail
```

## Breadcrumb Examples

```
Home > Dashboard
Home > Products > Alpha
Home > Products > Alpha > Earnings Calendar
Home > Signals > Alpha Signals > Signal #12345
Home > Insights > Reports > Q4 2024 Analysis
Home > Explorer > Δ144 Grid
```

## Mobile Navigation

On mobile devices (< 640px):
- Hamburger menu for main navigation
- Bottom tab bar for quick access:
  - Dashboard
  - Signals
  - Insights
  - More (menu)

## Search Navigation (Future)

Global search will provide quick access to:
- Signals by keyword
- Insights by topic
- Products by name
- Specific companies/entities
- Archetypes and symbolic elements

## TODO

- [ ] Implement breadcrumb component
- [ ] Create mobile navigation menu
- [ ] Add search functionality
- [ ] Implement deep linking
- [ ] Add navigation analytics
- [ ] Create navigation shortcuts (keyboard)
- [ ] Implement back/forward navigation
- [ ] Add navigation state persistence
