#!/usr/bin/env bash
# Fast test lane — proves the core product spine is healthy.
#
# Pure in-process tests only. No subprocess calls, no CLI invocations.
# Expected runtime: under 10 seconds on a normal dev machine.
#
# Does NOT run CLI subprocess integration tests (see remedy_test_runtime.sh).
# Does NOT run the full 6800+ test suite.
# Does NOT run UI builds, provider execution, or heavy smoke scripts.
#
# When to use: during development, before committing, quick health check.
# For CLI integration: scripts/remedy_test_runtime.sh
# For full coverage: scripts/remedy_test_full.sh
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-120}"

echo "=== Fast Test Lane (Core Product Spine — in-process only) ==="

# Pure in-process test files — no subprocess.run, no Popen, no CLI invocations.
#
# worker facade:        alias registry, doctor/add/disable, catalog, contract
# dogfood run:          mission run loop, morning report, CLI handlers, evidence
# managed builder exec: command templates, approval, execution safety, placeholders
# main builder adapter: adapter specs, enable/disable, mode management
# self-repair proposal: create/approve/deny/edit/worker-prompt lifecycle
# approval policy:      policy model, storage, integrity, evaluation, grant
# product spine:        operator command consistency, stale doc scanner, lane self-test
exec scripts/remedy_pytest.sh \
    tests/cli/test_worker_facade_cmd.py \
    tests/orchestration/test_dogfood_run.py \
    tests/orchestration/test_managed_builder_execution.py \
    tests/orchestration/test_main_builder_adapter.py \
    tests/orchestration/test_self_repair_proposal.py \
    tests/orchestration/test_execution_approval_policy.py \
    tests/cli/test_product_spine.py \
    -q
