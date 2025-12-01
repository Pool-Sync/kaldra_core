# Polarities & Modifiers — v2.7 Specification

**Version**: 2.7.0  
**Codename**: Axes & Masks  
**Status**: Implementation Spec  
**Date**: 2025-11-28

---

## Overview

KALDRA v2.7 activates **Polarities** (46 macro tensions) and **Modifiers** (59 state masks) as first-class intelligence layers across the entire pipeline.

### What Are Polarities?

**Polarities** are fundamental dimensional tensions that structure experience:
- **Examples**: LIGHT ↔ SHADOW, ORDER ↔ CHAOS, EXPANSION ↔ CONTRACTION
- **Dimensions**: 9 categories (existential, structure, energy, cognition, affect, etc.)
- **Total**: 46 polarities defined in `schema/archetypes/polarities.json`

**Role**: Macro-level tensions that modulate archetype probabilities, TW369 severity, and narrative dynamics.

### What Are Modifiers?

**Modifiers** are state masks that qualify how an archetype manifests:
- **Examples**: WOUNDED, SHADOW, RADIANT, CYNICAL, TRANSCENDENT
- **Categories**: 6 groups (wound/shadow, expansion, contraction, collective, mental, transcendence)
- **Total**: 59 modifiers defined in `schema/archetypes/archetype_modifiers.json`

**Role**: Fine-grained qualifiers that add nuance to Δ144 states (e.g., "WARRIOR" + "WOUNDED" vs "WARRIOR" + "RADIANT").

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  KALDRA v2.7 Pipeline                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Input Text                                              │
│      │                                                   │
│      ├──▶ Embeddings (v2.3) ──▶ Modifier Scores        │
│      │                                                   │
│      ├──▶ Meta-Engines (v2.5) ──▶ Polarity Scores      │
│      │        │                                          │
│      │        ├─ Nietzsche 12-axis                      │
│      │        ├─ Aurelius 12-axis                       │
│      │        └─ Campbell 12-stage                      │
│      │                                                   │
│      ▼                                                   │
│  ┌──────────────┐         ┌──────────────┐             │
│  │ Δ144 Engine  │◀────────│ Polarities   │             │
│  │ + Modifiers  │         │ (46 tensions)│             │
│  └──────────────┘         └──────────────┘             │
│      │                                                   │
│      ├──▶ Δ12 Vector ──▶ Polarity Modulation           │
│      │                                                   │
│      └──▶ TW369 ──▶ Polarity Severity Adjustment       │
│                                                          │
│  Story Engine (v2.6)                                     │
│      └──▶ Polarity Oscillation Detection                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Integration Points

### 1. Δ144 State Inference

**Current (v2.6)**:
- Modifiers are loaded but require manual `modifier_scores` input
- Polarities are not used

**v2.7 Enhancement**:
- ✅ **Auto-infer modifier scores** from embeddings (cosine similarity)
- ✅ **Load polarities** as first-class objects
- ✅ Modifiers respect `state.default_modifiers` and `allowed_modifiers`

**Result**: `Delta144Result.active_modifiers` populated automatically.

### 2. Δ12 Projection

**Current (v2.6)**:
- Δ12 computed purely from Δ144 state probabilities
- No polarity influence

**v2.7 Enhancement**:
- ✅ **Polarity modulation** of archetype probabilities
- ✅ Example: High `POL_EXPANSION_CONTRACTION` (expansion) boosts WARRIOR/RULER
- ✅ Bounded, normalized adjustments (sum = 1.0)
- ✅ Behind feature flag (default: OFF)

**Function**: `apply_polarities_to_delta12()`

### 3. TW369 Drift & Severity

**Current (v2.6)**:
- TW369 severity computed from Tracy-Widom statistics
- Polarities have `tw_alignment` fields but unused

**v2.7 Enhancement**:
- ✅ **Polarity-based severity modulation**
- ✅ Uses `tw_alignment` from polarities.json (planes 3/6/9)
- ✅ Bounded changes (+/- 10-20%)
- ✅ Behind feature flag `KALDRA_TW_POLARITY_ENABLED` (default: OFF)

**Function**: `modulate_tw_severity_with_polarities()`

### 4. Meta-Engines (Nietzsche/Aurelius/Campbell)

**Current (v2.5)**:
- Meta-engines output 12-axis scores
- No connection to polarities

**v2.7 Enhancement**:
- ✅ **Extract polarity scores** from meta-engine outputs
- ✅ Mappings:
  - Nietzsche `will_to_power` → `POL_DOMINANCE_SERVICE`
  - Aurelius `serenity` → `POL_CALM_ANXIETY`
  - Campbell stages → `POL_CALL_REFUSAL`, `POL_DESCENT_ASCENT`
- ✅ Non-breaking: adds optional `polarity_scores` field

**Function**: `extract_polarity_scores()`

### 5. Story Engine (v2.6)

**Current (v2.6)**:
- StoryEvent tracks delta12, meta_scores, drift_state
- No polarity or modifier tracking

**v2.7 Enhancement**:
- ✅ **StoryEvent.polarity_scores** field
- ✅ **StoryEvent.active_modifiers** field
- ✅ **Polarity oscillation detection** (e.g., HOPE → DESPAIR → HOPE)
- ✅ Extended StorySignal schema

**Functions**: `detect_polarity_oscillations()`, `PolaritySwing` dataclass

### 6. Kindra (Optional)

**Current (v2.6)**:
- Kindra L1/L2/L3 independent
- No polarity/modifier awareness

**v2.7 Enhancement** (Light hooks only):
- ⚠️ **Optional hooks** for L1 (cultural polarities) and L2 (media modifiers)
- ⚠️ Can be left as TODOs if time-constrained
- ⚠️ No large refactor required

**Functions**: `adjust_l1_with_polarities()`, `adjust_l2_with_modifiers()`

---

## Must-Have vs Optional

### ✅ Must-Have (Core v2.7)

1. **Polarity loading** - `load_polarities()`, Polarity dataclass
2. **Modifier auto-inference** - Embedding-based scoring
3. **Polarity extraction** - From meta-engines
4. **Δ12 modulation** - Polarity-aware adjustment
5. **TW369 modulation** - Polarity-aware severity
6. **Story integration** - Polarity/modifier tracking
7. **Tests** - 5 new test files
8. **Docs** - Spec, release notes, roadmap update

### ⚠️ Optional (Can Defer)

1. **Kindra hooks** - L1/L2 integration (can be TODOs)
2. **Advanced polarity config** - JSON-based mapping rules (can use hardcoded for v2.7)
3. **Polarity visualization** - Temporal polarity charts (v2.8+)

---

## Configuration Flags

### New Environment Variables

```bash
# TW369 polarity modulation (default: false)
KALDRA_TW_POLARITY_ENABLED=true

# Δ12 polarity modulation (default: false)
KALDRA_DELTA12_POLARITY_ENABLED=true
```

### Behavior

- **Flags OFF** (default): v2.7 behaves like v2.6 (100% backward compatible)
- **Flags ON**: Polarity modulation active

---

## Data Flow Example

### Input
```
Text: "I feel wounded but ready to rise again."
```

### v2.7 Pipeline

1. **Embeddings** (v2.3):
   - Generate semantic vector
   - Compute modifier scores via cosine similarity:
     - `MOD_WOUNDED`: 0.82
     - `MOD_REBORN`: 0.71

2. **Meta-Engines** (v2.5):
   - Nietzsche: `will_to_power`: 0.65, `amor_fati`: 0.58
   - Aurelius: `serenity`: 0.42, `emotional_regulation`: 0.51
   - Campbell: stage = "ordeal"

3. **Polarity Extraction**:
   - `POL_DOMINANCE_SERVICE`: 0.65 (from will_to_power)
   - `POL_CALM_ANXIETY`: 0.42 (from serenity, inverted)
   - `POL_DESCENT_ASCENT`: 0.75 (from ordeal stage)

4. **Δ144 Inference**:
   - Base state: `A03_WARRIOR_3_06`
   - Active modifiers: `[MOD_WOUNDED, MOD_REBORN]`

5. **Δ12 Modulation** (if flag ON):
   - Base: `{A03_WARRIOR: 0.65, A05_SEEKER: 0.25, A10_SAGE: 0.10}`
   - After polarity adjustment: `{A03_WARRIOR: 0.70, A05_SEEKER: 0.22, A10_SAGE: 0.08}`

6. **TW369 Modulation** (if flag ON):
   - Base severity: 0.58
   - After polarity adjustment: 0.62 (boosted by high DESCENT_ASCENT on plane 6)

7. **Story Tracking**:
   - StoryEvent stores:
     - `polarity_scores`: `{POL_DESCENT_ASCENT: 0.75, ...}`
     - `active_modifiers`: `["MOD_WOUNDED", "MOD_REBORN"]`

---

## Backward Compatibility

### Guarantees

1. **All v2.3-v2.6 tests pass** without modification
2. **Default behavior unchanged** (flags OFF)
3. **Optional fields only** - no required schema changes
4. **Additive modulation** - never replaces base calculations
5. **Safe fallbacks** - missing polarities/modifiers → graceful degradation

### Migration Path

- **v2.6 → v2.7**: Zero code changes required
- **To enable v2.7 features**: Set environment flags
- **To use polarities**: Call new functions explicitly (opt-in)

---

## Performance Impact

- **Polarity loading**: One-time at engine init (~1ms)
- **Modifier inference**: Per-request embedding similarity (~2-5ms)
- **Polarity extraction**: Per-request meta-engine mapping (~1ms)
- **Modulation**: Negligible (<1ms)

**Total overhead**: ~5-10ms per request (when enabled)

---

## Future Enhancements (v2.8+)

- **Polarity config externalization** - JSON-based mapping rules
- **Temporal polarity visualization** - Charts of polarity swings
- **Multi-dimensional polarity analysis** - Polarity clusters
- **Polarity-aware routing** - App selection based on polarities
- **Full Kindra integration** - L1/L2/L3 polarity/modifier awareness

---

**KALDRA v2.7 - Axes & Masks Specification** 🎭
