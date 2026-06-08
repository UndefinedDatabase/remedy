#!/usr/bin/env python3
"""Runtime wrapper smoke supervisor.

Runs propose and worker pytest wrappers in isolated processes.

Usage:
    python3 scripts/remedy_runtime_wrapper_smoke.py
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

    print(f"=== Runtime Wrapper Smoke (timeout={timeout}s) ===", flush=True)

    rc = run_phase(
        "Propose wrapper",
        ["bash", PYTEST_SH, "tests/cli/test_propose_cli_runtime.py", "-q", "--cache-clear"],
        timeout=timeout,
        env={"REMEDY_PYTEST_TIMEOUT_SEC": str(timeout)},
    )
    if rc != 0:
        return rc

    rc = run_phase(
        "Worker wrapper",
        ["bash", PYTEST_SH, "tests/cli/test_worker_cli_runtime.py", "-q", "--cache-clear"],
        timeout=timeout,
        env={"REMEDY_PYTEST_TIMEOUT_SEC": str(timeout)},
    )
    if rc != 0:
        return rc

    print("=== Runtime Wrapper Smoke PASSED ===", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
