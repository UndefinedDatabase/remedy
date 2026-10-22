"""CLI handler for `remedy doctor health` (F199 T001, DECISION F199 D1)."""

from __future__ import annotations

import sys
from typing import Any

from apps.cli.json_envelope import emit_ok, fail


def _cmd_doctor_health(ns: Any) -> None:
    """Print each of Remedy's own health checks as PASS, WARN or FAIL; exit 1 on a FAIL."""
    from packages.orchestration.self_health import (
        health_check_lines,
        health_exit_code,
        health_failure_message,
        health_report_document,
        health_verdict,
        run_health_checks,
    )

    results = run_health_checks()
    verdict = health_verdict(results)
    if getattr(ns, "json", False):
        document = health_report_document(results)
        if health_exit_code(results) == 1:
            fail(
                "health_failed",
                health_failure_message(results),
                json_output=True,
                verdict=document["verdict"],
                checks=document["checks"],
            )
        emit_ok(verdict=document["verdict"], checks=document["checks"])
        return
    print(f"Remedy health: {verdict}")
    for line in health_check_lines(r.as_json() for r in results):
        print(line)
    if health_exit_code(results) == 1:
        sys.exit(1)


COMMAND_HANDLERS = {"doctor.health": _cmd_doctor_health}
