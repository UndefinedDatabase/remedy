#!/usr/bin/env bash
# Backend basis smoke test — targeted tests only, no full suite.
# Uses scripts/remedy_pytest.sh for flock + timeout safety.
set -euo pipefail

echo "=== Backend Basis Smoke ==="

scripts/remedy_pytest.sh \
  tests/cli/test_propose_cli_runtime.py \
  tests/cli/test_worker_cli_runtime.py \
  tests/orchestration/test_worker_execution.py \
  tests/orchestration/test_task_execution.py \
  tests/orchestration/test_proposed_tasks.py \
  tests/test_storage.py \
  -q --cache-clear

echo "=== Backend Basis Smoke PASSED ==="
