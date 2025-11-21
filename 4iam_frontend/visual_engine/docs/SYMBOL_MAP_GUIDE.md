# KALDRA Symbol Map Guide

## Overview

The KALDRA Symbol Map defines geometric shapes and visual symbols for representing KALDRA symbolic systems.

## Shape Types

### Basic Shapes

| Shape | Use Case | Properties |
|-------|----------|------------|
| Circle | Neutral, balanced states | Radius |
| Square | Stable, structured states | Side length |
| Triangle | Dynamic, directional states | Base, height, orientation |
| Hexagon | Complex, multi-faceted states | Radius, rotation |
| Star | Exceptional, highlighted states | Points, inner/outer radius |

### Archetype Shapes

**12 Archetype Symbols**

TODO: Define unique shape for each archetype

| Archetype | Shape | Description |
|-----------|-------|-------------|
| TODO | TODO | TODO |

**Design Principles:**
- Visually distinct
- Meaningful symbolism
- Scalable
- Recognizable at small sizes

### Kindra Glyphs

**Symbolic Glyphs**

TODO: Define Kindra glyph library

| Kindra | Glyph | SVG Path | Meaning |
|--------|-------|----------|---------|
| TODO | TODO | TODO | TODO |

**Design Principles:**
- Cultural significance
- Visual clarity
- Unique identity
- Consistent style

## Shape Mapping Functions

### Archetype Shape Mapping

```typescript
function getArchetypeShape(archetype: string): ShapeDefinition {
  // TODO: Map archetype to geometric shape
  // - Lookup in archetype shape map
  // - Return shape definition with properties
  return {
    type: ShapeType.CIRCLE,
    size: 0
  };
}
```

### Kindra Glyph Mapping

```typescript
function getKindraGlyph(kindra: string): GlyphDefinition {
  // TODO: Map Kindra to glyph
  // - Lookup in Kindra glyph library
  // - Return glyph with SVG path
  return {
    type: ShapeType.GLYPH,
    size: 0,
    symbol: kindra,
    path: ""
  };
}
```

## Shape Generation

### Polygon Generation

```typescript
function generatePolygon(sides: number, radius: number): ShapeDefinition {
  // TODO: Generate regular polygon
  // - Calculate vertex positions
  // - Generate SVG path
  return {
    type: ShapeType.HEXAGON,
    size: radius,
    vertices: []
  };
}
```

### Star Generation

```typescript
function generateStar(
  points: number,
  innerRadius: number,
  outerRadius: number
): ShapeDefinition {
  // TODO: Generate star shape
  // - Calculate alternating vertices
  // - Generate SVG path
  return {
    type: ShapeType.STAR,
    size: outerRadius,
    vertices: []
  };
}
```

## Shape Transformations

### Translation

```typescript
function translate(shape: ShapeDefinition, x: number, y: number): ShapeDefinition {
  // TODO: Translate shape
  return shape;
}
```

### Rotation

```typescript
function rotate(shape: ShapeDefinition, angle: number): ShapeDefinition {
  // TODO: Rotate shape
  return shape;
}
```

### Scaling

```typescript
function scale(shape: ShapeDefinition, factor: number): ShapeDefinition {
  // TODO: Scale shape
  return shape;
}
```

## SVG Path Generation

### Path Commands

- `M` - Move to
- `L` - Line to
- `C` - Cubic Bezier curve
- `Q` - Quadratic Bezier curve
- `A` - Arc
- `Z` - Close path

### Example Paths

```typescript
// Circle
const circlePath = `M ${cx - r},${cy} A ${r},${r} 0 1,0 ${cx + r},${cy} A ${r},${r} 0 1,0 ${cx - r},${cy} Z`;

// Triangle
const trianglePath = `M ${x1},${y1} L ${x2},${y2} L ${x3},${y3} Z`;

// Star
const starPath = `M ${points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x},${p.y}`).join(' ')} Z`;
```

## Symbol Library

### Archetype Symbols

TODO: Create SVG library for archetype symbols

### Kindra Glyphs

TODO: Create SVG library for Kindra glyphs

### UI Icons

TODO: Create SVG library for UI icons

## Rendering Guidelines

### Size Guidelines

- **Minimum Size**: 16px (for recognition)
- **Default Size**: 32px (for clarity)
- **Maximum Size**: 128px (for detail)

### Stroke Guidelines

- **Thin**: 1px (for large shapes)
- **Normal**: 2px (for default)
- **Thick**: 3px (for emphasis)

### Fill Guidelines

- Use solid fills for simple shapes
- Use gradients for depth
- Use patterns for texture

## Accessibility

### Shape Distinction

Ensure shapes are distinguishable:
- By form (not just color)
- By size
- By pattern

### Labels

Always provide text labels:
- For screen readers
- For clarity
- For searchability

## Status

**⚠️ TODO: Define all shapes and glyphs**

All shapes are placeholders. No actual SVG paths defined.

## Next Steps

1. Define 12 archetype shapes
2. Create Kindra glyph library
3. Implement shape generation functions
4. Create SVG path library
5. Test rendering at different sizes
6. Ensure accessibility

---

**Version:** 1.0  
**Status:** Placeholder  
**Last Updated:** 2025-11-21
