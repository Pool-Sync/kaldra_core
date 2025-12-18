# Δ144 Grid Design

## Overview

This document describes the visual design for the Δ144 Grid visualization.

## Concept

The Δ144 Grid represents:
- **144 States**: Complete state space (12 archetypes × 12 modifiers)
- **Archetype Groups**: Visual grouping by archetype
- **State Transitions**: Paths between states
- **Current State**: Highlighted active state

## Grid Layout

### Structure

**12×12 Grid**

```
[0  ] [1  ] [2  ] ... [11 ]  ← Archetype 0
[12 ] [13 ] [14 ] ... [23 ]  ← Archetype 1
...
[132] [133] [134] ... [143]  ← Archetype 11
```

**Alternative: Grouped Layout**

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Archetype 0 │ │ Archetype 1 │ │ Archetype 2 │
│ [0-11]      │ │ [12-23]     │ │ [24-35]     │
└─────────────┘ └─────────────┘ └─────────────┘
...
```

### Cell Design

**Cell Properties:**
- **Size**: 40×40px (desktop), 24×24px (mobile)
- **Spacing**: 4px gap
- **Border**: 1px solid
- **Border Radius**: 4px

**Cell States:**
- **Default**: Base color, normal opacity
- **Hover**: Lighter color, tooltip
- **Active**: Bold border, highlighted
- **Inactive**: Reduced opacity

### Color Coding

**Archetype Colors**

TODO: Define 12 archetype base colors

**Modifier Variations**

- Lightness variation: 12 steps from dark to light
- Saturation variation: Maintain hue, adjust saturation
- Pattern: Consistent across archetypes

### Labels

**Archetype Labels**
- Position: Above or left of group
- Font: Bold, larger size
- Color: Archetype color

**State Numbers**
- Position: Inside cell (if space) or tooltip
- Font: Small, monospace
- Color: Contrasting with background

## Visual Elements

### Grid Lines

- **Archetype Separators**: Thick lines (2px)
- **State Separators**: Thin lines (1px)
- **Color**: Neutral gray

### Hover Effects

- **Cell Highlight**: Brighten color
- **Related States**: Dim other states
- **Tooltip**: Show state details
  - State number
  - Archetype name
  - Modifier name
  - Description

### Active State Indicator

- **Bold Border**: 3px solid
- **Glow Effect**: Subtle shadow
- **Animation**: Pulse effect

### Transition Paths

**Show State Transitions**
- **Lines**: Connect related states
- **Arrows**: Show direction
- **Color**: Gradient from source to target
- **Animation**: Flow along path

## Interactions

### Click

- **Select State**: Highlight and show details
- **Navigate**: Go to state detail page
- **Compare**: Select multiple for comparison

### Hover

- **Tooltip**: Show state information
- **Highlight**: Emphasize current cell
- **Dim**: Reduce opacity of others

### Filter

- **By Archetype**: Show only selected archetype
- **By Modifier**: Show only selected modifier
- **By Property**: Filter by state properties

### Search

- **By Number**: Find state by number
- **By Name**: Find state by archetype/modifier
- **By Description**: Search state descriptions

## Legend

**Components:**
- **Archetype Colors**: Color swatches with names
- **Modifier Scale**: Lightness/saturation scale
- **State Count**: Total states shown
- **Filter Status**: Active filters

## Responsive Design

### Desktop (>1024px)
- Full 12×12 grid
- All labels visible
- Detailed tooltips
- Transition paths

### Tablet (768-1024px)
- Condensed grid
- Archetype labels only
- Simplified tooltips
- No transition paths

### Mobile (<768px)
- Grouped by archetype
- Expandable groups
- Tap for details
- Minimal labels

## Accessibility

### Keyboard Navigation
- Arrow keys: Navigate cells
- Enter: Select cell
- Tab: Move between sections
- Escape: Clear selection

### Screen Readers
- Announce cell position
- Read state information
- Describe archetype groups
- Provide data table alternative

### Color Contrast
- Ensure text is readable
- Provide pattern alternatives
- Test with color blindness simulators

## Examples

### Default View
- All 144 states visible
- Grouped by archetype
- Neutral state (no selection)

### Filtered View
- Single archetype highlighted
- Other states dimmed
- Filter indicator shown

### Transition View
- Source and target states highlighted
- Transition path shown
- Animation in progress

## Status

**⚠️ TODO: Implement Δ144 Grid visualization**

All design elements are placeholders. No functional implementation.

## Next Steps

1. Define 12 archetype colors
2. Generate 144 state color variations
3. Implement grid layout
4. Add cell interactions
5. Implement filtering
6. Add transition visualization
7. Test responsiveness
8. Ensure accessibility

---

**Version:** 1.0  
**Status:** Placeholder  
**Last Updated:** 2025-11-21
