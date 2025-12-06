# Story Engine Phase 1: Temporal Mind Primitives

**Version:** KALDRA v3.2 (Temporal Mind)  
**Phase:** 1 - Core Primitives  
**Status:** Implemented  
**Date:** 2025-12-03

---

## 1. Overview

Phase 1 of the Story Engine introduces the foundational primitives for **Temporal Mind** capabilities. These components enable KALDRA to analyze narrative structures over time, detecting arcs, transitions, and coherence.

**Key Characteristics:**
- **Backend-Only:** No API exposure or frontend integration yet.
- **Isolated:** Does not affect v3.1 Exoskeleton or Unification Layer.
- **In-Memory:** Uses efficient in-memory buffers (no persistence yet).
- **Opt-In:** Must be explicitly instantiated and used.

---

## 2. Architecture

The Story Engine consists of four decoupled components:

1.  **StoryBuffer**: Stores the temporal sequence of events.
2.  **TimelineBuilder**: Analyzes the buffer to track archetype transitions.
3.  **ArcDetector**: Maps events to Hero's Journey stages.
4.  **CoherenceScorer**: Evaluates narrative consistency.

```mermaid
graph TD
    Input[Input Text] --> Event[StoryEvent]
    Event --> Buffer[StoryBuffer]
    Buffer -->|List[Event]| TimelineBuilder
    Buffer -->|List[Event]| ArcDetector
    
    TimelineBuilder --> Timeline[StoryTimeline]
    ArcDetector --> Arc[StoryArc]
    
    Timeline --> CoherenceScorer
    Arc --> CoherenceScorer
    
    CoherenceScorer --> Score[CoherenceScore]
```

---

## 3. Data Structures

### 3.1 StoryEvent
Represents a single point in narrative time.
```python
@dataclass
class StoryEvent:
    timestamp: datetime
    text: str
    archetype_id: Optional[str]
    archetype_scores: Dict[str, float]
    polarities: Dict[str, float]
    metadata: Dict[str, Any]
```

### 3.2 StoryTimeline
Aggregates events and analyzes transitions.
```python
@dataclass
class StoryTimeline:
    events: List[StoryEvent]
    archetype_transitions: List[ArchetypeTransition]
    transition_counts: Dict[str, int]
    metadata: Dict[str, Any]  # e.g., {"has_cycle": True}
```

### 3.3 StoryArc
Represents the detected narrative structure.
```python
@dataclass
class StoryArc:
    dominant_stage: str  # e.g., "ORDEAL"
    stage_scores: Dict[str, float]
    notes: List[str]
```

### 3.4 CoherenceScore
Metrics for narrative quality and consistency.
```python
@dataclass
class CoherenceScore:
    overall: float               # [0, 1]
    archetype_consistency: float # [0, 1]
    polarity_smoothness: float   # [0, 1]
    stage_alignment: float       # [0, 1]
```

---

## 4. Integration Points (Planned)

These components are designed to be integrated into the **Unification Pipeline** in Phase 2:

1.  **StoryStage**: A new pipeline stage that will:
    - Convert `UnifiedContext` inputs into `StoryEvents`.
    - Push events to a persistent `StoryBuffer`.
    - Run `TimelineBuilder`, `ArcDetector`, and `CoherenceScorer`.
    - Populate `StoryContext` in the final signal.

2.  **TW369 Integration**:
    - TW drift metrics will feed into `CoherenceScorer`.
    - Temporal coupling will use `StoryTimeline` to adjust drift vectors.

---

## 5. Limitations (Phase 1)

- **Memory Only**: Events are lost on process restart.
- **Heuristic Detection**: Arc detection relies on simple keywords and archetype mapping, not deep semantic understanding.
- **No Persistence**: No database backing.
- **Single Session**: Designed for single-session analysis or short-term memory.

---

## 6. Testing

Run the dedicated test suite:
```bash
python -m pytest tests/story/ -v
```

Current coverage:
- **StoryBuffer**: Capacity, windowing, indexing.
- **TimelineBuilder**: Transition tracking, cycle detection.
- **ArcDetector**: Stage detection, normalization.
- **CoherenceScorer**: Consistency, smoothness, alignment.

---

## 7. Next Steps

1.  **Phase 2: StoryStage Integration**
    - Wire components into `src/unification/pipeline/story_stage.py`.
    - Connect to `UnifiedKaldra`.

2.  **Phase 3: Persistence**
    - Implement file-based or DB-based backing for `StoryBuffer`.

3.  **Phase 4: Advanced Intelligence**
    - Integrate CampbellEngine v3.1 for deeper arc analysis.
    - Connect TW369 temporal vectors.
