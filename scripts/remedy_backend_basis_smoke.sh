#!/usr/bin/env bash
# Backend basis smoke test — targeted tests only, no full suite.
# Uses scripts/remedy_pytest.sh for flock + timeout safety.
# Fails if tests hang (REMEDY_PYTEST_TIMEOUT_SEC enforced).
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-120}"

echo "=== Backend Basis Smoke (timeout=${REMEDY_PYTEST_TIMEOUT_SEC}s) ==="

# Standalone runtime CLI smoke (no pytest — full process isolation)
echo "--- Runtime CLI smoke (standalone) ---"
python3 scripts/remedy_runtime_cli_smoke.py --mode all

# Pytest-based tests (thin wrappers + unit tests + orchestration)
echo "--- Pytest suite ---"
scripts/remedy_pytest.sh \
  tests/cli/test_propose_cli_runtime.py \
  tests/cli/test_worker_cli_runtime.py \
  tests/cli/test_runtime_helpers.py \
  tests/orchestration/test_worker_execution.py \
  tests/orchestration/test_task_execution.py \
  tests/orchestration/test_proposed_tasks.py \
  tests/test_storage.py \
  -q --cache-clear

echo "=== Backend Basis Smoke PASSED ==="
