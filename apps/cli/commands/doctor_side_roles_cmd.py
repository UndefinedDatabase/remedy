"""CLI handler for `remedy doctor side-roles` (F113 T003b, DECISION F113 D3)."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from apps.cli.json_envelope import emit_ok, fail


def _cmd_doctor_side_roles(ns: Any) -> None:
    """Show where each mapped side role runs and why; with --check, spot-check each, flip on a failure, exit 1."""
    from packages.orchestration.local_endpoints import LOCAL_ENDPOINT_PROBES
    from packages.orchestration.side_role_quality import (
        OUTCOME_FAILED,
        SPOT_CHECK_SETS,
        record_spot_check,
        run_spot_check,
        side_role_status_lines,
    )
    from packages.orchestration.side_role_routing import resolve_side_role_routes

    json_output = bool(getattr(ns, "json", False))
    routes = resolve_side_role_routes()
    checks = []
    if getattr(ns, "check", False):
        for role, endpoint in routes.items():
            if role in SPOT_CHECK_SETS:
                record = run_spot_check(role, endpoint, probes=LOCAL_ENDPOINT_PROBES)
                record_spot_check(record)
                checks.append(record)
    lines = side_role_status_lines(routes)
    failed = [record.role for record in checks if record.outcome == OUTCOME_FAILED]
    payload = {"side_roles": lines, "checks": [asdict(record) for record in checks]}
    if failed:
        message = f"spot check failed for {', '.join(failed)}; the role runs on its own model until a re-check passes"
        if not json_output:
            _print(lines, checks)
        fail("spot_check_failed", message, json_output=json_output,
             side_roles=payload["side_roles"], checks=payload["checks"])
    if json_output:
        emit_ok(**payload)
        return
    _print(lines, checks)


def _print(lines: list[str], checks: list[Any]) -> None:
    for record in checks:
        print(f"Spot check {record.record_id} of {record.role} on {record.endpoint} ({record.model}): "
              f"{record.outcome}{': ' + record.reason if record.reason else ''}")
    print("Side roles:" if lines else "Side roles: none is mapped to a local endpoint")
    for line in lines:
        print(f"  {line}")


COMMAND_HANDLERS = {"doctor.side-roles": _cmd_doctor_side_roles}
