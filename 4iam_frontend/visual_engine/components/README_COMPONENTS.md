# KALDRA Visual Engine - UI Components

## Overview

The `components/` directory contains reusable UI components for building KALDRA visualizations and dashboards.

## Components

### `kaldra_canvas.tsx`
Generic canvas wrapper for rendering visualizations.

**Features:**
- Canvas context management
- Resize handling
- Rendering pipeline integration
- Interaction overlay

### `kaldra_svg.tsx`
Generic SVG wrapper for vector graphics.

**Features:**
- SVG context management
- ViewBox calculations
- Zoom/pan support
- Layer management

### `kaldra_legend.tsx`
Legend component for chart annotations.

**Features:**
- Horizontal/vertical orientation
- Color swatches
- Symbol rendering
- Interactive filtering

### `kaldra_card.tsx`
Card UI component for content containers.

**Features:**
- Multiple variants (default, outlined, elevated)
- Header/body/footer sections
- Hover effects
- Responsive design

### `kaldra_panel.tsx`
Modular panel for dashboard layouts.

**Features:**
- Collapsible panels
- Resize handles
- Header with title
- Content area

### `kaldra_infobox.tsx`
Information box for contextual messages.

**Features:**
- Multiple types (info, warning, error, success)
- Icon rendering
- Dismissible
- Styled variants

### `kaldra_tooltip.tsx`
Tooltip component for hover interactions.

**Features:**
- Multiple positions (top, bottom, left, right)
- Auto-positioning
- Fade animations
- Rich content support

## Usage Pattern

```tsx
import { KaldraCard, KaldraCanvas, KaldraLegend } from '@/visual_engine/components';

function MyVisualization() {
  return (
    <KaldraCard title="Δ144 Grid">
      <KaldraCanvas>
        {/* Visualization content */}
      </KaldraCanvas>
      <KaldraLegend items={legendItems} />
    </KaldraCard>
  );
}
```

## Status

**⚠️ All components are placeholders. No functional logic implemented.**

## Integration

All components:
- Use design system tokens
- Support responsive layouts
- Include accessibility features
- Integrate with visual engine core
