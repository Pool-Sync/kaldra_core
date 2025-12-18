# Delta144 Learned Mapping Specification v3.5

**Status:** ✅ IMPLEMENTED  
**Version:** v3.5 Phase 2

---

## Overview

This document specifies the heuristic scoring algorithm for Kindra→Δ144 learned mappings.

---

## Scoring Formula

For each candidate Delta144 state, compute score:

```
score[state] = W_base × P_base[state]
             + Σ(k∈Kindra) S_k × W_k[domain] × P_k→state
             + λ × I(state = current_state)
```

**Where:**
- `W_base`: Base prior weight (default: 0.1)
- `P_base[state]`: Uniform base probability
- `S_k`: Kindra score for kindra k
- `W_k[domain]`: Learned weight for kindra k in domain
- `P_k→state`: Prior probability kindra k → state
- `λ`: Current state boost (default: 0.2)
- `I(·)`: Indicator function

---

## Normalization

After computing raw scores, normalize to probability distribution:

```
P[state] = score[state] / Σ(s) score[s]
```

**Edge case:** If all scores are 0, use uniform distribution.

---

## Confidence Computation

Confidence based on distribution entropy and feature richness:

### Entropy-Based Clarity

```
H = -Σ(s) P[s] × log(P[s])
H_max = log(|states|)
clarity = 1 - (H / H_max)
```

Lower entropy → higher clarity → higher confidence.

### Feature Richness

```
richness = min(|Kindra_scores| / 10, 1.0)
```

More Kindra features → higher richness.

### Combined Confidence

```
confidence = 0.7 × clarity + 0.3 × richness
```

Clamped to [0, 1].

---

## Examples

### Example 1: Clear Winner

**Kindra scores:** `{"k1": 1.0}`  
**Priors:** `k1 → threshold: 0.9, emergence: 0.1`  
**Weights:** `k1[alpha]: 1.0`

**Result:**
- `threshold` dominates distribution
- High clarity
- `confidence ≈ 0.5-0.7`

### Example 2: Ambiguous

**Kindra scores:** `{"k1": 0.5, "k2": 0.5}`  
**Priors:** `k1 → {threshold: 0.5, emergence: 0.5}, k2 → {threshold: 0.5, emergence: 0.5}`

**Result:**
- Uniform distribution
- Low clarity
- `confidence ≈ 0.1-0.3`

---

## Edge Cases

### No Kindra Scores
- Use uniform distribution over all states
- Low confidence (~0-0.1)

### Current State Boost
- Adds `λ` to current state score
- Helps hybrid mode stay stable

### Unknown Kindra
- Weight defaults to 0.5
- Prior defaults to empty dict (no contribution)

---

## Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `base_prior_weight` | 0.1 | Base score for all states |
| `current_state_boost` | 0.2 | Boost for current state |
| `global_weight` | 0.3 | Overall learned weight |

---

## Implementation

See [delta144_mapping_engine.py](file:///Users/niki/Desktop/kaldra_core/src/learning/delta144_mapping_engine.py)
