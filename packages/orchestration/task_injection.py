"""F028 T001 — the draft pass of a task injection (DECISION F028 D1).

A running job's record is written only by its own runner, at its own safe
points (DECISION F026 D1): a command that wrote ``job.json`` directly while a
job runs would simply be overwritten at the runner's next save. An injection
therefore reaches a running job as a create-only control file the runner
folds in at its own pace — never as a write of ``job.json`` itself.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from decimal import ROUND_CEILING, Decimal
from pathlib import Path
from typing import Any, ClassVar, Literal

from pydantic import Field, ValidationError, model_validator

from packages.common import secure_fs as _fs
from packages.orchestration import budget_guard, plan_editing
from packages.orchestration import safe_points as _sp
from packages.orchestration.data_paths import job_dod_path
from packages.orchestration.job_plan import (
    APPROVED_PLAN_HASH_KEY,
    map_task_plan_to_tasks,
    plan_content_hash,
)
from packages.orchestration.mission_compiler import PLAN_VERSION_KEY
from packages.orchestration.pingpong_job import job_is_terminal
from packages.orchestration.schemas.models import _MAX_TASK_PLAN_TASKS as MAX_PLAN_TASKS
from packages.orchestration.schemas.models import (
    TASK_PLAN_SCHEMA_V,
    PlannedTask,
    TaskPlan,
)
from packages.orchestration.schemas.models import TokenBand as PlanTokenBand
from packages.orchestration.stream_evidence import redact_text
from packages.orchestration.structured_base import _Structured
from packages.orchestration.structured_outputs import run_structured_call
from packages.orchestration.task_deliverables import record_llm_task_deliverables
from packages.orchestration.task_veto import _bounded_actor
from packages.orchestration.token_economy import TokenBand

__all__ = [
    "TaskInjectionRefused",
    "TaskInjectionError",
    "InjectedTaskDraft",
    "INJECTION_DRAFT_SCHEMA_V",
    "INJECTION_DRAFTS_DIRNAME",
    "INJECTION_DRAFT_TTL_SECONDS",
    "MAX_INJECTION_TEXT_CHARS",
    "INJECTED_TASK_ID_PREFIX",
    "MAX_PLAN_TASKS",
    "PLACEMENT_STATED",
    "PLACEMENT_CONTENT_OVERLAP",
    "PLACEMENT_FRONTIER_DEFAULT",
    "SHORTFALL_OPTIONS",
    "PLAN_BAND_TO_TOKEN_BAND",
    "ORIGIN_HUMAN_INJECTED",
    "INJECTED_TASKS_DIRNAME",
    "INJECTION_ANSWERS_DIRNAME",
    "validate_injection_text",
    "injection_refusal",
    "next_injected_task_id",
    "place_injected_task",
    "injection_budget_check",
    "shortfall_decision_seed",
    "injection_budget_inputs",
    "injection_call_fn",
    "fence_conflicts",
    "compose_injection_prompt",
    "draft_task_injection",
    "read_injection_draft",
    "confirmed_injections",
    "confirm_task_injection",
    "apply_injection_to_job",
    "answer_injection_shortfall",
]

# ---------------------------------------------------------------------------
# S1 — constants
# ---------------------------------------------------------------------------

INJECTION_DRAFT_SCHEMA_V = "task_injection_draft_v1"
INJECTION_DRAFTS_DIRNAME = "injection_drafts"
INJECTION_DRAFT_TTL_SECONDS = 900
MAX_INJECTION_TEXT_CHARS = 2000
INJECTED_TASK_ID_PREFIX = "INJ"

PLACEMENT_STATED = "stated"
PLACEMENT_CONTENT_OVERLAP = "content_overlap"
PLACEMENT_FRONTIER_DEFAULT = "frontier_default"

SHORTFALL_OPTIONS = ("extend_budget", "shrink_task", "drop")

#: DECISION F028 D2 (4) — the provenance an injected task's plan inputs carry, distinguishing
#: it from a task the planner produced.
ORIGIN_HUMAN_INJECTED = "human_injected"

#: DECISION F028 D2 (2) — the confirmed-injection control files, beside `INJECTION_DRAFTS_DIRNAME`
#: under the same job control directory.
INJECTED_TASKS_DIRNAME = "injected_tasks"

#: DECISION F028 D3 (1) — a shortfall draft's answer, beside the other two control
#: directories, under the same job control directory.
INJECTION_ANSWERS_DIRNAME = "injection_answers"

#: F028 D1 (7) — a plan band maps onto the predictive engine's token band; XL has no
#: class default of its own and takes the "missing band" path deliberately (A9).
PLAN_BAND_TO_TOKEN_BAND: dict[str, str] = {
    "S": TokenBand.LOW,
    "M": TokenBand.MEDIUM,
    "L": TokenBand.HIGH,
    "XL": TokenBand.UNKNOWN,
}

#: The next smaller plan band a shortfall's seed offers to shrink into; None for "S",
#: which cannot shrink any further.
_SHRINK_BAND: dict[str, str | None] = {"XL": "L", "L": "M", "M": "S", "S": None}

_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


class TaskInjectionRefused(Exception):
    """A refusal an operator can act on: a bad text, or the gate. Carries ``code`` and
    ``detail`` rather than a bare message, so a caller can render either without parsing text.
    """

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail


class TaskInjectionError(RuntimeError):
    """The injection control area could not be used, or an on-disk entry could not be trusted.

    Loud on purpose, same as ``task_veto.TaskVetoError``: a silently dropped or mistrusted
    draft entry could let a stale or tampered injection be confirmed.
    """


# ---------------------------------------------------------------------------
# S2 — the draft model
# ---------------------------------------------------------------------------


class InjectedTaskDraft(_Structured):
    """One planner-drafted task from an operator's injected text (F028 T001).

    Deliberately NOT entered in ``SCHEMA_REGISTRY``: it never leaves the one
    structured call ``draft_task_injection`` makes, the same reason the DoD's own
    provider-facing draft contract is not registered either.
    """

    SCHEMA_V: ClassVar[str] = INJECTION_DRAFT_SCHEMA_V
    schema_v: Literal["task_injection_draft_v1"]  # required: no default
    title: str
    goal: str
    acceptance: list[str] = Field(min_length=1)
    est_tokens_band: PlanTokenBand
    files_hint: list[str] = Field(default_factory=list)
    rationale: str

    @model_validator(mode="after")
    def _validate_non_blank(self) -> InjectedTaskDraft:
        if not self.title.strip():
            raise ValueError("InjectedTaskDraft.title must not be blank")
        if not self.goal.strip():
            raise ValueError("InjectedTaskDraft.goal must not be blank")
        for i, entry in enumerate(self.acceptance):
            if not entry.strip():
                raise ValueError(f"InjectedTaskDraft.acceptance[{i}] must not be blank")
        return self


# ---------------------------------------------------------------------------
# S3 — the text, kept verbatim
# ---------------------------------------------------------------------------


def validate_injection_text(text: Any) -> str:
    """Refuse, or return ``text`` UNCHANGED — never stripped, bounded or redacted.

    In order: not a string, or blank after ``.strip()``, is ``text_required``; longer than
    ``MAX_INJECTION_TEXT_CHARS`` is ``text_too_long``; holding a character of
    ``[\\x00-\\x08\\x0b-\\x1f\\x7f]``, or differing from ``redact_text``'s reading of it, is
    ``text_invalid``. Newline (``\\n``) and tab (``\\t``) pass.
    """
    if not isinstance(text, str) or not text.strip():
        raise TaskInjectionRefused(
            "text_required",
            "an injected task's text is required and must not be empty or blank")
    if len(text) > MAX_INJECTION_TEXT_CHARS:
        raise TaskInjectionRefused(
            "text_too_long",
            f"an injected task's text is at most {MAX_INJECTION_TEXT_CHARS} characters")
    if _CONTROL_CHAR_RE.search(text) or redact_text(text) != text:
        raise TaskInjectionRefused(
            "text_invalid",
            "an injected task's text holding a control character or secret-shaped text is "
            "refused rather than stored altered")
    return text


# ---------------------------------------------------------------------------
# S4 — the gate and the id, pure
# ---------------------------------------------------------------------------


def _state_str(value: Any) -> str:
    """A ``RunState`` or a plain string, read as its bare string value either way."""
    return value.value if hasattr(value, "value") else str(value)


def injection_refusal(job_state: Any, plan_task_count: int) -> TaskInjectionRefused | None:
    """Pure, no I/O. None when ``job_state``/``plan_task_count`` admit an injection.

    A terminal job (``pingpong_job.job_is_terminal``) is refused ``job_terminal`` and told to
    start a follow-up job instead; a plan already at ``MAX_PLAN_TASKS`` is ``plan_full``.
    """
    if job_is_terminal(job_state):
        state = _state_str(job_state)
        return TaskInjectionRefused(
            "job_terminal",
            f"the job is {state!r}; start a follow-up job for this work instead")
    if plan_task_count >= MAX_PLAN_TASKS:
        return TaskInjectionRefused(
            "plan_full", f"the plan is already at its {MAX_PLAN_TASKS}-task cap")
    return None


def next_injected_task_id(existing_ids: Any) -> str:
    """The smallest ``INJ<k>``, ``k`` from 1, not already an id of ``existing_ids``."""
    existing = set(existing_ids)
    k = 1
    while True:
        candidate = f"{INJECTED_TASK_ID_PREFIX}{k}"
        if candidate not in existing:
            return candidate
        k += 1


# ---------------------------------------------------------------------------
# S5 — the placement, pure
# ---------------------------------------------------------------------------


def _norm_path(path: str) -> str:
    """Surrounding whitespace and one leading ``./`` are dropped before comparison."""
    cleaned = path.strip()
    if cleaned.startswith("./"):
        cleaned = cleaned[2:]
    return cleaned


def place_injected_task(plan_tasks: Any, files_hint: Any, *,
                        after: str | None = None) -> dict[str, Any]:
    """Where a new task lands: always at the END of the plan, over a list of ``PlannedTask``.

    In order: ``after`` not None and not an id of ``plan_tasks`` raises
    ``TaskInjectionRefused("unknown_task", ...)``; ``after`` given and known is
    ``depends_on=[after]``, basis ``stated``; otherwise every plan task sharing a path with
    ``files_hint``, in plan order, is basis ``content_overlap``; otherwise ``depends_on=[]``,
    basis ``frontier_default``.
    """
    tasks = list(plan_tasks)
    ids = [t.id for t in tasks]
    position = len(tasks)

    if after is not None:
        if after not in ids:
            listing = ", ".join(ids[:10])
            if len(ids) > 10:
                listing += f" and {len(ids) - 10} more"
            raise TaskInjectionRefused(
                "unknown_task",
                f"there is no task {after!r} in this job's plan; its tasks are: {listing}")
        return {
            "depends_on": [after],
            "basis": PLACEMENT_STATED,
            "position": position,
            "rationale": f"placed after {after} because you named it",
        }

    hint_paths = {_norm_path(p) for p in files_hint}
    overlap_ids: list[str] = []
    overlap_paths: set[str] = set()
    for task in tasks:
        task_paths = {_norm_path(p) for p in (task.files_hint or [])}
        shared = task_paths & hint_paths
        if shared:
            overlap_ids.append(task.id)
            overlap_paths |= shared

    if overlap_ids:
        return {
            "depends_on": list(overlap_ids),
            "basis": PLACEMENT_CONTENT_OVERLAP,
            "position": position,
            "rationale": (
                f"placed after {', '.join(overlap_ids)} because they touch the same files: "
                f"{', '.join(sorted(overlap_paths))}"),
        }

    return {
        "depends_on": [],
        "basis": PLACEMENT_FRONTIER_DEFAULT,
        "position": position,
        "rationale": (
            "placed at the end of the plan with no dependency, because no planned task "
            "touches its files"),
    }


# ---------------------------------------------------------------------------
# S6 — the budget check and the shortfall seed
# ---------------------------------------------------------------------------


def injection_budget_check(budgets: Any, counters: Any, *, band: str, config: Any
                           ) -> dict[str, Any]:
    """``budget_guard.predict_next_task_cost`` over the draft's plan band (F104 D1 (7))."""
    prediction = budget_guard.predict_next_task_cost(
        budgets, counters, band=PLAN_BAND_TO_TOKEN_BAND[band], config=config)
    result = prediction.to_json()
    result["plan_band"] = band
    result["shortfall"] = prediction.would_breach
    return result


def shortfall_decision_seed(check: dict[str, Any]) -> dict[str, Any]:
    """The three-option menu a shortfall answers with, keyed by option (DECISION F028 D3 (3)):
    ``option_labels`` is a ``dict`` of complete sentences, the same shape ``veto_proposal``'s
    seed uses, not the list DECISION F028 D1 (8) originally answered."""
    plan_band = check["plan_band"]
    shrink_band = _SHRINK_BAND.get(plan_band)

    spent = check.get("spent_cost_usd")
    expected = check.get("expected_cost_usd")
    extend_to_usd: float | None = None
    if spent is not None and expected is not None:
        extend_to_usd = float(
            Decimal(repr(round(spent + expected, 6))).quantize(
                Decimal("0.01"), rounding=ROUND_CEILING))

    if shrink_band is None:
        shrink_label = "The task is already the smallest size, so it cannot shrink."
    else:
        shrink_label = (
            f"Draft the task again one size smaller, as size {shrink_band}, and check "
            f"the cost again.")
    option_labels = {
        "extend_budget": f"Raise the job's cost limit to ${extend_to_usd:.2f} and add the task.",
        "shrink_task": shrink_label,
        "drop": "Drop this task and add nothing to the job.",
    }
    return {
        "question": "Adding this task would go over the job's cost limit. What should happen?",
        "options": list(SHORTFALL_OPTIONS),
        "option_labels": option_labels,
        "arithmetic": check["arithmetic"],
        "extend_to_usd": extend_to_usd,
        "shrink_band": shrink_band,
    }


# ---------------------------------------------------------------------------
# DECISION F028 D4 (3) — the shared budget and planner inputs: the CLI's `job inject`
# and round 5's browser command read a job's budget state and its planner call_fn
# through these two, so the two doors can never disagree about either.
# ---------------------------------------------------------------------------


def injection_budget_inputs(job: Any) -> tuple[Any, Any, Any]:
    """``(budgets, counters, config)`` for a job about to draft or answer an injection.

    ``budgets`` is None when ``job.budgets`` is None, else ``JobBudgets.model_validate(
    job.budgets)``; ``counters`` is ``BudgetCounters()`` when ``job.budget_actuals`` is
    None, else decoded and built from it; ``config`` is the repo's predictive budget
    config. A pydantic ``ValidationError``, a ``budget_guard.BudgetCounterError``, a
    ``ValueError`` or a ``TypeError`` raised while reading the budgets or the counters
    raises ``TaskInjectionRefused("budget_unreadable", ...)`` instead — a job whose stored
    state cannot be trusted must never be read as a job that has spent nothing.
    """
    from packages.core.models import JobBudgets
    from packages.orchestration.budget_resolution import resolve_predictive_budget_config

    try:
        budgets = None if job.budgets is None else JobBudgets.model_validate(job.budgets)
        if job.budget_actuals is None:
            counters = budget_guard.BudgetCounters()
        else:
            validated = budget_guard.decode_persisted_budget_actuals(
                job.budget_actuals, first_running_at=job.first_running_at or None)
            counters = budget_guard.counters_from_persisted(validated)
    except (ValidationError, budget_guard.BudgetCounterError, ValueError, TypeError) as exc:
        raise TaskInjectionRefused(
            "budget_unreadable", f"this job's budget state cannot be read: {exc}") from exc

    config = resolve_predictive_budget_config(project_root=job.repo_path or None)
    return budgets, counters, config


def injection_call_fn() -> Callable[[str, int], str] | None:
    """The one planner call an injection draft or a derived draft makes: ``intake
    .make_structured_call_fn(InjectedTaskDraft)``. DECISION F028 D4 (3): the CLI and
    round 5's browser command share this so both name the operator's configured
    planner identically, never two independently-resolved calls that could disagree.
    """
    from packages.orchestration import intake

    return intake.make_structured_call_fn(InjectedTaskDraft)


# ---------------------------------------------------------------------------
# S7 — the fences and the prompt
# ---------------------------------------------------------------------------


def fence_conflicts(files_hint: Any, fences: Any) -> list[dict[str, Any]]:
    """Every ``files_hint`` path that breaks a job's fences, in ``files_hint`` order.

    A path meeting a deny glob is flagged with it; a path meeting no allow glob when the job
    declares some is flagged ``not_allowed``; a path meeting neither is not flagged at all. A
    flag never refuses — S8 stores it beside the draft for a human to see.
    """
    if fences is None:
        return []
    deny_globs = list(getattr(fences, "deny", None) or [])
    allow_globs = list(getattr(fences, "allow", None) or [])
    conflicts: list[dict[str, Any]] = []
    for path in files_hint:
        deny_glob = next((glob for glob in deny_globs if fnmatch.fnmatch(path, glob)), None)
        if deny_glob is not None:
            conflicts.append({"path": path, "rule": "deny", "glob": deny_glob})
            continue
        if allow_globs and not any(fnmatch.fnmatch(path, glob) for glob in allow_globs):
            conflicts.append({"path": path, "rule": "not_allowed", "glob": ""})
    return conflicts


def compose_injection_prompt(text: str, plan_tasks: Any, *, after: str | None = None) -> str:
    """The one prompt the planner drafts a task from: the operator's text verbatim, every
    plan task's id/title/files_hint, the stated ``after`` when given, and instructions to
    phrase acceptance criteria as checks a test can make, choose ``est_tokens_band`` and
    name the files the task will touch.
    """
    lines = [
        "An operator asked to inject a new task into this running job's plan.",
        "",
        "The operator's task text, verbatim:",
        text,
        "",
        "The plan's existing tasks:",
    ]
    for task in plan_tasks:
        files = ", ".join(task.files_hint) if task.files_hint else "(none)"
        lines.append(f"- {task.id}: {task.title} (files_hint: {files})")
    if after is not None:
        lines.append("")
        lines.append(f"The operator asked for this task to be placed after {after!r}.")
    lines.append("")
    lines.append(
        "Phrase each acceptance criterion as a check a test can make. Choose "
        "est_tokens_band from S, M, L or XL. Name the files this task will touch in "
        "files_hint.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# S8 — the draft and its file
# ---------------------------------------------------------------------------


def _draft_filename(draft_id: str) -> str:
    """Named by a digest of the draft id, never by the id itself — mirrors
    ``task_veto._veto_filename`` exactly."""
    digest = hashlib.sha256(draft_id.encode("utf-8")).hexdigest()[:32]
    return f"{digest}.json"


def _open_named_dir(parent_fd: int, name: str, *, create: bool) -> int | None:
    """One verified subdirectory of the job's control directory. Mirrors
    ``task_veto._open_named_dir``, written fresh so this module need not import it."""
    try:
        return _fs.open_verified_dir(name, dir_fd=parent_fd, error_cls=TaskInjectionError,
                                     noun="task-injection-control")
    except _fs.MissingComponent:
        if not create:
            return None
    _fs.require_writable_dir(parent_fd, error_cls=TaskInjectionError,
                             noun="task-injection-control", label=name)
    try:
        os.mkdir(name, _sp.CONTROL_DIR_MODE, dir_fd=parent_fd)
    except FileExistsError:
        pass                                        # a concurrent creator; verify below
    except OSError as exc:
        raise TaskInjectionError(
            f"cannot create the task-injection control directory {name!r} "
            f"({type(exc).__name__}: {exc.strerror or exc})") from exc
    try:
        return _fs.open_verified_dir(name, dir_fd=parent_fd, error_cls=TaskInjectionError,
                                     noun="task-injection-control")
    except _fs.MissingComponent as exc:
        raise TaskInjectionError(
            f"the task-injection control directory {name!r} vanished after creation") from exc


def _publish_injection_draft(job_id: str, draft_id: str, record: dict[str, Any], *,
                             control_root_path: Path | None) -> None:
    jid = _sp.validate_job_id(job_id)
    try:
        job_fd = _sp.open_job_control_fd(jid, control_root_path, create=True)
    except _sp.StopControlError as exc:
        raise TaskInjectionError(str(exc)) from exc
    assert job_fd is not None
    drafts_fd = None
    try:
        drafts_fd = _open_named_dir(job_fd, INJECTION_DRAFTS_DIRNAME, create=True)
        assert drafts_fd is not None
        name = _draft_filename(draft_id)
        published = _fs.write_file_atomically(
            drafts_fd, name, _fs.json_bytes(record), create_only=True,
            file_mode=_sp.CONTROL_FILE_MODE, error_cls=TaskInjectionError,
            noun="task injection draft")
        if not published:
            raise TaskInjectionError(
                f"an injection draft already exists for id {draft_id!r}; a fresh draft id "
                f"collided, which should never happen")
    finally:
        if drafts_fd is not None:
            os.close(drafts_fd)
        os.close(job_fd)


def draft_task_injection(
    job: Any,
    text: Any,
    *,
    call_fn: Callable[[str, int], str] | None,
    budgets: Any,
    counters: Any,
    config: Any,
    actor: Any,
    after: str | None = None,
    now: datetime | None = None,
    control_root_path: Path | None = None,
) -> dict[str, Any]:
    """Draft one injected task from ``text``, or answer a refusal. NEVER raises.

    Checks, in order: S3's text, S4's terminal check, ``job.task_plan`` (``no_task_plan``),
    S4's task-cap check, S5's unknown ``after`` (before any planner call), a missing
    ``call_fn`` (``planner_unavailable``), the one structured call (``draft_unparseable``),
    and the candidate ``TaskPlan`` the drafted task would join (``draft_invalid``). A refusal
    writes nothing.
    """
    try:
        validated_text = validate_injection_text(text)
    except TaskInjectionRefused as exc:
        return {"outcome": "refused", "code": exc.code, "detail": exc.detail}

    job_state = getattr(job, "state", "")
    refusal = injection_refusal(job_state, 0)
    if refusal is not None:
        return {"outcome": "refused", "code": refusal.code, "detail": refusal.detail}

    raw_plan = getattr(job, "task_plan", None)
    plan: TaskPlan | None = None
    if isinstance(raw_plan, dict):
        try:
            plan = TaskPlan.model_validate(
                {k: v for k, v in raw_plan.items() if not k.startswith("_")})
        except ValidationError:
            plan = None
    if plan is None:
        return {"outcome": "refused", "code": "no_task_plan",
                "detail": "this job has no readable task plan to inject into"}

    refusal = injection_refusal(job_state, len(plan.tasks))
    if refusal is not None:
        return {"outcome": "refused", "code": refusal.code, "detail": refusal.detail}

    try:
        place_injected_task(plan.tasks, [], after=after)
    except TaskInjectionRefused as exc:
        return {"outcome": "refused", "code": exc.code, "detail": exc.detail}

    if call_fn is None:
        return {"outcome": "refused", "code": "planner_unavailable",
                "detail": "no planner call is available to draft this task"}

    prompt = compose_injection_prompt(validated_text, plan.tasks, after=after)
    outcome = run_structured_call(InjectedTaskDraft, prompt, call_fn)
    if not outcome.ok:
        return {"outcome": "refused", "code": "draft_unparseable",
                "detail": "the planner's draft reply could not be parsed as a task"}

    draft = outcome.value
    assert isinstance(draft, InjectedTaskDraft)

    placement = place_injected_task(plan.tasks, draft.files_hint, after=after)
    new_id = next_injected_task_id([t.id for t in plan.tasks])
    new_task = PlannedTask(
        id=new_id,
        title=draft.title,
        goal=draft.goal,
        acceptance=list(draft.acceptance),
        depends_on=list(placement["depends_on"]),
        est_tokens_band=draft.est_tokens_band,
        files_hint=list(draft.files_hint),
    )
    try:
        TaskPlan(schema_v=TASK_PLAN_SCHEMA_V, tasks=[*plan.tasks, new_task])
    except ValidationError:
        return {"outcome": "refused", "code": "draft_invalid",
                "detail": "the drafted task cannot be added to this job's plan"}

    check = injection_budget_check(budgets, counters, band=draft.est_tokens_band, config=config)
    shortfall = bool(check["shortfall"])

    now_dt = now if now is not None else datetime.now(timezone.utc)
    expires_dt = now_dt + timedelta(seconds=INJECTION_DRAFT_TTL_SECONDS)
    draft_id = _sp.new_request_id()

    answer: dict[str, Any] = {
        "outcome": "shortfall" if shortfall else "drafted",
        "job_id": job.job_id,
        "draft_id": draft_id,
        "confirm_token": None if shortfall else draft_id,
        "task": new_task.model_dump(),
        "placement": placement,
        "task_rationale": draft.rationale,
        "budget_check": check,
        "decision_seed": shortfall_decision_seed(check) if shortfall else None,
        "fence_conflicts": fence_conflicts(draft.files_hint, getattr(job, "fences", None)),
        "drafted_at": now_dt.isoformat(),
        "expires_at": expires_dt.isoformat(),
        "planner_calls": outcome.calls,
        "text": validated_text,
        # DECISION F028 D3 (2): a drafted-from-scratch task carries no extension; only a
        # `extend_budget` answer's derived draft (S3) sets this to a real number.
        "budget_extend_to_usd": None,
    }

    record = dict(answer)
    record["injection_draft_v"] = 1
    record["status"] = "needs_decision" if shortfall else "confirmable"
    record["actor"] = _bounded_actor(actor)
    record["after"] = after

    _publish_injection_draft(job.job_id, draft_id, record, control_root_path=control_root_path)

    return answer


def read_injection_draft(job_id: str, draft_id: str, *, now: datetime | None = None,
                         control_root_path: Path | None = None) -> dict[str, Any]:
    """The stored draft record, or a refusal. Never deletes a file.

    ``draft_unknown`` when ``draft_id`` fails ``safe_points.is_safe_id`` or no file exists;
    ``draft_expired`` when ``now`` is at or past the record's ``expires_at``. A file that is
    not a JSON object, or whose own ``draft_id`` differs from the one asked for, raises
    ``TaskInjectionError`` — a corrupt or tampered entry is never silently accepted. R-1076's
    repair: a record whose ``expires_at`` is missing, not a string, not parseable by
    ``datetime.fromisoformat`` or parsed without a time zone raises ``TaskInjectionError`` too
    — DECISION F028 D1 (10) makes expiry what renders an unconfirmed draft harmless, so a
    record that cannot prove its own expiry is never read as still live.
    """
    if not _sp.is_safe_id(draft_id):
        raise TaskInjectionRefused("draft_unknown", f"no injection draft {draft_id!r} exists")
    jid = _sp.validate_job_id(job_id)
    try:
        job_fd = _sp.open_job_control_fd(jid, control_root_path, create=False)
    except _sp.StopControlError as exc:
        raise TaskInjectionError(str(exc)) from exc
    if job_fd is None:
        raise TaskInjectionRefused("draft_unknown", f"no injection draft {draft_id!r} exists")

    drafts_fd = None
    try:
        drafts_fd = _open_named_dir(job_fd, INJECTION_DRAFTS_DIRNAME, create=False)
        if drafts_fd is None:
            raise TaskInjectionRefused(
                "draft_unknown", f"no injection draft {draft_id!r} exists")
        name = _draft_filename(draft_id)
        raw = _fs.read_verified_file(name, drafts_fd, max_bytes=_sp.MAX_CONTROL_BYTES,
                                     error_cls=TaskInjectionError, noun="task injection draft")
        if raw is None:
            raise TaskInjectionRefused(
                "draft_unknown", f"no injection draft {draft_id!r} exists")
        try:
            record = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise TaskInjectionError(
                f"the injection draft entry is not valid JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise TaskInjectionError("the injection draft entry is not a JSON object")
        if record.get("draft_id") != draft_id:
            raise TaskInjectionError(
                f"the injection draft entry does not match the requested id {draft_id!r}")
    finally:
        if drafts_fd is not None:
            os.close(drafts_fd)
        os.close(job_fd)

    expires_at = record.get("expires_at")
    if not isinstance(expires_at, str) or not expires_at:
        raise TaskInjectionError(
            f"the injection draft entry for {draft_id!r} carries no readable expiry")
    try:
        expires_dt = datetime.fromisoformat(expires_at)
    except ValueError as exc:
        raise TaskInjectionError(
            f"the injection draft entry for {draft_id!r} carries an unparseable expiry "
            f"{expires_at!r}: {exc}") from exc
    if expires_dt.tzinfo is None:
        raise TaskInjectionError(
            f"the injection draft entry for {draft_id!r} carries an expiry with no time "
            f"zone: {expires_at!r}")

    now_dt = now if now is not None else datetime.now(timezone.utc)
    if now_dt >= expires_dt:
        raise TaskInjectionRefused(
            "draft_expired", f"the injection draft {draft_id!r} expired at {expires_at}")

    return record


# ---------------------------------------------------------------------------
# DECISION F028 D3 (1) — the answer: a create-only file, and (for two of the three
# options) a derived draft published through the same helper a fresh draft uses
# ---------------------------------------------------------------------------


def _read_injection_answer(job_id: str, draft_id: str, *,
                           control_root_path: Path | None) -> dict[str, Any] | None:
    """The stored answer record for *draft_id*, or None when none exists yet. A file that is
    not a JSON object raises ``TaskInjectionError``, same as every other control reader here."""
    jid = _sp.validate_job_id(job_id)
    try:
        job_fd = _sp.open_job_control_fd(jid, control_root_path, create=False)
    except _sp.StopControlError as exc:
        raise TaskInjectionError(str(exc)) from exc
    if job_fd is None:
        return None

    answers_fd = None
    try:
        answers_fd = _open_named_dir(job_fd, INJECTION_ANSWERS_DIRNAME, create=False)
        if answers_fd is None:
            return None
        name = _draft_filename(draft_id)
        raw = _fs.read_verified_file(name, answers_fd, max_bytes=_sp.MAX_CONTROL_BYTES,
                                     error_cls=TaskInjectionError, noun="injection answer")
        if raw is None:
            return None
        try:
            record = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise TaskInjectionError(
                f"an injection answer entry is not valid JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise TaskInjectionError("an injection answer entry is not a JSON object")
        return record
    finally:
        if answers_fd is not None:
            os.close(answers_fd)
        os.close(job_fd)


def _publish_injection_answer(job_id: str, draft_id: str, record: dict[str, Any], *,
                              control_root_path: Path | None) -> bool:
    """Publish one create-only answer file. Mirrors ``_publish_confirmed_injection``: a lost
    race is the caller's ``already_answered`` to answer, not a raised error."""
    jid = _sp.validate_job_id(job_id)
    try:
        job_fd = _sp.open_job_control_fd(jid, control_root_path, create=True)
    except _sp.StopControlError as exc:
        raise TaskInjectionError(str(exc)) from exc
    assert job_fd is not None
    answers_fd = None
    try:
        answers_fd = _open_named_dir(job_fd, INJECTION_ANSWERS_DIRNAME, create=True)
        assert answers_fd is not None
        name = _draft_filename(draft_id)
        return _fs.write_file_atomically(
            answers_fd, name, _fs.json_bytes(record), create_only=True,
            file_mode=_sp.CONTROL_FILE_MODE, error_cls=TaskInjectionError,
            noun="injection answer")
    finally:
        if answers_fd is not None:
            os.close(answers_fd)
        os.close(job_fd)


def answer_injection_shortfall(
    job: Any,
    draft_id: Any,
    option: Any,
    *,
    actor: Any,
    budgets: Any,
    counters: Any,
    config: Any,
    now: datetime | None = None,
    control_root_path: Path | None = None,
) -> dict[str, Any]:
    """Answer a shortfall draft's decision seed with one of ``SHORTFALL_OPTIONS``. NEVER
    raises for a refusal.

    Checks, in order: S4's terminal check (``job_terminal``); ``read_injection_draft``
    refusing with its own code; a record naming another job (``draft_unknown``); a
    ``status`` other than ``needs_decision`` (``draft_not_in_shortfall``); *option* outside
    ``SHORTFALL_OPTIONS`` (``unknown_option``); an answer already on file for this draft
    (``already_answered``); ``shrink_task`` when the stored seed's ``shrink_band`` is None
    (``cannot_shrink``). A refusal writes nothing.

    Otherwise mints a derived draft id (None for ``drop``) and publishes ONE create-only
    answer file in ``INJECTION_ANSWERS_DIRNAME``, named as a draft file is — a lost race there
    answers ``already_answered`` too. Then: ``drop`` answers ``{"outcome": "dropped",
    "job_id", "draft_id", "answered_at"}`` and nothing more is written. ``shrink_task``
    derives a new draft whose task is the old one at the seed's ``shrink_band``, checked again
    over *budgets*/*counters*/*config*, itself a fresh shortfall (``needs_decision``, a fresh
    seed) when that check still breaches. ``extend_budget`` derives a new draft at the old
    band, ``confirmable``, carrying ``budget_extend_to_usd`` equal to the seed's
    ``extend_to_usd``, its check computed over ``budgets`` with ``max_cost_usd`` raised to
    that figure. Either derived draft keeps the old record's task id, placement,
    ``task_rationale``, ``text``, ``after`` and ``fence_conflicts``, takes the new draft id,
    the answering actor, ``drafted_at`` *now* and a fresh ``expires_at``, and adds
    ``derived_from`` (the old draft id) and ``answer`` (*option*); it is published through
    ``_publish_injection_draft`` (round 1's draft helper) and answered in the shape
    ``draft_task_injection`` answers, plus those two keys and ``budget_extend_to_usd``.
    """
    refusal = injection_refusal(getattr(job, "state", ""), 0)
    if refusal is not None:
        return {"outcome": "refused", "code": refusal.code, "detail": refusal.detail}

    try:
        record = read_injection_draft(
            job.job_id, draft_id, now=now, control_root_path=control_root_path)
    except TaskInjectionRefused as exc:
        return {"outcome": "refused", "code": exc.code, "detail": exc.detail}

    if record.get("job_id") != job.job_id:
        return {"outcome": "refused", "code": "draft_unknown",
                "detail": f"no injection draft {draft_id!r} exists"}

    if record.get("status") != "needs_decision":
        return {"outcome": "refused", "code": "draft_not_in_shortfall",
                "detail": "this injection draft is not awaiting a shortfall decision"}

    if option not in SHORTFALL_OPTIONS:
        return {"outcome": "refused", "code": "unknown_option",
                "detail": f"{option!r} is not a valid shortfall option"}

    if _read_injection_answer(
            job.job_id, draft_id, control_root_path=control_root_path) is not None:
        return {"outcome": "refused", "code": "already_answered",
                "detail": f"injection draft {draft_id!r} was already answered"}

    seed = record.get("decision_seed") or {}
    if option == "shrink_task" and seed.get("shrink_band") is None:
        return {"outcome": "refused", "code": "cannot_shrink",
                "detail": "this task is already at the smallest size; it cannot shrink"}

    now_dt = now if now is not None else datetime.now(timezone.utc)
    bounded_actor = _bounded_actor(actor)
    derived_draft_id = None if option == "drop" else _sp.new_request_id()

    answer_record = {
        "injection_answer_v": 1,
        "job_id": job.job_id,
        "draft_id": draft_id,
        "option": option,
        "actor": bounded_actor,
        "answered_at": now_dt.isoformat(),
        "derived_draft_id": derived_draft_id,
    }
    published = _publish_injection_answer(
        job.job_id, draft_id, answer_record, control_root_path=control_root_path)
    if not published:
        return {"outcome": "refused", "code": "already_answered",
                "detail": f"injection draft {draft_id!r} was already answered"}

    if option == "drop":
        return {"outcome": "dropped", "job_id": job.job_id, "draft_id": draft_id,
                "answered_at": answer_record["answered_at"]}

    task = dict(record["task"])
    placement = record["placement"]
    expires_dt = now_dt + timedelta(seconds=INJECTION_DRAFT_TTL_SECONDS)

    if option == "shrink_task":
        shrink_band = seed["shrink_band"]
        task["est_tokens_band"] = shrink_band
        check = injection_budget_check(budgets, counters, band=shrink_band, config=config)
        shortfall = bool(check["shortfall"])
        budget_extend_to_usd = None
    else:                                                          # extend_budget
        # DECISION F028 D4 (4): re-check against the CURRENT counters before trusting the
        # seed's amount — spend between the draft and this answer must not leave the
        # raised limit short. Rounded up to the cent exactly as `shortfall_decision_seed`
        # rounds it, and only the larger of the two ever wins.
        fresh_check = injection_budget_check(
            budgets, counters, band=task["est_tokens_band"], config=config)
        fresh_spent = fresh_check.get("spent_cost_usd")
        fresh_expected = fresh_check.get("expected_cost_usd")
        if fresh_spent is not None and fresh_expected is not None:
            recomputed_extend_to_usd = float(
                Decimal(repr(round(fresh_spent + fresh_expected, 6))).quantize(
                    Decimal("0.01"), rounding=ROUND_CEILING))
            extend_to_usd = max(recomputed_extend_to_usd, seed["extend_to_usd"])
        else:
            extend_to_usd = seed["extend_to_usd"]
        extended_budgets = budgets.model_copy(update={"max_cost_usd": extend_to_usd})
        check = injection_budget_check(
            extended_budgets, counters, band=task["est_tokens_band"], config=config)
        shortfall = False
        budget_extend_to_usd = extend_to_usd

    derived_answer: dict[str, Any] = {
        "outcome": "shortfall" if shortfall else "drafted",
        "job_id": job.job_id,
        "draft_id": derived_draft_id,
        "confirm_token": None if shortfall else derived_draft_id,
        "task": task,
        "placement": placement,
        "task_rationale": record["task_rationale"],
        "budget_check": check,
        "decision_seed": shortfall_decision_seed(check) if shortfall else None,
        "fence_conflicts": record.get("fence_conflicts", []),
        "drafted_at": now_dt.isoformat(),
        "expires_at": expires_dt.isoformat(),
        "planner_calls": 0,
        "text": record["text"],
        "derived_from": draft_id,
        "answer": option,
        "budget_extend_to_usd": budget_extend_to_usd,
    }

    derived_record = dict(derived_answer)
    derived_record["injection_draft_v"] = 1
    derived_record["status"] = "needs_decision" if shortfall else "confirmable"
    derived_record["actor"] = bounded_actor
    derived_record["after"] = record.get("after")

    _publish_injection_draft(
        job.job_id, derived_draft_id, derived_record, control_root_path=control_root_path)

    return derived_answer


# ---------------------------------------------------------------------------
# S3/T002 — the confirmation: a second create-only control file (DECISION F028 D2 (2))
# ---------------------------------------------------------------------------


def _validate_confirmed_record(record: dict[str, Any]) -> None:
    """R-1077's repair: every field ``apply_injection_to_job`` reads must exist, with the type
    it needs, before this record is trusted. ``apply_injection_to_job`` indexes ``placement``,
    ``task_rationale``, ``actor``, ``text`` and ``confirmed_at`` AFTER it had already started
    mutating ``job`` — a record lacking one raised a bare ``KeyError`` there, leaving the job
    ``running`` on disk instead of the blocked state DECISION F028 D2 (3) promises. Checking
    every field here, before any record reaches the apply, closes that hole regardless of
    which caller reads the record next.
    """
    draft_id = record.get("draft_id")
    if not isinstance(draft_id, str) or not draft_id:
        raise TaskInjectionError("a confirmed task injection entry carries no draft id")
    if not isinstance(record.get("task"), dict):
        raise TaskInjectionError("a confirmed task injection entry carries no task")
    placement = record.get("placement")
    if not isinstance(placement, dict):
        raise TaskInjectionError("a confirmed task injection entry carries no placement")
    if not isinstance(placement.get("rationale"), str):
        raise TaskInjectionError(
            "a confirmed task injection entry's placement carries no rationale")
    if not isinstance(placement.get("basis"), str):
        raise TaskInjectionError(
            "a confirmed task injection entry's placement carries no basis")
    for field in ("task_rationale", "text", "actor", "confirmed_at"):
        if not isinstance(record.get(field), str):
            raise TaskInjectionError(f"a confirmed task injection entry carries no {field}")
    if "budget_extend_to_usd" in record:
        extend_to_usd = record["budget_extend_to_usd"]
        if extend_to_usd is not None:
            if (isinstance(extend_to_usd, bool)
                    or not isinstance(extend_to_usd, (int, float))
                    or extend_to_usd <= 0):
                raise TaskInjectionError(
                    "a confirmed task injection entry carries an invalid budget_extend_to_usd")
    if "confirmed_unseen" in record and not isinstance(record["confirmed_unseen"], bool):
        raise TaskInjectionError(
            "a confirmed task injection entry carries a non-bool confirmed_unseen")


def confirmed_injections(job_id: str, *,
                         control_root_path: Path | None = None) -> tuple[dict, ...]:
    """Every confirmed injection, ordered by ``(confirmed_at, draft_id)``.

    ``()`` when the control root, the job's directory or ``INJECTED_TASKS_DIRNAME`` does not
    exist. A file that is not a JSON object, or fails ``_validate_confirmed_record`` (R-1077),
    raises ``TaskInjectionError`` — dropping it would silently forget a confirmed injection the
    operator already made.
    """
    jid = _sp.validate_job_id(job_id)
    try:
        job_fd = _sp.open_job_control_fd(jid, control_root_path, create=False)
    except _sp.StopControlError as exc:
        raise TaskInjectionError(str(exc)) from exc
    if job_fd is None:
        return ()

    injections_fd = None
    try:
        injections_fd = _open_named_dir(job_fd, INJECTED_TASKS_DIRNAME, create=False)
        if injections_fd is None:
            return ()
        names = _fs.list_dir_names(injections_fd, error_cls=TaskInjectionError,
                                   noun="confirmed task injections")
        out: list[dict[str, Any]] = []
        for name in names:
            raw = _fs.read_verified_file(
                name, injections_fd, max_bytes=_sp.MAX_CONTROL_BYTES,
                error_cls=TaskInjectionError, noun="confirmed task injection")
            if raw is None:
                continue
            try:
                record = json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeDecodeError) as exc:
                raise TaskInjectionError(
                    f"a confirmed task injection entry is not valid JSON: {exc}") from exc
            if not isinstance(record, dict):
                raise TaskInjectionError("a confirmed task injection entry is not a JSON object")
            _validate_confirmed_record(record)
            out.append(record)
        out.sort(key=lambda r: (r.get("confirmed_at") or "", r["draft_id"]))
        return tuple(out)
    finally:
        if injections_fd is not None:
            os.close(injections_fd)
        os.close(job_fd)


def _publish_confirmed_injection(job_id: str, draft_id: str, record: dict[str, Any], *,
                                 control_root_path: Path | None) -> bool:
    """Publish one create-only confirmed-injection file. Mirrors ``_publish_injection_draft``,
    but a lost race is the caller's ``already_confirmed`` to answer, not a raised error, so
    this returns whether the write won rather than raising when it did not."""
    jid = _sp.validate_job_id(job_id)
    try:
        job_fd = _sp.open_job_control_fd(jid, control_root_path, create=True)
    except _sp.StopControlError as exc:
        raise TaskInjectionError(str(exc)) from exc
    assert job_fd is not None
    injections_fd = None
    try:
        injections_fd = _open_named_dir(job_fd, INJECTED_TASKS_DIRNAME, create=True)
        assert injections_fd is not None
        name = _draft_filename(draft_id)
        return _fs.write_file_atomically(
            injections_fd, name, _fs.json_bytes(record), create_only=True,
            file_mode=_sp.CONTROL_FILE_MODE, error_cls=TaskInjectionError,
            noun="confirmed task injection")
    finally:
        if injections_fd is not None:
            os.close(injections_fd)
        os.close(job_fd)


def confirm_task_injection(
    job: Any,
    confirm_token: Any,
    *,
    actor: Any,
    unseen: bool = False,
    now: datetime | None = None,
    control_root_path: Path | None = None,
) -> dict[str, Any]:
    """Confirm a drafted injection, or answer a refusal. NEVER raises for a refusal.

    Checks, in order: S4's terminal check (``job_terminal``); ``read_injection_draft``
    refusing with its own code; a record naming another job (``draft_unknown``); a
    ``status`` other than ``confirmable`` (``draft_needs_decision``); a confirmation already
    on file for this draft (``already_confirmed``); ``job.task_plan`` unreadable
    (``no_task_plan``); the draft's task id already used, by the plan or by a confirmed
    injection ``job.metadata["task_injections"]`` does not yet hold, or a ``depends_on`` id
    in neither set (``draft_stale``, telling the operator to draft again); and the two sets
    together at ``MAX_PLAN_TASKS`` or more (``plan_full``). A refusal writes nothing.

    DECISION F028 D4 (2): ``unseen``, True only when a caller confirms a draft without a
    human reviewing it first (the CLI's ``job inject --yes``), is stored on the persisted
    record as ``confirmed_unseen`` (``bool(unseen)``) so an unattended confirmation is told
    apart from a reviewed one wherever the add is read.

    Otherwise publishes ONE create-only file in ``INJECTED_TASKS_DIRNAME`` and answers
    ``{"outcome": "confirmed", "job_id", "draft_id", "task_id", "placement", "confirmed_at"}``.
    """
    refusal = injection_refusal(getattr(job, "state", ""), 0)
    if refusal is not None:
        return {"outcome": "refused", "code": refusal.code, "detail": refusal.detail}

    try:
        record = read_injection_draft(
            job.job_id, confirm_token, now=now, control_root_path=control_root_path)
    except TaskInjectionRefused as exc:
        return {"outcome": "refused", "code": exc.code, "detail": exc.detail}

    if record.get("job_id") != job.job_id:
        return {"outcome": "refused", "code": "draft_unknown",
                "detail": f"no injection draft {confirm_token!r} exists"}

    if record.get("status") != "confirmable":
        return {"outcome": "refused", "code": "draft_needs_decision",
                "detail": "this injection draft needs its shortfall decision answered first"}

    draft_id = record["draft_id"]
    task_injections = job.metadata.get("task_injections") or {}
    existing = confirmed_injections(job.job_id, control_root_path=control_root_path)
    if any(r["draft_id"] == draft_id for r in existing):
        return {"outcome": "refused", "code": "already_confirmed",
                "detail": f"injection draft {confirm_token!r} was already confirmed"}

    raw_plan = getattr(job, "task_plan", None)
    plan: TaskPlan | None = None
    if isinstance(raw_plan, dict):
        try:
            plan = TaskPlan.model_validate(
                {k: v for k, v in raw_plan.items() if not k.startswith("_")})
        except ValidationError:
            plan = None
    if plan is None:
        return {"outcome": "refused", "code": "no_task_plan",
                "detail": "this job has no readable task plan to confirm an injection into"}

    plan_ids = {t.id for t in plan.tasks}
    unfolded_ids = {
        r["task"]["id"] for r in existing if r["draft_id"] not in task_injections
    }
    known_ids = plan_ids | unfolded_ids

    task = record["task"]
    if task["id"] in known_ids:
        return {"outcome": "refused", "code": "draft_stale",
                "detail": f"task id {task['id']!r} is already used; draft again"}
    for dep in task.get("depends_on") or []:
        if dep not in known_ids:
            return {"outcome": "refused", "code": "draft_stale",
                    "detail": f"task {task['id']!r} depends on {dep!r}, which is no longer "
                              "in the plan; draft again"}

    if len(known_ids) >= MAX_PLAN_TASKS:
        return {"outcome": "refused", "code": "plan_full",
                "detail": f"the plan is already at its {MAX_PLAN_TASKS}-task cap"}

    now_dt = now if now is not None else datetime.now(timezone.utc)
    confirmed_record = {
        "injected_task_v": 1,
        "job_id": job.job_id,
        "draft_id": draft_id,
        "task": task,
        "placement": record["placement"],
        "task_rationale": record["task_rationale"],
        "text": record["text"],
        "drafted_by": record.get("actor"),
        "actor": _bounded_actor(actor),
        "confirmed_at": now_dt.isoformat(),
        # DECISION F028 D4 (2): True only for an unattended `--yes` confirmation.
        "confirmed_unseen": bool(unseen),
        # DECISION F028 D3 (2): carried from the draft, None when the draft never named an
        # extension, into the fold's own reading of `apply_injection_to_job`.
        "budget_extend_to_usd": record.get("budget_extend_to_usd"),
    }
    published = _publish_confirmed_injection(
        job.job_id, draft_id, confirmed_record, control_root_path=control_root_path)
    if not published:
        return {"outcome": "refused", "code": "already_confirmed",
                "detail": f"injection draft {confirm_token!r} was already confirmed"}

    return {"outcome": "confirmed", "job_id": job.job_id, "draft_id": draft_id,
            "task_id": task["id"], "placement": confirmed_record["placement"],
            "confirmed_at": confirmed_record["confirmed_at"]}


# ---------------------------------------------------------------------------
# S4/T002 — the apply: one edit, one entry, one provenance block (DECISION F028 D2 (4))
# ---------------------------------------------------------------------------


def apply_injection_to_job(job: Any, record: dict[str, Any], *,
                           now: datetime | None = None) -> dict[str, Any]:
    """Apply one confirmed injection to *job*, changing only the in-memory object.

    Raises ``TaskInjectionRefused("injection_invalid", detail)``, leaving ``job`` untouched,
    when ``job.task_plan`` does not read as a plan or
    ``plan_editing.apply_edit(plan, "plan_add_task", ...)`` refuses. R-1077's repair: every
    other value this function reads from ``record`` is read, and every value it derives is
    computed, BEFORE ``job`` changes — the mutations of ``job`` (``job.tasks.append``,
    ``job.task_plan = ...`` and, when it applies, ``job.budgets = ...``) are its LAST
    statements, so an exception anywhere above them (a record missing a field the caller
    should have validated first) leaves ``job`` exactly as it was, never half-applied.
    Otherwise, as ``edit_task_at_runtime`` does: ``map_task_plan_to_tasks``,
    ``record_llm_task_deliverables``, and the one mapped entry for the new task is appended to
    ``job.tasks`` with its ``inputs["plan"]`` carrying the provenance, the plan version
    bumped, the approval hash re-sealed when the old body was approved with one, and the edit
    log extended by one entry naming ``plan_add_task`` and carrying an ``injection`` block —
    gaining ``budget_extend_to_usd`` (the record's value) when the record carries that key at
    all, and always carrying ``confirmed_unseen`` (DECISION F028 D4 (2), the record's value,
    False for one lacking the key). DECISION F028 D3 (2): when the record's
    ``budget_extend_to_usd`` is a real number,
    ``job.budgets`` is a dict and its current ``max_cost_usd`` is not None and lower than it,
    ``job.budgets["max_cost_usd"]`` is raised to it — an extension never creates a limit and
    never lowers one. Answers ``{"task_id", "planned_id", "folded_at"}``.
    """
    raw_plan = getattr(job, "task_plan", None)
    plan: TaskPlan | None = None
    if isinstance(raw_plan, dict):
        try:
            plan = TaskPlan.model_validate(
                {k: v for k, v in raw_plan.items() if not k.startswith("_")})
        except ValidationError:
            plan = None
    if plan is None:
        raise TaskInjectionRefused(
            "injection_invalid", "this job has no readable task plan to apply the injection to")

    body = raw_plan
    task_dict = record["task"]
    try:
        new_plan = plan_editing.apply_edit(plan, "plan_add_task", {"task": task_dict})
    except plan_editing.PlanEditRefused as exc:
        raise TaskInjectionRefused("injection_invalid", exc.detail) from exc

    mapped = map_task_plan_to_tasks(new_plan)
    record_llm_task_deliverables(mapped)
    planned_id = task_dict["id"]
    fresh = next(
        t for t in mapped if (t.inputs.get("plan") or {}).get("planned_id") == planned_id)

    placement = record["placement"]
    plan_rationale = placement["rationale"]
    basis = placement["basis"]
    task_rationale = record["task_rationale"]
    draft_id = record["draft_id"]
    actor = record["actor"]
    text = record["text"]
    confirmed_at = record["confirmed_at"]

    # `fresh` is a fresh object `map_task_plan_to_tasks` just built — not yet part of
    # `job.tasks` — so filling in its provenance here is not yet a change to `job`.
    fresh.inputs["plan"]["origin"] = ORIGIN_HUMAN_INJECTED
    fresh.inputs["plan"]["plan_rationale"] = plan_rationale
    fresh.inputs["plan"]["task_rationale"] = task_rationale
    fresh.inputs["plan"]["injection_draft_id"] = draft_id

    version = plan_editing.plan_version(body)
    now_dt = now if now is not None else datetime.now(timezone.utc)

    new_body = new_plan.model_dump()
    new_body.update({k: v for k, v in body.items() if k.startswith("_")})
    new_body[PLAN_VERSION_KEY] = version + 1

    if body.get("_approval") == "approved" and body.get(APPROVED_PLAN_HASH_KEY):
        new_body[APPROVED_PLAN_HASH_KEY] = plan_content_hash(new_body)

    dod_resync_pending = job_dod_path(job.job_id).is_file()
    injection_block: dict[str, Any] = {
        "draft_id": draft_id,
        "task_id": fresh.task_id,
        "planned_id": planned_id,
        "origin": ORIGIN_HUMAN_INJECTED,
        "basis": basis,
        "plan_rationale": plan_rationale,
        "text": text,
        "confirmed_at": confirmed_at,
        # DECISION F028 D4 (2): carried from the confirmation, False for one lacking the
        # key at all (a record round 2 or round 3 wrote, before this field existed).
        "confirmed_unseen": record.get("confirmed_unseen", False),
        "dod_resync_pending": dod_resync_pending,
    }
    if "budget_extend_to_usd" in record:
        injection_block["budget_extend_to_usd"] = record["budget_extend_to_usd"]

    log_entry: dict[str, Any] = {
        "version": version + 1,
        "ts": now_dt.isoformat(),
        "actor": actor,
        "command": "plan_add_task",
        "args": {"task": task_dict},
        "before": [t.model_dump() for t in plan.tasks],
        "after": [t.model_dump() for t in new_plan.tasks],
        "injection": injection_block,
    }
    new_body[plan_editing.EDIT_LOG_KEY] = [*body.get(plan_editing.EDIT_LOG_KEY, []), log_entry]

    # DECISION F028 D3 (2) — computed last: raise the job's cost limit, never create or
    # lower one.
    extend_to_usd = record.get("budget_extend_to_usd")
    new_budgets: dict[str, Any] | None = None
    if (extend_to_usd is not None and isinstance(job.budgets, dict)
            and job.budgets.get("max_cost_usd") is not None
            and job.budgets["max_cost_usd"] < extend_to_usd):
        new_budgets = dict(job.budgets)
        new_budgets["max_cost_usd"] = extend_to_usd

    # THE MUTATIONS — everything above is computed; `job` changes only from here on.
    job.tasks.append(fresh)
    job.task_plan = new_body
    if new_budgets is not None:
        job.budgets = new_budgets

    folded_at = now_dt.isoformat()
    return {"task_id": fresh.task_id, "planned_id": planned_id, "folded_at": folded_at}
