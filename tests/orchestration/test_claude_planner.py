"""amend0920-selfuse-real Part A — the Claude CLI planner, driven by a fake subprocess.

Covers the three properties the amendment names for
``packages/providers/claude_planner/provider.py``: a fenced reply is stripped
and accepted, one bad reply is retried exactly once, and a second bad reply
raises the same exception class ``OllamaPlanner.plan`` documents. Every test
drives the ONE spawn point the planner shares with the ping-pong provider,
``pingpong_provider._guarded_cli_run``, so the route itself is under test and
not merely the parsing.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest
from pydantic import ValidationError

from packages.orchestration import pingpong_provider
from packages.providers.claude_planner.provider import ClaudeCliPlanner

_PLAN_OBJECT = {
    "summary": "Two tasks.",
    "proposed_tasks": [
        {"task_type": "write_tests", "description": "Add the failing test."},
        {"task_type": "implement_feature", "description": "Make it pass."},
    ],
    "acceptance_checks": [],
    "notes": [],
}


class _FakeCli:
    """A scripted ``claude -p``: one canned stdout per call, argv recorded."""

    def __init__(self, *replies: str, returncode: int = 0) -> None:
        self._replies = list(replies)
        self._returncode = returncode
        self.calls: list[list[str]] = []

    def __call__(self, cmd, timeout_sec, cwd):  # noqa: ANN001 - mirrors _guarded_cli_run
        self.calls.append(list(cmd))
        reply = self._replies.pop(0) if self._replies else ""
        envelope = json.dumps({"result": reply})
        return subprocess.CompletedProcess(cmd, self._returncode, envelope, "")


@pytest.fixture
def cli(monkeypatch):
    """Put a `claude` binary on PATH and hand back a spawn-point installer."""
    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")

    def install(*replies: str, returncode: int = 0) -> _FakeCli:
        fake = _FakeCli(*replies, returncode=returncode)
        monkeypatch.setattr(pingpong_provider, "_guarded_cli_run", fake)
        return fake

    return install


class TestFenceStripping:

    def test_a_fenced_reply_is_accepted(self, cli):
        fenced = "```json\n" + json.dumps(_PLAN_OBJECT) + "\n```"
        fake = cli(fenced)
        out = ClaudeCliPlanner().plan("build a summariser")
        assert out.summary == "Two tasks."
        assert [t.task_type for t in out.proposed_tasks] == [
            "write_tests", "implement_feature",
        ]
        assert len(fake.calls) == 1, "a valid first reply must not be retried"

    def test_raw_call_returns_the_stripped_json_object(self, cli):
        cli("```\n{\"goal\": \"ship it\"}\n```")
        text = ClaudeCliPlanner().raw_call(
            "state the goal", schema={"type": "object", "required": ["goal"]},
        )
        assert json.loads(text) == {"goal": "ship it"}

    def test_the_schema_and_the_one_object_rule_are_in_the_prompt(self, cli):
        fake = cli(json.dumps(_PLAN_OBJECT))
        ClaudeCliPlanner().plan("build a summariser")
        prompt = fake.calls[0][fake.calls[0].index("-p") + 1]
        assert "Answer with one JSON object and nothing else." in prompt
        assert "proposed_tasks" in prompt, "the schema itself must be stated"

    def test_the_model_reaches_the_command_line(self, cli):
        fake = cli(json.dumps(_PLAN_OBJECT))
        ClaudeCliPlanner(model="claude-test-model").plan("build a summariser")
        argv = fake.calls[0]
        assert argv[argv.index("--model") + 1] == "claude-test-model"

    def test_the_default_model_is_the_sonnet_alias(self, monkeypatch):
        from packages.orchestration.model_aliases import resolve_model_alias

        monkeypatch.delenv("REMEDY_CLAUDE_PLANNER_MODEL", raising=False)
        assert ClaudeCliPlanner().model == resolve_model_alias("claude-workhorse")


class TestExactlyOneRetry:

    def test_a_bad_first_reply_is_retried_once_and_the_second_wins(self, cli):
        fake = cli("I cannot answer that.", json.dumps(_PLAN_OBJECT))
        out = ClaudeCliPlanner().plan("build a summariser")
        assert out.summary == "Two tasks."
        assert len(fake.calls) == 2, "exactly one retry"

    def test_the_retry_names_what_was_wrong_with_the_first_reply(self, cli):
        fake = cli(json.dumps({"summary": "no tasks"}), json.dumps(_PLAN_OBJECT))
        ClaudeCliPlanner().plan("build a summariser")
        retry_prompt = fake.calls[1][fake.calls[1].index("-p") + 1]
        assert "Your previous response was invalid:" in retry_prompt
        assert "proposed_tasks" in retry_prompt

    def test_a_schema_incomplete_reply_is_retried_on_raw_call_too(self, cli):
        fake = cli(json.dumps({"other": 1}), json.dumps({"goal": "ship it"}))
        text = ClaudeCliPlanner().raw_call(
            "state the goal", schema={"type": "object", "required": ["goal"]},
        )
        assert json.loads(text) == {"goal": "ship it"}
        assert len(fake.calls) == 2


class TestFailureAfterTheSecondBadReply:

    def test_two_unparsable_replies_raise_validation_error(self, cli):
        fake = cli("nope", "still nope")
        with pytest.raises(ValidationError):
            ClaudeCliPlanner().plan("build a summariser")
        assert len(fake.calls) == 2, "never a third attempt"

    def test_two_schema_incomplete_replies_raise_validation_error(self, cli):
        fake = cli(json.dumps({"summary": "a"}), json.dumps({"summary": "b"}))
        with pytest.raises(ValidationError):
            ClaudeCliPlanner().plan("build a summariser")
        assert len(fake.calls) == 2

    def test_raw_call_raises_the_same_class(self, cli):
        cli("nope", "still nope")
        with pytest.raises(ValidationError):
            ClaudeCliPlanner().raw_call(
                "state the goal", schema={"type": "object", "required": ["goal"]},
            )

    def test_the_ollama_planner_raises_that_very_class_for_a_schema_failure(self):
        """The exception class is SHARED, not merely similar (the amendment's word)."""
        from packages.orchestration.planner_models import PlannerOutput

        with pytest.raises(ValidationError):
            PlannerOutput.model_validate_json(json.dumps({"summary": "no tasks"}))


class TestTheSurfaceMatchesTheOllamaPlanner:

    def test_the_same_three_methods_with_the_same_signatures(self):
        import inspect

        from packages.providers.ollama_planner.provider import OllamaPlanner

        for name in ("plan", "raw_call", "plan_raw"):
            ours = inspect.signature(getattr(ClaudeCliPlanner, name))
            theirs = inspect.signature(getattr(OllamaPlanner, name))
            assert ours == theirs, f"{name} must match the Ollama planner"


class TestTheCliFailuresStaySeparateFromSchemaFailures:

    def test_a_missing_cli_is_a_runtime_error(self, monkeypatch):
        monkeypatch.setattr(shutil, "which", lambda name: None)
        with pytest.raises(RuntimeError, match="claude CLI not found"):
            ClaudeCliPlanner().plan("build a summariser")

    def test_a_non_zero_exit_is_a_runtime_error(self, cli):
        cli(json.dumps(_PLAN_OBJECT), returncode=3)
        with pytest.raises(RuntimeError, match="exited 3"):
            ClaudeCliPlanner().plan("build a summariser")
