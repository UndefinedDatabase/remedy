"""F038 T001 — the grounded chat's evidence: the item, its problems, the composer
that keeps an ordered prefix under the token cap, the node scope's collector of one
task's own records and its prompt trace, and the project scope's collector of one
registry project's own records (DECISION F038 D1, DECISION F038 D3).

Remedy deliberately does not let a scope's evidence reach past its own records: the
node scope answers only from one task's own record, its own rounds, its own prompt
trace, its own diff and its own run-log events — never another task's, and never the
whole job's; the project scope answers only from one registered project's own record,
its linked jobs and its own missions — never another project's.
"""

from __future__ import annotations

import json
import re
import sqlite3
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from packages.orchestration.data_paths import resolve_data_root, run_dir
from packages.orchestration.decision_queue import list_decisions, open_decisions
from packages.orchestration.diff_view_source import build_diff_view
from packages.orchestration.evidence_index import resolve_job_evidence_dir
from packages.orchestration.job_digest import build_job_digest
from packages.orchestration.mission_dossier import load_dossier_state
from packages.orchestration.mission_state import list_missions_safe
from packages.orchestration.pingpong_job import list_job_plans_safe
from packages.orchestration.project_summary import detect_patterns
from packages.orchestration.roadmap_index import (
    RoadmapGrammarError,
    build_index,
    proposed_feature,
)
from packages.orchestration.run_rounds_view import build_task_run_rounds
from packages.orchestration.stream_evidence import redact_text
from packages.orchestration.timeline import load_run_events
from packages.orchestration.token_economy import estimate_text_tokens
from packages.orchestration.token_ledger import query_cost

#: The node scope: one task's own record, rounds, prompt trace, diff and run log
#: (DECISION F038 D1).
CHAT_SCOPE_NODE = "node"
#: The project scope: one registry project's own record, its repository's roadmap
#: position, its linked jobs' open decisions and patterns, its missions' dossiers,
#: its token ledger's totals and one digest per linked job (DECISION F038 D3).
CHAT_SCOPE_PROJECT = "project"
#: Both scopes the composer accepts.
CHAT_SCOPES = (CHAT_SCOPE_NODE, CHAT_SCOPE_PROJECT)

#: Every evidence anchor kind either scope cites: the node scope's five
#: (DECISION F038 D1, extended with the prompt trace) and the project scope's
#: seven (DECISION F038 D3).
CHAT_ANCHOR_KINDS = (
    "node", "round", "prompt", "diff", "event",
    "project", "roadmap", "decision", "pattern", "dossier", "ledger", "job",
)

#: The run id shape a task's prompt trace is filed under (DECISION F038 D3).
_RUN_ID_RE = re.compile(r"^[0-9a-f]{8,32}$")

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


def _prompt_trace_items(task: Any, task_id: str) -> list[ChatEvidenceItem]:
    """S2: the task's own prompt trace, one item per entry — metadata only, never
    the prompt text. Directly after the rounds and before the diff."""
    run_id = getattr(task, "run_id", None)
    if not isinstance(run_id, str) or not _RUN_ID_RE.fullmatch(run_id):
        return [
            make_chat_item(
                "node", task_id, "Prompt trace: not recorded (no_run_recorded)"
            )
        ]
    trace_path = run_dir(run_id) / "prompt_trace.jsonl"
    try:
        text = trace_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [
            make_chat_item("node", task_id, "Prompt trace: not recorded (trace_missing)")
        ]
    except (OSError, UnicodeDecodeError):
        return [
            make_chat_item(
                "node", task_id, "Prompt trace: not recorded (trace_unreadable)"
            )
        ]

    items: list[ChatEvidenceItem] = []
    for line in text.splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(entry, dict):
            continue
        round_number = entry.get("round")
        role = entry.get("role") or CHAT_NOT_RECORDED
        prompt_kind = entry.get("prompt_kind") or CHAT_NOT_RECORDED
        provider = entry.get("provider") or CHAT_NOT_RECORDED
        configured_model = entry.get("configured_model") or CHAT_NOT_RECORDED
        tokens_estimated = entry.get("prompt_tokens_estimated")
        text_line = (
            f"Prompt for round {round_number}, {role} ({prompt_kind}): "
            f"{tokens_estimated} tokens estimated; provider {provider}; "
            f"model {configured_model}"
        )
        items.append(
            make_chat_item("prompt", f"{task_id}#{round_number}/{role}", text_line)
        )
    if not items:
        return [
            make_chat_item("node", task_id, "Prompt trace: not recorded (trace_empty)")
        ]
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
    """One task's own evidence: its record, its rounds, its prompt trace, its diff
    and its run log.

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
        *_prompt_trace_items(task, task_id),
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


# ---------------------------------------------------------------------------
# S3 THE PROJECT SCOPE (DECISION F038 D3).
# ---------------------------------------------------------------------------


def _project_record_item(project: Any, pid: str, job_count: int) -> ChatEvidenceItem:
    """S3 (a): the project's own record, anchored at the project id."""
    repo = project.canonical_repo_path or CHAT_NOT_RECORDED
    return make_chat_item(
        "project", pid,
        f"Project {project.name}: {job_count} linked jobs; repository {repo}",
    )


def _project_roadmap_items(project: Any, pid: str) -> list[ChatEvidenceItem]:
    """S3 (b): the project's roadmap position, read from its own repository."""
    repo_path = project.canonical_repo_path
    if not repo_path:
        return [
            make_chat_item(
                "project", pid, "Roadmap position: not recorded (no repository)"
            )
        ]
    try:
        index = build_index(repo_path)
    except (RoadmapGrammarError, OSError, UnicodeDecodeError) as exc:
        return [
            make_chat_item(
                "project", pid,
                f"Roadmap position: not recorded ({type(exc).__name__})",
            )
        ]
    feature, reason = proposed_feature(index)
    if feature is None:
        return [make_chat_item("project", pid, "Roadmap position: no open feature")]
    verb = "is in progress" if reason == "in_progress" else "is the next open feature"
    return [
        make_chat_item(
            "roadmap", feature.id, f"Roadmap: {feature.id} — {feature.title} {verb}"
        )
    ]


def _project_decision_items(
    jobs: list[Any], events_by_job_id: dict[str, list[dict[str, Any]]]
) -> list[ChatEvidenceItem]:
    """S3 (c): every open decision of every linked job, newest job first."""
    items: list[ChatEvidenceItem] = []
    for job in jobs:
        job_id = str(job.job_id)
        for decision in open_decisions(list_decisions(job, events_by_job_id[job_id])):
            summary = decision.safe_summary or decision.type
            items.append(
                make_chat_item(
                    "decision", f"{job_id}/{decision.id}",
                    f"Open {decision.severity} decision on job {job_id}: {summary}",
                )
            )
    return items


def _project_pattern_items(
    jobs: list[Any], events_by_job_id: dict[str, list[dict[str, Any]]]
) -> list[ChatEvidenceItem]:
    """S3 (d): each pattern detected across the linked jobs."""
    return [
        make_chat_item(
            "pattern", pattern.pattern_id,
            f"Pattern {pattern.kind} ({pattern.severity}): {pattern.summary}",
        )
        for pattern in detect_patterns(jobs, events_by_job_id)
    ]


def _project_dossier_items(project: Any, pid: str) -> list[ChatEvidenceItem]:
    """S3 (e): each mission's dossier goal, next step and open risks."""
    missions, _degraded, _skipped = list_missions_safe(pid)
    items: list[ChatEvidenceItem] = []
    for mission in missions:
        dossier = load_dossier_state(pid, mission.id)
        if dossier is None:
            continue
        items.append(
            make_chat_item("dossier", mission.id, f"Mission goal: {dossier.goal}")
        )
        if dossier.next_step:
            items.append(
                make_chat_item(
                    "dossier", mission.id, f"Mission next step: {dossier.next_step}"
                )
            )
        for risk in dossier.risks:
            if not risk.resolved:
                items.append(
                    make_chat_item("dossier", mission.id, f"Mission risk: {risk.text}")
                )
    if not items:
        return [make_chat_item("project", pid, "Mission dossier: not recorded")]
    return items


def _ledger_figure(value: Any) -> str:
    """S3 (f): an unmeasured figure reads ``unmeasured``, never a fabricated 0."""
    return "unmeasured" if value is None else str(value)


def _project_ledger_items(pid: str) -> list[ChatEvidenceItem]:
    """S3 (f): the project's token ledger totals."""
    try:
        report = query_cost(project_id=pid)
    except sqlite3.Error as exc:
        return [
            make_chat_item(
                "project", pid, f"Token ledger: not readable ({type(exc).__name__})"
            )
        ]
    if not report.ledger_exists:
        return [make_chat_item("project", pid, "Token ledger: not recorded")]
    total = report.total
    cost = "unmeasured" if total.cost_usd is None else f"${total.cost_usd:.2f}"
    return [
        make_chat_item(
            "ledger", pid,
            f"Token ledger: calls {total.calls}; tokens in "
            f"{_ledger_figure(total.tokens_in)}; tokens out "
            f"{_ledger_figure(total.tokens_out)}; cost {cost}",
        )
    ]


def _project_job_items(
    jobs: list[Any], pid: str, events_by_job_id: dict[str, list[dict[str, Any]]]
) -> list[ChatEvidenceItem]:
    """S3 (g): one digest per linked job, newest first."""
    if not jobs:
        return [make_chat_item("project", pid, "Jobs: not recorded for this project")]
    items = []
    for job in jobs:
        job_id = str(job.job_id)
        digest = build_job_digest(job, events_by_job_id[job_id])
        items.append(
            make_chat_item(
                "job", job_id,
                f"Job {job_id} ({digest['state']}): {digest['headline']} "
                f"Open decisions: {digest['decisions']['open_count']}. "
                f"Next: {digest['primary_action']['label']}",
            )
        )
    return items


def collect_project_evidence(project: Any) -> list[ChatEvidenceItem]:
    """One registry project's own evidence (DECISION F038 D3): its record, its
    repository's roadmap position, its linked jobs' open decisions and patterns,
    its missions' dossiers, its token ledger's totals and one digest per linked
    job, newest first.
    """
    pid = str(project.id)
    all_jobs, _degraded, _skipped = list_job_plans_safe()
    linked_ids = set(project.job_ids)
    jobs = [job for job in all_jobs if str(job.job_id) in linked_ids]
    events_by_job_id = {
        str(job.job_id): load_run_events(resolve_data_root(), str(job.job_id))
        for job in jobs
    }
    return [
        _project_record_item(project, pid, len(jobs)),
        *_project_roadmap_items(project, pid),
        *_project_decision_items(jobs, events_by_job_id),
        *_project_pattern_items(jobs, events_by_job_id),
        *_project_dossier_items(project, pid),
        *_project_ledger_items(pid),
        *_project_job_items(jobs, pid, events_by_job_id),
    ]


def project_evidence_set(
    project: Any, *, token_cap: int = CHAT_EVIDENCE_TOKEN_CAP
) -> ChatEvidenceSet:
    """The composed project-scope evidence set for one registry project."""
    return compose_chat_evidence(
        CHAT_SCOPE_PROJECT, str(project.id), collect_project_evidence(project),
        token_cap=token_cap,
    )
