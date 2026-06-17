#!/usr/bin/env bash
# Fast test lane — proves the core product spine is healthy.
#
# Targeted test files (~420 tests). Expected runtime: under 15 seconds
# on a normal dev machine. Actual time depends on environment.
#
# Some included files use bounded subprocess.run calls for CLI
# integration tests (config, review bundle, catalog). These are
# lightweight CLI invocations, not heavy process-group smoke tests.
#
# Does NOT run the full 6800+ test suite.
# Does NOT run UI builds, provider execution, or heavy smoke scripts.
#
# When to use: during development, before committing, quick health check.
# For full coverage: scripts/remedy_test_full.sh
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-180}"

echo "=== Fast Test Lane (Core Product Spine) ==="

# Core spine test files — one per subsystem that matters for operators.
#
# worker facade:           alias registry, doctor/add/disable, catalog, contract
# dogfood run:             mission run loop, morning report, CLI handlers, evidence
# managed builder exec:    command templates, approval, execution safety, placeholders
# main builder adapter:    adapter specs, enable/disable, mode management
# self-repair proposal:    create/approve/deny/edit/worker-prompt lifecycle
# review bundle:           evidence safety, no raw leaks, progress summary
# command catalog:         catalog integrity, group definitions, handler wiring
# run contract:            allowed/denied actions, budget, contract evaluation
# config:                  config layer basics
# product spine:           operator command consistency, stale doc scanner, lane self-test
exec scripts/remedy_pytest.sh \
    tests/cli/test_worker_facade_cmd.py \
    tests/orchestration/test_dogfood_run.py \
    tests/orchestration/test_managed_builder_execution.py \
    tests/orchestration/test_main_builder_adapter.py \
    tests/orchestration/test_self_repair_proposal.py \
    tests/cli/test_review_bundle_runtime.py \
    tests/cli/test_command_catalog.py \
    tests/cli/test_contract_runtime.py \
    tests/cli/test_config_cmd.py \
    tests/cli/test_product_spine.py \
    -q
