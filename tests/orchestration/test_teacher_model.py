"""The teacher's own model transport and the one row an answer costs (F255 T004).

Every test here injects the ``call`` seam or a FAKE ``ollama`` module, so NO test
opens a socket and none needs a running Ollama — which is the whole point of
DECISION F255 D8's injectable transport.

The load-bearing properties: a refusal is NEVER billed (no call happened, so a
row claiming one would be a fabrication), an answered question writes EXACTLY
one row through ``teacher_spend``, and an unreported usage figure lands as NULL
rather than as a zero.
"""

from __future__ import annotations

import sqlite3
import sys
import types

import pytest

from packages.orchestration import teacher_model
from packages.orchestration.role_config import RoleConfig
from packages.orchestration.teacher_model import (
    TEACHER_TRANSPORTS,
    TeacherAnswer,
    TeacherReply,
    TeacherTransportUnavailable,
    ask_teacher,
    ollama_teacher_call,
    resolve_teacher_transport,
)
from packages.orchestration.teacher_spend import TEACHER_ROLE, TeacherUsage

_EVENTS = [
    {"event": "job_created", "timestamp": "2026-08-21T00:00:01Z"},
    {"event": "task_run_started", "task_id": "t7", "timestamp": "2026-08-21T00:00:02Z"},
]


def _rows(ledger) -> list[dict]:
    """Every stored ledger row, read straight from SQLite."""
    conn = sqlite3.connect(ledger)
    try:
        conn.row_factory = sqlite3.Row
        return [dict(r) for r in conn.execute("SELECT * FROM calls ORDER BY call_id")]
    finally:
        conn.close()


class _RecordingTransport:
    """A fake ``call`` that answers offline and remembers what it was asked."""

    def __init__(self, reply: TeacherReply | None = None) -> None:
        self.reply = reply or TeacherReply(text="a plain answer", usage=TeacherUsage())
        self.prompts: list[str] = []
        self.models: list[str] = []

    def __call__(self, prompt: str, *, model: str) -> TeacherReply:
        self.prompts.append(prompt)
        self.models.append(model)
        return self.reply


def _fake_ollama_module(*, chat) -> types.ModuleType:
    """A stand-in for the ``ollama`` package whose Client never leaves the process."""
    module = types.ModuleType("ollama")

    class Client:
        def __init__(self, host=None):
            self.host = host

        def chat(self, **kwargs):
            return chat(**kwargs)

    module.Client = Client
    return module


class TestTheTransportSet:
    def test_the_teacher_can_call_ollama_and_nothing_else(self):
        # Narrow on purpose: ollama is the only transport this round BUILDS, and
        # a provider outside this tuple must be refused rather than mis-called.
        assert TEACHER_TRANSPORTS == ("ollama",)

    def test_the_default_configuration_resolves_to_a_usable_transport(self):
        resolved = resolve_teacher_transport()
        assert resolved is not None
        provider, model = resolved
        assert provider in TEACHER_TRANSPORTS
        assert model

    def test_a_provider_outside_the_set_resolves_to_no_transport(self):
        assert resolve_teacher_transport(config_file={"provider": "claude-cli"}) is None

    def test_a_configured_teacher_model_is_what_the_transport_reports(self):
        resolved = resolve_teacher_transport(
            config_file={"teacher": {"provider": "ollama", "model": "tutor-model"}}
        )
        assert resolved == ("ollama", "tutor-model")


class TestTheInjectedSeam:
    def test_the_default_transport_is_ollama_teacher_call_by_identity(self, tmp_path, monkeypatch):
        """The seam's default IS the module's own transport — and it is never called.

        The real :func:`ollama_teacher_call` would need a running Ollama, so the
        module attribute is replaced by a sentinel and the assertion is that the
        object which ran IS that attribute. ``ollama_teacher_call`` itself is
        only ever compared, never invoked.
        """
        sentinel = _RecordingTransport()
        monkeypatch.setattr(teacher_model, "ollama_teacher_call", sentinel)

        ask_teacher("what happened?", ledger_path=tmp_path / "ledger.sqlite")

        assert sentinel.prompts, "ask_teacher did not dispatch to the module's default"
        assert teacher_model.ollama_teacher_call is sentinel

    def test_the_prompt_the_seam_receives_is_the_rendered_grounded_prompt(self, tmp_path):
        transport = _RecordingTransport()

        ask_teacher(
            "why did task t7 start?",
            events=_EVENTS,
            call=transport,
            ledger_path=tmp_path / "ledger.sqlite",
        )

        prompt = transport.prompts[0]
        assert "why did task t7 start?" in prompt
        assert "[ledger]" in prompt and "[concept]" in prompt
        assert "Name the source you answer from." in prompt


class TestAnAnsweredQuestion:
    def test_one_question_writes_exactly_one_row_attributed_to_the_teacher(self, tmp_path):
        ledger = tmp_path / "ledger.sqlite"

        answer = ask_teacher("q", call=_RecordingTransport(), ledger_path=ledger)

        assert isinstance(answer, TeacherAnswer)
        assert answer.refused is False
        assert answer.billed is True
        assert answer.text == "a plain answer"
        rows = _rows(ledger)
        assert len(rows) == 1
        assert rows[0]["call_id"] == answer.call_id
        assert rows[0]["role"] == TEACHER_ROLE
        assert rows[0]["task_id"] is None

    def test_the_answer_names_the_resolved_model(self, tmp_path):
        transport = _RecordingTransport()

        answer = ask_teacher("q", call=transport, ledger_path=tmp_path / "ledger.sqlite")

        _, model = resolve_teacher_transport()
        assert answer.model == model
        assert transport.models == [model]

    def test_reported_usage_reaches_the_row_and_silence_stays_null(self, tmp_path):
        reported = tmp_path / "reported.sqlite"
        silent = tmp_path / "silent.sqlite"

        ask_teacher(
            "q",
            call=_RecordingTransport(
                TeacherReply(text="x", usage=TeacherUsage(tokens_in=11, tokens_out=4))
            ),
            ledger_path=reported,
        )
        ask_teacher("q", call=_RecordingTransport(), ledger_path=silent)

        assert (_rows(reported)[0]["tokens_in"], _rows(reported)[0]["tokens_out"]) == (11, 4)
        assert _rows(silent)[0]["tokens_in"] is None
        assert _rows(silent)[0]["tokens_out"] is None

    def test_the_job_id_is_carried_onto_the_row(self, tmp_path):
        ledger = tmp_path / "ledger.sqlite"

        ask_teacher("q", call=_RecordingTransport(), job_id="job-9", ledger_path=ledger)

        assert _rows(ledger)[0]["job_id"] == "job-9"


class TestARefusalIsNeverBilled:
    def test_no_usable_transport_refuses_and_writes_no_row(self, tmp_path, monkeypatch):
        ledger = tmp_path / "ledger.sqlite"
        monkeypatch.setattr(
            teacher_model,
            "resolve_role_config",
            lambda role, **kw: RoleConfig(role=role, provider="claude-cli", model="opus"),
        )

        answer = ask_teacher("q", call=_RecordingTransport(), ledger_path=ledger)

        assert answer.refused is True
        assert answer.call_id is None
        assert answer.billed is False
        assert "claude-cli" in answer.text and "opus" in answer.text
        # The refusal names Stage 1, because Stage 1 is offline by construction
        # and still works — the operator should be told what they still have.
        assert "remedy teach narrate" in answer.text
        assert not ledger.exists()

    def test_a_refusal_never_reaches_the_transport(self, tmp_path, monkeypatch):
        transport = _RecordingTransport()
        monkeypatch.setattr(
            teacher_model,
            "resolve_role_config",
            lambda role, **kw: RoleConfig(role=role, provider="fake", model="m"),
        )

        ask_teacher("q", call=transport, ledger_path=tmp_path / "ledger.sqlite")

        assert transport.prompts == []

    def test_an_unavailable_transport_refuses_and_writes_no_row(self, tmp_path):
        ledger = tmp_path / "ledger.sqlite"

        def failing(prompt, *, model):
            raise TeacherTransportUnavailable("the Ollama call failed: connection refused")

        answer = ask_teacher("q", call=failing, ledger_path=ledger)

        assert answer.refused is True
        assert answer.call_id is None
        assert answer.billed is False
        assert "connection refused" in answer.text
        assert not ledger.exists()

    def test_a_transport_failure_is_not_swallowed_into_a_plausible_answer(self, tmp_path):
        def failing(prompt, *, model):
            raise TeacherTransportUnavailable("dependency absent")

        answer = ask_teacher("q", call=failing, ledger_path=tmp_path / "ledger.sqlite")

        assert answer.text.startswith("I cannot answer that")


class TestTheOllamaTransport:
    """Exercised against a FAKE ``ollama`` module: no package, no server, no socket."""

    def test_a_missing_ollama_package_raises_transport_unavailable(self, monkeypatch):
        monkeypatch.setitem(sys.modules, "ollama", None)
        with pytest.raises(TeacherTransportUnavailable):
            ollama_teacher_call("prompt", model="m")

    def test_a_failing_call_raises_transport_unavailable(self, monkeypatch):
        def chat(**kwargs):
            raise RuntimeError("connection refused")

        monkeypatch.setitem(sys.modules, "ollama", _fake_ollama_module(chat=chat))
        with pytest.raises(TeacherTransportUnavailable):
            ollama_teacher_call("prompt", model="m")

    def test_the_call_carries_no_schema_because_a_tutor_answer_is_prose(self, monkeypatch):
        seen: dict = {}

        def chat(**kwargs):
            seen.update(kwargs)
            return {"message": {"content": "hello"}}

        monkeypatch.setitem(sys.modules, "ollama", _fake_ollama_module(chat=chat))
        reply = ollama_teacher_call("prompt", model="tutor-model")

        assert reply.text == "hello"
        assert "format" not in seen
        assert seen["model"] == "tutor-model"
        assert seen["messages"] == [{"role": "user", "content": "prompt"}]

    def test_reported_counts_are_read_and_unreported_ones_stay_null(self, monkeypatch):
        def with_counts(**kwargs):
            return {"message": {"content": "hi"}, "prompt_eval_count": 7, "eval_count": 2}

        monkeypatch.setitem(sys.modules, "ollama", _fake_ollama_module(chat=with_counts))
        assert ollama_teacher_call("p", model="m").usage == TeacherUsage(tokens_in=7, tokens_out=2)

        def without_counts(**kwargs):
            return {"message": {"content": "hi"}}

        monkeypatch.setitem(sys.modules, "ollama", _fake_ollama_module(chat=without_counts))
        # NULL, never 0: a fabricated zero sums where an honest unknown does not.
        assert ollama_teacher_call("p", model="m").usage == TeacherUsage()
