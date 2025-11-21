# KALDRA Visual Engine - Chart Components

## Overview

The `charts/` directory contains specialized visualization components for KALDRA symbolic systems.

## Components

### `delta144_grid.tsx`
Grid visualization of the 144-state Δ144 system.

**Features:**
- 12x12 grid layout (or custom)
- Color-coded states
- Archetype grouping
- Interactive state selection

### `tw369_wave.tsx`
Wave pattern visualization for TW369 drift dynamics.

**Features:**
- SVG wave rendering
- Drift intensity coloring
- Phase markers
- Tracy-Widom distribution reference

### `drift_map.tsx`
Heatmap/contour visualization of drift patterns.

**Features:**
- Drift intensity heatmap
- Vector field overlay
- Time animation
- Resonance zones

### `polarity_axes.tsx`
Multi-dimensional polarity visualization.

**Features:**
- 2D/3D axis rendering
- Archetype positioning
- Polarity gradients
- Interactive rotation

### `kindra_radar.tsx`
Radar chart for Kindra symbolic dimensions.

**Features:**
- Multi-axis radar
- Dimension labels
- Comparison overlays
- Value indicators

### `kindra_glyph_grid.tsx`
Grid display of Kindra symbolic glyphs.

**Features:**
- Glyph library
- SVG symbol rendering
- Search and filtering
- Interactive tooltips

### `cultural_vector_map.tsx`
Vector field visualization of cultural dynamics.

**Features:**
- Flow arrows
- Cultural clusters
- Narrative paths
- Time animation

### `archetype_badge.tsx`
Badge/card component for archetype display.

**Features:**
- Archetype icon
- Color coding
- Polarity indicators
- State count

### `state_transition_map.tsx`
Graph visualization of Δ144 state transitions.

**Features:**
- Node-edge graph
- Transition probabilities
- Time animation
- Interactive exploration

### `narrative_spiral.tsx`
Spiral visualization of narrative evolution.

**Features:**
- Spiral path rendering
- Event plotting
- Time markers
- Zoom/pan controls

### `meta_signal_arc.tsx`
Arc visualization of meta-signal patterns.

**Features:**
- Arc path rendering
- Signal nodes
- Resonance zones
- Interactive selection

## Status

**⚠️ All components are placeholders. No functional logic implemented.**

## Integration

All chart components:
- Accept data via props
- Use core rendering engine
- Apply design system tokens
- Support interactions (hover, click, zoom)
