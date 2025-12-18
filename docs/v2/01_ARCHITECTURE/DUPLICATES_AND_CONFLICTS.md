# ⚠️ Duplicates and Conflicts

> **Version**: v2.0 | **Source**: [[MODULE_INVENTORY]]

Known duplicate modules and naming conflicts requiring resolution.

---

## Duplicate Modules

### 1. `story_aggregator.py` — Critical Duplicate

**Locations**:
1. `packages/engine/kaldra_engine/core/story_aggregator.py` (7,929 bytes)
2. `packages/engine/kaldra_engine/story/story_aggregator.py` (16,410 bytes)

**Issue**: Same module name in two engines

**Analysis**:
| Aspect | `packages/engine/kaldra_engine/core/` | `packages/engine/kaldra_engine/story/` |
|--------|-------------|--------------|
| Size | 7,929 bytes | 16,410 bytes |
| Purpose | Core aggregation | Full story engine |
| Likely Status | Legacy/subset | Primary |

**Impact**:
- Import ambiguity
- Potential behavior differences
- Maintenance burden

**Recommendation**: 🔄 **Remove or rename core version**

**Resolution Path**:
1. Compare both implementations
2. If core version is a subset: delete and update imports
3. If different purposes: rename core to `core_story_aggregator.py`
4. Update all imports across codebase

---

## Naming Conflicts

### 2. `infra/` vs `packages/engine/kaldra_engine/infrastructure/` vs `packages/engine/kaldra_engine/infra/`

**Locations**:
1. `infra/` (top-level) — Deployment configs
2. `packages/engine/kaldra_engine/infrastructure/` — Runtime execution (parallel_executor)
3. `packages/engine/kaldra_engine/infra/` — 4 utility files

**Issue**: Three directories with overlapping "infrastructure" naming

**Recommendation**: 🔄 **Clarify naming**

| Directory | Rename To | Purpose |
|-----------|-----------|---------|
| `infra/` | Keep | Deployment |
| `packages/engine/kaldra_engine/infrastructure/` | `packages/engine/kaldra_engine/execution/` | Runtime |
| `packages/engine/kaldra_engine/infra/` | Merge into above | Utilities |

---

### 3. `packages/engine/kaldra_engine/data/` vs `kaldra_data/`

**Locations**:
1. `packages/engine/kaldra_engine/data/` (16 files) — Data utilities
2. `kaldra_data/` (63 files) — Data pipelines

**Issue**: Two data-related directories with unclear boundaries

**Recommendation**: 🔄 **Clarify or merge**

| Directory | Role | Action |
|-----------|------|--------|
| `kaldra_data/` | Primary data layer | Keep |
| `packages/engine/kaldra_engine/data/` | Utilities | Rename to `packages/engine/kaldra_engine/data_utils/` or merge |

---

### 4. `packages/engine/kaldra_engine/embeddings/` vs `packages/engine/kaldra_engine/core/embedding_*`

**Locations**:
1. `packages/engine/kaldra_engine/embeddings/` (2 files)
2. `packages/engine/kaldra_engine/core/embedding_generator.py`
3. `packages/engine/kaldra_engine/core/embedding_cache.py`

**Issue**: Embedding functionality split across locations

**Recommendation**: 🔄 **Consolidate in core**

**Resolution Path**:
1. Move `packages/engine/kaldra_engine/embeddings/` contents to `packages/engine/kaldra_engine/core/embeddings/`
2. Update imports
3. Delete `packages/engine/kaldra_engine/embeddings/`

---

## Import Conflicts

### 5. Circular Import Risk: `core` ↔ `tw369`

**Modules**:
- `packages/engine/kaldra_engine/core/kaldra_master_engine.py` imports from `packages/engine/kaldra_engine/tw369/`
- `packages/engine/kaldra_engine/tw369/` imports from `packages/engine/kaldra_engine/core/` (potential)

**Risk**: Circular import errors at runtime

**Recommendation**: 🔍 **Audit and refactor**

**Resolution Path**:
1. Map all imports between core and tw369
2. Extract shared types to `packages/engine/kaldra_engine/common/`
3. Use lazy imports if needed

---

## Schema Gaps

### 6. Empty Schema Directories

**Missing Schemas**:
- `schema/tau/` (empty)
- `schema/safeguard/` (empty)

**Issue**: No schema validation for Tau and Safeguard engines

**Recommendation**: 🔧 **Add schemas**

**Resolution Path**:
1. Create `tau_config.json` schema
2. Create `safeguard_policy.json` schema
3. Add validation on engine init

---

## Summary Table

| Issue | Type | Priority | Status |
|-------|------|----------|--------|
| `story_aggregator.py` duplicate | Duplicate | **HIGH** | ✅ Resolved (Core renamed) |
| `infra/` naming conflict | Naming | Medium | ✅ Resolved (packages/engine/kaldra_engine/execution) |
| `packages/engine/kaldra_engine/data/` overlap | Naming | Medium | ✅ Resolved (packages/engine/kaldra_engine/data_utils) |
| `packages/engine/kaldra_engine/embeddings/` split | Naming | Low | ✅ Resolved (packages/engine/kaldra_engine/core/embeddings) |
| Circular imports | Import | Medium | ✅ Resolved (packages/engine/kaldra_engine/common) |
| Empty schemas | Missing | Medium | ⏳ Pending |

---

## Future Implementations

1. Automated duplicate detection
2. Import cycle detection in CI
3. Schema completeness validation

---

## Enhancements (Short/Medium Term)

1. Add lint rules for naming conventions
2. Create migration scripts
3. Document resolution decisions

---

## Research Track (Long Term)

1. Automated refactoring tools
2. Dependency graph visualization
3. Breaking change detection

---

## Known Limitations

1. Resolution requires import updates across codebase
2. Some changes may break existing tests
3. Manual review required

---

## Testing

| Aspect | Status |
|--------|--------|
| Duplicates identified | ✅ Done |
| Priorities assigned | ✅ Done |
| Resolution paths defined | ✅ Done |

---

## Next Steps

1. [ ] Create ticket for story_aggregator resolution
2. [ ] Audit imports for circular dependencies
3. [ ] Create schemas for Tau and Safeguard

---

## Related

- [[MOC_HOME]]
- [[MODULE_INVENTORY]]
- [[GREY_ZONES]]
