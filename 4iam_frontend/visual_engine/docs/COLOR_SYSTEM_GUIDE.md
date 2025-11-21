# KALDRA Color System Guide

## Overview

The KALDRA Color System provides a comprehensive palette for visualizing symbolic systems including Δ144, TW369, Kindras, and Polarities.

## Color Palettes

### Δ144 Archetype Colors

**12 Base Archetype Colors**

TODO: Define 12 distinct colors for archetypes

| Archetype | Color | Hex | Meaning |
|-----------|-------|-----|---------|
| TODO | TODO | #000000 | TODO |

**144 State Colors**

TODO: Define color variations for 144 states (12 archetypes × 12 modifiers)

**Strategy:**
- Base color from archetype
- Lightness/saturation variation from modifier
- Maintain visual distinction

### TW369 Wave Colors

**Drift Intensity Gradient**

TODO: Define gradient from low to high drift

| Drift Level | Color | Hex | Description |
|-------------|-------|-----|-------------|
| Low | TODO | #000000 | Stable, low drift |
| Medium | TODO | #000000 | Moderate drift |
| High | TODO | #000000 | High drift, instability |

**Phase Colors**

TODO: Define colors for wave phases

### Kindra Colors

**Symbolic Colors**

TODO: Define colors for Kindra symbols

| Kindra | Color | Hex | Symbolic Meaning |
|--------|-------|-----|------------------|
| TODO | TODO | #000000 | TODO |

**Cultural Vector Colors**

TODO: Define colors for cultural dimensions

### Polarity Colors

**Polarity Gradient**

TODO: Define gradient from negative to positive

| Polarity | Color | Hex | Description |
|----------|-------|-----|-------------|
| -1.0 (Negative) | TODO | #000000 | Extreme negative |
| 0.0 (Neutral) | TODO | #000000 | Balanced |
| +1.0 (Positive) | TODO | #000000 | Extreme positive |

## Color Mapping Functions

### Δ144 State Mapping

```typescript
function getDelta144Color(state: number): string {
  // TODO: Map state (0-143) to color
  // - Extract archetype (state / 12)
  // - Extract modifier (state % 12)
  // - Combine base color with modifier variation
  return "#000000";
}
```

### TW369 Drift Mapping

```typescript
function getTW369Color(drift: number): string {
  // TODO: Map drift value to gradient
  // - Normalize drift to [0, 1]
  // - Interpolate between gradient stops
  return "#000000";
}
```

### Kindra Mapping

```typescript
function getKindraColor(kindra: string): string {
  // TODO: Map Kindra symbol to color
  // - Lookup in Kindra color map
  // - Return default if not found
  return "#000000";
}
```

### Polarity Mapping

```typescript
function getPolarityColor(value: number): string {
  // TODO: Map polarity (-1 to 1) to gradient
  // - Normalize to [0, 1]
  // - Interpolate between negative and positive
  return "#000000";
}
```

## Color Utilities

### Gradient Generation

```typescript
function generateGradient(from: string, to: string, steps: number): string[] {
  // TODO: Generate color gradient
  // - Parse colors
  // - Interpolate in HSL space
  // - Return array of colors
  return [];
}
```

### Color Manipulation

```typescript
function lighten(color: string, amount: number): string {
  // TODO: Lighten color
  return color;
}

function darken(color: string, amount: number): string {
  // TODO: Darken color
  return color;
}

function saturate(color: string, amount: number): string {
  // TODO: Increase saturation
  return color;
}

function desaturate(color: string, amount: number): string {
  // TODO: Decrease saturation
  return color;
}
```

## Accessibility

### Color Contrast

All color combinations must meet WCAG AA standards:
- Normal text: 4.5:1 contrast ratio
- Large text: 3:1 contrast ratio
- UI components: 3:1 contrast ratio

### Color Blindness

Provide alternative visual cues:
- Patterns
- Shapes
- Labels
- Textures

### Dark Mode

TODO: Define dark mode color variants

## Design System Integration

Colors integrate with design system tokens:

```typescript
// Example integration
const archetypeColor = tokens.colors.delta144.archetype[0];
const driftColor = tokens.colors.tw369.drift.high;
```

## Status

**⚠️ TODO: Define all color values**

All colors are placeholders (#000000). No actual color values defined.

## Next Steps

1. Define 12 archetype base colors
2. Generate 144 state color variations
3. Define TW369 drift gradient
4. Define Kindra symbolic colors
5. Define polarity gradient
6. Implement color mapping functions
7. Test accessibility
8. Integrate with design system

---

**Version:** 1.0  
**Status:** Placeholder  
**Last Updated:** 2025-11-21
