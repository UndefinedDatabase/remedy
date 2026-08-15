"""CLI handlers for the ``ci`` command group — Remedy's own CI, run locally.

The stage TABLE is :mod:`packages.orchestration.ci_stages` and the RUNNER is
:mod:`packages.orchestration.ci_run`; this module owns only the seam between them
and the terminal — stage selection, the summary table, and the process exit code.
Rendering lives HERE rather than in the runner because a summary is a property of
the command that prints it, not of the run (T2_F083). `remedy ci` runs every stage
in table order; `--stage NAME` runs exactly one. A stage marked `runs_in_ci=False`
is REPORTED as skipped with the command that runs it by hand — never silently
dropped, because the coverage claim is honest only while the exclusions stay
visible. Remedy deliberately does NOT give this command a "stop at the first red"
switch: `run_ci_stage` never raises on a red stage, so every selected stage always
runs and the summary is always complete.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

def repo_root_for_ci() -> Path:
    """The repository root every stage is anchored at (finding R-0456).

    This file is `apps/cli/commands/ci_cmd.py`, so the root is three levels up.
    """
    return Path(__file__).resolve().parents[3]


def summarize_ci_results(results: tuple[Any, ...]) -> str:
    """The per-stage table a human reads: one line per stage, in run order."""
    lines = ["STAGE        RESULT      TIME  NOTE"]
    for result in results:
        if not result.ran:
            verdict = "skipped"
        elif result.exit_code == 0:
            verdict = "passed"
        else:
            verdict = f"failed({result.exit_code})"
        lines.append(f"{result.stage:<12} {verdict:<11} {result.duration_s:5.1f}  {result.note}".rstrip())
    return "\n".join(lines)


def ci_results_as_json(results: tuple[Any, ...]) -> str:
    """The same table as JSON, for a caller that parses instead of reads."""
    rows = [
        {
            "stage": result.stage, "ran": result.ran, "exit_code": result.exit_code,
            "duration_s": round(result.duration_s, 3), "note": result.note,
        }
        for result in results
    ]
    return json.dumps(rows, indent=2)


def _cmd_ci_run(args: Any) -> None:
    """Run the selected CI stages and exit with the run's honest verdict."""
    from packages.orchestration.ci_run import ci_exit_code, run_ci_stage
    from packages.orchestration.ci_stages import CI_STAGES, ci_stage_by_name

    selected = getattr(args, "stage", None)
    stages = (ci_stage_by_name(selected),) if selected else CI_STAGES
    root = repo_root_for_ci()
    results = tuple(run_ci_stage(stage, root) for stage in stages)

    if getattr(args, "json", False):
        print(ci_results_as_json(results))
    else:
        print(summarize_ci_results(results))

    sys.exit(ci_exit_code(results))


COMMAND_HANDLERS = {
    "ci.run": lambda args: _cmd_ci_run(args),
}
