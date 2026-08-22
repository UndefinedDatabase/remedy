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
from packages.orchestration.prompt_facts import repo_facts_block
from packages.orchestration.prompt_segments import (
    ComposedPrompt,
    PromptSegmentRegistry,
    SegmentStabilityRank,
    compose_prompt_segments,
)
from packages.orchestration.prompt_trace import build_trace_entry
from packages.orchestration.schemas.models import (
    _LARGE_PLAN_THRESHOLD,
    FlightPlan,
    FlightPlanClarification,
)
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


#: Rank-0 SYSTEM segment: what the provider is being asked to do. It never
#: varies, so it composes first and the cacheable prefix starts at byte 0.
_PLAN_SYSTEM_SEGMENT = """\
You are a project planner. Given the intake and repo facts below, produce
a flight plan: a DAG of tasks with goals, acceptance criteria, dependencies,
and token band estimates."""

#: Rank-4 TASK segment, the volatile one: the intake JSON is different on every
#: call, so it composes after everything stable.
_PLAN_INTAKE_TEMPLATE = """\
## Intake
{intake_json}"""

#: Rank-2 DOSSIER segment: the SHARED repo-facts block. Stable while the repo
#: is, which is longer than one call and shorter than the conventions.
_PLAN_REPO_FACTS_TEMPLATE = """\
## Repo Facts
{repo_facts}"""

#: Rank-1 CONVENTIONS segment: these bytes carry NO caller-varied parameter, so
#: they are byte-identical across every planner call and the cacheable prefix
#: runs to the end of them. A plain constant — never `.format`ted, no braces.
_PLAN_RULES_SEGMENT = """\
## Rules
- Each task needs a unique id (e.g. "T001", "T002").
- depends_on lists task ids that must complete first.
- est_tokens_band is one of: S, M, L, XL.
- acceptance must have at least one non-empty criterion per task.
- No cycles in dependencies.
- Maximum 25 tasks.
- RESOLVE the intake's clarifications into plan choices wherever the
  intake, the repo facts, or ordinary engineering judgement settle them.
  Record each one you resolved in clarifications_resolved with your
  chosen answer — that is an assumption you are declaring, not a
  question. The target for a routine mission is zero questions left.
- Carry forward ONLY genuinely ambiguous questions: ones whose answer
  changes the plan and that you cannot settle from the material given.
  Leave those with an empty answer; a human resolves them once, at the
  plan-approval gate, and they are never asked again during the run.
- Every clarification needs a conservative default_answer and an impact
  line. A default keeps existing behavior or does nothing; it never
  deletes, overwrites, migrates, or otherwise takes a destructive path.
  If the safe choice is "change nothing", that is the default."""

#: Rank-5 STEERING segment. Its TRAILING NEWLINE is load bearing: the
#: pre-migration template ended with one and `compose_prompt_segments` adds
#: none, so dropping it is a one-byte CONTENT change, not a formatting nit.
_PLAN_SCHEMA_DIRECTIVE_SEGMENT = """\
Return ONLY a JSON object matching the flight_plan_v1 schema.
"""

# The conservative-defaults rule this prompt encodes, stated verbatim as
# the feature specifies it (T1_F034, Edge cases & assumption defaults):
#
#   Defaults must be conservative: the planner prompt mandates keep/no-op
#   style defaults with impact text; a fixture asserts a keep-style
#   default survives the round trip. Remedy never defaults to destructive
#   choices — humans can, explicitly.


# Rank order puts the never-changing system line and the rules block AHEAD of
# the repo facts and the intake, so the cacheable prefix runs to the end of the
# rules instead of stopping at the first intake character (F105 T003 site 3).
# The segment BYTES are unchanged from the pre-migration template — only their
# ORDER differs, which is the "modulo ordering" content-equality F105 requires.
def compose_flight_plan_prompt(
    intake_dict: dict[str, Any], *, project_facts: str = "",
) -> ComposedPrompt:
    """Compose the flight-plan prompt from registered segments, with its manifest."""
    registry = PromptSegmentRegistry()
    registry.register(
        "plan_system", SegmentStabilityRank.SYSTEM, _PLAN_SYSTEM_SEGMENT
    )
    registry.register(
        "plan_intake",
        SegmentStabilityRank.TASK,
        _PLAN_INTAKE_TEMPLATE.format(intake_json=json.dumps(intake_dict, indent=2)),
    )
    registry.register(
        "plan_repo_facts",
        SegmentStabilityRank.DOSSIER,
        _PLAN_REPO_FACTS_TEMPLATE.format(
            repo_facts=project_facts or repo_facts_block()),
    )
    registry.register(
        "plan_rules", SegmentStabilityRank.CONVENTIONS, _PLAN_RULES_SEGMENT
    )
    registry.register(
        "plan_schema_directive",
        SegmentStabilityRank.STEERING,
        _PLAN_SCHEMA_DIRECTIVE_SEGMENT,
    )
    return compose_prompt_segments(registry.registered_segments())


def _build_plan_prompt(intake_dict: dict[str, Any], *,
                       project_facts: str = "") -> str:
    """The provider prompt for one job intake.

    ``project_facts`` defaults to the SHARED repo-facts block — the same one
    the mission compiler puts in front of its provider. A caller that already
    knows the project's shape passes it instead of paying for a second listing,
    and a test passes it to keep the rendered prompt independent of the working
    directory.
    """
    return compose_flight_plan_prompt(intake_dict, project_facts=project_facts).text


# The recorder lives beside the composer, in this module, so the manifest and
# the prompt it describes cannot drift apart: whoever changes flight-plan
# composition sees the evidence writer in the same file (F105 T003 site 5, the
# same reason `make_intake_call_recorder` sits in `intake.py`).
def make_flight_plan_call_recorder(
    traces: list[Any],
    composed: ComposedPrompt,
    *,
    provider: str = "",
    provider_kind: str = "",
) -> Callable[[int, str, bool, str], None]:
    """Build the ``on_call`` recorder ``plan_job_llm`` expects.

    Every provider invocation appends one prompt trace entry to ``traces``,
    carrying ``composed``'s segment manifest so call evidence records which
    named segments produced the prompt.

    The role is ``flight_plan``, deliberately NOT ``planner``: the ``planner``
    traces belong to the OTHER planner path
    (``packages/orchestration/structured_planner.py`` over ``PlannerPlan``), and
    one spelling per concept is what keeps a per-role cache report from summing
    two different prompts into one row.
    """
    def _record(
        attempt: int, schema_v: str, is_parse_retry: bool, effective_prompt: str,
    ) -> None:
        kind = "flight-plan-retry" if is_parse_retry else "flight-plan"
        traces.append(build_trace_entry(
            prompt_text=effective_prompt,
            role="flight_plan",
            provider=provider,
            provider_kind=provider_kind,
            prompt_kind=kind,
            schema_v=schema_v,
            phase=kind,
            transport_attempt=attempt,
            is_transport_retry=False,
            composed_prompt=composed,
        ))

    return _record


# ---------------------------------------------------------------------------
# F034 — bundled clarification (plan-time, never at runtime)
# ---------------------------------------------------------------------------

def _as_record(clarification: Any) -> dict[str, Any] | None:
    """Normalize a clarification to a plain dict.

    Callers hand us either the model (fresh plan) or the stored dict
    (job JSON), and both must read the same way.
    """
    if isinstance(clarification, dict):
        return clarification
    dump = getattr(clarification, "model_dump", None)
    if callable(dump):
        return dump()
    return None


def carry_intake_clarifications(
    plan: FlightPlan,
    intake: dict[str, Any] | None,
) -> FlightPlan:
    """Carry the intake's open questions into ``clarifications_resolved``.

    Every intake clarification becomes an UNANSWERED entry (empty
    ``answer``/``answered_by``) with a stable id assigned by intake order
    (``q1``, ``q2``, …) — those are the questions the single approval
    decision bundles. Entries the planner produced on its own (a question
    it already resolved, i.e. an A9 assumption) are preserved verbatim
    after them and get the next free id.

    A plan whose intake has no clarifications and whose planner declared
    none is returned unchanged.
    """
    carried: list[FlightPlanClarification] = []
    intake_clarifications = list((intake or {}).get("clarifications") or [])
    from_intake: set[str] = set()

    for raw in intake_clarifications:
        if not isinstance(raw, dict):
            continue
        question = str(raw.get("question", ""))
        carried.append(FlightPlanClarification(
            id=f"q{len(carried) + 1}",
            question=question,
            default_answer=str(raw.get("default_answer", "")),
            impact=str(raw.get("impact", "")),
            answer="",
            answered_by="",
        ))
        from_intake.add(question)

    for c in plan.clarifications_resolved:
        # The planner echoing an intake question back does not close it —
        # the intake entry above is authoritative and stays open.
        if c.question in from_intake:
            continue
        carried.append(c.model_copy(
            update={"id": c.id or f"q{len(carried) + 1}"}))

    if carried == list(plan.clarifications_resolved):
        return plan
    return plan.model_copy(update={"clarifications_resolved": carried})


def open_clarification_questions(
    clarifications: list[Any] | None,
) -> list[dict[str, str]]:
    """Return the still-open questions as decision-payload records.

    Accepts the raw ``clarifications_resolved`` list from either a plan
    model or a stored flight-plan dict. Open means: no answer AND no
    ``answered_by`` — a planner-declared assumption arrives with an answer
    and is therefore never asked again.
    """
    out: list[dict[str, str]] = []
    for c in clarifications or []:
        rec = _as_record(c)
        if rec is None:
            continue
        if str(rec.get("answer", "") or "").strip():
            continue
        if str(rec.get("answered_by", "") or "").strip():
            continue
        out.append({
            "id": str(rec.get("id", "") or ""),
            "question": str(rec.get("question", "") or ""),
            "default_answer": str(rec.get("default_answer", "") or ""),
            "impact": str(rec.get("impact", "") or ""),
        })
    return out


def clarifications_already_resolved(clarifications: list[Any] | None) -> bool:
    """True once the approval gate has written answers back.

    ``answered_by`` is the marker: it is empty on every unresolved record
    and on planner assumptions, and non-empty only after resolution.
    """
    for c in clarifications or []:
        rec = _as_record(c)
        if rec and str(rec.get("answered_by", "") or "").strip():
            return True
    return False


def apply_clarification_answers(
    clarifications: list[Any] | None,
    answers: dict[str, str] | None,
) -> list[dict[str, Any]]:
    """Resolve every open question: supplied answer, else its default.

    Returns a NEW record list — the caller's records are not mutated. An
    answered question gets ``answered_by="human"``; an unanswered one runs
    on its documented default with ``answered_by="default"``, which is
    what makes an unattended run auditable rather than silent. Planner
    assumptions (already answered, ``answered_by`` empty) are left
    untouched, and so is anything already resolved.
    """
    supplied = answers or {}
    out: list[dict[str, Any]] = []
    for c in clarifications or []:
        rec = _as_record(c)
        if rec is None:
            continue
        rec = dict(rec)
        is_open = (not str(rec.get("answer", "") or "").strip()
                   and not str(rec.get("answered_by", "") or "").strip())
        if is_open:
            qid = str(rec.get("id", "") or "")
            if qid in supplied:
                rec["answer"] = supplied[qid]
                rec["answered_by"] = "human"
            else:
                rec["answer"] = str(rec.get("default_answer", "") or "")
                rec["answered_by"] = "default"
        out.append(rec)
    return out


#: How a clarification's answer came to be, for the audit log.
_SOURCE_HUMAN = "human"
_SOURCE_DEFAULT = "default"
_SOURCE_PLANNER = "planner"
_SOURCE_OPEN = "unresolved"


def clarification_source(clarification: Any) -> str:
    """Classify where a clarification's answer came from.

    ``human``/``default`` are written by the approval gate. An answer with
    no ``answered_by`` is a planner-declared A9 assumption — the planner
    resolved the question itself instead of spending a human touchpoint on
    it. Anything still empty is ``unresolved``.
    """
    rec = _as_record(clarification) or {}
    answered_by = str(rec.get("answered_by", "") or "").strip()
    if answered_by in (_SOURCE_HUMAN, _SOURCE_DEFAULT):
        return answered_by
    if str(rec.get("answer", "") or "").strip():
        return _SOURCE_PLANNER
    return _SOURCE_OPEN


def _cell(text: Any) -> str:
    """Make a value safe for a markdown table cell."""
    return " ".join(str(text or "").split()).replace("|", "\\|") or "-"


def render_assumptions_md(clarifications: list[Any] | None) -> str:
    """Render the assumption log: what was assumed, and on whose authority.

    One row per question — question → chosen answer → source → impact —
    covering human answers, documented defaults, and planner-declared A9
    assumptions alike. This is the artifact a reviewer reads to see what
    an unattended run decided on its own.
    """
    records = [r for r in (_as_record(c) for c in clarifications or [])
               if r is not None]

    lines = ["# Assumptions", ""]
    lines.append(
        "Every question below was asked once, at plan time, on the single "
        "plan-approval decision. Nothing here was asked mid-run.")
    lines.append("")

    if not records:
        lines.append("No clarifications — the plan required no assumptions.")
        lines.append("")
        return "\n".join(lines)

    lines.append("| ID | Question | Answer | Source | Impact |")
    lines.append("| --- | --- | --- | --- | --- |")
    for rec in records:
        lines.append(
            f"| {_cell(rec.get('id'))} | {_cell(rec.get('question'))} "
            f"| {_cell(rec.get('answer'))} | {clarification_source(rec)} "
            f"| {_cell(rec.get('impact'))} |")
    lines.append("")

    counts = {src: sum(1 for r in records if clarification_source(r) == src)
              for src in (_SOURCE_HUMAN, _SOURCE_DEFAULT, _SOURCE_PLANNER,
                          _SOURCE_OPEN)}
    lines.append(
        f"Sources: {counts[_SOURCE_HUMAN]} human, "
        f"{counts[_SOURCE_DEFAULT]} default, "
        f"{counts[_SOURCE_PLANNER]} planner, "
        f"{counts[_SOURCE_OPEN]} unresolved.")
    lines.append("")
    return "\n".join(lines)


def write_assumptions_md(
    clarifications: list[Any] | None,
    evidence_dir: Path,
) -> Path:
    """Write the assumption log into the job's evidence area."""
    evidence_dir.mkdir(parents=True, exist_ok=True)
    path = evidence_dir / "assumptions.md"
    path.write_text(render_assumptions_md(clarifications), encoding="utf-8")
    return path


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
    composed: ComposedPrompt | None = None,
) -> FlightPlanResult:
    """Generate a FlightPlan from a job's intake via LLM.

    Uses run_structured_call for schema validation + one parse retry.
    Returns a FlightPlanResult; on failure, plan is None and error_hint
    describes the failure class.

    ``composed`` lets a caller that ALREADY composed this prompt — the CLI, for
    its trace manifest — hand those exact bytes over, so one composition feeds
    both the provider and the evidence row (R-0256). Omitted, this function
    composes for itself as it always has. The composition deliberately stays
    ABOVE the ``try``: moving it inside is R-0262, which needs this function
    and the CLI's call sites in one round and is NOT fixed here.

    The validated plan then passes through F016 task-granularity
    normalization — the single insertion point for it — and the result
    carries the transformation record. Finally the intake's open questions
    are carried into the plan (F034) so the approval gate can bundle them.
    """
    prompt = composed.text if composed is not None else _build_plan_prompt(intake)
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

    # F034: after normalization, so the questions ride the final plan shape.
    plan = carry_intake_clarifications(plan, intake)

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
        lines.append(
            "Full audit log with sources: [assumptions.md](assumptions.md)")
        lines.append("")
        for c in plan.clarifications_resolved:
            lines.append(f"**Q:** [{c.id or '-'}] {c.question}")
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


#: What ``_approval_audit.mode`` records for an unattended approval. One
#: spelling, so a reader of a persisted job can tell an audited auto-approval
#: from a human one without knowing which caller wrote it.
AUTO_APPROVAL_MODE = "auto_yes"

#: The audit reason that accompanies it.
AUTO_APPROVAL_REASON = "auto-approved via --yes"


def auto_approve_flight_plan(
    flight_plan_body: dict[str, Any],
    evidence_dir: Path,
    *,
    reason: str = AUTO_APPROVAL_REASON,
) -> dict[str, Any]:
    """Apply the unattended approval to a flight-plan body. Audited, never silent.

    THE ``--yes`` semantics, in one place (F034): every open clarification runs
    on its documented default, the approval is stamped with an audit record
    naming the mode, and the assumption log is written to the job's evidence
    area. Unattended is not the same as undocumented — a reader of that log can
    see every question that was answered without a human.

    Returns a NEW body; the caller persists it. Writing the job is deliberately
    NOT done here, because the two callers (``remedy do --yes`` and the
    orchestrator loop) own their own persistence and their own ledger entries.
    """
    body = dict(flight_plan_body)
    if body.get("clarifications_resolved"):
        body["clarifications_resolved"] = apply_clarification_answers(
            body.get("clarifications_resolved"), None)
    body["_approval"] = "approved"
    body["_approval_audit"] = {"mode": AUTO_APPROVAL_MODE, "reason": reason}
    write_assumptions_md(body.get("clarifications_resolved"), evidence_dir)
    return body


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


def resolve_flight_plan_approval(
    job: Any,
    *,
    reason: str,
    answers: dict[str, str],
    questions: list[dict[str, Any]],
) -> Path | None:
    """Approve or reject a job's pending flight plan and persist the outcome.

    Extracted from `apps/cli/commands/decision.py` for DECISION F009 D5, so the UI
    write door can reach the SAME code the CLI has always run instead of growing a
    second copy of the approval sequence beside it — the duplication the P3 contract
    exists to prevent. The CLI stays the first caller and keeps every `print`: this
    function performs the mutation, the save and the assumption log, and hands the
    log path back for the caller to report.

    The caller validates `reason` and the plan's pending state before calling,
    because the CLI and the write door word their refusals differently and neither
    wording belongs in a package. Any `reason` other than `"approve"` rejects, which
    is the branch the extracted code already had.

    Returns the assumption-log path on an approval and None on a rejection.
    """
    from packages.orchestration.storage import save_job

    fp = job.flight_plan
    if reason != "approve":
        fp["_approval"] = "rejected"
        job.flight_plan = fp
        save_job(job)
        return None
    if questions:
        fp["clarifications_resolved"] = apply_clarification_answers(
            fp.get("clarifications_resolved"), answers)
    fp["_approval"] = "approved"
    job.flight_plan = fp
    save_job(job)
    from packages.orchestration.data_paths import job_evidence_export_dir
    return write_assumptions_md(
        fp.get("clarifications_resolved"),
        job_evidence_export_dir(str(job.id)))
