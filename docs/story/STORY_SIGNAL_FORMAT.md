# Story Signal Format - v2.6 Extended Output

**Version**: v2.6.0  
**Schema**: `schema/story/story_signal.schema.json`

---

## Overview

StorySignal extends the standard KALDRA signal with a `story` block containing temporal narrative analysis.

---

## Complete Format

```json
{
  "signal_id": "uuid-string",
  "timestamp": 1234567890.123,
  
  "delta12": {
    "A01_INNOCENT": 0.2,
    "A03_WARRIOR": 0.5,
    "A07_RULER": 0.3
  },
  
  "delta144": {
    "state": "A03_WARRIOR_3_05",
    "profile": "neutral",
    "modifier": 5
  },
  
  "kindra": {
    "layer1": [...],
    "layer2": [...],
    "layer3": [...]
  },
  
  "meta": {
    "nietzsche": {
      "will_to_power": 0.75,
      "amor_fati": 0.45,
      ...
    },
    "aurelius": {
      "serenity": 0.62,
      "emotional_regulation": 0.58,
      ...
    },
    "campbell": {
      "stage": "tests_allies_enemies",
      "confidence": 0.72
    }
  },
  
  "tw369": {
    "severity": 0.52,
    "plane": "3",
    "regime": "expansion"
  },
  
  "story": {
    "narrative_stage": "tests_allies_enemies",
    "arc_progress": 0.42,
    "timeline": [...],
    "inflection_points": [...],
    "motion_vectors": [...],
    "drift_trajectory": {...},
    "predicted_next_stage": "approach_to_cave",
    "tension_trend": +0.14,
    "transition_likelihood": 0.65
  }
}
```

---

## Story Block Fields

### narrative_stage

**Type**: `string`  
**Description**: Current Campbell Hero's Journey stage

**Values**:
- `ordinary_world`
- `call_to_adventure`
- `refusal_of_the_call`
- `meeting_with_the_mentor`
- `crossing_the_threshold`
- `tests_allies_enemies`
- `approach_to_cave`
- `ordeal`
- `reward`
- `road_back`
- `resurrection`
- `return_with_elixir`

### arc_progress

**Type**: `number` (0.0-1.0)  
**Description**: Progress through Hero's Journey arc

**Interpretation**:
- `0.0`: Beginning (ordinary_world)
- `0.5`: Midpoint (approach_to_cave/ordeal)
- `1.0`: Complete (return_with_elixir)

### timeline

**Type**: `array`  
**Description**: Recent timeline points (condensed)

**Format**:
```json
[
  {
    "sequence_id": 10,
    "timestamp": 1234567890.0,
    "delta12_dominant": "A03_WARRIOR",
    "drift_level": 0.52
  },
  ...
]
```

### inflection_points

**Type**: `array`  
**Description**: Detected narrative inflection points

**Format**:
```json
[
  {
    "event_id": "uuid",
    "inflection_type": "drift_peak",
    "magnitude": 0.85,
    "description": "Drift peak at 0.85"
  },
  {
    "event_id": "uuid",
    "inflection_type": "archetype_shift",
    "magnitude": 0.62,
    "description": "Archetype shift: A01_INNOCENT → A03_WARRIOR"
  }
]
```

**Inflection Types**:
- `drift_peak`: Local maximum in drift
- `archetype_shift`: Dominant archetype changed
- `stage_transition`: Campbell stage changed
- `meta_inversion`: Meta-score sign flip

### motion_vectors

**Type**: `array`  
**Description**: Narrative motion between events

**Format**:
```json
[
  {
    "delta12_shift_magnitude": 0.42,
    "drift_velocity": 0.05,
    "time_delta": 2.5
  },
  ...
]
```

### drift_trajectory

**Type**: `object`  
**Description**: Drift evolution analysis

**Format**:
```json
{
  "drift_slope": 0.05,
  "drift_acceleration": 0.02,
  "drift_volatility": 0.12
}
```

**Interpretation**:
- **drift_slope > 0**: Rising tension
- **drift_slope < 0**: Falling tension
- **drift_acceleration > 0**: Accelerating change
- **drift_volatility > 0.2**: Highly unstable

### predicted_next_stage

**Type**: `string`  
**Description**: Predicted next Campbell stage

### tension_trend

**Type**: `number`  
**Description**: Change in narrative tension (+/-)

**Interpretation**:
- **> +0.1**: Rapidly rising tension
- **-0.1 to +0.1**: Stable
- **< -0.1**: Rapidly falling tension

### transition_likelihood

**Type**: `number` (0.0-1.0)  
**Description**: Probability of transitioning to next stage

**Interpretation**:
- **> 0.7**: Transition imminent
- **0.4-0.7**: Moderate likelihood
- **< 0.4**: Unlikely to transition soon

---

## Example: Complete Story Signal

```json
{
  "signal_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": 1701234567.890,
  
  "delta12": {
    "A03_WARRIOR": 0.65,
    "A05_SEEKER": 0.25,
    "A10_SAGE": 0.10
  },
  
  "delta144": {
    "state": "A03_WARRIOR_3_06"
  },
  
  "meta": {
    "campbell": {
      "stage": "tests_allies_enemies",
      "confidence": 0.75
    }
  },
  
  "tw369": {
    "severity": 0.58,
    "plane": "3"
  },
  
  "story": {
    "narrative_stage": "tests_allies_enemies",
    "arc_progress": 0.42,
    "timeline": [
      {"sequence_id": 8, "delta12_dominant": "A01_INNOCENT", "drift_level": 0.25},
      {"sequence_id": 9, "delta12_dominant": "A03_WARRIOR", "drift_level": 0.45},
      {"sequence_id": 10, "delta12_dominant": "A03_WARRIOR", "drift_level": 0.58}
    ],
    "inflection_points": [
      {
        "event_id": "uuid-9",
        "inflection_type": "archetype_shift",
        "magnitude": 0.52,
        "description": "Archetype shift: A01_INNOCENT → A03_WARRIOR"
      }
    ],
    "motion_vectors": [
      {"delta12_shift_magnitude": 0.52, "drift_velocity": 0.08},
      {"delta12_shift_magnitude": 0.15, "drift_velocity": 0.05}
    ],
    "drift_trajectory": {
      "drift_slope": 0.06,
      "drift_acceleration": 0.01,
      "drift_volatility": 0.08
    },
    "predicted_next_stage": "approach_to_cave",
    "tension_trend": +0.12,
    "transition_likelihood": 0.55
  }
}
```

---

## Backward Compatibility

**Story block is optional**:
- If `story_mode=false` (default): No `story` block
- If `story_mode=true`: Full `story` block included

**All v2.5 fields preserved**:
- `delta12`, `delta144`, `kindra`, `meta`, `tw369` unchanged

---

## Schema Validation

Use JSON Schema validator:

```python
import json
import jsonschema

with open("schema/story/story_signal.schema.json") as f:
    schema = json.load(f)

jsonschema.validate(story_signal, schema)
```

---

## Use Cases

### 1. Real-Time Narrative Monitoring

```python
if story_signal["story"]["tension_trend"] > 0.15:
    alert("Tension rising rapidly!")

if story_signal["story"]["narrative_stage"] == "ordeal":
    alert("Crisis moment detected!")
```

### 2. Arc Progress Tracking

```python
progress = story_signal["story"]["arc_progress"]

if progress < 0.3:
    print("Early in journey")
elif progress < 0.7:
    print("Midpoint crisis")
else:
    print("Approaching resolution")
```

### 3. Inflection Detection

```python
inflections = story_signal["story"]["inflection_points"]

for inf in inflections:
    if inf["inflection_type"] == "drift_peak":
        print(f"Peak tension: {inf['magnitude']:.2f}")
```

---

**See Also**:
- [Story Engine Spec](./STORY_ENGINE_SPEC.md)
- [Narrative Arc Engine](./NARRATIVE_ARC_ENGINE.md)
- [Timeline Engine](./TIMELINE_ENGINE.md)
