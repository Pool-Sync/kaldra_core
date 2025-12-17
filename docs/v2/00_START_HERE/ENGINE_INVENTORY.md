# 🔧 KALDRA Engine Inventory

> **Version**: v2.0 | **Generated**: 2024-12-17 | **Status**: Discovery Phase

This document catalogs all detected "engines" in the `kaldra_core` repository.

---

## Engine Summary Table

| Engine | Path | Key Entry Point | Domain |
|--------|------|-----------------|--------|
| UnifiedKernel | `src/unification/` | `kernel.py` | Orchestration |
| KaldraMasterEngine | `src/core/` | `kaldra_master_engine.py` | Core Pipeline |
| TW369 Integrator | `src/tw369/` | `tw369_integration.py` | Mathematical/Drift |
| Kindra Engine | `src/kindras/` | `kindra_engine.py` | Cultural Scoring |
| Delta144 Engine | `src/archetypes/` | `delta144_engine.py` | Archetypal Analysis |
| Meta Engines | `src/meta/` | `engine_router.py` | Philosophical Analysis |
| Story Engine | `src/story/` | `story_aggregator.py` | Temporal/Narrative |
| Explainability Engine | `src/explainability/` | `explanation_generator.py` | Interpretation |
| Bias Engine | `src/bias/` | `detector.py` | Bias Detection |
| Tau Layer | `src/tau/` | `tau_layer.py` | Epistemic Limiter |
| Safeguard Engine | `src/safeguard/` | `safeguard_engine.py` | Safety/Risk |

---

## 1. UnifiedKernel (v3.0 Entry Point)

**Canonical Name**: `UnifiedKernel`

**Repo Paths**:
- `src/unification/` (main directory)
- `src/unification/kernel.py` (entry point)
- `src/unification/registry.py` (module registry)
- `src/unification/orchestrator.py` (pipeline orchestrator)
- `src/unification/router.py` (mode router)

**Key Entry Files**:
- `kernel.py` → `UnifiedKernel` class
- `orchestrator.py` → `PipelineOrchestrator`
- `registry.py` → `ModuleRegistry`, `get_global_registry()`

**Looks Like Engine Because**:
- Contains a `UnifiedKernel` class that is documented as "the main entry point for all KALDRA operations"
- Auto-loads all v2.9 engines via `load_engines()` method
- Has a `run()` method accepting `mode` parameter: signal, story, full, safety-first, exploratory
- Contains pipeline orchestration via `PipelineOrchestrator`
- Has subdirectories: `adapters/`, `exoskeleton/`, `output/`, `pipeline/`, `states/`

**Related Docs Found**:
- `docs/exoskeleton/` (3 files)
- `schema/unified/` (8 files)

**Pipeline Stages** (`src/unification/pipeline/`):
- `input_stage.py`
- `core_stage.py`
- `meta_stage.py`
- `story_stage.py`
- `safeguard_stage.py`
- `multi_stream_stage.py`
- `output_stage.py`

---

## 2. KaldraMasterEngineV2 (Core Orchestrator)

**Canonical Name**: `KaldraMasterEngineV2`

**Repo Paths**:
- `src/core/` (main directory)
- `src/core/kaldra_master_engine.py` (primary file)
- `src/core/kaldra_engine_pipeline.py` (pipeline)

**Key Entry Files**:
- `kaldra_master_engine.py` → `KaldraMasterEngineV2` class (~486 lines)
- Produces `KaldraSignal` dataclass output

**Looks Like Engine Because**:
- Named as "Orquestrador mínimo do KALDRA v2.0" (Minimal orchestrator)
- Contains `infer_from_embedding()` as main inference entry point
- Orchestrates: Δ144 (Base), Kindra 3×48 (Cultural Modulation), TW Oracle (Anomaly Detection)
- Has parallel execution support via `ParallelExecutor`
- Integrates with audit trail and logging

**Related Docs Found**:
- `docs/MASTER_ENGINE_V2.md`
- `docs/core/` (38 files)

**Supporting Modules in `src/core/`**:
- `embedding_generator.py` - Semantic embedding generation
- `embedding_cache.py` - Caching layer
- `epistemic_limiter.py` - Epistemic constraints
- `audit_trail.py` - Audit trail logging
- `story_aggregator.py` / `story_tracker.py` - Temporal tracking
- `hardening/` - Fallbacks, timeouts (8 files)
- `observability/` - Monitoring (2 files)

---

## 3. TW369 Integrator (Tracy-Widom / Mathematical Engine)

**Canonical Name**: `TW369Integrator`

**Repo Paths**:
- `src/tw369/` (main directory)
- `src/tw369/tw369_integration.py` (primary file, ~568 lines)

**Key Entry Files**:
- `tw369_integration.py` → `TW369Integrator`, `TWState`
- `tracy_widom.py` → Tracy-Widom statistical distribution
- `drift_topology.py` → `TW369Topology`

**Looks Like Engine Because**:
- Integrates Kindra 3×48 layers with TW369 temporal/drift engine
- Maps layers to planes 3, 6, 9 (Tracy-Widom planes)
- Contains drift calculation: `compute_drift()`, `evolve()`
- Has state management: `TWState`, `create_state()`, `modulate_state()`
- Contains advanced drift models in `advanced_drift_models.py`

**Related Docs Found**:
- `docs/tw369/` (2 files)
- `schema/tw369/` (10 files)
- `src/tw369/README_TW369.md`

**Key Components**:
- `drift.py`, `drift_history.py`, `drift_memory.py`, `drift_state.py` - Drift management
- `drift_topology.py` - Topological analysis
- `temporal_coherence.py` - Temporal coherence checking
- `oracle_tw_painleve.py`, `tw_painleve_core.py` - Painlevé integration
- `state_plane_mapping.py` - State-to-plane mapping
- `regime_utils.py` - Regime detection
- `painleve/` - Painlevé subdirectory (4 files)

---

## 4. Kindra Engine (Cultural / Semiotic Scoring)

**Canonical Name**: `KindraEngine`

**Repo Paths**:
- `src/kindras/` (main directory)
- `src/kindras/kindra_engine.py` (entry point)

**Key Entry Files**:
- `kindra_engine.py` → `KindraEngine` class (v3.1)
- `kindra_cultural_mod.py` → `KaldraKindraCulturalMod`
- `kindra_hybrid_scorer.py`, `kindra_llm_scorer.py` - Scoring variants

**Looks Like Engine Because**:
- Named "KindraEngine v3.1 — 3×48 semantic/cultural engine"
- Implements 3-layer architecture: Cultural/Macro (L1), Semiotic/Media (L2), Structural/Systemic (L3)
- Main method: `score_all_layers()` returning `KindraContext`
- Produces TW plane distribution and delta144 weights
- Uses LLM scoring + embeddings

**Related Docs Found**:
- `docs/kindras/` (15 files)
- `docs/CULTURAL_VECTORS_48.md`
- `schema/kindras/` (6 files)
- `src/kindras/README_KINDRAS.md`

**Key Components**:
- `loaders.py` - Load vectors and mappings
- `llm_adapter.py` - LLM integration
- `scoring/` - Scoring implementations (26 files)
- `layer1_*.py`, `layer2_*.py`, `layer3_*.py` - Layer-specific scoring + bridges
- `normalization.py` - Score normalization

---

## 5. Delta144 Engine (Archetypal Analysis)

**Canonical Name**: `Delta144Engine`

**Repo Paths**:
- `src/archetypes/` (main directory)
- `src/archetypes/delta144_engine.py` (primary file, ~842 lines)

**Key Entry Files**:
- `delta144_engine.py` → `Delta144Engine` class
- `delta12_vector.py` → `Delta12Vector` (12 primary archetypes)
- `polarity_mapping.py` - Polarity mappings

**Looks Like Engine Because**:
- Named "Motor Δ144 (Delta-144) — Arquétipos × Estados"
- Loads 12 archetypes × 12 states = 144 archetype states
- Contains dataclasses: `Archetype`, `ArchetypeState`, `Modifier`, `Polarity`, `StateInferenceResult`
- Factory method: `from_schema()` loads from JSON schemas
- Has embedding support for state inference

**Related Docs Found**:
- `docs/archetypes/` (4 files)
- `schema/archetypes/` (4 files)

**Key Components**:
- `Archetype` - 12 base archetypes (Creator, Sage, Ruler, etc.)
- `ArchetypeState` - 144 state matrix cells
- `Modifier` - 59 qualifiers
- `Polarity` - 46 dimensional tensions (v2.7)
- `tw_delta_bridge.py` - TW-Delta bridge

---

## 6. Meta Engines (Philosophical Analysis)

**Canonical Name**: `MetaEngines` (collective)

**Repo Paths**:
- `src/meta/` (main directory)

**Key Entry Files**:
- `engine_router.py` → `MetaRouter` - Context-based routing to engines
- `engine_orchestrator.py` → Orchestration
- `meta_router.py` → `MetaRouter` (secondary)
- `aurelius.py` → `AureliusEngine` (Stoic analysis, ~734 lines)
- `nietzsche.py` → `NietzscheEngine` (will-to-power)
- `campbell.py` → Campbell hero's journey
- `campbell_engine.py` → Campbell engine implementation (~30k bytes)

**Looks Like Engine Because**:
- Contains multiple named philosophical engines
- `MetaRouter` routes to engine variants: alpha, geo, product, safeguard, default
- Each engine produces specialized signals (e.g., `AureliusSignal`)
- Has 12 Stoic axes in Aurelius, mapped to 4 Cardinal Virtues
- Integrates with Kindra 3×48 and TW369

**Related Docs Found**:
- `docs/meta/` (4 files)
- `docs/META_ENGINE_ROUTING.md`

**Engine Variants**:
| Engine | Focus | Key Metrics |
|--------|-------|-------------|
| Aurelius | Stoic philosophy | 12 axes, 4 virtues, dichotomy of control |
| Nietzsche | Will-to-power | Power dynamics, creative destruction |
| Campbell | Hero's journey | Arc progression, stages |

---

## 7. Story Engine (Temporal / Narrative Analysis)

**Canonical Name**: `StoryEngine`

**Repo Paths**:
- `src/story/` (main directory)

**Key Entry Files**:
- `story_aggregator.py` → `aggregate_story()`, ~492 lines
- `story_buffer.py` → `StoryBuffer`, `StoryEvent`
- `narrative_arc.py` - Arc detection
- `multi_stream_buffer.py` - Multi-stream handling

**Looks Like Engine Because**:
- Named "Story Aggregator - Temporal pattern detection for KALDRA v2.6"
- Produces: `MotionVector`, `InflectionPoint`, `DriftTrajectory`, `ArcProgression`
- Detects: motion vectors, inflection points, arc progression, drift trajectories
- Implements Campbell arc progression tracking
- Has narrative oscillation index

**Related Docs Found**:
- `docs/story/` (7 files)
- `schema/story/` (1 file)

**Key Components**:
- `arc_detector.py` - Arc detection
- `archetypal_timeline.py` - Timeline tracking
- `coherence_scorer.py` - Narrative coherence
- `stream_comparator.py` - Stream comparison
- `timeline_builder.py` - Timeline construction

---

## 8. Explainability Engine

**Canonical Name**: `ExplainabilityEngine`

**Repo Paths**:
- `src/explainability/` (main directory)

**Key Entry Files**:
- `explanation_generator.py` → Main generator (~17k bytes)
- `explanation_output.py` → Output formatting
- `explanation_confidence.py` → Confidence scoring (~13k bytes)

**Looks Like Engine Because**:
- Dedicated to generating human-readable explanations
- Has templating system (`templates/` - 3 files)
- Proto definitions (`proto/` - 4 files)
- Computes confidence for explanations

**Related Docs Found**:
- `docs/explainability/` (4 files)

---

## 9. Bias Engine

**Canonical Name**: `BiasEngine` / `BiasDetector`

**Repo Paths**:
- `src/bias/` (main directory)

**Key Entry Files**:
- `detector.py` → `BiasDetector`
- `scoring.py` → Bias scoring
- `mitigation.py` → Bias mitigation

**Looks Like Engine Because**:
- Contains detection, scoring, and mitigation components
- Has provider system (`providers/` - 8 files)
- Schema definition (`bias_schema.json`)
- Registered in UnifiedKernel as "bias" module

**Related Docs Found**:
- `docs/BIAS_ENGINE_SPEC.md`

---

## 10. Tau Layer (Epistemic Limiter)

**Canonical Name**: `TauLayer`

**Repo Paths**:
- `src/tau/` (main directory)

**Key Entry Files**:
- `tau_layer.py` → `TauLayer` class
- `tau_integration.py` → Integration layer
- `tau_policy.py` → Policy definitions
- `tau_risk_model.py` → Risk modeling
- `tau_state.py` → State management

**Looks Like Engine Because**:
- Named "Epistemic reliability limiter" in kernel registration
- Has policy, risk, and state management
- Modulates system confidence/reliability
- Registered in UnifiedKernel as "tau" module

**Related Docs Found**:
- `docs/tau/` (1 file)
- `schema/tau/` (empty)

---

## 11. Safeguard Engine

**Canonical Name**: `SafeguardEngine`

**Repo Paths**:
- `src/safeguard/` (main directory)

**Key Entry Files**:
- `safeguard_engine.py` → `SafeguardEngine`
- `safeguard_policy.py` → Policy definitions
- `safeguard_risk_model.py` → Risk assessment
- `safeguard_integration.py` → Integration layer

**Looks Like Engine Because**:
- Named "Safety and risk mitigation" in kernel registration
- Has policy and risk components
- Part of pipeline's safety-first mode
- Registered in UnifiedKernel as "safeguard" module

**Related Docs Found**:
- `docs/safeguard/` (1 file)
- `schema/safeguard/` (empty)

---

## Future Implementations

1. **Schema Discovery Engine** - Auto-detect and validate schema changes
2. **Adapter Expansion** - Additional input/output adapters in `src/unification/adapters/`
3. **Exoskeleton Integration** - Full exoskeleton preset system (`src/unification/exoskeleton/`)
4. **Learning Engine** - Formalize `src/learning/` as first-class engine

---

## Enhancements (Short/Medium Term)

1. **Engine Registry API** - Expose hot-reloadable engine registry
2. **Unified Metrics** - Cross-engine performance metrics dashboard
3. **Engine Versioning** - Semantic versioning for each engine independently
4. **Dependency Graph Visualization** - Auto-generate mermaid diagrams from imports
5. **Configuration Validation** - Schema validation for all engine configs at startup

---

## Research Track (Long Term)

1. **Engine Fusion** - Explore merging related engines (e.g., Tau + Safeguard)
2. **Modular Loading** - Lazy-load engines based on pipeline mode
3. **ML-Based Engine Selection** - Learn optimal engine routing from usage patterns
4. **Cross-Engine Caching** - Shared embedding cache across engines

---

## Known Limitations

1. **Circular Dependencies** - Some engines import each other (e.g., core ↔ tw369)
2. **Inconsistent Naming** - Mix of Spanish/English docstrings
3. **Overlapping Functionality** - `src/core/story_aggregator.py` vs `src/story/story_aggregator.py`
4. **Missing Schema** - `schema/tau/` and `schema/safeguard/` are empty
5. **Hardcoded Paths** - Some engines use relative paths that may break

---

## Testing

| Engine | Test Path | Coverage |
|--------|-----------|----------|
| Core | `tests/core/` | 63 files |
| TW369 | `tests/tw369/` | 12 files |
| Kindras | `tests/kindras/` | 18 files |
| Archetypes | `tests/archetypes/` | 10 files |
| Meta | `tests/meta/` | 18 files |
| Story | `tests/story/` | 16 files |
| Explainability | `tests/explainability/` | 12 files |
| Unification | `tests/unification/` | 34 files |
| Integration | `tests/integration/` | 20 files |
| E2E | `tests/e2e/` | 2 files |

---

## Next Steps

1. [ ] Review MODULE_INVENTORY.md for per-engine module breakdown
2. [ ] Review DOMAIN_MAP.md for domain groupings
3. [ ] Review EDGES_DRAFT.csv for dependency relationships
4. [ ] Validate engine boundaries and propose refactoring
5. [ ] Create engine-level README files where missing
