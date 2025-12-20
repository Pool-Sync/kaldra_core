# KALDRA Monorepo

The core monorepo for the KALDRA AI system.

## Quickstart (Unicorn Standard)

We use `uv` and `make` for a standardized, fast development workflow.

### Prerequisites

- Python 3.11+
- `make`

### Commands

| Command | Description |
|---------|-------------|
| `make setup` | Install `uv` and all dependencies (dev + engine) |
| `make engine-install` | Re-install `kaldra_engine` in editable mode |
| `make verify` | Run full verification (Lint, Type, Test, Imports) |
| `make lint` | Check code style (Ruff) |
| `make format` | Fix code style (Ruff) |
| `make type` | Run type checking (Pyright) |
| `make test` | Run fast tests |

### Directory Structure

- `packages/engine`: Core logic (`kaldra_engine`)
- `apps/api`: FastAPI application
- `tests`: Unified test suite
- `scripts`: Maintenance and verification scripts

## Development

1. **Setup**:
   ```bash
   make setup
   ```

2. **Verify Changes**:
   ```bash
   make verify
   ```

3. **Commit**:
   Ensure `make verify` passes before pushing. CI enforces this gate.
