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
