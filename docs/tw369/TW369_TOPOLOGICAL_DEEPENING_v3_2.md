# KALDRA v3.2 — TW369 Topological Deepening

## Overview

The TW369 Topological Deepening enhancement elevates the TW369 drift analysis module from a basic scalar drift metric to a complete topological system capable of:

- **Temporal trajectory tracking**: Full history of drift evolution over time
- **Regime transition detection**: Automatic identification of turning points between stability regimes
- **Tracy-Widom severity scoring**: Mathematical rigor from random matrix theory
- **Volatility analysis**: Statistical characterization of drift dynamics
- **Painlevé II smoothing**: Physics-informed noise reduction (with placeholder implementation for future enhancement)

This is a **backend-only Phase 2 enhancement** (designated v3.2) that does not modify:
- API v3.1
- SignalAdapter interfaces
- StoryStage / Temporal Mind components (integration deferred to v3.3+)

---

## Architecture

### Component Hierarchy

```
TW369Integrator (tw369_integration.py)
├── DriftHistory (drift_history.py)
│   └── DriftSample[] (deque, max 512)
├── TW369Topology (drift_topology.py)
│   ├── smooth_with_painleve()
│   ├── compute_tracy_widom_severity()
│   ├── compute_volatility()
│   ├── classify_regime()
│   └── build_drift_context()
└── _latest_drift_context: DriftContext
```

### Integration Point

The topological analysis is integrated into `TW369Integrator.compute_drift()`:

1. **Existing drift computation** proceeds normally (gradients → models → drift values)
2. **New topological layer** (v3.2):
   - Compute Tracy-Widom severity from drift magnitude
   - Classify preliminary regime
   - Add sample to DriftHistory
   - Build complete DriftContext with trajectory & turning points
3. **Graceful degradation**: All topological code wrapped in try-except blocks
4. **Backward compatibility**: Existing DriftState tracking continues unchanged

---

## Data Structures

### DriftPoint

```python
@dataclass
class DriftPoint:
    timestamp: float            # Unix timestamp
    drift_value: float          # Drift metric at this instant
    tracy_widom_severity: float # Severity score [0, 1]
    regime: str                 # "STABLE" | "VOLATILE" | "CRITICAL" | "TRANSITION"
```

### TurningPoint

```python
@dataclass
class TurningPoint:
    timestamp: float       # When transition occurred
    from_regime: str       # Previous regime
    to_regime: str         # New regime
    reason: str            # Why (e.g., "regime_change", "severity_spike")
```

### DriftContext (Extended)

New fields added to existing `DriftContext`:

```python
@dataclass
class DriftContext:
    # Existing fields (v3.1)
    tw_state: Optional[Any]
    drift_state: Optional[DriftState]
    regime: str
    drift_metric: float
    
    # NEW v3.2 Topological fields
    volatility: float = 0.0
    tracy_widom_severity: float = 0.0
    painleve_smoothed: bool = False
    trajectory: List[DriftPoint] = field(default_factory=list)
    turning_points: List[TurningPoint] = field(default_factory=list)
```

**Backward compatibility**: All new fields have default values. Existing code reading `drift_metric` and `regime` works unchanged.

---

## Regime Classification

### Classification Logic

```python
def classify_regime(severity: float, volatility: float) -> str:
    if severity >= 0.95:                    # Critical threshold
        return "CRITICAL"
    elif severity >= 0.85:                  # Severe threshold
        return "VOLATILE"
    elif volatility <= 0.1:                 # Low volatility
        return "STABLE"
    else:
        return "TRANSITION"
```

### Regime Semantics

| Regime | Condition | Interpretation |
|--------|-----------|----------------|
| **STABLE** | Low severity (<0.85) + low volatility (≤0.1) | Normal operating range, predictable drift |
| **VOLATILE** | High severity (0.85-0.95) | Significant drift tension, active dynamics |
| **CRITICAL** | Very high severity (≥0.95) | Extreme drift, potential regime shift imminent |
| **TRANSITION** | Low severity (<0.85) + high volatility (>0.1) | Unstable but not severe, transitional state |

---

## Future Implementations

### Short-Term (v3.3)

1. **Real Painlevé II integration**: Replace placeholder moving average with actual Painlevé filter from `painleve_filter.py`
2. **Real Tracy-Widom CDF**: Integrate `tracy_widom.py` module for rigorous severity computation
3. **StoryStage integration**: Connect drift topology with narrative arc detection
4. **Meta Engine awareness**: Update Nietzsche/Aurelius/Campbell to leverage trajectory data

### Medium-Term (v3.4-v3.5)

1. **Adaptive thresholds**: Learn regime classification thresholds from historical data
2. **Causality tracking**: Extend `TurningPoint.reason` with causal attribution (e.g., "polarity_spike: POL_ORDER_CHAOS")
3. **Drift prediction**: Use trajectory to forecast next N samples
4. **Persistence layer**: Optional disk storage for long-term drift history analysis

---

## Enhancements (Short/Medium Term)

### Performance Optimizations

- **Lazy trajectory construction**: Only build full trajectory when explicitly requested
- **Windowed volatility cache**: Pre-compute volatility for sliding windows
- **Sparse sampling**: Decimate trajectory for long histories (keep all turning points + sparse intermediate samples)

### Calibration & Tuning

- **Domain-specific thresholds**: Different severity/volatility thresholds per application domain (KALDRA-Alpha vs KALDRA-Safeguard)
- **Archetype-aware regimes**: Map regimes to Delta144 states for richer classification
- **Tau-modulated sensitivity**: Let Tau Layer adjust regime sensitivity based on epistemic risk

### Usability & Observability

- **Drift visualization helpers**: Export trajectory as time series for plotting
- **Regime transition logs**: Structured logging of all turning points for debugging
- **Health metrics**: Expose `drift_history.is_empty()`, sample count, volatility stats via monitoring API

---

## Research Track (Long Term)

### Painlevé Transcendents

Current placeholder uses simple moving average. Future research directions:

1. **Painlevé II solutions**: Map drift dynamics to solutions of `u''(x) = 2u³ + xu + α`
2. **Archetype-specific α**: Calibrate Painlevé parameter `α` per Delta144 archetype
3. **Multi-scale Painlevé**: Combine Painlevé smoothing at different temporal scales

### Tracy-Widom Distribution Theory

1. **Calibrated severity mapping**: Empirically validate Tracy-Widom tail probabilities against observed drift extremes
2. **Beta ensemble selection**: Investigate β=1, β=4 ensembles beyond default β=2
3. **Finite-size corrections**: Account for finite embedding dimension effects

### Topological Data Analysis

1. **Persistent homology**: Detect topological features (voids, cycles) in drift trajectory embeddings
2. **Regime phase diagrams**: Map (severity, volatility) space to identify bifurcation boundaries
3. **Causal topology**: Infer causal structure of regime transitions via Granger causality on trajectories

---

## Known Limitations

### v3.2 Implementation Gaps

1. **Placeholder Painlevé smoothing**: Uses 3-point moving average instead of real Painlevé II solver
   - **Impact**: Limited noise reduction, no physics-informed dynamics
   - **Mitigation**: Documented as TODO; future integration straightforward

2. **Logistic approximation for Tracy-Widom**: Falls back to `1 / (1 + exp(-z))` if real TW unavailable
   - **Impact**: Severity scores less rigorous, may not match true TW tail probabilities
   - **Mitigation**: Real TW module exists (`tracy_widom.py`), integration planned for v3.3

3. **Fixed regime thresholds**: Hardcoded `0.85`, `0.95`, `0.1` for all contexts
   - **Impact**: May misclassify regimes in domains with different drift characteristics
   - **Mitigation**: Thresholds configurable via constructor; adaptive calibration in v3.4

4. **In-memory only**: No persistence to disk
   - **Impact**: Drift history lost on process restart
   - **Mitigation**: Deque-based storage efficient up to 512 samples; disk persistence deferred to avoid complexity

5. **No causality attribution**: Turning points don't track which factors triggered transition
   - **Impact**: Difficult to diagnose why regime changed
   - **Mitigation**: Manual inspection of plane tensions + polarity scores; causal tracking in v3.4

### Scope Exclusions (Intentional)

1. **No SignalAdapter exposure**: Topological data not yet surfaced via API
   - **Rationale**: Backend stabilization first; API design for v3.3
2. **No StoryStage integration**: Drift topology disconnected from narrative analysis
   - **Rationale**: Story Engine components (v3.2 Phase 1) must mature first
3. **No Tau Layer awareness**: Regime classification doesn't account for epistemic risk
   - **Rationale**: Deferred to multi-layer integration in v3.5+

---

## Testing

### Test Suite

**File**: `tests/tw369/test_tw369_topology.py`

**Coverage** (20 tests, 100% passing):

- **Painlevé smoothing** (3 tests): variance reduction, empty handling, length preservation
- **Tracy-Widom severity** (3 tests): monotonicity, bounds [0,1], zero-std edge case
- **Volatility** (3 tests): constant series → 0, variance correlation, empty/single handling
- **Regime classification** (4 tests): STABLE, VOLATILE, CRITICAL, TRANSITION conditions
- **DriftContext building** (4 tests): trajectory construction, turning point detection, empty history, field population
- **DriftHistory** (3 tests): sample storage, max-length enforcement, emptiness check

**Run**:
```bash
pytest tests/tw369/test_tw369_topology.py -v
```

### Backward Compatibility Verification

**Tested suites**:
- `tests/tw369/test_drift_memory.py` (5 tests) ✅
- `tests/tw369/test_archetype_regimes.py` (6 tests) ✅
- `tests/tw369/test_tw369_modulation.py` (4 tests) ✅

**Result**: 15/15 existing TW369 tests pass without modification.

**Confirmed**: No breakage in drift memory, archetype regime mapping, or plane modulation.

---

## Next Steps

### Immediate (Post-v3.2 Deployment)

1. **Real-world calibration**: Deploy to KALDRA-Alpha staging, collect drift samples, tune thresholds
2. **Performance profiling**: Measure overhead of topological analysis in production workloads
3. **Tracy-Widom integration**: Replace logistic fallback with `severity_from_index()` from `tracy_widom.py`

### v3.3 Roadmap

1. **SignalAdapter extension**: Expose `trajectory` and `turning_points` via new API endpoints
2. **StoryStage connection**: Use drift topology to enrich narrative arc detection
3. **Meta Engine updates**: Pass `DriftContext` to Nietzsche/Aurelius/Campbell for deeper analysis
4. **Painlevé filter activation**: Integrate `painleve_filter.py` into `smooth_with_painleve()`

### v3.4+ Vision

1. **Adaptive regime thresholds**: Learn from historical data using online optimization
2. **Causality tracking**: Extend `TurningPoint` with causal factors (polarity spikes, archetype shifts)
3. **Multi-scale analysis**: Hierarchical drift analysis (micro/meso/macro timescales)
4. **Predictive drift**: Forecast future drift trajectory using topological features

---

## Acknowledgments

This enhancement builds upon:
- **TW369 v2.4**: Tracy-Widom module and Painlevé II solver foundations
- **Drift Memory design**: Deque-based storage pattern from existing `DriftMemory` class
- **Unification Layer v3.1**: DriftContext integration point

Mathematical foundations:
- Tracy-Widom distribution (random matrix theory)
- Painlevé transcendents (integrable systems)
- Topological data analysis (persistent homology, in future work)
