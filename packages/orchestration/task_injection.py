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
from packages.orchestration import budget_guard
from packages.orchestration import safe_points as _sp
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
    "validate_injection_text",
    "injection_refusal",
    "next_injected_task_id",
    "place_injected_task",
    "injection_budget_check",
    "shortfall_decision_seed",
    "fence_conflicts",
    "compose_injection_prompt",
    "draft_task_injection",
    "read_injection_draft",
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
    """The three-option menu a shortfall answers with (DECISION F028 D1 (8))."""
    plan_band = check["plan_band"]
    shrink_band = _SHRINK_BAND.get(plan_band)

    spent = check.get("spent_cost_usd")
    expected = check.get("expected_cost_usd")
    extend_to_usd: float | None = None
    if spent is not None and expected is not None:
        extend_to_usd = float(
            Decimal(repr(round(spent + expected, 6))).quantize(
                Decimal("0.01"), rounding=ROUND_CEILING))

    shrink_label = (
        "the task cannot shrink any further" if shrink_band is None
        else f"shrink the task to the {shrink_band} band")
    option_labels = {
        "extend_budget": "extend the job's budget to cover this task",
        "shrink_task": shrink_label,
        "drop": "drop this task",
    }
    return {
        "question": "the injected task would breach the job's budget; how should it proceed?",
        "options": list(SHORTFALL_OPTIONS),
        "option_labels": [option_labels[option] for option in SHORTFALL_OPTIONS],
        "arithmetic": check["arithmetic"],
        "extend_to_usd": extend_to_usd,
        "shrink_band": shrink_band,
    }


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
    ``TaskInjectionError`` — a corrupt or tampered entry is never silently accepted.
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
    now_dt = now if now is not None else datetime.now(timezone.utc)
    if isinstance(expires_at, str) and expires_at:
        expires_dt = datetime.fromisoformat(expires_at)
        if now_dt >= expires_dt:
            raise TaskInjectionRefused(
                "draft_expired", f"the injection draft {draft_id!r} expired at {expires_at}")

    return record
