#!/usr/bin/env bash
# Runtime test lane — CLI integration tests that use subprocess.run.
#
# These tests invoke `remedy` CLI subcommands via bounded subprocess.run
# calls (30-second timeout). They are lightweight but can hang in
# environments where stdin/tty behavior differs (e.g. review sandboxes).
#
# Expected runtime: under 30 seconds on a normal dev machine.
#
# Does NOT run heavy smoke scripts, provider execution, or overnight tests.
# For pure in-process tests: scripts/remedy_test_fast.sh
# For full coverage: scripts/remedy_test_full.sh
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-120}"

echo "=== Runtime Test Lane (CLI Integration — bounded subprocess) ==="

exec scripts/remedy_pytest.sh \
    tests/cli/test_review_bundle_runtime.py \
    tests/cli/test_command_catalog.py \
    tests/cli/test_contract_runtime.py \
    tests/cli/test_config_cmd.py \
    -q
