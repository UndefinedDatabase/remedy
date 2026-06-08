#!/usr/bin/env bash
# Fast test lane — safe to run constantly during development.
#
# Excludes: subprocess, real_ollama, ui_contract, smoke, slow
# Includes: unit, integration, architecture, safety (pure logic only)
#
# Target: ~30-60 seconds on normal dev machine.
set -euo pipefail

export REMEDY_PYTEST_TIMEOUT_SEC="${REMEDY_PYTEST_TIMEOUT_SEC:-120}"

echo "=== Fast Tests ==="
exec scripts/remedy_pytest.sh tests/ -q --cache-clear \
    -m "not subprocess and not real_ollama and not ui_contract and not smoke and not slow"
