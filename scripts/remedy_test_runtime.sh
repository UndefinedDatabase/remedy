#!/usr/bin/env bash
# Runtime test lane — CLI integration tests that use subprocess.run.
#
# Each test suite runs as a separate bounded pytest invocation to isolate
# hangs. If one suite hangs or fails, the others still get a chance to run,
# and the failing suite is clearly identified.
#
# Expected runtime: under about 60 seconds on a normal dev machine.
#
# Does NOT run heavy smoke scripts, provider execution, or overnight tests.
# For pure in-process tests: scripts/remedy_test_fast.sh
# For full coverage: scripts/remedy_test_full.sh
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-120}"

echo "=== Runtime Test Lane (CLI Integration — bounded subprocess) ==="

RUNTIME_FILES=(
    tests/cli/test_review_bundle_runtime.py
    tests/cli/test_command_catalog.py
    tests/cli/test_contract_runtime.py
    tests/cli/test_config_cmd.py
)

total_passed=0
total_failed=0

for f in "${RUNTIME_FILES[@]}"; do
    echo "--- runtime suite: $f ---"
    if scripts/remedy_pytest.sh "$f" -q; then
        total_passed=$((total_passed + 1))
    else
        total_failed=$((total_failed + 1))
        echo "FAIL: $f"
    fi
done

echo "=== Runtime Lane: $total_passed/$((total_passed + total_failed)) suites passed ==="

if [ "$total_failed" -gt 0 ]; then
    exit 1
fi
