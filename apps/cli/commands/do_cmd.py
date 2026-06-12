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

    # v1 cohesive flow — phased result
    from packages.orchestration.do_run import (
        export_do_run_json,
        run_do,
        summarize_do_run,
    )
    try:
        result = run_do(
            goal, repo,
            autonomy_level=autonomy_level,
            max_loops=max_cycles,
            stop_before_apply=True,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(json.dumps(export_do_run_json(result, contract=result._contract), indent=2))
    else:
        print(summarize_do_run(result))


def _cmd_do_continue(
    job_id: str,
    *,
    intent_id: str | None = None,
    json_output: bool = False,
) -> None:
    """Run one controlled continuation cycle (Step 1166).

    Canonical public form: ``remedy do continue <job_id> [--intent-id <id>] [--json]``.
    No prompt is required. When multiple approved intents exist, --intent-id is
    mandatory (the eligibility gate blocks implicit selection).
    """
    from packages.orchestration.do_continue import (
        ContinueRequest,
        export_continue_result_json,
        run_do_continue,
        summarize_continue_result,
    )

    try:
        result = run_do_continue(
            ContinueRequest(job_id=job_id, intent_id=intent_id or "", source="cli_v1")
        )
    except Exception as exc:
        # Never leak a traceback to the public surface.
        print(f"Error: continuation failed ({type(exc).__name__})", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(json.dumps(export_continue_result_json(result), indent=2, sort_keys=True))
    else:
        print(summarize_continue_result(result))


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
    "do.continue": lambda args: _cmd_do_continue(
        args.job_id,
        intent_id=getattr(args, "intent_id", None),
        json_output=getattr(args, "json", False),
    ),
}
