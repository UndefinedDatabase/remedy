#!/usr/bin/env bash
# Full test lane — runs all tests except known environment-sensitive ones.
#
# Runtime: ~3-4 minutes, 6800+ tests.
# Excludes: test_full_chain_order (filesystem ordering dependent).
#
# When to use: before creating a PR, after major changes, CI.
# For quick checks: scripts/remedy_test_fast.sh
set -euo pipefail

echo "=== Full Test Lane ==="
exec scripts/remedy_pytest.sh -k "not test_full_chain_order"
