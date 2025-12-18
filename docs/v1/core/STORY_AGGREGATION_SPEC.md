# KALDRA Story Aggregation — Specification v1.0
**Version:** 1.0  
**Status:** Production-Ready (Core v2.5 – Story-Level Base)  
**Last Updated:** 2025-11-27  
**Module:** `src/core/story_aggregator.py`, `src/core/story_tracker.py`  

---

## 1. Overview

The **KALDRA Story Aggregation layer** provides multi-turn narrative tracking on top of turn-level `KaldraSignal` outputs.

Instead of analyzing each turn in isolation, this layer:

- Groups multiple turns into a **story/session**
- Tracks **Δ144 state evolution** over time
- Computes a scalar **narrative coherence** metric
- Extracts **dominant archetypes** at story-level
- Produces a structure aligned with `schema/story/story_schema.json`

This module is **purely aggregative**: it does **not** change any engine logic (`Δ144`, `TW369`, `Kindras`, Master Engine). It reads signals and builds a higher-level representation.

---

## 2. Architecture

### 2.1 High-Level Flow

```mermaid
graph TD
    A[Raw Text Turns] --> B[KALDRA Master Engine]
    B --> C[KaldraSignal (per turn)]
    C --> D[StoryTracker]
    D --> E[StoryAggregator]
    E --> F[Story Object (schema/story/story_schema.json)]
```

### 2.2 Module Structure

```text
schema/
└── story/
    └── story_schema.json        # Story object schema

src/core/
├── story_aggregator.py          # StoryAggregator + StoryTurnSignal
└── story_tracker.py             # StoryTracker + StoryTurn (in-memory)

tests/core/
└── test_story_aggregation.py    # Story-level tests
```

---

## 3. Data Model (Story Schema)

**Location:** `schema/story/story_schema.json`

Key fields (resumo):

* `story_id: str` — Unique story/session identifier
* `turns: List[Turn]` — Ordered list of turns
* `delta144_evolution: List[DeltaStep]` — Evolution of Δ144 states
* `narrative_coherence: float ∈ [0,1]` — Overall coherence metric
* `dominant_archetypes: List[int]` — Top archetype indices for the story
* `coherence_trace: List[{turn_index, coherence}]` — Per-turn coherence
* `metadata: Dict[str, Any]` — Optional story-level metadata

Each `Turn` contains:

* `turn_index: int`
* `timestamp: str (ISO)`
* `role: str` (e.g., `"user"`, `"assistant"`, `"system"`)
* `text: str`
* `metadata: object`
* `signal_summary: object` — compact KALDRA signal summary

Each `signal_summary` contains:

* `archetype_top_index: int`
* `archetype_top_prob: float`
* `delta_state_id: str | null`
* `tw_trigger: bool | null`
* `tw_severity: float | null`
* `epistemic_status: str | null`

---

## 4. Core Components

### 4.1 `StoryTurnSignal`

**Location:** `src/core/story_aggregator.py`

Minimal protocol-level view over a `KaldraSignal`-like object:

* `archetype_probs: np.ndarray` (1D)
* `delta_state: Optional[dict]` — should expose `id` or `state_id`
* `tw_trigger: Optional[bool]`
* `tw_stats: Optional[dict]` — may contain `severity`
* `epistemic_status: Optional[str]`

Factory:

```python
StoryTurnSignal.from_signal(signal: Any) -> StoryTurnSignal
```

Responsibility: normalize engine-specific signal into a stable structure for aggregation.

---

### 4.2 `StoryAggregator`

**Location:** `src/core/story_aggregator.py`

Main responsibilities:

* Convert a list of **turn payloads** into a **story object** aligned with `story_schema.json`
* Compute:

  * `narrative_coherence` (placeholder v1.0)
  * `dominant_archetypes`
  * `coherence_trace`
  * `delta144_evolution`

Public API:

```python
class StoryAggregator:
    def __init__(self, top_k_archetypes: int = 3) -> None: ...

    def aggregate(
        self,
        story_id: str,
        turns: Sequence[Dict[str, Any]],
    ) -> Dict[str, Any]:
        ...
```

`turns` expected shape:

```python
{
  "turn_index": int,
  "timestamp": str,     # ISO
  "role": str,
  "text": str,
  "metadata": dict,
  "signal": KaldraSignal-like | StoryTurnSignal
}
```

#### 4.2.1 Dominant Archetypes

* Extract `np.argmax(archetype_probs)` per turn
* Count frequency across story
* Return top `top_k_archetypes` indices

#### 4.2.2 Narrative Coherence (v1.0)

Combination of:

1. **Stability** of dominant archetype across adjacent turns

   * Fraction of turns where `idx_t == idx_(t-1)`
2. **Mean top probability** (from `coherence_trace`)

Formula (v1.0):

```python
coherence = clamp(0.5 * stability + 0.5 * avg_conf, 0.0, 1.0)
```

This is a placeholder metric to be refined in later versions.

---

### 4.3 `StoryTracker`

**Location:** `src/core/story_tracker.py`

In-memory session manager.

Responsibilities:

* Create story IDs
* Append turns (text + signal)
* Aggregate stories via `StoryAggregator`

Public API (v1.0):

```python
class StoryTracker:
    def create_story(self, create_story: Optional[str] = None) -> str: ...
    def add_turn(
        self,
        story_id: str,
        role: str,
        text: str,
        signal: Any,
        timestamp: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> StoryTurn: ...
    def get_story_turns(self, story_id: str) -> List[StoryTurn]: ...
    def aggregate_story(self, story_id: str) -> Dict[str, Any]: ...
    def reset_story(self, story_id: str) -> None: ...
    def delete_story(self, story_id: str) -> None: ...
    def list_story_ids(self) -> List[str]: ...
```

Implementation:

* Uses `uuid.uuid4().hex` for default IDs
* Stores turns in a dict: `self._stories: Dict[str, List[StoryTurn]]`
* Uses `StoryAggregator` internally in `aggregate_story`.

---

## 5. Example Usage

### 5.1 Engine + Story Tracking (Pseudo-Example)

```python
import numpy as np
from src.core.kaldra_master_engine import KaldraMasterEngineV2
from src.core.story_tracker import StoryTracker

engine = KaldraMasterEngineV2(d_ctx=256)
tracker = StoryTracker()

# 1) Create story
story_id = tracker.create_story()

# 2) Simulate conversation
turn_texts = [
    ("user", "The company reported strong earnings this quarter."),
    ("assistant", "The results suggest confidence in future growth."),
    ("user", "However, some regions are still underperforming."),
]

for role, text in turn_texts:
    # Here you would generate an embedding and call engine.infer_from_embedding(...)
    # For this example, assume `signal` is already produced.
    embedding = np.random.randn(256).astype(np.float32)
    signal = engine.infer_from_embedding(embedding)

    tracker.add_turn(
        story_id=story_id,
        role=role,
        text=text,
        signal=signal,
    )

# 3) Aggregate story
story_obj = tracker.aggregate_story(story_id)
print(story_obj["story_id"])
print(story_obj["narrative_coherence"])
print(story_obj["dominant_archetypes"])
```

---

## 6. Future Implementations (Short/Medium Term)

### 6.1 Persistent Story Storage

* Store stories in:

  * PostgreSQL (relational, indexed by `story_id`, `created_at`)
  * MongoDB (flexible nested structures)
  * Time-series DB for coherence traces
* Features:

  * Query stories by domain (Alpha/GEO/Product/Safeguard)
  * Replay stories
  * Longitudinal analysis of narrative evolution

### 6.2 Domain-Aware Story Profiles

* Map stories to:

  * **Alpha**: Earnings call multi-turn analysis
  * **GEO**: Speech sequences, geopolitical briefings
  * **Product**: UX feedback threads
  * **Safeguard**: Multi-turn risk narratives
* Add domain-specific metadata:

  * `domain`, `ticker`, `region`, `channel`, etc.

### 6.3 Configurable Coherence Models

* Replace simple v1.0 metric with pluggable models:

  * Cosine similarity of archetype distributions across turns
  * Drift-based metrics from TW369
  * Multi-window coherence (local vs global)

---

## 7. Enhancements (Short/Medium Term)

### 7.1 Story-Level Features

* **Archetype Volatility**:

  * Measure how often the dominant archetype changes
  * Label stories as “stable”, “volatile”, “bifurcated”
* **Regime Segmentation**:

  * Segment stories into regimes (e.g., “EXPANSIVE block”, “CONTRACTIVE block”)
* **TW Event Markers**:

  * Mark turns with TW triggers as structural breakpoints

### 7.2 Story Filters & Queries

* Filter stories by:

  * `narrative_coherence` thresholds
  * Presence of specific archetypes
  * TW trigger density
* Return:

  * Top-N “most coherent” stories
  * Top-N “most unstable” stories

### 7.3 Story Serialization & Export

* JSON export aligned with `story_schema.json`
* NDJSON for large collections
* Integration with external tools (e.g., BI dashboards) via export files

---

## 8. Research Track (Long Term)

### 8.1 Narrative Coherence Metrics

* Investigate:

  * Graph-based measures over turn-level archetype transitions
  * Information-theoretic measures (entropy, KL divergence across turns)
  * Dynamic systems view using TW369 drift as trajectory

### 8.2 Story Archetype Trajectories

* Model story as path in a 144-dimensional archetype manifold:

  * Identify canonical paths (e.g., “Hero’s Journey” signatures)
  * Compare real stories to templates (Campbell / Jung patterns)

### 8.3 Multi-Story Comparative Analysis

* Cross-story similarity:

  * Clustering by archetype evolution
  * Compare multiple earnings calls from same company or sector
* Detect:

  * Regime shifts in narrative over quarters / years
  * Drift in “official story” of institutions

### 8.4 Integration with Bias Engine

* Story-level bias metrics:

  * Aggregate bias scores over turns
  * Identify stories with concentrated bias regions
* Use case:

  * Multi-turn content moderation
  * Narrative fairness evaluation

---

## 9. Known Limitations

### 9.1 In-Memory Only

* `StoryTracker` v1.0 uses an in-memory dict.
* No persistence:

  * Stories lost when process restarts.
* Not suitable for large-scale or multi-process deployments.

### 9.2 Simplified Coherence Metric

* Current `narrative_coherence` is a simple blend:

  * Archetype stability
  * Average top probability
* Does **not**:

  * Capture semantic consistency of text directly
  * Use TW369 or Δ144 in full depth (yet)

### 9.3 Engine-Agnostic Assumptions

* `StoryTurnSignal.from_signal` assumes:

  * `archetype_probs` exists and is 1D
  * `delta_state` has an `id` or `state_id`
* If these invariants change in the core engine, adapter may require updates.

### 9.4 No Concurrency Guarantees

* `StoryTracker` is not thread-safe:

  * Concurrent writes to same `story_id` may race
* For multi-thread/multi-process, a synchronized or external store is required.

---

## 10. Testing

### 10.1 Unit Tests

**Location:** `tests/core/test_story_aggregation.py`

Covered behaviors:

* `StoryAggregator.aggregate()`:

  * Produces valid structure with:

    * `story_id`
    * `turns`
    * `delta144_evolution`
    * `narrative_coherence`
    * `dominant_archetypes`
  * `narrative_coherence ∈ [0,1]`
  * `dominant_archetypes` length ≤ `top_k_archetypes`
* `StoryTracker` lifecycle:

  * `create_story()`
  * `add_turn()`
  * `get_story_turns()`
  * `aggregate_story()`
  * `reset_story()`

### 10.2 Dummy Signals

Tests use a `DummySignal`:

* `archetype_probs` (manually constructed)
* Optional `delta_state`, `tw_trigger`, `tw_severity`, `epistemic_status`
* Ensures Story Aggregation logic is tested **without** invoking real engines.

### 10.3 Example Commands

```bash
# Story-level tests only
pytest tests/core/test_story_aggregation.py -v

# Full test suite (example)
pytest -v
```

---

## 11. Next Steps

### 11.1 Immediate (Story v1.0 – Done)

* [x] Define `story_schema.json`
* [x] Implement `StoryAggregator` with basic coherence metric
* [x] Implement `StoryTracker` in-memory
* [x] Add unit tests (`test_story_aggregation.py`)
* [x] Document architecture and behavior (this file)

### 11.2 Short Term (v2.6)

* [ ] Add optional persistence layer (e.g., simple SQLite/PostgreSQL adapter)
* [ ] Expose story aggregation via API Gateway endpoint
* [ ] Integrate with KALDRA Explorer (story-level timeline views)
* [ ] Add story-level filters in 4iam.ai frontend

### 11.3 Medium Term (v2.7+)

* [ ] Replace coherence placeholder with advanced metric
* [ ] Integrate TW369 drift and Δ144 regime detection in story-level features
* [ ] Enable domain-specific story types (Alpha/GEO/Product/Safeguard)
* [ ] Add story comparison and clustering utilities

---

## 12. Related Documentation

* `docs/core/MASTER_ENGINE_AND_DATALAB_OVERVIEW.md`
* `docs/core/BIAS_ENGINE_SPEC.md`
* `docs/core/TW369_ENGINE_SPEC.md` (when available)
* `docs/core/DELTA144_ENGINE_SPEC.md` (when available)

---

## 13. Version History

* **v1.0** (2025-11-27)

  * Initial story schema (`schema/story/story_schema.json`)
  * `StoryAggregator` v1.0 with basic coherence
  * `StoryTracker` in-memory implementation
  * Unit tests for story aggregation and tracking
  * This specification document

---

**Document Status:** Complete & aligned with Story-Level Aggregation v1.0
**Location:** `docs/core/STORY_AGGREGATION_SPEC.md`
**Maintainer:** KALDRA Core Team
