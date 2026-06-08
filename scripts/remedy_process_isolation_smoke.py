#!/usr/bin/env python3
"""Process isolation smoke supervisor.

Verifies helper and contract tests for process isolation infrastructure.
Intentionally separate from runtime smoke and backend basis smoke.

Usage:
    python3 scripts/remedy_process_isolation_smoke.py

Environment:
    REMEDY_PYTEST_TIMEOUT_SEC  — per-phase timeout (default: 60)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from smoke_runner import run_phase  # noqa: E402

SCRIPTS_DIR = Path(__file__).resolve().parent
PYTEST_SH = str(SCRIPTS_DIR / "remedy_pytest.sh")


def main() -> int:
    timeout = int(os.environ.get("REMEDY_PYTEST_TIMEOUT_SEC", "60"))

    print(f"=== Process Isolation Smoke (timeout={timeout}s) ===", flush=True)

    # Phase 1: Runtime helper unit tests
    rc = run_phase(
        "Runtime helper tests",
        ["bash", PYTEST_SH, "tests/cli/test_runtime_helpers.py", "-q", "--cache-clear"],
        timeout=timeout,
        env={"REMEDY_PYTEST_TIMEOUT_SEC": str(timeout)},
    )
    if rc != 0:
        return rc

    # Phase 2: Smoke script contract tests
    rc = run_phase(
        "Smoke script contracts",
        ["bash", PYTEST_SH, "tests/cli/test_smoke_scripts.py", "-q", "--cache-clear"],
        timeout=timeout,
        env={"REMEDY_PYTEST_TIMEOUT_SEC": str(timeout)},
    )
    if rc != 0:
        return rc

    # Phase 3: Pytest runner contract tests
    rc = run_phase(
        "Pytest runner contracts",
        ["bash", PYTEST_SH, "tests/cli/test_pytest_runner.py", "-q", "--cache-clear"],
        timeout=timeout,
        env={"REMEDY_PYTEST_TIMEOUT_SEC": str(timeout)},
    )
    if rc != 0:
        return rc

    print("=== Process Isolation Smoke PASSED ===", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
