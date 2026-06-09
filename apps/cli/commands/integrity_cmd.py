"""CLI handlers for the ``integrity`` command group."""

from __future__ import annotations

import json
import sys
from typing import Any


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
        print(json.dumps(export_integrity_json(result), indent=2))
    else:
        print(summarize_integrity(result))

    if not result.passed:
        sys.exit(1)


COMMAND_HANDLERS = {
    "integrity.check": lambda args: _cmd_integrity_check(args),
}
