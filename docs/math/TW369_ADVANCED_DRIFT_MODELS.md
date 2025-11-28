# TW369 — Advanced Drift Models

## 1. Overview

This document describes the **Advanced Drift Models** for TW369, which extend the baseline Model A with three additional mathematical formulations:

- **Model A (Linear)**: Baseline linear drift (preserved for backward compatibility)
- **Model B (Nonlinear)**: Non-linear response using power + tanh transformations
- **Model C (Multiscale)**: Temporal memory with short-term and long-term components
- **Model D (Stochastic)**: Controlled Gaussian noise injection

## 2. Model Selection

The drift model is selected via configuration:

```json
{
  "drift_model": "model_a"  // Options: "model_a", "nonlinear", "multiscale", "stochastic"
}
```

**Default**: `model_a` (preserves existing behavior)

## 3. Model Descriptions

### Model A: Linear Drift (Baseline)

**Formula**:
```
drift[key] = (gradient[key] / k) * severity
```

Where:
- `gradient`: Tension difference between planes
- `k`: Normalization factor = max(1.0, |g_3_6| + |g_6_9| + |g_9_3|)
- `severity`: Global severity factor ∈ [0, 1]

**Characteristics**:
- Linear scaling with severity
- Preserves gradient signs
- Normalized to prevent extreme values

**Use Case**: Default behavior, stable and predictable

---

### Model B: Nonlinear Drift

**Formula**:
```
g' = tanh(sign(g) * |g|^p / tanh_scale)
drift[key] = (g' / k) * severity
```

**Parameters** (in `drift_parameters.json`):
```json
{
  "advanced_models": {
    "nonlinear": {
      "enabled": false,
      "exponent": 1.5,
      "tanh_scale": 1.0,
      "mode": "power_then_tanh"
    }
  }
}
```

**Characteristics**:
- Power transformation emphasizes strong gradients
- Tanh bounds output to [-1, 1]
- Preserves gradient signs
- Saturates at extremes

**Use Case**: When strong tensions should dominate, but with bounded response

---

### Model C: Multiscale Drift

**Formula**:
```
d_short = α * d_instant + (1 - α) * d_last
d_long  = β * d_instant + (1 - β) * d_long_prev
```

**Parameters**:
```json
{
  "advanced_models": {
    "multiscale": {
      "enabled": false,
      "short_term_alpha": 0.7,
      "long_term_beta": 0.3
    }
  }
}
```

**Characteristics**:
- Combines instantaneous drift with memory
- Short-term (α): Fast adaptation to current state
- Long-term (β): Slow baseline drift
- Stateful (maintains `DriftState`)

**Use Case**: When temporal smoothing and memory effects are important

---

### Model D: Stochastic Drift

**Formula**:
```
sigma = base_sigma * (1 + severity * severity_scale)
drift[key] = base_drift[key] + N(0, sigma)
```

**Parameters**:
```json
{
  "advanced_models": {
    "stochastic": {
      "enabled": false,
      "base_sigma": 0.05,
      "severity_scale": 0.5,
      "random_seed": null
    }
  }
}
```

**Characteristics**:
- Adds Gaussian noise to linear drift
- Noise scales with severity
- Reproducible with `random_seed`
- Non-deterministic without seed

**Use Case**: Modeling uncertainty or exploring drift variations

---

## 4. Configuration

### Schema Files

**`schema/tw369/drift_parameters.json`**:
Contains `advanced_models` block with all model parameters.

**`schema/tw369/tw369_config_schema.json`**:
Contains `drift_model` field for model selection.

### Example Configuration

```json
{
  "enabled": true,
  "drift_model": "nonlinear",
  "drift_parameters_ref": "schema/tw369/drift_parameters.json"
}
```

Then in `drift_parameters.json`:

```json
{
  "advanced_models": {
    "default_model": "model_a",
    "nonlinear": {
      "enabled": true,
      "exponent": 1.5,
      "tanh_scale": 1.0
    }
  }
}
```

## 5. Usage Examples

### Example 1: Using Model A (Default)

```python
from src.tw369.tw369_integration import TW369Integrator, TWState

integrator = TW369Integrator()
state = TWState(
    plane3_cultural_macro={"E01": 0.3},
    plane6_semiotic_media={"E01": 0.1},
    plane9_structural_systemic={"E01": -0.2}
)

drift = integrator.compute_drift(state)
# Uses Model A by default
```

### Example 2: Enabling Nonlinear Model

```python
integrator = TW369Integrator()

# Configure for nonlinear
integrator._drift_model = "nonlinear"
integrator._drift_model_config.nonlinear_enabled = True
integrator._drift_model_config.nonlinear_exponent = 2.0

drift = integrator.compute_drift(state)
# Uses Model B with custom exponent
```

### Example 3: Multiscale with Memory

```python
integrator = TW369Integrator()
integrator._drift_model = "multiscale"
integrator._drift_model_config.multiscale_enabled = True

# First call initializes state
drift1 = integrator.compute_drift(state)

# Second call uses memory from first
drift2 = integrator.compute_drift(state)

# drift2 incorporates memory from drift1
```

### Example 4: Stochastic with Reproducibility

```python
integrator = TW369Integrator()
integrator._drift_model = "stochastic"
integrator._drift_model_config.stochastic_enabled = True
integrator._drift_model_config.stochastic_seed = 42

drift1 = integrator.compute_drift(state)
drift2 = integrator.compute_drift(state)

# drift1 == drift2 (reproducible with seed)
```

## 6. Mathematical Properties

### Model A (Linear)
- **Linearity**: drift ∝ severity
- **Normalization**: Bounded by k
- **Stability**: Always stable

### Model B (Nonlinear)
- **Saturation**: Output bounded to [-1, 1]
- **Emphasis**: Strong gradients emphasized by power
- **Smoothness**: Continuous and differentiable

### Model C (Multiscale)
- **Memory**: Exponential moving average
- **Statefulness**: Requires `DriftState`
- **Convergence**: Converges to instantaneous drift

### Model D (Stochastic)
- **Variance**: σ² ∝ (1 + severity)²
- **Distribution**: Gaussian noise
- **Reproducibility**: Deterministic with seed

## 7. Integration with TW369

The advanced models are integrated into `TW369Integrator.compute_drift()`:

1. Compute plane tensions
2. Calculate severity factor
3. Compute tension gradients
4. Select model based on `_drift_model`
5. Apply model-specific transformation
6. Return drift dictionary

**Fallback**: Always falls back to Model A if model is invalid or disabled.

## 8. Testing

Run the test suite:

```bash
pytest tests/core/test_advanced_drift_models.py \
       tests/integration/test_tw369_advanced_drift_selection.py -v
```

Tests verify:
- Model A linear scaling
- Model B tanh bounding
- Model C memory accumulation
- Model D reproducibility with seed
- Integration with TW369Integrator
- Fallback to Model A

## 9. Performance Considerations

- **Model A**: Fastest (simple arithmetic)
- **Model B**: Moderate (power + tanh computations)
- **Model C**: Moderate (state management overhead)
- **Model D**: Moderate (RNG overhead)

All models are O(1) in the number of planes (always 3).

## 10. Future Extensions

Potential future models:

- **Model E (Adaptive)**: Learning-based drift adjustment
- **Model F (Coupled)**: Cross-plane coupling effects
- **Model G (Hierarchical)**: Multi-level drift decomposition

## 11. References

- TW369 Engine Spec: `docs/TW369_ENGINE_SPEC.md`
- Drift Parameters: `schema/tw369/drift_parameters.json`
- Config Schema: `schema/tw369/tw369_config_schema.json`
- Implementation: `src/tw369/advanced_drift_models.py`
- Integration: `src/tw369/tw369_integration.py`
