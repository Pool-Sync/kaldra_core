# KALDRA v3.x — High-Level Roadmap (v3.1–v3.5)

**Date:** November 30, 2025  
**Status:** PLANNING  
**Foundation:** v3.0 Unification Layer (COMPLETE)

---

## Vision

Transform KALDRA from a **unified engine** (v3.0) into a **cognitive intelligence system** (v3.5) through systematic deepening of:
1. **Semantic Intelligence** (Kindra)
2. **Temporal Intelligence** (Story, TW369)
3. **Philosophical Intelligence** (Meta Engines)
4. **Multi-Modal Intelligence** (Input/Output)
5. **Application Intelligence** (Apps Convergence)

**Guiding Principle:**
> **Grow UP, not sideways.** Every version deepens intelligence within the unified architecture.

---

## Version Overview Table

| Version | Codename | Focus | Key Deliverables | Timeline |
|---------|----------|-------|------------------|----------|
| **v3.1** | **Exoskeleton** | Meta + Kindra | 3 Meta Engines, Kindra 3×48, Presets | Q1 2026 |
| **v3.2** | **Temporal Mind** | Story + TW369 | Story Buffer, Arc Detection, Drift Topology | Q2 2026 |
| **v3.3** | **Multi-Stream** | Input Enhancement | Multi-modal input, Parallel narratives | Q3 2026 |
| **v3.4** | **Explainable** | Output Enhancement | NL Explanations, Confidence breakdown | Q4 2026 |
| **v3.5** | **Convergence** | Apps + Learning | Apps 2.0, Learned mappings, Production | Q1 2027 |

---

## v3.1 — Exoskeleton

**Codename:** "The Philosophical Layer"  
**Timeline:** Q1 2026  
**Status:** PLANNING

### Objective

Add **philosophical depth** and **semantic intelligence** to the unified engine, creating an "exoskeleton" of preset modes and profiles that expose KALDRA's intelligence through the 4iam.ai frontend.

### Core Deliverables

#### 1. Meta Engines (3 Philosophical Lenses) ⭐⭐⭐⭐⭐

**Nietzsche Engine:**
- Will to Power detection
- Master/Slave morality classification
- Eternal Return pattern matching
- Übermensch transcendence markers

**Aurelius Engine:**
- Dichotomy of Control analysis
- Virtue Ethics scoring (Wisdom, Courage, Justice, Temperance)
- Memento Mori urgency detection
- Amor Fati acceptance measurement

**Campbell Engine:**
- Hero's Journey stage identification
- Archetypal role mapping (Hero, Mentor, Shadow, Ally)
- Transformation arc measurement
- Mythic resonance scoring

**Integration:**
- Implement in `src/meta/` (nietzsche_engine.py, aurelius_engine.py, campbell_engine.py)
- Register in `ModuleRegistry`
- Activate in `MetaStage`
- Populate `MetaContext` with real signals

---

#### 2. Kindra 3×48 Full Integration ⭐⭐⭐⭐⭐

**Layer 1: Cultural/Macro (16 dimensions)**
- Geopolitical stance
- Economic ideology
- Cultural values
- Temporal orientation

**Layer 2: Semiotic/Media (16 dimensions)**
- Narrative framing
- Rhetorical devices
- Emotional tone
- Information density

**Layer 3: Archetypal/Micro (16 dimensions)**
- Character archetypes
- Relational dynamics
- Psychological depth
- Symbolic resonance

**Integration:**
- Implement `src/kindras/kindra_engine.py` (unified)
- Connect to LLM scoring (OpenAI/local)
- Integrate into `CoreStage`
- Populate `KindraContext` with 3×48 scores

---

#### 3. Exoskeleton Layer (Presets & Profiles)

**Purpose:**
Create a **configuration layer** that exposes KALDRA through preset modes and user profiles.

**Presets:**
```python
# Alpha Mode (Financial Analysis)
alpha_preset = {
    "mode": "full",
    "emphasis": ["kindra.layer1", "story", "meta.nietzsche"],
    "thresholds": {"risk": 0.3},
    "output_format": "financial_brief"
}

# Geo Mode (Geopolitical Analysis)
geo_preset = {
    "mode": "story",
    "emphasis": ["kindra.layer1", "drift", "meta.aurelius"],
    "thresholds": {"risk": 0.4},
    "output_format": "geopolitical_brief"
}

# Safeguard Mode (Safety-First)
safeguard_preset = {
    "mode": "safety-first",
    "emphasis": ["safeguard", "tau", "bias"],
    "thresholds": {"risk": 0.2},
    "output_format": "safety_report"
}

# Product Mode (Brand/Marketing)
product_preset = {
    "mode": "full",
    "emphasis": ["kindra.layer2", "meta.campbell", "polarities"],
    "thresholds": {"risk": 0.35},
    "output_format": "brand_brief"
}
```

**Implementation:**
- Create `src/unification/exoskeleton/` directory
- `presets.py` - Preset definitions
- `profiles.py` - User profile management
- `preset_router.py` - Route based on preset
- Integrate with `UnifiedRouter`

---

#### 4. Frontend Integration (4iam.ai)

**API Enhancements:**
```python
# New endpoint
POST /api/v3/analyze
{
  "text": "...",
  "preset": "alpha",  # or "geo", "safeguard", "product"
  "user_profile": "analyst_001"
}

# Response includes preset-specific formatting
{
  "version": "3.1",
  "preset": "alpha",
  "meta": {
    "nietzsche": {...},  # NEW
    "aurelius": {...},   # NEW
    "campbell": {...}    # NEW
  },
  "kindra": {
    "layer1": {...},  # FULL 16 dims
    "layer2": {...},  # FULL 16 dims
    "layer3": {...}   # FULL 16 dims
  },
  ...
}
```

---

### Success Metrics

- ✅ 3 meta engines fully functional
- ✅ Kindra 3×48 scoring operational
- ✅ 4 presets (Alpha, Geo, Safeguard, Product) working
- ✅ Frontend integration complete
- ✅ All tests passing
- ✅ Documentation complete

---

## v3.2 — Temporal Mind

**Codename:** "The Memory Layer"  
**Timeline:** Q2 2026  
**Status:** FUTURE

### Objective

Add **temporal intelligence** through story buffer, narrative arc detection, and topological drift analysis.

### Core Deliverables

#### 1. Story Buffer & Timeline ⭐⭐⭐⭐⭐

**Story Buffer:**
- Persistent event storage
- Sliding window memory (configurable size)
- Event indexing and retrieval

**Archetypal Timeline:**
- Track archetype transitions over time
- Detect patterns and cycles
- Measure temporal coherence

**Narrative Arc Detection:**
- Identify story structure (Setup, Conflict, Resolution)
- Detect Hero's Journey stages
- Measure arc completeness

**Implementation:**
- `src/story/story_buffer.py` (enhanced)
- `src/story/timeline_builder.py` (new)
- `src/story/arc_detector.py` (new)
- `src/story/coherence_scorer.py` (new)
- Integrate into `StoryStage`

---

#### 2. TW369 Topological Deepening ⭐⭐⭐⭐

**Tracy-Widom Integration:**
- Use real TW statistics (already in v2.4)
- Regime-specific calibration
- CDF-based severity scoring

**Painlevé II Filtering:**
- Apply Painlevé filtering (already in v2.4)
- Regime-aware parameters
- Drift trajectory smoothing

**Drift Memory:**
- Persistent drift history (already in v2.4)
- Transition detection
- Regime change alerts

**Implementation:**
- Fully integrate existing v2.4 TW369 code
- Connect to `DriftContext`
- Enhance `CoreStage` with TW369 analysis

---

#### 3. Temporal Coherence Scoring

**Measure:**
- Consistency of archetype over time
- Smoothness of polarity transitions
- Narrative continuity

**Use Cases:**
- Detect narrative drift (Alpha App)
- Identify inconsistencies (Safeguard App)
- Track brand evolution (Product App)

---

### Success Metrics

- ✅ Story buffer operational with 1000+ event capacity
- ✅ Arc detection working on test narratives
- ✅ TW369 fully integrated
- ✅ Temporal coherence scoring functional
- ✅ Alpha/Geo apps using temporal intelligence

---

## v3.3 — Multi-Stream

**Codename:** "The Multi-Modal Layer"  
**Timeline:** Q3 2026  
**Status:** FUTURE

### Objective

Extend input beyond pure text to **multi-modal, multi-source, multi-stream** analysis.

### Core Deliverables

#### 1. Multi-Modal Input ⭐⭐⭐

**Enhanced InputContext:**
```python
@dataclass
class InputContext:
    # Core
    text: str
    embedding: np.ndarray
    
    # NEW: Metadata
    metadata: Dict[str, Any]  # Source, author, timestamp, etc.
    
    # NEW: Multi-source
    sources: List[str]  # Multiple versions/translations
    
    # NEW: Structured data
    structured_data: Optional[Dict]  # JSON, tables, code
    
    # Existing
    bias_score: float
    tau_input: TauState
```

**Use Cases:**
- Earnings reports + company metadata (Alpha)
- News articles + geolocation (Geo)
- Reviews + product metadata (Product)

---

#### 2. Multi-Stream Narratives ⭐⭐⭐

**Track Multiple Parallel Narratives:**
- Company narrative (Alpha)
- Sector narrative (Alpha)
- Regional narrative (Geo)
- Product narrative (Product)

**Cross-Stream Analysis:**
- Compare narratives
- Detect divergence
- Identify correlations

**Implementation:**
- `src/story/multi_stream_buffer.py`
- `src/story/stream_comparator.py`
- Enhanced `StoryContext`

---

#### 3. Ensemble Embeddings

**Support Multiple Models:**
- OpenAI (semantic)
- Sentence-Transformers (local)
- Domain-specific (financial, medical)

**Ensemble Strategy:**
- Weighted average
- Model selection based on input type
- Fallback chain

---

### Success Metrics

- ✅ Multi-modal input working
- ✅ Multi-stream narratives operational
- ✅ Ensemble embeddings functional
- ✅ Apps using enhanced input

---

## v3.4 — Explainable

**Codename:** "The Transparency Layer"  
**Timeline:** Q4 2026  
**Status:** FUTURE

### Objective

Make KALDRA **explainable** through natural language explanations and confidence breakdowns.

### Core Deliverables

#### 1. Natural Language Explanations ⭐⭐⭐

**Generate Explanations For:**
- "Why this archetype?"
- "What drove this risk score?"
- "How did the narrative evolve?"
- "What are the key polarities?"

**Implementation:**
- `src/explainability/explanation_generator.py`
- LLM-based explanation generation
- Template-based fallbacks
- Integrate into `OutputStage`

---

#### 2. Confidence Breakdown

**Detailed Confidence Scoring:**
- Per-stage confidence
- Per-module confidence
- Overall confidence with breakdown

**Visualization:**
- Confidence heatmap
- Decision tree
- Attribution scores

---

#### 3. Decision Tracing

**Track Decision Path:**
- Which stages executed
- Which modules contributed
- Which thresholds triggered
- Which fallbacks used

**Use Cases:**
- Debugging
- Auditing
- User trust

---

### Success Metrics

- ✅ NL explanations generated for all analyses
- ✅ Confidence breakdown available
- ✅ Decision tracing operational
- ✅ Frontend displaying explanations

---

## v3.5 — Convergence

**Codename:** "The Learning Layer"  
**Timeline:** Q1 2027  
**Status:** FUTURE

### Objective

**Converge** all intelligence layers into production-ready apps with learning capabilities.

### Core Deliverables

#### 1. Apps 2.0 (Redesigned)

**Alpha App 2.0:**
- Full Kindra 3×48 integration
- Temporal earnings narrative tracking
- Multi-stream company/sector analysis
- Nietzschean power dynamics

**Geo App 2.0:**
- Geopolitical narrative tracking
- Regional drift detection
- Stoic crisis analysis
- Multi-source news aggregation

**Product App 2.0:**
- Brand narrative evolution
- Campbell's Hero's Journey for products
- Multi-stream review analysis
- Sentiment trajectory

**Safeguard App 2.0:**
- Advanced risk detection
- Mitigation action engine
- Adaptive thresholds
- Real-time monitoring

---

#### 2. Learned Mappings ⭐⭐⭐

**Δ144 Learned Mapping:**
- Train neural network: embedding → archetype/state
- Use historical data
- Fine-tune per domain

**Kindra Learned Weights:**
- Learn optimal weights for 3×48 dimensions
- Domain-specific calibration
- Continuous improvement

---

#### 3. Production Optimization

**Caching Layer:**
- Redis-based caching
- Embedding cache
- Signal cache

**Parallel Execution:**
- Parallel stage execution where possible
- Async processing
- Queue-based architecture

**Database Integration:**
- PostgreSQL for persistent storage
- TimescaleDB for temporal data
- Vector DB for embeddings

---

### Success Metrics

- ✅ 4 apps fully operational
- ✅ Learned mappings deployed
- ✅ Production infrastructure ready
- ✅ Performance targets met (<100ms for signal mode)
- ✅ Monitoring and observability complete

---

## v3.1 Exoskeleton — Detailed Planning

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EXOSKELETON LAYER (v3.1)                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Presets    │───▶│   Profiles   │───▶│ Preset Router│ │
│  │ (Alpha/Geo)  │    │ (User Prefs) │    │ (Config)     │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│                                                             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                UNIFICATION LAYER (v3.0)                     │
│  Kernel → Router → Orchestrator → Pipeline                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    ENHANCED STAGES (v3.1)                   │
│  Input → Core (+ Kindra 3×48) → Meta (+ 3 Engines) →       │
│  Story → Safeguard → Output                                 │
└─────────────────────────────────────────────────────────────┘
```

---

### Exoskeleton Functions

#### 1. Preset Management

**Purpose:** Expose KALDRA through domain-specific configurations

**Interface:**
```python
from src.unification.exoskeleton import PresetManager

preset_mgr = PresetManager()

# Load preset
alpha_config = preset_mgr.get_preset("alpha")

# Apply preset
kaldra = UnifiedKaldra()
result = kaldra.analyze(text, preset="alpha")
```

---

#### 2. Profile Management

**Purpose:** Manage user-specific preferences and history

**Interface:**
```python
from src.unification.exoskeleton import ProfileManager

profile_mgr = ProfileManager()

# Create profile
profile = profile_mgr.create_profile(
    user_id="analyst_001",
    preferences={
        "risk_tolerance": 0.3,
        "preferred_preset": "alpha",
        "output_format": "detailed"
    }
)

# Use profile
result = kaldra.analyze(text, profile=profile)
```

---

#### 3. Frontend Integration

**4iam.ai API Endpoints:**

```
POST /api/v3.1/analyze
- Body: {text, preset, profile}
- Returns: Enhanced signal with meta + kindra

GET /api/v3.1/presets
- Returns: Available presets

GET /api/v3.1/profile/{user_id}
- Returns: User profile

PUT /api/v3.1/profile/{user_id}
- Body: {preferences}
- Updates: User profile
```

---

### Implementation Phases (v3.1)

#### Phase 1: Meta Engines (Weeks 1-4)
1. Implement Nietzsche Engine
2. Implement Aurelius Engine
3. Implement Campbell Engine
4. Integrate into MetaStage
5. Test and validate

#### Phase 2: Kindra 3×48 (Weeks 5-8)
1. Implement unified Kindra engine
2. Connect to LLM scoring
3. Integrate into CoreStage
4. Calibrate weights
5. Test and validate

#### Phase 3: Exoskeleton (Weeks 9-12)
1. Implement preset system
2. Implement profile system
3. Create 4 presets (Alpha, Geo, Safeguard, Product)
4. Integrate with router
5. Test and validate

#### Phase 4: Frontend (Weeks 13-16)
1. Update API endpoints
2. Integrate with 4iam.ai
3. Create UI for presets
4. Create UI for profiles
5. End-to-end testing

---

## Conclusion

The KALDRA v3.x roadmap provides a **clear path** from unified engine (v3.0) to cognitive intelligence system (v3.5):

- **v3.1 Exoskeleton** - Philosophical + Semantic depth
- **v3.2 Temporal Mind** - Temporal intelligence
- **v3.3 Multi-Stream** - Multi-modal input
- **v3.4 Explainable** - Transparency
- **v3.5 Convergence** - Production apps + learning

**Next Step:** Begin v3.1 Exoskeleton implementation after user approval.

---

**The roadmap is clear. The priorities are set. The future is intelligent.** 🚀
