# TW369 Engine Specification

The **TW369 Engine** models the dynamic tension, drift, and evolution of the system using a tensor-based approach mapped to three fundamental planes: 3 (Action), 6 (Structure), and 9 (Metanoia).

## 1. Core Concepts

### 1.1. The Three Planes
- **Plane 3 (Action/Expansion)**: Represents kinetic energy, movement, growth, and manifestation.
- **Plane 6 (Structure/Contraction)**: Represents potential energy, stability, order, and defense.
- **Plane 9 (Metanoia/Transcendence)**: Represents transformation, synthesis, and the void/source.

### 1.2. Drift
Drift is the measure of system instability or deviation from equilibrium. It is calculated based on the tension between the planes.

### 1.3. Painlevé Filter
A mathematical filter based on Painlevé II transcendents used to smooth drift trajectories and detect critical phase transitions.

## 2. Drift Models

The engine supports four drift models, selectable via configuration.

### 2.1. Model A: Linear Drift (Default)
The baseline model. Drift is a linear function of plane tensions.
`drift = w3*T3 + w6*T6 + w9*T9`

### 2.2. Model B: Nonlinear Drift
Introduces power laws and tanh saturation to model explosive growth and saturation limits.
`drift = tanh( (w3*T3)^k + (w6*T6)^k + ... )`

### 2.3. Model C: Multiscale Drift
Incorporates memory effects, distinguishing between short-term volatility and long-term trends.
`drift = alpha * short_term + beta * long_term`

### 2.4. Model D: Stochastic Drift
Adds severity-dependent Gaussian noise to simulate real-world unpredictability.
`drift = model_a_drift + noise(severity)`

## 3. Adaptive State-Plane Mapping

The influence of each plane on the final Δ144 state is not static. It adapts based on the context.

- **Fixed Mapping**: Static weights (e.g., Plane 3 always contributes 40% to Expansive states).
- **Adaptive Mapping**: Context-aware weights (e.g., in a "Crisis" context, Plane 6 influence is boosted to 80%).

See `docs/TW369_ADAPTIVE_MAPPING.md` for details.

## 4. Schemas

### 4.1. TWState (`schema/tw369/tw369_state_schema.json`)
Defines the structure of the system state.
```json
{
  "plane_3_val": 0.5,
  "plane_6_val": 0.3,
  "plane_9_val": 0.2,
  "drift_metric": 0.15,
  "painleve_coherence": 0.9,
  "evolution_stage": "stable"
}
```

### 4.2. Drift Parameters (`schema/tw369/drift_parameters.json`)
Configures the coefficients and thresholds for drift calculation.
```json
{
  "weights": {"w3": 1.0, "w6": 1.0, "w9": 1.0},
  "advanced_models": {
    "nonlinear": {"enabled": true, "exponent": 1.5},
    "multiscale": {"enabled": true, "short_term_alpha": 0.7},
    "stochastic": {"enabled": true, "noise_scale": 0.1}
  }
}
```

### 4.3. Config (`schema/tw369/tw369_config_schema.json`)
General engine configuration.
```json
{
  "drift_model": "nonlinear",
  "adaptive_mapping_enabled": true
}
```

## 5. Pipeline Flow

```ascii
+--------+    +--------+    +--------+
| Kindra | -> | TW369  | -> | Δ144   |
| Scores |    | Engine |    | Engine |
+--------+    +--------+    +--------+
    |             |             ^
    v             v             |
+--------+    +--------+        |
| Plane  |    | Drift  |        |
| Values | -> | Calc   | -------+
+--------+    +--------+
                  |
                  v
             +----------+
             | Painlevé |
             | Filter   |
             +----------+
```

## 6. Interaction with Kindra

Kindra vectors are mapped to TW369 planes:
- **L1 Vectors** -> Plane 9
- **L2 Vectors** -> Plane 3
- **L3 Vectors** -> Plane 6

This mapping allows cultural and semiotic data to drive the dynamic modeling of the system.

## 7. Future Implementations

*   **Model E (Topological Drift)**: Modeling drift as a deformation of the state manifold itself, not just a scalar value.
*   **Painlevé Phase Detection**: Automatically triggering "State Metamorphosis" when the Painlevé function crosses zero.
*   **Tensor Persistence**: Storing the full 3x3x3 tensor state history for deep temporal analysis.
*   **Drift Alerting System**: Real-time webhooks when drift exceeds critical thresholds (e.g., > 0.8).

## 8. Enhancements (Short/Medium Term)

*   **Vectorized Operations**: Rewriting the core drift calculation using `numpy` for 100x speedup.
*   **Configurable Noise Profiles**: Allowing different "colors" of noise (Pink, White, Brownian) in Model D.
*   **Adaptive Windowing**: Dynamically sizing the Painlevé filter window based on signal volatility.
*   **Drift Visualization**: Generating SVG plots of the drift trajectory for debugging.

## 9. Research Track (Long Term)

*   **Quantum Tensor Networks**: Exploring the use of tensor networks (MPS/PEPS) to model high-dimensional state interactions.
*   **Chaotic Attractor Mapping**: Identifying if the system settles into strange attractors under certain conditions.
*   **Painlevé VI Integration**: Upgrading from Painlevé II to VI for a more general solution to the deformation equations.
*   **Causal Drift Analysis**: Using causal inference to determine *which* vector caused the drift spike.

## 10. Known Limitations

*   **Scalar Reduction**: The current engine reduces complex tensor interactions to a single scalar "Drift Metric", losing information.
*   **Memoryless (mostly)**: Apart from Model C, the drift calculation is largely stateless (Markovian).
*   **Parameter Sensitivity**: The Painlevé filter is highly sensitive to the `window_size` and `alpha` parameters.
*   **No Feedback Loop**: Currently, drift does not feed back into Kindra to adjust vector sensitivity (open loop).
