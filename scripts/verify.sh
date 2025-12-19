#!/bin/bash
set -e

echo "=== KALDRA VERIFICATION =="
echo "Branch: $(git branch --show-current)"
echo "Date: $(date)"

echo -e "\n1. Checking Environment..."
python3 -m pip list | grep -E "kaldra-engine|fastapi|httpx"

echo -e "\n2. Verifying Engine Import..."
python3 -c "import kaldra_engine; print('✅ kaldra_engine imported')"

echo -e "\n3. Verifying API Import..."
export PYTHONPATH=$PYTHONPATH:.
python3 -c "from apps.api.main import app; print('✅ apps.api imported')"

echo -e "\n4. Running Smoke Tests..."
pytest -q tests/smoke

echo -e "\n5. Running Test Suite (Collection Check)..."
pytest --collect-only -q

echo -e "\n6. Running Fast Tests..."
pytest -q -m "not slow" tests/

echo -e "\n✅ VERIFICATION COMPLETE - GREEN BAR REACHED"
