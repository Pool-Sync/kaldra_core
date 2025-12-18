# 📦 KALDRA Module Inventory

> **Version**: v2.0 | **Generated**: 2024-12-17 | **Status**: Discovery Phase

Per-engine breakdown of modules, submodules, and public surfaces.

---

## 1. UnifiedKernel Engine (`packages/engine/kaldra_engine/unification/`)

### Core Modules

| Module | Path | Purpose | Public Surface |
|--------|------|---------|----------------|
| kernel | `kernel.py` | Main v3.0 entry point | `UnifiedKernel`, `run()`, `load_engines()` |
| registry | `registry.py` | Module registration | `ModuleRegistry`, `get_global_registry()` |
| orchestrator | `orchestrator.py` | Pipeline execution | `PipelineOrchestrator`, `execute()` |
| router | `router.py` | Mode routing | Router functions |

### Pipeline Stages (`packages/engine/kaldra_engine/unification/pipeline/`)

| Module | Path | Purpose | Public Surface |
|--------|------|---------|----------------|
| input_stage | `input_stage.py` | Input processing | `InputStage` |
| core_stage | `core_stage.py` | Core engine execution | `CoreStage` |
| meta_stage | `meta_stage.py` | Meta engine execution | `MetaStage` |
| story_stage | `story_stage.py` | Story/temporal analysis | `StoryStage` |
| safeguard_stage | `safeguard_stage.py` | Safety checks | `SafeguardStage` |
| multi_stream_stage | `multi_stream_stage.py` | Multi-stream processing | `MultiStreamStage` |
| output_stage | `output_stage.py` | Output formatting | `OutputStage` |
| pipeline_orchestrator | `pipeline_orchestrator.py` | Stage orchestration | `PipelineOrchestrator` |

### States (`packages/engine/kaldra_engine/unification/states/`)

| Module | Path | Purpose |
|--------|------|---------|
| unified_state | `unified_state.py` | `UnifiedContext`, `KindraContext`, `KindraLayerScores` |
| unified_context | `unified_context.py` | `ContextManager` |

### Exoskeleton (`packages/engine/kaldra_engine/unification/exoskeleton/`)

| Module | Path | Purpose |
|--------|------|---------|
| presets | `presets.py` | Execution presets |
| profiles | `profiles.py` | User profiles |
| preset_router | `preset_router.py` | Preset routing |

### Adapters (`packages/engine/kaldra_engine/unification/adapters/`)

6 files for input/output adaptation

### Output (`packages/engine/kaldra_engine/unification/output/`)

4 files for output formatting

**Tests Found**: `tests/unification/` (34 files)

---

## 2. Core Engine (`packages/engine/kaldra_engine/core/`)

### Core Modules

| Module | Path | Purpose | Public Surface |
|--------|------|---------|----------------|
| kaldra_master_engine | `kaldra_master_engine.py` | v2 orchestrator | `KaldraMasterEngineV2`, `KaldraSignal`, `infer_from_embedding()` |
| kaldra_engine_pipeline | `kaldra_engine_pipeline.py` | Pipeline runner | Pipeline classes |
| embedding_generator | `embedding_generator.py` | Semantic embeddings | `EmbeddingGenerator`, `EmbeddingConfig` |
| embedding_cache | `embedding_cache.py` | Embedding caching | Cache classes |
| epistemic_limiter | `epistemic_limiter.py` | Epistemic constraints | Limiter class |
| audit_trail | `audit_trail.py` | Audit logging | `AuditTrail` |
| cache_utils | `cache_utils.py` | Caching utilities | Cache functions |
| kaldra_logger | `kaldra_logger.py` | Logging | `KALDRALogger` |
| story_aggregator | `story_aggregator.py` | Story aggregation | Aggregator class |
| story_tracker | `story_tracker.py` | Story tracking | Tracker class |

### Hardening (`packages/engine/kaldra_engine/core/hardening/`)

| Module | Path | Purpose |
|--------|------|---------|
| fallbacks | `fallbacks.py` | `safe_fallback` decorator |
| timeouts | `timeouts.py` | `with_timeout` decorator |
| + 6 more files | | Circuit breakers, retries |

### Observability (`packages/engine/kaldra_engine/core/observability/`)

2 files for metrics and monitoring

**Tests Found**: `tests/core/` (63 files)

---

## 3. TW369 Engine (`packages/engine/kaldra_engine/tw369/`)

### Core Modules

| Module | Path | Purpose | Public Surface |
|--------|------|---------|----------------|
| tw369_integration | `tw369_integration.py` | Main integrator | `TW369Integrator`, `TWState`, `compute_drift()` |
| tracy_widom | `tracy_widom.py` | TW distribution | TW statistics functions |
| drift | `drift.py` | Drift calculation | Drift functions |
| drift_history | `drift_history.py` | Drift history tracking | `DriftHistory` |
| drift_memory | `drift_memory.py` | Drift memory | Memory class |
| drift_state | `drift_state.py` | Drift state | State class |
| drift_topology | `drift_topology.py` | Topological analysis | `TW369Topology` |
| temporal_coherence | `temporal_coherence.py` | Coherence checking | Coherence functions |
| advanced_drift_models | `advanced_drift_models.py` | Advanced models | Model A/B/C/D functions |
| state_plane_mapping | `state_plane_mapping.py` | State→plane mapping | Mapping functions |
| regime_utils | `regime_utils.py` | Regime detection | Regime functions |
| oracle_tw_painleve | `oracle_tw_painleve.py` | Painlevé oracle | Oracle class |
| tw_painleve_core | `tw_painleve_core.py` | Painlevé core | Core functions |
| tw_guard | `tw_guard.py` | TW guard | Guard class |

### Painlevé (`packages/engine/kaldra_engine/tw369/painleve/`)

4 files for Painlevé transcendent integration

### Configuration

| File | Purpose |
|------|---------|
| `tw369.config.json` | Default config |
| `config_loader.py` | Config loading |
| `schema_registry.py` | Schema registry |
| `schema_migration.py` | Schema migrations |
| `runtime_validation.py` | Runtime validation |

**Tests Found**: `tests/tw369/` (12 files)

---

## 4. Kindras Engine (`packages/engine/kaldra_engine/kindras/`)

### Core Modules

| Module | Path | Purpose | Public Surface |
|--------|------|---------|----------------|
| kindra_engine | `kindra_engine.py` | Main v3.1 engine | `KindraEngine`, `score_all_layers()` |
| kindra_cultural_mod | `kindra_cultural_mod.py` | Cultural modulation | `KaldraKindraCulturalMod` |
| kindra_hybrid_scorer | `kindra_hybrid_scorer.py` | Hybrid scoring | Scorer class |
| kindra_llm_scorer | `kindra_llm_scorer.py` | LLM scoring | LLM scorer class |
| kindra_inference | `kindra_inference.py` | Inference | Inference functions |
| kindra_mapping | `kindra_mapping.py` | Mapping | Mapping functions |
| loaders | `loaders.py` | Data loading | `load_layer_vectors()`, `load_layer_mapping()` |
| llm_adapter | `llm_adapter.py` | LLM adapter | `KindraLLMScorer` |
| normalization | `normalization.py` | Score normalization | Normalization functions |
| scoring_base | `scoring_base.py` | Base scoring | Base classes |
| scoring_dispatcher | `scoring_dispatcher.py` | Score dispatching | Dispatcher class |

### Layer Modules

| Module | Purpose |
|--------|---------|
| `layer1_cultural_macro_loader.py` | L1 loading |
| `layer1_cultural_macro_scoring.py` | L1 scoring (Cultural/Macro) |
| `layer1_delta144_bridge.py` | L1→Δ144 bridge |
| `layer2_semiotic_media_loader.py` | L2 loading |
| `layer2_semiotic_media_scoring.py` | L2 scoring (Semiotic/Media) |
| `layer2_delta144_bridge.py` | L2→Δ144 bridge |
| `layer3_structural_systemic_loader.py` | L3 loading |
| `layer3_structural_systemic_scoring.py` | L3 scoring (Structural/Systemic) |
| `layer3_delta144_bridge.py` | L3→Δ144 bridge |

### Scoring (`packages/engine/kaldra_engine/kindras/scoring/`)

26 files for specialized scoring implementations

### Prompts (`packages/engine/kaldra_engine/kindras/prompts/`)

1 file for LLM prompts

**Tests Found**: `tests/kindras/` (18 files)

---

## 5. Archetypes Engine (`packages/engine/kaldra_engine/archetypes/`)

### Core Modules

| Module | Path | Purpose | Public Surface |
|--------|------|---------|----------------|
| delta144_engine | `delta144_engine.py` | Main Δ144 engine | `Delta144Engine`, `Archetype`, `ArchetypeState`, `Modifier`, `Polarity` |
| delta12_vector | `delta12_vector.py` | Δ12 vectors | `Delta12Vector` |
| polarity_mapping | `polarity_mapping.py` | Polarity mapping | Mapping functions |
| api_adapter | `api_adapter.py` | API adapter | Adapter class |
| tw_delta_bridge | `tw_delta_bridge.py` | TW→Delta bridge | Bridge class |

### Key Data Classes

- `Archetype` - 12 base archetypes
- `ArchetypeState` - 144 state cells
- `Modifier` - 59 qualifiers
- `Polarity` - 46 dimensional tensions
- `StateInferenceResult` - Inference output

**Tests Found**: `tests/archetypes/` (10 files)

---

## 6. Meta Engines (`packages/engine/kaldra_engine/meta/`)

### Core Modules

| Module | Path | Purpose | Public Surface |
|--------|------|---------|----------------|
| engine_router | `engine_router.py` | Context routing | `MetaRouter`, `RoutingContext`, `RoutingDecision` |
| engine_orchestrator | `engine_orchestrator.py` | Orchestration | Orchestrator class |
| meta_router | `meta_router.py` | Secondary router | Router class |
| meta_engine_base | `meta_engine_base.py` | Base class | Base engine class |
| types | `types.py` | Shared types | `MetaInput` |

### Philosophical Engines

| Engine | Path | Focus | Output |
|--------|------|-------|--------|
| Aurelius | `aurelius.py` | Stoic philosophy | `AureliusSignal`, `AureliusProfile` |
| Nietzsche | `nietzsche.py` | Will-to-power | Nietzsche signal |
| Campbell | `campbell.py`, `campbell_engine.py` | Hero's journey | Arc progression |

**Tests Found**: `tests/meta/` (18 files)

---

## 7. Story Engine (`packages/engine/kaldra_engine/story/`)

### Core Modules

| Module | Path | Purpose | Public Surface |
|--------|------|---------|----------------|
| story_aggregator | `story_aggregator.py` | Main aggregation | `aggregate_story()`, `StoryAggregation` |
| story_buffer | `story_buffer.py` | Event buffer | `StoryBuffer`, `StoryEvent` |
| narrative_arc | `narrative_arc.py` | Arc detection | Arc functions |
| arc_detector | `arc_detector.py` | Arc detection | Detector class |
| archetypal_timeline | `archetypal_timeline.py` | Timeline tracking | Timeline class |
| coherence_scorer | `coherence_scorer.py` | Coherence scoring | Scorer class |
| multi_stream_buffer | `multi_stream_buffer.py` | Multi-stream | Buffer class |
| stream_comparator | `stream_comparator.py` | Stream comparison | Comparator class |
| timeline_builder | `timeline_builder.py` | Timeline building | Builder class |

### Key Data Classes

- `MotionVector` - Motion between states
- `InflectionPoint` - Narrative inflections
- `DriftTrajectory` - Drift evolution
- `ArcProgression` - Campbell arc progress

**Tests Found**: `tests/story/` (16 files)

---

## 8. Explainability Engine (`packages/engine/kaldra_engine/explainability/`)

### Core Modules

| Module | Path | Purpose | Public Surface |
|--------|------|---------|----------------|
| explanation_generator | `explanation_generator.py` | Main generator | Generator class |
| explanation_output | `explanation_output.py` | Output formatting | Output classes |
| explanation_confidence | `explanation_confidence.py` | Confidence scoring | Confidence functions |

### Templates (`packages/engine/kaldra_engine/explainability/templates/`)

3 files for explanation templates

### Proto (`packages/engine/kaldra_engine/explainability/proto/`)

4 files for protobuf definitions

**Tests Found**: `tests/explainability/` (12 files)

---

## 9. Bias Engine (`packages/engine/kaldra_engine/bias/`)

### Core Modules

| Module | Path | Purpose | Public Surface |
|--------|------|---------|----------------|
| detector | `detector.py` | Bias detection | `BiasDetector` |
| scoring | `scoring.py` | Bias scoring | Scoring functions |
| mitigation | `mitigation.py` | Bias mitigation | Mitigation functions |

### Providers (`packages/engine/kaldra_engine/bias/providers/`)

8 files for bias detection providers

### Schema

- `bias_schema.json` - Bias schema definition

**Tests Found**: `tests/bias/` (2 files)

---

## 10. Tau Layer (`packages/engine/kaldra_engine/tau/`)

### Core Modules

| Module | Path | Purpose | Public Surface |
|--------|------|---------|----------------|
| tau_layer | `tau_layer.py` | Main layer | `TauLayer` |
| tau_integration | `tau_integration.py` | Integration | Integration functions |
| tau_policy | `tau_policy.py` | Policies | Policy classes |
| tau_risk_model | `tau_risk_model.py` | Risk modeling | Risk model class |
| tau_state | `tau_state.py` | State management | State class |

**Tests Found**: `tests/tau/` (2 files)

---

## 11. Safeguard Engine (`packages/engine/kaldra_engine/safeguard/`)

### Core Modules

| Module | Path | Purpose | Public Surface |
|--------|------|---------|----------------|
| safeguard_engine | `safeguard_engine.py` | Main engine | `SafeguardEngine` |
| safeguard_policy | `safeguard_policy.py` | Policies | Policy classes |
| safeguard_risk_model | `safeguard_risk_model.py` | Risk assessment | Risk model class |
| safeguard_integration | `safeguard_integration.py` | Integration | Integration functions |

**Tests Found**: `tests/safeguard/` (2 files)

---

## Supporting Modules

### Learning (`packages/engine/kaldra_engine/learning/`)

| Module | Purpose |
|--------|---------|
| `delta144_mapping_engine.py` | Mapping engine |
| `kindra_priors.py` | Prior distributions |
| `kindra_weights_engine.py` | Weight learning |
| `features/` | Feature extraction (4 files) |

**Tests Found**: `tests/learning/` (12 files)

### Common (`packages/engine/kaldra_engine/common/`)

| Module | Purpose |
|--------|---------|
| 6 files | Shared utilities (unified_signal, etc.) |

### Domain (`packages/engine/kaldra_engine/domain/`)

| Module | Purpose |
|--------|---------|
| 5 files | Domain models |

### Embeddings (`packages/engine/kaldra_engine/embeddings/`)

| Module | Purpose |
|--------|---------|
| 2 files | Embedding utilities |

### Data (`packages/engine/kaldra_engine/data/`)

| Module | Purpose |
|--------|---------|
| 16 files | Data handling |

### Infrastructure (`packages/engine/kaldra_engine/infrastructure/`)

| Module | Purpose |
|--------|---------|
| 9 files | Execution, parallel processing |

### Infra (`packages/engine/kaldra_engine/infra/`)

| Module | Purpose |
|--------|---------|
| 4 files | Infrastructure utilities |

### Scripts (`packages/engine/kaldra_engine/scripts/`)

| Module | Purpose |
|--------|---------|
| 13 files | Utility scripts |

---

## Future Implementations

1. **Module Dependency Graph** - Auto-generate from imports
2. **Public API Surface Detection** - Automated `__all__` scanning
3. **Type Coverage Report** - Per-module typing coverage

---

## Enhancements (Short/Medium Term)

1. **Module Documentation** - Add docstrings to all modules
2. **Export Consolidation** - Proper `__init__.py` exports
3. **Circular Import Resolution** - Identify and fix cycles
4. **Test Coverage Mapping** - Map tests to specific modules

---

## Research Track (Long Term)

1. **Dynamic Module Loading** - Hot-reload modules
2. **Module Versioning** - Independent module versions
3. **Plugin Architecture** - External module support

---

## Known Limitations

1. **Duplicate Modules** - `story_aggregator.py` exists in both `packages/engine/kaldra_engine/core/` and `packages/engine/kaldra_engine/story/`
2. **Missing Exports** - Many `__init__.py` files are empty or incomplete
3. **Inconsistent Naming** - Mix of `_` and no `_` prefixes for internal modules
4. **Test Coverage Gaps** - Bias, Tau, Safeguard have only 2 test files each

---

## Testing

| Engine | Test Directory | File Count |
|--------|---------------|------------|
| Unification | `tests/unification/` | 34 |
| Core | `tests/core/` | 63 |
| TW369 | `tests/tw369/` | 12 |
| Kindras | `tests/kindras/` | 18 |
| Archetypes | `tests/archetypes/` | 10 |
| Meta | `tests/meta/` | 18 |
| Story | `tests/story/` | 16 |
| Explainability | `tests/explainability/` | 12 |
| Learning | `tests/learning/` | 12 |
| Integration | `tests/integration/` | 20 |
| E2E | `tests/e2e/` | 2 |
| Hardening | `tests/hardening/` | 8 |
| Performance | `tests/performance/` + `tests/perf/` | 11 |

---

## Next Steps

1. [ ] Validate public surface guesses with actual `__all__` exports
2. [ ] Map test files to specific modules
3. [ ] Identify unused modules
4. [ ] Review DOMAIN_MAP.md for domain groupings
