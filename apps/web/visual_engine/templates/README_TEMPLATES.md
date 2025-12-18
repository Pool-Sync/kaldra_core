# KALDRA Visual Engine - Dashboard Templates

## Overview

The `templates/` directory contains pre-built dashboard templates for different KALDRA products and use cases.

## Templates

### `dashboard_template.tsx`
General-purpose dashboard template.

**Features:**
- Flexible grid layout
- Navigation header
- Filter controls
- Panel system
- Responsive design

**Use Cases:**
- Custom dashboards
- Generic visualizations
- Prototyping

### `alpha_template.tsx`
Dashboard for Alpha (financial markets) product.

**Features:**
- Market overview panel
- Earnings calendar
- Δ144 state grid
- TW369 drift chart
- Signal alerts
- Portfolio recommendations

**Use Cases:**
- Financial analysis
- Market monitoring
- Trading signals

### `geo_template.tsx`
Dashboard for GEO (geopolitical analysis) product.

**Features:**
- World map with hotspots
- Regional analysis panels
- Narrative spiral
- Cultural vector map
- Polarity axes
- Conflict indicators

**Use Cases:**
- Geopolitical monitoring
- Regional analysis
- Narrative tracking

### `product_template.tsx`
Dashboard for Product (UX analysis) product.

**Features:**
- Product overview
- User sentiment analysis
- Archetype distribution
- Kindra radar for UX dimensions
- Feedback timeline
- Improvement recommendations

**Use Cases:**
- UX research
- Product development
- User feedback analysis

### `safeguard_template.tsx`
Dashboard for Safeguard (dangerous narratives) product.

**Features:**
- Threat level overview
- Narrative tracking timeline
- Drift map for dangerous patterns
- Cultural vector map
- Alert system
- Mitigation recommendations

**Use Cases:**
- Narrative monitoring
- Threat detection
- Risk assessment

### `kaldra_explorer_template.tsx`
Interactive explorer for KALDRA symbolic systems.

**Features:**
- System selector (Δ144, TW369, Kindras)
- Δ144 grid explorer
- Archetype details panel
- Kindra glyph library
- Polarity axes explorer
- State transition visualizer
- Documentation panel

**Use Cases:**
- System exploration
- Educational purposes
- Research and development

## Usage Pattern

```tsx
import AlphaTemplate from '@/visual_engine/templates/alpha_template';

function AlphaPage() {
  return <AlphaTemplate />;
}
```

## Customization

All templates can be customized by:
- Passing configuration props
- Overriding component styles
- Adding/removing panels
- Adjusting layouts

## Status

**⚠️ All templates are placeholders. No functional logic implemented.**

## Integration

All templates:
- Use visual engine components
- Apply design system tokens
- Connect to KALDRA API
- Support responsive layouts
