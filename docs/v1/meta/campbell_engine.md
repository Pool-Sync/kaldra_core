# CampbellEngine v3.1 — Hero's Journey Snapshot Analysis

**Version:** 3.1  
**Status:** INTEGRATED  
**Module:** `src/meta/campbell_engine.py`  
**Tests:** `tests/meta/test_campbell_engine.py`

---

## Overview

The **CampbellEngine** analyzes text through the lens of the **Hero's Journey (Monomyth)**. In v3.1, it operates in **Snapshot Mode**, detecting the current journey stage and active archetypal roles based on a single text input, without historical context (which arrives in v3.2).

### Core Capabilities

1.  **Archetype Normalization**: Maps Δ144 archetypes (e.g., `A04_HERO`) to standard Campbell roles (`HERO`, `MENTOR`, `SHADOW`).
2.  **Stage Detection**: Identifies one of the 12 Journey Stages using heuristic keyword analysis and semantic signals.
3.  **Mythic Resonance**: Uses **Kindra 3×48** to measure the depth and intensity of the mythic pattern.
4.  **Transformation Potential**: Uses **TW369** drift and regime data to estimate the potential for narrative growth or change.

---

## Archetype Mapping (Δ144 → Campbell)

The engine enforces a strict mapping from the 12 primary Δ144 archetypes to Campbellian roles:

| Δ144 ID | Campbell Role | Function |
| :--- | :--- | :--- |
| `A04_HERO` | **HERO** | The protagonist; growth, action, sacrifice. |
| `A02_SAGE` | **MENTOR** | Guidance, wisdom, gifts. |
| `A07_RULER` | **THRESHOLD_GUARDIAN** | Tests the hero at boundaries. |
| `A05_EXPLORER` | **HERALD** | Announces change, call to adventure. |
| `A03_MAGICIAN` | **SHAPESHIFTER** | Ambiguity, change, doubt. |
| `A08_REBEL` | **SHADOW** | The antagonist or repressed self. |
| `A06_CAREGIVER` | **ALLY** | Support, team, friendship. |
| `A11_TRICKSTER` | **TRICKSTER** | Disruptor, comic relief, chaos. |
| `A01_CREATOR` | **CREATOR** | Higher-order mentor or god-figure. |
| `A09_LOVER` | **LOVER** | Temptation or union (Goddess). |
| `A10_INNOCENT` | **INNOCENT** | Starting state, purity. |
| `A12_ORACLE` | **ORACLE** | Prophecy, insight. |

---

## Input Schema

### MetaInput

The engine accepts the standard `MetaInput` dataclass:

```python
@dataclass
class MetaInput:
    text: str                                    # Required
    delta144_state: Optional[str] = None         # e.g., "A04_HERO_STATE_01"
    archetype_scores: Dict[str, float] = {}      # Full distribution
    kindra: Optional[KindraContext] = None       # 3×48 vectors
    tw_state: Optional[TWState] = None           # Drift/Regime
    # ... other fields
```

---

## Output Schema

### CampbellSignal

```python
@dataclass
class CampbellSignal(MetaSignal):
    journey_stage: str                        # One of 12 stages
    archetypal_roles: Dict[str, str]          # {id: role}
    transformation_potential: float           # [0, 1]
    mythic_resonance: float                   # [0, 1]
    active_archetypes: List[str]              # Top active roles
    scores: Dict[str, float]                  # Auxiliary scores
    dominant_axes: List[Tuple[str, float]]    # Top stages/themes
    severity: float                           # Mythic pattern strength
    notes: List[str]                          # Interpretive notes
```

---

## Integration Logic

### Kindra 3×48 Integration
The engine extracts a **Mythic Signature** from Kindra layers:
*   **Narrative Intensity (Layer 2):** Conflict, urgency. High intensity suggests `ORDEAL` or `RESURRECTION`.
*   **Archetypal Depth (Layer 3):** Symbolism, meaning. Increases `mythic_resonance`.
*   **Liminality (Layer 2+3):** Transition signals. Suggests `CROSSING_THRESHOLD`.

### TW369 Integration
Estimates **Transformation Potential**:
*   **High Drift + Critical Regime:** Increases potential (crisis forces change).
*   **Stable Regime + Ordinary World:** Decreases potential (stagnation).

---

## Examples

### 1. Call to Adventure
**Input:** *"A mysterious message arrived today, challenging everything I know."*
**Output:**
*   **Stage:** `CALL_TO_ADVENTURE`
*   **Roles:** `HERALD` (if A05 present)
*   **Notes:** "Stage: Call to Adventure (Conf: 0.85)"

### 2. The Ordeal (High Resonance)
**Input:** *"Facing the shadow in the abyss, a battle for the soul."* (with Kindra Depth=0.9)
**Output:**
*   **Stage:** `ORDEAL`
*   **Mythic Resonance:** 0.85 (High)
*   **Transformation Potential:** 0.9 (High)

---

## Limitations & Roadmap

*   **Snapshot Only:** v3.1 does not track the hero's progress over time. It only identifies the *current* stage of the input text.
*   **Heuristic Detection:** Stage detection relies on keywords and may be sensitive to phrasing.
*   **v3.2 (Future):** Will introduce `StoryContext` to track the full 12-stage cycle across multiple events.

---

**Last Updated:** 2025-12-01
**Version:** 3.1.0
