# Duplicates and Conflicts Resolution

> **Status**: ✅ RESOLVED (Hardening v1)

## Summary of Resolutions

1. **Infra Naming Conflict**: Renamed `src/infrastructure` to `src/execution`.
2. **Data Naming Conflict**: Renamed `src/data` to `kaldra_engine/data_utils` (and `apps/workers/kaldra_data` kept).
3. **Embeddings**: Consolidated into `kaldra_engine/core/embeddings`.
4. **Circular Imports**: Resolved via `kaldra_engine/common/types.py`.
5. **Monorepo Structure**:
    - **Engine**: `packages/engine/kaldra_engine`
    - **Solutions**: `packages/engine/kaldra_engine/solutions` (was apps)
    - **Apps**: `apps/api`, `apps/web`
6. **Package Rename**: `src` -> `kaldra_engine` (Package mode).

## Verification
- Smoke tests pass.
- Duplicates removed (`* 2.py`).
- Garbage cleaned.
