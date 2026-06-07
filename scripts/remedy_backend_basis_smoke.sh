#!/usr/bin/env bash
# Backend basis smoke test — targeted tests only, no full suite.
# Uses scripts/remedy_pytest.sh for flock + timeout safety.
# Fails if tests hang (REMEDY_PYTEST_TIMEOUT_SEC enforced).
#
# IMPORTANT: Runtime wrapper tests and runtime helper tests are run in
# SEPARATE pytest invocations to prevent combined-process teardown hangs.
#
# Do NOT run standalone runtime smoke (remedy_runtime_cli_smoke.py) before
# wrapper tests here. The wrappers already call it internally. Running it
# twice leaves process state that can prevent pytest wrappers from exiting.
# Use scripts/remedy_runtime_cli_smoke.py --mode all separately if needed.
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-120}"

echo "=== Backend Basis Smoke (timeout=${REMEDY_PYTEST_TIMEOUT_SEC}s) ==="

# 1. Runtime wrapper tests — each in its own pytest process
echo "--- Runtime wrapper: propose ---"
scripts/remedy_pytest.sh tests/cli/test_propose_cli_runtime.py -q --cache-clear

echo "--- Runtime wrapper: worker ---"
scripts/remedy_pytest.sh tests/cli/test_worker_cli_runtime.py -q --cache-clear

# 2. Runtime helper unit tests — separate pytest process
echo "--- Runtime helper unit tests ---"
scripts/remedy_pytest.sh tests/cli/test_runtime_helpers.py -q --cache-clear

# 3. Orchestration and storage tests
echo "--- Orchestration + storage ---"
scripts/remedy_pytest.sh \
  tests/orchestration/test_worker_execution.py \
  tests/orchestration/test_task_execution.py \
  tests/orchestration/test_proposed_tasks.py \
  tests/test_storage.py \
  -q --cache-clear

echo "=== Backend Basis Smoke PASSED ==="
