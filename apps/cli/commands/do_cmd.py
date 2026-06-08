"""CLI handler for ``remedy do`` — high-level guided autorun."""

from __future__ import annotations

import json
import sys
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    import argparse


_VALID_PROVIDERS = frozenset({"none", "fixture", "ollama"})


def _parse_builder_provider(val: object) -> str:
    s = str(val).lower().strip()
    if s in _VALID_PROVIDERS:
        return s
    print(
        f"Error: invalid --builder-provider: {val!r}. "
        f"Allowed: none, fixture, ollama.",
        file=sys.stderr,
    )
    sys.exit(2)


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
    fixture_builder: bool | str = False,
    builder_provider: str = "none",
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
        builder_provider=builder_provider,
        json_output=json_output,
    )

    if json_output:
        out: dict = {
            "version": 2,
            "job_id": result.job_id,
            "stage": result.stage,
            "cycles_run": result.cycles_run,
            "stop_reason": result.stop_reason,
            "provider": result.provider,
            "ui_url": result.ui_url,
            "error": result.error,
        }
        _BOOL_EVENTS = frozenset({
            "structured_patch_attempted", "parse_success",
            "source_context_injected", "structured_patch_created",
            "approval_required", "source_patch_applied", "tests_passed",
            "repair_context_created", "repair_loop_used",
        })
        for ev in result.events:
            key = ev.get("event", "")
            val = ev.get("value", "")
            if not key or key in out:
                continue
            if key in _BOOL_EVENTS:
                out[key] = val == "True"
            else:
                out[key] = val
        print(json.dumps(out, indent=2))
    else:
        print(f"Job: {result.job_id}")
        print(f"Stage: {result.stage}")
        print(f"Cycles: {result.cycles_run}")
        if result.provider:
            print(f"Provider: {result.provider}")
        for ev in result.events:
            key = ev.get("event", "")
            val = ev.get("value", "")
            if key:
                print(f"  {key}: {val}")
        if result.stop_reason:
            print(f"Stop reason: {result.stop_reason}")
        if result.ui_url:
            print(f"UI: {result.ui_url}")
        if result.error:
            print(f"Error: {result.error}", file=sys.stderr)


_VALID_FIXTURE_MODES = frozenset({"true", "false", "repair-loop"})


def _parse_fixture_builder(val: object) -> bool | str:
    """Parse --fixture-builder value: true/false/repair-loop.

    Fails with SystemExit(2) on unknown modes.
    """
    s = str(val).lower().strip()
    if s in ("true", "1", "yes"):
        return True
    if s == "repair-loop":
        return "repair-loop"
    if s in ("false", "0", "no"):
        return False
    import sys
    print(
        f"Error: invalid --fixture-builder mode: {val!r}. "
        f"Allowed: true, false, repair-loop.",
        file=sys.stderr,
    )
    sys.exit(2)


COMMAND_HANDLERS: dict[str, Callable[["argparse.Namespace"], None]] = {
    "do.run": lambda args: _cmd_do(
        args.goal,
        repo=getattr(args, "repo", None) or ".",
        project=getattr(args, "project", None),
        autonomy_level=int(getattr(args, "autonomy_level", None) or 2),
        max_cycles=int(getattr(args, "max_cycles", None) or 3),
        enable_ui=(
            bool(getattr(args, "ui", False))
            and not getattr(args, "no_ui", False)
        ),
        dry_run=getattr(args, "dry_run", False),
        json_output=getattr(args, "json", False),
        fixture_builder=_parse_fixture_builder(getattr(args, "fixture_builder", "false")),
        builder_provider=_parse_builder_provider(getattr(args, "builder_provider", "none")),
    ),
}
