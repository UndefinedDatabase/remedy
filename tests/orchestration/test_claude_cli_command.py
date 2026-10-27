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
    BUILDER_COMMAND_ALLOWLIST,
    BUILDER_COMMAND_REFUSALS_FILENAME,
    build_claude_cli_args,
    builder_bash_rules,
    builder_command_allowed,
    builder_test_commands,
    claude_cli_launch_switches,
    log_builder_command_refusals,
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
            "--safe-mode", "--tools", "Read,Glob,Grep,Edit,Write,MultiEdit,Bash"]

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
        rules = builder_bash_rules(None)
        start = argv.index("--allowedTools")
        assert argv[start:start + 2 + len(rules)] == ["--allowedTools", "Edit,Write,MultiEdit", *rules]
        assert argv[-3:] == ["--safe-mode", "--tools", _WRITER_TOOLS]

    def test_a_reviewer_command_line_ends_with_the_reading_tools(self):
        argv = build_claude_cli_args("claude", "P", json_schema="{}", config=_keys())
        assert argv[-3:] == ["--safe-mode", "--tools", _READER_TOOLS]

    def test_the_old_command_line_comes_back_when_both_keys_are_true(self):
        on = _keys(customizations=True, all_tools=True)
        assert build_claude_cli_args("claude", "P", write_mode="allowed-tools", config=on) == [
            "claude", "-p", "P", "--output-format", "json", "--allowedTools", "Edit,Write,MultiEdit",
            *builder_bash_rules(None), "--permission-mode", "dontAsk"]


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


class TestTheBuilderMayRunOnlyTheListedCommands:
    """Operator amendment amend1024-one-real-order, Part C: the builder's Bash and its refusals."""

    def test_every_listed_command_becomes_one_bash_rule_after_the_test_commands(self):
        rules = builder_bash_rules(None)
        assert rules[:3] == ["Bash(python -m pytest:*)", "Bash(python3 -m pytest:*)", "Bash(pnpm test:*)"]
        assert rules[3:] == [f"Bash({command}:*)" for command in BUILDER_COMMAND_ALLOWLIST]
        assert "Bash(git diff:*)" in rules and "Bash(pnpm lint:*)" in rules

    def test_the_projects_own_test_command_comes_first(self, tmp_path):
        (tmp_path / ".remedy").mkdir()
        (tmp_path / ".remedy" / "config.toml").write_text('[tests]\ncommand = ["make", "check"]\n')
        assert builder_test_commands(str(tmp_path))[0] == "make check"

    def test_a_reviewer_and_a_dangerous_skip_builder_get_no_bash_rules(self):
        assert not any(arg.startswith("Bash(") for arg in build_claude_cli_args("claude", "P", config=_keys()))
        skip = build_claude_cli_args("claude", "P", write_mode="dangerous-skip", config=_keys())
        assert "--dangerously-skip-permissions" in skip and not any(arg.startswith("Bash(") for arg in skip)

    @pytest.mark.parametrize("command", ["git diff --stat", "python3 -m pytest -q tests", "pnpm test", "ls",
                                         "grep -rn greet src"])
    def test_a_listed_command_is_allowed(self, command):
        assert builder_command_allowed(command, builder_test_commands(None) + BUILDER_COMMAND_ALLOWLIST)

    @pytest.mark.parametrize("command", ["rm -rf build", "curl https://example.com", "git push", "pip install x",
                                         "git status; rm -rf x", "cat a > b", "ls | sh", "echo $(id)", "lsblk",
                                         "python -c 'print(1)'"])
    def test_a_command_outside_the_list_is_refused(self, command):
        assert not builder_command_allowed(command, builder_test_commands(None) + BUILDER_COMMAND_ALLOWLIST)

    def test_a_refused_command_is_logged_as_evidence(self, tmp_path):
        """C3: the CLI refuses a command outside the list; the refusal it reports lands in the evidence."""
        log = tmp_path / "evidence" / BUILDER_COMMAND_REFUSALS_FILENAME
        envelope = json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "done",
                               "permission_denials": [{"tool_name": "Bash", "tool_use_id": "t1",
                                                       "tool_input": {"command": "rm -rf build"}}]})
        assert not builder_command_allowed("rm -rf build", BUILDER_COMMAND_ALLOWLIST)
        with patch.object(pingpong_provider, "_guarded_cli_run",
                          return_value=MagicMock(returncode=0, stdout=envelope, stderr="")):
            _provider(write_mode="allowed-tools", command_refusals_path=str(log)).build("B")
        [line] = [json.loads(text) for text in log.read_text(encoding="utf-8").splitlines()]
        assert line == {"tool": "Bash", "command": "rm -rf build", "reason": "outside the builder's command list"}

    def test_a_reply_without_refusals_writes_nothing(self, tmp_path):
        log = tmp_path / BUILDER_COMMAND_REFUSALS_FILENAME
        assert log_builder_command_refusals(json.dumps({"result": "ok"}), str(log)) == []
        assert log_builder_command_refusals("not json", str(log)) == []
        assert not log.exists()


class TestTheBuilderMayRunTheProjectsTests:
    """Operator amendment amend1027-green-builds, Part A: the found test command and its spellings."""

    def test_a_package_json_project_gets_its_runners_and_its_test_scripts(self, tmp_path):
        (tmp_path / "package.json").write_text(json.dumps(
            {"scripts": {"test": "vitest run", "e2e": "playwright test", "build": "vite build",
                         "test;rm": "x"}}))
        commands = builder_test_commands(str(tmp_path))
        assert commands[0] == "npm test"
        for spelling in ("pnpm exec playwright test", "npx vitest", "pnpm vitest", "pnpm e2e",
                         "pnpm run e2e", "npm run e2e"):
            assert spelling in commands
        assert "pnpm build" not in commands and not any("rm" in c for c in commands)
        allowed = commands + BUILDER_COMMAND_ALLOWLIST
        assert builder_command_allowed("pnpm e2e tests/e2e/memory-net-592.spec.ts -g net", allowed)
        assert builder_command_allowed("npx playwright test tests/e2e/a.spec.ts", allowed)
        assert not builder_command_allowed("pnpm install", allowed)

    def test_a_python_project_gets_pytest_under_every_spelling(self, tmp_path):
        (tmp_path / "tests").mkdir()
        commands = builder_test_commands(str(tmp_path))
        assert commands[0] == "python -m pytest -p no:cacheprovider tests -q"
        for spelling in ("pytest", "python -m pytest", "python3 -m pytest", "uv run pytest",
                         ".venv/bin/pytest", ".venv/bin/python -m pytest"):
            assert spelling in commands
        assert "npx vitest" not in commands

    def test_a_configured_pytest_command_counts_as_python(self, tmp_path):
        (tmp_path / ".remedy").mkdir()
        (tmp_path / ".remedy" / "config.toml").write_text('[tests]\ncommand = ["pytest", "-q"]\n')
        commands = builder_test_commands(str(tmp_path))
        assert commands[0] == "pytest -q" and "uv run pytest" in commands

    def test_a_builder_that_may_write_is_never_asked(self):
        """A3: `--permission-mode dontAsk` ends a builder's rules; a reader and dangerous-skip lack it."""
        argv = build_claude_cli_args("claude", "P", write_mode="allowed-tools", config=_keys())
        assert argv[argv.index("--permission-mode") + 1] == "dontAsk"
        assert argv.index("--permission-mode") > max(i for i, a in enumerate(argv) if a.startswith("Bash("))
        assert "--permission-mode" not in build_claude_cli_args("claude", "P", config=_keys())
        skip = build_claude_cli_args("claude", "P", write_mode="dangerous-skip", config=_keys())
        assert "--permission-mode" not in skip and "--dangerously-skip-permissions" in skip


class TestTheBuildersEnvironment:
    """A2: the project's tool folders come first on the builder's PATH, with its tests' variables."""

    def test_the_project_tools_come_first_and_the_tests_env_is_set(self, tmp_path, monkeypatch):
        from packages.orchestration.claude_cli_command import with_project_tools
        from packages.orchestration.exec_guard import ExecGuardPolicy

        (tmp_path / "node_modules" / ".bin").mkdir(parents=True)
        venv = tmp_path / ".venv"
        (venv / "bin").mkdir(parents=True)
        (venv / "pyvenv.cfg").write_text("home = /usr\n")
        (venv / "bin" / "python").write_text("")
        (tmp_path / ".remedy").mkdir()
        (tmp_path / ".remedy" / "config.toml").write_text('[tests]\nenv = { KIT = "/k" }\n')
        policy = with_project_tools(
            ExecGuardPolicy(env={"PATH": "/usr/bin", "HOME": "/h"}, env_allowlist=("PATH", "HOME")),
            str(tmp_path))
        assert policy.env["PATH"].split(":") == [
            str(venv / "bin"), str(tmp_path / "node_modules" / ".bin"), "/usr/bin"]
        assert policy.env["KIT"] == "/k" and policy.env["VIRTUAL_ENV"] == str(venv)
        assert {"PATH", "HOME", "KIT", "VIRTUAL_ENV"} <= set(policy.env_allowlist)

    def test_no_workspace_changes_nothing(self):
        from packages.orchestration.claude_cli_command import with_project_tools
        from packages.orchestration.exec_guard import ExecGuardPolicy

        policy = ExecGuardPolicy(env={"PATH": "/usr/bin"})
        assert with_project_tools(policy, None) is policy
