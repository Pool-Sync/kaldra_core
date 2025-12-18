# KALDRA v3.x — Engine Expansion Points

**Version:** 3.x Planning  
**Date:** November 30, 2025  
**Status:** PLANNING

---

## Executive Summary

The KALDRA v3.0 Unification Layer provides a **solid, modular foundation** for engine expansion. This document maps the natural expansion points across the pipeline, identifying where deepening intelligence will have maximum impact.

**Current State (v3.0):**
- ✅ Unified API (`UnifiedKaldra.analyze()`)
- ✅ 6 modular pipeline stages
- ✅ 5 v2.9 engines loaded (embeddings, archetypes, bias, tau, safeguard)
- ✅ Graceful degradation
- ✅ Multiple execution modes

**Expansion Philosophy:**
> **Grow UP, not sideways.** Deepen intelligence within the unified architecture, never bypass it.

---

## 1. Current v3.0 Capabilities

### What Works Today

**Pipeline Flow:**
```
Input → Core → Meta → Story → Safeguard → Output
```

**Loaded Engines:**
1. **Embeddings** (v2.3) - Semantic vectors (OpenAI/local)
2. **Archetypes** (v2.7) - Δ12, Δ144, 46 polarities
3. **Bias** (v2.3) - Bias detection (Perspective API/heuristic)
4. **Tau** (v2.8) - Epistemic reliability limiter
5. **Safeguard** (v2.8) - Risk evaluation and mitigation

**Execution Modes:**
- `signal` - Fast (4 stages, ~100ms)
- `full` - Complete (6 stages, ~300ms)
- `story` - Temporal (6 stages, ~400ms)
- `safety-first` - Strict safety (6 stages, ~350ms)
- `exploratory` - Maximum depth (6 stages, ~500ms)

---

## 2. Expansion Points by Stage

### Stage 1: Input Stage

**Current Implementation:**
- Bias detection (basic)
- Tau input phase (epistemic risk)
- Embedding generation (single model)

**Expansion Points:**

#### 2.1.1 Multi-Input Modalities ⭐⭐⭐
**Impact:** HIGH | **Complexity:** MEDIUM

**Description:**
Extend input beyond pure text to include:
- **Metadata** - Source, author, timestamp, context
- **Multi-text** - Compare multiple versions/translations
- **Structured data** - JSON, tables, code

**Implementation:**
```python
# Enhanced InputContext
@dataclass
class InputContext:
    text: str
    metadata: Dict[str, Any]  # NEW
    sources: List[str]  # NEW (multi-source)
    structured_data: Optional[Dict]  # NEW
    embedding: np.ndarray
    bias_score: float
    tau_input: TauState
```

**Use Cases:**
- Alpha App: Earnings reports + metadata (company, sector, date)
- Geo App: News articles + geolocation + source credibility
- Product App: Reviews + product metadata + sentiment history

---

#### 2.1.2 Multi-Model Embeddings ⭐⭐
**Impact:** MEDIUM | **Complexity:** LOW

**Description:**
Support multiple embedding models simultaneously:
- OpenAI (semantic)
- Sentence-Transformers (local)
- Domain-specific models (financial, medical, etc.)

**Implementation:**
- Ensemble embeddings (weighted average)
- Model selection based on input type
- Fallback chain for reliability

---

#### 2.1.3 Input Classification ⭐⭐
**Impact:** MEDIUM | **Complexity:** LOW

**Description:**
Pre-classify input type to optimize pipeline:
- Narrative vs. analytical
- Emotional vs. factual
- Short-form vs. long-form

**Benefit:**
- Route to appropriate stages
- Skip irrelevant analysis
- Optimize performance

---

### Stage 2: Core Stage

**Current Implementation:**
- Δ144 state inference (working)
- Δ12 projection (basic)
- Kindra 3×48 (placeholder)
- TW369 drift (basic)

**Expansion Points:**

#### 2.2.1 Kindra 3×48 Full Integration ⭐⭐⭐⭐⭐
**Impact:** CRITICAL | **Complexity:** HIGH

**Description:**
Complete the Kindra 3×48 scoring system:
- **Layer 1:** Cultural/Macro (16 dimensions)
- **Layer 2:** Semiotic/Media (16 dimensions)
- **Layer 3:** Archetypal/Micro (16 dimensions)

**Current Gap:**
- Kindra is mentioned but not fully integrated
- No real 3×48 scoring in pipeline
- Missing LLM-based scoring

**Implementation:**
```python
# In CoreStage
kindra_scores = self.kindra_engine.score_all_layers(
    text=text,
    embedding=embedding,
    delta12=delta12,
    polarities=polarities
)

kindra_ctx = KindraContext(
    layer1=kindra_scores['layer1'],  # 16 dims
    layer2=kindra_scores['layer2'],  # 16 dims
    layer3=kindra_scores['layer3']   # 16 dims
)
```

**Impact:**
- **Massive** - Kindra is the semantic intelligence layer
- Enables deep cultural/semiotic analysis
- Foundation for Alpha/Geo/Product apps

---

#### 2.2.2 TW369 Topological Deepening ⭐⭐⭐⭐
**Impact:** HIGH | **Complexity:** HIGH

**Description:**
Enhance TW369 from basic drift to full topological analysis:
- **Tracy-Widom statistics** (already in v2.4, needs integration)
- **Painlevé II filtering** (already in v2.4, needs integration)
- **Drift memory** (already in v2.4, needs integration)
- **Regime detection** (archetypal transitions)

**Current Gap:**
- TW369 exists in v2.9 but barely used in v3.0
- DriftContext is mostly empty
- No temporal coherence tracking

**Implementation:**
```python
# In CoreStage
tw_result = self.tw369_engine.analyze(
    embedding=embedding,
    archetype=delta144_state.archetype,
    history=drift_memory.get_history()
)

drift_ctx = DriftContext(
    tw_state=tw_result.tw_state,
    drift_state=tw_result.drift_state,
    regime=tw_result.regime,
    drift_metric=tw_result.drift_metric,
    trajectory=tw_result.trajectory  # NEW
)
```

**Impact:**
- Temporal intelligence
- Detect archetypal transitions
- Predict narrative drift

---

#### 2.2.3 Δ144 Learned Mapping ⭐⭐⭐
**Impact:** MEDIUM-HIGH | **Complexity:** VERY HIGH

**Description:**
Replace heuristic Δ144 inference with learned mapping:
- Train neural network: embedding → archetype/state
- Use historical data for calibration
- Fine-tune per domain (finance, news, etc.)

**Current Gap:**
- Δ144 uses geometric/heuristic mapping
- No learning from feedback
- No domain adaptation

**Benefit:**
- Higher accuracy
- Domain-specific intelligence
- Continuous improvement

---

### Stage 3: Meta Stage

**Current Implementation:**
- Placeholder only
- No real meta engines

**Expansion Points:**

#### 2.3.1 Nietzsche Engine ⭐⭐⭐⭐
**Impact:** HIGH | **Complexity:** MEDIUM

**Description:**
Implement Nietzschean analysis:
- **Will to Power** - Detect power dynamics
- **Master/Slave Morality** - Identify value systems
- **Eternal Return** - Cyclical patterns
- **Übermensch** - Transcendence markers

**Implementation:**
```python
class NietzscheEngine:
    def analyze(self, text, archetypes, polarities):
        return MetaSignal(
            will_to_power=self._detect_power_dynamics(text),
            morality_type=self._classify_morality(text),
            eternal_return=self._detect_cycles(archetypes),
            transcendence=self._measure_transcendence(polarities)
        )
```

**Use Cases:**
- Political discourse analysis
- Leadership assessment
- Cultural critique

---

#### 2.3.2 Aurelius Engine ⭐⭐⭐
**Impact:** MEDIUM-HIGH | **Complexity:** MEDIUM

**Description:**
Implement Stoic analysis:
- **Dichotomy of Control** - What's controllable vs. not
- **Virtue Ethics** - Wisdom, courage, justice, temperance
- **Memento Mori** - Urgency and mortality awareness
- **Amor Fati** - Acceptance of fate

**Use Cases:**
- Personal development content
- Crisis communication
- Resilience assessment

---

#### 2.3.3 Campbell Engine ⭐⭐⭐⭐
**Impact:** HIGH | **Complexity:** MEDIUM

**Description:**
Implement Hero's Journey analysis:
- **Journey Stage** - Identify current stage (Call, Threshold, Ordeal, Return)
- **Archetypal Roles** - Hero, Mentor, Shadow, Ally
- **Transformation** - Measure character growth
- **Mythic Resonance** - Universal pattern matching

**Implementation:**
```python
class CampbellEngine:
    def analyze(self, text, story_ctx, archetypes):
        return MetaSignal(
            journey_stage=self._identify_stage(text, story_ctx),
            archetypal_roles=self._map_roles(archetypes),
            transformation_arc=self._measure_transformation(story_ctx),
            mythic_resonance=self._compute_resonance(text)
        )
```

**Use Cases:**
- Story analysis (Alpha App)
- Brand narrative (Product App)
- Leadership journey (Geo App)

---

### Stage 4: Story Stage

**Current Implementation:**
- Placeholder only
- Skipped in `signal` mode

**Expansion Points:**

#### 2.4.1 Story Buffer & Timeline ⭐⭐⭐⭐⭐
**Impact:** CRITICAL | **Complexity:** HIGH

**Description:**
Implement full temporal analysis:
- **Story Buffer** - Maintain event history
- **Archetypal Timeline** - Track archetype transitions
- **Narrative Arc Detection** - Identify story structure
- **Coherence Scoring** - Measure temporal consistency

**Current Gap:**
- No temporal memory
- No arc detection
- No coherence measurement

**Implementation:**
```python
class StoryStage:
    def execute(self, context):
        # Add event to buffer
        event = StoryEvent(
            timestamp=now,
            text=context.input_ctx.text,
            archetype=context.archetype_ctx.delta144_state.archetype,
            polarities=context.archetype_ctx.polarity_scores
        )
        self.story_buffer.add(event)
        
        # Detect arc
        arc = self.arc_detector.detect(self.story_buffer.get_events())
        
        # Build timeline
        timeline = self.timeline_builder.build(
            events=self.story_buffer.get_events(),
            archetypes=context.archetype_ctx
        )
        
        # Compute coherence
        coherence = self.coherence_scorer.score(timeline)
        
        return StoryContext(
            events=self.story_buffer.get_events(),
            arc=arc,
            timeline=timeline,
            coherence=coherence
        )
```

**Impact:**
- **Massive** - Enables true temporal intelligence
- Foundation for Alpha App (earnings narratives)
- Foundation for Geo App (geopolitical arcs)

---

#### 2.4.2 Multi-Stream Narratives ⭐⭐⭐
**Impact:** MEDIUM-HIGH | **Complexity:** HIGH

**Description:**
Track multiple parallel narratives:
- **Company narrative** (Alpha App)
- **Sector narrative** (Alpha App)
- **Regional narrative** (Geo App)
- **Product narrative** (Product App)

**Benefit:**
- Compare narratives
- Detect divergence
- Cross-narrative insights

---

### Stage 5: Safeguard Stage

**Current Implementation:**
- Tau output phase (working)
- Safeguard evaluation (working)
- Risk consolidation (working)

**Expansion Points:**

#### 2.5.1 Adaptive Risk Thresholds ⭐⭐⭐
**Impact:** MEDIUM-HIGH | **Complexity:** MEDIUM

**Description:**
Make risk thresholds context-aware:
- **Domain-specific** - Finance vs. news vs. social
- **User-specific** - Risk tolerance profiles
- **Temporal** - Adjust based on drift history

**Current Gap:**
- Fixed thresholds
- No context adaptation
- No user profiles

---

#### 2.5.2 Mitigation Action Engine ⭐⭐
**Impact:** MEDIUM | **Complexity:** MEDIUM

**Description:**
Generate actionable mitigation strategies:
- **Reframing suggestions**
- **Alternative perspectives**
- **Risk-aware rewrites**

**Benefit:**
- Not just detection, but correction
- Proactive safety
- User guidance

---

### Stage 6: Output Stage

**Current Implementation:**
- Signal assembly (working)
- Confidence calculation (basic)
- JSON formatting (working)

**Expansion Points:**

#### 2.6.1 Multi-Format Output ⭐⭐
**Impact:** MEDIUM | **Complexity:** LOW

**Description:**
Support multiple output formats:
- **JSON** (current)
- **Markdown** (human-readable)
- **GraphQL** (flexible queries)
- **Protobuf** (high-performance)

---

#### 2.6.2 Explanation Generation ⭐⭐⭐
**Impact:** MEDIUM-HIGH | **Complexity:** MEDIUM

**Description:**
Generate natural language explanations:
- **Why this archetype?**
- **What drove this risk score?**
- **How did the narrative evolve?**

**Benefit:**
- Transparency
- User trust
- Debugging

---

## 3. Expansion Point Ranking

### Top 10 by Impact × Feasibility

| Rank | Expansion Point | Impact | Complexity | ROI | Version |
|------|----------------|--------|------------|-----|---------|
| 1 | **Kindra 3×48 Full Integration** | ⭐⭐⭐⭐⭐ | HIGH | **CRITICAL** | v3.1 |
| 2 | **Story Buffer & Timeline** | ⭐⭐⭐⭐⭐ | HIGH | **CRITICAL** | v3.2 |
| 3 | **TW369 Topological Deepening** | ⭐⭐⭐⭐ | HIGH | **HIGH** | v3.2 |
| 4 | **Campbell Engine** | ⭐⭐⭐⭐ | MEDIUM | **HIGH** | v3.1 |
| 5 | **Nietzsche Engine** | ⭐⭐⭐⭐ | MEDIUM | **HIGH** | v3.1 |
| 6 | **Multi-Input Modalities** | ⭐⭐⭐ | MEDIUM | **MEDIUM-HIGH** | v3.3 |
| 7 | **Aurelius Engine** | ⭐⭐⭐ | MEDIUM | **MEDIUM-HIGH** | v3.1 |
| 8 | **Explanation Generation** | ⭐⭐⭐ | MEDIUM | **MEDIUM** | v3.4 |
| 9 | **Δ144 Learned Mapping** | ⭐⭐⭐ | VERY HIGH | **MEDIUM** | v3.5 |
| 10 | **Multi-Stream Narratives** | ⭐⭐⭐ | HIGH | **MEDIUM** | v3.3 |

---

## 4. Strategic Priorities

### Phase 1: Intelligence Depth (v3.1)
**Focus:** Meta engines + Kindra

**Rationale:**
- Meta engines (Nietzsche, Aurelius, Campbell) add philosophical depth
- Kindra 3×48 adds semantic/cultural intelligence
- Both are **foundational** for apps

**Deliverables:**
- 3 meta engines fully implemented
- Kindra 3×48 integrated into CoreStage
- Enhanced MetaContext and KindraContext

---

### Phase 2: Temporal Intelligence (v3.2)
**Focus:** Story + TW369

**Rationale:**
- Story buffer enables narrative tracking
- TW369 enables drift detection
- Both are **critical** for Alpha/Geo apps

**Deliverables:**
- Story buffer with arc detection
- TW369 topological analysis
- Temporal coherence scoring

---

### Phase 3: Multi-Modal Input (v3.3)
**Focus:** Input enhancement

**Rationale:**
- Real-world data is multi-modal
- Metadata is crucial for context
- Enables richer analysis

**Deliverables:**
- Multi-input support (text + metadata + structured)
- Multi-stream narratives
- Enhanced InputContext

---

### Phase 4: Explainability (v3.4)
**Focus:** Output enhancement

**Rationale:**
- Users need to understand "why"
- Transparency builds trust
- Debugging requires explanations

**Deliverables:**
- Natural language explanations
- Confidence breakdown
- Decision tracing

---

### Phase 5: Learning & Optimization (v3.5)
**Focus:** Performance + learning

**Rationale:**
- Learned mappings improve accuracy
- Optimization enables scale
- Continuous improvement

**Deliverables:**
- Δ144 learned mapping
- Caching layer
- Performance optimization

---

## 5. Architectural Principles

### Principle 1: Never Bypass Unification
**All expansions MUST use the v3.0 architecture:**
- Register new modules in `ModuleRegistry`
- Integrate into existing stages (or create new ones)
- Use `UnifiedContext` for state
- Output via `SignalAdapter`

**Anti-pattern:**
```python
# ❌ WRONG - bypassing unification
from src.meta.nietzsche import NietzscheEngine
nietzsche = NietzscheEngine()
result = nietzsche.analyze(text)  # Direct call
```

**Correct pattern:**
```python
# ✅ CORRECT - using unification
kernel.registry.register("nietzsche", NietzscheEngine())
# Then use in MetaStage via registry
```

---

### Principle 2: Grow Stages, Don't Multiply Them
**Prefer deepening existing stages over creating new ones:**
- Input Stage → Multi-modal input
- Core Stage → Kindra, TW369
- Meta Stage → 3 meta engines
- Story Stage → Buffer, arcs, timeline

**Only create new stages if:**
- Fundamentally different responsibility
- Clear separation of concerns
- Doesn't fit existing stages

---

### Principle 3: Maintain Graceful Degradation
**Every expansion must handle failure gracefully:**
- Don't crash pipeline
- Return partial results
- Mark context as degraded
- Log errors clearly

---

### Principle 4: Optimize for Apps
**Every expansion should enable at least one app:**
- Kindra → Alpha, Geo, Product
- Story → Alpha, Geo
- Meta → All apps
- TW369 → Alpha, Geo

---

## 6. Conclusion

The v3.0 Unification Layer provides **10+ natural expansion points** across all 6 pipeline stages. The highest-impact expansions are:

1. **Kindra 3×48** - Semantic/cultural intelligence (v3.1)
2. **Story Buffer** - Temporal intelligence (v3.2)
3. **Meta Engines** - Philosophical depth (v3.1)
4. **TW369 Topological** - Drift intelligence (v3.2)

**Next Step:** Create detailed roadmap for v3.1-v3.5 based on these expansion points.

---

**The engine is unified. The expansion points are clear. The path forward is modular.** 🚀
