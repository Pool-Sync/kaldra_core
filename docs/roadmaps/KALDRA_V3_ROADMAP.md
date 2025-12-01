# KALDRA v3.x — Master Roadmap (REBUILT)

**Version:** 3.x Series (v3.1–v3.5)  
**Date:** December 1, 2025  
**Status:** ACTIVE PLANNING  
**Rebuild:** Complete roadmap reconstruction with all corrections

---

## Executive Summary

The KALDRA v3.x roadmap transforms the unified engine (v3.0) into a **cognitive intelligence system** (v3.5) through systematic deepening across five dimensions:

1. **Philosophical Intelligence** (Meta Engines) — v3.1
2. **Semantic Intelligence** (Kindra 3×48) — v3.1
3. **Temporal Intelligence** (Story + TW369) — v3.2
4. **Multi-Modal Intelligence** (Input/Output) — v3.3–v3.4
5. **Application Intelligence** (Apps Convergence) — v3.5

**Guiding Principle:**
> **Grow UP, not sideways.** Every version deepens intelligence within the unified architecture.

---

## Critical Corrections in This Rebuild

### ✅ 1. Kindra 3×48 Accuracy
**OLD (INCORRECT):**
- Described as "3 layers × 16 dimensions" = 48 total

**NEW (CORRECT):**
- **3 layers × 48 vectors = 144 total vectors**
- Each layer has exactly 48 distinct vectors
- "16 dimensions" are conceptual groupings for UI/resonance, NOT the vector count
- Files: `kindra_vectors_layer{1,2,3}_*.json` each contain 48 entries

**Impact:** Major - affects all Kindra integration planning

---

### ✅ 2. Campbell Engine Archetype Normalization
**OLD (INCORRECT):**
- Used non-canonical archetypes: A03_WARRIOR, A12_CREATOR, A05_SEEKER, A11_JESTER

**NEW (CORRECT):**
- Normalized to Δ144 canonical set:
  - A03_WARRIOR → **A04_HERO**
  - A12_CREATOR → **A01_CREATOR**
  - A05_SEEKER → **A05_EXPLORER**
  - A11_JESTER → **A11_TRICKSTER**

**Impact:** Critical - ensures Campbell aligns with Δ144 vocabulary

---

### ✅ 3. Story Timeline Integration Clarity
**OLD (AMBIGUOUS):**
- Unclear when Story Stage becomes operational

**NEW (CLEAR):**
- **v3.1:** Story Stage remains **placeholder**
- **v3.2:** Full Story implementation:
  - StoryBuffer with persistent events
  - TimelineBuilder for archetypal transitions
  - ArcDetector for narrative structure
  - CoherenceScorer for temporal consistency
  - **CampbellEngine v3.2** uses StoryContext

**Impact:** High - clarifies dependencies and timeline

---

### ✅ 4. TW369 Topological Deepening
**OLD (INCOMPLETE):**
- Mentioned TW369 but lacked detail

**NEW (COMPLETE):**
- **drift_metric** - Numerical drift measure
- **regime** - Current archetypal regime
- **volatility** - Regime stability measure
- **trajectory** - Historical drift path
- **turning_points** - Regime transition markers
- **Painlevé II smoothing** - Trajectory filtering
- **Tracy-Widom severity** - Statistical significance
- **Persistent drift history** - Sliding window memory

**Impact:** High - enables true temporal intelligence

---

### ✅ 5. Multi-Stream Narratives Placement
**OLD (INCORRECT):**
- Multi-stream mentioned in v3.2

**NEW (CORRECT):**
- Multi-stream moved to **v3.3 ONLY**
- Clear separation: v3.2 = single-stream temporal, v3.3 = multi-stream

**Impact:** Medium - better version scoping

---

## Version Overview

| Version | Codename | Focus | Timeline | Status |
|---------|----------|-------|----------|--------|
| **v3.0** | **Unification Layer** | Unified API + Pipeline | COMPLETE | ✅ |
| **v3.1** | **Exoskeleton** | Meta + Kindra + Presets | Q1 2026 | PLANNING |
| **v3.2** | **Temporal Mind** | Story + TW369 Topology | Q2 2026 | FUTURE |
| **v3.3** | **Multi-Stream** | Multi-modal + Multi-stream | Q3 2026 | FUTURE |
| **v3.4** | **Explainable** | NL Explanations + Transparency | Q4 2026 | FUTURE |
| **v3.5** | **Convergence** | Apps 2.0 + Learned Mappings | Q1 2027 | FUTURE |

---

## v3.1 — Exoskeleton

**Codename:** "The Philosophical Layer"  
**Timeline:** Q1 2026 (16 weeks)  
**Status:** PLANNING

### Objective

Add **philosophical depth** and **semantic intelligence** through:
1. Three meta engines (Nietzsche, Aurelius, Campbell)
2. Full Kindra 3×48 integration (144 vectors)
3. Preset/Profile system (Exoskeleton)
4. Frontend integration (4iam.ai)

### Core Deliverables

#### 1. Meta Engines ⭐⭐⭐⭐⭐

**NietzscheEngine** (Integrate & Refine)
- Already exists in `src/meta/nietzsche_engine.py`
- Refine integration with Kindra 3×48
- Add TW369 basic integration
- Output: MetaSignal with Will to Power, Morality Type, Eternal Return, Transcendence

**AureliusEngine** (Integrate & Refine)
- Already exists in `src/meta/aurelius_engine.py`
- Refine integration with Kindra 3×48
- Add TW369 basic integration
- Output: MetaSignal with Dichotomy of Control, Virtue Ethics, Memento Mori, Amor Fati

**CampbellEngine v3.1** (NEW - Snapshot Mode)
- **NEW implementation** following MetaInput → MetaSignal pattern
- **Archetype normalization applied** (see correction #2)
- Snapshot analysis (no temporal context yet)
- Journey stage identification (static)
- Archetypal role mapping
- Integration with Kindra 3×48
- Integration with TW369 basic
- **Location:** `src/meta/campbell_engine.py`

**Normalized Campbell Archetypes:**
```python
CAMPBELL_ARCHETYPES = {
    "HERO": "A04_HERO",          # was A03_WARRIOR
    "MENTOR": "A02_SAGE",
    "THRESHOLD_GUARDIAN": "A07_RULER",
    "HERALD": "A05_EXPLORER",    # was A05_SEEKER
    "SHAPESHIFTER": "A03_MAGICIAN",
    "SHADOW": "A08_REBEL",
    "ALLY": "A06_CAREGIVER",
    "TRICKSTER": "A11_TRICKSTER", # was A11_JESTER
    "CREATOR": "A01_CREATOR",    # was A12_CREATOR
    "LOVER": "A09_LOVER",
    "INNOCENT": "A10_INNOCENT",
    "ORACLE": "A12_ORACLE"
}
```

---

#### 2. Kindra 3×48 Full Integration ⭐⭐⭐⭐⭐

**CORRECTED SPECIFICATION:**

**Layer 1: Cultural/Macro (48 vectors)**
- File: `kindra_vectors_layer1_cultural_macro_48.json`
- 48 distinct cultural/geopolitical/temporal vectors
- Conceptual groupings (for UI): Geopolitical, Economic, Cultural, Temporal (4×12 ≈ 16 concepts)

**Layer 2: Semiotic/Media (48 vectors)**
- File: `kindra_vectors_layer2_semiotic_media_48.json`
- 48 distinct narrative/rhetorical/emotional vectors
- Conceptual groupings: Narrative, Rhetorical, Emotional, Information (4×12 ≈ 16 concepts)

**Layer 3: Structural/Systemic (48 vectors)**
- File: `kindra_vectors_layer3_structural_systemic_48.json`
- 48 distinct archetypal/relational/symbolic vectors
- Conceptual groupings: Archetypal, Relational, Psychological, Symbolic (4×12 ≈ 16 concepts)

**Total:** 3 × 48 = **144 vectors**

**Implementation:**
```python
@dataclass
class KindraContext:
    layer1: Dict[str, float]  # 48 scores
    layer2: Dict[str, float]  # 48 scores
    layer3: Dict[str, float]  # 48 scores
    tw_plane_distribution: Dict[str, float]  # {"3": 0.33, "6": 0.33, "9": 0.34}
    
    def get_total_vectors(self) -> int:
        return len(self.layer1) + len(self.layer2) + len(self.layer3)  # = 144
```

**Kindra → Δ144 Maps:**
- Already normalized (see `tools/fix_kindra_maps.py`)
- All 3 maps use canonical Δ144 archetypes
- 48 entries per map
- Tests: `tests/test_kindra_maps_alignment.py` (3/3 passing)

---

#### 3. Exoskeleton Layer (Presets & Profiles)

**Presets:**
```python
PRESETS = {
    "alpha": {
        "mode": "full",
        "emphasis": ["kindra.layer1", "story", "meta.nietzsche"],
        "thresholds": {"risk": 0.3},
        "output_format": "financial_brief"
    },
    "geo": {
        "mode": "story",
        "emphasis": ["kindra.layer1", "drift", "meta.aurelius"],
        "thresholds": {"risk": 0.4},
        "output_format": "geopolitical_brief"
    },
    "safeguard": {
        "mode": "safety-first",
        "emphasis": ["safeguard", "tau", "bias"],
        "thresholds": {"risk": 0.2},
        "output_format": "safety_report"
    },
    "product": {
        "mode": "full",
        "emphasis": ["kindra.layer2", "meta.campbell", "polarities"],
        "thresholds": {"risk": 0.35},
        "output_format": "brand_brief"
    }
}
```

**Implementation:**
- `src/unification/exoskeleton/presets.py`
- `src/unification/exoskeleton/profiles.py`
- `src/unification/exoskeleton/preset_router.py`

---

#### 4. Frontend Integration (4iam.ai)

**API Endpoints:**
```
POST /api/v3.1/analyze
GET /api/v3.1/presets
GET /api/v3.1/profile/{user_id}
PUT /api/v3.1/profile/{user_id}
```

**Enhanced Signal:**
```json
{
  "version": "3.1",
  "preset": "alpha",
  "meta": {
    "nietzsche": {...},
    "aurelius": {...},
    "campbell": {...}
  },
  "kindra": {
    "layer1": {...},  // 48 scores
    "layer2": {...},  // 48 scores
    "layer3": {...},  // 48 scores
    "total_vectors": 144
  }
}
```

---

### Success Metrics (v3.1)

- ✅ 3 meta engines operational
- ✅ Kindra 3×48 (144 vectors) scoring functional
- ✅ 4 presets working (Alpha, Geo, Safeguard, Product)
- ✅ Frontend integration complete
- ✅ All tests passing
- ✅ Documentation complete

---

## v3.2 — Temporal Mind

**Codename:** "The Memory Layer"  
**Timeline:** Q2 2026 (16 weeks)  
**Status:** FUTURE

### Objective

Add **temporal intelligence** through:
1. Story Buffer & Timeline
2. TW369 Topological Deepening
3. Campbell Engine v3.2 (Temporal)
4. Temporal Coherence Scoring

### Core Deliverables

#### 1. Story Engine ⭐⭐⭐⭐⭐

**StoryBuffer:**
- Persistent event storage (1000+ events)
- Sliding window memory
- Event indexing by archetype, time, polarity

**TimelineBuilder:**
- Track archetype transitions
- Detect patterns and cycles
- Measure temporal coherence

**ArcDetector:**
- Identify narrative structure (Setup, Conflict, Resolution)
- Detect Hero's Journey stages
- Measure arc completeness

**CoherenceScorer:**
- Consistency of archetype over time
- Smoothness of polarity transitions
- Narrative continuity

**Implementation:**
```python
@dataclass
class StoryContext:
    events: List[StoryEvent]  # Historical events
    arc: Optional[NarrativeArc]  # Detected arc
    timeline: Optional[ArchetypalTimeline]  # Archetype transitions
    coherence: float  # Temporal coherence [0, 1]
    turning_points: List[TurningPoint]  # Key transitions
```

---

#### 2. TW369 Topological Deepening ⭐⭐⭐⭐

**Enhanced DriftContext:**
```python
@dataclass
class DriftContext:
    tw_state: TWState
    drift_state: DriftState
    regime: str  # Current archetypal regime
    drift_metric: float  # Numerical drift measure
    volatility: float  # Regime stability
    trajectory: List[DriftPoint]  # Historical path
    turning_points: List[TurningPoint]  # Regime transitions
    painleve_smoothed: bool  # Painlevé II applied
    tracy_widom_severity: float  # Statistical significance
```

**Painlevé II Smoothing:**
- Apply to drift trajectory
- Regime-aware parameters
- Reduce noise while preserving transitions

**Tracy-Widom Severity:**
- Use real TW statistics (from v2.4)
- Regime-specific calibration
- CDF-based severity scoring

**Persistent Drift History:**
- Sliding window (configurable size)
- Transition detection
- Regime change alerts

---

#### 3. CampbellEngine v3.2 (Temporal) ⭐⭐⭐⭐

**NEW FEATURES:**
- **StoryContext integration** - Read full event timeline
- **Transformation arc** - Measure character growth over time
- **Journey sequence detection** - Identify multi-stage progression
- **TW369 trajectory integration** - Correlate drift with journey stages
- **Δ144 timeline integration** - Map archetypes to journey roles

**Enhanced Output:**
```python
@dataclass
class CampbellSignal(MetaSignal):
    journey_stage: str  # Current stage
    journey_sequence: List[str]  # Historical progression
    transformation_arc: float  # Growth measure [0, 1]
    archetypal_roles: Dict[str, str]  # Δ144 → Campbell mapping
    mythic_resonance: float
    temporal_coherence: float  # NEW - journey consistency
```

---

#### 4. Temporal Coherence Scoring

**Measures:**
- Archetype consistency over time
- Polarity transition smoothness
- Narrative continuity
- Journey progression logic

**Use Cases:**
- Detect narrative drift (Alpha App)
- Identify inconsistencies (Safeguard App)
- Track brand evolution (Product App)

---

### Success Metrics (v3.2)

- ✅ Story buffer operational (1000+ events)
- ✅ Arc detection working
- ✅ TW369 fully integrated with topology
- ✅ Campbell v3.2 temporal analysis functional
- ✅ Temporal coherence scoring operational
- ✅ Alpha/Geo apps using temporal intelligence

---

## v3.3 — Multi-Stream

**Codename:** "The Multi-Modal Layer"  
**Timeline:** Q3 2026 (12 weeks)  
**Status:** FUTURE

### Objective

Extend to **multi-modal, multi-source, multi-stream** analysis.

### Core Deliverables

#### 1. Multi-Modal Input ⭐⭐⭐

**Enhanced InputContext:**
```python
@dataclass
class InputContext:
    text: str
    embedding: np.ndarray
    metadata: Dict[str, Any]  # NEW - source, author, timestamp
    sources: List[str]  # NEW - multiple versions
    structured_data: Optional[Dict]  # NEW - JSON, tables, code
    bias_score: float
    tau_input: TauState
```

---

#### 2. Multi-Stream Narratives ⭐⭐⭐

**Stream-Aware StoryEvent:**
```python
@dataclass
class StoryEvent:
    timestamp: float
    text: str
    archetype: Archetype
    polarities: Dict[str, float]
    stream_id: str  # NEW - "company", "sector", "region", etc.
```

**Cross-Stream Analysis:**
- Compare narratives (company vs sector)
- Detect divergence (Kindra, Δ144, TW-regime)
- Identify correlations

**Implementation:**
- `src/story/multi_stream_buffer.py`
- `src/story/stream_comparator.py`

---

#### 3. Ensemble Embeddings

**Multiple Models:**
- OpenAI (semantic)
- Sentence-Transformers (local)
- Domain-specific (financial, medical)

**Ensemble Strategy:**
- Weighted average
- Model selection by input type
- Fallback chain

---

### Success Metrics (v3.3)

- ✅ Multi-modal input working
- ✅ Multi-stream narratives operational
- ✅ Ensemble embeddings functional
- ✅ Apps using enhanced input

---

## v3.4 — Explainable

**Codename:** "The Transparency Layer"  
**Timeline:** Q4 2026 (12 weeks)  
**Status:** FUTURE

### Objective

Make KALDRA **explainable** through NL explanations and transparency.

### Core Deliverables

#### 1. Natural Language Explanations ⭐⭐⭐

**Generate Explanations:**
- "Why this archetype?"
- "What drove this risk score?"
- "How did the narrative evolve?"
- "What are the key polarities?"

**Implementation:**
- `src/explainability/explanation_generator.py`
- LLM-based generation
- Template fallbacks

---

#### 2. Confidence Breakdown

**Detailed Scoring:**
- Per-stage confidence
- Per-module confidence
- Overall confidence with breakdown

---

#### 3. Decision Tracing

**Track:**
- Which stages executed
- Which modules contributed
- Which thresholds triggered
- Which fallbacks used

---

#### 4. Multi-Format Output

**Formats:**
- JSON (current)
- Markdown (human-readable)
- GraphQL (flexible queries)
- Protobuf (high-performance)

---

### Success Metrics (v3.4)

- ✅ NL explanations for all analyses
- ✅ Confidence breakdown available
- ✅ Decision tracing operational
- ✅ Multi-format output working

---

## v3.5 — Convergence

**Codename:** "The Learning Layer"  
**Timeline:** Q1 2027 (16 weeks)  
**Status:** FUTURE

### Objective

**Converge** all layers into production apps with learning.

### Core Deliverables

#### 1. Apps 2.0

**Alpha App 2.0:**
- Full Kindra 3×48
- Temporal earnings narratives
- Multi-stream (company/sector)
- Nietzschean power dynamics

**Geo App 2.0:**
- Geopolitical narrative tracking
- Regional drift detection
- Stoic crisis analysis
- Multi-source aggregation

**Product App 2.0:**
- Brand narrative evolution
- Campbell's Hero's Journey
- Multi-stream reviews
- Sentiment trajectory

**Safeguard App 2.0:**
- Advanced risk detection
- Mitigation actions
- Adaptive thresholds
- Real-time monitoring

---

#### 2. Learned Mappings ⭐⭐⭐

**Δ144 Learned Mapping:**
- Train: embedding → archetype/state
- **MUST use normalized Kindra→Δ144 priors**
- Fine-tune per domain
- Continuous improvement

**Kindra Learned Weights:**
- Learn optimal weights for 144 vectors
- Domain-specific calibration

---

#### 3. Production Optimization

**Caching:**
- Redis-based
- Embedding cache
- Signal cache

**Parallel Execution:**
- Async processing
- Queue-based

**Database:**
- PostgreSQL (persistent)
- TimescaleDB (temporal)
- Vector DB (embeddings)

---

### Success Metrics (v3.5)

- ✅ 4 apps fully operational
- ✅ Learned mappings deployed
- ✅ Production infrastructure ready
- ✅ Performance targets met (<100ms signal mode)

---

## Implementation Phases

### Phase 1: Foundation (v3.0) ✅ COMPLETE
- Unified API
- Modular pipeline
- 5 v2.9 engines loaded

### Phase 2: Intelligence (v3.1) 🔄 PLANNING
- Meta engines
- Kindra 3×48
- Presets/Profiles

### Phase 3: Memory (v3.2) 📅 FUTURE
- Story engine
- TW369 topology
- Temporal coherence

### Phase 4: Multi-Modal (v3.3) 📅 FUTURE
- Multi-input
- Multi-stream
- Ensemble embeddings

### Phase 5: Transparency (v3.4) 📅 FUTURE
- NL explanations
- Confidence breakdown
- Multi-format output

### Phase 6: Production (v3.5) 📅 FUTURE
- Apps 2.0
- Learned mappings
- Production optimization

---

## Known Limitations

### v3.1
- Story Stage remains placeholder
- Campbell v3.1 is snapshot-only (no temporal)

### v3.2
- No multi-stream until v3.3
- Campbell temporal requires Story Timeline

### v3.3–v3.4
- No learned mappings until v3.5

### v3.5
- Δ144 remains heuristic until learned model deployed

---

## Testing Strategy

### v3.1
- Meta engines unit tests
- Kindra 3×48 integration tests
- Preset/Profile tests
- End-to-end v3.1 tests

### v3.2
- Story buffer tests
- TW369 topology tests
- Campbell temporal tests
- Temporal coherence tests

### v3.3
- Multi-stream tests
- Ensemble embedding tests
- Divergence detection tests

### v3.4
- Explanation generation tests
- Confidence breakdown tests
- Multi-format output tests

### v3.5
- Learned mapping tests
- Production performance tests
- Apps integration tests

---

## Conclusion

The KALDRA v3.x roadmap provides a **clear, corrected path** from unified engine to cognitive intelligence system:

- **v3.1 Exoskeleton** - Philosophical + Semantic depth (Meta + Kindra 3×48)
- **v3.2 Temporal Mind** - Temporal intelligence (Story + TW369 topology)
- **v3.3 Multi-Stream** - Multi-modal input
- **v3.4 Explainable** - Transparency
- **v3.5 Convergence** - Production apps + learning

**All critical corrections applied. The roadmap is rebuilt. The path is clear.** 🚀

---

**Next:** Generate version-specific documents (v3.1–v3.5)
