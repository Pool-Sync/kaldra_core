# Kindra Learned Weights Specification v3.5

**Status:** ✅ IMPLEMENTED  
**Version:** v3.5 Phase 2

---

## Overview

Kindra weights control the importance of each Kindra (from 3×48 vector) per domain in the learned mapping.

---

## Weight Structure

### Config Format

```json
{
  "domain_weights": {
    "alpha": {
      "kindra_001": 0.8,
      "kindra_002": 0.5,
      ...
    },
    "geo": {
      "kindra_001": 0.3,
      "kindra_045": 0.9,
      ...
    },
    ...
  }
}
```

### Weight Semantics

- **Range:** [0, 1] typical, but not enforced
- **Meaning:** Importance/contribution of Kindra in domain
- **Default:** 0.5 if not specified

---

## Domain Mapping

KALDRA supports 4 primary domains:

1. **alpha**: General narrative signals
2. **geo**: Geopolitical signals
3. **product**: Product/market signals
4. **safeguard**: Security/risk signals

Each domain can have different weight vectors for the same Kindras.

---

## Update Policy (Phase 2)

### Current: Offline Only

Weights are **static** in Phase 2:
- Loaded from config at initialization
- No automatic updates
- Manual curation required

### Stub: `update_from_observations()`

Method exists but does nothing in Phase 2:
```python
def update_from_observations(self, observations):
    # Phase 2: No-op
    # Future (v3.6+): Implement learning
    pass
```

---

## Usage

```python
from src.learning.kindra_weights_engine import KindraWeightsEngine

# Load config config = {"domain_weights": {...}}
engine = KindraWeightsEngine(config)

# Get weights for domain
weights = engine.get_weights("alpha")
print(weights.weights)  # Dict[str, float]

# Get weight for specific Kindra
w = weights.weights.get("kindra_001", 0.5)
```

---

## Future Work (v3.6+)

### Planned Learning Strategies

1. **Regression-Based:**
   - Train weights to predict Delta144 from Kindra
   - Use historical signal data

2. **Ranking-Based:**
   - Learn weights that rank correct state higher
   - Pairwise or listwise ranking loss

3. **Multi-Task:**
   - Share weights across domains
   - Domain-specific fine-tuning

4. **Personalization:**
   - User/org-specific weight adjustments
   - Contextual bandits

---

## Validation

### Tests

- Load from config
- Get weights for known domain
- Handle unknown domain (empty dict)
- Update stub doesn't crash

### Constraints

- Weights should be positive (recommended)
- Sum not required to be 1.0 (not probabilities)
- Missing Kindra defaults to 0.5

---

## Related

- [Kindra Priors](file:///Users/niki/Desktop/kaldra_core/docs/learning/DELTA144_LEARNED_MAPPING_SPEC_v3_5.md)
- [Future Work](file:///Users/niki/Desktop/kaldra_core/docs/learning/LEARNED_MAPPINGS_v3_6_FUTURE_WORK.md)
