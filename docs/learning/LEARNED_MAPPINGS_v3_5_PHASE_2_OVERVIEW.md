# KALDRA Learned Mappings v3.5 Phase 2 - Overview

**Status:** ✅ IMPLEMENTED  
**Version:** v3.5 Phase 2  
**Date:** December 2025  
**Codename:** "The Learning Layer — Mappings"

---

## Executive Summary

Phase 2 transforms KALDRA from **fixed Kindra→Δ144 mappings** to **learned mappings** with domain-specific adjustments, while maintaining 100% backward compatibility.

**Key Innovation:** Heuristic-based learned scoring that combines:
- Kindra priors (base mappings)
- Domain-specific weights
- Current context features

---

## Architecture

```
UnifiedContext
    ↓
LearningFeatureVector
    ├─ Delta144 state
    ├─ Kindra scores (3×48)
    ├─ Delta12 scores
    ├─ Polarities
    ├─ TW369 regime
    └─ Story coherence
    ↓
Delta144MappingEngine
    ├─ KindraPriors (base mappings)
    ├─ KindraWeightsEngine (domain weights)
    └─ Config (modes)
    ↓
Delta144MappingResult
    ├─ suggested_state_id
    ├─ state_distribution
    └─ confidence
```

---

## Components

### 1. Feature Builder

**Module:** `src/learning/features/feature_builder.py`

Extracts features from `UnifiedContext`:
- Delta144 current state
- Kindra scores
- Archetypes (Delta12)
- Polarities
- TW369 regime
- Story coherence

### 2. Mapping Engine

**Module:** `src/learning/delta144_mapping_engine.py`

**Scoring Formula:**
```
score[state] = base_prior 
             + Σ(kindra_score × kindra_weight × prior[kindra→state])
             + λ × indicator(state == current_state)
```

**Confidence:**
- Entropy-based distribution clarity
- Feature richness bonus
- Combined: `0.7 × clarity + 0.3 × richness`

### 3. Priors & Weights

**Priors:** Kindra→Δ144 base mappings  
**Weights:** Domain-specific Kindra importance

---

## Configuration Modes

### Fixed Mode (Default)
Current behavior preserved. No learned mapping applied.

### Hybrid Mode
Combines base Delta144 logic with learned suggestions.

### Learned-Only Mode
Uses learned mapping as primary decision.

**Config:** `configs/learning/delta144_mapping.config.json`

---

## Usage

```python
from src.learning.features.feature_builder import build_from_unified_context
from src.learning.delta144_mapping_engine import Delta144MappingEngine
from src.learning.kindra_priors import KindraPriors
from src.learning.kindra_weights_engine import KindraWeightsEngine

# Setup
priors = KindraPriors.from_config("configs/learning/kindra_priors.config.json")
weights_engine = KindraWeightsEngine(config)
mapping_engine = Delta144MappingEngine(config, priors, weights_engine)

# Extract features
features = build_from_unified_context(unified_context, domain="alpha")

# Get suggestion
result = mapping_engine.suggest(features)
print(f"Suggested: {result.suggested_state_id}")
print(f"Confidence: {result.confidence:.2f}")
```

---

## Testing

**18 tests, all passing:**
- Feature Builder: 3 tests
- Mapping Engine: 5 tests
- Priors: 3 tests
- Weights: 3 tests
- Integration: 4 tests

---

## Backward Compatibility

✅ **Zero Breaking Changes:**
- Default mode: `fixed`
- Delta144 engine unchanged
- No API modifications
- Optional opt-in per domain

---

## Limitations

- **Heuristic-based:** Not ML/statistical
- **Offline only:** No online learning in Phase 2
- **Seed data:** Priors/weights need population
- **Backend-only:** Not exposed via API

---

## Future Work (v3.6+)

See [LEARNED_MAPPINGS_v3_6_FUTURE_WORK.md](file:///Users/niki/Desktop/kaldra_core/docs/learning/LEARNED_MAPPINGS_v3_6_FUTURE_WORK.md)

---

## Related Documentation

- [Delta144 Mapping Spec](file:///Users/niki/Desktop/kaldra_core/docs/learning/DELTA144_LEARNED_MAPPING_SPEC_v3_5.md)
- [Kindra Weights Spec](file:///Users/niki/Desktop/kaldra_core/docs/learning/KINDRA_LEARNED_WEIGHTS_SPEC_v3_5.md)
