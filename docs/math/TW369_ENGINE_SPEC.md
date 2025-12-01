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

## 7. v2.4 — Deepening Plan (TW369 + Tracy-Widom + Painlevé)

**Status**: Planning Document (No Code Changes Yet)

### 7.1. Tracy-Widom Layer (Plane of Extremes)

**Current State**: `_compute_severity_factor` uses heuristic approximation

```python
# Current (heuristic)
severity = tanh(instability_index * 2.0)
```

**v2.4 Vision**: Real Tracy-Widom statistics

#### Proposed Approach

1. **Lookup Table Implementation**
   - Pre-compute Tracy-Widom CDF for common parameter ranges
   - Store in `schema/tw369/tracy_widom_lookup.json`
   - Interpolate for runtime queries

2. **Parametric Approximation**
   - Fit polynomial or rational function to TW distribution
   - Configurable via `schema/tw369/tw_parameters.json`
   - Parameters: β (ensemble type: 1, 2, 4), scale, location

3. **Collection-Based Analysis**
   - Apply TW not to single calls, but to **windows of events**
   - Example: Analyze 10 consecutive earnings calls
   - Detect extreme deviations in the collection

#### Files to Create/Modify (v2.4)
- `schema/tw369/tracy_widom_lookup.json` (NEW)
- `schema/tw369/tw_parameters.json` (NEW)
- `src/tw369/tracy_widom.py` (NEW - TW module)
- `src/tw369/integration.py` (MODIFY - use TW module)

#### Acceptance Criteria
- [ ] TW lookup table covers β=1,2,4 with 0.01 precision
- [ ] `_compute_severity_factor` uses real TW CDF
- [ ] Window-based TW analysis for collections
- [ ] Configurable TW parameters via schema

---

### 7.2. Painlevé II Calibration

**Current State**: `PainleveIISolver` exists with hardcoded parameters

```python
# Current (hardcoded)
solver = PainleveIISolver(alpha=0.0, x_start=-5.0, x_end=5.0)
```

**v2.4 Vision**: Configurable, regime-aware Painlevé

#### Proposed Approach

1. **Schema-Driven Configuration**
   - Move all Painlevé parameters to `schema/tw369/painleve_config.json`
   - Parameters: `alpha`, `x_range`, `step_size`, `tolerance`

2. **Regime-Specific Calibration**
   - Map Δ12 archetypes to Painlevé parameter sets
   - Example:
     ```json
     {
       "A07_RULER": {"alpha": 0.0, "sensitivity": "low"},
       "A08_REBEL": {"alpha": 0.5, "sensitivity": "high"}
     }
     ```

3. **Adaptive Filter Windows**
   - Adjust Painlevé filter window based on drift volatility
   - High volatility → shorter window (faster response)
   - Low volatility → longer window (smoother trajectory)

#### Files to Create/Modify (v2.4)
- `schema/tw369/painleve_config.json` (NEW)
- `schema/tw369/regime_calibration.json` (NEW)
- `src/tw369/painleve/painleve2_solver.py` (MODIFY - load from schema)
- `src/tw369/painleve/painleve_filter.py` (MODIFY - adaptive windows)

#### Acceptance Criteria
- [ ] All Painlevé parameters configurable via schema
- [ ] Regime-specific calibration for 12 archetypes
- [ ] Adaptive filter window based on volatility
- [ ] Documented mapping: Δ12/Δ144 → Painlevé params

---

### 7.3. Drift Memory & State Persistence

**Current State**: Mostly stateless (except Model C short-term memory)

**v2.4 Vision**: Full drift memory with persistence

#### Proposed Approach

1. **DriftState Dataclass**
   ```python
   @dataclass
   class DriftState:
       timestamp: float
       plane_values: Dict[str, float]  # 3, 6, 9
       drift_metric: float
       painleve_coherence: float
       history_window: List[Dict]  # Last N states
       regime: str  # Current Δ12 regime
   ```

2. **Serialization**
   - JSON-serializable format
   - Save/load from file or database
   - Schema: `schema/tw369/drift_state_schema.json`

3. **Sliding Window Memory**
   - Maintain last N events (configurable, default 10)
   - Use for:
     - Trend detection
     - Volatility estimation
     - Regime change detection

4. **Storage Integration**
   - **v2.4**: In-memory (Python dict)
   - **v2.5+**: Redis (fast, ephemeral)
   - **v2.6+**: PostgreSQL (persistent, queryable)

#### Files to Create/Modify (v2.4)
- `schema/tw369/drift_state_schema.json` (NEW)
- `src/tw369/drift_state.py` (NEW - DriftState class)
- `src/tw369/drift_memory.py` (NEW - memory management)
- `src/tw369/integration.py` (MODIFY - use drift memory)

#### Acceptance Criteria
- [ ] `DriftState` fully serializable to JSON
- [ ] Sliding window memory (configurable size)
- [ ] In-memory storage working
- [ ] Save/load drift state to/from file
- [ ] API to query drift history

---

### 7.4. Integration with Δ12/Δ144

**Current State**: Δ12 not explicitly represented; Δ144 feeds TW369 implicitly

**v2.4 Vision**: Explicit Δ12 ↔ TW369 coupling

#### Proposed Approach

1. **Δ12 → TW369 Regime Mapping**
   - Each archetype defines expected TW369 behavior
   - Schema: `schema/tw369/archetype_regimes.json`
   - Example:
     ```json
     {
       "A07_RULER": {
         "preferred_plane": "6",
         "drift_tolerance": 0.3,
         "painleve_alpha": 0.0
       }
     }
     ```

2. **Δ144 → TW369 Input Refinement**
   - Use Δ144 state to modulate TW369 inputs
   - State profile (EXPANSIVE/CONTRACTIVE/TRANSCENDENT) → plane weights
   - State modifiers → drift sensitivity

3. **TW369 → Δ12 Feedback (Future)**
   - Drift accumulation adjusts Δ12 probabilities
   - High drift in Plane 3 → increase REBEL/CREATOR archetypes
   - Schema for feedback rules: `schema/tw369/feedback_rules.json`

#### Files to Create/Modify (v2.4)
- `schema/tw369/archetype_regimes.json` (NEW)
- `docs/math/DELTA12_AND_DELTA144_RELATION.md` (CREATED)
- `src/tw369/integration.py` (MODIFY - use Δ12 regime)
- `src/archetypes/delta144_engine.py` (MODIFY - expose Δ12)

#### Acceptance Criteria
- [ ] Δ12 regime mapping documented
- [ ] TW369 uses Δ12 to configure behavior
- [ ] Δ144 state modulates TW369 inputs
- [ ] Cross-reference with `DELTA12_AND_DELTA144_RELATION.md`

---

## 8. Future Implementations (v2.5+)

*   **Model E (Topological Drift)**: Modeling drift as a deformation of the state manifold itself, not just a scalar value.
*   **Painlevé Phase Detection**: Automatically triggering "State Metamorphosis" when the Painlevé function crosses zero.
*   **Tensor Persistence**: Storing the full 3x3x3 tensor state history for deep temporal analysis.
*   **Drift Alerting System**: Real-time webhooks when drift exceeds critical thresholds (e.g., > 0.8).

## 9. Enhancements (Short/Medium Term)

*   **Vectorized Operations**: Rewriting the core drift calculation using `numpy` for 100x speedup.
*   **Configurable Noise Profiles**: Allowing different "colors" of noise (Pink, White, Brownian) in Model D.
*   **Adaptive Windowing**: Dynamically sizing the Painlevé filter window based on signal volatility.
*   **Drift Visualization**: Generating SVG plots of the drift trajectory for debugging.

## 10. Research Track (Long Term)

*   **Quantum Tensor Networks**: Exploring the use of tensor networks (MPS/PEPS) to model high-dimensional state interactions.
*   **Chaotic Attractor Mapping**: Identifying if the system settles into strange attractors under certain conditions.
*   **Painlevé VI Integration**: Upgrading from Painlevé II to VI for a more general solution to the deformation equations.
*   **Causal Drift Analysis**: Using causal inference to determine *which* vector caused the drift spike.

## 11. Known Limitations

*   **Scalar Reduction**: The current engine reduces complex tensor interactions to a single scalar "Drift Metric", losing information.
*   **Memoryless (mostly)**: Apart from Model C, the drift calculation is largely stateless (Markovian).
*   **Parameter Sensitivity**: The Painlevé filter is highly sensitive to the `window_size` and `alpha` parameters.
*   **No Feedback Loop**: Currently, drift does not feed back into Kindra to adjust vector sensitivity (open loop).

