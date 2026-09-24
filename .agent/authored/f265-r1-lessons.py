"""F265 T001 — the post-task lesson: one sealed record per completed Run, built from its real diff.

When a task of a job completes, the teacher reads the diff that task's Run actually produced
(`runs/<run_id>/result.diff`, the file the ping-pong loop writes and the job's evidence hashes)
and explains it: what was built, which constructs it uses, what they do, why they are used
here, and whether that is good practice, stated as the teacher's judgement (T5_F265.md,
"Goal & Done"). The lesson is stored as a SEALED, create-once record beside that Run's diff,
keyed on the Run and naming its Mission (DECISION F265 D1), so reading a lesson again is a
file read and never a second model call.

The call runs under the `teacher` role's own transport and model (`teacher_model`) and inside
the teacher's own budget pot for the job, which is measured from the teacher's rows in the
token ledger before any call is made. Every call that happens is billed there as role
`teacher` through `teacher_spend`, the one place such a row is built.

Remedy deliberately records an HONEST EMPTY LESSON instead of a thin one: a Run with no diff,
a diff too large to send whole, a spent pot, an unusable transport or an unreadable reply each
produce a record whose status says which, and none of them carries a summary. A lesson built
from part of a diff while presenting itself as complete would teach the plan, not what
shipped (T5_F265.md, "Design").
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import sqlite3
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.common.secure_fs import SecureFsError, json_bytes, write_file_atomically

SCHEMA = "remedy.lesson.v1"
LESSON_FILENAME = "lesson.json"
#: The Run's diff as the ping-pong loop writes it; the lesson reads this file and nothing else.
RUN_DIFF_FILENAME = "result.diff"
#: A diff longer than this is not sent at all: cutting it would teach part of the change as whole.
LESSON_MAX_DIFF_CHARS = 60_000
#: A reply longer than this is not parsed; a lesson is a page, not a transcript.
LESSON_MAX_REPLY_CHARS = 40_000

STATUS_READY = "ready"
STATUS_NO_DIFF = "no_diff"
STATUS_DIFF_TOO_LARGE = "diff_too_large"
STATUS_NO_LEDGER = "no_ledger"
STATUS_BUDGET_EXHAUSTED = "budget_exhausted"
STATUS_TEACHER_UNAVAILABLE = "teacher_unavailable"
STATUS_UNREADABLE_REPLY = "unreadable_reply"
LESSON_STATUSES = (
    STATUS_READY, STATUS_NO_DIFF, STATUS_DIFF_TOO_LARGE, STATUS_NO_LEDGER,
    STATUS_BUDGET_EXHAUSTED, STATUS_TEACHER_UNAVAILABLE, STATUS_UNREADABLE_REPLY,
)
_CONSTRUCT_FIELDS = ("name", "what", "why_here", "judgement")


class LessonError(ValueError):
    """A stored lesson is not intact, or cannot be written."""


def _seal(body: dict[str, Any]) -> str:
    unsealed = {k: v for k, v in body.items() if k != "record_sha256"}
    return hashlib.sha256(json.dumps(unsealed, sort_keys=True).encode("utf-8")).hexdigest()


def lesson_path(run_id: str, root: Path | None = None) -> Path:
    """Where the lesson of ``run_id`` lives: beside the diff it was built from."""
    from packages.orchestration.data_paths import run_dir

    return run_dir(run_id, root) / LESSON_FILENAME


def read_run_diff(run_id: str, root: Path | None = None) -> str | None:
    """The Run's recorded diff, or None when the Run recorded none."""
    from packages.orchestration.data_paths import run_dir

    try:
        return (run_dir(run_id, root) / RUN_DIFF_FILENAME).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def build_lesson_prompt(diff_text: str, *, task_title: str) -> str:
    """The one prompt a lesson costs: the task's title and its WHOLE diff, never a cut of it."""
    return "\n".join([
        "You are the teacher of a software team. A task has just been completed and its",
        "change is the diff below. Teach a curious developer what this change does.",
        "",
        "Answer with ONE JSON object and nothing else, in this shape:",
        '{"summary": "<two to four sentences: what was built and why>",',
        ' "constructs": [{"name": "<a function, class, call or construct, spelled exactly',
        '                  as it appears on an added line of the diff>",',
        '                 "what": "<what it does>",',
        '                 "why_here": "<why this change uses it here>",',
        '                 "judgement": "<whether this is good practice here, as your',
        '                               judgement, saying what you would weigh>"}]}',
        "Name at most eight constructs. Name only what the diff's added lines contain.",
        "",
        f"TASK: {task_title}",
        "DIFF:",
        diff_text,
    ])


def parse_lesson_reply(text: str) -> tuple[str, list[dict[str, str]]]:
    """The summary and constructs of a reply, or `LessonError` naming why it cannot be read."""
    if len(text) > LESSON_MAX_REPLY_CHARS:
        raise LessonError(f"the reply is {len(text)} characters long; the limit is "
                          f"{LESSON_MAX_REPLY_CHARS}")
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise LessonError("the reply holds no JSON object")
    try:
        body = json.loads(text[start:end + 1])
    except ValueError as exc:
        raise LessonError(f"the reply's JSON does not parse: {exc}") from exc
    if not isinstance(body, dict):
        raise LessonError("the reply's JSON is not an object")
    summary = body.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        raise LessonError("the reply has no summary")
    raw = body.get("constructs", [])
    if not isinstance(raw, list):
        raise LessonError("the reply's constructs are not a list")
    constructs = []
    for item in raw:
        if not isinstance(item, dict) or not all(
                isinstance(item.get(key), str) and item[key].strip() for key in _CONSTRUCT_FIELDS):
            raise LessonError("a construct lacks one of: " + ", ".join(_CONSTRUCT_FIELDS))
        constructs.append({key: item[key].strip() for key in _CONSTRUCT_FIELDS})
    return summary.strip(), constructs


def added_lines(diff_text: str) -> list[str]:
    """The lines the diff ADDS, without their leading `+`; file headers are not content."""
    return [line[1:] for line in diff_text.splitlines()
            if line.startswith("+") and not line.startswith("+++")]


def ground_constructs(constructs: list[dict[str, str]],
                      diff_text: str) -> tuple[list[dict[str, str]], list[str]]:
    """Split ``constructs`` into those named on an added line of the diff and the names that are not.

    This is what makes a lesson about the REAL diff: a construct the model names that no added
    line contains is a construct the change does not use, so it is dropped and its name kept
    in the record's `ungrounded` list rather than taught.
    """
    added = added_lines(diff_text)
    kept: list[dict[str, str]] = []
    dropped: list[str] = []
    for construct in constructs:
        if any(construct["name"] in line for line in added):
            kept.append(construct)
        else:
            dropped.append(construct["name"])
    return kept, dropped


def teacher_pot(job_id: str, budgets: Any, *, project_id: str | None = None,
                ledger_path: Path | str | None = None) -> Any:
    """The teacher's budget pot for ``job_id``, evaluated from the ledger's `teacher` rows.

    Counts every call billed to role `teacher` for this job and the tokens those calls
    reported. A call that reported no tokens still counts as a call, which is why a pot
    carries a call limit beside its token limit (DECISION F265 D1).
    """
    from packages.orchestration.budget_guard import BudgetCounters, evaluate_budget
    from packages.orchestration.teacher_spend import TEACHER_ROLE
    from packages.orchestration.token_ledger import query_cost

    report = query_cost(project_id=project_id, path=ledger_path, job_id=job_id, by="role")
    row = next((r for r in report.rows if r.bucket == TEACHER_ROLE), None)
    calls = row.calls if row is not None else 0
    tokens = [n for n in ((row.tokens_in, row.tokens_out) if row is not None else ())
              if n is not None]
    counters = BudgetCounters(
        provider_calls=calls,
        measured_token_total=sum(tokens),
        measured_call_count=calls if tokens else 0,
        unmeasured_call_count=0 if tokens else calls,
        actual_sources=("token_actuals",) if tokens else (),
    )
    return evaluate_budget(budgets, counters)


def verify_lesson_record(path: Path) -> list[str]:
    """Every reason the lesson at ``path`` is not intact; empty when it is."""
    try:
        body = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"unreadable: {exc}"]
    if not isinstance(body, dict):
        return ["not a JSON object"]
    problems: list[str] = []
    if body.get("schema") != SCHEMA:
        problems.append(f"schema is {body.get('schema')!r}, not {SCHEMA!r}")
    if body.get("record_sha256") != _seal(body):
        problems.append("record_sha256 does not match the record")
    if body.get("run_id") != Path(path).parent.name:
        problems.append(f"run_id {body.get('run_id')!r} does not match the Run's folder")
    if body.get("status") not in LESSON_STATUSES:
        problems.append(f"status {body.get('status')!r} is not a lesson status")
    return problems


def load_lesson(run_id: str, root: Path | None = None) -> dict[str, Any] | None:
    """The stored lesson of ``run_id``, or None when there is none. READ-ONLY.

    A lesson that fails verification raises `LessonError`: a tampered lesson must be loud,
    never silently skipped or silently shown.
    """
    path = lesson_path(run_id, root)
    if not path.is_file():
        return None
    problems = verify_lesson_record(path)
    if problems:
        raise LessonError(f"lesson {path} is not intact: {'; '.join(problems)}")
    return json.loads(path.read_text(encoding="utf-8"))


def generate_lesson(
    *, run_id: str, job_id: str, task_id: str, task_title: str = "", mission_id: str = "",
    budgets: Any = None, call: Callable[..., Any] | None = None,
    config_file: Mapping[str, Any] | None = None, project_id: str | None = None,
    ledger_path: Path | str | None = None, root: Path | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Produce, store and return the lesson of one completed Run.

    A Run that already has a lesson returns it without a model call. Otherwise, in order:
    read the Run's diff, refuse an empty or oversize one, refuse when no ledger can bill the
    call, check the teacher's pot, resolve the teacher's transport, make ONE call, bill it,
    and ground the reply in the diff. Every outcome is stored, so the index can say why a
    Run has no lesson. ``call`` is the transport seam `teacher_model` defines; every test
    supplies a fake.
    """
    existing = load_lesson(run_id, root)
    if existing is not None:
        return existing
    body: dict[str, Any] = {
        "schema": SCHEMA, "lesson_id": f"lesson-{run_id}", "run_id": str(run_id),
        "job_id": str(job_id), "task_id": str(task_id), "mission_id": str(mission_id),
        "task_title": str(task_title), "status": STATUS_READY, "reason": "",
        "generated_at": (now or datetime.now(timezone.utc)).isoformat(),
        "model": "", "diff_sha256": "", "diff_chars": 0, "summary": "",
        "constructs": [], "ungrounded": [], "call_id": "", "billed": False,
    }
    diff = read_run_diff(run_id, root)
    if diff is not None:
        body["diff_sha256"] = hashlib.sha256(diff.encode("utf-8")).hexdigest()
        body["diff_chars"] = len(diff)
    _teach(body, diff, budgets=budgets, call=call, config_file=config_file,
           project_id=project_id, ledger_path=ledger_path)
    return _publish(body, root)


def _teach(body: dict[str, Any], diff: str | None, *, budgets: Any, call: Any,
           config_file: Any, project_id: str | None, ledger_path: Any) -> None:
    """Fill ``body`` with the lesson, or with the status and reason there is none."""
    from packages.orchestration.teacher_model import (
        TEACHER_TRANSPORTS,
        TeacherTransportUnavailable,
        ollama_teacher_call,
        resolve_teacher_transport,
    )
    from packages.orchestration.teacher_spend import record_teacher_question

    def refuse(status: str, reason: str) -> None:
        body["status"], body["reason"] = status, reason

    if diff is None or not diff.strip():
        return refuse(STATUS_NO_DIFF, "this Run recorded no diff, so there is nothing to teach")
    if len(diff) > LESSON_MAX_DIFF_CHARS:
        return refuse(STATUS_DIFF_TOO_LARGE,
                      f"the diff is {len(diff)} characters long and the teacher reads at most "
                      f"{LESSON_MAX_DIFF_CHARS}; a lesson from part of it would not be the change")
    if project_id is None and ledger_path is None:
        return refuse(STATUS_NO_LEDGER, "the job belongs to no registered project, so the "
                      "teacher's spend could not be billed or capped; no model was called")
    try:
        pot = teacher_pot(body["job_id"], budgets, project_id=project_id, ledger_path=ledger_path)
    except sqlite3.Error as exc:
        return refuse(STATUS_NO_LEDGER, f"the job's ledger could not be read ({exc}), so the "
                      "teacher's pot is unknown; no model was called")
    if pot.exhausted:
        return refuse(STATUS_BUDGET_EXHAUSTED, "the teacher's budget pot for this job is spent "
                      f"({pot.first_exhausted_limit}); no model was called")
    transport = resolve_teacher_transport(config_file=config_file)
    if transport is None:
        return refuse(STATUS_TEACHER_UNAVAILABLE, "the teacher role resolves to a provider "
                      f"with no teacher transport (the teacher can call: "
                      f"{', '.join(TEACHER_TRANSPORTS)})")
    _provider, model = transport
    body["model"] = model
    prompt = build_lesson_prompt(diff, task_title=body["task_title"])
    try:
        reply = (call or ollama_teacher_call)(prompt, model=model)
    except TeacherTransportUnavailable as exc:
        return refuse(STATUS_TEACHER_UNAVAILABLE, f"the teacher's transport failed: {exc}")
    body["call_id"], body["billed"] = record_teacher_question(
        model=model, usage=reply.usage, job_id=body["job_id"], path=ledger_path,
        project_id=project_id, call_id=f"teacher:lesson:{body['run_id']}")
    try:
        summary, constructs = parse_lesson_reply(reply.text)
    except LessonError as exc:
        return refuse(STATUS_UNREADABLE_REPLY, f"the teacher's reply could not be read: {exc}")
    kept, dropped = ground_constructs(constructs, diff)
    body["summary"], body["constructs"], body["ungrounded"] = summary, kept, dropped
    return None


def _publish(body: dict[str, Any], root: Path | None) -> dict[str, Any]:
    """Seal ``body`` and publish it create-once; a Run that already has a lesson keeps it."""
    body["record_sha256"] = _seal(body)
    folder = lesson_path(body["run_id"], root).parent
    try:
        folder.mkdir(parents=True, exist_ok=True)
        dir_fd = os.open(folder, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    except OSError as exc:
        raise LessonError(f"the Run's folder cannot be opened: {exc}") from exc
    try:
        published = write_file_atomically(dir_fd, LESSON_FILENAME, json_bytes(body),
                                          create_only=True, noun="lesson")
        if published:
            with contextlib.suppress(OSError):
                os.fsync(dir_fd)
    except SecureFsError as exc:
        raise LessonError(str(exc)) from exc
    finally:
        os.close(dir_fd)
    if not published:
        return load_lesson(body["run_id"], root) or body
    return body


def lessons_enabled() -> bool:
    """Whether a completed task gets a lesson: the `teacher.lessons` key, off by default."""
    from packages.orchestration.config import get_config

    return bool(get_config().get("teacher.lessons"))


def lesson_budgets() -> Any:
    """The teacher's pot per job, from `teacher.lesson_max_calls` and `teacher.lesson_max_tokens`."""
    from packages.core.models import JobBudgets
    from packages.orchestration.config import get_config

    config = get_config()
    return JobBudgets(max_provider_calls=config.get("teacher.lesson_max_calls"),
                      max_total_tokens=config.get("teacher.lesson_max_tokens"))


def lesson_role_overrides() -> dict[str, str] | None:
    """The teacher's configured model as a role override, or None when `teacher.model` is unset."""
    from packages.orchestration.config import get_config

    model = get_config().get("teacher.model")
    return {"model": str(model)} if model else None
