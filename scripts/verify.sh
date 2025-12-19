#!/bin/bash
set -e

echo "=== KALDRA UNICORN VERIFICATION ==="
echo "Branch: $(git branch --show-current)"
echo "Date: $(date)"

# 1. Formatting Check
echo -e "\n1. Checking Format (Ruff)..."
uv run ruff format --check .

# 2. Lint Check
echo -e "\n2. Checking Lint (Ruff)..."
uv run ruff check .

# 3. Type Check
echo -e "\n3. Checking Types (Pyright)..."
uv run pyright

# 4. Smoke Tests & Imports
echo -e "\n4. Verifying Critical Imports..."
python3 -c "import kaldra_engine; print('✅ kaldra_engine imported')"
export PYTHONPATH=$PYTHONPATH:.
python3 -c "from apps.api.main import app; print('✅ apps.api imported')"

# 5. Fast Tests
echo -e "\n5. Running Fast Tests & Smoke..."
uv run pytest -q -m "not slow" tests/

echo -e "\n✅ UNICORN GATE PASSED - GREEN BAR"
