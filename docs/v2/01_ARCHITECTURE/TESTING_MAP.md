# Testing Strategy & Map

> **Status**: Stabilization v1 (Partially Green)
> **Smoke Test**: `tests/smoke/test_imports.py` ✅ PASSED
> **Last Run**: 21 errors -> 0 errors (Collection phase fixed)

## Test Suites

| Suite | Status | Path | Notes |
|-------|--------|------|-------|
| Smoke | ✅ Pass | `tests/smoke/` | Verifies Engine & API imports |
| Unit | ⚠️ Partial | `tests/` | Cleaned up legacy tests. Some logic may still fail execution. |
| API | 🔄 Update | `tests/api/` | Refactored to `fastapi.testclient`. `kaldra_api` -> `apps.api`. |
| E2E | ⚠️ Fail | `scripts/` | Legacy scripts updated, need verification. |

## Critical Path Verification

1. **Engine Install**: `pip install -e packages/engine` (OK)
2. **API Import**: `from apps.api.main import app` (OK)
3. **Engine Import**: `import kaldra_engine` (OK)

## Recent Cleanup (Stabilization v1)
- Deleted `tests/apps/` (Tests for archived v2.9 code)
- Deleted `tests/core/test_meta.py` (Legacy vector meta)
- Deleted `tests/core/test_llm_dummy_...` (Legacy API)
- Deleted `tests/kaldra_engine/test_engine.py` (Legacy entry point)
- Fixed imports in `tests/core/test_pipeline.py` & `test_tw369.py`
- Fixed `test_scorers_bridges.py`
