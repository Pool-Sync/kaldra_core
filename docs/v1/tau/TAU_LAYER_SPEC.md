# KALDRA Tau Layer Specification (v2.8)

**Version:** 1.0 (KALDRA v2.8)
**Status:** Active
**Component:** Epistemic Precision Layer

## Overview

The **Tau Layer** (formerly Epistemic Limiter) acts as the "Guardian of Truth" within the KALDRA architecture. It is responsible for assessing the epistemic reliability of inputs, internal states, and outputs, modulating the system's confidence and behavior to prevent hallucinations, bias amplification, and narrative instability.

Unlike the previous Epistemic Limiter (v1), the Tau Layer is a **dual-phase** system that operates at both the input (pre-inference) and output (post-inference) stages of the pipeline.

## Core Concepts

### Tau Score (τ)
A scalar value `[0.0, 1.0]` representing the system's epistemic confidence.
- **1.0**: Absolute certainty, safe, balanced.
- **0.0**: Critical uncertainty, high risk, chaotic.

### Tau Risk Levels
The Tau Score is classified into four risk levels:
- **LOW** (τ ≥ 0.8): Normal operation.
- **MID** (0.5 ≤ τ < 0.8): Cautionary state.
- **HIGH** (0.2 ≤ τ < 0.5): Active defense.
- **CRITICAL** (τ < 0.2): System lockdown.

### Dual-Phase Operation

1.  **Input Phase (τ_in)**:
    - Analyzes raw input, bias scores, and polarity extremity.
    - Modulates **internal engine parameters** (e.g., drift damping, archetype smoothing) *before* inference runs.
    - Prevents "garbage in" from destabilizing the core engines.

2.  **Output Phase (τ_out)**:
    - Analyzes the generated narrative state, drift trajectory, and meta-engine outputs.
    - Determines the final reliability of the signal.
    - Triggers **Safeguard** actions if necessary.

## Architecture

### Components

- **`TauState`**: Dataclass holding the score, risk level, modifiers, and actions.
- **`TauRiskModel`**: Mathematical model calculating τ based on weighted risk features.
- **`TauPolicy`**: Rule engine determining modifiers and actions based on risk level.
- **`TauLayer`**: Main orchestrator.

### Risk Features

The Tau Score is calculated using a sigmoid function over a weighted sum of risk features:
`τ = sigmoid(baseline - Σ(weight_i * feature_i))`

| Feature | Weight | Description |
| :--- | :--- | :--- |
| **Bias Score** | 2.5 | Detected bias in input or state. |
| **Polarity Extremity** | 2.0 | Distance of polarities from equilibrium (0.5). |
| **Semantic Entropy** | 1.0 | Confusion or lack of clarity in embeddings. |
| **TW Severity** | 1.5 | Tracy-Widom criticality (painlevé coherence). |
| **Drift Instability** | 2.0 | Velocity/Acceleration of narrative drift. |
| **Meta Inversions** | 3.0 | Pathological meta-states (e.g., Active Nihilism). |

## Integration

### Modifiers

The Tau Layer exerts control via dynamic modifiers:

- **`drift_damping`**: Multiplier for TW369 drift velocity. Low τ reduces drift to prevent runaway chaos.
- **`archetype_smoothing`**: Temperature modulator for Δ144 inference. Low τ flattens distributions to express uncertainty.
- **`meta_influence`**: Scaling factor for meta-engine impact.

### Pipeline Flow

1.  **Input**: `Embedding` + `Text`
2.  **Tau Input Phase**: Calculate `τ_in` → Generate `modifiers`.
3.  **Core Engines**:
    - **Δ144**: Apply `archetype_smoothing`.
    - **TW369**: Apply `drift_damping`.
4.  **Tau Output Phase**: Calculate `τ_out` based on engine results.
5.  **Safeguard**: Final check based on `τ_out`.

## Configuration

Configuration is stored in `schema/tau/tau_config.json` and `schema/tau/tau_policy_rules.json`.
