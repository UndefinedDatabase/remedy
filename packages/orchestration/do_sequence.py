"""F268 — `remedy do "<order>"` as DATA: the step names, the step table, one walker.

This first slice holds only the shape step's job planning, moved here from
`_cmd_do_mission` in apps/cli/commands/do_cmd.py; the sequence, the step table
and the walker follow (DECISION F268 D4).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from packages.orchestration.pingpong_job import JobPlan
    from packages.orchestration.project_registry import RemyProject


# ---------------------------------------------------------------------------
# The shape step's job planning — moved here from `_cmd_do_mission` in
# apps/cli/commands/do_cmd.py (the F147 golden path), not copied.
# ---------------------------------------------------------------------------


class OrderJobPlanError(Exception):
    """The task plan for an order could not be generated; the job is left unplanned."""


@dataclass
class OrderJobPlan:
    """The one job planned for an order, and how its intake and plan were made."""

    job: JobPlan
    intake_result: Any
    intake_fallback_reason: str
    plan_label: str

    @property
    def intake_label(self) -> str:
        if self.intake_result.source == "llm":
            return "intake: llm"
        if self.intake_fallback_reason == "forced":
            return "intake: heuristic (forced by --no-llm)"
        if self.intake_fallback_reason == "provider_unavailable":
            return "intake: heuristic fallback (provider unavailable)"
        if self.intake_fallback_reason == "provider_error":
            return "intake: heuristic fallback (provider error)"
        return f"intake: {self.intake_result.source}"

    def to_json(self) -> dict[str, Any]:
        return {
            "job_id": str(self.job.job_id),
            "state": self.job.state.value,
            "order": self.job.mission,
            "intake": {
                "source": self.intake_result.source,
                "goal": self.intake_result.value.goal,
                "fallback_reason": self.intake_fallback_reason,
            },
            "tasks": [
                {"task_id": str(t.task_id), "description": t.title}
                for t in self.job.tasks
            ],
            "plan_label": self.plan_label,
        }


def plan_order_job(
    order: str,
    *,
    project: RemyProject,
    repo_path: str = "",
    no_llm: bool = False,
    yes: bool = False,
) -> OrderJobPlan:
    """Plan ONE job for an order: intake, then an LLM task plan or the deterministic skeleton.

    ``repo_path`` is the job's target repository. ``yes`` auto-approves an LLM
    task plan through ``job_plan.auto_approve_task_plan`` (F034). The job is
    saved and attached to ``project``. Raises :class:`OrderJobPlanError` when
    an LLM task plan cannot be parsed, after writing the job's post-mortem.
    """
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

    mission = order
    repo = repo_path
    target_repo_path = str(Path(repo_path).resolve()) if repo_path else ""

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
                repo_path=target_repo_path,
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
                repo_path=target_repo_path,
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
            raise OrderJobPlanError(
                f"task plan generation failed: "
                f"{fp_result.error_hint or 'parse failure'}"
            )

    if job is None:
        job = JobPlan(
            job_title=mission[:80], mission=mission, user_prompt=mission,
            project_id=str(project.id),
            repo_path=target_repo_path,
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

    return OrderJobPlan(
        job=job,
        intake_result=intake_result,
        intake_fallback_reason=intake_fallback_reason,
        plan_label=plan_label,
    )
