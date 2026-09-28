"""F038 T002 — the model-written intent parse: the mechanical parse first, the reply's
verb, arguments and confidence filtered, grounded and checked, and the switch that keeps
it off by default (DECISION F038 D8).
"""

from __future__ import annotations

import json

import pytest

from apps.cli.command_catalog import UI_EXPOSED_COMMANDS
from packages.orchestration import chat_intent
from packages.orchestration.chat_intent_model import (
    CHAT_VERB_OPTIONAL_ARGS,
    GeneratedChatIntent,
    build_intent_prompt,
    parse_chat_intent_with_model,
)


@pytest.fixture(autouse=True)
def _isolated_data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))


def _stub_call_fn(response_text: str):
    """A call function that never reaches a model: it returns `response_text` and
    records every prompt it was asked, mirroring test_chat_answer.py's `_stub_call_fn`."""
    prompts: list[str] = []

    def _call(prompt: str, attempt: int) -> str:
        prompts.append(prompt)
        return response_text

    _call.prompts = prompts
    return _call


def _reply(verb: str, args: dict[str, str], confidence: float) -> str:
    return json.dumps({"verb": verb, "args": args, "confidence": confidence})


# ---------------------------------------------------------------------------
# The verb tables agree with the door's own catalog.
# ---------------------------------------------------------------------------


def test_every_verb_is_an_exposed_command_and_optional_keys_are_required_keys():
    for verb in chat_intent.CHAT_VERB_REQUIRED_ARGS:
        assert verb in UI_EXPOSED_COMMANDS, verb
    for verb in CHAT_VERB_OPTIONAL_ARGS:
        assert verb in chat_intent.CHAT_VERB_REQUIRED_ARGS, verb


# ---------------------------------------------------------------------------
# The mechanical parse first — anything but unknown, the model is never asked.
# ---------------------------------------------------------------------------


def test_mechanical_hits_come_back_as_the_mechanical_parse_gives_them():
    call_fn = _stub_call_fn(_reply("job.pause", {}, 0.99))

    pause = parse_chat_intent_with_model("pause", call_fn=call_fn)
    question = parse_chat_intent_with_model("what changed?", call_fn=call_fn)

    assert pause == chat_intent.parse_chat_intent("pause")
    assert question == chat_intent.parse_chat_intent("what changed?")
    assert call_fn.prompts == []


# ---------------------------------------------------------------------------
# The reply's confidence.
# ---------------------------------------------------------------------------


def test_a_high_confidence_reply_is_kept_after_exactly_one_call():
    call_fn = _stub_call_fn(_reply("job.pause", {}, 0.9))

    intent = parse_chat_intent_with_model("hold on a moment", call_fn=call_fn)

    assert intent.kind == chat_intent.CHAT_INTENT_ACTION
    assert intent.verb == "job.pause"
    assert intent.missing == ()
    assert len(call_fn.prompts) == 1


def test_a_low_confidence_reply_is_unknown():
    call_fn = _stub_call_fn(_reply("job.pause", {}, 0.5))

    intent = parse_chat_intent_with_model("hold on a moment", call_fn=call_fn)

    assert intent.kind == chat_intent.CHAT_INTENT_UNKNOWN


def test_a_reply_naming_a_verb_outside_the_chat_tables_is_unknown():
    call_fn = _stub_call_fn(_reply("job.plan-delete-task", {}, 0.99))

    intent = parse_chat_intent_with_model("make the plan lose that task", call_fn=call_fn)

    assert intent.kind == chat_intent.CHAT_INTENT_UNKNOWN


# ---------------------------------------------------------------------------
# Grounding — decision.resolve.
# ---------------------------------------------------------------------------


def test_decision_id_outside_the_open_set_comes_back_missing_it():
    call_fn = _stub_call_fn(
        _reply("decision.resolve", {"decision_id": "D-9", "answer": "yes"}, 0.9))

    intent = parse_chat_intent_with_model(
        "answer the decision with yes", call_fn=call_fn, open_decision_ids=("D-1",))

    assert intent.verb == "decision.resolve"
    assert intent.args == {"answer": "yes"}
    assert intent.missing == ("decision_id",)


def test_decision_id_in_the_open_set_is_complete_and_confirmable():
    call_fn = _stub_call_fn(
        _reply("decision.resolve", {"decision_id": "D-1", "answer": "yes"}, 0.9))

    intent = parse_chat_intent_with_model(
        "answer the decision with yes", call_fn=call_fn, open_decision_ids=("D-1",))
    card = chat_intent.build_action_card(intent, job_id="J1")

    assert card.lines == ("Job: J1", "Decision: D-1", "Answer: yes", "Command: decision.resolve")
    assert card.confirmable is True


# ---------------------------------------------------------------------------
# Grounding — the task id is always the focused task.
# ---------------------------------------------------------------------------


def test_task_id_is_always_the_focused_task_whatever_the_reply_said():
    call_fn = _stub_call_fn(
        _reply("job.veto-task", {"task_id": "zzz", "reason": "out of scope"}, 0.9))

    intent = parse_chat_intent_with_model(
        "get rid of the task, it is wrong", call_fn=call_fn, focused_task_id="abc")
    assert intent.args["task_id"] == "abc"
    assert intent.missing == ()

    intent_no_focus = parse_chat_intent_with_model(
        "get rid of the task, it is wrong", call_fn=call_fn)
    assert "task_id" in intent_no_focus.missing


# ---------------------------------------------------------------------------
# Grounding — only the verb's own argument names survive.
# ---------------------------------------------------------------------------


def test_job_inject_keeps_only_its_own_argument_names():
    call_fn = _stub_call_fn(_reply(
        "job.inject",
        {"text": "write docs", "after": "T1", "priority": "high"},
        0.9,
    ))

    intent = parse_chat_intent_with_model(
        "add a task to write docs after T1", call_fn=call_fn)
    card = chat_intent.build_action_card(intent, job_id="J1")

    assert intent.args == {"text": "write docs", "after": "T1"}
    assert card.lines == ("Job: J1", "Text: write docs", "After: T1", "Command: job.inject")


# ---------------------------------------------------------------------------
# An unusable reply.
# ---------------------------------------------------------------------------


def test_a_reply_that_is_not_json_is_unknown():
    call_fn = _stub_call_fn("not json at all")

    intent = parse_chat_intent_with_model("make the unusual thing happen", call_fn=call_fn)

    assert intent.kind == chat_intent.CHAT_INTENT_UNKNOWN


def test_a_reply_whose_verb_is_not_a_string_is_unknown():
    call_fn = _stub_call_fn(json.dumps({"verb": 5, "args": {}, "confidence": 0.9}))

    intent = parse_chat_intent_with_model("make the unusual thing happen", call_fn=call_fn)

    assert intent.kind == chat_intent.CHAT_INTENT_UNKNOWN


def test_a_call_function_raising_connection_error_is_unknown():
    def _raise(prompt: str, attempt: int) -> str:
        raise ConnectionError("boom")

    intent = parse_chat_intent_with_model("make the unusual thing happen", call_fn=_raise)

    assert intent.kind == chat_intent.CHAT_INTENT_UNKNOWN


# ---------------------------------------------------------------------------
# The switch.
# ---------------------------------------------------------------------------


def test_unset_call_function_asks_chat_call_fn_only_when_the_switch_is_on(monkeypatch):
    import packages.orchestration.chat_intent_model as chat_intent_model_module
    from packages.orchestration.config import reset_config

    calls: list[object] = []

    def spy(schema):
        calls.append(schema)
        return None

    monkeypatch.setattr(chat_intent_model_module, "chat_call_fn", spy)

    parse_chat_intent_with_model("make the unusual thing happen")
    assert calls == []

    monkeypatch.setenv("REMEDY_CHAT_MODEL_WRITTEN", "1")
    reset_config()

    parse_chat_intent_with_model("make the unusual thing happen")
    assert calls == [GeneratedChatIntent]

    monkeypatch.delenv("REMEDY_CHAT_MODEL_WRITTEN")
    reset_config()


# ---------------------------------------------------------------------------
# The prompt.
# ---------------------------------------------------------------------------


def test_prompt_names_every_verb_the_focused_task_and_the_open_decisions():
    prompt = build_intent_prompt(
        "do something", focused_task_id="abc", open_decision_ids=("D-1", "D-2"))

    for verb in chat_intent.CHAT_VERB_REQUIRED_ARGS:
        assert verb in prompt
    assert "abc" in prompt
    assert "D-1, D-2" in prompt
