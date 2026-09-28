"""F038 T003 — `run_chat_turn`: a line becomes a grounded answer or an action card, through
one module both doors call (DECISION F038 D9). No test here reaches a real model: a call
function that must not be called raises `AssertionError`, and a model reply is a stub
returning fixed JSON.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from packages.orchestration import chat_turn
from packages.orchestration.chat_answer import CHAT_NOT_IN_EVIDENCE
from packages.orchestration.chat_evidence import CHAT_SCOPE_NODE
from packages.orchestration.chat_intent import CHAT_INTENT_ACTION, ChatIntent
from packages.orchestration.chat_turn import (
    CHAT_TURN_ANSWER,
    CHAT_TURN_CARD,
    ChatTurnError,
    chat_open_decision_ids,
    run_chat_turn,
)
from packages.orchestration.escalation import answer_task_decision, enqueue_task_decision
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan


@pytest.fixture(autouse=True)
def _isolated_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))


def _never_called(prompt: str, attempt: int) -> str:
    raise AssertionError("this call function must never be called")


def _stub_call_fn(response_text: str):
    """A call function that never reaches a model: returns `response_text` and records
    every prompt it was asked, mirroring test_chat_intent_model.py's own copy."""
    prompts: list[str] = []

    def _call(prompt: str, attempt: int) -> str:
        prompts.append(prompt)
        return response_text

    _call.prompts = prompts
    return _call


def _reply(verb: str, args: dict[str, str], confidence: float) -> str:
    return json.dumps({"verb": verb, "args": args, "confidence": confidence})


def _make_job() -> tuple[JobPlan, str]:
    """A saved job with one done, passing task, carrying the minted default id."""
    task = TaskEntry(title="Write the README", status="done", test_passed=True)
    job = JobPlan(
        job_title="f038-chat-turn-job", tasks=[task],
        metadata={"target_repo": "/tmp/repo"},
    )
    save_job_plan(job)
    return job, task.task_id


# ---------------------------------------------------------------------------
# A mechanical hit never touches a model.
# ---------------------------------------------------------------------------


def test_pause_is_a_card_with_no_answer_and_no_evidence_the_stub_never_called():
    job, _task_id = _make_job()

    turn = run_chat_turn(job, "pause", intent_call_fn=_never_called, answer_call_fn=_never_called)

    assert turn.kind == CHAT_TURN_CARD
    assert turn.card.verb == "job.pause"
    assert turn.answer is None
    assert turn.evidence is None


def test_an_unrecognized_action_with_intent_call_fn_none_is_the_unknown_card():
    job, _task_id = _make_job()

    turn = run_chat_turn(job, "deploy it", intent_call_fn=None, answer_call_fn=_never_called)

    assert turn.kind == CHAT_TURN_CARD
    assert turn.card.confirmable is False


# ---------------------------------------------------------------------------
# A question, focused and unfocused.
# ---------------------------------------------------------------------------


def test_a_focused_question_is_answered_from_the_node_scope():
    job, task_id = _make_job()

    turn = run_chat_turn(
        job, "Did the tests pass?", task_id=task_id,
        intent_call_fn=_never_called, answer_call_fn=None)

    assert turn.kind == CHAT_TURN_ANSWER
    assert turn.answer.scope == CHAT_SCOPE_NODE
    assert turn.answer.subject == task_id


def test_an_unfocused_question_with_no_registered_project_is_not_in_evidence():
    job, _task_id = _make_job()

    turn = run_chat_turn(
        job, "What is the roadmap position?",
        intent_call_fn=_never_called, answer_call_fn=None)

    assert turn.kind == CHAT_TURN_ANSWER
    assert turn.evidence.items == ()
    assert len(turn.answer.sentences) == 1
    assert turn.answer.sentences[0].text == CHAT_NOT_IN_EVIDENCE


# ---------------------------------------------------------------------------
# The focused task id must name a real task of the job.
# ---------------------------------------------------------------------------


def test_a_task_id_naming_no_task_of_the_job_raises():
    job, _task_id = _make_job()

    with pytest.raises(ChatTurnError, match="task_id"):
        run_chat_turn(job, "pause", task_id="0123456789abcdef")


# ---------------------------------------------------------------------------
# The open decisions the inbox would let `decision.resolve` answer.
# ---------------------------------------------------------------------------


def test_an_open_task_decision_is_listed_then_cleared_once_answered():
    job, task_id = _make_job()
    now = datetime.now(timezone.utc)
    record = enqueue_task_decision(job, task_id=task_id, question="Which database?", now=now)

    assert chat_open_decision_ids(job) == (record["decision_id"],)

    answer_task_decision(job, record["decision_id"], answer="postgres", now=now)

    assert chat_open_decision_ids(job) == ()


def test_an_open_decision_resolve_reply_gives_a_confirmable_card():
    job, task_id = _make_job()
    now = datetime.now(timezone.utc)
    record = enqueue_task_decision(job, task_id=task_id, question="Which database?", now=now)
    call_fn = _stub_call_fn(_reply(
        "decision.resolve", {"decision_id": record["decision_id"], "answer": "postgres"}, 0.9))

    turn = run_chat_turn(
        job, "use postgres for the decision",
        intent_call_fn=call_fn, answer_call_fn=_never_called)

    assert turn.kind == CHAT_TURN_CARD
    assert turn.card.confirmable is True
    assert turn.card.args == {"decision_id": record["decision_id"], "answer": "postgres"}


def test_the_intent_parse_receives_exactly_the_open_decision_ids(monkeypatch):
    job, task_id = _make_job()
    now = datetime.now(timezone.utc)
    enqueue_task_decision(job, task_id=task_id, question="Which database?", now=now)

    received: list[tuple[str, ...]] = []

    def _recorder(text, *, focused_task_id="", open_decision_ids=(), **_kwargs):
        received.append(tuple(open_decision_ids))
        return ChatIntent(kind=CHAT_INTENT_ACTION, verb="job.pause", args={}, missing=())

    monkeypatch.setattr(chat_turn, "parse_chat_intent_with_model", _recorder)

    run_chat_turn(job, "pause")

    assert received == [chat_open_decision_ids(job)]
