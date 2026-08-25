"""CLI handler for ``remedy do`` — high-level guided autorun."""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from apps.cli.commands.run_invocation import (
    RunInvocation,
)
from apps.cli.commands.run_invocation import (
    invocation_from_args as _invocation_from_args,
)

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

_DEFAULT_RAW_TIMEOUT = 120


def _resolve_timeout_precedence(
    raw_timeout: int | None,
    timeout_profile: str | None,
) -> tuple[int, str]:
    """Resolve timeout precedence for F001.

    Precedence:
    1. Explicit raw timeout (--timeout-sec / --provider-timeout-sec) wins.
    2. Explicit --timeout-profile wins.
    3. Default: adaptive profile "normal".

    Returns (timeout_sec, timeout_profile).
    When raw timeout wins, timeout_profile is "" (empty) so run_pingpong
    uses timeout_sec directly.
    """
    if raw_timeout is not None:
        # User explicitly passed raw timeout — override adaptive profile
        return raw_timeout, ""
    if timeout_profile is not None:
        # User explicitly passed --timeout-profile
        return _DEFAULT_RAW_TIMEOUT, timeout_profile
    # Neither passed — default to adaptive normal
    return _DEFAULT_RAW_TIMEOUT, "normal"

# --- Per-role model override flags (T002) ---------------------------------
# CLI accepts --<role>-provider / --<role>-model / --<role>-effort for the
# builder, reviewer, and repair roles. Values are validated at the CLI layer
# before being passed through to role_config.resolve_role_config.
_VALID_ROLE_PROVIDERS = frozenset(
    {"ollama", "claude", "claude-cli", "fake", "fixture"}
)
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

    from packages.core.models import Job, RunState
    from packages.orchestration.intake import (
        compose_intake_prompt,
        heuristic_intake,
        make_intake_call_recorder,
        make_provider_call_fn,
        run_intake,
    )
    from packages.orchestration.job_runner import plan_job
    from packages.orchestration.storage import save_job

    call_fn = None
    intake_result = None
    # One list, one write: it carries every prompt trace this command produces,
    # intake and flight plan alike, because `write_trace_jsonl` opens its path
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

    # --- Flight Plan (LLM) or deterministic fallback ---
    job = None
    plan_label = "deterministic skeleton"

    plan_call_fn = None
    if call_fn is not None and not no_llm:
        from packages.orchestration.intake import make_structured_call_fn
        from packages.orchestration.schemas.models import FlightPlan
        # Planning needs a call_fn bound to FlightPlan: the intake one binds
        # the provider's native schema to JobIntake, so the provider would
        # answer in intake shape and every plan attempt would fail validation.
        # There is deliberately NO fallback to it — without a FlightPlan-bound
        # provider we skip LLM planning and take the deterministic skeleton
        # below, exactly as the no-provider path does.
        plan_call_fn = make_structured_call_fn(FlightPlan)

    if plan_call_fn is not None:
        from packages.orchestration.flight_plan import (
            apply_plan_budgets,
            apply_plan_fences,
            compose_flight_plan_prompt,
            make_flight_plan_call_recorder,
            map_flight_plan_to_tasks,
            plan_job_llm,
            write_plan_md,
        )
        plan_intake_dict = intake_result.value.model_dump()
        # Composed exactly ONCE here and handed to `plan_job_llm`, so the bytes
        # the provider receives and the manifest the trace records come from the
        # same composition — `prompt_chars` and `segment_manifest_chars` can no
        # longer describe two different prompts (R-0256).
        plan_composed = compose_flight_plan_prompt(plan_intake_dict)
        fp_result = plan_job_llm(
            plan_intake_dict,
            plan_call_fn,
            composed=plan_composed,
            on_call=make_flight_plan_call_recorder(
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
            tasks = map_flight_plan_to_tasks(fp_result.plan)
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
            job = Job(
                name=mission[:80], mission=mission, user_prompt=mission,
                project_id=str(project.id),
                intake=intake_result.value.model_dump(),
                flight_plan=fp_dict,
                tasks=tasks,
                state=RunState.PLANNED,
                budgets=job_budgets,
                fences=job_fences,
            )
            save_job(job)
            from packages.orchestration.data_paths import job_evidence_export_dir
            write_plan_md(
                fp_result.plan, job_evidence_export_dir(str(job.id)),
                transformations=fp_result.transformations)
            if yes:
                # F034: --yes covers approval AND clarifications. Every open
                # question runs on its documented default, recorded in the
                # assumption log — unattended, but never silent. The semantics
                # live in flight_plan.auto_approve_flight_plan so the
                # orchestrator loop runs the SAME approval, not a copy of it.
                from packages.orchestration.flight_plan import auto_approve_flight_plan
                fp_dict = auto_approve_flight_plan(
                    fp_dict, job_evidence_export_dir(str(job.id)))
                job.flight_plan = fp_dict
                save_job(job)
                plan_label = (
                    f"flight plan {fp_result.plan.schema_v} (approved via --yes)"
                )
            else:
                plan_label = (
                    f"flight plan {fp_result.plan.schema_v} (awaiting approval)"
                )
        else:
            job = Job(
                name=mission[:80], mission=mission, user_prompt=mission,
                project_id=str(project.id),
                intake=intake_result.value.model_dump(),
                state=RunState.PENDING,
            )
            save_job(job)
            from packages.orchestration.data_paths import job_evidence_export_dir
            from packages.orchestration.failure_postmortem import (
                FailureSignals,
                build_job_rollup,
                write_postmortem,
            )
            signals = FailureSignals(
                error_class="parse",
                error_text=fp_result.error_hint or "flight plan parse failure",
            )
            pm = build_job_rollup(job_id=str(job.id), signals=signals)
            ev_dir = job_evidence_export_dir(str(job.id))
            ev_dir.mkdir(parents=True, exist_ok=True)
            try:
                write_postmortem(ev_dir, pm, root=ev_dir)
            except Exception as exc:
                print(f"Warning: postmortem write failed: {exc}", file=sys.stderr)
            print(
                f"Error: flight plan generation failed: "
                f"{fp_result.error_hint or 'parse failure'}",
                file=sys.stderr,
            )
            sys.exit(1)

    if job is None:
        job = Job(
            name=mission[:80], mission=mission, user_prompt=mission,
            project_id=str(project.id),
            intake=intake_result.value.model_dump(),
        )
        plan_result = plan_job(job)
        job = plan_result.job
        save_job(job)

    if prompt_traces:
        from packages.orchestration.prompt_trace import write_trace_jsonl
        from packages.orchestration.run_log import RunLogWriter
        log = RunLogWriter(job_id=job.id)
        try:
            write_trace_jsonl(prompt_traces, log.path.parent / "prompt_trace.jsonl")
        except OSError:
            pass

    from packages.orchestration.project_registry import attach_job, save_project
    attach_job(project, str(job.id))
    save_project(project)

    short_id = str(job.id)[:8]
    display_mission = mission if len(mission) <= _MISSION_DISPLAY_MAX else mission[:_MISSION_DISPLAY_MAX] + "…"

    if json_output:
        import json as _json
        print(_json.dumps({
            "job_id": str(job.id),
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
                {"task_id": str(t.id), "description": t.description}
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
        print(f"  - {task_type}: {t.description}")
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
    builder: str = "none",
    reviewer: str = "none",
    max_rounds: int = 3,
    mode: str = "staged",
    test_command: str = "",
    provider_timeout_sec: int = 120,
    timeout_profile: str = "",
    max_output_chars_val: int = 50000,
    keep_staging: bool = False,
    claude_cli_write_mode: str = "none",
    task_file: str = "",
    task_stdin: bool = False,
    scope_file: str = "",
    approve_scope: bool = False,
    repair_rounds: int | None = None,
    stream_evidence: bool = False,
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
            timeout_profile=timeout_profile,
            max_output_chars=max_output_chars_val, keep_staging=keep_staging,
            claude_cli_write_mode=claude_cli_write_mode,
            task_input=task_input,
            scope_data=scope_data,
            scope_validation=scope_validation,
            repair_rounds=repair_rounds,
            repair_rounds_source=repair_rounds_source,
            stream_evidence=stream_evidence,
            budgets=budgets,
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


#: What the bare `remedy do run` path prints for a role whose provider is
#: handed no model and has no built-in default of its own to name. The `claude`
#: CLI then picks whatever the OPERATOR configured it to pick, and Remedy cannot
#: name that id without running the binary — so it says exactly that instead of
#: printing a guess.
_INHERITED_CLI_MODEL_LABEL = "CLI default (no --model passed)"


def pingpong_effective_model(provider_name: str) -> str:
    """The model one role of a bare `remedy do run` actually uses.

    THIS PATH TAKES NO MODEL OPTION. `_cmd_do_pingpong` passes none to
    ``run_pingpong``, whose ``builder_model``/``reviewer_model`` therefore stay
    empty, so the id is decided entirely by the provider that was named. Two
    real claude-cli runs during operator dogfooding on 2026-08-25 were never
    told which model answered them; printing this at startup is what makes that
    visible.

    Remedy deliberately does NOT add a model option to this path. `remedy do
    job-run` is the path that carries `--builder-model` and `--reviewer-model`;
    this function only reports, and adding an option here is recorded as an
    operator finding rather than built.

    ``tests/cli/test_do_cmd_pingpong_budget.py`` pins each answer against what
    the provider really does, so this cannot drift into a comfortable fiction.
    """
    if provider_name == "claude-cli":
        # ClaudeCliProvider passes --model only when it HAS one
        # (`pingpong_provider.build_claude_cli_args`), so an empty model means
        # the argument is never on the command line at all.
        return _INHERITED_CLI_MODEL_LABEL
    if provider_name == "claude":
        # The direct-API provider names its own built-in default, which comes
        # from the one F254 alias table.
        from packages.orchestration.model_aliases import resolve_model_alias
        return f"{resolve_model_alias('claude-workhorse')} (Remedy built-in default)"
    if provider_name == "fake":
        return "none (fake provider makes no model call)"
    return "unknown"


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
    timeout_profile: str = "",
    max_output_chars: int = 50000,
    keep_staging: bool = False,
    claude_cli_write_mode: str = "none",
    task_input: Any = None,
    scope_data: dict[str, Any] | None = None,
    scope_validation: Any = None,
    repair_rounds: int = 0,
    repair_rounds_source: str = "",
    stream_evidence: bool = False,
    budgets: Any = None,
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
        print(f"Builder model: {pingpong_effective_model(effective_builder)}")
        print(f"Reviewer: {effective_reviewer}")
        print(f"Reviewer model: {pingpong_effective_model(effective_reviewer)}")
        print(f"Max rounds: {max_rounds}")
        if test_command:
            print(f"Test command: {test_command}")
        if repair_rounds > 0:
            print(f"Repair rounds: {repair_rounds}")
        if budgets is not None:
            print(f"Budgets: {budgets}")
        print()

    # F018: build a budget-aware stop_check for the bare ping-pong path.
    _stop_check = None
    _on_provider_call = None
    if budgets is not None:
        from datetime import datetime as _dt
        from datetime import timezone as _tz

        from packages.orchestration.budget_guard import BudgetCounters as _BC
        from packages.orchestration.budget_guard import evaluate_budget as _evaluate
        from packages.orchestration.safe_points import ShouldStopResult as _StopResult

        _pp_started = _dt.now(_tz.utc)
        _pp_calls = 0
        _pp_tokens = 0
        _pp_measured = 0
        _pp_unmeasured = 0

        def _on_provider_call(attempt):
            nonlocal _pp_calls, _pp_tokens, _pp_measured, _pp_unmeasured
            if getattr(attempt, "provider", "fake") == "fake":
                return
            _pp_calls += 1
            ua = getattr(attempt, "usage_actuals", None)
            if ua is not None:
                _pp_measured += 1
                _pp_tokens += (
                    getattr(ua, "input_tokens", 0) +
                    getattr(ua, "output_tokens", 0)
                )
            else:
                _pp_unmeasured += 1

        def _stop_check():
            """The safe-point probe for a run that HAS NO JOB ID.

            Remedy deliberately does not call ``safe_points.should_stop`` here.
            That function's first act is the OPERATOR stop check, and an
            operator stop is addressed BY JOB ID: `remedy job stop <id>` writes
            a request under ``<data_root>/control/<job-id>/``. The bare
            `remedy do run` ping-pong path mints no job, persists no job
            record and prints no id, so an operator has no target to name and
            this run has nothing to look up. The reviewed build asked anyway,
            with a hardcoded empty id, and ``validate_job_id`` correctly
            refused it — every budgeted `do run` died with StopControlError
            "invalid job id ''" before the first provider call (operator
            dogfooding, 2026-08-25). The fix is to ask the question this path
            can actually answer, not to weaken the id rule.

            So the BUDGET GUARD is consulted directly, and it is the only
            safe-point authority a job-less run has. `remedy do job-run`,
            which does mint a job id, keeps the full unified check.

            No budget tick is emitted for the same reason: a tick is written to
            ``<data_root>/runs/<job-id>/`` and there is no job id to file it
            under. Returning the same ``ShouldStopResult`` shape the unified
            check returned keeps ``run_pingpong``'s stop handling unchanged.
            """
            counters = _BC(
                provider_calls=_pp_calls,
                measured_token_total=_pp_tokens,
                measured_call_count=_pp_measured,
                unmeasured_call_count=_pp_unmeasured,
                started_at=_pp_started,
            )
            evaluation = _evaluate(budgets, counters)
            if not evaluation.exhausted:
                return None
            limit = evaluation.first_exhausted_limit or "unknown"
            return _StopResult(
                should_stop=True,
                reason=f"budget_exhausted:{limit}",
                source="budget",
                budget_evaluation=evaluation,
            )

    result = run_pingpong(
        goal,
        repo,
        builder_name=effective_builder,
        reviewer_name=effective_reviewer,
        max_rounds=max_rounds,
        timeout_sec=provider_timeout_sec,
        timeout_profile=timeout_profile,
        max_output_chars=max_output_chars,
        test_command=test_command,
        keep_staging=keep_staging,
        claude_cli_write_mode=claude_cli_write_mode,
        task_input=task_input,
        scope_data=scope_data,
        scope_validation=scope_validation,
        repair_rounds=repair_rounds,
        repair_rounds_source=repair_rounds_source,
        stream_evidence=stream_evidence,
        stop_check=_stop_check,
        on_provider_call=_on_provider_call,
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


def _cmd_do_repair_attest(
    job_id: str,
    task_id: str,
    *,
    note: str = "",
    repo: str = ".",
    yes: bool = False,
    task_scoped: bool = False,
    allowed_files: str = "",
    linked_prior_job_id: str = "",
    json_output: bool = False,
) -> None:
    """Attest a manual operator repair as a valid evidence path for one task."""
    from packages.orchestration.repair_attest import (
        attest_operator_repair,
        collect_diff_stat,
    )

    diff_stat = collect_diff_stat(repo)

    if not yes:
        print("Diff stat for attestation:", file=sys.stderr)
        print(diff_stat, file=sys.stderr)
        print(
            "\nError: --yes required to confirm attestation. "
            "Review the diff stat above and re-run with --yes.",
            file=sys.stderr,
        )
        sys.exit(2)

    _allowed = [f.strip() for f in (allowed_files or "").split(",") if f.strip()] or None
    result = attest_operator_repair(
        job_id, task_id, note, repo,
        task_scoped=task_scoped, allowed_files=_allowed,
        linked_prior_job_id=linked_prior_job_id,
    )

    if result.get("error"):
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(json.dumps(result, indent=2))
    else:
        print(f"Diff stat:\n{diff_stat}\n")
        print(
            f"Operator repair attested [OPERATOR ATTESTED] | "
            f"job={result['job_id']} task={result['task_id']} "
            f"files={len(result.get('changed_files', []))} "
            f"diff_sha256={result['diff_sha256'][:12]}"
        )
        for filename in result.get("files", {}):
            print(f"  {filename}")


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
    max_total_tokens: str | None = None,
    max_provider_calls: str | None = None,
    max_wall_clock_minutes: str | None = None,
    max_cost_usd: str | None = None,
    deadline: str | None = None,
    json_output: bool = False,
) -> None:
    """Parse a job file into ordered tasks (no provider calls)."""
    from packages.orchestration.pingpong_job import plan_job_from_file

    if not job_file:
        print("Error: --job-file is required", file=sys.stderr)
        sys.exit(1)

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

    job = plan_job_from_file(job_file, repo)

    if job.error:
        print(f"Error: {job.error}", file=sys.stderr)
        sys.exit(1)

    if budgets is not None:
        job.budgets = budgets.model_dump(mode="json")
        from packages.orchestration.pingpong_job import save_job_plan
        save_job_plan(job)

    if json_output:
        print(json.dumps({
            "job_id": job.job_id,
            "job_title": job.job_title,
            "status": job.status,
            "budgets": job.budgets,
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
        if budgets is not None:
            print(f"Budgets: {job.budgets}")
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
        from packages.orchestration.pingpong_job import load_job_plan
        _existing = load_job_plan(job_id)
        if _existing is not None and getattr(_existing, "status", "") == "stopped":
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
        builder_name=builder,
        reviewer_name=reviewer,
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

    if json_output:
        print(json.dumps(export_job_report(job), indent=2))
    else:
        from packages.orchestration.pingpong_job import format_job_report_text
        print(format_job_report_text(job))


def _cmd_do_job_evidence(
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
        _index_job_evidence(job_id, result.get("out_dir", out), "do.job-evidence")

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


def _cmd_do_job_resume(
    job_id: str,
    *,
    builder: str | None = None,
    reviewer: str | None = None,
    max_rounds: int | None = None,
    repair_rounds: int | None = None,
    test_command: str | None = None,
    invocation: RunInvocation | None = None,
    json_output: bool = False,
) -> None:
    """Resume an interrupted JobPlan in its own job-owned worktree.

    JobPlan IDs are 16-character hex values (``ee71656400f646e0``) — a different
    storage model from the UUID Core Jobs that ``remedy job resume`` handles. The
    two are deliberately kept apart rather than pretending to be the same object.

    F1: the material invocation controls come through the shared ``RunInvocation`` with
    omission preserved as ``None``, so resume never clears a persisted cap by passing 0.
    """
    import json as _json

    from apps.cli.commands.run_invocation import RunInvocation
    from packages.orchestration.pingpong_job import export_job_report, resume_job_plan

    if invocation is None:
        invocation = RunInvocation()

    def _as_int(v, default=None):
        return default if v in (None, "") else int(v)

    try:
        job = resume_job_plan(
            job_id,
            builder_name=builder,
            reviewer_name=reviewer,
            max_rounds=_as_int(max_rounds),
            repair_rounds=_as_int(repair_rounds),
            test_command=test_command,
            **invocation.as_run_job_kwargs(),
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    report = export_job_report(job)
    if json_output:
        print(_json.dumps(report, indent=2))
        return
    print(f"Job {job.job_id}: {job.status}")
    print(f"  Isolation:  {job.isolation_mode}")
    if job.isolation_mode == "worktree":
        print(f"  Branch:     {job.worktree_branch}")
        print(f"  Worktree:   {job.worktree_path} ({job.worktree_cleanup_status})")
    for t in job.tasks:
        print(f"  {t.task_id}: {t.status}")


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


def _effective_timeout_sec(job: Any) -> int | None:
    """The timeout that ACTUALLY ran, read from the JobPlan's resolved execution config.

    F1 (round 16): the timeout hint used to read a local `timeout_sec` that the shared
    `RunInvocation` removed — `do job-flow` died with `NameError: timeout_sec is not defined`
    before printing anything. The tempting repair is to resolve a default back at the call site,
    but that is exactly what `RunInvocation` exists to prevent: an omitted control must stay
    `None` all the way into `run_job` so its explicit > persisted > product-default precedence
    decides. So the hint asks the JobPlan what `run_job` RESOLVED and recorded, after the fact.

    `None` when no execution config was persisted — the hint says nothing rather than inventing a
    number it cannot know.
    """
    ec = getattr(job, "execution_config", None)
    if ec is None:
        return None
    v = getattr(ec, "timeout_sec", None)
    return int(v) if isinstance(v, int) and not isinstance(v, bool) else None


def _build_timeout_hint(
    builder: str | None, reviewer: str | None, timeout_sec: int | None,
) -> str:
    """Warn when claude-cli providers run under recommended timeout.

    Informational only — it never changes execution. An unknown timeout produces no hint.
    """
    uses_cli = (builder == "claude-cli" or reviewer == "claude-cli")
    if not uses_cli or timeout_sec is None or timeout_sec >= 900:
        return ""
    return (
        f"Current timeout is {timeout_sec}s. Real claude-cli jobs usually "
        f"need ~900s per provider call. Consider --timeout-sec 900."
    )


def _read_final_verifier(ev_path: Any) -> dict[str, Any] | None:
    """Read final_verifier_report.json if it exists."""
    fv_path = ev_path / "final_verifier_report.json"
    if not fv_path.exists():
        return None
    try:
        import json as _json
        data = _json.loads(fv_path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and data.get("schema_version"):
            return data
    except (OSError, ValueError):
        pass
    return None


def _read_gate_report(ev_path: Any, filename: str) -> dict[str, Any] | None:
    """Read a job-level gate JSON from the evidence dir if it exists."""
    gate_path = ev_path / filename
    if not gate_path.exists():
        return None
    try:
        import json as _json
        data = _json.loads(gate_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except (OSError, ValueError):
        pass
    return None


def _read_token_truth(ev_path: Any) -> dict[str, Any] | None:
    """Read token_truth.json if it exists."""
    tt_path = ev_path / "token_truth.json"
    if not tt_path.exists():
        return None
    try:
        import json as _json
        data = _json.loads(tt_path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and data.get("schema_version"):
            return data
    except (OSError, ValueError):
        pass
    return None


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

    # --- Final verifier override ---
    fv_report = _read_final_verifier(ev_path)
    fv_verdict = fv_report.get("verdict", "") if fv_report else ""
    tt_report = _read_token_truth(ev_path)

    _FV_STATUS_MAP = {
        "BLOCKED": "BLOCKED",
        "NEEDS_TESTS": "NEEDS_TESTS",
        "NEEDS_REPAIR": "NEEDS_REPAIR",
        "PASS_WITH_RISKS": "NEEDS_REVIEW",
    }
    _FV_ACTION_MAP = {
        "BLOCKED": "Blocked: resolve gate violations before promoting.",
        "NEEDS_TESTS": "Run the missing tests before promoting.",
        "NEEDS_REPAIR": "Resolve the open findings before promoting.",
        "PASS_WITH_RISKS": "Approve with risks; review missing optional evidence before promoting.",
    }

    if fv_verdict in _FV_STATUS_MAP:
        status = _FV_STATUS_MAP[fv_verdict]
        action = _FV_ACTION_MAP[fv_verdict]
        if fv_verdict != "PASS":
            promote_ready = False
    elif all_passed and promote_ready and not missing_artifacts:
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

    result = {
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

    if fv_report:
        result["final_verifier_verdict"] = fv_verdict
        result["final_verifier_report_ref"] = "final_verifier_report.json"
        fv_auth = fv_report.get("authoritative_changed_files", [])
        if fv_auth:
            result["changed_files"] = sorted(set(fv_auth))
        raw_mtg = fv_report.get("missing_tests_gate", "")
        result["missing_tests_gate_status"] = raw_mtg
        result["scratch_file_guard_status"] = fv_report.get("scratch_file_guard", "")

        vt_path = ev_path / "verification_tests.json"
        vt_data = None
        if vt_path.exists():
            try:
                vt_data = json.loads(vt_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                pass
        vt_passed = (
            isinstance(vt_data, dict)
            and vt_data.get("exit_code") == 0
            and vt_data.get("passed", 0) > 0
            and vt_data.get("failed", 0) == 0
        )
        result["verification_tests_status"] = "PASS" if vt_passed else (
            "FAIL" if vt_data else ""
        )
        if vt_passed and raw_mtg == "NEEDS_TESTS":
            result["effective_missing_tests_gate_status"] = "PASS"
        else:
            result["effective_missing_tests_gate_status"] = raw_mtg
    if tt_report:
        result["token_truth_ref"] = "token_truth.json"
        result["token_truth_actual_available"] = tt_report.get("actual_available", False)
        result["token_truth_estimated_total"] = tt_report.get("estimated_total_tokens", 0)

    # Expose gate verdicts from the evidence pipeline.
    for gate_file, status_key in (
        ("fresh_evidence_gate.json", "fresh_evidence_gate_status"),
        ("artifact_contract_gate.json", "artifact_contract_gate_status"),
        ("runtime_integration_gate.json", "runtime_integration_gate_status"),
        ("change_provenance_gate.json", "change_provenance_gate_status"),
        ("commit_execution_gate.json", "commit_execution_gate_status"),
    ):
        gate_report = _read_gate_report(ev_path, gate_file)
        result[status_key] = gate_report.get("verdict", "") if gate_report else ""

    feg_report = _read_gate_report(ev_path, "fresh_evidence_gate.json")
    if feg_report:
        result["evidence_authoritative"] = feg_report.get("evidence_authoritative", False)
        ev_validity = feg_report.get("evidence_validity", {})
        result["evidence_validity_status"] = (
            "valid" if ev_validity.get("is_valid_current_run") else "invalid"
        )
    else:
        result["evidence_authoritative"] = False
        result["evidence_validity_status"] = ""

    # Wire final job review results into audit
    fjr_path = ev_path / "final_job_review.json"
    if fjr_path.exists():
        try:
            fjr_data = json.loads(fjr_path.read_text(encoding="utf-8"))
            result["final_job_review_verdict"] = fjr_data.get("verdict", "")
            result["final_job_review_ref"] = "final_job_review.json"
            result["final_job_review_findings_count"] = len(fjr_data.get("findings", []))
        except (OSError, ValueError):
            pass

    # Wire token cost policy results into audit
    tcp_path = ev_path / "token_cost_policy.json"
    if tcp_path.exists():
        try:
            tcp_data = json.loads(tcp_path.read_text(encoding="utf-8"))
            result["token_cost_policy_ref"] = "token_cost_policy.json"
            result["token_cost_risk_findings_count"] = len(tcp_data.get("cost_risk_findings", []))
        except (OSError, ValueError):
            pass

    # Hard consistency: if any gate is BLOCKED, final_audit cannot be READY.
    _HARD_BLOCK_GATE_KEYS = [
        "change_provenance_gate_status",
        "fresh_evidence_gate_status",
        "artifact_contract_gate_status",
        "runtime_integration_gate_status",
    ]
    ce_status = result.get("commit_execution_gate_status", "")
    gate_blocked = any(
        result.get(k) == "BLOCKED" for k in _HARD_BLOCK_GATE_KEYS
    ) or ce_status in ("BLOCKED", "NEEDS_TESTS", "NEEDS_REPAIR")
    if gate_blocked and result["status"] == "READY_FOR_APPROVAL":
        result["status"] = "BLOCKED"
        result["promote_ready"] = False
        result["recommended_next_action"] = (
            "Blocked: one or more verification gates failed. Resolve before promoting."
        )

    return result


def _sanitize_shareable_paths(obj: Any) -> Any:
    """Recursively sanitize absolute private paths in shareable JSON.

    Replaces private path prefixes with canonical refs while preserving
    trailing artifact names. Evidence paths become evidence/current/...,
    staging becomes [staging]/..., other private paths become [local]/...
    """
    import re

    _STAGING_RE = re.compile(r"/tmp/remedy-pingpong-[a-f0-9]+")
    _EVIDENCE_RE = re.compile(
        r"(?:/tmp|/[a-zA-Z0-9._/-]*)/remedy-job-evidence-[a-f0-9]+"
    )
    _JOB_WORKSPACE_RE = re.compile(
        r"[a-zA-Z0-9._/:-]*\.data/job_workspaces/[a-zA-Z0-9._/-]*"
    )
    _DATA_ROOT_RE = re.compile(
        r"[a-zA-Z0-9._/:-]*\.data/[a-zA-Z0-9._-]+"
    )
    _TMP_DIR_RE = re.compile(r"/tmp/[a-zA-Z0-9._-]+")
    _HOME_RE = re.compile(r"/home/[a-zA-Z0-9._-]+")
    _USERS_RE = re.compile(r"/Users/[a-zA-Z0-9._-]+")
    _PRIVATE_RE = re.compile(r"/private/[a-zA-Z0-9._-]+")
    _MNT_RE = re.compile(r"/mnt/[a-zA-Z0-9._-]+")

    if isinstance(obj, str):
        obj = _STAGING_RE.sub("[staging]", obj)
        obj = _EVIDENCE_RE.sub("evidence/current", obj)
        obj = _JOB_WORKSPACE_RE.sub("[workspace]", obj)
        obj = _DATA_ROOT_RE.sub("[data]", obj)
        obj = _TMP_DIR_RE.sub("[tmpdir]", obj)
        obj = _HOME_RE.sub("[local]", obj)
        obj = _USERS_RE.sub("[local]", obj)
        obj = _PRIVATE_RE.sub("[local]", obj)
        obj = _MNT_RE.sub("[local]", obj)
        return obj
    if isinstance(obj, dict):
        return {k: _sanitize_shareable_paths(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_shareable_paths(v) for v in obj]
    return obj


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
        status = getattr(job, "status", "") or ""
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


def _persist_evidence_index(job_id: str, evidence_out: str, trace_summary: dict) -> None:
    """Write evidence location index under Remedy data dir for cockpit bridge.

    Delegates to the shared index writer so job-flow and job-evidence produce one
    record format (no second index).
    """
    try:
        _index_job_evidence(job_id, evidence_out, "do.job-flow")
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


def _persist_command_transcript(
    job_id: str,
    evidence_out: str,
    flow_result: dict,
    repo: str,
    started_at: str,
    target_hash_before: str,
    target_hash_after: str,
    changed_content_files: list[str] | None = None,
    ignored_noise_files: list[str] | None = None,
    ignored_operational_artifacts: list[str] | None = None,
) -> None:
    """Write command_transcript.json to evidence output directory.

    Terminal artifact: must be called AFTER final_audit, final_verifier,
    commit_execution_gate, job_flow.json, and target_guard.json are stable.

    Mutation reporting uses the same three-way classification policy as the
    target guard: only real source changes count as a target mutation.
    Operational review/evidence artifacts (remedy-review-*.zip, run_transcript.txt,
    remedy-job-evidence-* bundles) and volatile tool-cache files (.mypy_cache,
    .pytest_cache, .ruff_cache, __pycache__, *.pyc, ...) never count as a target
    mutation. This keeps command_transcript.json and target_guard.json from
    contradicting each other when only operational/cache files change.
    """
    from datetime import datetime, timezone
    from pathlib import Path

    changed_content_files = changed_content_files or []
    ignored_noise_files = ignored_noise_files or []
    ignored_operational_artifacts = ignored_operational_artifacts or []

    out_path = Path(evidence_out).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    # Read target_guard.json for authoritative mutation state
    tg_data: dict = {}
    tg_path = out_path / "target_guard.json"
    if tg_path.exists():
        try:
            tg_data = json.loads(tg_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass

    # Use target_guard as source of truth for mutation fields when available.
    # target_guard.json is authoritative — its explicit false values override
    # any classification derived from ignored lists.
    if tg_data:
        target_repo_mutated = bool(tg_data.get("target_mutated", False))
        target_content_mutated = bool(tg_data.get("target_content_mutated", False))
        target_noise_changed = bool(tg_data.get("target_noise_changed", False))
        target_operational_artifacts_changed = bool(
            tg_data.get("target_operational_artifacts_changed", False)
        )
    else:
        target_repo_mutated = bool(changed_content_files)
        target_content_mutated = bool(changed_content_files)
        target_noise_changed = bool(ignored_noise_files)
        target_operational_artifacts_changed = bool(ignored_operational_artifacts)

    final_audit = flow_result.get("final_audit", {})
    effective_promote_ready = final_audit.get("promote_ready", flow_result.get("promote_ready", False))

    transcript = {
        "command_id": "do.job-flow",
        "argv_safe": "remedy do job-flow --job-file <job> --repo <repo> --out <evidence>",
        "repo_ref_safe": "<repo>",
        "evidence_ref": "evidence/current",
        "json_stdout_preview_safe": _sanitize_shareable_paths({
            "command": flow_result.get("command", "do.job-flow"),
            "job_id": job_id,
            "status": final_audit.get("status", "unknown"),
            "promote_ready": effective_promote_ready,
            "next_approve_command_safe": flow_result.get("next_approve_command_safe", ""),
        }),
        "final_audit": final_audit,
        "promote_ready": effective_promote_ready,
        "stderr_ref": "",
        "exit_code": 0,
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "target_repo_hash_before": target_hash_before,
        "target_repo_hash_after": target_hash_after,
        "target_repo_mutated": target_repo_mutated,
        "target_content_mutated": target_content_mutated,
        "target_operational_artifacts_changed": target_operational_artifacts_changed,
        "target_noise_changed": target_noise_changed,
        "ignored_operational_artifacts": sorted(ignored_operational_artifacts),
        "ignored_noise_files": sorted(ignored_noise_files),
        "data_root_ref_safe": "<data>",
        "review_zip_hint": "scripts/make_review_zip.sh --evidence-dir <evidence>",
        "target_guard": tg_data if tg_data else {"note": "target_guard.json not available at transcript time"},
    }
    (out_path / "command_transcript.json").write_text(
        json.dumps(transcript, indent=2) + "\n"
    )


def _persist_observability_index(evidence_out: str) -> dict:
    """Build self_run_observability_index.json in the evidence directory.

    Best-effort: never raises, so it can never fail the job flow. The index
    builder itself marks missing data as ``"absent"``, so it still produces a
    file on incomplete evidence dirs.

    Returns a status dict to merge into the job-flow output:
      - ``observability_index_status``: ``"generated"``, ``"failed"``, or
        ``"skipped"``
      - ``observability_index_error``: present only when not ``"generated"``
      - ``observability_index_ref``: present only when ``"generated"``
    """
    import importlib.util
    from pathlib import Path

    try:
        repo_root = Path(__file__).resolve().parents[3]
        script_path = repo_root / "scripts" / "build_observability_index.py"
        if not script_path.is_file():
            reason = f"builder script not found at {script_path}"
            sys.stderr.write(
                f"Warning: observability index skipped: {reason}\n"
            )
            return {
                "observability_index_status": "skipped",
                "observability_index_error": reason,
            }
        spec = importlib.util.spec_from_file_location(
            "remedy_build_observability_index", str(script_path)
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot load builder at {script_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.write_observability_index(str(Path(evidence_out).resolve()))
        return {
            "observability_index_status": "generated",
            "observability_index_ref": "self_run_observability_index.json",
        }
    except Exception as exc:  # noqa: BLE001 - must never fail the job flow
        sys.stderr.write(
            f"Warning: observability index generation failed: {exc}\n"
        )
        return {
            "observability_index_status": "failed",
            "observability_index_error": str(exc),
        }


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

    Job/task lifecycle events are reconstructed from persisted run data. When a
    task captured F004 raw stream evidence, its provider/tool events (tool use,
    tool result, API retry, provider result, provider error, stream cap) come
    from the normalized ``run_events.jsonl`` instead and are marked
    ``normalized_raw_stream`` — never duplicated by reconstruction.
    """
    from packages.orchestration.agent_run_trace import (
        create_trace_event,
        task_has_stream_evidence,
        trace_events_from_task_streams,
    )
    from packages.orchestration.data_paths import jobs_dir
    from packages.orchestration.pingpong_loop import _provider_kind, load_run

    _SRC = "reconstructed_legacy_evidence"
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

        # F004: normalized provider/tool events replace reconstruction for this
        # task when its per-call stream artifacts exist.
        _task_ev_dir = jobs_dir() / job_id / "evidence" / "task_runs" / task.task_id
        if task_has_stream_evidence(_task_ev_dir):
            events.extend(trace_events_from_task_streams(
                _task_ev_dir, job_id=job_id, task_id=task.task_id, run_id=task.run_id,
            ))

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
    invocation: RunInvocation | None = None,
    out: str = "",
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
) -> None:
    """Compose the safe job workflow as one human-readable command.

    Runs, in order: job-plan → job-run → job-report → job-evidence →
    job-promote --dry-run. It stops before an approved promote: the real
    target repo is never mutated and no git commit/push/reset/checkout is
    performed. When the dry-run is ready, a clear next approve command is
    printed.
    """
    from apps.cli.commands.run_invocation import RunInvocation
    if invocation is None:
        invocation = RunInvocation()
    if not job_file:
        print("Error: --job-file is required", file=sys.stderr)
        sys.exit(2)
    # Per-role model override flags are validated and resolved at the CLI
    # layer (invalid values exit 2) before any run work begins.
    role_configs = _resolve_cli_role_configs(
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

    import hashlib as _hashlib
    from datetime import datetime, timezone
    from pathlib import Path as _RepoPath

    from packages.orchestration.pingpong_job import (
        export_job_report,
        format_job_report_text,
        load_job_plan,
        plan_job_from_file,
        run_job,
    )

    # --- 0. Capture start state for command transcript ---
    _started_at = datetime.now(timezone.utc).isoformat()

    def _target_repo_snapshot(repo_dir: str) -> dict[str, str]:
        """Map of {rel_path: content_hash} for every non-.git file in the repo.

        Used both to derive the aggregate repo hash and to classify which
        files changed (real source vs. ignored tool-cache noise).
        """
        rp = _RepoPath(repo_dir)
        snapshot: dict[str, str] = {}
        if not rp.is_dir():
            return snapshot
        for p in sorted(rp.rglob("*")):
            if p.is_file() and ".git" not in p.parts:
                fh = _hashlib.sha256()
                rel = p.relative_to(rp).as_posix()
                fh.update(rel.encode())
                try:
                    fh.update(p.read_bytes())
                except OSError:
                    pass
                snapshot[rel] = fh.hexdigest()[:16]
        return snapshot

    def _quick_repo_hash(repo_dir: str) -> str:
        rp = _RepoPath(repo_dir)
        if not rp.is_dir():
            return "missing"
        h = _hashlib.sha256()
        for rel, file_hash in sorted(_target_repo_snapshot(repo_dir).items()):
            h.update(rel.encode())
            h.update(file_hash.encode())
        return h.hexdigest()[:16]

    _repo_snapshot_before = _target_repo_snapshot(repo)
    _repo_hash_before = _quick_repo_hash(repo)

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
        **invocation.as_run_job_kwargs(),
    )

    # --- 3. job-report (reload for an authoritative view) ---
    report_job = load_job_plan(job_id) or job
    report_data = export_job_report(report_job)

    # --- 4. job-evidence ---
    from packages.orchestration.data_paths import job_evidence_export_dir as _jeed
    from packages.orchestration.job_evidence import export_job_evidence
    from packages.orchestration.review_subject import read_declared_base
    evidence_out = out or str(_jeed(job_id))
    # F6 (round 17): forward the operator's declared review base, read ONCE here at the top level.
    # `do job-evidence` already did this; `do job-flow` did not, so a clean committed feature
    # branch exported through the full workflow lost its committed ReviewSubject entirely —
    # `export_job_evidence` correctly reads no ambient environment (F6, round 16), so a base that
    # is not passed is a base that does not exist.
    evidence_result = export_job_evidence(
        job_id, evidence_out, declared_base=read_declared_base())

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
    # F1 (round 16): the hint reports what `run_job` RESOLVED and persisted — never a default
    # re-invented here, which would defeat the invocation's omission sentinel.
    timeout_warning = _build_timeout_hint(
        builder, reviewer, _effective_timeout_sec(report_job))

    # Add final_audit_completed to trace
    run_trace_events.append(create_trace_event(
        "final_audit_completed",
        job_id=job_id,
        status=final_audit["status"],
        safe_summary=final_audit["recommended_next_action"],
        trace_source="reconstructed_legacy_evidence",
    ))
    # Re-persist trace and summary with final event
    write_run_trace_jsonl(run_trace_events, ev_path / "agent_run_trace.jsonl")
    run_trace_summary = build_run_trace_summary(run_trace_events)
    (ev_path / "agent_run_trace_summary.json").write_text(
        json.dumps(run_trace_summary, indent=2) + "\n"
    )

    # --- 8. Persist job_flow.json to evidence output ---
    # Use final_audit's promote_ready which may have been overridden by
    # final verifier verdict (e.g. NEEDS_TESTS -> promote_ready=false).
    effective_promote_ready = final_audit.get("promote_ready", promote_ready)
    flow_result = {
        "command": "do.job-flow",
        "job_id": job_id,
        "steps": ["job-plan", "job-run", "job-report", "job-evidence", "job-promote-dry-run"],
        "report": report_data,
        "evidence": evidence_result,
        "promote_dry_run": export_job_promotion_json(promo),
        "promote_ready": effective_promote_ready,
        "next_approve_command": next_approve_command if effective_promote_ready else "",
        "next_approve_command_safe": next_approve_command_safe if effective_promote_ready else "",
        "token_summary": token_summary,
        "final_audit": final_audit,
        "timeout_warning": timeout_warning,
        "agent_run_trace_summary": run_trace_summary,
        "role_configs": role_configs,
    }

    _persist_job_flow_json(flow_result, evidence_out)

    # --- 9. Persist evidence index for cockpit bridge (after job_flow.json) ---
    _persist_evidence_index(job_id, evidence_out, run_trace_summary)

    # --- 10. Persist command transcript ---
    # Classify changed files using the same noise-exclusion policy as the
    # target guard, so the transcript never claims a target mutation when only
    # volatile tool-cache files (.mypy_cache, .pytest_cache, .ruff_cache, ...)
    # changed. Without this, hash-only comparison contradicts target_guard.json.
    from packages.orchestration.pingpong_loop import (
        _is_operational_artifact,
        _is_target_noise,
    )
    _repo_snapshot_after = _target_repo_snapshot(repo)
    _repo_hash_after = _quick_repo_hash(repo)
    _changed_rel_paths = [
        rel for rel in set(_repo_snapshot_before) | set(_repo_snapshot_after)
        if _repo_snapshot_before.get(rel) != _repo_snapshot_after.get(rel)
    ]
    # Three-way classification (must agree with target guard): operational
    # review/evidence artifacts and cache noise never count as a source mutation.
    _ignored_operational_artifacts = sorted(
        rel for rel in _changed_rel_paths if _is_operational_artifact(rel)
    )
    _ignored_noise_files = sorted(
        rel for rel in _changed_rel_paths
        if not _is_operational_artifact(rel) and _is_target_noise(rel)
    )
    _changed_content_files = sorted(
        rel for rel in _changed_rel_paths
        if not _is_operational_artifact(rel) and not _is_target_noise(rel)
    )
    # --- 11. Build observability index (best-effort; never fails job flow) ---
    # The index is generated AFTER job_flow.json is first written (it reads the
    # evidence dir, including job_flow.json). Re-persist job_flow.json so the
    # index status lands in a durable evidence artifact, not only in stdout.
    index_status = _persist_observability_index(evidence_out)
    flow_result.update(index_status)
    _persist_job_flow_json(flow_result, evidence_out)

    # --- 12. Terminal artifact: command transcript ---
    # Written AFTER observability index and final job_flow.json so all fields
    # are stable. Reads target_guard.json for authoritative mutation state.
    _persist_command_transcript(
        job_id, evidence_out, flow_result, repo,
        _started_at, _repo_hash_before, _repo_hash_after,
        changed_content_files=_changed_content_files,
        ignored_noise_files=_ignored_noise_files,
        ignored_operational_artifacts=_ignored_operational_artifacts,
    )

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
    if effective_promote_ready:
        print(f"  Would apply {len(promo.files_planned)} file(s). No target files changed.")
        print("  The target repo stays unchanged until you explicitly approve the promote.")
        print("\nNext (approval required):")
        print(f"  {next_approve_command}")
    else:
        reason = promo.blocked_reason or "see report"
        fv_v = final_audit.get("final_verifier_verdict", "")
        if fv_v and fv_v != "PASS":
            reason = f"final verifier: {fv_v}"
        print(f"  Not ready to promote: {reason}")
        print("  The target repo was not changed.")

    # Final audit
    _print_final_audit(final_audit)


def _cmd_do_replan(
    job_id_str: str,
    *,
    json_output: bool = False,
) -> None:
    """Regenerate the flight plan for an existing job."""
    from packages.orchestration.data_paths import job_evidence_export_dir, resolve_job_id
    from packages.orchestration.storage import JobNotFoundError, load_job, save_job

    job_id = resolve_job_id(job_id_str)
    try:
        job = load_job(job_id)
    except JobNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    fp = getattr(job, "flight_plan", None)
    if not isinstance(fp, dict):
        print("Error: job has no flight plan to replan.", file=sys.stderr)
        sys.exit(1)

    intake = getattr(job, "intake", None)
    if not isinstance(intake, dict):
        print("Error: job has no intake data.", file=sys.stderr)
        sys.exit(1)

    from packages.orchestration.intake import make_structured_call_fn
    from packages.orchestration.schemas.models import FlightPlan
    # Replanning is a flight-plan call: bind the provider's native schema to
    # FlightPlan, not to the intake model.
    call_fn = make_structured_call_fn(FlightPlan)
    if call_fn is None:
        print("Error: no provider available for replan.", file=sys.stderr)
        sys.exit(1)

    any_completed = any(
        getattr(t, "status", None) in ("completed", "passed")
        for t in getattr(job, "tasks", [])
    )

    from packages.orchestration.flight_plan import (
        ReplanRejectedError,
        compose_flight_plan_prompt,
        make_flight_plan_call_recorder,
        map_flight_plan_to_tasks,
        plan_job_llm,
        replan,
    )

    replan_traces: list = []
    replan_composed = compose_flight_plan_prompt(intake)
    fp_result = plan_job_llm(
        intake,
        call_fn,
        composed=replan_composed,
        on_call=make_flight_plan_call_recorder(
            replan_traces,
            replan_composed,
            provider="ollama",
            provider_kind="ollama",
        ),
    )
    if fp_result.plan is None:
        print(
            f"Error: replan failed: {fp_result.error_hint or 'parse failure'}",
            file=sys.stderr,
        )
        sys.exit(1)

    ev_dir = job_evidence_export_dir(str(job.id))
    try:
        new_fp_dict, version = replan(
            fp, fp_result.plan, ev_dir,
            any_task_completed=any_completed,
            transformations=fp_result.transformations,
        )
    except ReplanRejectedError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    new_fp_dict["_normalization"] = fp_result.transformations
    job.flight_plan = new_fp_dict
    job.tasks = map_flight_plan_to_tasks(fp_result.plan)
    save_job(job)

    # APPEND, never write: this job's first run already left its intake and
    # flight-plan traces in the same per-job file (F105 R28).
    if replan_traces:
        from packages.orchestration.prompt_trace import append_trace_jsonl
        from packages.orchestration.run_log import RunLogWriter
        log = RunLogWriter(job_id=job.id)
        try:
            append_trace_jsonl(replan_traces, log.path.parent / "prompt_trace.jsonl")
        except OSError:
            pass

    if json_output:
        print(json.dumps({
            "job_id": str(job.id),
            "version": version,
            "approval": new_fp_dict.get("_approval", "pending"),
        }, indent=2))
    else:
        print(f"Replanned job {str(job.id)[:8]} → version {version} (awaiting approval)")


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
        builder=getattr(args, "builder", None) or "none",
        reviewer=getattr(args, "reviewer", None) or "none",
        max_rounds=int(getattr(args, "max_rounds", None) or 3),
        mode=getattr(args, "mode", None) or "staged",
        test_command=getattr(args, "test_command", None) or "",
        provider_timeout_sec=_resolve_timeout_precedence(int(getattr(args, "provider_timeout_sec")) if getattr(args, "provider_timeout_sec", None) is not None else None, getattr(args, "timeout_profile", None))[0],
        timeout_profile=_resolve_timeout_precedence(int(getattr(args, "provider_timeout_sec")) if getattr(args, "provider_timeout_sec", None) is not None else None, getattr(args, "timeout_profile", None))[1],
        max_output_chars_val=int(getattr(args, "max_output_chars", None) or 50000),
        keep_staging=getattr(args, "keep_staging", False),
        claude_cli_write_mode=getattr(args, "claude_cli_write_mode", None) or "none",
        task_file=getattr(args, "task_file", None) or "",
        task_stdin=getattr(args, "task_stdin", False),
        scope_file=getattr(args, "scope_file", None) or "",
        approve_scope=getattr(args, "approve_scope", False),
        repair_rounds=getattr(args, "repair_rounds", None),
        stream_evidence=getattr(args, "stream_evidence", False),
        max_total_tokens=getattr(args, "max_total_tokens", None),
        max_provider_calls=getattr(args, "max_provider_calls", None),
        max_wall_clock_minutes=getattr(args, "max_wall_clock_minutes", None),
        max_cost_usd=getattr(args, "max_cost_usd", None),
        deadline=getattr(args, "deadline", None),
        no_llm=getattr(args, "no_llm", False),
        yes=getattr(args, "yes", False),
    ),
    "do.replan": lambda args: _cmd_do_replan(
        args.job_id,
        json_output=getattr(args, "json", False),
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
    "do.repair-attest": lambda args: _cmd_do_repair_attest(
        args.job_id,
        args.task_id,
        note=getattr(args, "note", None) or "",
        repo=getattr(args, "repo", None) or ".",
        yes=getattr(args, "yes", False),
        task_scoped=getattr(args, "task_scoped", False),
        allowed_files=getattr(args, "allowed_files", None)
        or getattr(args, "expected_files", None) or "",
        linked_prior_job_id=getattr(args, "linked_prior_job_id", None) or "",
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
        max_total_tokens=getattr(args, "max_total_tokens", None),
        max_provider_calls=getattr(args, "max_provider_calls", None),
        max_wall_clock_minutes=getattr(args, "max_wall_clock_minutes", None),
        max_cost_usd=getattr(args, "max_cost_usd", None),
        deadline=getattr(args, "deadline", None),
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
    "do.job-resume": lambda args: _cmd_do_job_resume(
        args.job_id,
        builder=getattr(args, "builder", None),
        reviewer=getattr(args, "reviewer", None),
        max_rounds=getattr(args, "max_rounds", None),
        repair_rounds=getattr(args, "repair_rounds", None),
        test_command=getattr(args, "test_command", None),
        invocation=_invocation_from_args(args),
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
        verification_command=getattr(args, "verification_command", None),
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
        invocation=_invocation_from_args(args),
        out=getattr(args, "out", None) or "",
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
    ),
}
