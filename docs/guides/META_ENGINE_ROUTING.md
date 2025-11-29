# Meta-Engine Routing Guide

**KALDRA v2.5**

This guide documents the three meta-analysis engines and their use in intelligent routing.

---

## Overview

KALDRA v2.5 introduces three philosophical meta-engines that analyze text and signals through different lenses:

1. **NietzscheEngine-12** - Nietzschean analysis (power, nihilism, values)
2. **AureliusEngine-12** - Stoic analysis (discipline, regulation, serenity)
3. **CampbellEngine** - Hero's Journey stage detection

These engines feed into **MetaRouter** for intelligent app routing decisions.

---

## NietzscheEngine-12

### 12 Axes

1. **will_to_power** - Drive for dominance, creation, self-overcoming
2. **resentment** - Envy, victimization, reactive negativity
3. **life_affirmation** - Positive embrace of existence
4. **life_negation** - Rejection, exhaustion, world-weariness
5. **free_spirit** - Independence from tradition and convention
6. **active_nihilism** - Creative destruction, burning the old
7. **passive_nihilism** - Despair, apathy, giving up
8. **eternal_return_acceptance** - Radical acceptance of fate
9. **transvaluation** - Inversion of traditional values
10. **dionysian_force** - Chaos, excess, primal energy
11. **apollonian_order** - Form, harmony, rational structure
12. **amor_fati** - Loving acceptance of what is

### Usage

```python
from meta.nietzsche import analyze_meta

result = analyze_meta("We must overcome and dominate our challenges with strength!")

# Result
{
  "scores": {
    "will_to_power": 0.82,
    "dionysian_force": 0.61,
    "life_affirmation": 0.54,
    "amor_fati": 0.12,
    ...
  },
  "dominant_axes": [
    ("will_to_power", 0.82),
    ("dionysian_force", 0.61),
    ("life_affirmation", 0.54)
  ],
  "severity": 0.82,
  "notes": [
    "Dominant: will to power (0.82)",
    "High dionysian and apollonian forces"
  ]
}
```

---

## AureliusEngine-12

### 12 Stoic Axes

1. **perception_clarity** - Clear, undistorted perception of reality
2. **assent_to_reality** - Acceptance of facts as they are
3. **right_action** - Focus on duty, responsibility, virtue
4. **discipline_of_will** - Consistency, commitment, self-control
5. **emotional_regulation** - Low reactivity, measured response
6. **fate_acceptance** - Acceptance of what cannot be controlled
7. **control_dichotomy** - Distinction between controllable/uncontrollable
8. **premeditatio_malorum** - Anticipation of difficulties
9. **desire_restraint** - Moderation, absence of excess
10. **character_integrity** - Concern with honor, values, coherence
11. **self_mastery** - Internal dominion, not moved by externals
12. **serenity** - Calm tone, absence of catastrophizing

### Usage

```python
from meta.aurelius import analyze_meta

result = analyze_meta("I accept what I cannot control with calm discipline.")

# Result
{
  "scores": {
    "serenity": 0.74,
    "control_dichotomy": 0.81,
    "emotional_regulation": 0.68,
    "fate_acceptance": 0.72,
    ...
  },
  "dominant_axes": [
    ("control_dichotomy", 0.81),
    ("serenity", 0.74),
    ("fate_acceptance", 0.72)
  ],
  "severity": 0.68,  // Overall Stoic alignment
  "notes": [
    "Dominant: control dichotomy (0.81)",
    "High Stoic alignment: Strong discipline and regulation",
    "Strong control dichotomy awareness"
  ]
}
```

---

## CampbellEngine - Hero's Journey

### 12 Canonical Stages

1. **ordinary_world** - Mundo comum, low drift, stable
2. **call_to_adventure** - Rising drift, action archetypes emerging
3. **refusal_of_the_call** - High tension, defensive archetypes
4. **meeting_with_the_mentor** - Wisdom archetypes, high coherence
5. **crossing_the_threshold** - Clear regime change, rising drift
6. **tests_allies_enemies** - Oscillating drift, moderate coherence
7. **approach_to_cave** - Rising drift, preparation mode
8. **ordeal** - Peak drift, low coherence, crisis
9. **reward** - Falling drift after peak, constructive archetypes
10. **road_back** - Stabilizing drift, structural archetypes
11. **resurrection** - Transformative peak, transcendent archetypes
12. **return_with_elixir** - Low drift, high coherence, integration

### Usage

```python
from meta.campbell import CampbellEngine

engine = CampbellEngine()
result = engine.run(kaldra_signal)

# Result (MetaSignal format)
{
  "name": "campbell",
  "score": 0.78,
  "label": "ordeal",
  "details": {
    "stage_index": 7,
    "stage_name": "ordeal",
    "confidence": 0.78,
    "drift_pattern": {...},
    "archetype_context": {...}
  }
}
```

---

## MetaRouter

### Routing Logic

The MetaRouter combines all three engines to make intelligent routing decisions:

```python
from meta import MetaRouter

router = MetaRouter()
meta_signals = router.evaluate(kaldra_signal)
routing = router.decide_route(meta_signals)
```

### Routing Heuristics

1. **Crisis stages → Safeguard**
   - Campbell: `ordeal`, `approach_to_cave`, `tests_allies_enemies`
   - High drift + low coherence

2. **High Will to Power → Alpha/Product**
   - Nietzsche: `will_to_power` > 0.7
   - Action-oriented, expansion mode

3. **Regulated + Wisdom → Geo**
   - Aurelius: `serenity` > 0.7, `control_dichotomy` > 0.7
   - Strategic, macro analysis

4. **Reactive/Panic → Safeguard**
   - Aurelius: `emotional_regulation` < 0.4
   - Low Stoic alignment

5. **Transformative stages → Product**
   - Campbell: `reward`, `resurrection`, `return_with_elixir`
   - Creation/integration phase

6. **Beginning of journey → Alpha**
   - Campbell: `call_to_adventure`, `crossing_the_threshold`
   - Exploration mode

### Example Output

```json
{
  "dominant_app": "safeguard",
  "secondary_apps": ["kaldra"],
  "confidence": 0.78,
  "reasoning": "Hero's Journey stage 'ordeal' indicates crisis/challenge",
  "meta_signals": {
    "nietzsche": {...},
    "aurelius": {...},
    "campbell": {...}
  }
}
```

---

## Integration with KALDRA Signal

Meta-engines can optionally use KALDRA components for richer analysis:

```python
result = analyze_nietzsche(
    text="...",
    delta12=delta12_vector,      # Archetype adjustments
    tw_state=tw_state,            # Drift adjustments
    bias_score=0.3                # Bias context
)
```

### Adjustments

- **Nietzsche + Archetypes**: WARRIOR/REBEL → boost `will_to_power`
- **Nietzsche + TW369**: High drift → boost `dionysian_force`
- **Aurelius + Archetypes**: SAGE/RULER → boost `discipline_of_will`
- **Aurelius + TW369**: Low drift → boost `serenity`
- **Aurelius + Bias**: High bias → reduce `perception_clarity`

---

## Technical Notes

- **Keyword-based**: No LLM dependency, fast and lightweight
- **Fail-safe**: Errors never break pipeline
- **Optional**: All meta-analysis is optional and configurable
- **Backward compatible**: Can be disabled via feature flag

---

**See also**:
- [KALDRA v2.5 Release Notes](../KALDRA_V2.5_RELEASE_NOTES.md)
- [Narrative Archetypes & Hero's Journey](./NARRATIVE_ARCHETYPES_HERO_JOURNEY_DRIFT.md)
