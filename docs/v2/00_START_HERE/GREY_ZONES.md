# 🟡 Grey Zones

> **Version**: v2.0 | **Source**: [[DOMAIN_MAP]]

Components that don't fit cleanly into a single domain, with recommended resolution paths.

---

## Overview

Grey zones are areas of the codebase with unclear ownership, overlapping functionality, or ambiguous purpose. Each requires a resolution decision.

---

## Grey Zone Inventory

### 1. `src/common/` — Shared Utilities

**Location**: `src/common/` (6 files)

**Issue**: Cross-cutting utilities used by multiple engines.

**Current State**:
- `unified_signal.py` — Signal definitions
- Various shared types and utilities

**Recommendation**: ✅ **Keep as shared**

**Resolution Path**:
1. Audit all usages across engines
2. Document which engines depend on each file
3. Consider moving to a `src/shared/` or keeping as `src/common/`
4. No action required — this is a valid pattern

---

### 2. `src/domain/` — Domain Models

**Location**: `src/domain/` (5 files)

**Issue**: Unclear scope — should these be in engine-specific locations?

**Current State**:
- Contains domain model definitions
- Used by multiple engines

**Recommendation**: 🔄 **Merge into relevant engines**

**Resolution Path**:
1. Identify which models belong to which engine
2. Move engine-specific models to their engine directories
3. Keep truly shared models in `src/common/`
4. Delete empty `src/domain/` after migration

---

### 3. `src/embeddings/` — Embedding Utilities

**Location**: `src/embeddings/` (2 files)

**Issue**: Overlaps with `src/core/embedding_generator.py`

**Current State**:
- Contains embedding-related utilities
- `src/core/` has `embedding_generator.py`, `embedding_cache.py`

**Recommendation**: 🔄 **Merge into `src/core/`**

**Resolution Path**:
1. Review both locations for duplicate functionality
2. Merge `src/embeddings/` into `src/core/embeddings/` subdir
3. Update all imports
4. Delete `src/embeddings/`

---

### 4. `src/data/` — Data Handling

**Location**: `src/data/` (16 files)

**Issue**: Overlaps with `kaldra_data/`

**Current State**:
- Contains data handling utilities
- `kaldra_data/` is the primary data layer

**Recommendation**: 🔄 **Clarify boundary or merge**

**Resolution Path**:
1. Audit what `src/data/` contains vs `kaldra_data/`
2. If utilities: keep in `src/data/`
3. If pipelines/ingestion: move to `kaldra_data/`
4. Rename to `src/data_utils/` for clarity

---

### 5. `src/infrastructure/` — Execution Layer

**Location**: `src/infrastructure/` (9 files)

**Issue**: Overlaps with top-level `infra/`

**Current State**:
- Contains `execution/parallel_executor.py`
- `infra/` contains deployment configs

**Recommendation**: 🔄 **Rename to `src/execution/`**

**Resolution Path**:
1. `src/infrastructure/` → `src/execution/`
2. Keep `infra/` for deployment-specific configs
3. Clear naming: `execution` = runtime, `infra` = deployment

---

### 6. `src/infra/` — Infrastructure Utilities

**Location**: `src/infra/` (4 files)

**Issue**: Overlaps with both `infra/` and `src/infrastructure/`

**Current State**:
- Small utility files
- Naming conflicts with top-level `infra/`

**Recommendation**: 🔄 **Merge or rename**

**Resolution Path**:
1. Review contents
2. If runtime utilities: merge into `src/infrastructure/` (or `src/execution/`)
3. If deployment configs: move to `infra/`
4. Delete `src/infra/`

---

### 7. `src/scripts/` — Utility Scripts

**Location**: `src/scripts/` (13 files)

**Issue**: Mix of utilities — unclear categorization

**Current State**:
- Various utility scripts
- Some may be one-off, others may be production

**Recommendation**: 🔍 **Review and categorize**

**Resolution Path**:
1. Categorize scripts: production vs. development vs. one-off
2. Production scripts → keep in `src/scripts/`
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
- `src/explainability/proto/` also exists

**Recommendation**: 🔄 **Move to schema/proto**

**Resolution Path**:
1. Move to `schema/proto/`
2. Update import paths
3. Delete top-level `proto/`

---

## Summary Dashboard

| Grey Zone | Issue | Recommendation | Priority |
|-----------|-------|----------------|----------|
| `src/common/` | Cross-cutting | ✅ Keep | Low |
| `src/domain/` | Unclear scope | 🔄 Merge | Medium |
| `src/embeddings/` | Overlap | 🔄 Merge into core | Medium |
| `src/data/` | Overlap | 🔄 Clarify | Medium |
| `src/infrastructure/` | Naming | 🔄 Rename | Low |
| `src/infra/` | Overlap | 🔄 Merge | Medium |
| `src/scripts/` | Mixed | 🔍 Review | Low |
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
