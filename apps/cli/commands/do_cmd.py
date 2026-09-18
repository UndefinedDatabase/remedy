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


_MISSION_DISPLAY_MAX = 120


def _cmd_do_mission(
    mission: str,
    *,
    repo: str = ".",
    json_output: bool = False,
    no_llm: bool = False,
    yes: bool = False,
) -> None:
    """Golden-path: mission string → planned job (F147 T001)."""
    if not mission or not mission.strip():
        print("Error: mission must not be empty.", file=sys.stderr)
        sys.exit(2)

    from packages.orchestration.project_registry import resolve_project
    project = resolve_project(repo)
    if project is None:
        print(
            "No project registered for this repo. Run: remedy init",
            file=sys.stderr,
        )
        sys.exit(3)

    from packages.core.models import RunState
    from packages.orchestration.intake import (
        compose_intake_prompt,
        heuristic_intake,
        make_intake_call_recorder,
        make_provider_call_fn,
        run_intake,
    )
    from packages.orchestration.job_runner import plan_job
    from packages.orchestration.pingpong_job import JobPlan, save_job_plan

    call_fn = None
    intake_result = None
    # One list, one write: it carries every prompt trace this command produces,
    # intake and task plan alike, because `write_trace_jsonl` opens its path
    # with mode "w" and a second write would truncate the first.
    prompt_traces: list = []
    intake_fallback_reason = ""
    if no_llm:
        intake_result = heuristic_intake(mission)
        intake_fallback_reason = "forced"
    else:
        call_fn = make_provider_call_fn()
        if call_fn is not None:
            intake_composed = compose_intake_prompt(mission)
            intake_result = run_intake(
                mission,
                call_fn,
                composed=intake_composed,
                on_call=make_intake_call_recorder(
                    prompt_traces,
                    intake_composed,
                    provider="ollama",
                    provider_kind="ollama",
                ),
            )
            if intake_result.source == "heuristic":
                intake_fallback_reason = "provider_error"

        if intake_result is None:
            intake_result = heuristic_intake(mission)
            intake_fallback_reason = "provider_unavailable"

    # --- Task Plan (LLM) or deterministic fallback ---
    job = None
    plan_label = "deterministic skeleton"

    plan_call_fn = None
    if call_fn is not None and not no_llm:
        from packages.orchestration.intake import make_structured_call_fn
        from packages.orchestration.schemas.models import TaskPlan
        # Planning needs a call_fn bound to TaskPlan: the intake one binds
        # the provider's native schema to JobIntake, so the provider would
        # answer in intake shape and every plan attempt would fail validation.
        # There is deliberately NO fallback to it — without a TaskPlan-bound
        # provider we skip LLM planning and take the deterministic skeleton
        # below, exactly as the no-provider path does.
        plan_call_fn = make_structured_call_fn(TaskPlan)

    if plan_call_fn is not None:
        from packages.orchestration.job_plan import (
            apply_plan_budgets,
            apply_plan_fences,
            compose_task_plan_prompt,
            make_task_plan_call_recorder,
            map_task_plan_to_tasks,
            plan_job_llm,
            write_plan_md,
        )
        plan_intake_dict = intake_result.value.model_dump()
        # Composed exactly ONCE here and handed to `plan_job_llm`, so the bytes
        # the provider receives and the manifest the trace records come from the
        # same composition — `prompt_chars` and `segment_manifest_chars` can no
        # longer describe two different prompts (R-0256).
        plan_composed = compose_task_plan_prompt(plan_intake_dict)
        fp_result = plan_job_llm(
            plan_intake_dict,
            plan_call_fn,
            composed=plan_composed,
            on_call=make_task_plan_call_recorder(
                prompt_traces,
                plan_composed,
                provider="ollama",
                provider_kind="ollama",
            ),
        )
        if fp_result.plan is not None:
            fp_dict = fp_result.plan.model_dump()
            fp_dict["_approval"] = "pending"
            fp_dict["_normalization"] = fp_result.transformations
            tasks = map_task_plan_to_tasks(fp_result.plan)
            from packages.core.models import JobBudgets, JobFences
            from packages.orchestration.budget_resolution import resolve_job_budgets
            config_budgets = resolve_job_budgets(project_root=repo)
            config_budgets_dict = config_budgets.model_dump(exclude_none=True) if config_budgets else None
            merged_budgets = apply_plan_budgets(config_budgets_dict, fp_result.plan.budgets)
            merged_fences = apply_plan_fences(None, fp_result.plan.fences)
            job_budgets = None
            if merged_budgets:
                try:
                    job_budgets = JobBudgets(**{
                        k: v for k, v in merged_budgets.items()
                        if k in JobBudgets.model_fields})
                except Exception:
                    pass
            job_fences = None
            if merged_fences:
                try:
                    job_fences = JobFences(**{
                        k: v for k, v in merged_fences.items()
                        if k in JobFences.model_fields})
                except Exception:
                    pass
            job = JobPlan(
                job_title=mission[:80], mission=mission, user_prompt=mission,
                project_id=str(project.id),
                intake=intake_result.value.model_dump(),
                task_plan=fp_dict,
                tasks=tasks,
                state=RunState.PLANNED,
                budgets=job_budgets.model_dump(mode="json") if job_budgets is not None else None,
                fences=job_fences,
            )
            save_job_plan(job)
            from packages.orchestration.data_paths import job_evidence_export_dir
            write_plan_md(
                fp_result.plan, job_evidence_export_dir(str(job.job_id)),
                transformations=fp_result.transformations)
            if yes:
                # F034: --yes covers approval AND clarifications. Every open
                # question runs on its documented default, recorded in the
                # assumption log — unattended, but never silent. The semantics
                # live in job_plan.auto_approve_task_plan so the
                # orchestrator loop runs the SAME approval, not a copy of it.
                from packages.orchestration.job_plan import auto_approve_task_plan
                fp_dict = auto_approve_task_plan(
                    fp_dict, job_evidence_export_dir(str(job.job_id)))
                job.task_plan = fp_dict
                save_job_plan(job)
                plan_label = (
                    f"task plan {fp_result.plan.schema_v} (approved via --yes)"
                )
            else:
                plan_label = (
                    f"task plan {fp_result.plan.schema_v} (awaiting approval)"
                )
        else:
            job = JobPlan(
                job_title=mission[:80], mission=mission, user_prompt=mission,
                project_id=str(project.id),
                intake=intake_result.value.model_dump(),
                state=RunState.PENDING,
            )
            save_job_plan(job)
            from packages.orchestration.data_paths import job_evidence_export_dir
            from packages.orchestration.failure_postmortem import (
                FailureSignals,
                build_job_rollup,
                write_postmortem,
            )
            signals = FailureSignals(
                error_class="parse",
                error_text=fp_result.error_hint or "task plan parse failure",
            )
            pm = build_job_rollup(job_id=str(job.job_id), signals=signals)
            ev_dir = job_evidence_export_dir(str(job.job_id))
            ev_dir.mkdir(parents=True, exist_ok=True)
            try:
                write_postmortem(ev_dir, pm, root=ev_dir)
            except Exception as exc:
                print(f"Warning: postmortem write failed: {exc}", file=sys.stderr)
            print(
                f"Error: task plan generation failed: "
                f"{fp_result.error_hint or 'parse failure'}",
                file=sys.stderr,
            )
            sys.exit(1)

    if job is None:
        job = JobPlan(
            job_title=mission[:80], mission=mission, user_prompt=mission,
            project_id=str(project.id),
            intake=intake_result.value.model_dump(),
        )
        plan_result = plan_job(job)
        job = plan_result.job
        save_job_plan(job)

    if prompt_traces:
        from packages.orchestration.prompt_trace import write_trace_jsonl
        from packages.orchestration.run_log import RunLogWriter
        log = RunLogWriter(job_id=job.job_id)
        try:
            write_trace_jsonl(prompt_traces, log.path.parent / "prompt_trace.jsonl")
        except OSError:
            pass

    from packages.orchestration.project_registry import attach_job, save_project
    attach_job(project, str(job.job_id))
    save_project(project)

    short_id = str(job.job_id)[:8]
    display_mission = mission if len(mission) <= _MISSION_DISPLAY_MAX else mission[:_MISSION_DISPLAY_MAX] + "…"

    if json_output:
        import json as _json
        print(_json.dumps({
            "job_id": str(job.job_id),
            "short_id": short_id,
            "project_slug": project.slug,
            "state": job.state.value,
            "mission": mission,
            "intake": {
                "source": intake_result.source,
                "goal": intake_result.value.goal,
                "fallback_reason": intake_fallback_reason,
            },
            "tasks": [
                {"task_id": str(t.task_id), "description": t.title}
                for t in job.tasks
            ],
            "plan_label": plan_label,
            "next_command": "remedy status",
        }, indent=2))
        return

    print(f"Job: {short_id}")
    print(f"Project: {project.slug}")
    print(f"Mission: {display_mission}")
    print(f"State: {job.state.value}")
    if intake_result.source == "llm":
        intake_label = "intake: llm"
    elif intake_fallback_reason == "forced":
        intake_label = "intake: heuristic (forced by --no-llm)"
    elif intake_fallback_reason == "provider_unavailable":
        intake_label = "intake: heuristic fallback (provider unavailable)"
    elif intake_fallback_reason == "provider_error":
        intake_label = "intake: heuristic fallback (provider error)"
    else:
        intake_label = f"intake: {intake_result.source}"
    print(intake_label)
    print("Tasks:")
    for t in job.tasks:
        task_type = t.inputs.get("task_type", "")
        print(f"  - {task_type}: {t.title}")
    print(f"plan: {plan_label}")
    print("Next: remedy status")


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
    max_total_tokens: str | None = None,
    max_provider_calls: str | None = None,
    max_wall_clock_minutes: str | None = None,
    max_cost_usd: str | None = None,
    deadline: str | None = None,
    injected_default: bool = False,
    truly_bare: bool = False,
    no_llm: bool = False,
    yes: bool = False,
) -> None:
    # --- Bare-mission golden path (F147) ---
    # Fires ONLY when grouped.py determined the invocation is truly bare:
    # `run` was injected AND no flag tokens besides --json/--repo/--no-llm/--yes
    # appeared in the raw argv. This catches `do "x" --autonomy-level 1`
    # (explicit flag at default value) which value-equality checks cannot
    # distinguish.
    if truly_bare and goal:
        _cmd_do_mission(goal, repo=repo, json_output=json_output, no_llm=no_llm, yes=yes)
        return

    # --- Budget resolution (always runs — catches config-only budgets) ---
    from packages.orchestration.budget_resolution import BudgetConfigError, resolve_job_budgets
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
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    # Require a goal
    if not goal:
        print("Error: provide a goal.", file=sys.stderr)
        sys.exit(2)

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
    from packages.orchestration.project_registry import ProjectNotFoundError, select_project

    _resolved_project = None
    try:
        _resolved_project, _src = select_project(project, repo)
        _resolved_project_id = str(_resolved_project.id)
    except ProjectNotFoundError:
        print(
            "Error: no project found. Run: remedy init\n"
            "  or pass --project <slug-or-id>",
            file=sys.stderr,
        )
        sys.exit(3)

    try:
        result = run_do(
            goal, repo,
            autonomy_level=autonomy_level,
            max_loops=max_cycles,
            stop_before_apply=True,
            budgets=budgets,
            project_id=_resolved_project_id,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if _resolved_project is not None and result.job_id:
        from packages.orchestration.project_registry import attach_job, save_project
        attach_job(_resolved_project, result.job_id)
        save_project(_resolved_project)

    if json_output:
        print(json.dumps(export_do_run_json(result, contract=result._contract), indent=2))
    else:
        print(summarize_do_run(result))


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
        autonomy_level=int(getattr(args, "autonomy_level", None) or 2),
        max_cycles=int(getattr(args, "max_cycles", None) or 3),
        injected_default=getattr(args, "_injected_default", False),
        truly_bare=getattr(args, "_truly_bare", False),
        enable_ui=(
            bool(getattr(args, "ui", False))
            and not getattr(args, "no_ui", False)
        ),
        dry_run=getattr(args, "dry_run", False),
        json_output=getattr(args, "json", False),
        fixture_builder=_parse_fixture_builder(getattr(args, "fixture_builder", "false")),
        builder_provider=_parse_builder_provider(getattr(args, "builder_provider", "none")),
        max_total_tokens=getattr(args, "max_total_tokens", None),
        max_provider_calls=getattr(args, "max_provider_calls", None),
        max_wall_clock_minutes=getattr(args, "max_wall_clock_minutes", None),
        max_cost_usd=getattr(args, "max_cost_usd", None),
        deadline=getattr(args, "deadline", None),
        no_llm=getattr(args, "no_llm", False),
        yes=getattr(args, "yes", False),
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
