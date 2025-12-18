# Polarity Map Design

## Overview

This document describes the visual design for polarity map visualizations.

## Concept

The Polarity Map visualizes multi-dimensional polarity spaces where:
- **Axes**: Represent polarity dimensions
- **Points**: Represent archetypes or entities
- **Position**: Indicates polarity values
- **Distance**: Shows similarity/difference

## Visualization Types

### 2D Polarity Map

**Two-Axis Visualization**

```
        Positive Y
             ↑
             │
             │  • Archetype A
             │
─────────────┼─────────────→ Positive X
Negative X   │   Negative Y
             │
        • Archetype B
             │
             ↓
```

**Features:**
- Two polarity dimensions
- Quadrant division
- Point plotting
- Interactive rotation

### 3D Polarity Space

**Three-Axis Visualization**

- X, Y, Z axes
- 3D point cloud
- Octant division
- Interactive rotation and zoom

### Radar Polarity

**Multi-Axis Radar**

```
        Axis 1
          │
    Axis 6│  Axis 2
         \│/
    ──────●──────
         /│\
    Axis 5│  Axis 3
          │
        Axis 4
```

**Features:**
- Multiple polarity dimensions (6+)
- Radar/spider chart layout
- Polygon overlay
- Comparison support

## Visual Elements

### Axes

**Axis Design:**
- **Line**: Thin, neutral color
- **Arrow**: Directional indicator
- **Labels**: Dimension names
- **Ticks**: Value markers (-1, 0, +1)

**Axis Colors:**
- Positive direction: TODO (e.g., blue)
- Negative direction: TODO (e.g., red)
- Neutral point: Gray

### Quadrants/Octants

**Background Shading:**
- Light shading for quadrants
- Different colors for different regions
- Subtle, non-intrusive
- Helps orientation

**Labels:**
- Quadrant names (if applicable)
- Polarity combinations
- Contextual meaning

### Points

**Archetype Points:**
- **Shape**: Circle or archetype symbol
- **Size**: 8-16px
- **Color**: Archetype color
- **Border**: 2px stroke
- **Label**: Archetype name (on hover or always)

**Point States:**
- **Default**: Normal appearance
- **Hover**: Larger, highlighted
- **Selected**: Bold border, emphasized
- **Dimmed**: Reduced opacity

### Connections

**Relationship Lines:**
- Connect related points
- Line thickness indicates strength
- Color indicates relationship type
- Dashed for weak relationships

### Gradient Background

**Polarity Gradient:**
- Smooth color transition
- From negative to positive
- Helps visualize polarity values
- Subtle, non-distracting

## Interactions

### Rotation (3D)

- **Mouse Drag**: Rotate view
- **Scroll**: Zoom in/out
- **Reset**: Return to default view

### Point Selection

- **Click**: Select point
- **Shift+Click**: Multi-select
- **Details Panel**: Show selected point info

### Axis Adjustment

- **Drag Axis**: Change dimension
- **Dropdown**: Select different polarity
- **Lock**: Fix axis in place

### Filtering

- **By Archetype**: Show/hide archetypes
- **By Quadrant**: Focus on region
- **By Value**: Filter by polarity range

## Layout

### 2D Layout

**Canvas:**
- Square or rectangular
- Centered axes
- Equal scaling
- Padding for labels

**Legend:**
- Archetype colors
- Axis meanings
- Quadrant descriptions

### 3D Layout

**Canvas:**
- 3D perspective
- Rotatable view
- Depth indicators
- Grid floor (optional)

**Controls:**
- Rotation controls
- Zoom slider
- Reset button
- Axis toggles

## Color Schemes

### Polarity Gradient

TODO: Define gradient from negative to positive

| Value | Color | Hex | Description |
|-------|-------|-----|-------------|
| -1.0 | TODO | #000000 | Extreme negative |
| -0.5 | TODO | #000000 | Moderate negative |
| 0.0 | TODO | #000000 | Neutral |
| +0.5 | TODO | #000000 | Moderate positive |
| +1.0 | TODO | #000000 | Extreme positive |

### Archetype Colors

Use archetype colors for points (from Δ144 system)

### Quadrant Colors

TODO: Define subtle background colors for quadrants

## Responsive Design

### Desktop (>1024px)
- Full polarity map
- All labels visible
- Interactive controls
- 3D support

### Tablet (768-1024px)
- Condensed map
- Essential labels
- Touch controls
- 2D preferred

### Mobile (<768px)
- Simplified map
- Minimal labels
- Tap interactions
- 2D only

## Accessibility

### Keyboard Navigation
- Arrow keys: Navigate points
- Tab: Move between controls
- Enter: Select point
- Escape: Deselect

### Screen Readers
- Announce point positions
- Read polarity values
- Describe relationships
- Provide data table alternative

### Color Contrast
- Ensure point visibility
- Provide pattern alternatives
- Test with color blindness simulators

## Examples

### Archetype Polarity Map

**Two Dimensions:**
- X: Individual ↔ Collective
- Y: Stability ↔ Change

**Points:**
- Plot 12 archetypes
- Show polarity positions
- Reveal archetype relationships

### Cultural Polarity Map

**Multiple Dimensions:**
- Traditional ↔ Progressive
- Authoritarian ↔ Libertarian
- Collectivist ↔ Individualist

**Points:**
- Plot cultural narratives
- Show cultural positions
- Track shifts over time

## Animation

### Entrance

- Points fade in
- Axes draw from center
- Stagger for multiple points

### Transition

- Smooth point movement
- Axis rotation
- Dimension changes

### Emphasis

- Pulse selected points
- Highlight connections
- Glow on hover

## Status

**⚠️ TODO: Implement polarity map visualization**

All design elements are placeholders. No functional implementation.

## Next Steps

1. Define polarity dimensions
2. Implement 2D map
3. Implement 3D space
4. Add radar variant
5. Implement interactions
6. Add animations
7. Test responsiveness
8. Ensure accessibility

---

**Version:** 1.0  
**Status:** Placeholder  
**Last Updated:** 2025-11-21
