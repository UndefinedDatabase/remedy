"""CLI handler for ``remedy do`` — high-level guided autorun."""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    import argparse


def _cmd_do(
    goal: str,
    *,
    repo: str = ".",
    project: str | None = None,
    autonomy_level: int = 2,
    max_cycles: int = 3,
    enable_ui: bool = False,
    dry_run: bool = False,
    json_output: bool = False,
    fixture_builder: bool = False,
) -> None:
    if dry_run:
        from packages.orchestration.autorun import dry_run_autorun
        plan = dry_run_autorun(
            goal, repo,
            project_id=project,
            autonomy_level=autonomy_level,
            max_cycles=max_cycles,
            enable_ui=enable_ui,
        )
        if json_output:
            print(json.dumps(plan, indent=2))
        else:
            print(f"Dry run: {goal}")
            print(f"Repo: {plan['repo_path']}")
            print(f"Autonomy: {plan['autonomy_label']} (level {autonomy_level})")
            print(f"Phases: {', '.join(plan['phases'])}")
            print(f"Max cycles: {max_cycles}")
            if plan["gates"]:
                print(f"Gates: {', '.join(g['gate'] for g in plan['gates'])}")
        return

    from packages.orchestration.autorun import run_autorun
    result = run_autorun(
        goal, repo,
        project_id=project,
        autonomy_level=autonomy_level,
        max_cycles=max_cycles,
        enable_ui=enable_ui,
        fixture_builder=fixture_builder,
        json_output=json_output,
    )

    if json_output:
        print(json.dumps({
            "job_id": result.job_id,
            "stage": result.stage,
            "cycles_run": result.cycles_run,
            "ui_url": result.ui_url,
            "error": result.error,
        }, indent=2))
    else:
        print(f"Job: {result.job_id}")
        print(f"Stage: {result.stage}")
        if result.ui_url:
            print(f"UI: {result.ui_url}")
        if result.error:
            print(f"Error: {result.error}", file=sys.stderr)


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "do.run": lambda args: _cmd_do(
        args.goal,
        repo=getattr(args, "repo", None) or ".",
        project=getattr(args, "project", None),
        autonomy_level=int(getattr(args, "autonomy_level", None) or 2),
        max_cycles=int(getattr(args, "max_cycles", None) or 3),
        enable_ui=str(getattr(args, "ui", "false")).lower() == "true",
        dry_run=getattr(args, "dry_run", False),
        json_output=getattr(args, "json", False),
        fixture_builder=getattr(args, "fixture_builder", False),
    ),
}
