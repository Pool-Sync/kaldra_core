# KALDRA Core — Master Roadmap v2.3–v2.9

**Last Updated**: 2025-11-29  
**Status**: v2.8 COMPLETE ✅

---

## Version Status

- ✅ **v2.3** — Real Intelligence Injection (COMPLETE)
- ✅ **v2.4** — Mathematical Deepening & Drift Memory (COMPLETE)
- ✅ **v2.5** — Meta-Engine Soul & Routing (COMPLETE)
- ✅ **v2.6** — Story Aggregation & Narrative Arcs (COMPLETE)
- ✅ **v2.7** — Axes & Masks (COMPLETE)
- ✅ **v2.8** — The Guardian Layer (COMPLETE)
- 🔄 **v2.9** — Hardening & Performance (PLANNED)

---

## Overview
Este arquivo será preenchido pelo Pool (ChatGPT) com base no relatório de auditoria v2.2 e no plano de evolução dos motores (Δ12/Δ144, Kindra 3×48, TW369, Painlevé, Tracy-Widom, Meta-Engines, Tau, Bias, Apps).

## v2.3 — Real Intelligence Injection ✅ COMPLETE

**Goal**: Replace simulation stubs with real AI capabilities (LLM, Embeddings, Bias Detection) while maintaining legacy fallbacks.

### 2.3.1 LLM Client Integration ✅
- **Objective**: Inject a real LLM client into `KindraLLMScorer`.
- **Files**: `src/kindras/scoring/llm_client_base.py`, `src/kindras/scoring/llm_openai_client.py`, `src/kindras/kindra_llm_scorer.py`.
- **Acceptance**:
    - [x] `KindraLLMScorer` accepts `llm_client` injection.
    - [x] Configurable via `KALDRA_LLM_PROVIDER` (default: dummy).
    - [x] Tests pass with both dummy and mocked real client.

### 2.3.2 Semantic Embeddings ✅
- **Objective**: Replace random-seed embeddings with real semantic vectors.
- **Files**: `src/core/embedding_generator.py`, `src/archetypes/delta144_engine.py`.
- **Acceptance**:
    - [x] `EmbeddingGenerator` supports `REAL` (OpenAI/Local) and `LEGACY` modes.
    - [x] `Delta144Engine` uses the generator instead of internal RNG.
    - [x] Configurable via `KALDRA_EMBEDDINGS_MODE`.

### 2.3.3 Bias Engine Activation ✅
- **Objective**: Activate real bias detection providers.
- **Files**: `src/bias/detector.py`, `src/bias/providers/perspective_provider.py`.
- **Acceptance**:
    - [x] `BiasDetector` supports provider injection.
    - [x] Implementation of Perspective API provider.
    - [x] Fallback to heuristic if provider fails or is unconfigured.

### v2.3 Results
- ✅ **LLM real integrado ao Kindra** - OpenAI API support with dummy fallback
- ✅ **Δ144 usando embeddings semânticos reais** - EmbeddingGenerator with legacy/openai/sentence-transformers providers
- ✅ **Bias Engine com provider real** - Perspective API integration with heuristic fallback
- ✅ **14/14 tests passing** - All v2.3 features fully tested and verified




## v2.4 — Mathematical Deepening (TW369 & Painlevé) ✅ COMPLETE

**Goal**: Transform TW369 from heuristic approximations to mathematically rigorous implementations with drift memory and Δ12/Δ144 integration.

### 2.4.1 Tracy-Widom Real Statistics Layer ✅
- **Objective**: Replace heuristic severity factor with real Tracy-Widom distribution.
- **Files**:
  - `schema/tw369/tracy_widom_lookup.json` (NEW)
  - `schema/tw369/tw_parameters.json` (NEW)
  - `src/tw369/tracy_widom.py` (NEW)
  - `src/tw369/tw369_integration.py` (MODIFIED)
- **Acceptance**:
  - [x] TW lookup table covers β=1,2,4 with 0.01 precision
  - [x] `_compute_severity_factor` uses real TW CDF (with legacy fallback)
  - [x] Configurable TW parameters via schema

### 2.4.2 Painlevé II Calibration ✅
- **Objective**: Make Painlevé solver configurable and regime-aware.
- **Files**:
  - `schema/tw369/painleve_config.json` (NEW)
  - `schema/tw369/regime_calibration.json` (NEW)
  - `src/tw369/painleve/painleve2_solver.py` (MODIFIED)
  - `src/tw369/config_loader.py` (NEW)
- **Acceptance**:
  - [x] All Painlevé parameters configurable via schema
  - [x] Regime-specific calibration for 12 archetypes
  - [x] `build_default_solver()` function with schema loading

### 2.4.3 Drift Memory & State Persistence ✅
- **Objective**: Implement persistent drift state with sliding window memory.
- **Files**:
  - `schema/tw369/drift_state_schema.json` (NEW)
  - `src/tw369/drift_state.py` (NEW)
  - `src/tw369/drift_memory.py` (NEW)
  - `src/tw369/tw369_integration.py` (MODIFIED)
- **Acceptance**:
  - [x] `DriftState` fully serializable to JSON
  - [x] Sliding window memory (configurable size)
  - [x] Integrated into TW369 flow (non-blocking)
  - [x] `get_drift_history()` accessor function

### 2.4.4 Δ12/Δ144 Integration ✅
- **Objective**: Explicit coupling between archetypal layers and TW369.
- **Files**:
  - `schema/tw369/archetype_regimes.json` (NEW)
  - `src/archetypes/delta12_vector.py` (NEW)
  - `src/archetypes/delta144_engine.py` (MODIFIED)
  - `src/tw369/regime_utils.py` (NEW)
- **Acceptance**:
  - [x] Delta12Vector class with normalization
  - [x] `compute_delta12()` in Delta144Engine
  - [x] Regime utilities for TW369 coupling

### v2.4 Results
- ✅ **Tracy-Widom real statistics** - Lookup tables + legacy fallback
- ✅ **Painlevé schema-driven** - Configurable solver with regime calibration
- ✅ **Drift memory active** - Non-blocking tracking in TW369
- ✅ **Δ12 explicit** - compute_delta12() projects plane scores to archetypes
- ✅ **10/10 tests passing** - All v2.4 features tested and verified
- ✅ **100% backward compatible** - All features optional, v2.3 behavior preserved

## v2.5 — Meta-Engine "Soul" & Routing ✅ COMPLETE

**Goal**: Deep philosophical meta-analysis through Nietzschean, Stoic, and Campbellian lenses for intelligent routing and narrative understanding.

### 2.5.1 NietzscheEngine-12 ✅
- **Objective**: 12-dimensional Nietzschean analysis
- **Files**:
  - `src/meta/nietzsche.py` (REFACTORED)
  - `tests/meta/test_nietzsche_engine.py` (UPDATED)
- **Acceptance**:
  - [x] 12 axes implemented (will to power, resentment, life affirmation/negation, nihilism, dionysian/apollonian, amor fati, etc.)
  - [x] Keyword-based heuristics for each axis
  - [x] Archetype and TW369 adjustments
  - [x] analyze_meta() unified interface
  - [x] 9/9 tests passing

### 2.5.2 AureliusEngine-12 ✅
- **Objective**: 12-dimensional Stoic analysis
- **Files**:
  - `src/meta/aurelius.py` (REFACTORED)
  - `tests/meta/test_aurelius_engine.py` (UPDATED)
- **Acceptance**:
  - [x] 12 Stoic axes implemented (perception clarity, emotional regulation, control dichotomy, serenity, etc.)
  - [x] Anti-pattern penalties (reactivity, excess)
  - [x] Archetype, TW369, and bias adjustments
  - [x] Stoic alignment calculation
  - [x] 12/12 tests passing

### 2.5.3 CampbellEngine - Hero's Journey ✅
- **Objective**: 12-stage Hero's Journey detection
- **Files**:
  - `src/meta/campbell.py` (CREATED)
  - `tests/meta/test_campbell_engine.py` (CREATED)
- **Acceptance**:
  - [x] 12 canonical stages defined
  - [x] Stage detection using Δ144, DriftMemory, TWState
  - [x] Drift pattern and archetype analysis
  - [x] 5/5 tests passing

### 2.5.4 MetaRouter & Routing ✅
- **Objective**: Orchestration and intelligent app routing
- **Files**:
  - `src/meta/meta_router.py` (CREATED)
  - `tests/meta/test_meta_router_routing.py` (CREATED)
- **Acceptance**:
  - [x] MetaRouter orchestrates all engines
  - [x] RoutingDecision with reasoning
  - [x] Routing heuristics (Ordeal→Safeguard, Will to Power→Alpha, etc.)
  - [x] 5/5 tests passing

### v2.5 Results
- ✅ **NietzscheEngine-12** - Deep philosophical analysis with 12 axes
- ✅ **AureliusEngine-12** - Stoic analysis with 12 dimensions
- ✅ **CampbellEngine** - Hero's Journey stage detection
- ✅ **MetaRouter** - Intelligent routing based on meta-signals
- ✅ **31/31 tests passing** - All meta-engines tested and verified
- ✅ **100% backward compatible** - All features optional, no breaking changes
- ✅ **Documentation complete** - Release notes and technical guides
## v2.6 — Story Aggregation & Narrative Arcs
- ✅ **v2.6 Results**: ✅ COMPLETE
- 26/26 tests passing (100%)
- 6 core components (StoryBuffer, Aggregator, NarrativeArc, Timeline, TW369 Temporal, StorySignal)
- 5 comprehensive documentation files
- 100% backward compatible
- Transforms KALDRA into temporal narrative engine

---

## v2.7 — Polarities & Modifiers Integration 🔄

**Codename**: Axes & Masks  
**Status**: IN PROGRESS  
**Start Date**: 2025-11-28

### 2.7.1 Core Types & Loading 🔄
- **Objective**: Make polarities first-class citizens
- **Files**:
  - `src/archetypes/delta144_engine.py` (MODIFY)
  - `docs/archetypes/POLARITIES_MODIFIERS_V2.7_SPEC.md` (CREATED)
### 2.7.1 Core Types & Schema ✅
- **Objective**: Define 46 Polarities and 59 Modifiers
- **Files**:
  - `src/archetypes/polarity_mapping.py` (CREATE)
  - `src/archetypes/delta12_vector.py` (MODIFY)
- **Acceptance**:
  - [x] Polarity dataclass implemented
  - [x] load_polarities() function working
  - [x] Delta144Engine loads 46 polarities
  - [x] Modifiers loading reviewed and stable

### 2.7.2 Modifier Auto-Inference ✅
- **Objective**: Auto-infer modifiers from embeddings
- **Files**:
  - `src/archetypes/delta144_engine.py` (MODIFY)
  - `tests/archetypes/test_modifier_inference.py` (CREATE)
- **Acceptance**:
  - [x] infer_modifier_scores_from_embedding() implemented
  - [x] Integration with v2.3 EmbeddingGenerator
  - [x] Auto-inference when modifier_scores not provided
  - [x] Tests passing

### 2.7.3 Polarity Extraction from Meta-Engines ✅
- **Objective**: Map meta-engine outputs to polarity scores
- **Files**:
  - `src/archetypes/polarity_mapping.py` (CREATE)
  - `src/meta/meta_router.py` (MODIFY)
  - `tests/meta/test_polarity_mapping.py` (CREATE)
- **Acceptance**:
  - [x] extract_polarity_scores() implemented
  - [x] Nietzsche/Aurelius/Campbell mappings defined
  - [x] MetaRouter wired with polarity extraction
  - [x] Tests passing

### 2.7.4 Δ12 & TW369 Modulation ✅
- **Objective**: Polarity-aware modulation layers
- **Files**:
  - `src/archetypes/delta12_vector.py` (MODIFY)
  - `src/tw369/tw369_integration.py` (MODIFY)
  - `src/config.py` (MODIFY)
  - `tests/tw369/test_tw369_modulation.py` (CREATE)
- **Acceptance**:
  - [x] apply_polarities_to_delta12() implemented
  - [x] modulate_tw_severity_with_polarities() implemented
  - [x] Feature flags added (default: OFF)
  - [x] Bounded, safe modulation
  - [x] Tests passing

### 2.7.5 Story Engine Integration ✅
- **Objective**: Track polarity/modifier evolution
- **Files**:
  - `src/story/story_buffer.py` (MODIFY)
  - `src/story/story_aggregator.py` (MODIFY)
  - `schema/story/story_signal.schema.json` (MODIFY)
  - `tests/story/test_story_polarity.py` (CREATE)
- **Acceptance**:
  - [x] StoryEvent has polarity_scores and active_modifiers
  - [x] detect_polarity_oscillations() implemented
  - [x] StorySignal schema extended
  - [x] Tests passing

### 2.7.6 Documentation & Release ✅
- **Files**:
  - `docs/KALDRA_V2.7_RELEASE_NOTES.md` (CREATE)
  - `CHANGELOG.md` (UPDATE)
- **Acceptance**:
  - [x] Complete release notes
  - [x] CHANGELOG entry
  - [x] Roadmap updated
  - [x] All v2.3-v2.6 tests still passing

**v2.7 Goals**:
- Activate 46 polarities across pipeline
- Auto-infer 59 modifiers from embeddings
- Extract polarities from meta-engines
- Modulate Δ12 and TW369 with polarities
- Track polarity swings in Story Engine
- 100% backward compatible

---

## v2.8 — The Guardian Layer ✅ COMPLETE

**Codename**: The Guardian Layer  
**Status**: COMPLETE  
**Completion Date**: 2025-11-29

### 2.8.1 Tau Layer (Epistemic Limiter v2) ✅
- **Objective**: Dual-phase epistemic reliability system
- **Files**:
  - `src/tau/tau_layer.py` (CREATED)
  - `src/tau/tau_risk_model.py` (CREATED)
  - `src/tau/tau_policy.py` (CREATED)
  - `docs/tau/TAU_LAYER_SPEC.md` (CREATED)
- **Acceptance**:
  - [x] Tau Score calculation (sigmoid of weighted risks)
  - [x] Input Phase (pre-inference) modulation
  - [x] Output Phase (post-inference) analysis
  - [x] Dynamic modifiers (drift damping, archetype smoothing)
  - [x] Tests passing

### 2.8.2 Safeguard Engine ✅
- **Objective**: Narrative safety and risk mitigation
- **Files**:
  - `src/safeguard/safeguard_engine.py` (CREATED)
  - `src/safeguard/safeguard_risk_model.py` (CREATED)
  - `docs/safeguard/SAFEGUARD_ENGINE_SPEC.md` (CREATED)
- **Acceptance**:
  - [x] Risk Taxonomy (Toxicity, Manipulation, etc.)
  - [x] Mitigation Policies (Block, Dampen, Flag)
  - [x] Integration with Tau, TW369, and Meta-Engines
  - [x] Tests passing

### 2.8.3 Pipeline Integration ✅
- **Objective**: Full integration into Master Engine
- **Files**:
  - `src/core/kaldra_master_engine.py` (MODIFIED)
  - `src/tw369/tw369_integration.py` (MODIFIED)
  - `src/archetypes/delta144_engine.py` (MODIFIED)
- **Acceptance**:
  - [x] Master Engine orchestrates Tau Input -> Core -> Tau Output -> Safeguard
  - [x] TW369 accepts drift damping
  - [x] Delta144 accepts archetype smoothing
  - [x] KaldraSignal includes Tau and Safeguard data

### v2.8 Results
- ✅ **Tau Layer Active** - Epistemic precision control
- ✅ **Safeguard Engine Active** - Safety and ethics enforcement
- ✅ **Pipeline Hardened** - Dynamic modulation of internal engines
- ✅ **Tests Passing** - Unit and integration tests verified
- ✅ **Documentation Complete** - Specs and Release Notes created

---

## v2.9 — Hardening & Performance (PLANNED)

> NÃO editar este stub com detalhes agora. O preenchimento completo será feito em próxima task.
