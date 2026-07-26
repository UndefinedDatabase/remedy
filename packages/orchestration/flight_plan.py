"""F014 — LLM-generated Flight Plan.

Turns a job's intake into a validated, DAG-structured FlightPlan via an
LLM call (with one parse retry), then maps it onto core Task objects.
Deterministic planner remains the --no-llm/provider-down fallback.
"""
from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packages.core.models import AcceptanceCheck, RunState, Task
from packages.orchestration.schemas.models import _LARGE_PLAN_THRESHOLD, FlightPlan
from packages.orchestration.structured_outputs import StructuredOutcome, run_structured_call
from packages.orchestration.task_granularity import GranularityConfig, normalize_plan


@dataclass
class FlightPlanResult:
    """Result of plan_job_llm."""

    plan: FlightPlan | None
    source: str
    error_hint: str = ""
    calls: int = 0
    call_log: list[dict[str, Any]] | None = None
    #: F016 granularity record: what normalization changed, if anything.
    transformations: list[dict[str, Any]] = field(default_factory=list)


_PLAN_PROMPT_TEMPLATE = """\
You are a project planner. Given the intake and repo facts below, produce
a flight plan: a DAG of tasks with goals, acceptance criteria, dependencies,
and token band estimates.

## Intake
{intake_json}

## Repo Facts
{repo_facts}

## Rules
- Each task needs a unique id (e.g. "T001", "T002").
- depends_on lists task ids that must complete first.
- est_tokens_band is one of: S, M, L, XL.
- acceptance must have at least one non-empty criterion per task.
- No cycles in dependencies.
- Maximum 25 tasks.
- If clarifications were present in the intake, carry them into
  clarifications_resolved with your chosen answer.

Return ONLY a JSON object matching the flight_plan_v1 schema.
"""


def _cheap_repo_facts() -> str:
    """Gather minimal repo context for the planner prompt."""
    import os
    lines: list[str] = []
    cwd = os.getcwd()
    try:
        entries = sorted(os.listdir(cwd))
        dirs = [e for e in entries if os.path.isdir(os.path.join(cwd, e))
                and not e.startswith(".")]
        files = [e for e in entries if os.path.isfile(os.path.join(cwd, e))
                 and not e.startswith(".")]
        if dirs:
            lines.append(f"Top-level dirs: {', '.join(dirs[:20])}")
        if files:
            lines.append(f"Top-level files: {', '.join(files[:20])}")
    except OSError:
        lines.append("(repo listing unavailable)")
    return "\n".join(lines) if lines else "(no repo facts available)"


def _build_plan_prompt(intake_dict: dict[str, Any]) -> str:
    return _PLAN_PROMPT_TEMPLATE.format(
        intake_json=json.dumps(intake_dict, indent=2),
        repo_facts=_cheap_repo_facts(),
    )


def granularity_config() -> GranularityConfig:
    """Read the F016 thresholds from Remedy config.

    Lives here, not in task_granularity: that module stays pure and takes
    its thresholds as an argument.
    """
    from packages.orchestration.config import get_config
    cfg = get_config()
    return GranularityConfig(
        enabled=bool(cfg.get("planning.granularity.enabled")),
        split_band=str(cfg.get("planning.granularity.split_band")),
        max_acceptance=int(cfg.get("planning.granularity.max_acceptance")),
        merge_group_size=int(cfg.get("planning.granularity.merge_group_size")),
    )


def plan_job_llm(
    intake: dict[str, Any],
    call_fn: Callable[[str, int], str],
    *,
    on_call: Callable[[int, str, bool, str], None] | None = None,
    granularity: GranularityConfig | None = None,
) -> FlightPlanResult:
    """Generate a FlightPlan from a job's intake via LLM.

    Uses run_structured_call for schema validation + one parse retry.
    Returns a FlightPlanResult; on failure, plan is None and error_hint
    describes the failure class.

    The validated plan then passes through F016 task-granularity
    normalization — the single insertion point for it — and the result
    carries the transformation record.
    """
    prompt = _build_plan_prompt(intake)
    try:
        outcome: StructuredOutcome = run_structured_call(
            FlightPlan,
            prompt,
            call_fn,
            on_call=on_call,
            allow_parse_retry=True,
        )
    except Exception as exc:
        return FlightPlanResult(
            plan=None, source="llm", error_hint=f"provider error: {exc}")

    if not outcome.ok:
        return FlightPlanResult(
            plan=None,
            source="llm",
            error_hint=outcome.hint,
            calls=outcome.calls,
            call_log=outcome.call_log,
        )

    assert isinstance(outcome.value, FlightPlan)
    plan = outcome.value
    transformations: list[dict[str, Any]] = []
    try:
        normalized = normalize_plan(plan, granularity or granularity_config())
        plan = normalized.plan
        transformations = normalized.as_dicts()
    except Exception as exc:
        # Misconfigured thresholds must not lose a valid plan; same fail-open
        # rule the normalizer applies to its own revalidation.
        transformations = [{
            "kind": "aborted",
            "source_ids": [t.id for t in plan.tasks],
            "result_ids": [t.id for t in plan.tasks],
            "reason": f"normalization not run, original plan kept: {exc}",
        }]

    return FlightPlanResult(
        plan=plan,
        source="llm",
        calls=outcome.calls,
        call_log=outcome.call_log,
        transformations=transformations,
    )


def map_flight_plan_to_tasks(plan: FlightPlan) -> list[Task]:
    """Convert FlightPlan tasks to core Task objects, preserving order.

    Flight plan metadata is stored in task.inputs["flight"] so the
    runner and evidence pipeline can trace provenance without modifying
    the core Task model.
    """
    tasks: list[Task] = []
    for pt in plan.tasks:
        task = Task(
            description=f"{pt.title}: {pt.goal}",
            acceptance_checks=[
                AcceptanceCheck(description=ac) for ac in pt.acceptance
            ],
            inputs={
                "flight": {
                    "planned_id": pt.id,
                    "title": pt.title,
                    "depends_on": list(pt.depends_on),
                    "est_tokens_band": pt.est_tokens_band,
                    "files_hint": list(pt.files_hint),
                },
            },
            status=RunState.PENDING,
        )
        tasks.append(task)
    return tasks


def apply_plan_budgets(
    job_budgets: dict[str, Any] | None,
    plan_budgets: dict[str, int | str | None] | None,
) -> dict[str, Any] | None:
    """Merge plan-suggested budgets into job budgets (CLI/config wins).

    Returns the merged dict, or None if both inputs are None.
    Plan budgets fill only UNSET fields — explicit user values are never
    overwritten.
    """
    if plan_budgets is None:
        return job_budgets
    if job_budgets is None:
        return dict(plan_budgets)
    merged = dict(job_budgets)
    for key, val in plan_budgets.items():
        if key not in merged or merged[key] is None:
            merged[key] = val
    return merged


def apply_plan_fences(
    job_fences: dict[str, list[str]] | None,
    plan_fences: dict[str, list[str]] | None,
) -> dict[str, list[str]] | None:
    """Merge plan-suggested fences into job fences (CLI/config wins).

    Returns the merged dict, or None if both inputs are None.
    Plan fences fill only UNSET fields — explicit user values are never
    overwritten.
    """
    if plan_fences is None:
        return job_fences
    if job_fences is None:
        return dict(plan_fences)
    merged = dict(job_fences)
    for key, val in plan_fences.items():
        if key not in merged or not merged[key]:
            merged[key] = val
    return merged


# ---------------------------------------------------------------------------
# Renderer (T003)
# ---------------------------------------------------------------------------

def render_plan_md(
    plan: FlightPlan,
    transformations: list[dict[str, Any]] | None = None,
) -> str:
    """Render a FlightPlan to deterministic, stably ordered markdown.

    *transformations* is the F016 granularity record. The section is always
    rendered so the approving human sees either what was changed or an
    explicit statement that nothing was.
    """
    lines: list[str] = []
    lines.append("# Flight Plan")
    lines.append("")
    lines.append(f"Schema: {plan.schema_v}")
    lines.append(f"Tasks: {len(plan.tasks)}")
    lines.append("")

    if plan.large_plan:
        lines.append(
            f"> **Note:** This plan has {len(plan.tasks)} tasks "
            f"(threshold {_LARGE_PLAN_THRESHOLD}). "
            "Consider splitting the mission into smaller units.")
        lines.append("")

    lines.append("## Tasks")
    lines.append("")

    for i, t in enumerate(plan.tasks, 1):
        deps = ", ".join(t.depends_on) if t.depends_on else "none"
        lines.append(f"### {i}. {t.id} — {t.title}")
        lines.append("")
        lines.append(f"**Goal:** {t.goal}")
        lines.append(f"**Band:** {t.est_tokens_band} | **Depends on:** {deps}")
        lines.append("")
        lines.append("**Acceptance:**")
        for ac in t.acceptance:
            lines.append(f"- {ac}")
        if t.files_hint:
            lines.append("")
            lines.append("**Files hint:**")
            for f in t.files_hint:
                lines.append(f"- `{f}`")
        lines.append("")

    lines.append("## Normalization")
    lines.append("")
    if not transformations:
        lines.append("No transformations — the plan is used as generated.")
        lines.append("")
    else:
        for entry in transformations:
            sources = ", ".join(entry.get("source_ids", [])) or "-"
            results = ", ".join(entry.get("result_ids", [])) or "-"
            lines.append(
                f"- **{entry.get('kind', 'unknown')}** {sources} → {results}")
            lines.append(f"  - {entry.get('reason', '')}")
        lines.append("")

    if plan.risks:
        lines.append("## Risks")
        lines.append("")
        for r in plan.risks:
            lines.append(f"- {r}")
        lines.append("")

    if plan.clarifications_resolved:
        lines.append("## Clarifications Resolved")
        lines.append("")
        for c in plan.clarifications_resolved:
            lines.append(f"**Q:** {c.question}")
            lines.append(f"**A:** {c.answer} (default: {c.default_answer})")
            lines.append(f"**Impact:** {c.impact}")
            lines.append("")

    if plan.budgets:
        lines.append("## Budgets")
        lines.append("")
        for k, v in sorted(plan.budgets.items()):
            lines.append(f"- {k}: {v}")
        lines.append("")

    if plan.fences:
        lines.append("## Fences")
        lines.append("")
        for k, v in sorted(plan.fences.items()):
            lines.append(f"- {k}: {', '.join(v) if isinstance(v, list) else v}")
        lines.append("")

    return "\n".join(lines)


def write_plan_md(
    plan: FlightPlan,
    evidence_dir: Path,
    version: int = 1,
    transformations: list[dict[str, Any]] | None = None,
) -> Path:
    """Write rendered plan to evidence dir. Returns the written path."""
    evidence_dir.mkdir(parents=True, exist_ok=True)
    filename = "plan.md" if version == 1 else f"plan_v{version}.md"
    path = evidence_dir / filename
    path.write_text(render_plan_md(plan, transformations), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Replan versioning (T003)
# ---------------------------------------------------------------------------

def flight_plan_blocks_execution(job: Any) -> str | None:
    """Return blocking reason if flight plan prevents execution, else None.

    Returns "pending" when awaiting approval, "rejected" when plan was
    rejected and needs replanning.
    """
    fp = getattr(job, "flight_plan", None)
    if not isinstance(fp, dict):
        return None
    approval = fp.get("_approval")
    if approval in ("pending", "rejected"):
        return approval
    return None


def flight_plan_approval_open(job: Any) -> bool:
    """Return True if the job has a pending flight plan approval gate."""
    return flight_plan_blocks_execution(job) is not None


class ReplanRejectedError(Exception):
    """Raised when replanning is rejected (e.g. after task completion)."""


def replan(
    job_flight_plan: dict[str, Any],
    new_plan: FlightPlan,
    evidence_dir: Path,
    *,
    any_task_completed: bool = False,
    transformations: list[dict[str, Any]] | None = None,
) -> tuple[dict[str, Any], int]:
    """Apply a new flight plan version.

    Returns (updated flight_plan dict for Job, new version number).
    Raises ReplanRejectedError if any task has already completed.
    Old plan.md files are kept (plan.md, plan_v2.md, plan_v3.md, ...).
    """
    if any_task_completed:
        raise ReplanRejectedError(
            "Cannot replan after a task has completed. "
            "This limitation will be lifted in a future feature.")

    versions = job_flight_plan.get("_versions", [])
    current_version = len(versions) + 1
    new_version = current_version + 1

    new_plan_dict = new_plan.model_dump()
    new_plan_dict["_versions"] = versions + [job_flight_plan]
    new_plan_dict["_version"] = new_version
    new_plan_dict["_approval"] = "pending"

    write_plan_md(
        new_plan, evidence_dir, version=new_version,
        transformations=transformations)
    return new_plan_dict, new_version
