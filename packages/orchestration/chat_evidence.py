"""F038 T001 — the grounded chat's node-scope evidence: the item, its problems, the
composer that keeps an ordered prefix under the token cap, and the collector of one
task's own records (DECISION F038 D1).

Remedy deliberately does not let a scope's evidence reach past its own records: the
node scope answers only from one task's own record, its own rounds, its own diff and
its own run-log events — never another task's, and never the whole job's.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.diff_view_source import build_diff_view
from packages.orchestration.evidence_index import resolve_job_evidence_dir
from packages.orchestration.run_rounds_view import build_task_run_rounds
from packages.orchestration.stream_evidence import redact_text
from packages.orchestration.timeline import load_run_events
from packages.orchestration.token_economy import estimate_text_tokens

#: The one scope this round lands. The project scope joins a later round
#: (DECISION F038 D1 (6)).
CHAT_SCOPE_NODE = "node"
CHAT_SCOPES = (CHAT_SCOPE_NODE,)

#: The four evidence anchor kinds the node scope cites (DECISION F038 D1 (4)).
CHAT_ANCHOR_KINDS = ("node", "round", "diff", "event")

#: DECISION F038 D1 (3): the composed set's token ceiling.
CHAT_EVIDENCE_TOKEN_CAP = 4000

#: DECISION F038 D1 (2): one fact, one line, at most this many characters — a cut
#: never leaves half a secret, because redaction runs before the cut.
CHAT_ITEM_TEXT_MAX_CHARS = 400

#: The fact an absent-fact answer cites (DECISION F038 D1 (4)).
CHAT_NOT_RECORDED = "not recorded"


class ChatEvidenceError(ValueError):
    """A malformed evidence item, or a scope this module does not compose."""


@dataclass(frozen=True)
class ChatEvidenceItem:
    """One numbered fact a grounded chat answer can cite: an anchor and its text."""

    kind: str
    ref: str
    text: str


@dataclass(frozen=True)
class ChatEvidenceSet:
    """An ordered, capped set of evidence items composed for one scope and subject."""

    scope: str
    subject: str
    items: tuple[ChatEvidenceItem, ...]
    omitted: int
    tokens_estimated: int


def chat_item_problems(item: Any) -> list[str]:
    """Every way ``item`` breaches the evidence-item contract, one line each.

    ``[]`` for a sound item. An item that is not even a :class:`ChatEvidenceItem`
    reports only that — its kind, ref and text cannot be trusted to exist at all.
    """
    if not isinstance(item, ChatEvidenceItem):
        return ["not a ChatEvidenceItem"]
    problems: list[str] = []
    if item.kind not in CHAT_ANCHOR_KINDS:
        problems.append(
            f"kind {item.kind!r} is not one of {', '.join(CHAT_ANCHOR_KINDS)}"
        )
    if not isinstance(item.ref, str) or not item.ref:
        problems.append("ref is not a non-empty string")
    if not isinstance(item.text, str) or not item.text.strip():
        problems.append("text is not a non-empty string")
    elif "\n" in item.text or "\r" in item.text:
        problems.append("text holds a line break")
    elif len(item.text) > CHAT_ITEM_TEXT_MAX_CHARS:
        problems.append(f"text is longer than {CHAT_ITEM_TEXT_MAX_CHARS} characters")
    return problems


def make_chat_item(kind: str, ref: str, text: str) -> ChatEvidenceItem:
    """Build one evidence item: redact first, fold to one line, then cut to the bound.

    Redaction runs BEFORE the fold and the cut, so a cut never leaves half a secret.
    """
    redacted = redact_text(text)
    folded = " ".join(redacted.split())
    if len(folded) > CHAT_ITEM_TEXT_MAX_CHARS:
        folded = folded[: CHAT_ITEM_TEXT_MAX_CHARS - 1] + "…"
    return ChatEvidenceItem(kind=kind, ref=ref, text=folded)


def render_chat_item(number: int, item: ChatEvidenceItem) -> str:
    """One citable line: ``[n] kind:ref — text``."""
    return f"[{number}] {item.kind}:{item.ref} — {item.text}"


def render_chat_evidence(evidence_set: ChatEvidenceSet) -> str:
    """Every item of ``evidence_set``, numbered from 1, one per line. ``""`` for none."""
    return "\n".join(
        render_chat_item(number, item)
        for number, item in enumerate(evidence_set.items, start=1)
    )


def compose_chat_evidence(
    scope: str,
    subject: str,
    items: Sequence[ChatEvidenceItem],
    *,
    token_cap: int = CHAT_EVIDENCE_TOKEN_CAP,
) -> ChatEvidenceSet:
    """Keep an ordered prefix of ``items`` whose rendering estimates at most ``token_cap``.

    Refuses a scope this module does not compose, or an item with any problem, before
    composing anything. Otherwise walks the items in order, keeping each while the
    rendered set of everything kept so far plus this one estimates within the cap;
    stops at the first item that does not fit and counts the rest as omitted.
    """
    if scope not in CHAT_SCOPES:
        raise ChatEvidenceError(f"scope {scope!r} is not one of {', '.join(CHAT_SCOPES)}")
    for index, item in enumerate(items):
        problems = chat_item_problems(item)
        if problems:
            raise ChatEvidenceError(f"item {index}: {'; '.join(problems)}")

    kept: list[ChatEvidenceItem] = []
    tokens_estimated = 0
    for item in items:
        candidate = [*kept, item]
        rendered = "\n".join(
            render_chat_item(number, it) for number, it in enumerate(candidate, start=1)
        )
        estimate = estimate_text_tokens(rendered)
        if estimate > token_cap:
            break
        kept.append(item)
        tokens_estimated = estimate
    omitted = len(items) - len(kept)

    return ChatEvidenceSet(
        scope=scope,
        subject=subject,
        items=tuple(kept),
        omitted=omitted,
        tokens_estimated=tokens_estimated,
    )


def _tests_word(test_passed: Any) -> str:
    if test_passed is True:
        return "passed"
    if test_passed is False:
        return "failed"
    return CHAT_NOT_RECORDED


def _record_items(task: Any, task_id: str) -> list[ChatEvidenceItem]:
    """S5 (a): the task's own record, each fact its own item anchored at the task id."""
    items = [
        make_chat_item(
            "node", task_id, f"Task {task_id}: {task.title or CHAT_NOT_RECORDED}"
        )
    ]

    status_text = f"Status: {task.status}"
    final_status = task.final_status
    if final_status:
        status_text += f"; final status: {final_status}"
        if task.final_status_detail:
            status_text += f" ({task.final_status_detail})"
    items.append(make_chat_item("node", task_id, status_text))

    items.append(
        make_chat_item(
            "node", task_id,
            f"Reviewer verdict: {task.reviewer_verdict or CHAT_NOT_RECORDED}",
        )
    )
    items.append(
        make_chat_item("node", task_id, f"Tests: {_tests_word(task.test_passed)}")
    )
    items.append(
        make_chat_item(
            "node", task_id,
            f"Repair rounds used: {task.repair_rounds_used} of "
            f"{task.repair_rounds_allowed}",
        )
    )
    if task.error:
        items.append(make_chat_item("node", task_id, f"Error: {task.error}"))
    if task.tripped_limit:
        items.append(
            make_chat_item("node", task_id, f"Tripped limit: {task.tripped_limit}")
        )
    return items


def _round_items(job: Any, task_id: str) -> list[ChatEvidenceItem]:
    """S5 (b): the task's latest run's rounds, or one node item naming the absence."""
    envelope = build_task_run_rounds(job, task_id)
    if not envelope["available"]:
        return [
            make_chat_item(
                "node", task_id, f"Run rounds: not recorded ({envelope['reason']})"
            )
        ]
    items = []
    for round_facts in envelope["rounds"]:
        round_number = round_facts.get("round")
        kind = round_facts.get("kind") or CHAT_NOT_RECORDED
        reviewer = round_facts.get("reviewer") or {}
        verdict = reviewer.get("verdict") or CHAT_NOT_RECORDED
        text = (
            f"Round {round_number} ({kind}): "
            f"tests {_tests_word(round_facts.get('test_passed'))}; "
            f"reviewer verdict {verdict}"
        )
        items.append(make_chat_item("round", f"{task_id}#{round_number}", text))
    return items


def _diff_items(job_id: str, task_id: str) -> list[ChatEvidenceItem]:
    """S5 (c): the task's own diff, or one node item naming the absence."""
    view = build_diff_view(resolve_job_evidence_dir(job_id), task_id=task_id)
    if not view["available"]:
        return [
            make_chat_item("node", task_id, f"Diff: not recorded ({view['reason']})")
        ]
    items = []
    for file_entry in view["files"]:
        path = file_entry["path"]
        stats = file_entry.get("stats") or {}
        added = stats.get("added", 0)
        deleted = stats.get("deleted", 0)
        text = f"Changed {path} ({file_entry['status']}, +{added} −{deleted})"
        items.append(make_chat_item("diff", path, text))
    if view["truncated"]:
        items.append(
            make_chat_item(
                "node", task_id,
                "Diff: cut at its size ceiling; later files are not listed",
            )
        )
    return items


def _event_task_ref(event: dict[str, Any]) -> Any:
    """The task an event names: its top-level ``task_id`` when set, else the one
    under ``metadata`` when ``metadata`` is a dict."""
    top_level = event.get("task_id")
    if top_level is not None:
        return top_level
    metadata = event.get("metadata")
    return metadata.get("task_id") if isinstance(metadata, dict) else None


def _run_log_items(job_id: str, task_id: str) -> list[ChatEvidenceItem]:
    """S5 (d): the task's own run-log events, newest first, or one node item naming
    the absence."""
    events = load_run_events(resolve_data_root(), job_id)
    qualifying = [
        event
        for event in reversed(events)
        if isinstance(event.get("event"), str)
        and event.get("event")
        and _event_task_ref(event) == task_id
    ]
    if not qualifying:
        return [
            make_chat_item("node", task_id, "Run log: not recorded for this task")
        ]
    items = []
    for event in qualifying:
        name = event["event"]
        timestamp = event.get("timestamp", "")
        text = f"{timestamp} {name}"
        message = event.get("message")
        if message:
            text += f": {message}"
        outcome = event.get("outcome")
        if outcome:
            text += f" (outcome {outcome})"
        items.append(make_chat_item("event", f"{name}@{timestamp}", text))
    return items


def collect_node_evidence(job: Any, task_id: str) -> list[ChatEvidenceItem]:
    """One task's own evidence: its record, its rounds, its diff and its run log.

    Raises :class:`ChatEvidenceError` when ``task_id`` names no task of ``job``.
    """
    task = next(
        (t for t in (getattr(job, "tasks", None) or []) if str(t.task_id) == task_id),
        None,
    )
    if task is None:
        raise ChatEvidenceError(
            f"task {task_id!r} is not a task of job {job.job_id}"
        )
    return [
        *_record_items(task, task_id),
        *_round_items(job, task_id),
        *_diff_items(job.job_id, task_id),
        *_run_log_items(job.job_id, task_id),
    ]


def node_evidence_set(
    job: Any, task_id: str, *, token_cap: int = CHAT_EVIDENCE_TOKEN_CAP
) -> ChatEvidenceSet:
    """The composed node-scope evidence set for one task of ``job``."""
    return compose_chat_evidence(
        CHAT_SCOPE_NODE, task_id, collect_node_evidence(job, task_id), token_cap=token_cap
    )
