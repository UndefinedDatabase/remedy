"""F038 T003 — one chat turn: a line becomes a grounded answer or an action card, through one
module both doors call (DECISION F038 D9).

Remedy deliberately does not let a chat turn send anything: confirming a card is its caller's
step.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from packages.orchestration.chat_answer import ChatAnswer, answer_chat_question
from packages.orchestration.chat_evidence import (
    CHAT_SCOPE_PROJECT,
    ChatEvidenceSet,
    compose_chat_evidence,
    node_evidence_set,
    project_evidence_set,
)
from packages.orchestration.chat_intent import (
    CHAT_INTENT_QUESTION,
    ChatActionCard,
    build_action_card,
)
from packages.orchestration.chat_intent_model import parse_chat_intent_with_model

#: The two shapes :func:`run_chat_turn` returns.
CHAT_TURN_ANSWER = "answer"
CHAT_TURN_CARD = "card"


class ChatTurnError(ValueError):
    """Raised for a turn this module refuses: a focused task id naming no task of the job."""


@dataclass(frozen=True)
class ChatTurn:
    """One chat turn's result: an ANSWER with the evidence it was answered from, or a CARD."""

    kind: str
    evidence: ChatEvidenceSet | None = None
    answer: ChatAnswer | None = None
    card: ChatActionCard | None = None


#: `run_chat_turn`'s own sentinel, meaning unset for both `intent_call_fn` and
#: `answer_call_fn`: distinguishes "no call_fn argument was given" (let
#: `parse_chat_intent_with_model` / `answer_chat_question` decide from their own switches)
#: from "call_fn=None was given" (used as given). A bare `None` default cannot tell those
#: apart, mirroring `chat_answer._UNSET_CALL_FN` and `chat_intent_model._UNSET_CALL_FN`.
_UNSET_CALL_FN = object()


def chat_open_decision_ids(job: Any) -> tuple[str, ...]:
    """The id of every decision card of `job`'s inbox the write door would accept an answer
    to (DECISION F038 D9 (2)), in the inbox's own order."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.decision_inbox import build_decision_inbox
    from packages.orchestration.timeline import load_run_events

    events = load_run_events(resolve_data_root(), job.job_id)
    inbox = build_decision_inbox(job, events)
    return tuple(
        card["id"] for card in inbox["decisions"] if card.get("answerable_by_decision_resolve")
    )


def chat_project_for_job(job: Any) -> Any | None:
    """The registered project owning `job`'s repository, or None when `job.repo_path` is
    empty or no project owns it."""
    if not job.repo_path:
        return None
    from packages.orchestration.project_registry import find_project_by_repo

    return find_project_by_repo(os.path.realpath(job.repo_path))


def run_chat_turn(
    job: Any,
    text: str,
    *,
    task_id: str = "",
    intent_call_fn: Callable[[str, int], str] | None = _UNSET_CALL_FN,
    answer_call_fn: Callable[[str, int], str] | None = _UNSET_CALL_FN,
) -> ChatTurn:
    """Answer `text` from `job`'s evidence, or turn it into an action card.

    A non-empty `task_id` naming no task of `job` is refused with :class:`ChatTurnError`
    before anything else is read. Otherwise the intent is read with the model-written parse,
    grounded against the job's own open decisions; anything but a QUESTION becomes a card.
    A QUESTION is answered from the focused task's own evidence, or from the project owning
    the job's repository, or from an empty evidence set when no project owns it.
    """
    if task_id and task_id not in {str(task.task_id) for task in job.tasks}:
        raise ChatTurnError(f"task_id {task_id!r} does not name a task of job {job.job_id}")

    intent_kwargs: dict[str, Any] = {}
    if intent_call_fn is not _UNSET_CALL_FN:
        intent_kwargs["call_fn"] = intent_call_fn
    intent = parse_chat_intent_with_model(
        text,
        focused_task_id=task_id,
        open_decision_ids=chat_open_decision_ids(job),
        **intent_kwargs,
    )

    if intent.kind != CHAT_INTENT_QUESTION:
        return ChatTurn(
            kind=CHAT_TURN_CARD, card=build_action_card(intent, job_id=str(job.job_id))
        )

    if task_id:
        evidence = node_evidence_set(job, task_id)
    else:
        project = chat_project_for_job(job)
        evidence = (
            project_evidence_set(project)
            if project is not None
            else compose_chat_evidence(CHAT_SCOPE_PROJECT, "", [])
        )

    answer_kwargs: dict[str, Any] = {}
    if answer_call_fn is not _UNSET_CALL_FN:
        answer_kwargs["call_fn"] = answer_call_fn
    answer = answer_chat_question(text, evidence, **answer_kwargs)
    return ChatTurn(kind=CHAT_TURN_ANSWER, evidence=evidence, answer=answer)


def chat_turn_view(turn: ChatTurn) -> dict[str, Any]:
    """The one wire shape a turn gives both doors (DECISION F038 D11): an ANSWER's scope,
    subject, question, generator, checked sentences and numbered evidence, or a CARD's
    verb, title, lines, arguments, what is still missing and whether it is confirmable."""
    if turn.kind == CHAT_TURN_ANSWER:
        answer = turn.answer
        evidence = turn.evidence
        return {
            "kind": CHAT_TURN_ANSWER,
            "scope": answer.scope,
            "subject": answer.subject,
            "question": answer.question,
            "generator": answer.generator,
            "sentences": [
                {"text": sentence.text, "citations": list(sentence.citations),
                 "supported": sentence.supported, "problem": sentence.problem}
                for sentence in answer.sentences
            ],
            "evidence": [
                {"number": number, "kind": item.kind, "ref": item.ref, "text": item.text}
                for number, item in enumerate(evidence.items, start=1)
            ],
            "omitted": evidence.omitted,
        }
    card = turn.card
    return {
        "kind": CHAT_TURN_CARD,
        "verb": card.verb,
        "title": card.title,
        "lines": list(card.lines),
        "args": dict(card.args),
        "missing": list(card.missing),
        "confirmable": card.confirmable,
    }
