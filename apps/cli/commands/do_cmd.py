"""CLI handler for ``remedy do`` — high-level guided autorun."""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING

from apps.cli.commands.run_invocation import (
    RunInvocation,
)
from apps.cli.commands.run_invocation import (
    invocation_from_args as _invocation_from_args,
)

if TYPE_CHECKING:
    import argparse


_VALID_CLI_WRITE_MODES = frozenset({"none", "allowed-tools", "dangerous-skip"})


# --- Per-role model override flags (T002) ---------------------------------
# CLI accepts --<role>-provider / --<role>-model / --<role>-effort for the
# builder, reviewer, and repair roles. Values are validated at the CLI layer
# before being passed through to role_config.resolve_role_config.
# Exactly the names create_provider (packages/orchestration/pingpong_provider.py) builds.
_VALID_ROLE_PROVIDERS = frozenset({"ollama", "claude", "claude-cli", "fake"})
_VALID_ROLE_EFFORTS = frozenset({"low", "medium", "high", "max"})
_ROLE_OVERRIDE_ROLES = ("builder", "reviewer", "repair")


def _validate_role_override(role: str, field: str, value: object) -> None:
    """Reject an invalid per-role provider/model/effort at the CLI layer.

    ``None`` means "flag omitted" and is always accepted (backward compatible).
    Empty/whitespace-only values and out-of-set providers/efforts exit with
    code 2, matching the other CLI validators.
    """
    if value is None:
        return
    if field == "provider" and value not in _VALID_ROLE_PROVIDERS:
        print(
            f"Error: invalid --{role}-provider: {value!r}. "
            f"Allowed: {', '.join(sorted(_VALID_ROLE_PROVIDERS))}.",
            file=sys.stderr,
        )
        sys.exit(2)
    if field == "effort" and value not in _VALID_ROLE_EFFORTS:
        print(
            f"Error: invalid --{role}-effort: {value!r}. "
            f"Allowed: {', '.join(sorted(_VALID_ROLE_EFFORTS))}.",
            file=sys.stderr,
        )
        sys.exit(2)
    if field == "model" and not str(value).strip():
        print(
            f"Error: invalid --{role}-model: must not be empty.",
            file=sys.stderr,
        )
        sys.exit(2)


def _resolve_cli_role_configs(
    *,
    builder_provider: str | None = None,
    builder_model: str | None = None,
    builder_effort: str | None = None,
    reviewer_provider: str | None = None,
    reviewer_model: str | None = None,
    reviewer_effort: str | None = None,
    repair_provider: str | None = None,
    repair_model: str | None = None,
    repair_effort: str | None = None,
) -> dict[str, dict[str, str]]:
    """Validate per-role override flags and resolve them into role configs.

    Invalid values exit(2) at the CLI layer. Valid overrides are passed through
    to :func:`packages.orchestration.role_config.resolve_role_config`, whose
    result (provider/model/effort per role) is returned as a plain dict.

    When every override is ``None`` the returned configs are the built-in
    defaults, so existing invocations are unaffected (backward compatible).
    """
    from packages.orchestration.role_config import resolve_role_config

    overrides: dict[str, dict[str, str]] = {
        "builder": {
            "provider": builder_provider,
            "model": builder_model,
            "effort": builder_effort,
        },
        "reviewer": {
            "provider": reviewer_provider,
            "model": reviewer_model,
            "effort": reviewer_effort,
        },
        "repair": {
            "provider": repair_provider,
            "model": repair_model,
            "effort": repair_effort,
        },
    }

    resolved: dict[str, dict[str, str]] = {}
    for role in _ROLE_OVERRIDE_ROLES:
        fields = overrides[role]
        for field, value in fields.items():
            _validate_role_override(role, field, value)
        cli_args = {k: v for k, v in fields.items() if v is not None}
        cfg = resolve_role_config(role, cli_args=cli_args)
        resolved[role] = {
            "provider": cfg.provider,
            "model": cfg.model,
            "effort": cfg.effort,
        }
    return resolved


#: DECISION F268 D9 (3): `do.run`'s flags whose feature is not built yet, and that
#: feature. Each refuses with exit 2 before any step; the entry leaves this table
#: in the round its feature lands. `--with-history` is deliberately never declared.
_DO_FLAGS_NOT_YET_AVAILABLE: tuple[tuple[str, str], ...] = (
    ("--contract", "F269"),
    ("--commit", "F270"),
    ("--commit-auto", "F270"),
    ("--commit-with-history", "F270"),
    ("--push", "F270"),
)


def _refuse_do_flags_not_yet_available(given: dict[str, object]) -> None:
    """Exit 2 naming the first flag given whose feature is not built yet, and that feature.

    ``given`` maps each flag of `_DO_FLAGS_NOT_YET_AVAILABLE` to its parsed value;
    ``None`` or ``False`` means the flag was not given.
    """
    for flag, feature in _DO_FLAGS_NOT_YET_AVAILABLE:
        value = given.get(flag)
        if value is not None and value is not False:
            print(f"Error: {flag} is not yet available; {feature} brings it. "
                  f"Nothing was run.", file=sys.stderr)
            sys.exit(2)


def _cmd_do_order(
    order: str,
    *,
    repo: str = ".",
    json_output: bool = False,
    no_llm: bool = False,
    yes: bool = False,
    builder_provider: str | None = None,
    reviewer_provider: str | None = None,
    builder_model: str | None = None,
    reviewer_model: str | None = None,
    planner_model: str | None = None,
    project: str | None = None,
    max_total_tokens: str | None = None,
    max_provider_calls: str | None = None,
    max_wall_clock_minutes: str | None = None,
    max_cost_usd: str | None = None,
    deadline: str | None = None,
    no_ui: bool = False,
    force_job: bool = False,
    force_mission: bool = False,
    step_by_step: bool = False,
    plan_only: bool = False,
    apply: bool = False,
) -> None:
    """`remedy do "<order>"` — walk the F268 sequence (DECISION F268 D4).

    init, study, plan, shape, run, ui and apply, in that order, through
    `packages.orchestration.do_sequence`; the walk stops before apply unless
    `--apply`, and the ui step opens the cockpit detached through
    `launch_do_cockpit` unless `--no-ui` (DECISION F268 D9).
    `--force-job` / `--force-mission` override the planner's shape and exit 2
    together (DECISION F268 D5). `--step-by-step` halts between steps and
    reads each answer with `input`; `--plan-only` ends the walk after
    shape (DECISION F268 D8). `--json` carries `contract: null` until F269
    lands (DECISION F268 D1), `shape` / `shape_source`, `mission_plan_path`
    and `jobs`, every job's tasks with their deliverables. In a walk of two or
    more jobs only the first runs and `waiting_job_ids` names the rest
    (DECISION F268 D12). Every job run is mirrored into the F103 ledger, and
    `do` ends with the measured tokens per role and cost read back from it,
    under `cost` in `--json` (DECISION F268 D11). `--project` selects the
    project the init step uses; the budget flags are resolved before the first
    step and reach the run, as do `--builder-model` and `--reviewer-model`,
    which every `remedy job run` Next line carries too; `--planner-model`
    reaches every structured planner call (DECISION F268 D16 (4) to (7)).
    """
    if not order or not order.strip():
        print("Error: order must not be empty.", file=sys.stderr)
        sys.exit(2)
    if force_job and force_mission:
        print("Error: --force-job and --force-mission cannot be given together.",
              file=sys.stderr)
        sys.exit(2)
    _validate_role_override("builder", "provider", builder_provider)
    _validate_role_override("reviewer", "provider", reviewer_provider)
    _validate_role_override("builder", "model", builder_model)
    _validate_role_override("reviewer", "model", reviewer_model)

    # DECISION F268 D16 (5): resolved before the first step, as `job run` resolves
    # them, and carried to the run only when a budget flag was given.
    budgets_dict = None
    if any(v is not None for v in (max_total_tokens, max_provider_calls,
                                   max_wall_clock_minutes, max_cost_usd, deadline)):
        from packages.orchestration.budget_resolution import (
            BudgetConfigError,
            resolve_job_budgets,
        )
        try:
            budgets = resolve_job_budgets(
                cli_max_total_tokens=max_total_tokens,
                cli_max_provider_calls=max_provider_calls,
                cli_max_wall_clock_minutes=max_wall_clock_minutes,
                cli_max_cost_usd=max_cost_usd,
                cli_deadline=deadline,
                project_root=repo,
            )
        except (BudgetConfigError, ValueError) as exc:
            print(f"Error: {exc} Nothing was run.", file=sys.stderr)
            sys.exit(2)
        budgets_dict = budgets.model_dump(mode="json") if budgets is not None else None

    from packages.orchestration.do_sequence import (
        DoContext,
        do_cost_summary,
        do_cost_summary_lines,
        do_job_task_listing,
        launch_do_cockpit,
        walk_do_sequence,
    )

    ctx = walk_do_sequence(DoContext(
        order=order,
        repo=repo,
        builder_provider=builder_provider,
        reviewer_provider=reviewer_provider,
        project_selector=project,
        budgets=budgets_dict,
        builder_model=builder_model,
        reviewer_model=reviewer_model,
        planner_model=planner_model,
        no_ui=no_ui,
        yes=yes,
        no_llm=no_llm,
        force_job=force_job,
        force_mission=force_mission,
        step_by_step=step_by_step,
        plan_only=plan_only,
        apply=apply,
        # Looked up at call time, so the walk reads the terminal the CLI runs in.
        read_line=input,
        ui_launcher=launch_do_cockpit,
    ))
    jobs = do_job_task_listing(ctx)
    # DECISION F268 D11: measured tokens per role and cost, read from the ledger.
    cost = do_cost_summary(ctx)

    if json_output:
        print(json.dumps({
            "mission_id": ctx.mission_id or None,
            "job_ids": list(ctx.job_ids),
            "waiting_job_ids": list(ctx.waiting_job_ids),
            "contract": None,
            "stopped_before_apply": ctx.stopped_before_apply,
            "shape": ctx.shape or None,
            "shape_source": ctx.shape_source or None,
            "mission_plan_path": ctx.mission_plan_path or None,
            "jobs": jobs,
            "steps": [r.to_json() for r in ctx.results],
            "cost": cost,
            "next": list(ctx.next_lines),
        }, indent=2))
    else:
        for result in ctx.results:
            print(f"[{result.status}] {result.name}: {result.detail}")
            if result.name == "shape" and result.status == "done":
                for job in jobs:
                    for number, task in enumerate(job["tasks"], start=1):
                        print(f"  job {job['job_id']} task {number}: {task['title']}"
                              f" — deliverable: {task['deliverable'] or '(none)'}")
        for line in do_cost_summary_lines(cost):
            print(line)
        for line in ctx.next_lines:
            print(f"Next: {line}")
    if ctx.failed:
        print(f"Error: {ctx.results[-1].name} failed: {ctx.results[-1].detail}",
              file=sys.stderr)
        sys.exit(1)


def _cmd_do(
    goal: str,
    *,
    repo: str = ".",
    project: str | None = None,
    json_output: bool = False,
    builder_provider: str | None = None,
    reviewer_provider: str | None = None,
    builder_model: str | None = None,
    reviewer_model: str | None = None,
    planner_model: str | None = None,
    no_ui: bool = False,
    max_total_tokens: str | None = None,
    max_provider_calls: str | None = None,
    max_wall_clock_minutes: str | None = None,
    max_cost_usd: str | None = None,
    deadline: str | None = None,
    no_llm: bool = False,
    yes: bool = False,
    force_job: bool = False,
    force_mission: bool = False,
    step_by_step: bool = False,
    plan_only: bool = False,
    apply: bool = False,
    contract: str | None = None,
    commit: str | None = None,
    commit_auto: bool = False,
    commit_with_history: bool = False,
    push: bool = False,
) -> None:
    """`remedy do`, with or without the word `run`: the F268 sequence, always (DECISION F268 D16 (1)).

    Remedy deliberately has no second route under `do`: the autorun branch and the
    flags only it read (`--autonomy-level`, `--max-cycles`, `--ui`, `--dry-run`)
    were deleted by DECISION F268 D16 (1) and (2).
    """
    # DECISION F268 D9 (3): before any step.
    _refuse_do_flags_not_yet_available({
        "--contract": contract, "--commit": commit, "--commit-auto": commit_auto,
        "--commit-with-history": commit_with_history, "--push": push,
    })
    _cmd_do_order(goal, repo=repo, json_output=json_output, no_llm=no_llm,
                  yes=yes, builder_provider=builder_provider,
                  reviewer_provider=reviewer_provider, builder_model=builder_model,
                  reviewer_model=reviewer_model, planner_model=planner_model,
                  project=project, max_total_tokens=max_total_tokens,
                  max_provider_calls=max_provider_calls,
                  max_wall_clock_minutes=max_wall_clock_minutes,
                  max_cost_usd=max_cost_usd, deadline=deadline, no_ui=no_ui,
                  force_job=force_job, force_mission=force_mission,
                  step_by_step=step_by_step, plan_only=plan_only, apply=apply)


def _cmd_run_show(
    run_id: str,
    *,
    json_output: bool = False,
) -> None:
    """Show a persisted ping-pong run report."""
    from packages.orchestration.pingpong_loop import load_run

    data = load_run(run_id)
    if data is None:
        print(f"Error: No run matches {run_id!r}. Try: remedy run list.", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(json.dumps(data, indent=2))
    else:
        _print_text_report(run_id, data)


def _cmd_run_list(
    *,
    json_output: bool = False,
    sort: str | None = None,
    desc: bool = False,
    since: str | None = None,
    until: str | None = None,
    limit: str | None = None,
) -> None:
    """List persisted ping-pong runs.

    `list_runs()` already orders by run directory, so `default_sort_field` is None and a call
    with no list flag returns its rows untouched: the payload `do report list` printed.
    """
    from packages.orchestration.list_options import ListOptionError, apply_list_options
    from packages.orchestration.pingpong_loop import list_runs

    try:
        runs = apply_list_options(
            list_runs(),
            sort=sort, desc=desc, since=since, until=until, limit=limit,
            sort_fields={
                "run_id": lambda r: r.get("run_id", ""),
                "goal": lambda r: r.get("goal", ""),
                "status": lambda r: r.get("status", ""),
                "finished_at": lambda r: r.get("finished_at", ""),
            },
            date_getter=lambda r: r.get("finished_at") or None,
        )
    except ListOptionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if not runs:
        print("No ping-pong runs found.")
        return
    if json_output:
        print(json.dumps(runs, indent=2))
    else:
        for r in runs:
            print(f"  {r['run_id']}  {r['status']:<24s}  {r['goal']}")


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
        print(f"Builder: {b_label}")
        print(f"Reviewer: {r_label}")
    else:
        print(f"Builder: {data.get('builder_provider', 'unknown')}")
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


def _cmd_job_run(
    job_id: str,
    *,
    max_rounds: int | None = None,
    repair_rounds: int | None = None,
    test_command: str | None = None,
    claude_cli_write_mode: str | None = None,
    invocation: RunInvocation | None = None,
    json_output: bool = False,
    builder_provider: str | None = None,
    builder_model: str | None = None,
    builder_effort: str | None = None,
    reviewer_provider: str | None = None,
    reviewer_model: str | None = None,
    reviewer_effort: str | None = None,
    repair_provider: str | None = None,
    repair_model: str | None = None,
    repair_effort: str | None = None,
    max_total_tokens: str | None = None,
    max_provider_calls: str | None = None,
    max_wall_clock_minutes: str | None = None,
    max_cost_usd: str | None = None,
    deadline: str | None = None,
) -> None:
    """Run pending tasks sequentially through the ping-pong loop.

    ``invocation`` carries the F012 material controls (timeout/profile/output/stream/max-tasks)
    with omission preserved as ``None`` (F1); resolution happens in ``run_job()``:
    explicit(non-None) CLI value > persisted config > product default.
    """
    from apps.cli.commands.run_invocation import RunInvocation

    if invocation is None:
        invocation = RunInvocation()
    # Per-role model override flags are validated and resolved at the CLI
    # layer (invalid values exit 2) before any run work begins.
    _resolve_cli_role_configs(
        builder_provider=builder_provider,
        builder_model=builder_model,
        builder_effort=builder_effort,
        reviewer_provider=reviewer_provider,
        reviewer_model=reviewer_model,
        reviewer_effort=reviewer_effort,
        repair_provider=repair_provider,
        repair_model=repair_model,
        repair_effort=repair_effort,
    )
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

    # F018: only resolve budgets from CLI/config when the caller explicitly passed budget
    # flags.  When no flags are given, the persisted JobPlan budgets are authoritative —
    # do NOT re-read mutable CWD config and silently replace them.
    _has_budget_flags = any(v is not None for v in (
        max_total_tokens, max_provider_calls, max_wall_clock_minutes,
        max_cost_usd, deadline))
    budgets_dict = None
    if _has_budget_flags:
        # F018: raw budget flags must not silently override a stopped job's limits.
        # Changing limits requires an explicit Decision answer (extend/abandon).
        from packages.orchestration.pingpong_job import JOB_STOPPED, load_job_plan
        _existing = load_job_plan(job_id)
        if _existing is not None and _existing.state == JOB_STOPPED:
            print(
                "Error: job is stopped — budget limits cannot be changed via CLI flags. "
                "Use the Decision workflow (extend/abandon) to resume a stopped job.",
                file=sys.stderr,
            )
            sys.exit(2)
        from packages.orchestration.budget_resolution import BudgetConfigError, resolve_job_budgets
        try:
            budgets = resolve_job_budgets(
                cli_max_total_tokens=max_total_tokens,
                cli_max_provider_calls=max_provider_calls,
                cli_max_wall_clock_minutes=max_wall_clock_minutes,
                cli_max_cost_usd=max_cost_usd,
                cli_deadline=deadline,
            )
        except (BudgetConfigError, ValueError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(2)
        budgets_dict = budgets.model_dump(mode="json") if budgets is not None else None

    from packages.orchestration.pingpong_job import (
        export_job_report,
        run_job,
    )

    job = run_job(
        job_id,
        builder_name=builder_provider,
        reviewer_name=reviewer_provider,
        builder_model=builder_model,
        builder_effort=builder_effort,
        reviewer_model=reviewer_model,
        reviewer_effort=reviewer_effort,
        repair_provider_name=repair_provider,
        repair_model=repair_model,
        repair_effort=repair_effort,
        max_rounds=max_rounds,
        repair_rounds=repair_rounds_val,
        repair_rounds_source=repair_source,
        test_command=test_command,
        claude_cli_write_mode=claude_cli_write_mode,
        budgets=budgets_dict,
        **invocation.as_run_job_kwargs(),
    )

    # F103 cost truth on the job path: a run that spent money must leave a cost
    # row, so the evidence export that arms the live ledger mirror runs here
    # rather than waiting for someone to type `job evidence`. Never fatal.
    from packages.orchestration.job_evidence import mirror_job_run_into_ledger
    cost_mirror = mirror_job_run_into_ledger(job.job_id)

    if json_output:
        report = export_job_report(job)
        report["cost_mirror"] = cost_mirror
        print(json.dumps(report, indent=2))
    else:
        from packages.orchestration.pingpong_job import format_job_report_text
        print(format_job_report_text(job))
        if cost_mirror["ledger_mirrored"]:
            print("Cost recorded to the ledger. See: remedy stats cost")
        else:
            print(
                f"Cost NOT recorded to the ledger: {cost_mirror['error']}\n"
                f"Next: run `remedy job evidence {job.job_id}` and then "
                f"`remedy stats backfill-ledger` to reconcile it.",
                file=sys.stderr,
            )


def _cmd_job_evidence(
    job_id: str,
    *,
    out: str = "",
    verification_command: list[str] | None = None,
    json_output: bool = False,
) -> None:
    """Export a self-contained evidence bundle for an entire job."""
    from packages.orchestration.data_paths import job_evidence_export_dir
    from packages.orchestration.job_evidence import export_job_evidence

    if not out:
        # Default to the hidden data-dir location; never litter the repo root.
        out = str(job_evidence_export_dir(job_id))

    # F6 (round 16): the TOP LEVEL reads the operator's base declaration exactly once and passes
    # it explicitly. Nothing downstream consults the environment or the process CWD to decide
    # what this package is a review of.
    from packages.orchestration.review_subject import read_declared_base

    result = export_job_evidence(
        job_id, out, verification_commands=verification_command or None,
        declared_base=read_declared_base(),
    )

    if not result.get("error"):
        _index_job_evidence(job_id, result.get("out_dir", out), "job.evidence")

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


def _cmd_job_apply(
    job_id: str,
    *,
    repo: str = ".",
    approve: bool = False,
    dry_run: bool = False,
    test_command: str = "",
    skip_blocked: bool = False,
    json_output: bool = False,
) -> None:
    """Review and apply job workspace changes to target repo."""
    from packages.orchestration.job_apply import (
        apply_job,
        export_job_apply_json,
        summarize_job_apply,
    )

    if not approve and not dry_run:
        dry_run = True

    result = apply_job(
        job_id,
        target_repo=repo,
        approve=approve,
        dry_run=dry_run,
        test_command=test_command,
        skip_blocked=skip_blocked,
    )

    if json_output:
        print(json.dumps(export_job_apply_json(result), indent=2))
    else:
        print(summarize_job_apply(result))


def _index_job_evidence(job_id: str, evidence_out: str, source_command: str) -> None:
    """Record this export in the existing job evidence index (best effort).

    Captures the resolved repository, branch, commit, export path, timestamp,
    job status and the changed source/test file set so review-zip selection can
    match evidence to the current working tree instead of guessing by mtime.
    """
    try:
        from packages.orchestration.evidence_index import (
            dirty_source_test_files,
            write_index_record,
        )
        from packages.orchestration.pingpong_job import load_job_plan

        job = load_job_plan(job_id)
        repo = getattr(job, "repo_path", "") or "."
        status = getattr(job, "state", "") or ""
        changed: list[str] = []
        try:
            from packages.orchestration.job_evidence import _read_changed_files_for_index
            changed = _read_changed_files_for_index(evidence_out)
        except Exception:
            changed = []
        if not changed:
            changed = dirty_source_test_files(repo)
        write_index_record(
            job_id, evidence_out, repo_path=repo, job_status=status,
            changed_files=changed, source_command=source_command,
        )
    except Exception:
        pass


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "do.run": lambda args: _cmd_do(
        getattr(args, "goal", None) or "",
        repo=getattr(args, "repo", None) or ".",
        project=getattr(args, "project", None),
        json_output=getattr(args, "json", False),
        builder_provider=getattr(args, "builder_provider", None),
        reviewer_provider=getattr(args, "reviewer_provider", None),
        builder_model=getattr(args, "builder_model", None),
        reviewer_model=getattr(args, "reviewer_model", None),
        planner_model=getattr(args, "planner_model", None),
        no_ui=bool(getattr(args, "no_ui", False)),
        max_total_tokens=getattr(args, "max_total_tokens", None),
        max_provider_calls=getattr(args, "max_provider_calls", None),
        max_wall_clock_minutes=getattr(args, "max_wall_clock_minutes", None),
        max_cost_usd=getattr(args, "max_cost_usd", None),
        deadline=getattr(args, "deadline", None),
        no_llm=getattr(args, "no_llm", False),
        yes=getattr(args, "yes", False),
        force_job=bool(getattr(args, "force_job", False)),
        force_mission=bool(getattr(args, "force_mission", False)),
        step_by_step=bool(getattr(args, "step_by_step", False)),
        plan_only=bool(getattr(args, "plan_only", False)),
        apply=bool(getattr(args, "apply", False)),
        contract=getattr(args, "contract", None),
        commit=getattr(args, "commit", None),
        commit_auto=bool(getattr(args, "commit_auto", False)),
        commit_with_history=bool(getattr(args, "commit_with_history", False)),
        push=bool(getattr(args, "push", False)),
    ),
    "run.show": lambda args: _cmd_run_show(
        args.run_id,
        json_output=getattr(args, "json", False),
    ),
    "run.list": lambda args: _cmd_run_list(
        json_output=getattr(args, "json", False),
        sort=getattr(args, "sort", None),
        desc=getattr(args, "desc", False),
        since=getattr(args, "since", None),
        until=getattr(args, "until", None),
        limit=getattr(args, "limit", None),
    ),
    "job.run": lambda args: _cmd_job_run(
        args.job_id,
        max_rounds=int(getattr(args, "max_rounds")) if getattr(args, "max_rounds", None) is not None else None,
        repair_rounds=int(getattr(args, "repair_rounds")) if getattr(args, "repair_rounds", None) is not None else None,
        test_command=getattr(args, "test_command", None),
        claude_cli_write_mode=getattr(args, "claude_cli_write_mode", None),
        invocation=_invocation_from_args(args),
        json_output=getattr(args, "json", False),
        builder_provider=getattr(args, "builder_provider", None),
        builder_model=getattr(args, "builder_model", None),
        builder_effort=getattr(args, "builder_effort", None),
        reviewer_provider=getattr(args, "reviewer_provider", None),
        reviewer_model=getattr(args, "reviewer_model", None),
        reviewer_effort=getattr(args, "reviewer_effort", None),
        repair_provider=getattr(args, "repair_provider", None),
        repair_model=getattr(args, "repair_model", None),
        repair_effort=getattr(args, "repair_effort", None),
        max_total_tokens=getattr(args, "max_total_tokens", None),
        max_provider_calls=getattr(args, "max_provider_calls", None),
        max_wall_clock_minutes=getattr(args, "max_wall_clock_minutes", None),
        max_cost_usd=getattr(args, "max_cost_usd", None),
        deadline=getattr(args, "deadline", None),
    ),
    "job.apply": lambda args: _cmd_job_apply(
        args.job_id,
        repo=getattr(args, "repo", None) or ".",
        approve=getattr(args, "approve", False),
        dry_run=getattr(args, "dry_run", False),
        test_command=getattr(args, "test_command", None) or "",
        skip_blocked=getattr(args, "skip_blocked", False),
        json_output=getattr(args, "json", False),
    ),
    "job.evidence": lambda args: _cmd_job_evidence(
        args.job_id,
        out=getattr(args, "out", None) or "",
        verification_command=getattr(args, "verification_command", None),
        json_output=getattr(args, "json", False),
    ),
}
