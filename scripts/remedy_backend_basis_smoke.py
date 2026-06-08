#!/usr/bin/env python3
"""Backend basis smoke supervisor.

Runs each smoke phase in full process isolation (Popen + start_new_session +
temp files + killpg). No Bash chaining. No pipe inheritance between phases.

Usage:
    python3 scripts/remedy_backend_basis_smoke.py

Environment:
    REMEDY_PYTEST_TIMEOUT_SEC  — per-phase timeout (default: 120)
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Ensure scripts/ is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))
from smoke_runner import run_phase  # noqa: E402

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
PYTEST_SH = str(SCRIPTS_DIR / "remedy_pytest.sh")
RUNTIME_SMOKE = str(SCRIPTS_DIR / "remedy_runtime_cli_smoke.py")


def main() -> int:
    timeout = int(os.environ.get("REMEDY_PYTEST_TIMEOUT_SEC", "120"))

    print(f"=== Backend Basis Smoke (timeout={timeout}s) ===", flush=True)

    # Phase 1: Standalone runtime CLI smoke (no pytest)
    rc = run_phase(
        "Runtime CLI smoke (standalone)",
        [sys.executable, RUNTIME_SMOKE, "--mode", "all"],
        timeout=timeout,
    )
    if rc != 0:
        return rc

    # Phase 2: Runtime helper unit tests
    rc = run_phase(
        "Runtime helper unit tests",
        ["bash", PYTEST_SH, "tests/cli/test_runtime_helpers.py", "-q", "--cache-clear"],
        timeout=timeout,
        env={"REMEDY_PYTEST_TIMEOUT_SEC": str(timeout)},
    )
    if rc != 0:
        return rc

    # Phase 3: Orchestration and storage tests
    rc = run_phase(
        "Orchestration + storage",
        [
            "bash", PYTEST_SH,
            "tests/orchestration/test_worker_execution.py",
            "tests/orchestration/test_task_execution.py",
            "tests/orchestration/test_proposed_tasks.py",
            "tests/test_storage.py",
            "-q", "--cache-clear",
        ],
        timeout=timeout,
        env={"REMEDY_PYTEST_TIMEOUT_SEC": str(timeout)},
    )
    if rc != 0:
        return rc

    print("=== Backend Basis Smoke PASSED ===", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
