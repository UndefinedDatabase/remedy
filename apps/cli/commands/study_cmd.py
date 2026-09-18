"""F266 T001 — the `remedy study run` command (CLI wiring for bounded comprehension pass).

Calls run_study with study_call_fn() as the default call_fn, completing the CLI
wiring for the study role. The command writes approved memory cards to the project's
memory store, classified as write_metadata like teacher.ask because both write to
project state and may cost a model call.
"""
from __future__ import annotations

import json as _json
import os
import sys


def _cmd_study_run(
    path: str | None = None,
    *,
    project: str | None = None,
    json_output: bool = False,
    call_fn=None,
) -> None:
    """Run the bounded comprehension pass over a repository.

    ``call_fn`` is the transport seam of study_call_fn; it stays None in
    every real invocation and exists so tests can prove this command's
    behavior without a running Ollama (same pattern as teacher_cmd's `call`
    parameter, DECISION F255 D8).
    """
    from packages.orchestration.project_scope import resolve_scope
    from packages.orchestration.study import (
        record_study_pass,
        run_study,
        study_call_fn,
    )

    target = os.path.abspath(path or ".")
    scope = resolve_scope(project_flag=project, all_projects=False, cwd=target)
    if scope.project_id is not None:
        resolved_project = scope.project_id
    else:
        resolved_project = project or target
        print(
            "No registered project found for this repository — cards are written "
            "unscoped by path and may not be retrievable by `teacher ask` later. "
            "Run `remedy init` first.",
            file=sys.stderr,
        )
    resolved_call_fn = call_fn if call_fn is not None else study_call_fn()

    result = run_study(target, project_id=resolved_project, call_fn=resolved_call_fn)
    if scope.project_id is not None:
        # DECISION F268 D3: a study run by hand is the one study `remedy do` reads.
        record_study_pass(scope.project_id, target)

    if json_output:
        print(_json.dumps({
            "project_id": result.project_id,
            "job_id": result.job_id,
            "cards_written": result.cards_written,
            "partial": result.partial,
            "stopped_reason": result.stopped_reason,
            "entries_scanned": result.entries_scanned,
        }, indent=2))
        return

    print(f"Studied repository: {target}")
    print(f"Memory cards written: {', '.join(result.cards_written)}")
    if result.partial:
        print(f"PARTIAL — {result.stopped_reason}")


COMMAND_HANDLERS = {
    "study.run": lambda args: _cmd_study_run(
        getattr(args, "path", None),
        project=getattr(args, "project", None),
        json_output=bool(getattr(args, "json", False)),
    ),
}
