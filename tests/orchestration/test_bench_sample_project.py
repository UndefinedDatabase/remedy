"""R-0411 / DECISION F082 D3 — the bench's own sample project.

The gauntlet pins its template's suite green the same way
(``test_gauntlet_orders.py::test_the_template_suite_is_green_and_self_sufficient``).
"""
from __future__ import annotations

import os
import subprocess
import sys

from packages.orchestration.bench_orders import default_bench_template_dir


def test_the_fixture_suite_is_green_and_self_sufficient() -> None:
    """A world whose own suite is red would make every DoD meaningless."""
    proc = subprocess.run([sys.executable, "-B", "-m", "pytest", "tests", "-q",
                           "-p", "no:cacheprovider"],
                          cwd=str(default_bench_template_dir()), capture_output=True,
                          text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                          timeout=120)
    assert proc.returncode == 0, proc.stdout[-2000:]
