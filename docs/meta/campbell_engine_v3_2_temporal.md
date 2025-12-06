# CampbellEngine v3.2 — Temporal Extension

## Overview

**CampbellEngine v3.2** elevates the Hero's Journey analyzer from **snapshot-only (v3.1)** to **temporal-aware**, enabling:

- **Journey sequence tracking**: Progression through Campbell stages over time
- **Arc completeness measurement**: How far along the full monomyth journey
- **Temporal coherence scoring**: Narrative consistency across events
- **Drift coupling**: Alignment between TW369 regime shifts and journey milestones
- **Δ144 alignment**: Archetypal evolution tracking with Campbell roles

**Constraints maintained**:
- ❌ No API v3.1 changes
- ❌ No SignalAdapter modifications
- ✅ 100% backward compatible (v3.1 tests: 9/9 passing)

---

## Data Structures

### StoryContext (Extended)

**File**: `src/unification/states/unified_state.py`

```python
@dataclass
class StoryContext:
    events: List[StoryEvent]
    arc: Optional[StoryArc]          # From arc_detector.py
    timeline: Optional[StoryTimeline] # From timeline_builder.py
    coherence: float                  # Scalar or CoherenceScore object
    metadata: Dict[str, Any]          # v3.2: "delta144_timeline"
```

**Δ144 Timeline format** (in `metadata["delta144_timeline"]`):
```python
[
    {"t": unix_timestamp, "state_id": "A04_HERO", "weight": 0.83},
    {"t": unix_timestamp, "state_id": "A02_SAGE", "weight": 0.76},
    ...
]
```

---

### CampbellSignal (Extended)

**File**: `src/meta/campbell_engine.py`

**New v3.2 fields**:
```python
@dataclass
class CampbellSignal(MetaSignal):
    # v3.1 fields (unchanged)
    journey_stage: str
    archetypal_roles: Dict[str, str]
    transformation_potential: float
    mythic_resonance: float
    active_archetypes: List[str]
    
    # v3.2 temporal fields (default values for backward compat)
    journey_sequence: List[str] = []           # Stages in temporal order
    temporal_coherence: float = 0.0           # [0, 1] Narrative consistency
    arc_completeness: float = 0.0             # [0, 1] Monomyth progress
    drift_coupling: float = 0.0               # [0, 1] Drift-journey alignment
    delta144_alignment: float = 0.0           # [0, 1] Archetype coherence
```

---

### MetaInput (Extended)

**File**: `src/meta/types.py`

```python
@dataclass
class MetaInput:
    # v3.1 fields (unchanged)
    text: str
    delta144_state: Optional[str]
    archetype_scores: Dict[str, float]
    kindra: Optional[KindraContext]
    tw_state: Optional[TWState]
    
    # v3.2 temporal contexts (TODO v3.3: unified refactor)
    drift_ctx: Optional[DriftContext] = None
    story_ctx: Optional[StoryContext] = None
```

---

## Temporal Metrics

### journey_sequence

**Method**: `_infer_journey_sequence_from_story(story_ctx)`

**Logic**:
1. Extract from `story_ctx.arc.stage_scores`
2. Include stages with score > 0.1 (threshold)
3. Sort by score descending
4. Remove consecutive duplicates

**Example**:
```python
story_ctx.arc.stage_scores = {
    "CALL_TO_ADVENTURE": 0.8,
    "MEETING_MENTOR": 0.6,
    "ORDEAL": 0.9
}
# → journey_sequence = ["ORDEAL", "CALL_TO_ADVENTURE", "MEETING_MENTOR"]
```

---

### arc_completeness

**Method**: `_measure_transformation_arc(story_ctx, delta144_timeline)`

**Scoring rubric**:
- **0.0-0.3**: Early stages (ORDINARY_WORLD, REFUSAL_OF_CALL)
- **0.4-0.6**: Middle stages (ORDEAL, REWARD) but incomplete
- **0.7-1.0**: Late stages (RESURRECTION, RETURN_WITH_ELIXIR)

**Δ144 boost**:
- +0.15 if evolution from early archetypes (INNOCENT, HERO) to mature (SAGE, CREATOR)
- +0.08 if only mature archetype present

---

### temporal_coherence

**Method**: `_compute_temporal_coherence(story_ctx)`

**Logic**:
1. Use `story_ctx.coherence.overall` if object
2. Else use `story_ctx.coherence` if float
3. Fallback: 0.5 (default moderate coherence)

**Example**:
```python
# If coherence is CoherenceScore object with .overall attribute
coherence.overall = 0.85  # → temporal_coherence = 0.85
```

---

### drift_coupling

**Method**: `_compute_drift_coupling(drift_ctx, journey_sequence)`

**Logic**:
1. Extract `drift_ctx.turning_points`
2. Identify critical stages in sequence: ORDEAL, RESURRECTION, RETURN_WITH_ELIXIR, CROSSING_THRESHOLD
3. Heuristic: if critical stages present + turning points exist → coupling = min(len(turning_points) / 3.0, 1.0)

**TODO v3.3**: Use actual timestamp matching between turning_points and story events

---

### delta144_alignment

**Method**: `_compute_delta144_alignment(delta144_timeline, journey_sequence)`

**Expected pairings** (heuristic):
- CALL_TO_ADVENTURE → A04_HERO, A05_EXPLORER
- MEETING_MENTOR → A02_SAGE, A06_CAREGIVER
- ORDEAL → A04_HERO, A08_REBEL
- RESURRECTION → A04_HERO, A01_CREATOR
- RETURN_WITH_ELIXIR → A02_SAGE, A01_CREATOR, A06_CAREGIVER

**Scoring**: (matches / total_checks) where checks are critical stages in sequence

---

## Integration Points

### analyze() Method Flow

```python
def analyze(meta_input: MetaInput) -> CampbellSignal:
    # 1. v3.1 snapshot analysis (unchanged)
    signal = build_snapshot_signal(...)
    
    # 2. v3.2 temporal enrichment (additive)
    try:
        if meta_input.story_ctx or meta_input.drift_ctx:
            # Extract contexts
            story_ctx = meta_input.story_ctx
            drift_ctx = meta_input.drift_ctx
            delta144_timeline = story_ctx.metadata.get("delta144_timeline")
            
            # Compute temporal metrics
            signal.journey_sequence = _infer_journey_sequence(story_ctx)
            signal.temporal_coherence = _compute_coherence(story_ctx)
            signal.arc_completeness = _measure_arc(story_ctx, delta144_timeline)
            signal.drift_coupling = _compute_coupling(drift_ctx, journey_sequence)
            signal.delta144_alignment = _compute_alignment(delta144_timeline, journey_sequence)
    except Exception as e:
        logging.warning(f"Temporal enrichment failed: {e}")
        
    return signal
```

---

### Backward Compatibility

**v3.1 usage** (no changes required):
```python
input = MetaInput(text="...", delta144_state="A04_HERO")
signal = CampbellEngine().analyze(input)
# Works identically to v3.1
# signal.journey_sequence == []
# signal.temporal_coherence == 0.0
```

**v3.2 usage**:
```python
input = MetaInput(
    text="...",
    story_ctx=StoryContext(...),
    drift_ctx=DriftContext(...)
)
signal = CampbellEngine().analyze(input)
# All temporal fields populated
```

---

### MetaStage Consumption (Future v3.3)

**Planned usage**:
```python
class MetaStage:
    def _integrate_campbell(self, signal: CampbellSignal):
        # Use temporal fields for richer meta-analysis
        if signal.arc_completeness > 0.8:
            # Near journey completion - expect transformation
            self.boost_transformation_weight()
            
        if signal.drift_coupling > 0.6:
            # Drift aligns with journey - systemic coherence
            self.increase_coherence_confidence()
```

---

## Limitations

### v3.2 Constraints

1. **Heuristic algorithms**: Not ML-based
   - **Impact**: Metrics may not generalize to all narrative types
   - **Mitigation**: Calibration via domain-specific thresholds in v3.3

2. **Fixed thresholds**: 
   - Arc completeness stage ranges (0.2/0.5/0.9)
   - Journey sequence score > 0.1
   - **Mitigation**: Make configurable in v3.3

3. **Simplified drift coupling**: No actual timestamp matching yet
   - **Impact**: May miss misaligned turning points
   - **Mitigation**: Implement proper time-window matching in v3.3

4. **Expected archetype pairs**: Hardcoded heuristics
   - **Impact**: May not reflect all narrative traditions
   - **Mitigation**: Learn from data or allow custom mappings in v3.4

5. **Coherence fallback**: Returns 0.5 as default
   - **Impact**: Loss of signal when StoryContext incomplete
   - **Mitigation**: Implement stage-sequence coherence checking in v3.3

---

## Testing

### Test Coverage

**File**: `tests/meta/test_campbell_engine_temporal.py` (14 tests)

1. **Backward Compatibility** (2 tests):
   - ✅ v3.1-style input works unchanged
   - ✅ All fields clamped to [0, 1]

2. **Journey Sequence** (2 tests):
   - ✅ Extracts from arc.stage_scores
   - ✅ Empty sequence without story_ctx

3. **Arc Completeness** (3 tests):
   - ✅ Early stage → low completeness (<0.4)
   - ✅ Late stage → high completeness (>0.7)
   - ✅ Δ144 evolution boosts score (+0.15)

4. **Temporal Coherence** (2 tests):
   - ✅ Uses CoherenceScore.overall
   - ✅ Handles float coherence directly

5. **Drift Coupling** (2 tests):
   - ✅ High coupling with critical stages + turning points
   - ✅ Low coupling without critical stages

6. **Δ144 Alignment** (1 test):
   - ✅ Matches archetypes to expected stages

7. **Graceful Degradation** (2 tests):
   - ✅ Partial contexts don't crash
   - ✅ Malformed story_ctx logs warning, doesn't raise

**Backward Compatibility Tests**: `tests/meta/test_campbell_engine.py` (9 tests)
- ✅ All existing v3.1 tests pass unchanged

**Total**: 23/23 tests passing

---

## Next Steps

### Immediate (v3.2 Deployment)

1. Deploy to staging
2. Collect real temporal signals from KALDRA-Alpha
3. Calibrate arc_completeness thresholds per domain

### v3.3 Roadmap

1. **Timestamp-based drift coupling**: Match turning_point.timestamp with story event timestamps
2. **Adaptive thresholds**: Learn arc_completeness ranges from historical data
3. **Stage sequence coherence**: Penalize illogical jumps (e.g., CALL → RETURN without ORDEAL)
4. **Causality tracking**: Extend with "why did regime change at this journey stage?"

### v3.4+ Vision

1. **ML-based stage prediction**: Forecast next journey stage from trajectory
2. **Multi-meta-engine correlation**: Cross-reference Campbell + Nietzsche + Aurelius temporal signals
3. **Custom narrative templates**: Allow domain-specific journey definitions beyond monomyth
4. **Predictive arc completeness**: Estimate if journey will reach completion based on current trajectory

---

## Acknowledgments

This enhancement builds upon:
- **Story Engine Phase 1**: StoryBuffer, TimelineBuilder, ArcDetector, CoherenceScorer
- **TW369 v3.2**: DriftContext with trajectory + turning_points
- **CampbellEngine v3.1**: Snapshot-based stage detection with Δ144 + Kindra + TW369 integration
