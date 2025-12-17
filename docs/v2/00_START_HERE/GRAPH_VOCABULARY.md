# 📖 Graph Vocabulary

> **Version**: v2.0 | **Status**: Frozen

This document defines the **canonical relation types** used across all KALDRA documentation graphs. These relations are frozen and should not be extended without versioning.

---

## Relation Types

### `depends_on`

**Definition**: Module A requires Module B to function.

**Direction**: A → B (A depends on B)

**Examples**:
- `kaldra_master_engine.py` depends_on `delta144_engine.py`
- `kindra_engine.py` depends_on `loaders.py`

**Graph Usage**:
```csv
from,relation,to,notes
mod_master_engine,depends_on,mod_delta144_engine,Uses Delta144Engine for base inference
```

---

### `feeds`

**Definition**: Data/output from A flows into B as input.

**Direction**: A → B (A feeds B)

**Examples**:
- `kaldra_data/pipeline/pipeline_alpha.py` feeds `src/apps/alpha/`
- `learning/` feeds `kindras/`

**Graph Usage**:
```csv
from,relation,to,notes
data_pipeline_alpha,feeds,app_alpha,Provides data to Alpha app
```

---

### `exposes_api`

**Definition**: A router/endpoint makes B accessible via HTTP API.

**Direction**: A → B (A exposes B)

**Examples**:
- `kaldra_api/main.py` exposes_api `router_engine.py`
- `router_v3_1.py` exposes_api `UnifiedKernel`

**Graph Usage**:
```csv
from,relation,to,notes
api_main,exposes_api,router_engine,/engine endpoints
```

---

### `configures`

**Definition**: A provides configuration/settings for B.

**Direction**: A → B (A configures B)

**Examples**:
- `exoskeleton/presets.py` configures `UnifiedKernel`
- `engine_router.py` configures `apps/alpha/`

**Graph Usage**:
```csv
from,relation,to,notes
mod_exo_presets,configures,engine_unified_kernel,Presets configure kernel modes
```

---

### `reads_from`

**Definition**: A reads data/config from B (files, schemas, databases).

**Direction**: A → B (A reads from B)

**Examples**:
- `delta144_engine.py` reads_from `schema/archetypes/`
- `tw369_integration.py` reads_from `tw369_default_config.json`

**Graph Usage**:
```csv
from,relation,to,notes
mod_delta144_engine,reads_from,schema_archetypes,Loads archetype definitions
```

---

### `writes_to`

**Definition**: A writes data to B (files, databases, external services).

**Direction**: A → B (A writes to B)

**Examples**:
- `router_signals.py` writes_to `supabase/`
- `audit_trail.py` writes_to `logs/`

**Graph Usage**:
```csv
from,relation,to,notes
router_signals,writes_to,supabase,Writes signals to Supabase
```

---

### `tests`

**Definition**: A is a test suite for B.

**Direction**: A → B (A tests B)

**Examples**:
- `tests/core/` tests `src/core/`
- `tests/tw369/` tests `src/tw369/`

**Graph Usage**:
```csv
from,relation,to,notes
tests_core,tests,engine_core,Core engine tests
```

---

### `runs_as`

**Definition**: A is deployed/executed as B (container, service, process).

**Direction**: A → B (A runs as B)

**Examples**:
- `infra/docker/` runs_as `kaldra_api/main.py`
- `infra/k8s/` runs_as `kaldra-api-deployment`

**Graph Usage**:
```csv
from,relation,to,notes
infra_docker,runs_as,api_main,Docker container runs API
```

---

### `renders_ui`

**Definition**: A provides user interface for B (frontend rendering backend data).

**Direction**: A → B (A renders B)

**Examples**:
- `4iam_frontend/` renders_ui `kaldra_api/`
- `visual_engine/` renders_ui `router_engine.py`

**Graph Usage**:
```csv
from,relation,to,notes
frontend_4iam,renders_ui,api_main,Frontend consumes API
```

---

### `owned_by`

**Definition**: A is a component owned/contained by B (organizational).

**Direction**: A → B (A is owned by B)

**Examples**:
- `design_system/` owned_by `4iam_frontend/`
- `pipeline/` owned_by `unification/`

**Graph Usage**:
```csv
from,relation,to,notes
mod_design_system,owned_by,frontend_4iam,Design tokens for frontend
```

---

## Node ID Conventions

### Prefixes

| Prefix | Type | Example |
|--------|------|---------|
| `engine_` | Engine | `engine_tw369` |
| `mod_` | Module | `mod_tw369_integrator` |
| `app_` | Application | `app_alpha` |
| `api_` | API layer | `api_main` |
| `router_` | Router | `router_engine` |
| `schema_` | Schema | `schema_archetypes` |
| `data_` | Data layer | `data_pipeline_alpha` |
| `infra_` | Infrastructure | `infra_docker` |
| `frontend_` | Frontend | `frontend_4iam` |
| `tests_` | Tests | `tests_core` |

### Naming Rules

1. Use lowercase with underscores
2. Remove file extensions
3. Remove `src/` prefix
4. Preserve hierarchy with underscores

**Examples**:
- `src/tw369/tw369_integration.py` → `mod_tw369_integrator`
- `src/core/kaldra_master_engine.py` → `mod_core_master_engine`
- `kaldra_api/routers/router_engine.py` → `router_engine`

---

## Future Implementations

1. Add `version` relation for version dependencies
2. Add `deprecated_by` relation for migration paths
3. Add `extends` relation for inheritance

---

## Enhancements (Short/Medium Term)

1. Add confidence scores to relations
2. Add temporal metadata (when relation was established)
3. Create relation validation rules

---

## Research Track (Long Term)

1. Auto-extract relations from import statements
2. ML-based relation inference
3. Dynamic graph updates on code changes

---

## Known Limitations

1. No transitive closure (A→B→C doesn't imply A→C)
2. Relations are manually curated
3. Some relations are inferred, not verified

---

## Testing

| Aspect | Status |
|--------|--------|
| All relation types defined | ✅ Done |
| Node ID conventions documented | ✅ Done |
| Examples provided | ✅ Done |

---

## Next Steps

1. [ ] Validate all EDGES_V2.csv uses only these relations
2. [ ] Create relation validation script
3. [ ] Add reverse relation lookups

---

## Related

- [[MOC_HOME]]
- [[EDGES_V2.csv]]
- [[SYSTEM_OVERVIEW]]
