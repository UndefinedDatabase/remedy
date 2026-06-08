#!/usr/bin/env bash
# Integration test lane — run before merge.
#
# Includes: backend basis smoke + runtime wrapper smoke + process isolation smoke
# + full pytest excluding real_ollama and slow.
#
# Runs smoke supervisors first, then broad pytest.
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-120}"

echo "=== Integration Tests ==="

echo "--- Backend basis smoke ---"
python3 scripts/remedy_backend_basis_smoke.py

echo "--- Runtime wrapper smoke ---"
python3 scripts/remedy_runtime_wrapper_smoke.py

echo "--- Process isolation smoke ---"
python3 scripts/remedy_process_isolation_smoke.py

echo "--- Full pytest (excluding real_ollama, slow) ---"
scripts/remedy_pytest.sh tests/ -q --cache-clear \
    -m "not real_ollama and not slow"

echo "=== Integration Tests PASSED ==="
