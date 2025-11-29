# KALDRA v2.7 Release Notes: "Axes & Masks"

**Date:** November 29, 2025
**Version:** 2.7.0
**Codename:** Axes & Masks

## Overview

KALDRA v2.7 introduces the **Polarity System**, a dimensional layer that sits between the raw mathematical engines (TW369, Δ144) and the narrative output. This update enables the system to track, measure, and modulate 46 distinct "tensions" (e.g., Order vs. Chaos, Individual vs. Collective) derived from the Meta-Engines (Nietzsche, Aurelius, Campbell).

Additionally, this release brings **Modifier Auto-Inference**, allowing the system to automatically detect and apply archetype modifiers (e.g., "Wounded", "Exiled") based on semantic embedding similarity, removing the need for manual tagging.

## Key Features

### 1. Polarity System (46 Axes)
- **Dimensional Tensions**: Defined 46 core polarities covering Cultural, Semiotic, and Structural planes.
- **Meta-Engine Mapping**: Automatically extracts polarity scores from Nietzsche (12 axes), Aurelius (12 axes), and Campbell (12 stages) outputs.
- **Modulation**:
  - **Δ12 Archetypes**: Polarities now boost or suppress specific archetypes (e.g., High "Chaos" boosts Rebel/Trickster).
  - **TW369 Planes**: Polarities modulate the tension of specific Time Planes (e.g., High "Collective" boosts Plane 3).

### 2. Modifier Auto-Inference
- **Embedding-Based Detection**: `Delta144Engine` now calculates cosine similarity between input text and modifier definitions.
- **Dynamic Application**: Modifiers are applied automatically during inference if their score exceeds a threshold.
- **Backward Compatibility**: Fully compatible with existing manual modifier overrides.

### 3. Story Engine Integration
- **Narrative Oscillations**: The Story Engine now tracks "Polarity Deltas" between events.
- **Inversion Detection**: Automatically detects rapid shifts in polarity (e.g., a sudden flip from "Hope" to "Despair"), flagging them as significant inflection points.
- **Persistent Memory**: `StoryEvent` now stores the full 46-dimensional polarity state.

## Technical Changes

### Core Engine
- **`src/core/kaldra_master_engine.py`**: Integrated `extract_polarity_scores` and wired up the full pipeline.
- **`src/config.py`**: Added feature flags `KALDRA_TW_POLARITY_ENABLED` and `KALDRA_DELTA12_POLARITY_ENABLED`.

### Archetypes
- **`src/archetypes/delta12_vector.py`**: Added `modulate()` method and `ARCHETYPE_POLARITY_MAP`.
- **`src/archetypes/delta144_engine.py`**: Added `infer_modifier_scores_from_embedding()` and updated `infer_state()`.
- **`src/archetypes/polarity_mapping.py`**: New module for mapping Meta-Engine outputs to Polarities.

### Meta-Engines
- **`src/meta/nietzsche.py`**: Updated to return serializable results and fixed mapping keys.
- **`src/meta/aurelius.py`**: Updated to return serializable results.

### Story Engine
- **`src/story/story_buffer.py`**: Added `polarity_scores` to `StoryEvent`.
- **`src/story/story_aggregator.py`**: Added polarity motion tracking and inversion detection.

## Breaking Changes
- None. All new features are additive or behind feature flags.
- `Delta144Engine` constructor signature updated but remains compatible with keyword arguments.

## Verification
- **Unit Tests**: 100% pass rate for new modules (`test_delta12_modulation`, `test_tw369_modulation`, `test_story_polarity`).
- **Integration Tests**: End-to-end flow verified in `tests/integration/test_v2_7_end_to_end.py`.

## Next Steps (v2.8)
- **"The Mirror"**: Implementation of the self-reflective feedback loop using the new Polarity data.
- **Advanced Visualization**: UI components to visualize the 46 axes in real-time.
