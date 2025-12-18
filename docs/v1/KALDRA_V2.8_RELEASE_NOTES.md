# KALDRA v2.8 Release Notes

**Codename:** THE GUARDIAN LAYER
**Version:** 2.8.0
**Status:** STABLE
**Date:** 2025-11-29

## 2.8.1 — Overview

KALDRA v2.8 introduces **"The Guardian Layer"**, a fundamental architectural shift that prioritizes **Epistemic Confidence** and **Narrative Safety**. This release fuses two new critical components: the **Tau Layer** (Epistemic Limiter v2) and the **Safeguard Engine**.

Together, they transform KALDRA from a passive generator into a self-regulating system capable of assessing its own certainty and preventing narrative hazards. The system now "thinks before it speaks" (Input Phase) and "checks what it said" (Output Phase).

## 2.8.2 — What Changed

*   **Tau Layer Implementation**: A complete rewrite of the epistemic system.
    *   **TauScore (τ)**: A dynamic confidence metric `[0.0, 1.0]`.
    *   **TauRisk**: Classification of confidence into `LOW`, `MID`, `HIGH`, `CRITICAL`.
    *   **Dual-Phase Operation**:
        *   **Input Phase**: Analyzes raw input bias and polarity to modulate internal engines *before* inference.
        *   **Output Phase**: Analyzes generated narrative stability to determine final reliability.
*   **Deep Integration**:
    *   **Δ12 Smoothing**: Low Tau scores flatten archetype distributions, expressing uncertainty.
    *   **TW369 Regulation**: High risk triggers `drift_damping`, preventing runaway chaos.
    *   **Meta-Pathology**: Meta-engine states (e.g., Nihilism) now directly feed into risk models.

## 2.8.3 — Safeguard Engine

A new dedicated engine for ethical and narrative safety.

*   **New Modules**:
    *   `src/safeguard/safeguard_engine.py`
    *   `src/safeguard/safeguard_policy.py`
    *   `src/safeguard/safeguard_risk_model.py`
    *   `src/safeguard/safeguard_integration.py`
*   **Risk Taxonomy**:
    *   **Toxicity**: Harmful content.
    *   **Manipulation**: Deceptive framing.
    *   **Polarization**: Extreme "us vs. them" dynamics.
    *   **Extremism**: Radicalized archetypal expression.
    *   **Distortion / Shadow Loops**: Narrative entrapment in negative states.

## 2.8.4 — New Schemas

*   `schema/tau/tau_config.json`: Configuration for Tau sensitivity.
*   `schema/tau/tau_policy_rules.json`: Rules mapping risk levels to modifiers.
*   `schema/safeguard/safeguard_risk_rules.json`: Definitions of risk weights.
*   `schema/safeguard/safeguard_journey_map.json`: Risk profiles for different journey stages.

## 2.8.5 — New Output Format

The `KaldraSignal` now includes dedicated blocks for the Guardian Layer:

```json
{
  "tau": {
    "tau_score": 0.85,
    "tau_risk": "LOW",
    "tau_modifiers": {
      "drift_damping": 1.0,
      "archetype_smoothing": 1.0
    },
    "tau_actions": []
  },
  "safeguard": {
    "final_risk": "LOW",
    "risk_score": 0.12,
    "mitigation_actions": [],
    "bias": { "score": 0.0 },
    "polarity_risk": { "score": 0.1 },
    "drift_risk": { "score": 0.05 }
  },
  "risk_summary": "LOW"
}
```

## 2.8.6 — Mathematical Specification (Mini)

*   **Tau Score**: `τ = sigmoid(baseline - Σ(weight_i * feature_i))`
*   **Drift Damping**: `velocity_new = velocity_old * tau_modifiers['drift_damping']`
*   **Archetype Smoothing**: `temperature = base_temp / max(0.1, smoothing_factor)` (Higher temperature = flatter distribution)

## 2.8.7 — Testing Summary

*   **New Unit Tests**: Comprehensive suites for `TauLayer` and `SafeguardEngine`.
*   **Integration Tests**: `test_tau_pipeline_integration.py` verifies the full loop.
*   **Scenarios**:
    *   *"The Demagogue"* (High Manipulation/Polarization) → Triggers `HIGH` risk and `DAMPEN_DRIFT`.
    *   *"The Panic"* (High Drift/Chaos) → Triggers `MID` risk and `CLAMP_DRIFT`.
    *   *"The Extremist"* (High Toxicity) → Triggers `CRITICAL` risk and `BLOCK_OUTPUT`.

## 2.8.8 — Backward Compatibility

*   **Optional**: The Guardian Layer is enabled by default in `KaldraMasterEngineV2` but can be configured or bypassed if needed.
*   **Non-Breaking**: Existing consumers of `KaldraSignal` can ignore the new `tau` and `safeguard` fields without issue.

## 2.8.9 — Next Steps (v2.9 Preview)

*   **Hardening & Performance**: Optimizing the new multi-stage pipeline.
*   **The Mirror Stage**: Implementing recursive self-reflection.
