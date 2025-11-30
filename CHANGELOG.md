# Changelog
All notable changes to KALDRA Core will be documented in this file.

## [2.9.0] - 2025-11-30 — "Hardening & Performance"

### Added
- **Hardening Layer**: Timeouts, Retries, Circuit Breakers, Fallbacks.
- **Global Degraded Mode**: Master Engine resilience against catastrophic failures.
- **Profiling Suite**: `perf/` module for performance auditing.
- **Observability**: Structured logging and metrics hooks.
- **Test Suites**: Hardening, Chaos, and Performance tests.

### Changed
- **KaldraMasterEngineV2**: Wrapped in global exception handling.
- **EmbeddingGenerator**: Added circuit breakers for OpenAI/Cohere.
- **KindraLLMScorer**: Added retries and timeouts.
- **MetaRouter**: Added circuit breakers for engine evaluation.

---

## [2.8.0] - 2025-11-29 — "The Guardian Layer"

### Added
- **Tau Layer (Epistemic Limiter v2)**: Dual-phase reliability system.
  - `TauScore`: Dynamic confidence metric [0.0-1.0].
  - `TauRisk`: Risk classification (LOW, MID, HIGH, CRITICAL).
  - `Input Phase`: Pre-inference modulation of internal engines.
  - `Output Phase`: Post-inference stability analysis.
- **Safeguard Engine**: Narrative safety and ethics system.
  - Risk Taxonomy: Toxicity, Manipulation, Polarization, Extremism, Distortion, Shadow Loops.
  - Mitigation Policies: `CLAMP_DRIFT`, `SUPPRESS_POLARITY`, `BLOCK_OUTPUT`.
- **Pipeline Integration**:
  - `Drift Damping`: TW369 drift velocity modulated by Tau.
  - `Archetype Smoothing`: Δ144 probability distribution flattened by Tau.
  - `Signal Update`: `KaldraSignal` includes `tau` and `safeguard` blocks.

### Changed
- **KaldraMasterEngineV2**: Orchestrates the new Guardian Layer pipeline.
- **TW369Integrator**: Accepts external damping modifiers.
- **Delta144Engine**: Accepts external smoothing modifiers.

### Technical
- **New Modules**: `src/tau/`, `src/safeguard/`.
- **New Schemas**: `schema/tau/`, `schema/safeguard/`.
- **Testing**: Comprehensive unit and integration tests for new layers.

---

## [2.7.0] - 2025-11-29 — "Polarity Engine & Modifier Reintegration"

### Added
- **Polarity System**: 46-dimensional tension tracking across Cultural, Semiotic, and Structural planes.
- **Modifier Auto-Inference**: Embedding-based detection of archetype modifiers in `Delta144Engine`.
- **Meta-Engine Mapping**: `polarity_mapping` module to bridge Nietzsche/Aurelius/Campbell outputs to Polarities.
- **Story Engine Oscillations**: Detection of polarity inversions and narrative shifts in `StoryAggregator`.
- **Modulation Layers**:
  - **Δ12**: Archetype probabilities modulated by active polarities.
  - **TW369**: Drift severity modulated by polarity alignment.
- **Feature Flags**: `KALDRA_TW_POLARITY_ENABLED` and `KALDRA_DELTA12_POLARITY_ENABLED`.

### Changed
- **Delta144Engine**: Updated `infer_state` to accept `polarity_scores` and auto-infer modifiers.
- **Nietzsche/Aurelius Engines**: Standardized result serialization.
- **StoryEvent**: Added `polarity_scores` field for persistent storage.
- **API Adapter**: Exposed polarity and modifier data in standard response.

---

## [2.6.0] - 2025-11-28 — "The Narrative Spine"

### Added
- **Story Engine**: Complete temporal narrative intelligence system
  - `StoryBuffer`: Sliding window memory for narrative events (default: 12 events)
  - `StoryAggregator`: Motion vector computation, inflection detection, arc progression
  - `NarrativeArc`: Campbell-based arc tracking with prediction
  - `ArchetypalTimeline`: Δ12/Δ144 evolution tracking with curvature metrics
  - `TW369 Temporal Coherence`: Drift slope, acceleration, regime stability
- **StorySignal Format**: Extended JSON output with `story` block
- **Schemas**: `story_event.schema.json`, `story_signal.schema.json`

### Features
- Motion vectors between narrative states
- Inflection point detection (drift peaks, archetype shifts, stage transitions)
- Campbell stage prediction with transition likelihood
- Narrative tension computation
- Archetypal loop detection
- Drift trajectory analysis (slope, acceleration, volatility)
- Narrative oscillation index

### Technical
- 26 new tests (100% passing)
- 5 comprehensive documentation files
- Backward compatible (story features opt-in)
- In-memory buffer with full serialization

### Documentation
- `docs/story/STORY_ENGINE_SPEC.md`
- `docs/story/STORY_BUFFER.md`
- `docs/story/NARRATIVE_ARC_ENGINE.md`
- `docs/story/TIMELINE_ENGINE.md`
- `docs/story/STORY_SIGNAL_FORMAT.md`

---

## [2.5.0] — Meta-Engine Soul & Routing (2025-11-28)

### Added
- **NietzscheEngine-12**: 12-dimensional Nietzschean analysis (will to power, resentment, life affirmation/negation, nihilism, dionysian/apollonian, amor fati, etc.)
- **AureliusEngine-12**: 12-dimensional Stoic analysis (perception clarity, emotional regulation, control dichotomy, serenity, self-mastery, etc.)
- **CampbellEngine**: 12-stage Hero's Journey detection using Δ144, DriftMemory, and TWState
- **MetaRouter**: Orchestration and intelligent routing based on philosophical profiles
- **MetaEngineResult**: Unified result format with scores, dominant axes, severity, and notes

### Changed
- **Meta-engines**: Refactored from simple class-based heuristics to deep function-based 12-axis analysis
- **analyze_meta()**: New unified interface for Nietzsche and Aurelius engines
- **Routing logic**: Now uses 12-dimensional philosophical scores for app routing decisions

### Technical Details
- All v2.5 features are **optional** and **backward compatible**
- Meta-routing can be enabled via `KALDRA_META_ROUTING_ENABLED` flag (default: disabled)
- Keyword-based heuristics (no LLM dependency)
- Fail-safe design - meta-engine errors never break pipeline
- 31 tests passing (NietzscheEngine: 9, AureliusEngine: 12, CampbellEngine: 5, MetaRouter: 5)

## [2.4.0] — Mathematical Deepening & Drift Memory (2025-11-28)

### Added
- **Tracy-Widom Real Statistics**: Lookup tables for β=1,2,4 with real CDF calculations
- **Painlevé Configuration**: Schema-driven solver config with regime-specific calibration
- **DriftState & DriftMemory**: Persistent drift tracking with sliding window memory
- **Delta12Vector**: Explicit Δ12 representation with `compute_delta12()` in Delta144Engine
- **Regime Utilities**: TW369-Δ12 coupling for archetype-aware behavior

### Changed
- **TW369 severity calculation**: Now uses Tracy-Widom module (optional, with legacy fallback)
- **Painlevé solver**: Loads parameters from `schema/tw369/painleve_config.json`
- **Delta144Engine**: Added `compute_delta12()` method for explicit Δ12 projection
- **TW369 integration**: Tracks drift history in module-level DriftMemory

### Technical Details
- All v2.4 features are **optional** and **backward compatible**
- Tracy-Widom disabled by default (uses legacy heuristic)
- DriftMemory tracking is non-blocking (never fails drift calculation)
- Painlevé solver supports archetype-specific alpha calibration

## [2.3.0] — Real Intelligence Injection (2025-11-28)

### Added
- **LLM Client Integration**: `LLMClientBase`, `OpenAILLMClient`, and `DummyLLMClient` for Kindra LLM Scorer
- **Semantic Embeddings**: `EmbeddingGenerator` with providers (`legacy`, `openai`, `sentence-transformers`)
- **Bias Engine Providers**: Provider-based architecture (`BiasProvider`, `HeuristicProvider`, `PerspectiveProvider`)
- Environment variables for LLM (`KALDRA_LLM_PROVIDER`, `KALDRA_LLM_API_KEY`, `KALDRA_LLM_MODEL`)
- Environment variables for Embeddings (`KALDRA_EMBEDDINGS_MODE`, `KALDRA_EMBEDDINGS_API_KEY`, `KALDRA_EMBEDDINGS_MODEL`)
- Environment variables for Bias (`KALDRA_BIAS_PROVIDER`, `PERSPECTIVE_API_KEY`)

### Changed
- **Delta144Engine**: Now uses `EmbeddingGenerator` instead of internal RNG for state embeddings
- **BiasDetector**: Refactored to operate via injectable providers with heuristic fallback
- **KindraLLMScorer**: Updated to accept injected `LLMClientBase` instances

### Fixed
- Alignment between documentation and code for LLM Scoring, Δ144 Inference, and Bias Engine
- Eliminated "simulation debt" - all core AI components now support real API integration

### Documentation
- Updated `docs/math/KINDRA_LLM_SCORING.md` with v2.3 architecture
- Updated `docs/math/DELTA144_INFERENCE.md` with Semantic Embeddings section
- Updated `docs/core/BIAS_ENGINE_SPEC.md` with provider architecture
- Created `docs/core/TEST_SUITE_REPORT.md` for v2.3 test coverage

## [2.4.0] — Mathematical Deepening & Drift Memory (2025-11-28)

### Added
- **Tracy-Widom Real Statistics**: Lookup tables for β=1,2,4 with real CDF calculations
- **Painlevé Configuration**: Schema-driven solver config with regime-specific calibration
- **DriftState & DriftMemory**: Persistent drift tracking with sliding window memory
- **Delta12Vector**: Explicit Δ12 representation with `compute_delta12()` in Delta144Engine
- **Regime Utilities**: TW369-Δ12 coupling for archetype-aware behavior

### Changed
- **TW369 severity calculation**: Now uses Tracy-Widom module (optional, with legacy fallback)
- **Painlevé solver**: Loads parameters from `schema/tw369/painleve_config.json`
- **Delta144Engine**: Added `compute_delta12()` method for explicit Δ12 projection
- **TW369 integration**: Tracks drift history in module-level DriftMemory

### Technical Details
- All v2.4 features are **optional** and **backward compatible**
- Tracy-Widom disabled by default (uses legacy heuristic)
- DriftMemory tracking is non-blocking (never fails drift calculation)
- Painlevé solver supports archetype-specific alpha calibration

## [2.5.0] — Meta-Engine Soul & Routing (2025-11-28)

### Added
- **NietzscheEngine-12**: 12-dimensional Nietzschean analysis (will to power, resentment, life affirmation/negation, nihilism, dionysian/apollonian, amor fati, etc.)
- **AureliusEngine-12**: 12-dimensional Stoic analysis (perception clarity, emotional regulation, control dichotomy, serenity, self-mastery, etc.)
- **CampbellEngine**: 12-stage Hero's Journey detection using Δ144, DriftMemory, and TWState
- **MetaRouter**: Orchestration and intelligent routing based on philosophical profiles
- **MetaEngineResult**: Unified result format with scores, dominant axes, severity, and notes

### Changed
- **Meta-engines**: Refactored from simple class-based heuristics to deep function-based 12-axis analysis
- **analyze_meta()**: New unified interface for Nietzsche and Aurelius engines
- **Routing logic**: Now uses 12-dimensional philosophical scores for app routing decisions

### Technical Details
- All v2.5 features are **optional** and **backward compatible**
- Meta-routing can be enabled via `KALDRA_META_ROUTING_ENABLED` flag (default: disabled)
- Keyword-based heuristics (no LLM dependency)
- Fail-safe design - meta-engine errors never break pipeline
- 31 tests passing (NietzscheEngine: 9, AureliusEngine: 12, CampbellEngine: 5, MetaRouter: 5)

## [2.1.0] – 2025-11-28

### Frontend Deployment
- ✅ Deployed to Vercel (`https://4iam.ai`)
- ✅ Next.js 14 App Router with TypeScript
- ✅ Environment variables configured for production
- ✅ Fixed root directory configuration for Vercel build
- ✅ KALDRA Alpha dashboard operational

### API Gateway & Backend
- ✅ Full CORS configuration for production domains
  - `https://4iam.ai`
  - `https://www.4iam.ai`
  - `https://4iam-frontend.vercel.app`
  - Permissive regex for dev/preview environments
- ✅ FastAPI import fix (`Any` type in monitoring/metrics)
- ✅ Health check endpoint stable (`/health`)
- ✅ Deployed to Render with Docker
- ✅ Auto-deploy on main branch push

### Data Lab Workers
- ✅ News ingestion worker implementation
  - `kaldra_data/workers/news_ingest_worker.py`
  - `scripts/run_news_ingest.py`
- ✅ Mediastack and GNews API integration
- ✅ JSONL data storage pipeline
- ✅ Render cron job configuration (commented, ready to activate)

### Type System & Build Fixes
- ✅ Updated `KaldraTWRegime` type definition
- ✅ Fixed `kindra_distribution` structure (Object → Array)
- ✅ Fixed `narrative_risk` type (String → Number)
- ✅ Updated `KaldraSignalDistribution` component for array handling
- ✅ TW-Regime mock values updated for Vercel build compatibility

### Documentation
- ✅ `docs/ENV_REFERENCE_FRONTEND.md` - Frontend environment variables
- ✅ `docs/FRONTEND_STRUCTURE_CHECKLIST.md` - Structure validation
- ✅ `docs/DEPLOY_FRONTEND_VERCEL.md` - Deployment guide
- ✅ `docs/PRODUCTION_NOTES.md` - Production behavior notes
- ✅ `docs/DATALAB_WORKERS.md` - Worker implementation guide
- ✅ `docs/KALDRA_V2.1_RELEASE_NOTES.md` - Comprehensive release notes
- ✅ `docs/PRODUCTION_ARCHITECTURE_OVERVIEW.md` - System architecture
- ✅ `docs/KALDRA_CLOUD_ROADMAP.md` - Future development roadmap

### Infrastructure
- ✅ Render instance configuration (Starter plan)
- ✅ Docker containerization
- ✅ Uvicorn with 2 workers
- ✅ Environment variables managed via Render dashboard
- ✅ Automatic health monitoring

### Bug Fixes
- 🐛 Fixed FastAPI startup crash (missing `Any` import)
- 🐛 Fixed CORS errors between Vercel and Render
- 🐛 Fixed type mismatches in mock data
- 🐛 Fixed Vercel build failures due to type definitions
- 🐛 Several deployment recovery steps documented

### Known Issues
- No database integration (file-based storage)
- No user authentication
- Manual worker scheduling (cron jobs not activated)
- Single region deployment (Oregon)
- Limited monitoring (basic health checks only)



## v2.1
- API Enrichment completo
- Kindra Distribution
- Delta144 real
- Narrative Risk
- Logging estruturado
- News API integration
- Documentação produção criada

## v2.0
- Master Engine V2
- Delta144 semantic
- TW + Painlevé stub
- Bias Engine melhorado
- Testes core (37 total)
