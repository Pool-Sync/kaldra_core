# UX Architecture — 4IAM.AI

## 1. Objective

Define the user experience architecture for the 4IAM.AI platform, including information architecture, user flows, and interaction patterns.

**Status**: Design specification — implementation TODO

## 2. Information Architecture

### Site Structure

```
Home
├── Dashboard (unified view)
│   ├── Overview
│   ├── Recent Signals
│   └── Quick Actions
│
├── Products
│   ├── Alpha (Earnings Intelligence)
│   ├── GEO (Geopolitical Intelligence)
│   ├── Product (Market Intelligence)
│   └── Safeguard (Risk Intelligence)
│
├── Intelligence
│   ├── Signals (Real-time feed)
│   ├── Insights (Reports & Analysis)
│   └── Explorer (Symbolic Visualization)
│
└── Settings
    ├── Profile
    ├── Preferences
    └── API Access
```

## 3. User Personas

### Primary Users

**Intelligence Analyst**
- Needs: Deep analysis, historical data, trend identification
- Primary flows: Insights → Reports → Explorer
- Key features: Search, filtering, export, annotations

**Executive/Decision Maker**
- Needs: High-level overview, key metrics, alerts
- Primary flows: Dashboard → Signals → Product pages
- Key features: Customizable dashboard, real-time alerts, summaries

**Risk Manager**
- Needs: Risk monitoring, alerts, compliance tracking
- Primary flows: Safeguard → Signals → Detailed analysis
- Key features: Alert configuration, risk scoring, audit trails

## 4. User Flows

### Discovery Flow
1. Land on Home page
2. Browse product overview cards
3. Select product of interest
4. View product dashboard
5. Drill down into specific signals/insights

### Monitoring Flow
1. Access Dashboard
2. Review recent signals
3. Filter by product/priority
4. Click signal for details
5. Take action or save for later

### Analysis Flow
1. Navigate to Insights
2. Search/filter reports
3. Open detailed report
4. View related insights
5. Export or share findings

### Exploration Flow
1. Access Explorer
2. Select visualization type (Δ144, TW369, Kindras)
3. Interact with symbolic data
4. Drill down into archetypes/patterns
5. Connect to related signals/insights

## 5. Layout Patterns

### Global Layout
```
┌─────────────────────────────────────┐
│           Header (Nav)              │
├──────┬──────────────────────────────┤
│      │                              │
│ Side │      Main Content            │
│ bar  │                              │
│      │                              │
├──────┴──────────────────────────────┤
│           Footer                    │
└─────────────────────────────────────┘
```

### Dashboard Layout
- Grid-based card system
- Responsive columns (1, 2, 3, 4 based on viewport)
- Drag-and-drop customization (future)

### Product Page Layout
- Hero section with key metrics
- Tabbed navigation for sub-sections
- Chart visualizations from Visual Engine
- Related signals sidebar

### Detail View Layout
- Breadcrumb navigation
- Content area with rich formatting
- Metadata sidebar
- Related items section
- Action buttons (share, export, save)

## 6. Interaction Patterns

### Navigation
- **Primary**: Header navigation for main sections
- **Secondary**: Sidebar for contextual navigation
- **Tertiary**: Breadcrumbs for deep navigation
- **Search**: Global search in header (future)

### Data Display
- **Cards**: For lists and grids (signals, insights, products)
- **Tables**: For detailed data (future)
- **Charts**: From Visual Engine for visualizations
- **Timelines**: For temporal data (future)

### Actions
- **Primary**: Prominent buttons for main actions
- **Secondary**: Text links or icon buttons
- **Bulk**: Checkbox selection for multiple items (future)
- **Context**: Right-click or dropdown menus (future)

### Feedback
- **Loading**: Skeleton screens and spinners
- **Success**: Toast notifications
- **Error**: Inline error messages and toast alerts
- **Empty**: Empty state illustrations with CTAs

## 7. Responsive Design

### Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px
- Wide: > 1536px

### Adaptations
- **Mobile**: Single column, hamburger menu, bottom navigation
- **Tablet**: Two columns, collapsible sidebar
- **Desktop**: Full layout with sidebar
- **Wide**: Expanded content area, more columns

## 8. Accessibility

### Requirements
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatibility
- Focus indicators
- Color contrast compliance
- Alt text for images
- ARIA labels for interactive elements

## 9. Performance

### Optimization Strategies
- Code splitting by route
- Lazy loading for images and charts
- Prefetching for likely navigation
- Caching for static assets
- Progressive enhancement

### Loading Strategy
- Show skeleton screens immediately
- Load critical content first
- Defer non-critical content
- Stream data when possible

## 10. TODO

- [ ] Implement responsive layouts
- [ ] Add keyboard navigation
- [ ] Create loading states
- [ ] Design empty states
- [ ] Implement error handling
- [ ] Add accessibility features
- [ ] Create mobile navigation
- [ ] Implement search functionality
- [ ] Add user preferences
- [ ] Create onboarding flow
