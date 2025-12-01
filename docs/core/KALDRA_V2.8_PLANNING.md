# KALDRA v2.8 — Tau Layer & Safeguard Integration (PLANNING DOCUMENT)

**Version Target:** v2.8  
**Codename:** "The Guardian Layer"  
**Status:** DRAFT  
**Date:** 2025-11-29  

---

## 1. Overview

KALDRA v2.8 introduces **"The Guardian Layer"**, a fundamental architectural shift that transitions the system from a passive analyzer to an **epistemically aware intelligence**.

This release implements two critical components:
1.  **Tau Layer (Epistemic Precision Layer)**: A regulatory mechanism that calculates the "epistemic reliability" of inputs and internal states, dosing the system's confidence and reactivity.
2.  **Safeguard Engine Integration**: A deep integration with KALDRA Safeguard to detect, classify, and mitigate narrative risks (toxicity, manipulation, polarization, entropy).

**Core Philosophy**: v2.8 is about **trusting the input less and the system more**. It adds self-preservation and cognitive security to the KALDRA pipeline.

---

## 2. Components to Design

### 2.1. Tau Layer (Epistemic Limiter v2)

The Tau Layer acts as the system's "cognitive brakes" and "reliability filter".

**Functions:**
1.  **Calculate Epistemic Reliability**: Assess input quality, coherence, and safety.
2.  **Dose Influence**: Modulate the weight of Δ12, Δ144, Kindra, and Meta-Engines based on reliability.
3.  **Regulate Drift**: Dampen TW369 drift velocity in high-uncertainty or high-risk scenarios.
4.  **Protect System**: Prevent narrative hijacking or destabilization.

**Core Elements:**
-   **TauScore (0.0 - 1.0)**: The calculated reliability score. 1.0 = High Confidence/Safety, 0.0 = Critical Uncertainty/Risk.
-   **TauWeight**: A damping factor applied to system dynamics (e.g., `drift_velocity * tau_weight`).
-   **TauCategory**: Risk classification (`LOW`, `MID`, `HIGH`, `CRITICAL`).
-   **TauPolicy**: Rules defining how the engine reacts to each category.

**Data Representation:**
```python
@dataclass
class TauState:
    tau_score: float
    tau_risk: str  # "LOW", "MID", "HIGH", "CRITICAL"
    tau_modifiers: Dict[str, float]  # e.g., {"drift_damping": 0.5, "archetype_suppression": 0.2}
    tau_actions: List[str]  # e.g., ["CLAMP_DRIFT", "FLAG_UNCERTAINTY"]
```

### 2.2. Safeguard Engine Integration

The Safeguard Engine provides the semantic and narrative risk analysis that feeds into the Tau Layer.

**Capabilities:**
-   **Polarity Risk**: Detects dangerous polarity extremes (e.g., extreme Chaos + extreme Destruction).
-   **Meta-Risk**: Analyzes Nietzsche/Aurelius outputs for pathological states (e.g., Active Nihilism + Resentment).
-   **Drift Risk**: Identifies destabilizing drift trajectories.
-   **Narrative Harm**: Detects extremism, manipulation, and shadow loops.

**Safeguard Signal:**
```python
@dataclass
class SafeguardSignal:
    bias: Dict[str, Any]
    polarity_risk: Dict[str, float]
    drift_risk: Dict[str, float]
    journey_risk: Dict[str, float]
    meta_risk: Dict[str, float]
    final_risk: str  # "LOW", "MID", "HIGH", "CRITICAL"
    risk_score: float  # 0.0 - 1.0
```

---

## 3. v2.8 Architecture

### New Modules

**`src/tau/`**
-   `tau_layer.py`: Main entry point and logic for Tau calculation.
-   `tau_state.py`: Data structures for Tau state.
-   `tau_policy.py`: Policy definitions and action resolution.
-   `tau_risk_model.py`: Mathematical model for risk aggregation.
-   `tau_integration.py`: Helpers for integrating Tau into Master Engine.

**`src/safeguard/`**
-   `safeguard_engine.py`: Core Safeguard logic.
-   `safeguard_risk_model.py`: Risk scoring and classification.
-   `safeguard_policy.py`: Mitigation strategies.
-   `safeguard_integration.py`: Bridge to KALDRA core.

### New Schemas

-   `schema/tau/tau_config.json`: Configuration for Tau thresholds and weights.
-   `schema/tau/tau_policy_rules.json`: Rules mapping risks to actions.
-   `schema/safeguard/safeguard_risk_rules.json`: Definitions of risk patterns.
-   `schema/safeguard/safeguard_journey_map.json`: Risk mapping for Hero's Journey stages.

---

## 4. Pipeline Integration

The Tau Layer is applied **twice** in the pipeline: first to assess the raw input (Input Phase), and second to regulate the final output state (Output Phase).

```
[Input Text]
     ↓
[Bias Engine] → [Polarity Scores] → [Modifier Scores]
     ↓
┌───────────────────────────────┐
│  Tau Layer (Input Phase)      │ ◀── Calculates initial TauScore
└───────────────────────────────┘     (Based on Bias, Polarity Extremes)
     ↓
[Embeddings]
     ↓
[Kindra 3×48]
     ↓
[TW369 + Drift Memory] ◀─── Modulated by TauWeight (Drift Damping)
     ↓
[Meta Engines] (Nietzsche/Aurelius/Campbell)
     ↓
[Δ12 + Δ144] ◀─── Modulated by TauWeight (Probability Smoothing)
     ↓
[Story Engine (v2.6)]
     ↓
┌───────────────────────────────┐
│  Tau Layer (Output Phase)     │ ◀── Final Safety Check
└───────────────────────────────┘     (Checks for Shadow Loops, Instability)
     ↓
[Safeguard Engine] ◀─── Generates detailed risk report
     ↓
[Final KALDRA Signal]
```

---

## 5. Tau Math

The TauScore is calculated using a weighted sigmoid function of various risk features.

**Formula:**
`TauScore = sigmoid(baseline - weighted_sum(risk_features))`

**Features:**
1.  **Bias Score**: From Bias Engine.
2.  **Polarity Extremity**: Distance of polarities from neutral (0.5).
3.  **Semantic Entropy**: Confusion/ambiguity in embeddings.
4.  **TW Severity**: High severity increases risk.
5.  **Narrative Instability**: Rapid shifts in Story Engine.
6.  **Meta-Inversions**: Pathological meta-states (e.g., high Resentment).

**TauWeight Application:**
-   `drift_velocity_new = drift_velocity_raw * TauWeight`
-   `archetype_prob_new = normalize(archetype_prob_raw ^ TauWeight)` (Temperature scaling)

---

## 6. Safeguard Risk Model

**Risk Dimensions:**
1.  **Toxicity**: Direct harm, hate speech.
2.  **Manipulation**: Emotional coercion, deceit.
3.  **Polarization**: Us vs. Them, divisive rhetoric.
4.  **Extremism**: Radical ideology, violence.
5.  **Distortion**: Epistemic warping, gaslighting.
6.  **Shadow Loops**: Repetitive negative narrative cycles.

**Ontology:**
-   Defined in `schema/safeguard/safeguard_risk_rules.json`.
-   Maps specific combinations of Polarities + Modifiers + Meta-States to Risk Levels.

---

## 7. KALDRA v2.8 Signal Extensions

The `KaldraSignal` will be extended with:

```json
{
  ...
  "tau": {
    "score": 0.85,
    "risk_level": "LOW",
    "applied_actions": []
  },
  "safeguard": {
    "toxicity": 0.05,
    "manipulation": 0.10,
    "risk_flags": []
  },
  "risk_summary": "LOW"
}
```

---

## 8. Testing Plan

1.  **Unit Tests**:
    -   Verify Tau math (sigmoid, weighting).
    -   Verify Safeguard rule matching.
2.  **Integration Tests**:
    -   Full pipeline run with Tau enabled.
    -   Verify drift damping works when Tau is low.
3.  **Scenario Tests**:
    -   **"The Demagogue"**: Input highly manipulative text -> Expect Low Tau, High Safeguard Risk.
    -   **"The Panic"**: Input chaotic/fearful text -> Expect Drift Damping.
4.  **Edge Cases**:
    -   Zero input, noise input.
    -   Perfectly neutral input (Tau should be 1.0).

---

## 9. Documentation Requirements

-   `docs/tau/TAU_LAYER_SPEC.md`: Detailed mathematical spec.
-   `docs/safeguard/SAFEGUARD_ENGINE_SPEC.md`: Risk model and integration details.
-   `docs/safeguard/RISK_TAXONOMY.md`: Definitions of risk categories.
-   `docs/core/KALDRA_V2.8_RELEASE_NOTES.md`: Release documentation.

---

## 10. Acceptance Criteria

-   [ ] **Tau Layer** active in both Input and Output phases.
-   [ ] **Safeguard Engine** fully integrated and producing signals.
-   [ ] **Signal Extension**: `tau` and `safeguard` fields present in output.
-   [ ] **Modulation**: Δ12/Δ144 and TW369 demonstrably respond to TauScore (damping).
-   [ ] **Meta-Integration**: Meta-Engines contribute to risk mapping.
-   [ ] **Documentation**: All specs created and up-to-date.
-   [ ] **Tests**: >90% pass rate, including new risk scenarios.
-   [ ] **Regression**: No degradation of v2.3–v2.7 features.
