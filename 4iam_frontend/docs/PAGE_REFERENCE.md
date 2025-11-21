# Page Reference — 4IAM.AI

Complete reference for all pages in the 4IAM.AI dashboard.

## Core Pages

### Home Page
**Route**: `/`  
**File**: `app/page.tsx`  
**Status**: Placeholder  

**Purpose**: Landing page for 4IAM.AI platform

**Components**:
- Hero section with platform introduction
- Product overview cards (Alpha, GEO, Product, Safeguard)
- Featured insights
- Call-to-action sections

**TODO**:
- [ ] Implement hero section
- [ ] Add product navigation cards
- [ ] Display featured insights
- [ ] Add platform statistics
- [ ] Implement responsive layout

---

### Dashboard Page
**Route**: `/dashboard`  
**File**: `app/dashboard/page.tsx`  
**Status**: Placeholder with template integration point  

**Purpose**: Unified dashboard showing overview of all KALDRA products

**Template**: `visual_engine/templates/dashboard_template`

**Components**:
- Product overview cards
- Recent signals feed
- Key metrics
- Quick actions

**TODO**:
- [ ] Integrate DashboardTemplate
- [ ] Implement product summaries
- [ ] Add real-time signal updates
- [ ] Create customizable widgets
- [ ] Add data refresh controls

---

## Product Pages

### Alpha Page
**Route**: `/alpha`  
**File**: `app/alpha/page.tsx`  
**Status**: Placeholder with template integration point  

**Purpose**: Earnings intelligence and analysis dashboard

**Template**: `visual_engine/templates/alpha_template`

**Features**:
- Earnings calendar
- Company analysis
- Sector trends
- Alpha-specific signals

**TODO**:
- [ ] Integrate AlphaTemplate
- [ ] Implement earnings calendar
- [ ] Add company search
- [ ] Display sector analysis
- [ ] Connect to Alpha API endpoints

---

### GEO Page
**Route**: `/geo`  
**File**: `app/geo/page.tsx`  
**Status**: Placeholder with template integration point  

**Purpose**: Geopolitical intelligence and risk analysis

**Template**: `visual_engine/templates/geo_template`

**Features**:
- Regional overview maps
- Risk assessment dashboard
- Event tracking timeline
- GEO-specific signals

**TODO**:
- [ ] Integrate GeoTemplate
- [ ] Implement regional maps
- [ ] Add risk scoring visualization
- [ ] Create event timeline
- [ ] Connect to GEO API endpoints

---

### Product Page
**Route**: `/product`  
**File**: `app/product/page.tsx`  
**Status**: Placeholder with template integration point  

**Purpose**: Product intelligence and market analysis

**Template**: `visual_engine/templates/product_template`

**Features**:
- Market analysis dashboard
- Product trend tracking
- Competitive intelligence
- Product-specific signals

**TODO**:
- [ ] Integrate ProductTemplate
- [ ] Implement market analysis charts
- [ ] Add trend visualization
- [ ] Create competitive comparison
- [ ] Connect to Product API endpoints

---

### Safeguard Page
**Route**: `/safeguard`  
**File**: `app/safeguard/page.tsx`  
**Status**: Placeholder with template integration point  

**Purpose**: Risk intelligence and monitoring

**Template**: `visual_engine/templates/safeguard_template`

**Features**:
- Risk dashboard
- Alert management
- Compliance tracking
- Safeguard-specific signals

**TODO**:
- [ ] Integrate SafeguardTemplate
- [ ] Implement risk scoring
- [ ] Add alert configuration
- [ ] Create compliance reports
- [ ] Connect to Safeguard API endpoints

---

## Intelligence Pages

### Signals Page
**Route**: `/signals`  
**File**: `app/signals/page.tsx`  
**Status**: Placeholder  

**Purpose**: Real-time intelligence signals feed

**Features**:
- Signal cards with metadata
- Filtering by product and priority
- Search functionality
- Signal detail view
- Real-time updates

**TODO**:
- [ ] Implement signal feed
- [ ] Add filtering controls
- [ ] Create search functionality
- [ ] Build signal detail modal/page
- [ ] Add real-time WebSocket updates
- [ ] Implement pagination/infinite scroll

---

### Insights Page
**Route**: `/insights`  
**File**: `app/insights/page.tsx`  
**Status**: Placeholder  

**Purpose**: Intelligence reports and analysis library

**Features**:
- Insight cards with previews
- Categorization by type and product
- Search and filtering
- Detailed insight view
- Related insights

**TODO**:
- [ ] Implement insights library
- [ ] Add category navigation
- [ ] Create search functionality
- [ ] Build insight detail page
- [ ] Display related insights
- [ ] Add export functionality

---

### Explorer Page
**Route**: `/explorer`  
**File**: `app/explorer/page.tsx`  
**Status**: Placeholder with template integration point  

**Purpose**: Symbolic intelligence visualization (KALDRA Explorer)

**Template**: `visual_engine/templates/kaldra_explorer_template`

**Features**:
- Δ144 Grid visualization
- TW369 Wave patterns
- Kindra glyph renderer
- Archetype explorer
- Interactive symbolic navigation

**TODO**:
- [ ] Integrate ExplorerTemplate
- [ ] Implement Δ144 Grid interaction
- [ ] Add TW369 Wave visualization
- [ ] Create Kindra glyph renderer
- [ ] Build archetype navigation
- [ ] Add symbolic data connections

---

## Layout Components

### Root Layout
**File**: `app/layout.tsx`  
**Status**: Basic structure  

**Purpose**: Global layout wrapper for all pages

**Components**:
- HTML structure
- Global CSS imports
- Metadata configuration

**TODO**:
- [ ] Add Header component
- [ ] Add Footer component
- [ ] Implement global providers
- [ ] Add analytics
- [ ] Configure SEO metadata

---

## Page Templates

All product pages follow this structure:

```tsx
/**
 * Page Component
 * Status: Placeholder
 * Template: visual_engine/templates/[template_name]
 */

export default function Page() {
  return (
    <div className="container mx-auto p-4">
      <h1>Page Title</h1>
      <p>Page Description</p>
      
      {/* Template integration point */}
      {/* <Template /> */}
      
      <div className="placeholder">
        TODO: Implement page
      </div>
    </div>
  );
}
```

## Integration Checklist

For each page, complete these steps:

- [ ] Create page file in correct directory
- [ ] Add page metadata and SEO
- [ ] Integrate Visual Engine template (if applicable)
- [ ] Connect to backend API
- [ ] Implement data fetching
- [ ] Add loading states
- [ ] Add error handling
- [ ] Implement responsive design
- [ ] Add accessibility features
- [ ] Test navigation
- [ ] Optimize performance
