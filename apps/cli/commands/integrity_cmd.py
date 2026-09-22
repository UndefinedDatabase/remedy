"""CLI handlers for the ``integrity`` command group."""

from __future__ import annotations

import sys
from typing import Any

from apps.cli.json_envelope import emit_ok, fail


def _cmd_integrity_check(args: Any) -> None:
    """Run pre-handoff integrity checks."""
    from packages.orchestration.integrity_gate import (
        export_integrity_json,
        run_integrity_checks,
        summarize_integrity,
    )

    collect_only = getattr(args, "collect_only", False)

    result = run_integrity_checks(collect_only=collect_only)

    if getattr(args, "json", False):
        document = export_integrity_json(result)
        if not result.passed:
            fail("integrity_failed",
                 f"integrity gate failed with {result.fail_count} failing check(s)",
                 json_output=True, **document)
        emit_ok(**document)
    else:
        print(summarize_integrity(result))
        if not result.passed:
            sys.exit(1)


COMMAND_HANDLERS = {
    "integrity.check": lambda args: _cmd_integrity_check(args),
}
