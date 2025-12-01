# KALDRA v2.7 Release Notes

**Codename:** POLARITY ENGINE & MODIFIER REINTEGRATION
**Version:** 2.7.0
**Status:** STABLE
**Date:** 2025-11-29

## 2.7.1 — Overview

KALDRA v2.7 marks the return and full integration of the system's rich taxonomy, specifically the **46 Polarities** and **59 Modifiers**. While previous versions (v2.3–v2.6) focused on establishing the core engines (Kindra, TW369, Meta-Engines), v2.7 enriches the semantic resolution of the system by allowing these granular descriptors to modulate the entire pipeline.

This version bridges the gap between high-level archetypal dynamics and low-level semantic nuance, ensuring that every narrative signal is colored by specific tensions (Polarities) and transient states (Modifiers).

## 2.7.2 — What Changed

*   **Polarity System Activation**: Implemented `load_polarities()` to ingest the 46 dimensional tensions.
*   **Delta144 Integration**: The `Delta144Engine` now fully supports `Polarity` objects and uses them to refine state inference.
*   **Modifier Auto-Inference**: Leveraging the v2.3 Embedding Generator, the system can now automatically infer active modifiers from input text embeddings, removing the need for manual specification.
*   **Meta-Engine Polarity Extraction**: New logic in `polarity_mapping.py` translates high-level philosophical outputs (Nietzschean/Stoic/Campbellian) into concrete polarity scores (e.g., `POL_ORDER_CHAOS`).
*   **Deep Modulation**:
    *   **Δ12**: Archetype probabilities are now modulated by active polarities (e.g., High Chaos boosts Creator/Destroyer).
    *   **TW369**: Drift severity is modulated by polarity alignment with TW planes.
*   **Story Engine Tracking**: The `StoryAggregator` now tracks polarity oscillations over time, detecting inversions and rapid shifts.
*   **API Adapter**: Updated to expose polarity and modifier data in the standard response format.

## 2.7.3 — New Files

*   `src/archetypes/polarity_mapping.py`: Core logic for mapping meta-signals to polarities.
*   `tests/meta/test_polarity_mapping.py`: Verification of polarity extraction.
*   `tests/archetypes/test_delta12_modulation.py`: Verification of archetype modulation.
*   `tests/tw369/test_tw369_modulation.py`: Verification of drift modulation.
*   `tests/story/test_story_polarity.py`: Verification of narrative tracking.

## 2.7.4 — Modified Files

*   **`src/archetypes/delta144_engine.py`**: Integrated `polarity_scores` into `StateInferenceResult` and added `infer_modifier_scores_from_embedding`.
*   **`src/tw369/tw369_integration.py`**: Added `modulate_state` to adjust plane scores based on polarity alignment.
*   **`src/story/story_buffer.py`**: Added `polarity_scores` to `StoryEvent`.
*   **`src/story/story_aggregator.py`**: Added detection of `polarity_deltas` and `polarity_inversions`.
*   **`src/core/kaldra_master_engine.py`**: Wired up the full polarity extraction and modulation pipeline.

## 2.7.5 — Mathematical & Narrative Effects

*   **Δ144 Selection**: States are no longer just "best semantic match"; they are now "best match that aligns with current tensions."
*   **Δ12 Projection**: The archetypal distribution is "tilted" by polarities. A `POL_ORDER_CHAOS` score of 0.9 (High Chaos) will naturally suppress Ruler/Sage and amplify Trickster/Outlaw.
*   **TW369 Drift**: Polarities act as "wind" for the drift system. Aligned polarities accelerate drift; opposing ones dampen it.
*   **Meta-Engines**: Now act as the "source of truth" for polarity generation, grounding abstract philosophy in measurable vectors.
*   **Story Engine**: Can now detect "The Turn" (Peripeteia) by watching for sudden polarity inversions (e.g., Hope → Despair).

## 2.7.6 — Testing Summary

*   **Total Tests**: 25 new tests added.
*   **Coverage**: 100% coverage of new polarity and modifier logic.
*   **Key Scenarios**:
    *   *Polarity Modulation*: Verified that high chaos scores shift Δ12 distribution.
    *   *Auto-Inference*: Verified that "angry" text infers `MOD_AGGRESSIVE`.
    *   *End-to-End*: Verified that a full pipeline run preserves polarity data from input to signal.

## 2.7.7 — Backward Compatibility

*   **Fully Compatible**: The polarity system is additive. If no polarities are detected or provided, the system falls back to v2.6 behavior.
*   **Feature Flags**: `KALDRA_TW_POLARITY_ENABLED` and `KALDRA_DELTA12_POLARITY_ENABLED` allow granular control.

## 2.7.8 — Next Steps (v2.8 Preview)

*   **The Guardian Layer**: Using these new signals (Polarity/Modifier) to feed the Tau Layer for epistemic risk assessment.
