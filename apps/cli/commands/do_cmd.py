"""CLI handler for ``remedy do`` — high-level guided autorun."""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse


_VALID_PROVIDERS = frozenset({"none", "fixture", "ollama"})
_VALID_PINGPONG_PROVIDERS = frozenset({"none", "fake", "claude", "claude-cli"})


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


_VALID_CLI_WRITE_MODES = frozenset({"none", "allowed-tools", "dangerous-skip"})


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
    builder: str = "none",
    reviewer: str = "none",
    max_rounds: int = 3,
    mode: str = "staged",
    test_command: str = "",
    provider_timeout_sec: int = 120,
    max_output_chars_val: int = 50000,
    keep_staging: bool = False,
    claude_cli_write_mode: str = "none",
) -> None:
    # Ping-pong mode: --builder and/or --reviewer set to a real provider
    if builder != "none" or reviewer != "none":
        _cmd_do_pingpong(
            goal, repo=repo, builder=builder, reviewer=reviewer,
            max_rounds=max_rounds, mode=mode, json_output=json_output,
            test_command=test_command, provider_timeout_sec=provider_timeout_sec,
            max_output_chars=max_output_chars_val, keep_staging=keep_staging,
            claude_cli_write_mode=claude_cli_write_mode,
        )
        return

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


def _cmd_do_pingpong(
    goal: str,
    *,
    repo: str = ".",
    builder: str = "fake",
    reviewer: str = "fake",
    max_rounds: int = 3,
    mode: str = "staged",
    json_output: bool = False,
    test_command: str = "",
    provider_timeout_sec: int = 120,
    max_output_chars: int = 50000,
    keep_staging: bool = False,
    claude_cli_write_mode: str = "none",
) -> None:
    """Run Builder ↔ Reviewer ping-pong loop."""
    if builder not in _VALID_PINGPONG_PROVIDERS:
        print(f"Error: invalid --builder: {builder!r}. Allowed: {', '.join(sorted(_VALID_PINGPONG_PROVIDERS))}.", file=sys.stderr)
        sys.exit(2)
    if reviewer not in _VALID_PINGPONG_PROVIDERS:
        print(f"Error: invalid --reviewer: {reviewer!r}. Allowed: {', '.join(sorted(_VALID_PINGPONG_PROVIDERS))}.", file=sys.stderr)
        sys.exit(2)
    if mode != "staged":
        print("Error: only --mode staged is supported.", file=sys.stderr)
        sys.exit(2)
    if claude_cli_write_mode not in _VALID_CLI_WRITE_MODES:
        print(
            f"Error: invalid --claude-cli-write-mode: {claude_cli_write_mode!r}. "
            f"Allowed: {', '.join(sorted(_VALID_CLI_WRITE_MODES))}.",
            file=sys.stderr,
        )
        sys.exit(2)

    # Default: if only one side set, use fake for the other
    effective_builder = builder if builder != "none" else "fake"
    effective_reviewer = reviewer if reviewer != "none" else "fake"

    from packages.orchestration.pingpong_loop import (
        export_pingpong_json,
        run_pingpong,
        summarize_pingpong,
    )

    if not json_output:
        print("Job: ping-pong run")
        print(f"Mode: {mode}")
        print(f"Builder: {effective_builder}")
        print(f"Reviewer: {effective_reviewer}")
        print(f"Max rounds: {max_rounds}")
        if test_command:
            print(f"Test command: {test_command}")
        print()

    result = run_pingpong(
        goal,
        repo,
        builder_name=effective_builder,
        reviewer_name=effective_reviewer,
        max_rounds=max_rounds,
        timeout_sec=provider_timeout_sec,
        max_output_chars=max_output_chars,
        test_command=test_command,
        keep_staging=keep_staging,
        claude_cli_write_mode=claude_cli_write_mode,
    )

    if json_output:
        print(json.dumps(export_pingpong_json(result), indent=2))
    else:
        print(summarize_pingpong(result))


def _cmd_do_report(
    run_id: str,
    *,
    json_output: bool = False,
) -> None:
    """Show a persisted ping-pong run report."""
    from packages.orchestration.pingpong_loop import (
        list_runs,
        load_run,
    )

    if run_id == "list":
        runs = list_runs()
        if not runs:
            print("No ping-pong runs found.")
            return
        if json_output:
            print(json.dumps(runs, indent=2))
        else:
            for r in runs:
                print(f"  {r['run_id']}  {r['status']:<24s}  {r['goal']}")
        return

    data = load_run(run_id)
    if data is None:
        print(f"Error: run {run_id!r} not found.", file=sys.stderr)
        sys.exit(1)

    if json_output:
        from packages.orchestration.pingpong_promote import load_promotion
        promo = load_promotion(run_id)
        if promo:
            data["promotion"] = promo
        print(json.dumps(data, indent=2))
    else:
        _print_text_report(run_id, data)


def _print_text_report(run_id: str, data: dict) -> None:
    """Print concise user-facing text report."""
    # Header
    print(f"Remedy Run {run_id}")
    print(f"Goal: {data.get('goal', '')}")
    print(f"Status: {data.get('final_status', '')}")
    print()

    # Provider evidence
    pe = data.get("provider_evidence", {})
    if pe:
        b_kind = pe.get("builder_provider_kind", "")
        r_kind = pe.get("reviewer_provider_kind", "")
        b_wm = pe.get("builder_write_mode", "none")
        r_wm = pe.get("reviewer_write_mode", "none")
        b_label = f"{data.get('builder_provider', 'unknown')} ({b_kind}, write mode: {b_wm})" if b_kind else data.get("builder_provider", "unknown")
        r_label = f"{data.get('reviewer_provider', 'unknown')} ({r_kind}, write mode: {r_wm})" if r_kind else data.get("reviewer_provider", "unknown")
        print(f"Worker: {b_label}")
        print(f"Reviewer: {r_label}")
    else:
        print(f"Worker: {data.get('builder_provider', 'unknown')}")
        print(f"Reviewer: {data.get('reviewer_provider', 'unknown')}")

    # Rounds summary
    rounds = data.get("rounds", [])
    total = data.get("total_rounds", len(rounds))
    max_r = data.get("max_rounds", 0)
    print(f"Rounds: {total}/{max_r}")

    # Test summary from last round
    if rounds:
        last = rounds[-1]
        test_status = "passed" if last.get("test_passed") else "failed"
        print(f"Tests: {test_status}")
        rv = last.get("reviewer", {})
        if rv:
            print(f"Reviewer verdict: {rv.get('verdict', 'none')}")

    # Target mutation
    mutated = data.get("target_mutated", False)
    print(f"Target touched during run: {'yes' if mutated else 'no'}")

    if data.get("error"):
        print(f"Error: {data['error']}")

    # Staged files
    staged = data.get("staged_files", [])
    if staged:
        print("\nChanged in staging:")
        for f in staged:
            print(f"  - {f}")

    # Promotion
    from packages.orchestration.pingpong_promote import load_promotion
    promo = load_promotion(run_id)
    if promo:
        print(f"\nPromotion: {promo.get('status', 'unknown')}")
        if promo.get("applied_files"):
            print("Promoted to repo:")
            for f in promo["applied_files"]:
                print(f"  - {f}")
        if promo.get("post_test_passed") is not None:
            print(f"Post-promotion tests: {'passed' if promo['post_test_passed'] else 'FAILED'}")
        if promo.get("blocked_reason"):
            print(f"Blocked: {promo['blocked_reason']}")
        if promo.get("unexpected_artifacts"):
            print(f"Unexpected artifacts: {', '.join(promo['unexpected_artifacts'])}")
        if promo.get("duplicate_artifacts"):
            print(f"Duplicate artifacts: {', '.join(promo['duplicate_artifacts'])}")
        if promo.get("target_repo_mismatch"):
            print(f"Run repo: {promo.get('run_repo', '')}")
            print(f"Requested target: {promo.get('requested_target_repo', '')}")
    else:
        print("\nPromotion: not promoted")
        if data.get("final_status") == "staged_review_passed":
            print("\nNext steps:")
            print(f"  remedy do promote {run_id} --repo . --dry-run")
            print(f"  remedy do promote {run_id} --repo . --approve")

    # Token accounting
    ta = data.get("token_accounting", {})
    if ta:
        kind = ta.get("kind", "estimated")
        print(f"\nToken accounting: {kind}")
        ctx_est = ta.get("context_tokens_estimated", 0)
        if ctx_est:
            print(f"  Context sent: ~{ctx_est} tokens")
        full_est = ta.get("full_repo_tokens_estimated", 0)
        if full_est:
            print(f"  Full repo estimate: ~{full_est} tokens")
        savings = ta.get("estimated_context_savings_tokens", 0)
        ratio = ta.get("estimated_context_savings_ratio", 0.0)
        if savings > 0:
            pct = int(ratio * 100)
            print(f"  Estimated saved: ~{savings} tokens (~{pct}%)")
        if ta.get("token_note"):
            print(f"  Note: {ta['token_note']}")


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


def _cmd_do_promote(
    run_id: str,
    *,
    repo: str = ".",
    approve: bool = False,
    dry_run: bool = False,
    test_command: str = "",
    json_output: bool = False,
) -> None:
    """Promote reviewed staged artifacts into target repo."""
    from packages.orchestration.pingpong_promote import (
        export_promotion_json,
        promote_run,
        summarize_promotion,
    )

    result = promote_run(
        run_id,
        target_repo=repo,
        approve=approve,
        dry_run=dry_run,
        test_command=test_command,
    )

    if json_output:
        print(json.dumps(export_promotion_json(result), indent=2))
    else:
        print(summarize_promotion(result))


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
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
        builder=getattr(args, "builder", None) or "none",
        reviewer=getattr(args, "reviewer", None) or "none",
        max_rounds=int(getattr(args, "max_rounds", None) or 3),
        mode=getattr(args, "mode", None) or "staged",
        test_command=getattr(args, "test_command", None) or "",
        provider_timeout_sec=int(getattr(args, "provider_timeout_sec", None) or 120),
        max_output_chars_val=int(getattr(args, "max_output_chars", None) or 50000),
        keep_staging=getattr(args, "keep_staging", False),
        claude_cli_write_mode=getattr(args, "claude_cli_write_mode", None) or "none",
    ),
    "do.promote": lambda args: _cmd_do_promote(
        args.run_id,
        repo=getattr(args, "repo", None) or ".",
        approve=getattr(args, "approve", False),
        dry_run=getattr(args, "dry_run", False),
        test_command=getattr(args, "test_command", None) or "",
        json_output=getattr(args, "json", False),
    ),
    "do.report": lambda args: _cmd_do_report(
        args.run_id,
        json_output=getattr(args, "json", False),
    ),
    "do.continue": lambda args: _cmd_do_continue(
        args.job_id,
        intent_id=getattr(args, "intent_id", None),
        json_output=getattr(args, "json", False),
    ),
}
