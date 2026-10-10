"""The claude-cli worker's command line starts lean (F302 T003, DECISION F302 D2).

`claude_cli_launch_switches` answers `--safe-mode` unless `claude_cli.customizations` is true, and
`--tools` naming the role's tools unless `claude_cli.all_tools` is true; `build_claude_cli_args`
ends every command line with them, so every worker call — builder, reviewer, planner — carries
them. No real `claude` process runs here: the provider's calls patch
`packages.orchestration.pingpong_provider._guarded_cli_run`, and every configuration is a stand-in
passed in or put in place of `get_config`, never the operator's own files.
"""
from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from packages.orchestration import config as config_module
from packages.orchestration import pingpong_provider
from packages.orchestration.claude_cli_command import (
    _READER_TOOLS,
    _WRITER_TOOLS,
    build_claude_cli_args,
    claude_cli_launch_switches,
)
from packages.orchestration.config import get_key_spec, load_config
from packages.orchestration.pingpong_provider import ClaudeCliProvider


class _Config(dict):
    """A stand-in for `RemedyConfig`: `get` answers the value a key was given, else None."""


def _keys(**values) -> _Config:
    return _Config({f"claude_cli.{k}": v for k, v in values.items()})


class TestTheSwitchesByRole:
    def test_a_reader_gets_safe_mode_and_the_reading_tools(self):
        assert claude_cli_launch_switches("none", config=_keys()) == [
            "--safe-mode", "--tools", "Read,Glob,Grep"]

    def test_a_builder_that_may_write_also_gets_the_editing_tools(self):
        assert claude_cli_launch_switches("allowed-tools", config=_keys()) == [
            "--safe-mode", "--tools", "Read,Glob,Grep,Edit,Write,MultiEdit"]

    def test_a_builder_started_with_dangerous_skip_keeps_every_tool(self):
        assert claude_cli_launch_switches("dangerous-skip", config=_keys()) == ["--safe-mode"]

    def test_an_unknown_write_mode_is_read_as_a_reader(self):
        assert claude_cli_launch_switches("yolo", config=_keys()) == [
            "--safe-mode", "--tools", _READER_TOOLS]


class TestTheKeysTurnEachSourceBackOn:
    def test_customizations_true_drops_safe_mode(self):
        assert claude_cli_launch_switches("none", config=_keys(customizations=True)) == [
            "--tools", _READER_TOOLS]

    def test_all_tools_true_drops_the_tool_list(self):
        assert claude_cli_launch_switches("allowed-tools", config=_keys(all_tools=True)) == [
            "--safe-mode"]

    def test_both_true_add_nothing(self):
        assert claude_cli_launch_switches(
            "allowed-tools", config=_keys(customizations=True, all_tools=True)) == []

    @pytest.mark.parametrize("raw", ["1", "true", "TRUE", " yes "])
    def test_a_true_string_is_true(self, raw):
        assert claude_cli_launch_switches("none", config=_keys(customizations=raw)) == [
            "--tools", _READER_TOOLS]

    @pytest.mark.parametrize("raw", ["0", "false", "no", "", "on", 1, None])
    def test_any_other_value_is_false(self, raw):
        assert "--safe-mode" in claude_cli_launch_switches("none", config=_keys(customizations=raw))

    def test_no_config_reads_the_process_config(self, monkeypatch):
        monkeypatch.setattr(config_module, "get_config", lambda: _keys(all_tools=True))
        assert claude_cli_launch_switches("none") == ["--safe-mode"]


class TestTheCommandLineEndsWithTheSwitches:
    def test_the_switches_follow_the_write_mode_arguments(self):
        argv = build_claude_cli_args("claude", "P", write_mode="allowed-tools", config=_keys())
        assert argv[-5:] == ["--allowedTools", "Edit,Write,MultiEdit", "--safe-mode", "--tools",
                             _WRITER_TOOLS]

    def test_a_reviewer_command_line_ends_with_the_reading_tools(self):
        argv = build_claude_cli_args("claude", "P", json_schema="{}", config=_keys())
        assert argv[-3:] == ["--safe-mode", "--tools", _READER_TOOLS]

    def test_the_old_command_line_comes_back_when_both_keys_are_true(self):
        on = _keys(customizations=True, all_tools=True)
        assert build_claude_cli_args("claude", "P", write_mode="allowed-tools", config=on) == [
            "claude", "-p", "P", "--output-format", "json", "--allowedTools", "Edit,Write,MultiEdit"]


def _provider(**kw) -> ClaudeCliProvider:
    prov = ClaudeCliProvider(**kw)
    prov._claude_path = "/fake/claude"
    prov._cli_version = "1.0.0 (test)"
    prov._cli_version_resolved = True
    return prov


def _ok(**kw) -> MagicMock:
    env = {"type": "result", "subtype": "success", "is_error": False}
    env.update(kw)
    return MagicMock(returncode=0, stdout=json.dumps(env), stderr="")


class TestTheWorkerIsStartedWithTheSwitches:
    """The acceptance line: a test fails when the worker's command line loses a switch F302 added."""

    @pytest.fixture(autouse=True)
    def _default_keys(self, monkeypatch):
        monkeypatch.setattr(config_module, "get_config", lambda: _keys())

    def test_a_builder_call_carries_safe_mode_and_the_writing_tools(self):
        with patch.object(pingpong_provider, "_guarded_cli_run", return_value=_ok(result="done")) as run:
            _provider(write_mode="allowed-tools").build("B")
        argv = run.call_args[0][0]
        assert "--safe-mode" in argv
        assert argv[argv.index("--tools") + 1] == _WRITER_TOOLS

    def test_a_reviewer_call_carries_safe_mode_and_the_reading_tools(self, monkeypatch):
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        so = {"schema_v": "rv1", "verdict": "pass", "findings": [], "confidence": "high",
              "summary": "ok"}
        with patch.object(pingpong_provider, "_guarded_cli_run",
                          return_value=_ok(structured_output=so)) as run:
            out = _provider().review("R")
        argv = run.call_args[0][0]
        assert out.verdict == "pass"
        assert "--safe-mode" in argv
        assert argv[argv.index("--tools") + 1] == _READER_TOOLS


class TestTheKeysAreRegistered:
    @pytest.mark.parametrize("key, env_var", [
        ("claude_cli.all_tools", "REMEDY_CLAUDE_CLI_ALL_TOOLS"),
        ("claude_cli.customizations", "REMEDY_CLAUDE_CLI_CUSTOMIZATIONS"),
    ])
    def test_each_key_is_a_boolean_that_defaults_to_false(self, key, env_var):
        spec = get_key_spec(key)
        assert spec is not None
        assert (spec.value_type, spec.default, spec.env_var, spec.env_only) == (bool, False, env_var, False)

    def test_an_operator_turns_a_source_back_on_with_its_variable(self, monkeypatch, tmp_path):
        monkeypatch.setenv("REMEDY_CLAUDE_CLI_CUSTOMIZATIONS", "true")
        monkeypatch.delenv("REMEDY_CLAUDE_CLI_ALL_TOOLS", raising=False)
        config = load_config(project_path=tmp_path / "p.toml", user_path=tmp_path / "u.toml")
        assert claude_cli_launch_switches("none", config=config) == ["--tools", _READER_TOOLS]

    def test_an_operator_turns_a_source_back_on_in_the_project_file(self, monkeypatch, tmp_path):
        monkeypatch.delenv("REMEDY_CLAUDE_CLI_CUSTOMIZATIONS", raising=False)
        monkeypatch.delenv("REMEDY_CLAUDE_CLI_ALL_TOOLS", raising=False)
        project = tmp_path / "remedy.toml"
        project.write_text("[remedy.claude_cli]\nall_tools = true\n")
        config = load_config(project_path=project, user_path=tmp_path / "u.toml")
        assert claude_cli_launch_switches("allowed-tools", config=config) == ["--safe-mode"]
