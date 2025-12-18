# KALDRA v2.5 — Meta-Engine Soul & Routing

**Release Date**: November 28, 2025  
**Version**: 2.5.0  
**Codename**: Meta-Engine Soul

---

## Overview

KALDRA v2.5 introduces deep philosophical meta-analysis through three sophisticated engines that analyze text and signals through Nietzschean, Stoic, and Campbellian lenses. This release transforms meta-analysis from simple heuristics to rich, multi-dimensional philosophical frameworks.

### Key Achievements

- ✅ **NietzscheEngine-12** - 12-dimensional Nietzschean analysis
- ✅ **AureliusEngine-12** - 12-dimensional Stoic analysis  
- ✅ **CampbellEngine** - 12-stage Hero's Journey detection
- ✅ **MetaRouter** - Intelligent routing based on philosophical profiles
- ✅ **100% Backward Compatible** - All features optional

---

## What's New

### 1. NietzscheEngine-12

**12 Philosophical Axes**:
1. `will_to_power` - Drive for dominance, creation, self-overcoming
2. `resentment` - Envy, victimization, reactive negativity
3. `life_affirmation` - Positive embrace of existence
4. `life_negation` - Rejection, exhaustion, world-weariness
5. `free_spirit` - Independence from tradition
6. `active_nihilism` - Creative destruction
7. `passive_nihilism` - Despair, apathy
8. `eternal_return_acceptance` - Radical acceptance of fate
9. `transvaluation` - Inversion of traditional values
10. `dionysian_force` - Chaos, excess, primal energy
11. `apollonian_order` - Form, harmony, rational structure
12. `amor_fati` - Loving acceptance of what is

**Usage**:
```python
from meta.nietzsche import analyze_meta

result = analyze_meta("We must overcome and dominate our challenges!")
# result.scores = {"will_to_power": 0.82, "dionysian_force": 0.61, ...}
# result.dominant_axes = [("will_to_power", 0.82), ...]
```

### 2. AureliusEngine-12

**12 Stoic Axes**:
1. `perception_clarity` - Clear, undistorted perception
2. `assent_to_reality` - Acceptance of facts as they are
3. `right_action` - Focus on duty, responsibility
4. `discipline_of_will` - Consistency, self-control
5. `emotional_regulation` - Low reactivity, measured response
6. `fate_acceptance` - Acceptance of the uncontrollable
7. `control_dichotomy` - Distinguishing controllable/uncontrollable
8. `premeditatio_malorum` - Anticipation of difficulties
9. `desire_restraint` - Moderation, absence of excess
10. `character_integrity` - Concern with honor, values
11. `self_mastery` - Internal dominion
12. `serenity` - Calm tone, absence of catastrophizing

**Usage**:
```python
from meta.aurelius import analyze_meta

result = analyze_meta("I accept what I cannot control with calm discipline.")
# result.scores = {"serenity": 0.74, "control_dichotomy": 0.81, ...}
# result.severity = 0.68  # Overall Stoic alignment
```

### 3. CampbellEngine - Hero's Journey

**12 Canonical Stages**:
1. Ordinary World
2. Call to Adventure
3. Refusal of the Call
4. Meeting with the Mentor
5. Crossing the Threshold
6. Tests, Allies, Enemies
7. Approach to the Cave
8. **Ordeal** (crisis peak)
9. Reward
10. Road Back
11. Resurrection
12. Return with Elixir

Maps drift patterns, archetype transitions, and coherence to detect narrative stage.

### 4. MetaRouter

Orchestrates all three engines and produces intelligent routing decisions:

```python
from meta import MetaRouter

router = MetaRouter()
meta_signals = router.evaluate(kaldra_signal)
routing = router.decide_route(meta_signals)

# routing.dominant_app = "safeguard"  # if in Ordeal stage
# routing.reasoning = "Hero's Journey stage 'ordeal' indicates crisis"
```

### 5. Integration Functions

**Meta → Δ12 Integration**:
```python
from archetypes.delta12_vector import apply_meta_to_delta12

adjusted_delta12 = apply_meta_to_delta12(
    delta12,
    nietzsche_scores={"will_to_power": 0.8, "dionysian_force": 0.6},
    aurelius_scores={"serenity": 0.7, "discipline_of_will": 0.65}
)
```

**Meta → TW369 Integration**:
```python
from tw369.regime_utils import adjust_tw_regime_with_meta

adjusted_regime = adjust_tw_regime_with_meta(
    regime_config,
    nietzsche_scores={"active_nihilism": 0.8},
    aurelius_scores={"serenity": 0.75}
)
```

Both functions:
- Are **optional** (if meta scores = None, no adjustment)
- Make **small perturbations** (epsilon = 0.1 max)
- **Re-normalize** to maintain valid distributions
- Are **non-breaking** (backward compatible)

---

## Example Output

```json
{
  "meta": {
    "nietzsche": {
      "will_to_power": 0.82,
      "active_nihilism": 0.61,
      "dionysian_force": 0.54,
      "amor_fati": 0.12
    },
    "aurelius": {
      "perception_clarity": 0.74,
      "control_dichotomy": 0.81,
      "emotional_regulation": 0.45,
      "serenity": 0.29
    },
    "campbell": {
      "stage": "approach_to_cave",
      "confidence": 0.72
    }
  },
  "routing": {
    "dominant_app": "safeguard",
    "confidence": 0.72,
    "reasoning": "Approaching crisis stage with moderate regulation"
  }
}
```

---

## Migration Guide

### For Existing Users

**No action required**. v2.5 is fully backward compatible.

### To Use New Meta-Engines

```python
# Nietzsche analysis
from meta.nietzsche import analyze_meta as analyze_nietzsche
nietzsche_result = analyze_nietzsche(text)

# Aurelius analysis  
from meta.aurelius import analyze_meta as analyze_aurelius
aurelius_result = analyze_aurelius(text)

# Campbell (class-based)
from meta.campbell import CampbellEngine
campbell = CampbellEngine()
campbell_result = campbell.run(kaldra_signal)
```

---

## Configuration

### Feature Flag

Meta-routing is **disabled by default** and can be enabled via environment variable:

```bash
export KALDRA_META_ROUTING_ENABLED=true
```

Or in `.env`:
```
KALDRA_META_ROUTING_ENABLED=true
```

When disabled (default), KALDRA behaves identically to v2.4.

### Integration Parameters

**apply_meta_to_delta12()**:
- `epsilon`: Maximum adjustment magnitude (default: 0.1)
- Adjustments are proportional to meta-scores
- Re-normalization ensures valid probability distribution

**adjust_tw_regime_with_meta()**:
- `noise_scale`: Clamped to [0.1, 2.0]
- `drift_tolerance`: Clamped to [0.1, 1.0]
- `preferred_plane`: "3", "6", or "9"

---

## Technical Details

### Architecture

- **Function-based interface** for Nietzsche & Aurelius (not class-based)
- **Keyword-based heuristics** (no LLM dependency)
- **Optional archetype/TW369 adjustments** for richer analysis
- **Fail-safe design** - errors never break pipeline

### Performance

- **Lightweight** - keyword matching only
- **Fast** - sub-millisecond analysis
- **Scalable** - no external API calls

---

## Backward Compatibility

**All v2.5 features are optional and disabled by default.**

- Meta-routing can be enabled via `KALDRA_META_ROUTING_ENABLED` flag
- No breaking changes to v2.3/v2.4 behavior
- All existing tests continue to pass
## Test Coverage

**59 tests passing** (100%):
- NietzscheEngine: 9/9 ✅
- AureliusEngine: 12/12 ✅
- CampbellEngine: 5/5 ✅
- MetaRouter: 6/6 ✅
- Legacy meta tests: 27/27 ✅

All v2.3/v2.4 tests continue to pass (100% backward compatibility).

---

## Documentation

**New Guides**:
1. [Meta-Engine Routing](./guides/META_ENGINE_ROUTING.md) - Technical reference
2. [Narrative Archetypes & Hero's Journey](./guides/NARRATIVE_ARCHETYPES_HERO_JOURNEY_DRIFT.md) - Conceptual guide with complete example

**Updated**:
- [KALDRA Core Roadmap](./core/KALDRA_CORE_MASTER_ROADMAP_V2.3_V2.9.md) - v2.5 marked complete
- [CHANGELOG](../CHANGELOG.md) - v2.5 entry added

---

## Known Limitations

- Heuristics are keyword-based (not LLM-powered)
- English language only
- Meta-analysis is interpretive, not deterministic

---

## Next Steps (v2.6+)

- LLM-powered meta-analysis (optional)
- Story aggregation & narrative arcs
- Apps specialization (Alpha/Geo/Product)

---

**KALDRA v2.5 - Philosophical Depth Achieved** 🎯
