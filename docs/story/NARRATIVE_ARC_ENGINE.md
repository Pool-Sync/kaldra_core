# Narrative Arc Engine - Campbell-Based Arc Tracking

**Component**: NarrativeArc  
**Version**: v2.6.0

---

## Overview

The Narrative Arc Engine combines Campbell's Hero's Journey with Δ144 states, TW369 drift, and meta-engine scores to detect, track, and predict narrative progression.

---

## Hybrid Model

### Three Layers

1. **Macro-Arc**: Campbell's 12 stages (Hero's Journey)
2. **Micro-States**: Δ144 archetypal states
3. **Energetic Dynamics**: TW369 drift + Nietzsche/Aurelius alignment

---

## Campbell's 12 Stages

### Act I: Departure
1. **ordinary_world** - Status quo, comfort zone
2. **call_to_adventure** - Disruption emerges
3. **refusal_of_the_call** - Fear, resistance
4. **meeting_with_the_mentor** - Guidance received
5. **crossing_the_threshold** - Point of no return

### Act II: Initiation
6. **tests_allies_enemies** - Learning, forming bonds
7. **approach_to_cave** - Preparation for ordeal
8. **ordeal** - Supreme test, death/rebirth
9. **reward** - Seizing the treasure

### Act III: Return
10. **road_back** - Reintegration begins
11. **resurrection** - Final transformation
12. **return_with_elixir** - Sharing the gift

---

## NarrativeArc Output

```python
@dataclass
class NarrativeArc:
    current_stage: str              # Campbell stage
    stage_confidence: float         # 0-1
    arc_progress: float             # 0-1 (stage_index / 11)
    transition_likelihood: float    # Probability of moving to next stage
    tension_trend: float            # +/- change in tension
    predicted_next_stage: str       # Next stage name
    predicted_inflection_distance: int  # Events until inflection
    
    # Supporting data
    stage_index: int
    drift_level: float
    meta_alignment: Dict[str, float]  # Nietzsche/Aurelius
```

---

## API

### Analyze Arc

```python
from story import analyze_arc

arc = analyze_arc(buffer)

print(f"Stage: {arc.current_stage}")
print(f"Progress: {arc.arc_progress:.2%}")
print(f"Next: {arc.predicted_next_stage}")
print(f"Tension: {arc.tension_trend:+.2f}")
```

### Predict Next Stage

```python
from story import predict_next_stage

next_stage = predict_next_stage(arc, buffer)
# Returns next stage in sequence
```

### Compute Tension

```python
from story import compute_tension

tension_delta = compute_tension(events)
# Positive = rising tension
# Negative = falling tension
```

---

## Tension Computation

Tension is a weighted combination of:

- **Drift level** (40%): Higher drift = higher tension
- **Nietzsche scores** (30%): will_to_power + active_nihilism
- **Aurelius regulation** (30%): Inverse of emotional_regulation

```python
tension = (
    drift * 0.4 +
    (will_to_power + active_nihilism) * 0.3 -
    (emotional_regulation - 0.5) * 0.3
)
```

---

## Transition Likelihood

Based on:
- **Time in stage**: More events → higher likelihood
- **Drift acceleration**: Rapid change → higher likelihood
- **Meta-score changes**: Significant shifts → higher likelihood

**Typical Stage Duration**: 2-4 events

**Crisis Stages** (ordeal, approach, resurrection): 1-2 events

---

## Example: Complete Narrative

```python
from story import StoryBuffer, analyze_arc

buffer = StoryBuffer(capacity=12)

# Event 1: Ordinary World
buffer.add_event(
    "Life is stable and predictable.",
    meta_scores={"campbell": {"stage": "ordinary_world", "confidence": 0.8}}
)

# Event 2: Call to Adventure
buffer.add_event(
    "An unexpected opportunity arises.",
    meta_scores={"campbell": {"stage": "call_to_adventure", "confidence": 0.75}}
)

# Event 3: Refusal
buffer.add_event(
    "Fear and doubt hold me back.",
    meta_scores={"campbell": {"stage": "refusal_of_the_call", "confidence": 0.7}}
)

# Analyze
arc = analyze_arc(buffer)
print(f"Current: {arc.current_stage}")  # "refusal_of_the_call"
print(f"Progress: {arc.arc_progress:.2%}")  # "16.67%"
print(f"Next: {arc.predicted_next_stage}")  # "meeting_with_the_mentor"
```

---

## Integration with Meta-Engines

### Nietzsche Influence

- **High will_to_power** → Likely in active stages (threshold, tests, ordeal)
- **High passive_nihilism** → Likely in refusal or despair
- **High amor_fati** → Likely in return/resurrection

### Aurelius Influence

- **High serenity** → Likely in ordinary_world or return
- **Low emotional_regulation** → Likely in ordeal or crisis
- **High discipline** → Likely in tests or road_back

---

## Inflection Distance Prediction

Predicts how many events until next major inflection:

- **Crisis stages**: 1 event (fast transitions)
- **Normal stages**: 3 events (typical duration)
- **Based on**: Stage type, drift acceleration, meta-score volatility

---

## Future Enhancements

- LLM-powered stage detection
- Multi-path arc support (non-linear narratives)
- Sub-stage granularity
- Confidence calibration via historical data
- Cross-narrative arc comparison

---

**See Also**:
- [Story Engine Spec](./STORY_ENGINE_SPEC.md)
- [Narrative Archetypes & Hero's Journey](../guides/NARRATIVE_ARCHETYPES_HERO_JOURNEY_DRIFT.md)
