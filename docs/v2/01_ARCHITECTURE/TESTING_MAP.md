# Testing Strategy & Map

> **Status**: Hardening v1 (Refactor in progress)
> **Smoke Test**: `tests/smoke/test_imports.py` ✅ PASSED

## Test Suites

| Suite | Status | Path | Notes |
|-------|--------|------|-------|
| Smoke | ✅ Pass | `tests/smoke/` | Verifies Engine & API imports |
| Unit | ⚠️ Fail | `tests/` | Needs import refactor (kaldra_engine transition) |
| API | ⚠️ Fail | `tests/api/` | Needs TestClient update |
| E2E | ⚠️ Fail | `scripts/` | Needs path updates |

## Critical Path Verification

1. **Engine Install**: `pip install -e packages/engine` (OK)
2. **API Import**: `from apps.api.main import app` (OK)
3. **Engine Import**: `import kaldra_engine` (OK)

## Next Steps

1. Refactor all `tests/` to use `kaldra_engine` package imports.
2. Fix `Starlette/TestClient` runtime errors in API tests.
3. Update E2E scripts.
