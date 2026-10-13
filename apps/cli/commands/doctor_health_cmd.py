"""CLI handler for `remedy doctor health` (F199 T001, DECISION F199 D1)."""

from __future__ import annotations

import sys
from typing import Any

from apps.cli.json_envelope import emit_ok, fail


def _cmd_doctor_health(ns: Any) -> None:
    """Print each of Remedy's own health checks as PASS, WARN or FAIL; exit 1 on a FAIL."""
    from packages.orchestration.self_health import (
        HEALTH_FAIL,
        health_exit_code,
        health_verdict,
        run_health_checks,
    )

    results = run_health_checks()
    verdict = health_verdict(results)
    if getattr(ns, "json", False):
        document = {"verdict": verdict, "checks": [r.as_json() for r in results]}
        if health_exit_code(results) == 1:
            failed = sum(1 for r in results if r.level == HEALTH_FAIL)
            fail("health_failed", f"{failed} of {len(results)} health checks failed",
                 json_output=True, **document)
        emit_ok(**document)
        return
    print(f"Remedy health: {verdict}")
    for r in results:
        print(f"  [{r.level}] {r.check}: {r.detail}")
        if r.hint:
            print(f"         fix: {r.hint}")
    if health_exit_code(results) == 1:
        sys.exit(1)


COMMAND_HANDLERS = {"doctor.health": _cmd_doctor_health}
