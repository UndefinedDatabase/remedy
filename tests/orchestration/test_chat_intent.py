"""F038 T002 — the chat's mechanical intent parse: the question/action/unknown split, the
action card and the write door's request body, none of it sending, writing or calling a
model (DECISION F038 D6).
"""

from __future__ import annotations

import pytest

from apps.cli.command_catalog import UI_EXPOSED_COMMANDS
from packages.orchestration.chat_intent import (
    CHAT_AVAILABLE_ACTIONS,
    CHAT_INTENT_ACTION,
    CHAT_INTENT_QUESTION,
    CHAT_INTENT_UNKNOWN,
    CHAT_UNKNOWN_TITLE,
    CHAT_VERB_REQUIRED_ARGS,
    CHAT_VERB_TITLES,
    ChatIntentError,
    build_action_card,
    card_command_payload,
    parse_chat_intent,
)


@pytest.fixture(autouse=True)
def _isolated_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))


# ---------------------------------------------------------------------------
# S1 — the verb tables agree with the door's own catalog.
# ---------------------------------------------------------------------------

def test_every_verb_is_an_exposed_command():
    for verb in CHAT_VERB_REQUIRED_ARGS:
        assert verb in UI_EXPOSED_COMMANDS, verb


def test_verb_titles_cover_the_same_keys():
    assert set(CHAT_VERB_TITLES) == set(CHAT_VERB_REQUIRED_ARGS)


# ---------------------------------------------------------------------------
# S3 — questions.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("text", [
    "What changed?", "did the tests pass", "Can you stop it?", "  why  ", "stop it?",
])
def test_question_texts_are_questions(text):
    intent = parse_chat_intent(text)
    assert intent.kind == CHAT_INTENT_QUESTION
    assert intent.verb == ""


# ---------------------------------------------------------------------------
# S3 — job.stop, job.pause, job.unpause.
# ---------------------------------------------------------------------------

def test_stop_because_carries_its_reason():
    intent = parse_chat_intent("Stop the job because it loops")
    assert intent.kind == CHAT_INTENT_ACTION
    assert intent.verb == "job.stop"
    assert intent.args == {"reason": "it loops"}
    assert intent.missing == ()


def test_please_cancel_is_stop_with_no_args():
    intent = parse_chat_intent("please cancel")
    assert intent.verb == "job.stop"
    assert intent.args == {}
    assert intent.missing == ()


def test_pause_is_job_pause():
    intent = parse_chat_intent("Pause")
    assert intent.verb == "job.pause"
    assert intent.args == {}
    assert intent.missing == ()


@pytest.mark.parametrize("text", ["resume", "Unpause now", "continue"])
def test_resume_words_are_job_unpause(text):
    intent = parse_chat_intent(text)
    assert intent.verb == "job.unpause"
    assert intent.args == {}
    assert intent.missing == ()


# ---------------------------------------------------------------------------
# S3 — the note, task-focused vs job-wide.
# ---------------------------------------------------------------------------

def test_tell_the_builder_with_focus_is_steer():
    intent = parse_chat_intent("Tell the builder: use the New API", focused_task_id="abc")
    assert intent.verb == "job.steer"
    assert intent.args == {"task_id": "abc", "message": "use the New API"}
    assert intent.missing == ()


def test_note_without_focus_is_chat_send():
    intent = parse_chat_intent("note: keep it small")
    assert intent.verb == "chat.send"
    assert intent.args == {"message": "keep it small"}
    assert intent.missing == ()


def test_tell_it_with_no_message_misses_message():
    intent = parse_chat_intent("tell it")
    assert intent.verb == "chat.send"
    assert intent.args == {}
    assert intent.missing == ("message",)


# ---------------------------------------------------------------------------
# S3 — job.veto-task.
# ---------------------------------------------------------------------------

def test_veto_because_with_focus_is_complete():
    intent = parse_chat_intent(
        "Veto this because it is out of scope", focused_task_id="abc")
    assert intent.verb == "job.veto-task"
    assert intent.args == {"task_id": "abc", "reason": "it is out of scope"}
    assert intent.missing == ()


def test_skip_with_focus_misses_reason():
    intent = parse_chat_intent("skip this task", focused_task_id="abc")
    assert intent.verb == "job.veto-task"
    assert intent.args == {"task_id": "abc"}
    assert intent.missing == ("reason",)


def test_veto_without_focus_misses_both():
    intent = parse_chat_intent("veto it")
    assert intent.verb == "job.veto-task"
    assert intent.args == {}
    assert intent.missing == ("task_id", "reason")


# ---------------------------------------------------------------------------
# S3 — job.rerun-subtree.
# ---------------------------------------------------------------------------

def test_rerun_with_focus_is_complete():
    intent = parse_chat_intent("rerun", focused_task_id="abc")
    assert intent.verb == "job.rerun-subtree"
    assert intent.args == {"task_id": "abc"}
    assert intent.missing == ()


def test_run_again_without_focus_misses_task_id():
    intent = parse_chat_intent("Run again")
    assert intent.verb == "job.rerun-subtree"
    assert intent.args == {}
    assert intent.missing == ("task_id",)


# ---------------------------------------------------------------------------
# S3 — unknown.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("text", ["deploy to production", "", "   "])
def test_unrecognised_texts_are_unknown(text):
    intent = parse_chat_intent(text)
    assert intent.kind == CHAT_INTENT_UNKNOWN
    assert intent.verb == ""


# ---------------------------------------------------------------------------
# S4 — the card.
# ---------------------------------------------------------------------------

def test_note_card_lines_and_confirmable():
    intent = parse_chat_intent("Tell the builder: use X", focused_task_id="abc")
    card = build_action_card(intent, job_id="J1")
    assert card.lines == ("Job: J1", "Task: abc", "Message: use X", "Command: job.steer")
    assert card.confirmable is True


def test_focused_veto_card_lines_and_not_confirmable():
    intent = parse_chat_intent("skip this task", focused_task_id="abc")
    card = build_action_card(intent, job_id="J1")
    assert card.lines == (
        "Job: J1", "Task: abc", "Needs: reason. Say it again with them.",
        "Command: job.veto-task")
    assert card.confirmable is False


def test_unknown_card_titled_and_lined_as_s4_states():
    intent = parse_chat_intent("deploy to production")
    card = build_action_card(intent, job_id="J1")
    assert card.verb == ""
    assert card.title == CHAT_UNKNOWN_TITLE
    assert card.lines == (f"Available: {', '.join(CHAT_AVAILABLE_ACTIONS)}.",)
    assert card.args == {}
    assert card.missing == ()
    assert card.confirmable is False


def test_question_card_raises():
    intent = parse_chat_intent("What changed?")
    with pytest.raises(ChatIntentError, match="read path"):
        build_action_card(intent, job_id="J1")


# ---------------------------------------------------------------------------
# S5 — the payload.
# ---------------------------------------------------------------------------

def test_stop_card_payload_is_exact():
    intent = parse_chat_intent("stop because done")
    card = build_action_card(intent, job_id="J1")
    payload = card_command_payload(card, client_nonce="chat-1")
    assert payload == {
        "command": "job.stop", "client_nonce": "chat-1", "args": {"reason": "done"}}


def test_bad_nonce_raises():
    intent = parse_chat_intent("stop because done")
    card = build_action_card(intent, job_id="J1")
    with pytest.raises(ChatIntentError, match="client_nonce"):
        card_command_payload(card, client_nonce="")


def test_incomplete_card_raises_no_command():
    intent = parse_chat_intent("veto it")
    card = build_action_card(intent, job_id="J1")
    with pytest.raises(ChatIntentError, match="no command"):
        card_command_payload(card, client_nonce="chat-1")


def test_unknown_card_raises_no_command():
    intent = parse_chat_intent("deploy to production")
    card = build_action_card(intent, job_id="J1")
    with pytest.raises(ChatIntentError, match="no command"):
        card_command_payload(card, client_nonce="chat-1")


# ---------------------------------------------------------------------------
# Purity — nothing under tmp_path is ever written.
# ---------------------------------------------------------------------------

def test_parsing_and_building_cards_writes_no_file(tmp_path):
    intent = parse_chat_intent("Stop the job because it loops")
    card = build_action_card(intent, job_id="J1")
    card_command_payload(card, client_nonce="chat-1")
    parse_chat_intent("note: keep it small")
    build_action_card(parse_chat_intent("deploy to production"), job_id="J1")
    assert list(tmp_path.rglob("*")) == []
