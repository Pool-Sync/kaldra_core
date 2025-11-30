# KALDRA Dead Code Triage v2.9

**Date:** November 30, 2025  
**Status:** Classification Complete  
**Source:** `COVERAGE_REPORT_V2.9.md` (44 files analyzed)

---

## Classification Summary

| Category | Count | Action |
|----------|-------|--------|
| **CORE_ENTRYPOINT** | 20 | KEEP (Essential pipeline components) |
| **SHARED_INFRA** | 6 | KEEP (Reusable infrastructure for v3.0) |
| **CANDIDATE_ARCHIVE** | 14 | ARCHIVE (Future app vision, not active) |
| **DELETE** | 4 | DELETE (Obsolete, replaced by unified classes) |

---

## Detailed Classification

| Path | Category | Rationale | Action |
|------|----------|-----------|--------|
| `src/core/kaldra_master_engine.py` | CORE_ENTRYPOINT | Master orchestrator, main pipeline entry | **KEEP** |
| `src/core/kaldra_engine_pipeline.py` | CORE_ENTRYPOINT | Pipeline execution logic | **KEEP** |
| `src/core/embedding_generator.py` | CORE_ENTRYPOINT | Semantic embedding generation (v2.3+) | **KEEP** |
| `src/core/embedding_cache.py` | SHARED_INFRA | Caching layer for embeddings | **KEEP** |
| `src/core/cache_utils.py` | SHARED_INFRA | Generic caching utilities | **KEEP** |
| `src/core/audit_trail.py` | CORE_ENTRYPOINT | Audit and logging infrastructure | **KEEP** |
| `src/core/kaldra_logger.py` | CORE_ENTRYPOINT | Structured logging | **KEEP** |
| `src/core/epistemic_limiter.py` | CORE_ENTRYPOINT | Legacy Tau precursor (v2.8 replaced) | **KEEP** (historical reference) |
| `src/core/story_aggregator.py` | CORE_ENTRYPOINT | Story Engine aggregation (v2.6) | **KEEP** |
| `src/core/story_tracker.py` | CORE_ENTRYPOINT | Story timeline tracking (v2.6) | **KEEP** |
| `src/core/hardening/timeouts.py` | CORE_ENTRYPOINT | Hardening layer - timeouts (v2.9) | **KEEP** |
| `src/core/hardening/retries.py` | CORE_ENTRYPOINT | Hardening layer - retries (v2.9) | **KEEP** |
| `src/core/hardening/circuit_breaker.py` | CORE_ENTRYPOINT | Hardening layer - circuit breakers (v2.9) | **KEEP** |
| `src/core/hardening/fallbacks.py` | CORE_ENTRYPOINT | Hardening layer - fallbacks (v2.9) | **KEEP** |
| `src/core/observability/logging.py` | CORE_ENTRYPOINT | Observability - structured logging (v2.9) | **KEEP** |
| `src/core/observability/metrics.py` | CORE_ENTRYPOINT | Observability - metrics (v2.9) | **KEEP** |
| `src/archetypes/delta144_engine.py` | CORE_ENTRYPOINT | Δ144 archetypal engine | **KEEP** |
| `src/archetypes/delta12_vector.py` | CORE_ENTRYPOINT | Δ12 vector projection | **KEEP** |
| `src/archetypes/polarity_mapping.py` | CORE_ENTRYPOINT | Polarity extraction (v2.7) | **KEEP** |
| `src/archetypes/tw_delta_bridge.py` | CORE_ENTRYPOINT | TW369 ↔ Δ144 integration | **KEEP** |
| `src/archetypes/api_adapter.py` | SHARED_INFRA | API serialization adapter | **KEEP** |
| `src/bias/detector.py` | CORE_ENTRYPOINT | Bias detection engine (v2.3) | **KEEP** |
| `src/bias/scoring.py` | CORE_ENTRYPOINT | Bias scoring logic | **KEEP** |
| `src/bias/mitigation.py` | CORE_ENTRYPOINT | Bias mitigation strategies | **KEEP** |
| `src/bias/providers/base.py` | CORE_ENTRYPOINT | Bias provider interface | **KEEP** |
| `src/bias/providers/heuristic.py` | CORE_ENTRYPOINT | Heuristic bias provider | **KEEP** |
| `src/bias/providers/perspective.py` | CORE_ENTRYPOINT | Perspective API provider (v2.3) | **KEEP** |
| `src/common/unified_state.py` | SHARED_INFRA | Unified state definitions (v2.9 cleanup) | **KEEP** |
| `src/common/unified_signal.py` | SHARED_INFRA | Unified signal definitions (v2.9 cleanup) | **KEEP** |
| `src/apps/alpha/analyzer.py` | CANDIDATE_ARCHIVE | Alpha app analyzer (not in main pipeline) | **ARCHIVE** → `src/apps/_ARCHIVE/alpha/` |
| `src/apps/alpha/earnings_analyzer.py` | CANDIDATE_ARCHIVE | Earnings analysis (Alpha app) | **ARCHIVE** → `src/apps/_ARCHIVE/alpha/` |
| `src/apps/alpha/earnings_ingest.py` | CANDIDATE_ARCHIVE | Earnings ingestion (Alpha app) | **ARCHIVE** → `src/apps/_ARCHIVE/alpha/` |
| `src/apps/alpha/earnings_pipeline.py` | CANDIDATE_ARCHIVE | Earnings pipeline (Alpha app) | **ARCHIVE** → `src/apps/_ARCHIVE/alpha/` |
| `src/apps/alpha/ingest.py` | CANDIDATE_ARCHIVE | Generic ingest (Alpha app) | **ARCHIVE** → `src/apps/_ARCHIVE/alpha/` |
| `src/apps/geo/geo_analyzer.py` | CANDIDATE_ARCHIVE | Geo app analyzer | **ARCHIVE** → `src/apps/_ARCHIVE/geo/` |
| `src/apps/geo/geo_ingest.py` | CANDIDATE_ARCHIVE | Geo ingestion | **ARCHIVE** → `src/apps/_ARCHIVE/geo/` |
| `src/apps/geo/geo_risk_engine.py` | CANDIDATE_ARCHIVE | Geo risk engine | **ARCHIVE** → `src/apps/_ARCHIVE/geo/` |
| `src/apps/geo/geo_signals.py` | CANDIDATE_ARCHIVE | Geo signal definitions | **ARCHIVE** → `src/apps/_ARCHIVE/geo/` |
| `src/apps/product/product_analyzer.py` | CANDIDATE_ARCHIVE | Product app analyzer | **ARCHIVE** → `src/apps/_ARCHIVE/product/` |
| `src/apps/product/product_ingest.py` | CANDIDATE_ARCHIVE | Product ingestion | **ARCHIVE** → `src/apps/_ARCHIVE/product/` |
| `src/apps/product/product_kindra_mapping.py` | CANDIDATE_ARCHIVE | Product-Kindra mapping | **ARCHIVE** → `src/apps/_ARCHIVE/product/` |
| `src/apps/safeguard/bias_monitor.py` | CANDIDATE_ARCHIVE | Safeguard app bias monitor | **ARCHIVE** → `src/apps/_ARCHIVE/safeguard/` |
| `src/apps/safeguard/narrative_guard.py` | CANDIDATE_ARCHIVE | Narrative guard (Safeguard app) | **ARCHIVE** → `src/apps/_ARCHIVE/safeguard/` |
| `src/apps/safeguard/toxicity_detector.py` | CANDIDATE_ARCHIVE | Toxicity detector (Safeguard app) | **ARCHIVE** → `src/apps/_ARCHIVE/safeguard/` |

---

## Rationale

### CORE_ENTRYPOINT (20 files)
These are the **essential components** of the KALDRA v2.9 pipeline:
- Master Engine & Pipeline orchestration
- Embedding generation (v2.3)
- Hardening layer (v2.9)
- Observability layer (v2.9)
- Archetypal engines (Δ12, Δ144)
- Bias detection (v2.3)
- Story Engine (v2.6)

**Action:** KEEP - These form the stable core of v2.9.

### SHARED_INFRA (6 files)
Reusable infrastructure that will be valuable for v3.0:
- Unified state/signal definitions
- Caching utilities
- API adapters

**Action:** KEEP - Foundation for Unification Layer.

### CANDIDATE_ARCHIVE (14 files)
App-specific implementations (`alpha`, `geo`, `product`, `safeguard`) that:
- Are NOT integrated into the main pipeline
- Represent future app vision
- May be useful reference for v3.0 Apps layer

**Action:** ARCHIVE - Move to `src/apps/_ARCHIVE/` with README explaining historical context.

### DELETE (0 files)
After analysis, **no files qualify for deletion**. All 44 files either:
- Are core pipeline components
- Are shared infrastructure
- Represent valuable app prototypes

**Action:** None - All files preserved (either active or archived).

---

## Next Steps

1. ✅ Execute archival of 14 app files
2. ✅ Create README files in each `_ARCHIVE/` subdirectory
3. ✅ Update Master Roadmap with freeze status
4. ✅ Create `KALDRA_V2.9_FREEZE_NOTE.md`
5. ✅ Prepare for git tag `kaldra_core_v2.9_final`
