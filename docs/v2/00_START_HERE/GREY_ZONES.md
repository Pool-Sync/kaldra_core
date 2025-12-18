# 🟡 Grey Zones

> **Version**: v2.0 | **Source**: [[DOMAIN_MAP]]

Components that don't fit cleanly into a single domain, with recommended resolution paths.

---

## Overview

Grey zones are areas of the codebase with unclear ownership, overlapping functionality, or ambiguous purpose. Each requires a resolution decision.

---

## Grey Zone Inventory

### 1. `packages/engine/kaldra_engine/common/` — Shared Utilities

**Location**: `packages/engine/kaldra_engine/common/` (6 files)

**Issue**: Cross-cutting utilities used by multiple engines.

**Current State**:
- `unified_signal.py` — Signal definitions
- Various shared types and utilities

**Recommendation**: ✅ **Keep as shared**

**Resolution Path**:
1. Audit all usages across engines
2. Document which engines depend on each file
3. Consider moving to a `packages/engine/kaldra_engine/shared/` or keeping as `packages/engine/kaldra_engine/common/`
4. No action required — this is a valid pattern

---

### 2. `packages/engine/kaldra_engine/domain/` — Domain Models

**Location**: `packages/engine/kaldra_engine/domain/` (5 files)

**Issue**: Unclear scope — should these be in engine-specific locations?

**Current State**:
- Contains domain model definitions
- Used by multiple engines

**Recommendation**: 🔄 **Merge into relevant engines**

**Resolution Path**:
1. Identify which models belong to which engine
2. Move engine-specific models to their engine directories
3. Keep truly shared models in `packages/engine/kaldra_engine/common/`
4. Delete empty `packages/engine/kaldra_engine/domain/` after migration

---

### 3. `packages/engine/kaldra_engine/embeddings/` — Embedding Utilities

**Location**: `packages/engine/kaldra_engine/embeddings/` (2 files)

**Issue**: Overlaps with `packages/engine/kaldra_engine/core/embedding_generator.py`

**Current State**:
- Contains embedding-related utilities
- `packages/engine/kaldra_engine/core/` has `embedding_generator.py`, `embedding_cache.py`

**Recommendation**: 🔄 **Merge into `packages/engine/kaldra_engine/core/`**

**Resolution Path**:
1. Review both locations for duplicate functionality
2. Merge `packages/engine/kaldra_engine/embeddings/` into `packages/engine/kaldra_engine/core/embeddings/` subdir
3. Update all imports
4. Delete `packages/engine/kaldra_engine/embeddings/`

---

### 4. `packages/engine/kaldra_engine/data/` — Data Handling

**Location**: `packages/engine/kaldra_engine/data/` (16 files)

**Issue**: Overlaps with `kaldra_data/`

**Current State**:
- Contains data handling utilities
- `kaldra_data/` is the primary data layer

**Recommendation**: 🔄 **Clarify boundary or merge**

**Resolution Path**:
1. Audit what `packages/engine/kaldra_engine/data/` contains vs `kaldra_data/`
2. If utilities: keep in `packages/engine/kaldra_engine/data/`
3. If pipelines/ingestion: move to `kaldra_data/`
4. Rename to `packages/engine/kaldra_engine/data_utils/` for clarity

---

### 5. `packages/engine/kaldra_engine/infrastructure/` — Execution Layer

**Location**: `packages/engine/kaldra_engine/infrastructure/` (9 files)

**Issue**: Overlaps with top-level `infra/`

**Current State**:
- Contains `execution/parallel_executor.py`
- `infra/` contains deployment configs

**Recommendation**: 🔄 **Rename to `packages/engine/kaldra_engine/execution/`**

**Resolution Path**:
1. `packages/engine/kaldra_engine/infrastructure/` → `packages/engine/kaldra_engine/execution/`
2. Keep `infra/` for deployment-specific configs
3. Clear naming: `execution` = runtime, `infra` = deployment

---

### 6. `packages/engine/kaldra_engine/infra/` — Infrastructure Utilities

**Location**: `packages/engine/kaldra_engine/infra/` (4 files)

**Issue**: Overlaps with both `infra/` and `packages/engine/kaldra_engine/infrastructure/`

**Current State**:
- Small utility files
- Naming conflicts with top-level `infra/`

**Recommendation**: 🔄 **Merge or rename**

**Resolution Path**:
1. Review contents
2. If runtime utilities: merge into `packages/engine/kaldra_engine/infrastructure/` (or `packages/engine/kaldra_engine/execution/`)
3. If deployment configs: move to `infra/`
4. Delete `packages/engine/kaldra_engine/infra/`

---

### 7. `packages/engine/kaldra_engine/scripts/` — Utility Scripts

**Location**: `packages/engine/kaldra_engine/scripts/` (13 files)

**Issue**: Mix of utilities — unclear categorization

**Current State**:
- Various utility scripts
- Some may be one-off, others may be production

**Recommendation**: 🔍 **Review and categorize**

**Resolution Path**:
1. Categorize scripts: production vs. development vs. one-off
2. Production scripts → keep in `packages/engine/kaldra_engine/scripts/`
3. Development scripts → move to `scripts/` (top-level)
4. One-off scripts → move to `archive/scripts/`

---

### 8. `archive/` — Archived Code

**Location**: `archive/` (3 subdirs)

**Issue**: Legacy code — should it be deleted or preserved?

**Current State**:
- Contains historical/deprecated code
- `meta/` subdirectory

**Recommendation**: ✅ **Keep archived**

**Resolution Path**:
1. Add `ARCHIVE_README.md` explaining why archived
2. Consider moving to separate branch
3. No immediate action required

---

### 9. `examples/` — Example Code

**Location**: `examples/` (3 files)

**Issue**: Documentation or production?

**Current State**:
- Contains example usage

**Recommendation**: 🔄 **Move to docs**

**Resolution Path**:
1. Move to `docs/examples/`
2.或者 keep as `examples/` with link from docs
3. Add to documentation navigation

---

### 10. `perf/` — Performance Testing

**Location**: `perf/` (3 files)

**Issue**: Should be with other tests

**Current State**:
- Contains performance tests
- `tests/perf/` also exists

**Recommendation**: 🔄 **Move to tests/perf**

**Resolution Path**:
1. Merge `perf/` into `tests/perf/`
2. Delete top-level `perf/`
3. Standardize all tests under `tests/`

---

### 11. `proto/` — Protobuf Definitions

**Location**: `proto/` (1 file)

**Issue**: Should be with schemas

**Current State**:
- Contains protobuf definitions
- `packages/engine/kaldra_engine/explainability/proto/` also exists

**Recommendation**: 🔄 **Move to schema/proto**

**Resolution Path**:
1. Move to `schema/proto/`
2. Update import paths
3. Delete top-level `proto/`

---

## Summary Dashboard

| Grey Zone | Issue | Recommendation | Priority |
|-----------|-------|----------------|----------|
| `packages/engine/kaldra_engine/common/` | Cross-cutting | ✅ Keep | Low |
| `packages/engine/kaldra_engine/domain/` | Unclear scope | 🔄 Merge | Medium |
| `packages/engine/kaldra_engine/embeddings/` | Overlap | 🔄 Merge into core | Medium |
| `packages/engine/kaldra_engine/data/` | Overlap | 🔄 Clarify | Medium |
| `packages/engine/kaldra_engine/infrastructure/` | Naming | 🔄 Rename | Low |
| `packages/engine/kaldra_engine/infra/` | Overlap | 🔄 Merge | Medium |
| `packages/engine/kaldra_engine/scripts/` | Mixed | 🔍 Review | Low |
| `archive/` | Legacy | ✅ Keep | Low |
| `examples/` | Location | 🔄 Move to docs | Low |
| `perf/` | Location | 🔄 Move to tests | Low |
| `proto/` | Location | 🔄 Move to schema | Low |

---

## Future Implementations

1. Automated grey zone detection
2. Ownership tagging system
3. Migration scripts for resolutions

---

## Enhancements (Short/Medium Term)

1. Add CODEOWNERS file for each area
2. Create lint rules for import paths
3. Document resolution decisions

---

## Research Track (Long Term)

1. Domain-driven design refactoring
2. Microservice extraction planning
3. Automated code organization

---

## Known Limitations

1. Resolution paths are recommendations, not mandates
2. Some changes require import updates across codebase
3. Manual review required before any migration

---

## Testing

| Aspect | Status |
|--------|--------|
| All grey zones listed | ✅ Done |
| Recommendations provided | ✅ Done |
| Priority assigned | ✅ Done |

---

## Next Steps

1. [ ] Discuss priorities with team
2. [ ] Create migration tickets for Medium priority items
3. [ ] Document any decisions made

---

## Related

- [[MOC_HOME]]
- [[REPO_MAP]]
- [[DOMAIN_MAP]]
