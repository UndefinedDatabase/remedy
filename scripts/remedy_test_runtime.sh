#!/usr/bin/env bash
# Runtime test lane — CLI integration tests that use subprocess.run.
#
# Subprocess-heavy suites (test_review_bundle_runtime.py) run per-node
# to isolate hangs at the individual test level. Other suites run as
# whole-file invocations.
#
# Per-node diagnostics: START/END markers with wall-clock timing.
# Stale process check at end to catch orphaned children.
#
# Timeout model:
#   NODE_TIMEOUT (outer, default 90s) > REMEDY_PYTEST_TIMEOUT_SEC (inner).
#   Inner pytest timeout is set to NODE_TIMEOUT - 10s safety margin.
#   This ensures the pytest runner cleans child processes before the
#   outer timeout fires. The outer timeout is a last-resort safety net.
#
# Does NOT run heavy smoke scripts, provider execution, or overnight tests.
# For pure in-process tests: scripts/remedy_test_fast.sh
# For full coverage: scripts/remedy_test_full.sh
set -euo pipefail

# Outer timeout per node/suite (seconds).
NODE_TIMEOUT="${REMEDY_NODE_TIMEOUT_SEC:-90}"

# Inner pytest timeout: shorter than outer by safety margin.
# This ensures remedy_pytest_runner.py kills child processes before
# the outer timeout fires.
INNER_TIMEOUT=$((NODE_TIMEOUT - 10))
if [ "$INNER_TIMEOUT" -lt 10 ]; then
    INNER_TIMEOUT=10
fi
if [ "$INNER_TIMEOUT" -ge "$NODE_TIMEOUT" ]; then
    echo "ERROR: NODE_TIMEOUT=${NODE_TIMEOUT}s is too small. Minimum is 15s." >&2
    echo "  inner_timeout=${INNER_TIMEOUT}s must be < node_timeout=${NODE_TIMEOUT}s" >&2
    exit 1
fi
export REMEDY_PYTEST_TIMEOUT_SEC="$INNER_TIMEOUT"

# Lock: wait briefly for contention from prior node.
export REMEDY_PYTEST_LOCK_WAIT="${REMEDY_PYTEST_LOCK_WAIT:-10}"

echo "=== Runtime Test Lane (CLI Integration — bounded subprocess) ==="
echo "  node_timeout=${NODE_TIMEOUT}s, inner_pytest_timeout=${INNER_TIMEOUT}s"

# Subprocess-heavy suites: run each test node individually.
NODE_ISOLATED_FILES=(
    tests/cli/test_review_bundle_runtime.py
)

# Light suites: run as whole file.
WHOLE_FILE_SUITES=(
    tests/cli/test_command_catalog.py
    tests/cli/test_contract_runtime.py
    tests/cli/test_config_cmd.py
)

total_passed=0
total_failed=0
failed_nodes=()

# --- Per-node isolation for subprocess-heavy suites ---
for f in "${NODE_ISOLATED_FILES[@]}"; do
    echo "--- node-isolated suite: $f ---"
    nodes=$(timeout 30 scripts/remedy_pytest.sh "$f" --collect-only -q 2>/dev/null | grep "::" || true)
    if [ -z "$nodes" ]; then
        echo "  (no test nodes collected, skipping)"
        continue
    fi
    suite_pass=0
    suite_fail=0
    while IFS= read -r node; do
        node_start=$SECONDS
        echo "  START node: $node"
        if timeout --signal=TERM --kill-after=5 "$NODE_TIMEOUT" scripts/remedy_pytest.sh "$node" -q; then
            node_elapsed=$((SECONDS - node_start))
            echo "  END node: $node status=PASS (${node_elapsed}s)"
            suite_pass=$((suite_pass + 1))
        else
            exit_code=$?
            node_elapsed=$((SECONDS - node_start))
            if [ "$exit_code" -eq 124 ]; then
                echo "  END node: $node status=TIMEOUT (${node_elapsed}s)"
            else
                echo "  END node: $node status=FAIL (${node_elapsed}s)"
            fi
            suite_fail=$((suite_fail + 1))
            failed_nodes+=("$node")
        fi
    done <<< "$nodes"
    echo "  suite result: $suite_pass passed, $suite_fail failed"
    if [ "$suite_fail" -eq 0 ]; then
        total_passed=$((total_passed + 1))
    else
        total_failed=$((total_failed + 1))
    fi
done

# --- Whole-file suites ---
for f in "${WHOLE_FILE_SUITES[@]}"; do
    echo "--- runtime suite: $f ---"
    if timeout --signal=TERM --kill-after=5 "$NODE_TIMEOUT" scripts/remedy_pytest.sh "$f" -q; then
        total_passed=$((total_passed + 1))
    else
        total_failed=$((total_failed + 1))
        echo "FAIL: $f"
    fi
done

echo "=== Runtime Lane: $total_passed/$((total_passed + total_failed)) suites passed ==="

if [ ${#failed_nodes[@]} -gt 0 ]; then
    echo "Failed nodes:"
    for n in "${failed_nodes[@]}"; do
        echo "  - $n"
    done
fi

# --- Stale process diagnostic ---
stale=$(ps -ef | grep -E 'pytest|apps\.cli\.grouped|remedy_pytest_runner' | grep -v grep | grep -v "$$" || true)
if [ -n "$stale" ]; then
    echo "WARNING: stale test processes detected after runtime lane:"
    echo "$stale"
fi

if [ "$total_failed" -gt 0 ]; then
    exit 1
fi
