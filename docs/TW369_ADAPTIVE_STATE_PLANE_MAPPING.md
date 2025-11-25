# TW369 — Adaptive State-Plane Mapping

## 1. Purpose

This document describes the **adaptive state-plane mapping** mechanism for TW369.

The goal is to:
- Preserve the original TW369 math (Model A).
- Keep the static primary assignment:
  - Layer 1 → Plane 3 (Cultural / Surface)
  - Layer 2 → Plane 6 (Semiotic / Tension)
  - Layer 3 → Plane 9 (Structural / Deep)
- Add a **context-aware weighting layer** over planes 3, 6, 9:
  - Plane weights: w3, w6, w9
  - Always in [0,1] and w3 + w6 + w9 = 1
  - Used to reweight plane contributions in downstream calculations.

## 2. Core Types

Implemented in:
- `src/tw369/state_plane_mapping.py`
- `src/tw369/state_plane_mapping_utils.py`

### AdaptiveMappingContext

Fields:
- `domain`: `"ALPHA" | "GEO" | "PRODUCT" | "SAFEGUARD" | "DEFAULT"`
- `severity`: TW369 severity factor in [0,1]
- `instability_index`: any non-negative float
- `time_horizon`: `"short" | "medium" | "long"`
- `narrative_type`: optional label (`"crisis"`, `"optimistic"`, etc.)
- `country`, `sector`: optional hints

### PlaneWeights

Normalized weights:
- `plane3`, `plane6`, `plane9`
- in [0,1] with sum = 1.0

### PlaneMappingResult

Fields:
- `layer_primary_plane`: `{1: 3, 2: 6, 3: 9}`
- `plane_weights`: `PlaneWeights`
- `metadata`: explanation of the decision (severity class, baseline, shift_factor…)

## 3. Config Schema

Schemas:
- `schema/tw369/state_plane_mapping_config.json`
- `schema/tw369/state_plane_mapping_default.json`

Key parameters:
- `domains[DOMAIN].plane3/plane6/plane9`: baseline weights per domain
- `severity_thresholds.low/medium/high`: boundaries for piecewise behaviour
- `max_shift`: upper bound for how much weight can be shifted as severity grows

## 4. Rules (Domain-Specific Behaviour)

### ALPHA (Markets)
- Baseline: strong emphasis on plane 3 (surface) + 6 (tension).
- High severity:
  - plane 3 loses weight
  - plane 6 and 9 gain weight (tension + structural risk)

### GEO (Geopolitics)
- Baseline: deep weight on plane 9 (structural).
- Medium/High severity or long horizon:
  - more weight flows from plane 3/6 to plane 9.

### PRODUCT (UX / Brand / Experience)
- Baseline: surface + semiotic (planes 3 and 6).
- Short horizon + medium/high severity:
  - weight flows from 9 → 3/6 (experience + discourse).

### SAFEGUARD (Risk / Governance)
- Baseline: balanced 3/6/9 with structural bias.
- High severity or explicit crisis:
  - weight moves from 3 → 6/9 (risk + deep structure).

### DEFAULT
- Baseline: mild emphasis on 3/6.
- High severity:
  - modest shift from 3 → 6.

## 5. How to Use

### 5.1. Compute Mapping

```python
from src.tw369.state_plane_mapping import AdaptiveStatePlaneMapper, AdaptiveMappingContext
import json

with open("schema/tw369/state_plane_mapping_default.json") as f:
    cfg = json.load(f)

mapper = AdaptiveStatePlaneMapper(cfg)

ctx = AdaptiveMappingContext(
    domain="ALPHA",
    severity=0.85,
    instability_index=1.2,
    time_horizon="short",
    narrative_type="crisis",
    country="BR",
    sector="energy",
)

result = mapper.infer_mapping(ctx)
weights = result.plane_weights  # w3, w6, w9
```

### 5.2. Apply to Plane Tensions

```python
from src.tw369.state_plane_mapping_utils import apply_plane_weights_to_tensions

raw_tensions = {3: t3, 6: t6, 9: t9}
weighted_tensions = apply_plane_weights_to_tensions(raw_tensions, result)
```

The TW369 engine can keep using its math with either:
- raw plane tensions, or
- weighted tensions, depending on configuration.

## 6. Examples

### Example 1: ALPHA Domain, High Severity

```python
ctx = AdaptiveMappingContext(
    domain="ALPHA",
    severity=0.9,
    time_horizon="short",
    narrative_type="crisis"
)

result = mapper.infer_mapping(ctx)
# Expected: plane3 reduced, plane6 and plane9 increased
```

### Example 2: GEO Domain, Long Horizon

```python
ctx = AdaptiveMappingContext(
    domain="GEO",
    severity=0.6,
    time_horizon="long"
)

result = mapper.infer_mapping(ctx)
# Expected: plane9 significantly increased (structural focus)
```

### Example 3: PRODUCT Domain, Short Horizon

```python
ctx = AdaptiveMappingContext(
    domain="PRODUCT",
    severity=0.5,
    time_horizon="short"
)

result = mapper.infer_mapping(ctx)
# Expected: plane3 and plane6 emphasized (surface + semiotic)
```

## 7. Testing

Run the test suite:

```bash
pytest tests/core/test_state_plane_mapping.py -v
```

Tests verify:
- Weights always sum to 1.0
- Domain-specific rules work correctly
- Metadata is properly populated
- Utility functions scale tensions correctly

## 8. Future Work

- True dynamic reassignment of `layer_primary_plane` (e.g. L2 partially feeding plane 9 under extreme conditions).
- Learning the mapping from data (research track).
- Plugging this into TW369 severity and drift calculations as an optional module.
- Adding more sophisticated shift functions (non-linear, multi-factor).
- Integration with real-world context extraction from narrative text.

## 9. Integration with TW369

This module is **standalone** and does not modify TW369 core math. To integrate:

1. Compute adaptive mapping before calling TW369
2. Use the plane weights to:
   - Reweight plane tensions
   - Adjust severity calculations
   - Modulate drift factors
3. Pass weighted values to TW369 pipeline

Example integration pattern:

```python
# 1. Get context
ctx = extract_context_from_narrative(text)

# 2. Compute adaptive mapping
mapping = mapper.infer_mapping(ctx)

# 3. Compute TW369 state
tw_state = create_tw_state(kindra_scores)

# 4. Get plane tensions
tensions = compute_plane_tensions(tw_state)

# 5. Apply weights
weighted_tensions = apply_plane_weights_to_tensions(tensions, mapping)

# 6. Use in drift calculation (optional)
drift = compute_drift_with_weighted_tensions(weighted_tensions)
```

## 10. Configuration

Default configuration provides sensible baselines for each domain. To customize:

1. Copy `state_plane_mapping_default.json`
2. Adjust domain baselines
3. Tune severity thresholds
4. Modify max_shift parameter
5. Load custom config in mapper initialization

## 11. Validation

The system ensures:
- All weights are non-negative
- Weights always sum to 1.0 (normalized)
- Shift factors respect max_shift bounds
- Domain baselines are valid
- Severity classification is consistent

## 12. Metadata

Each mapping result includes rich metadata:
- Input context (domain, severity, horizon, etc.)
- Severity classification (low/medium/high/extreme)
- Shift factor applied
- Baseline weights before adaptation
- Final weights after adaptation

This enables full explainability and debugging of the mapping decisions.
