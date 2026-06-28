"""CLI handler for ``remedy do`` — high-level guided autorun."""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

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
    task_file: str = "",
    task_stdin: bool = False,
    scope_file: str = "",
    approve_scope: bool = False,
    repair_rounds: int | None = None,
) -> None:
    # --- Task input loading ---
    task_input = None
    if task_file and task_stdin:
        print("Error: cannot use both --task-file and --task-stdin.", file=sys.stderr)
        sys.exit(2)
    if task_file:
        from packages.orchestration.pingpong_loop import load_task_file
        try:
            task_input = load_task_file(task_file)
        except ValueError as exc:
            if json_output:
                print(json.dumps({"error": str(exc)}, indent=2))
            else:
                print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)
    elif task_stdin:
        from packages.orchestration.pingpong_loop import load_task_stdin
        stdin_text = sys.stdin.read()
        try:
            task_input = load_task_stdin(stdin_text)
        except ValueError as exc:
            if json_output:
                print(json.dumps({"error": str(exc)}, indent=2))
            else:
                print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)

    # Require at least goal or task input
    if not goal and not task_input:
        print("Error: provide a goal or --task-file/--task-stdin.", file=sys.stderr)
        sys.exit(2)

    # --- Scope file validation ---
    scope_validation = None
    scope_data = None
    if scope_file and not approve_scope:
        print("Error: --scope-file requires --approve-scope to confirm decisions.", file=sys.stderr)
        sys.exit(2)
    if scope_file and approve_scope:
        from packages.orchestration.scope_plan import load_scope_plan, validate_scope_plan
        try:
            scope_data = load_scope_plan(scope_file)
        except ValueError as exc:
            if json_output:
                print(json.dumps({"error": str(exc)}, indent=2))
            else:
                print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)
        scope_validation = validate_scope_plan(
            scope_data,
            task_sha256=task_input.sha256 if task_input else "",
            repo_path=repo,
        )
        if not scope_validation.valid:
            msg = "Scope validation failed:\n" + "\n".join(f"  - {e}" for e in scope_validation.errors)
            if json_output:
                print(json.dumps({"error": msg, "scope_errors": scope_validation.errors}, indent=2))
            else:
                print(f"Error: {msg}", file=sys.stderr)
            sys.exit(2)

    # Resolve and validate repair_rounds
    from packages.orchestration.pingpong_loop import resolve_repair_rounds
    try:
        repair_rounds_val, repair_rounds_source = resolve_repair_rounds(repair_rounds)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)
    repair_rounds = repair_rounds_val

    # Ping-pong mode: --builder and/or --reviewer set to a real provider
    if builder != "none" or reviewer != "none":
        _cmd_do_pingpong(
            goal, repo=repo, builder=builder, reviewer=reviewer,
            max_rounds=max_rounds, mode=mode, json_output=json_output,
            test_command=test_command, provider_timeout_sec=provider_timeout_sec,
            max_output_chars=max_output_chars_val, keep_staging=keep_staging,
            claude_cli_write_mode=claude_cli_write_mode,
            task_input=task_input,
            scope_data=scope_data,
            scope_validation=scope_validation,
            repair_rounds=repair_rounds,
            repair_rounds_source=repair_rounds_source,
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
    task_input: Any = None,
    scope_data: dict[str, Any] | None = None,
    scope_validation: Any = None,
    repair_rounds: int = 0,
    repair_rounds_source: str = "",
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
        if repair_rounds > 0:
            print(f"Repair rounds: {repair_rounds}")
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
        task_input=task_input,
        scope_data=scope_data,
        scope_validation=scope_validation,
        repair_rounds=repair_rounds,
        repair_rounds_source=repair_rounds_source,
    )

    data = export_pingpong_json(result)

    # Inject scope plan data into report
    if scope_data and scope_validation:
        from packages.orchestration.scope_plan import (
            build_scope_report_data,
            check_scope_hints,
        )
        hints = check_scope_hints(
            result.staged_files,
            result.safe_diff_summary,
            approved_features=scope_validation.approved_features,
            denied_features=scope_validation.denied_features,
            deferred_features=scope_validation.deferred_features,
            backlog_features=scope_validation.backlog_features,
        )
        data["scope_plan"] = build_scope_report_data(
            scope_data, scope_validation, scope_hints=hints,
        )
    else:
        data["scope_plan"] = None

    if json_output:
        print(json.dumps(data, indent=2))
    else:
        print(summarize_pingpong(result))
        # Scope summary in text report
        if scope_validation:
            _print_scope_summary(scope_validation)


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


def _cmd_do_evidence(
    run_id: str,
    *,
    out: str = "",
    json_output: bool = False,
) -> None:
    """Export a self-contained evidence bundle for a persisted run."""
    from packages.orchestration.pingpong_evidence import export_evidence

    if not out:
        out = f"remedy-evidence-{run_id}"

    result = export_evidence(run_id, out)

    if result.get("error"):
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(json.dumps(result, indent=2))
    else:
        print(f"Evidence bundle exported to: {result['out_dir']}")
        for filename, path in result.get("files", {}).items():
            print(f"  {filename}")
        status = result.get("manifest", {}).get("final_status", "")
        readiness = result.get("manifest", {}).get("promotion_readiness", {})
        print(f"\nRun status: {status}")
        print(f"Promotion ready: {readiness.get('ready', False)}")


def _print_text_report(run_id: str, data: dict) -> None:
    """Print concise user-facing text report."""
    # Header
    print(f"Remedy Run {run_id}")
    print(f"Goal: {data.get('goal', '')}")
    print(f"Status: {data.get('final_status', '')}")
    print()

    # Task input info
    ti = data.get("task_input")
    if ti:
        kind_label = ti.get("kind", "")
        title = ti.get("title", "")
        sha = ti.get("sha256", "")[:12]
        tokens = ti.get("tokens_estimated", 0)
        print(f"Task input: {kind_label}" + (f" ({title})" if title else ""))
        print(f"Task size: ~{tokens} tokens")
        print(f"Task hash: {sha}...")
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

    # Worker self-report vs Remedy verification (Step 4718)
    if rounds:
        last = rounds[-1]
        builder_info = last.get("builder", {})
        if builder_info:
            summary = builder_info.get("summary", "")
            if summary:
                print(f"\nWorker self-report: {summary[:200]}")

        # Remedy verification
        test_status = "passed" if last.get("test_passed") else "failed"
        print(f"Remedy verification: tests {test_status}")
        rv = last.get("reviewer", {})
        if rv:
            print(f"Reviewer verdict: {rv.get('verdict', 'none')}")

    # Scope summary (Step 4717)
    sp = data.get("scope_plan")
    if sp:
        approved = [f["id"] for f in sp.get("approved_features", [])]
        denied = [f["id"] for f in sp.get("denied_features", [])]
        deferred = [f["id"] for f in sp.get("deferred_features", [])]
        backlog = [f["id"] for f in sp.get("backlog_features", [])]
        pending = [f["id"] for f in sp.get("pending_features", [])]
        print("\nScope:")
        print(f"  Approved: {', '.join(approved) if approved else 'none'}")
        print(f"  Denied: {', '.join(denied) if denied else 'none'}")
        print(f"  Deferred: {', '.join(deferred) if deferred else 'none'}")
        print(f"  Backlog: {', '.join(backlog) if backlog else 'none'}")
        print(f"  Pending: {', '.join(pending) if pending else 'none'}")

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


def _print_scope_summary(validation: Any) -> None:
    """Print concise scope summary for text report."""
    print("\nScope:")
    approved = [f.id for f in validation.approved_features]
    denied = [f.id for f in validation.denied_features]
    deferred = [f.id for f in validation.deferred_features]
    backlog = [f.id for f in validation.backlog_features]
    pending = [f.id for f in validation.pending_features]
    print(f"  Approved: {', '.join(approved) if approved else 'none'}")
    print(f"  Denied: {', '.join(denied) if denied else 'none'}")
    print(f"  Deferred: {', '.join(deferred) if deferred else 'none'}")
    print(f"  Backlog: {', '.join(backlog) if backlog else 'none'}")
    print(f"  Pending: {', '.join(pending) if pending else 'none'}")


def _cmd_do_plan(
    *,
    task_file: str = "",
    repo: str = ".",
    json_output: bool = False,
) -> None:
    """Create a deterministic scope plan from a task file."""
    if not task_file:
        print("Error: --task-file is required for planning.", file=sys.stderr)
        sys.exit(2)

    from packages.orchestration.pingpong_loop import load_task_file
    try:
        task_input = load_task_file(task_file)
    except ValueError as exc:
        if json_output:
            print(json.dumps({"error": str(exc)}, indent=2))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    from packages.orchestration.scope_plan import (
        export_scope_plan,
        extract_scope_plan,
        persist_scope_plan,
    )

    plan = extract_scope_plan(
        task_input.body,
        task_sha256=task_input.sha256,
        repo_path=repo,
        task_title=task_input.title,
        task_input_kind=task_input.kind,
        task_tokens_estimated=task_input.tokens_estimated,
    )
    scope_file = persist_scope_plan(plan)
    data = export_scope_plan(plan)

    if json_output:
        print(json.dumps(data, indent=2))
    else:
        print(f"Scope plan created: {plan.plan_id}")
        print(f"Task: {plan.task_title}")
        print(f"Features: {len(plan.features)}")
        for f in plan.features:
            marker = "*" if f.default_selected else " "
            print(f"  [{marker}] {f.id}: {f.title} ({f.status})")
        if plan.warnings:
            for w in plan.warnings:
                print(f"  Warning: {w}")
        print(f"\nScope file: {scope_file}")
        print("Edit user_decision in the scope file, then run:")
        print(f"  remedy do run --task-file {task_file} --scope-file {scope_file} --approve-scope --repo {repo}")


def _cmd_do_job_plan(
    *,
    job_file: str = "",
    repo: str = ".",
    json_output: bool = False,
) -> None:
    """Parse a job file into ordered tasks (no provider calls)."""
    from packages.orchestration.pingpong_job import plan_job_from_file

    if not job_file:
        print("Error: --job-file is required", file=sys.stderr)
        sys.exit(1)

    job = plan_job_from_file(job_file, repo)

    if job.error:
        print(f"Error: {job.error}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(json.dumps({
            "job_id": job.job_id,
            "job_title": job.job_title,
            "status": job.status,
            "tasks": [
                {"task_id": t.task_id, "title": t.title, "status": t.status}
                for t in job.tasks
            ],
            "next_command": f"remedy do job-run {job.job_id}",
        }, indent=2))
    else:
        print(f"Job planned: {job.job_id}")
        print(f"Title: {job.job_title}")
        print(f"Tasks: {len(job.tasks)}")
        for t in job.tasks:
            print(f"  {t.task_id}: {t.title}")
        print(f"\nNext: remedy do job-run {job.job_id}")


def _cmd_do_job_run(
    job_id: str,
    *,
    builder: str | None = None,
    reviewer: str | None = None,
    max_rounds: int | None = None,
    repair_rounds: int | None = None,
    test_command: str | None = None,
    claude_cli_write_mode: str | None = None,
    max_tasks: int = 0,
    json_output: bool = False,
) -> None:
    """Run pending tasks sequentially through the ping-pong loop.

    None means "omitted by CLI". Resolution in run_job():
    explicit CLI value > persisted config > product default.
    """
    if builder is not None and builder not in _VALID_PINGPONG_PROVIDERS:
        print(f"Error: invalid --builder: {builder!r}. Allowed: {', '.join(sorted(_VALID_PINGPONG_PROVIDERS))}.", file=sys.stderr)
        sys.exit(2)
    if reviewer is not None and reviewer not in _VALID_PINGPONG_PROVIDERS:
        print(f"Error: invalid --reviewer: {reviewer!r}. Allowed: {', '.join(sorted(_VALID_PINGPONG_PROVIDERS))}.", file=sys.stderr)
        sys.exit(2)
    if claude_cli_write_mode is not None and claude_cli_write_mode not in _VALID_CLI_WRITE_MODES:
        print(
            f"Error: invalid --claude-cli-write-mode: {claude_cli_write_mode!r}. "
            f"Allowed: {', '.join(sorted(_VALID_CLI_WRITE_MODES))}.",
            file=sys.stderr,
        )
        sys.exit(2)

    repair_rounds_val: int | None = None
    repair_source: str | None = None
    if repair_rounds is not None:
        from packages.orchestration.pingpong_loop import resolve_repair_rounds
        try:
            repair_rounds_val, repair_source = resolve_repair_rounds(repair_rounds)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)

    from packages.orchestration.pingpong_job import (
        export_job_report,
        run_job,
    )

    job = run_job(
        job_id,
        builder_name=builder,
        reviewer_name=reviewer,
        max_rounds=max_rounds,
        repair_rounds=repair_rounds_val,
        repair_rounds_source=repair_source,
        test_command=test_command,
        claude_cli_write_mode=claude_cli_write_mode,
        max_tasks=max_tasks,
    )

    if json_output:
        print(json.dumps(export_job_report(job), indent=2))
    else:
        from packages.orchestration.pingpong_job import format_job_report_text
        print(format_job_report_text(job))


def _cmd_do_job_evidence(
    job_id: str,
    *,
    out: str = "",
    json_output: bool = False,
) -> None:
    """Export a self-contained evidence bundle for an entire job."""
    from packages.orchestration.job_evidence import export_job_evidence

    if not out:
        out = f"remedy-job-evidence-{job_id}"

    result = export_job_evidence(job_id, out)

    if result.get("error"):
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(json.dumps(result, indent=2))
    else:
        print(f"Job evidence bundle exported to: {result['out_dir']}")
        for filename in sorted(result.get("files", {}).keys()):
            print(f"  {filename}")
        manifest = result.get("manifest", {})
        print(f"\nJob status: {manifest.get('status', '')}")
        print(f"Tasks: {manifest.get('task_count', 0)}")


def _cmd_do_job_promote(
    job_id: str,
    *,
    repo: str = ".",
    approve: bool = False,
    dry_run: bool = False,
    test_command: str = "",
    json_output: bool = False,
) -> None:
    """Review and apply job workspace changes to target repo."""
    from packages.orchestration.job_promote import (
        export_job_promotion_json,
        promote_job,
        summarize_job_promotion,
    )

    if not approve and not dry_run:
        dry_run = True

    result = promote_job(
        job_id,
        target_repo=repo,
        approve=approve,
        dry_run=dry_run,
        test_command=test_command,
    )

    if json_output:
        print(json.dumps(export_job_promotion_json(result), indent=2))
    else:
        print(summarize_job_promotion(result))


def _cmd_do_job_report(
    job_id: str,
    *,
    json_output: bool = False,
) -> None:
    """Show a job report."""
    from packages.orchestration.pingpong_job import (
        export_job_report,
        format_job_report_text,
        load_job_plan,
    )

    job = load_job_plan(job_id)
    if job is None:
        print(f"Error: job not found: {job_id}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(json.dumps(export_job_report(job), indent=2))
    else:
        print(format_job_report_text(job))


def _build_next_approve_command(
    job_id: str, repo: str, test_command: str | None, promote_ready: bool,
) -> str:
    """Build a shell-safe approve command with --repo and --test-command."""
    if not promote_ready:
        return ""
    import shlex
    parts = [f"remedy do job-promote {job_id}"]
    parts.append(f"--repo {shlex.quote(repo)}")
    parts.append("--approve")
    if test_command:
        parts.append(f"--test-command {shlex.quote(test_command)}")
    return " ".join(parts)


def _build_next_approve_command_safe(
    job_id: str, test_command: str | None, promote_ready: bool,
) -> str:
    """Build a shareable approve command with <repo> placeholder."""
    if not promote_ready:
        return ""
    import shlex
    parts = [f"remedy do job-promote {job_id}"]
    parts.append("--repo <repo>")
    parts.append("--approve")
    if test_command:
        parts.append(f"--test-command {shlex.quote(test_command)}")
    return " ".join(parts)


def _build_job_token_summary(job: Any) -> dict[str, Any]:
    """Aggregate token accounting from per-task runs."""
    from packages.orchestration.pingpong_loop import load_run

    builder_calls = 0
    reviewer_calls = 0
    repair_rounds = 0
    est_prompt_total = 0
    est_context_total = 0
    est_diff_total = 0
    est_task_total = 0
    full_repo_est = 0
    actual_input = None
    actual_output = None

    for task in job.tasks:
        if not task.run_id:
            continue
        run_data = load_run(task.run_id)
        if not run_data:
            continue
        ta = run_data.get("token_accounting", {})
        rounds = run_data.get("rounds", [])
        for rd in rounds:
            if rd.get("builder"):
                builder_calls += 1
            if rd.get("reviewer"):
                reviewer_calls += 1
        repair_rounds += run_data.get("repair_loop", {}).get("repair_rounds_used", 0)
        est_prompt_total += (
            ta.get("builder_prompt_tokens_estimated", 0)
            + ta.get("reviewer_prompt_tokens_estimated", 0)
            + ta.get("repair_prompt_tokens_estimated", 0)
        )
        est_context_total += ta.get("context_tokens_estimated", 0)
        est_diff_total += ta.get("safe_diff_tokens_estimated", 0)
        est_task_total += ta.get("task_tokens_estimated", 0)
        fr = ta.get("full_repo_tokens_estimated", 0)
        if fr > full_repo_est:
            full_repo_est = fr

    savings = max(0, full_repo_est - est_context_total) if full_repo_est else 0
    ratio = round(savings / full_repo_est, 4) if full_repo_est else 0.0

    return {
        "provider_call_count": builder_calls + reviewer_calls,
        "builder_call_count": builder_calls,
        "reviewer_call_count": reviewer_calls,
        "repair_round_count": repair_rounds,
        "estimated_prompt_tokens_total": est_prompt_total,
        "estimated_context_tokens_total": est_context_total,
        "estimated_safe_diff_tokens_total": est_diff_total,
        "estimated_task_tokens_total": est_task_total,
        "full_repo_tokens_estimated": full_repo_est,
        "estimated_context_savings_tokens": savings,
        "estimated_context_savings_ratio": ratio,
        "actual_provider_tokens_available": actual_input is not None,
        "actual_provider_input_tokens": actual_input,
        "actual_provider_output_tokens": actual_output,
        "token_note": (
            "All token counts are deterministic estimates from character counts. "
            "Actual provider tokens are unavailable for this run."
        ),
    }


def _build_timeout_hint(
    builder: str | None, reviewer: str | None, timeout_sec: int,
) -> str:
    """Warn when claude-cli providers run under recommended timeout."""
    uses_cli = (builder == "claude-cli" or reviewer == "claude-cli")
    if not uses_cli or timeout_sec >= 900:
        return ""
    return (
        f"Current timeout is {timeout_sec}s. Real claude-cli jobs usually "
        f"need ~900s per provider call. Consider --timeout-sec 900."
    )


def _build_final_audit(
    job: Any,
    promo: Any,
    evidence_out: str,
    *,
    prompt_trace_available: bool | None = None,
    agent_run_trace_available: bool | None = None,
    token_summary: dict[str, Any] | None = None,
    job_flow_json_available: bool | None = None,
) -> dict[str, Any]:
    """Determine overall job-flow audit status from actual evidence."""
    from pathlib import Path

    passed = sum(1 for t in job.tasks if t.status in ("applied_to_job_workspace", "passed", "skipped"))
    blocked = sum(1 for t in job.tasks if t.status == "blocked")
    skipped = sum(1 for t in job.tasks if t.status == "skipped")
    pending = sum(1 for t in job.tasks if t.status == "pending")

    # Derive evidence availability from actual artifacts
    ev_path = Path(evidence_out)
    if prompt_trace_available is None:
        prompt_trace_available = ev_path.joinpath("prompt_trace_summary.json").exists()
    if agent_run_trace_available is None:
        agent_run_trace_available = ev_path.joinpath("agent_run_trace.jsonl").exists()
    token_summary_available = token_summary is not None and token_summary.get("provider_call_count", 0) > 0
    if job_flow_json_available is None:
        job_flow_json_available = ev_path.joinpath("job_flow.json").exists()
    evidence_bundle_available = ev_path.joinpath("manifest.json").exists()

    promote_ready = promo.status == "dry_run"
    all_passed = job.status == "completed" and blocked == 0 and pending == 0

    agent_run_trace_summary_available = ev_path.joinpath("agent_run_trace_summary.json").exists()

    missing_artifacts: list[str] = []
    if not evidence_bundle_available:
        missing_artifacts.append("manifest")
    if not prompt_trace_available:
        missing_artifacts.append("prompt_trace")
    if not agent_run_trace_available:
        missing_artifacts.append("agent_run_trace")
    if not agent_run_trace_summary_available:
        missing_artifacts.append("agent_run_trace_summary")
    if not job_flow_json_available:
        missing_artifacts.append("job_flow_json")
    if not token_summary_available:
        missing_artifacts.append("token_summary")

    if all_passed and promote_ready and not missing_artifacts:
        status = "READY_FOR_APPROVAL"
        action = "Run the next_approve_command to apply changes to the target repo."
    elif all_passed and promote_ready and missing_artifacts:
        status = "NEEDS_REVIEW"
        action = f"Promote-ready but observability artifacts missing: {', '.join(missing_artifacts)}."
    elif blocked > 0 or job.status == "blocked":
        status = "BLOCKED"
        action = "Review blocked tasks, fix issues, and re-run the job."
    else:
        status = "NEEDS_REVIEW"
        action = "Review task results and determine whether to proceed."

    changed_files: list[str] = []
    verdicts: list[str] = []
    test_results: list[str] = []
    for t in job.tasks:
        if hasattr(t, "safe_diff_files") and t.safe_diff_files:
            changed_files.extend(t.safe_diff_files)
        verdicts.append(f"{t.task_id}: {t.reviewer_verdict or 'none'}")
        tp = "pass" if t.test_passed else ("fail" if t.test_passed is False else "not_run")
        test_results.append(f"{t.task_id}: {tp}")

    return {
        "status": status,
        "job_status": job.status,
        "task_count": len(job.tasks),
        "passed_task_count": passed,
        "blocked_task_count": blocked,
        "skipped_task_count": skipped,
        "changed_files": sorted(set(changed_files)),
        "reviewer_verdict_summary": verdicts,
        "test_summary": test_results,
        "evidence_bundle_path": evidence_out,
        "prompt_trace_available": prompt_trace_available,
        "agent_run_trace_available": agent_run_trace_available,
        "token_summary_available": token_summary_available,
        "job_flow_json_available": job_flow_json_available,
        "evidence_bundle_available": evidence_bundle_available,
        "missing_observability_artifacts": missing_artifacts,
        "promote_dry_run_status": promo.status,
        "promote_ready": promote_ready,
        "human_decision_required": True,
        "recommended_next_action": action,
        "known_limitations": [
            "Actual provider token counts unavailable for fake/claude-cli providers.",
            "Prompt traces are redacted estimates, not exact provider-side records.",
        ],
    }


def _sanitize_shareable_paths(obj: Any) -> Any:
    """Recursively sanitize absolute private paths in shareable JSON.

    Catches /tmp/*, /home/*, /Users/*, /private/* to prevent leaking
    local filesystem structure in shareable evidence bundles.
    """
    import re

    _STAGING_RE = re.compile(r"/tmp/remedy-pingpong-[a-f0-9]+[^\s\"']*")
    _TMP_RE = re.compile(r"/tmp/[a-zA-Z0-9._-]+[^\s\"']*")
    _HOME_RE = re.compile(r"/home/[a-zA-Z0-9._-]+[^\s\"']*")
    _USERS_RE = re.compile(r"/Users/[a-zA-Z0-9._-]+[^\s\"']*")
    _PRIVATE_RE = re.compile(r"/private/[a-zA-Z0-9._-]+[^\s\"']*")

    if isinstance(obj, str):
        obj = _STAGING_RE.sub("[staging]", obj)
        obj = _TMP_RE.sub("[tmpdir]", obj)
        obj = _HOME_RE.sub("[local]", obj)
        obj = _USERS_RE.sub("[local]", obj)
        obj = _PRIVATE_RE.sub("[local]", obj)
        return obj
    if isinstance(obj, dict):
        return {k: _sanitize_shareable_paths(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_shareable_paths(v) for v in obj]
    return obj


def _persist_evidence_index(job_id: str, evidence_out: str, trace_summary: dict) -> None:
    """Write evidence location index under Remedy data dir for cockpit bridge."""
    from datetime import datetime, timezone
    from pathlib import Path

    try:
        from packages.orchestration.data_paths import resolve_data_root
        idx_dir = resolve_data_root() / "job_evidence_index"
        idx_dir.mkdir(parents=True, exist_ok=True)
        ev_path = Path(evidence_out).resolve()
        record = {
            "job_id": job_id,
            "evidence_dir_local": str(ev_path),
            "has_agent_run_trace": (ev_path / "agent_run_trace.jsonl").exists(),
            "has_job_flow_json": (ev_path / "job_flow.json").exists(),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "source_command": "do.job-flow",
        }
        (idx_dir / f"{job_id}.json").write_text(
            json.dumps(record, indent=2) + "\n"
        )
    except (ImportError, OSError):
        pass


def _persist_job_flow_json(flow_result: dict, evidence_out: str) -> None:
    """Write job_flow.json to evidence output directory."""
    from pathlib import Path
    out_path = Path(evidence_out).resolve()
    out_path.mkdir(parents=True, exist_ok=True)
    target = out_path / "job_flow.json"
    sanitized = _sanitize_shareable_paths(flow_result)
    target.write_text(json.dumps(sanitized, indent=2) + "\n")


def _print_token_summary(ts: dict) -> None:
    """Print concise Token / Context section."""
    print("Token / Context:")
    print(f"  Provider calls: {ts['provider_call_count']} "
          f"(builder: {ts['builder_call_count']}, reviewer: {ts['reviewer_call_count']})")
    print(f"  Repair rounds: {ts['repair_round_count']}")
    print(f"  Estimated prompt tokens: {ts['estimated_prompt_tokens_total']}")
    print(f"  Estimated context tokens: {ts['estimated_context_tokens_total']}")
    if ts["full_repo_tokens_estimated"]:
        pct = round(ts["estimated_context_savings_ratio"] * 100, 1)
        print(f"  Full repo tokens: {ts['full_repo_tokens_estimated']} "
              f"(context savings: {pct}%)")
    print()


def _print_blocked_diagnostics(job: Any) -> None:
    """Print blocked/skipped task diagnostics if any."""
    blocked = [t for t in job.tasks if t.status == "blocked"]
    skipped = [t for t in job.tasks if t.status == "skipped"]
    if not blocked and not skipped:
        return
    if blocked:
        print("Blocked tasks:")
        for t in blocked:
            print(f"  T{t.task_id}: {t.title}")
            print(f"    Reason: {t.error or 'unknown'}")
        print()
    if skipped:
        print("Skipped tasks:")
        for t in skipped:
            print(f"  T{t.task_id}: {t.title}")
        print()


def _print_final_audit(audit: dict) -> None:
    """Print final audit section."""
    print()
    print(f"Final audit: {audit['status']}")
    print(f"  Tasks: {audit['passed_task_count']}/{audit['task_count']} passed"
          f"{', ' + str(audit['blocked_task_count']) + ' blocked' if audit['blocked_task_count'] else ''}"
          f"{', ' + str(audit['skipped_task_count']) + ' skipped' if audit['skipped_task_count'] else ''}")
    print(f"  Recommended: {audit['recommended_next_action']}")
    print("  Human approval is required before the target repo is changed.")


def _load_prompt_trace_index(run_id: str) -> dict[tuple[int, str], dict]:
    """Load prompt trace entries for a run and index by (round, role)."""
    from packages.orchestration.pingpong_loop import _pingpong_runs_dir

    index: dict[tuple[int, str], dict] = {}
    trace_path = _pingpong_runs_dir() / run_id / "prompt_trace.jsonl"
    if not trace_path.exists():
        return index
    for line in trace_path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            key = (entry.get("round", 0), entry.get("role", ""))
            index[key] = entry
        except json.JSONDecodeError:
            continue
    return index


def _build_agent_run_trace(
    job: Any,
    promo: Any,
    evidence_result: dict,
    builder_name: str | None,
    reviewer_name: str | None,
) -> list:
    """Build agent run trace events from completed job state.

    All events are marked trace_source="reconstructed" because they are
    derived post-hoc from persisted run data, not captured live.
    """
    from packages.orchestration.agent_run_trace import create_trace_event
    from packages.orchestration.pingpong_loop import _provider_kind, load_run

    _SRC = "reconstructed"
    events = []
    job_id = job.job_id
    b_kind = _provider_kind(builder_name or "fake")
    r_kind = _provider_kind(reviewer_name or "fake")

    events.append(create_trace_event(
        "job_flow_started", job_id=job_id,
        safe_summary=f"Job flow started: {job.job_title}",
        trace_source=_SRC,
    ))
    events.append(create_trace_event(
        "job_planned", job_id=job_id,
        safe_summary=f"{len(job.tasks)} tasks planned",
        status=job.status,
        trace_source=_SRC,
    ))

    for task in job.tasks:
        events.append(create_trace_event(
            "task_started", job_id=job_id, task_id=task.task_id,
            safe_summary=task.title[:200],
            trace_source=_SRC,
        ))

        if not task.run_id:
            events.append(create_trace_event(
                "task_gate_evaluated", job_id=job_id, task_id=task.task_id,
                status=task.status,
                outcome="skipped" if task.status == "skipped" else "no_run",
                safe_summary=task.error or task.status,
                trace_source=_SRC,
            ))
            continue

        run_data = load_run(task.run_id)
        if not run_data:
            continue

        pt_index = _load_prompt_trace_index(task.run_id)
        pt_refs = [f"prompt_trace.jsonl:{task.run_id}"] if pt_index else []

        rounds = run_data.get("rounds", [])
        for rd in rounds:
            round_num = rd.get("round", 0)

            if rd.get("builder"):
                is_repair = round_num > 1
                pt_entry = pt_index.get((round_num, "builder"), {})
                events.append(create_trace_event(
                    "repair_prompt_created" if is_repair else "builder_prompt_created",
                    job_id=job_id, task_id=task.task_id, run_id=task.run_id,
                    round_num=round_num, role="builder",
                    provider=builder_name or "fake", provider_kind=b_kind,
                    prompt_kind="repair" if is_repair else "initial",
                    prompt_sha256=pt_entry.get("prompt_sha256", ""),
                    prompt_chars=pt_entry.get("prompt_chars", 0),
                    trace_source=_SRC,
                    source_artifact_refs=pt_refs,
                ))
                events.append(create_trace_event(
                    "repair_output_received" if is_repair else "builder_output_received",
                    job_id=job_id, task_id=task.task_id, run_id=task.run_id,
                    round_num=round_num, role="builder",
                    provider=builder_name or "fake", provider_kind=b_kind,
                    changed_files_safe=rd.get("staged_files", [])[:20],
                    trace_source=_SRC,
                ))

            if rd.get("reviewer"):
                reviewer_data = rd.get("reviewer", {})
                verdict = reviewer_data.get("verdict", "")
                findings = reviewer_data.get("findings", [])
                finding_ids = [f.get("id", "") for f in findings if isinstance(f, dict)][:20]

                is_repair = round_num > 1
                pt_entry = pt_index.get((round_num, "reviewer"), {})
                events.append(create_trace_event(
                    "reviewer_prompt_created",
                    job_id=job_id, task_id=task.task_id, run_id=task.run_id,
                    round_num=round_num, role="reviewer",
                    provider=reviewer_name or "fake", provider_kind=r_kind,
                    prompt_kind="re-review" if is_repair else "review",
                    prompt_sha256=pt_entry.get("prompt_sha256", ""),
                    prompt_chars=pt_entry.get("prompt_chars", 0),
                    trace_source=_SRC,
                    source_artifact_refs=pt_refs,
                ))
                events.append(create_trace_event(
                    "reviewer_output_received",
                    job_id=job_id, task_id=task.task_id, run_id=task.run_id,
                    round_num=round_num, role="reviewer",
                    provider=reviewer_name or "fake", provider_kind=r_kind,
                    verdict=verdict, finding_ids=finding_ids,
                    trace_source=_SRC,
                ))

                for fid in finding_ids:
                    events.append(create_trace_event(
                        "review_finding_rechecked" if is_repair else "review_finding_opened",
                        job_id=job_id, task_id=task.task_id, run_id=task.run_id,
                        round_num=round_num, finding_ids=[fid],
                        trace_source=_SRC,
                    ))

        events.append(create_trace_event(
            "task_gate_evaluated", job_id=job_id, task_id=task.task_id,
            run_id=task.run_id,
            status=task.status, verdict=task.reviewer_verdict or "",
            outcome="pass" if task.status in ("applied_to_job_workspace", "passed") else task.status,
            trace_source=_SRC,
        ))

        if task.status == "applied_to_job_workspace":
            safe_files = task.safe_diff_files[:20] if task.safe_diff_files else []
            events.append(create_trace_event(
                "task_workspace_applied", job_id=job_id, task_id=task.task_id,
                run_id=task.run_id, changed_files_safe=safe_files,
                trace_source=_SRC,
            ))

    if not evidence_result.get("error"):
        events.append(create_trace_event(
            "job_evidence_exported", job_id=job_id,
            safe_summary=f"{len(evidence_result.get('files', {}))} files exported",
            trace_source=_SRC,
        ))

    events.append(create_trace_event(
        "promotion_dry_run_completed", job_id=job_id,
        status=promo.status,
        outcome="ready" if promo.status == "dry_run" else "blocked",
        safe_summary=promo.blocked_reason or "dry_run_complete",
        trace_source=_SRC,
    ))

    return events


def _cmd_do_job_flow(
    *,
    job_file: str = "",
    repo: str = ".",
    builder: str | None = None,
    reviewer: str | None = None,
    max_rounds: int | None = None,
    repair_rounds: int | None = None,
    test_command: str | None = None,
    claude_cli_write_mode: str | None = None,
    timeout_sec: int = 120,
    out: str = "",
    json_output: bool = False,
) -> None:
    """Compose the safe job workflow as one human-readable command.

    Runs, in order: job-plan → job-run → job-report → job-evidence →
    job-promote --dry-run. It stops before an approved promote: the real
    target repo is never mutated and no git commit/push/reset/checkout is
    performed. When the dry-run is ready, a clear next approve command is
    printed.
    """
    if not job_file:
        print("Error: --job-file is required", file=sys.stderr)
        sys.exit(2)
    if builder is not None and builder not in _VALID_PINGPONG_PROVIDERS:
        print(f"Error: invalid --builder: {builder!r}. Allowed: {', '.join(sorted(_VALID_PINGPONG_PROVIDERS))}.", file=sys.stderr)
        sys.exit(2)
    if reviewer is not None and reviewer not in _VALID_PINGPONG_PROVIDERS:
        print(f"Error: invalid --reviewer: {reviewer!r}. Allowed: {', '.join(sorted(_VALID_PINGPONG_PROVIDERS))}.", file=sys.stderr)
        sys.exit(2)
    if claude_cli_write_mode is not None and claude_cli_write_mode not in _VALID_CLI_WRITE_MODES:
        print(
            f"Error: invalid --claude-cli-write-mode: {claude_cli_write_mode!r}. "
            f"Allowed: {', '.join(sorted(_VALID_CLI_WRITE_MODES))}.",
            file=sys.stderr,
        )
        sys.exit(2)

    repair_rounds_val: int | None = None
    repair_source: str | None = None
    if repair_rounds is not None:
        from packages.orchestration.pingpong_loop import resolve_repair_rounds
        try:
            repair_rounds_val, repair_source = resolve_repair_rounds(repair_rounds)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)

    from packages.orchestration.pingpong_job import (
        export_job_report,
        format_job_report_text,
        load_job_plan,
        plan_job_from_file,
        run_job,
    )

    # --- 1. job-plan ---
    job = plan_job_from_file(job_file, repo)
    if job.error:
        print(f"Error: {job.error}", file=sys.stderr)
        sys.exit(1)
    job_id = job.job_id

    # --- 2. job-run (timeout flows into the real runner/provider) ---
    job = run_job(
        job_id,
        builder_name=builder,
        reviewer_name=reviewer,
        max_rounds=max_rounds,
        repair_rounds=repair_rounds_val,
        repair_rounds_source=repair_source,
        test_command=test_command,
        timeout_sec=timeout_sec,
        claude_cli_write_mode=claude_cli_write_mode,
        max_tasks=0,
    )

    # --- 3. job-report (reload for an authoritative view) ---
    report_job = load_job_plan(job_id) or job
    report_data = export_job_report(report_job)

    # --- 4. job-evidence ---
    from packages.orchestration.job_evidence import export_job_evidence
    evidence_out = out or f"remedy-job-evidence-{job_id}"
    evidence_result = export_job_evidence(job_id, evidence_out)

    # --- 5. job-promote --dry-run (stops before approved promote) ---
    from packages.orchestration.job_promote import (
        export_job_promotion_json,
        promote_job,
    )
    promo = promote_job(
        job_id,
        target_repo=repo,
        approve=False,
        dry_run=True,
        test_command=test_command or "",
    )

    promote_ready = promo.status == "dry_run"
    next_approve_command = _build_next_approve_command(
        job_id, repo, test_command, promote_ready,
    )
    next_approve_command_safe = _build_next_approve_command_safe(
        job_id, test_command, promote_ready,
    )

    # --- 6. Build agent run trace ---
    from pathlib import Path as _Path

    from packages.orchestration.agent_run_trace import (
        build_trace_summary as build_run_trace_summary,
    )
    from packages.orchestration.agent_run_trace import (
        create_trace_event,
    )
    from packages.orchestration.agent_run_trace import (
        write_trace_jsonl as write_run_trace_jsonl,
    )

    run_trace_events = _build_agent_run_trace(
        report_job, promo, evidence_result, builder, reviewer,
    )

    ev_path = _Path(evidence_out).resolve()
    ev_path.mkdir(parents=True, exist_ok=True)
    write_run_trace_jsonl(run_trace_events, ev_path / "agent_run_trace.jsonl")
    run_trace_summary = build_run_trace_summary(run_trace_events)
    (ev_path / "agent_run_trace_summary.json").write_text(
        json.dumps(run_trace_summary, indent=2) + "\n"
    )

    # --- 7. Build observability: token summary, final audit, timeout hint ---
    token_summary = _build_job_token_summary(report_job)
    final_audit = _build_final_audit(
        report_job, promo, evidence_out,
        token_summary=token_summary,
        job_flow_json_available=True,
    )
    timeout_warning = _build_timeout_hint(builder, reviewer, timeout_sec)

    # Add final_audit_completed to trace
    run_trace_events.append(create_trace_event(
        "final_audit_completed",
        job_id=job_id,
        status=final_audit["status"],
        safe_summary=final_audit["recommended_next_action"],
        trace_source="reconstructed",
    ))
    # Re-persist trace and summary with final event
    write_run_trace_jsonl(run_trace_events, ev_path / "agent_run_trace.jsonl")
    run_trace_summary = build_run_trace_summary(run_trace_events)
    (ev_path / "agent_run_trace_summary.json").write_text(
        json.dumps(run_trace_summary, indent=2) + "\n"
    )

    # --- 8. Persist job_flow.json to evidence output ---
    flow_result = {
        "command": "do.job-flow",
        "job_id": job_id,
        "steps": ["job-plan", "job-run", "job-report", "job-evidence", "job-promote-dry-run"],
        "report": report_data,
        "evidence": evidence_result,
        "promote_dry_run": export_job_promotion_json(promo),
        "promote_ready": promote_ready,
        "next_approve_command": next_approve_command,
        "next_approve_command_safe": next_approve_command_safe,
        "token_summary": token_summary,
        "final_audit": final_audit,
        "timeout_warning": timeout_warning,
        "agent_run_trace_summary": run_trace_summary,
    }

    _persist_job_flow_json(flow_result, evidence_out)

    # --- 9. Persist evidence index for cockpit bridge (after job_flow.json) ---
    _persist_evidence_index(job_id, evidence_out, run_trace_summary)

    if json_output:
        safe_result = _sanitize_shareable_paths(flow_result)
        print(json.dumps(safe_result, indent=2))
        return

    print(f"Job flow: {job_file}")
    print(f"Job: {job_id} ({report_job.job_title}) — {len(report_job.tasks)} task(s)")
    print(f"Run status: {report_job.status}")
    print("This flow stops at a promote dry-run. The target repo is not changed.")
    print()
    print(format_job_report_text(report_job))
    print()

    # Blocked/skipped diagnostics
    _print_blocked_diagnostics(report_job)

    if evidence_result.get("error"):
        print(f"Evidence: error: {evidence_result['error']}")
    else:
        print(f"Evidence bundle: {evidence_result.get('out_dir', evidence_out)} (audit trail exported)")
    print()

    # Token / Context section
    _print_token_summary(token_summary)

    if timeout_warning:
        print(f"  Timeout hint: {timeout_warning}")
        print()

    print(f"Promote dry-run: {promo.status}")
    if promote_ready:
        print(f"  Would apply {len(promo.files_planned)} file(s). No target files changed.")
        print("  The target repo stays unchanged until you explicitly approve the promote.")
        print("\nNext (approval required):")
        print(f"  {next_approve_command}")
    else:
        print(f"  Not ready to promote: {promo.blocked_reason or 'see report'}")
        print("  The target repo was not changed.")

    # Final audit
    _print_final_audit(final_audit)


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "do.run": lambda args: _cmd_do(
        getattr(args, "goal", None) or "",
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
        task_file=getattr(args, "task_file", None) or "",
        task_stdin=getattr(args, "task_stdin", False),
        scope_file=getattr(args, "scope_file", None) or "",
        approve_scope=getattr(args, "approve_scope", False),
        repair_rounds=getattr(args, "repair_rounds", None),
    ),
    "do.plan": lambda args: _cmd_do_plan(
        task_file=getattr(args, "task_file", None) or "",
        repo=getattr(args, "repo", None) or ".",
        json_output=getattr(args, "json", False),
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
    "do.evidence": lambda args: _cmd_do_evidence(
        args.run_id,
        out=getattr(args, "out", None) or "",
        json_output=getattr(args, "json", False),
    ),
    "do.continue": lambda args: _cmd_do_continue(
        args.job_id,
        intent_id=getattr(args, "intent_id", None),
        json_output=getattr(args, "json", False),
    ),
    "do.job-plan": lambda args: _cmd_do_job_plan(
        job_file=getattr(args, "job_file", None) or "",
        repo=getattr(args, "repo", None) or ".",
        json_output=getattr(args, "json", False),
    ),
    "do.job-run": lambda args: _cmd_do_job_run(
        args.job_id,
        builder=getattr(args, "builder", None),
        reviewer=getattr(args, "reviewer", None),
        max_rounds=int(getattr(args, "max_rounds")) if getattr(args, "max_rounds", None) is not None else None,
        repair_rounds=int(getattr(args, "repair_rounds")) if getattr(args, "repair_rounds", None) is not None else None,
        test_command=getattr(args, "test_command", None),
        claude_cli_write_mode=getattr(args, "claude_cli_write_mode", None),
        max_tasks=int(getattr(args, "max_tasks", None) or 0),
        json_output=getattr(args, "json", False),
    ),
    "do.job-report": lambda args: _cmd_do_job_report(
        args.job_id,
        json_output=getattr(args, "json", False),
    ),
    "do.job-promote": lambda args: _cmd_do_job_promote(
        args.job_id,
        repo=getattr(args, "repo", None) or ".",
        approve=getattr(args, "approve", False),
        dry_run=getattr(args, "dry_run", False),
        test_command=getattr(args, "test_command", None) or "",
        json_output=getattr(args, "json", False),
    ),
    "do.job-evidence": lambda args: _cmd_do_job_evidence(
        args.job_id,
        out=getattr(args, "out", None) or "",
        json_output=getattr(args, "json", False),
    ),
    "do.job-flow": lambda args: _cmd_do_job_flow(
        job_file=getattr(args, "job_file", None) or "",
        repo=getattr(args, "repo", None) or ".",
        builder=getattr(args, "builder", None),
        reviewer=getattr(args, "reviewer", None),
        max_rounds=int(getattr(args, "max_rounds")) if getattr(args, "max_rounds", None) is not None else None,
        repair_rounds=int(getattr(args, "repair_rounds")) if getattr(args, "repair_rounds", None) is not None else None,
        test_command=getattr(args, "test_command", None),
        claude_cli_write_mode=getattr(args, "claude_cli_write_mode", None),
        timeout_sec=int(getattr(args, "timeout_sec", None) or 120),
        out=getattr(args, "out", None) or "",
        json_output=getattr(args, "json", False),
    ),
}
