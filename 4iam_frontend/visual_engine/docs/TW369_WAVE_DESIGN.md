# TW369 Wave Design

## Overview

This document describes the visual design for TW369 wave visualizations.

## Concept

The TW369 Wave visualization represents:
- **Wave Patterns**: Oscillating dynamics in data
- **Drift**: Deviation from expected patterns
- **Resonance**: Alignment with Tracy-Widom distribution
- **Phase**: Position in wave cycle

## Visual Elements

### Wave Path

**SVG Path Representation**

```typescript
// TODO: Generate wave path
function generateWavePath(
  amplitude: number,
  frequency: number,
  phase: number,
  length: number
): string {
  // Calculate wave points
  // Generate smooth SVG path
  return "";
}
```

**Properties:**
- **Amplitude**: Wave height (drift intensity)
- **Frequency**: Wave oscillation rate
- **Phase**: Starting position in cycle
- **Length**: Total wave duration

### Drift Coloring

**Color Mapping**

| Drift Level | Color | Meaning |
|-------------|-------|---------|
| Low (0-0.3) | TODO | Stable, predictable |
| Medium (0.3-0.7) | TODO | Moderate drift |
| High (0.7-1.0) | TODO | High drift, anomaly |

**Gradient Application:**
- Apply color gradient along wave path
- Intensity corresponds to drift value
- Smooth transitions between levels

### Phase Markers

**Visual Indicators**

- **Vertical Lines**: Mark wave phases
- **Labels**: Phase numbers (0, 3, 6, 9)
- **Spacing**: Evenly distributed
- **Style**: Subtle, non-intrusive

### Tracy-Widom Reference

**Reference Line**

- **Position**: Overlay on wave
- **Style**: Dashed line
- **Color**: Neutral gray
- **Purpose**: Show expected distribution

## Layout

### Axes

**X-Axis (Time)**
- Label: "Time" or custom dimension
- Ticks: Regular intervals
- Format: Timestamps or indices

**Y-Axis (Amplitude)**
- Label: "Drift Intensity"
- Ticks: 0.0 to 1.0 (normalized)
- Format: Decimal values

### Grid

- **Background Grid**: Light, subtle
- **Major Lines**: Every 0.25 on Y-axis
- **Minor Lines**: Every 0.1 on Y-axis

### Legend

- **Drift Levels**: Color scale
- **Phase Markers**: Symbol explanation
- **Reference Line**: Tracy-Widom indicator

## Interactions

### Hover

- **Highlight**: Current wave segment
- **Tooltip**: Show exact values
  - Time/position
  - Drift value
  - Phase
  - Resonance score

### Zoom

- **X-Axis Zoom**: Focus on time range
- **Y-Axis Zoom**: Adjust amplitude scale
- **Reset**: Return to full view

### Pan

- **Horizontal Pan**: Scroll through time
- **Vertical Pan**: Adjust view window

## Animation

### Wave Motion

```typescript
// TODO: Animate wave
function animateWave(config: AnimationConfig) {
  // Animate wave phase shift
  // Update wave path over time
  // Create flowing effect
}
```

**Properties:**
- **Duration**: 3-5 seconds per cycle
- **Easing**: Sine wave (natural)
- **Loop**: Continuous

### Drift Pulse

**Highlight High Drift**
- Pulse effect on high drift segments
- Attract attention to anomalies
- Subtle, non-distracting

## Responsive Design

### Desktop (>1024px)
- Full wave visualization
- All phase markers visible
- Detailed tooltips

### Tablet (768-1024px)
- Condensed wave
- Fewer phase markers
- Simplified tooltips

### Mobile (<768px)
- Minimal wave
- Essential markers only
- Tap for details

## Accessibility

### Color Blindness
- Use patterns in addition to colors
- Provide text labels
- Ensure sufficient contrast

### Screen Readers
- Describe wave pattern
- Announce drift levels
- Provide data table alternative

## Examples

### Low Drift Wave
- Smooth, regular oscillation
- Cool colors (blue, green)
- Minimal deviation from reference

### High Drift Wave
- Irregular, chaotic pattern
- Warm colors (orange, red)
- Significant deviation from reference

### Resonance Event
- Alignment with Tracy-Widom
- Special marker or highlight
- Annotation explaining significance

## Status

**⚠️ TODO: Implement TW369 wave visualization**

All design elements are placeholders. No functional implementation.

## Next Steps

1. Implement wave path generation
2. Define drift color gradient
3. Add phase markers
4. Overlay Tracy-Widom reference
5. Implement interactions
6. Add animations
7. Test responsiveness
8. Ensure accessibility

---

**Version:** 1.0  
**Status:** Placeholder  
**Last Updated:** 2025-11-21
