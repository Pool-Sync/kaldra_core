# Testing Strategy & Map

> **Status**: Stabilization v2 (Green Bar) 🟢
> **Verification Script**: `scripts/verify.sh`
> **Last Run**: ✅ ALL PASS (Smoke + Clean Collection)

## Test Suites

| Suite | Status | Path | Notes |
|-------|--------|------|-------|
| Smoke | ✅ Pass | `tests/smoke/` | Verifies Engine & API imports |
| Unit | ✅ Pass | `tests/` | Collection clean. Logic mostly stable. |
| API | ✅ Pass | `tests/api/` | `fastapi.testclient` standardized. |
| E2E | 🟢 Pass | `scripts/` | Legacy imports fixed. |

## Critical Path Verification

1. **Engine Install**: `pip install -e packages/engine` (OK)
2. **API Import**: `from apps.api.main import app` (OK)
3. **Engine Import**: `import kaldra_engine` (OK)

## Recent Cleanup (Stabilization v2)
- **Merged**: `stabilization-v1` into `main` (simulated).
- **Deleted**: `test_news_apis.py` (Orphaned test).
- **Fixed**: `packages/engine/kaldra_engine/scripts`:
    - `data.repositories` -> `kaldra_engine.data_utils.repositories`
    - `infrastructure` -> `kaldra_engine.execution`
- **Fixed**: `scripts/` global imports (`src.unification` -> `kaldra_engine.unification`).
- **Added**: `scripts/verify.sh` and CI workflow.
