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


def _cmd_integrity_block(args: Any) -> None:
    """Lint a reviewer step block against the checkable items of the §3 checklist (F279 T003)."""
    from pathlib import Path

    from packages.orchestration.block_lint import lint_block

    json_output = getattr(args, "json", False)
    path = Path(getattr(args, "path", "") or "")
    if not path.is_file():
        fail("block_not_found", f"no step block at {path}", json_output=json_output)
    results = lint_block(path.read_text(encoding="utf-8"))
    violations = [r for r in results if not r.ok]
    if json_output:
        document = {"results": [r.as_dict() for r in results], "violations": len(violations)}
        if violations:
            fail("block_lint_failed",
                 f"{len(violations)} of {len(results)} checklist items fail on {path}",
                 json_output=True, **document)
        emit_ok(**document)
        return
    for r in results:
        print(f"  [{'OK' if r.ok else 'FAIL'}] item {r.item} ({r.name}): {r.detail}")
    if violations:
        print(f"{len(violations)} of {len(results)} checklist items fail; each FAIL line names the item "
              f"of docs/agents/planner_reviewer_prompt.md section 3 it breaks.")
        sys.exit(1)
    print(f"All {len(results)} checkable items pass.")


COMMAND_HANDLERS = {
    "integrity.check": lambda args: _cmd_integrity_check(args),
    "integrity.block": lambda args: _cmd_integrity_block(args),
}
