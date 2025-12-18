# 🗺️ Repository Map

> **Version**: v2.0 | **Source**: [[DOMAIN_MAP]]

Human-readable map of the `kaldra_core` repository organized by domain.

---

## Domain Overview

```
kaldra_core/
├── 🎯 Engine Domain (src/)
│   ├── unification/     → UnifiedKernel (v3.0 entry)
│   ├── core/            → KaldraMasterEngineV2
│   ├── tw369/           → Tracy-Widom drift engine
│   ├── kindras/         → 3×48 cultural scoring
│   ├── archetypes/      → Delta144 (12×12 states)
│   ├── meta/            → Philosophical engines
│   ├── story/           → Narrative/temporal
│   ├── explainability/  → Human-readable output
│   ├── bias/            → Bias detection
│   ├── tau/             → Epistemic limiter
│   └── safeguard/       → Safety/risk
│
├── 📱 App Domain (src/apps/)
│   ├── alpha/           → Financial analysis
│   ├── geo/             → Geopolitical analysis
│   ├── product/         → Product intelligence
│   └── safeguard/       → Safety-focused
│
├── 🔌 API Domain (kaldra_api/)
│   ├── main.py          → FastAPI entry
│   ├── routers/         → 10 route modules
│   ├── schemas/         → Request/response schemas
│   └── clients/         → External service clients
│
├── 📊 Data Domain
│   ├── kaldra_data/     → Ingestion, pipelines
│   ├── schema/          → JSON schemas (7 areas)
│   └── data/            → Runtime data
│
├── 🏗️ Infrastructure Domain
│   ├── infra/           → Docker, K8s, CI/CD
│   ├── scripts/         → Utility scripts
│   └── supabase/        → Supabase integration
│
├── 🖥️ Frontend Domain
│   ├── 4iam_frontend/   → Next.js app
│   │   ├── app/         → Pages (46 files)
│   │   ├── components/  → React components
│   │   ├── visual_engine/ → Visualizations
│   │   └── design_system/ → Design tokens
│   └── frontend/        → Legacy (minimal)
│
├── 📚 Documentation
│   └── docs/            → All documentation
│       └── v2/          → This vault
│
└── 🧪 Testing
    └── tests/           → Test suites by engine
```

---

## Engine Domain Details

| Engine | Path | Entry Point | Status |
|--------|------|-------------|--------|
| [[UnifiedKernel/ENGINE_OVERVIEW\|UnifiedKernel]] | `src/unification/` | `kernel.py` | ✅ Active |
| [[Core/ENGINE_OVERVIEW\|Core]] | `src/core/` | `kaldra_master_engine.py` | ✅ Active |
| [[TW369/ENGINE_OVERVIEW\|TW369]] | `src/tw369/` | `tw369_integration.py` | ✅ Active |
| [[Kindra/ENGINE_OVERVIEW\|Kindra]] | `src/kindras/` | `kindra_engine.py` | ✅ Active |
| [[Delta144/ENGINE_OVERVIEW\|Delta144]] | `src/archetypes/` | `delta144_engine.py` | ✅ Active |
| [[Meta/ENGINE_OVERVIEW\|Meta]] | `src/meta/` | `engine_router.py` | ✅ Active |
| [[Story/ENGINE_OVERVIEW\|Story]] | `src/story/` | `story_aggregator.py` | ✅ Active |
| [[Explainability/ENGINE_OVERVIEW\|Explainability]] | `src/explainability/` | `explanation_generator.py` | ✅ Active |
| [[Bias/ENGINE_OVERVIEW\|Bias]] | `src/bias/` | `detector.py` | ✅ Active |
| [[Tau/ENGINE_OVERVIEW\|Tau]] | `src/tau/` | `tau_layer.py` | ✅ Active |
| [[Safeguard/ENGINE_OVERVIEW\|Safeguard]] | `src/safeguard/` | `safeguard_engine.py` | ✅ Active |

---

## App Domain Details

| App | Path | Domain Focus |
|-----|------|--------------|
| Alpha | `src/apps/alpha/` | Financial analysis (earnings, markets) |
| Geo | `src/apps/geo/` | Geopolitical analysis |
| Product | `src/apps/product/` | Product intelligence |
| Safeguard | `src/apps/safeguard/` | Safety-focused analysis |

---

## API Domain Details

| Component | Path | Purpose |
|-----------|------|---------|
| Main Entry | `kaldra_api/main.py` | FastAPI application |
| Engine Router | `routers/router_engine.py` | `/engine` endpoints |
| Alpha Router | `routers/router_alpha.py` | `/alpha` endpoints |
| Geo Router | `routers/router_geo.py` | `/geo` endpoints |
| Product Router | `routers/router_product.py` | `/product` endpoints |
| Safeguard Router | `routers/router_safeguard.py` | `/safeguard` endpoints |
| News Router | `routers/router_news.py` | `/kaldra` endpoints |
| v3.1 Router | `routers/router_v3_1.py` | `/api` v3.1 endpoints |
| Signals Router | `routers/router_signals.py` | `/signals` Supabase |
| Story Events | `routers/router_story_events.py` | `/story-events` |

---

## Data Domain Details

### Schema Areas

| Area | Path | Files |
|------|------|-------|
| Archetypes | `schema/archetypes/` | 4 |
| Kindras | `schema/kindras/` | 6 |
| TW369 | `schema/tw369/` | 10 |
| Unified | `schema/unified/` | 8 |
| Story | `schema/story/` | 1 |
| Tau | `schema/tau/` | 0 ⚠️ |
| Safeguard | `schema/safeguard/` | 0 ⚠️ |

# Monorepo Structure (v3.0)

| Directory | Domain | Purpose |
|-----------|--------|---------|
| `apps/api/` | App | FastAPI Gateway |
| `apps/web/` | App | Next.js Frontend (4iam_frontend) |
| `apps/workers/` | App | Data/Worker pipelines |
| `packages/engine/` | Core | KALDRA Python Engine (was src/) |
| `infra/` | Infra | Infrastructure & Deployment |
| `archive/` | Archive | Legacy code |

## `packages/engine/src/` (Engine Core)

| Directory | Domain | Purpose |
|-----------|--------|---------|
| `core/` | Core | Master Engine & Kernel |
| `unified_kernel/` | Core | v3 Unification |
| `kindras/` | Engine | 3x48 Cultural/Semiotic Engine |
| `delta144/` | Engine | 12x12 Archetypal Engine |
| `tw369/` | Engine | Tracy-Widom Temporal Engine |
| `meta/` | Engine | Meta-analysis (Aurelius, Nietzsche, Campbell) |
| `story/` | Engine | Narrative analysis |
| `explainability/` | Engine | Logic explanation generation |(5 files) |

---

## Supporting Directories

| Directory | Purpose | Status |
|-----------|---------|--------|
| `src/common/` | Shared utilities | Active |
| `src/domain/` | Domain models | Unclear |
| `src/embeddings/` | Embedding utilities | Overlaps core |
| `src/data/` | Data handling | Overlaps kaldra_data |
| `src/execution/` | Runtime | Parallel execution & task management |
| `src/data_utils/` | Data | Utilities for normalization/ingestion (NOT primary pipeline) |
| `src/core/embeddings/` | Core | Unified embedding generation & cache |

---

## Future Implementations

1. Add interactive tree visualization
2. Auto-generate from file system
3. Add file count badges

---

## Enhancements (Short/Medium Term)

1. Add clickable path links
2. Add last-modified dates
3. Color-code by status

---

## Research Track (Long Term)

1. 3D repository visualization
2. Time-based evolution view
3. Dependency heat maps

---

## Known Limitations

1. Manual sync with file system required
2. Some paths may be outdated
3. Deep nested paths not fully expanded

---

## Testing

| Aspect | Status |
|--------|--------|
| All domains mapped | ✅ Done |
| Engine paths verified | ✅ Done |
| Links to overviews | ✅ Done |

---

## Next Steps

1. [ ] Verify all paths exist
2. [ ] Add file counts per directory
3. [ ] Create validation script

---

## Related

- [[MOC_HOME]]
- [[DOMAIN_MAP]]
- [[GREY_ZONES]]
