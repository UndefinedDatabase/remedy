"""F152 T001, DECISION F152 D3 (3) to (5); T002, DECISION F152 D4 — the worker isolation module's
own pure helpers and its A/B proof utility."""
from __future__ import annotations

import dataclasses
import functools
import json
import os
import stat
import sys
from pathlib import Path

import pytest

from packages.contracts.adapter_contract import CliInvocation, WorkerIsolation
from packages.orchestration.worker_isolation import (
    ISOLATION_POISON_ENV,
    WORKER_ISOLATION_FILENAME,
    create_throwaway_home,
    declared_isolation,
    isolated_child_env,
    isolation_doctor_checks,
    read_tool_help,
    record_worker_isolation,
    remove_throwaway_home,
    run_isolation_ab,
    worker_env_digest,
    worker_isolation_record,
)
from packages.providers.adapters.claude_cli_reference import ClaudeCliReferenceAdapter

_ADR_REF = "docs/adr/0002-claude-cli-worker-isolation.md"

#: R-1460: `.agent/f302_claude_help.txt` lines 228 to 233 verbatim, so the flags check reads the
#: real help text's own spelling — including the parenthesized value `(user, project, local)`
#: that never matches the declared value `project,local` literally, which is why the check below
#: only looks up the two `--`-prefixed flags, never the value between them.
_HELP_TEXT_WITH_FLAGS = (
    "  --setting-sources <sources>           Comma-separated list of setting sources\n"
    "                                        to load (user, project, local).\n"
    "  --settings <file-or-json>             Path to a settings JSON file or a JSON\n"
    "                                        string to load additional settings from\n"
    "  --strict-mcp-config                   Only use MCP servers from --mcp-config,\n"
    "                                        ignoring all other MCP configurations\n"
)

_APPLIES = WorkerIsolation(
    method="tool_flag", adr_ref=_ADR_REF, tool_args=("--x",), env_allowlist=("HOME", "PATH"))
_NOT_APPLIED = WorkerIsolation(
    method="tool_flag", adr_ref=_ADR_REF, tool_args=("--x",), env_allowlist=("HOME", "PATH"),
    applies=False)
_EMPTY_ALLOWLIST = WorkerIsolation(method="tool_flag", adr_ref=_ADR_REF, tool_args=("--x",))


class TestIsolatedChildEnv:
    def test_holds_exactly_the_allowlisted_names_present_in_the_source_and_none_other(self):
        source = {"HOME": "/srv/x", "PATH": "/bin", "SECRET_TOKEN": "s", "OTHER": "o"}
        env = isolated_child_env(_APPLIES, source)
        assert env == {"HOME": "/srv/x", "PATH": "/bin"}

    def test_is_none_while_not_applies(self):
        assert isolated_child_env(_NOT_APPLIED, {"HOME": "/srv/x"}) is None

    def test_is_none_for_an_empty_allowlist(self):
        assert isolated_child_env(_EMPTY_ALLOWLIST, {"HOME": "/srv/x"}) is None


class TestDeclaredIsolation:
    def test_returns_the_adapters_own_isolation_answer(self):
        class _Declaring:
            adapter_id = "stub"

            def isolation(self):
                return _APPLIES

        assert declared_isolation(_Declaring()) is _APPLIES

    def test_raises_naming_the_adapter_for_an_isolation_answering_none(self):
        class _NoneIsolation:
            adapter_id = "stub-none"

            def isolation(self):
                return None

        with pytest.raises(TypeError, match="stub-none"):
            declared_isolation(_NoneIsolation())


class TestWorkerEnvDigest:
    def test_is_equal_for_equal_environments(self):
        env = {"HOME": "/srv/x", "PATH": "/bin"}
        assert worker_env_digest(dict(env)) == worker_env_digest(dict(env))

    def test_differs_when_a_non_secret_value_differs(self):
        first = worker_env_digest({"HOME": "/srv/x", "PATH": "/bin"})
        second = worker_env_digest({"HOME": "/srv/y", "PATH": "/bin"})
        assert first != second

    def test_is_equal_when_only_a_secret_named_value_differs(self):
        first = worker_env_digest({"HOME": "/srv/x", "ANTHROPIC_API_KEY": "sk-one"})
        second = worker_env_digest({"HOME": "/srv/x", "ANTHROPIC_API_KEY": "sk-two"})
        assert first == second

    def test_never_contains_a_value(self):
        digest = worker_env_digest({"HOME": "/srv/super-secret-path", "ANTHROPIC_API_KEY": "sk-x"})
        assert "/srv/super-secret-path" not in digest and "sk-x" not in digest

    def test_is_none_for_none(self):
        assert worker_env_digest(None) is None


class TestWorkerIsolationRecord:
    def test_fields_and_home_is_operator(self):
        env = {"HOME": "/srv/x", "PATH": "/bin"}
        record = worker_isolation_record(_APPLIES, env)
        assert record["method"] == "tool_flag"
        assert record["applied"] is True
        assert record["home"] == "operator"
        assert record["env_digest"] == worker_env_digest(env)
        assert record["names"] == ["HOME", "PATH"]
        assert record["tool_args"] == ["--x"]
        assert record["adr_ref"] == _ADR_REF

    def test_env_digest_none_and_names_empty_when_inherited(self):
        record = worker_isolation_record(_NOT_APPLIED, None)
        assert record["env_digest"] is None
        assert record["names"] == []


class TestRecordWorkerIsolation:
    def test_writes_nothing_for_a_falsy_directory(self, tmp_path):
        record_worker_isolation(
            None, role="builder", provider="claude-cli", model="m",
            record=worker_isolation_record(_APPLIES, {"HOME": "/x"}))
        record_worker_isolation(
            "", role="builder", provider="claude-cli", model="m",
            record=worker_isolation_record(_APPLIES, {"HOME": "/x"}))
        assert list(tmp_path.iterdir()) == []

    def test_appends_one_parseable_line_per_call(self, tmp_path):
        record = worker_isolation_record(_APPLIES, {"HOME": "/x", "PATH": "/bin"})
        record_worker_isolation(
            str(tmp_path), role="builder", provider="claude-cli", model="m", record=record)
        record_worker_isolation(
            str(tmp_path), role="reviewer", provider="claude-cli", model="m", record=record)
        lines = (tmp_path / WORKER_ISOLATION_FILENAME).read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2
        parsed = [json.loads(line) for line in lines]
        assert [p["role"] for p in parsed] == ["builder", "reviewer"]
        assert all(p["provider"] == "claude-cli" and p["model"] == "m" for p in parsed)


class TestThrowawayHome:
    def test_create_makes_a_private_worker_home_directory(self, tmp_path):
        path = create_throwaway_home(str(tmp_path))
        assert path.startswith(str(tmp_path))
        assert os.path.basename(path).startswith("worker-home-")
        mode = stat.S_IMODE(os.stat(path).st_mode)
        assert mode == 0o700

    def test_remove_deletes_the_directory(self, tmp_path):
        path = create_throwaway_home(str(tmp_path))
        remove_throwaway_home(path)
        assert not os.path.exists(path)

    def test_remove_refuses_a_directory_not_so_named(self, tmp_path):
        other = tmp_path / "not-a-worker-home"
        other.mkdir()
        with pytest.raises(ValueError, match="worker-home-"):
            remove_throwaway_home(str(other))
        assert other.exists()


def _write_stand_in_claude(bin_dir: Path) -> str:
    """A `claude` stand-in imitating the surfaces its own help text says the tool loads
    (`.agent/f302_claude_help.txt`): it prints `WORKER_ISOLATION_POISON`'s value when present in
    its own environment; the text of `$HOME/.claude/settings.json` unless `--setting-sources` is
    given without `user` in its value (`:228-229`); and the text of `$HOME/.claude.json` unless
    `--strict-mcp-config` is given (`:232-233`)."""
    bin_dir.mkdir(parents=True, exist_ok=True)
    path = bin_dir / "claude"
    path.write_text(
        f"#!{sys.executable}\n"
        "import json, os, sys\n"
        "argv = sys.argv[1:]\n"
        f"poison = os.environ.get({ISOLATION_POISON_ENV!r})\n"
        "if poison:\n"
        "    print(poison)\n"
        "sources = argv[argv.index('--setting-sources') + 1] if '--setting-sources' in argv else None\n"
        "settings_suppressed = sources is not None and 'user' not in sources.split(',')\n"
        "home = os.environ.get('HOME', '')\n"
        "settings_path = os.path.join(home, '.claude', 'settings.json')\n"
        "if not settings_suppressed and os.path.exists(settings_path):\n"
        "    print(open(settings_path).read())\n"
        "mcp_suppressed = '--strict-mcp-config' in argv\n"
        "mcp_path = os.path.join(home, '.claude.json')\n"
        "if not mcp_suppressed and os.path.exists(mcp_path):\n"
        "    print(open(mcp_path).read())\n"
        "print(json.dumps({'type': 'result', 'is_error': False, 'result': 'ab-proof'}))\n"
    )
    path.chmod(path.stat().st_mode | stat.S_IEXEC)
    return str(path)


def _poison_home(home: str, marker: str, *, settings: bool, mcp: bool) -> None:
    """Write MARKER into `$HOME/.claude/settings.json` and/or `$HOME/.claude.json` under HOME,
    the two file-based surfaces the stand-in claude reads besides its own environment."""
    if settings:
        claude_dir = os.path.join(home, ".claude")
        os.makedirs(claude_dir, exist_ok=True)
        Path(claude_dir, "settings.json").write_text(json.dumps({"marker": marker}))
    if mcp:
        Path(home, ".claude.json").write_text(json.dumps({"marker": marker}))


def _no_leftover_worker_home(parent: Path) -> bool:
    """True when PARENT holds no `worker-home-*` directory."""
    return not any(p.name.startswith("worker-home-") for p in parent.iterdir())


class TestRunIsolationAb:
    """F152 T002, DECISION F152 D4 (2) and (3): the A/B proof utility, proved against a stand-in
    `claude` rather than the real binary, which this session cannot run (DECISION F152 D2 (3))."""

    def _adapter(self, tmp_path, cls=ClaudeCliReferenceAdapter, customizations=False):
        claude_path = _write_stand_in_claude(tmp_path / "bin")
        return cls(claude_path=claude_path, config={"claude_cli.customizations": customizations})

    def test_proves_isolation_for_a_poison_in_both_settings_and_mcp(self, tmp_path):
        adapter = self._adapter(tmp_path)
        result = run_isolation_ab(
            adapter, marker="M-both", parent=str(tmp_path),
            poison_home=functools.partial(_poison_home, settings=True, mcp=True))
        assert result.proves_isolation

    def test_a_variable_only_poison_is_present_unisolated_and_absent_isolated(self, tmp_path):
        adapter = self._adapter(tmp_path)
        result = run_isolation_ab(
            adapter, marker="M-var", parent=str(tmp_path),
            poison_home=functools.partial(_poison_home, settings=False, mcp=False))
        assert result.marker_unisolated is True
        assert result.marker_isolated is False

    def test_a_settings_only_poison_is_present_unisolated_and_absent_isolated(self, tmp_path):
        adapter = self._adapter(tmp_path)
        result = run_isolation_ab(
            adapter, marker="M-settings", parent=str(tmp_path),
            poison_home=functools.partial(_poison_home, settings=True, mcp=False))
        assert result.marker_unisolated is True
        assert result.marker_isolated is False

    def test_an_mcp_only_poison_is_present_unisolated_and_absent_isolated(self, tmp_path):
        adapter = self._adapter(tmp_path)
        result = run_isolation_ab(
            adapter, marker="M-mcp", parent=str(tmp_path),
            poison_home=functools.partial(_poison_home, settings=False, mcp=True))
        assert result.marker_unisolated is True
        assert result.marker_isolated is False

    def test_a_declaration_that_still_allows_the_poison_variable_fails_the_variable_only_proof(
        self, tmp_path,
    ):
        class _LeakyEnvAdapter(ClaudeCliReferenceAdapter):
            """Red control (D4 (3)): its declaration keeps letting `ISOLATION_POISON_ENV` through
            its own allowlist, so the isolated run should still see the variable-only poison."""

            def isolation(self):
                declared = super().isolation()
                return dataclasses.replace(
                    declared, env_allowlist=declared.env_allowlist + (ISOLATION_POISON_ENV,))

        adapter = self._adapter(tmp_path, _LeakyEnvAdapter)
        result = run_isolation_ab(
            adapter, marker="M-leaky", parent=str(tmp_path),
            poison_home=functools.partial(_poison_home, settings=False, mcp=False))
        assert result.marker_isolated is True

    def test_a_declaration_dropping_strict_mcp_config_fails_the_mcp_only_proof(self, tmp_path):
        class _McpLeakingAdapter(ClaudeCliReferenceAdapter):
            """Red control (D4 (3)): its declaration drops `--strict-mcp-config` from its own
            tool_args, so its command line drops it too and the isolated run should still see
            the mcp-only poison."""

            def isolation(self):
                declared = super().isolation()
                return dataclasses.replace(
                    declared,
                    tool_args=tuple(a for a in declared.tool_args if a != "--strict-mcp-config"))

        adapter = self._adapter(tmp_path, _McpLeakingAdapter)
        result = run_isolation_ab(
            adapter, marker="M-mcp-leak", parent=str(tmp_path),
            poison_home=functools.partial(_poison_home, settings=False, mcp=True))
        assert result.marker_isolated is True

    def test_an_adapter_with_no_allowlist_leaks_the_poison_into_its_own_isolated_run(self, tmp_path):
        """Red control (R-1458): before the repair, `isolated_child_env` answered `None` for an
        empty allowlist, `run_guarded` then read that as "inherit the real process environment",
        and an adapter that cleans nothing could read `proves_isolation` true. The repair makes
        the isolated run BASE_ENV itself in that case, so the poison surfaces instead of hiding."""

        class _NoAllowlistAdapter(ClaudeCliReferenceAdapter):
            def isolation(self):
                declared = super().isolation()
                return dataclasses.replace(declared, env_allowlist=())

        adapter = self._adapter(tmp_path, _NoAllowlistAdapter)
        result = run_isolation_ab(
            adapter, marker="M-no-allowlist", parent=str(tmp_path),
            poison_home=functools.partial(_poison_home, settings=False, mcp=False))
        assert result.marker_isolated is True

    def test_a_declaration_that_does_not_apply_raises_and_leaves_no_home(self, tmp_path):
        adapter = self._adapter(tmp_path, customizations=True)
        with pytest.raises(ValueError, match="does not apply"):
            run_isolation_ab(
                adapter, marker="M-x", parent=str(tmp_path), poison_home=lambda h, m: None)
        assert _no_leftover_worker_home(tmp_path)

    def test_a_command_line_lacking_the_declared_flags_raises_and_leaves_no_home(self, tmp_path):
        class _FlagDroppingAdapter(ClaudeCliReferenceAdapter):
            """A command line that lacks the flags its own declaration still claims — the shape
            `run_isolation_ab`'s own refusal exists to catch."""

            def build_invocation(self, role, prompt_parts, options):
                invocation = super().build_invocation(role, prompt_parts, options)
                tool_args = self.isolation().tool_args
                return CliInvocation(argv=invocation.argv[: len(invocation.argv) - len(tool_args)])

        adapter = self._adapter(tmp_path, _FlagDroppingAdapter)
        with pytest.raises(ValueError, match="does not end with"):
            run_isolation_ab(
                adapter, marker="M-y", parent=str(tmp_path), poison_home=lambda h, m: None)
        assert _no_leftover_worker_home(tmp_path)

    def test_the_home_is_gone_after_a_run(self, tmp_path):
        adapter = self._adapter(tmp_path)
        run_isolation_ab(
            adapter, marker="M-z", parent=str(tmp_path),
            poison_home=functools.partial(_poison_home, settings=False, mcp=False))
        assert _no_leftover_worker_home(tmp_path)

    def test_the_home_is_gone_after_a_poison_home_that_raises(self, tmp_path):
        adapter = self._adapter(tmp_path)

        def _raising_poison(home, marker):
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError, match="boom"):
            run_isolation_ab(
                adapter, marker="M-w", parent=str(tmp_path), poison_home=_raising_poison)
        assert _no_leftover_worker_home(tmp_path)


def _patched_help(monkeypatch, help_text):
    """Replace `read_tool_help` module-wide, so `isolation_doctor_checks`'s own call to it never
    reaches a real binary (D5 (3))."""
    import packages.orchestration.worker_isolation as worker_isolation_module
    monkeypatch.setattr(worker_isolation_module, "read_tool_help", lambda executable, env: help_text)


class _ThrowawayHomeAdapter(ClaudeCliReferenceAdapter):
    """A `clean_env` declaration with a throwaway home, for the home check's throwaway branch."""

    def isolation(self):
        return WorkerIsolation(
            method="clean_env", adr_ref=_ADR_REF, env_allowlist=("PATH",), throwaway_home=True)


class TestIsolationDoctorChecks:
    """F152 T003, DECISION F152 D5 (2) and (3): `worker doctor`'s own four isolation checks."""

    def test_all_four_checks_pass_for_the_reference_adapter(self, monkeypatch):
        # R-1460: the captured help text's own spelling, "(user, project, local)", proves the
        # flags check never looks up the non-flag value "project,local" against it.
        _patched_help(monkeypatch, _HELP_TEXT_WITH_FLAGS)
        adapter = ClaudeCliReferenceAdapter(claude_path="claude")
        checks = {name: (ok, detail)
                  for name, ok, detail in isolation_doctor_checks(adapter, provider_id="claude_code")}
        assert set(checks) == {
            "isolation_claude_code_declaration", "isolation_claude_code_record",
            "isolation_claude_code_home", "isolation_claude_code_flags",
        }
        assert all(ok for ok, _detail in checks.values()), checks
        # R-1462: a passing home check's detail never prints the operator's own home path.
        assert os.sep not in checks["isolation_claude_code_home"][1]

    def test_the_flags_check_fails_and_names_the_rejected_flag(self, monkeypatch):
        _patched_help(monkeypatch, "--setting-sources project,local\n")  # drops --strict-mcp-config
        adapter = ClaudeCliReferenceAdapter(claude_path="claude")
        checks = {name: (ok, detail)
                  for name, ok, detail in isolation_doctor_checks(adapter, provider_id="claude_code")}
        ok, detail = checks["isolation_claude_code_flags"]
        assert ok is False
        assert "--strict-mcp-config" in detail

    def test_the_home_check_fails_when_home_is_unset(self, monkeypatch):
        _patched_help(monkeypatch, _HELP_TEXT_WITH_FLAGS)
        monkeypatch.delenv("HOME", raising=False)
        adapter = ClaudeCliReferenceAdapter(claude_path="claude")
        checks = {name: (ok, detail)
                  for name, ok, detail in isolation_doctor_checks(adapter, provider_id="claude_code")}
        ok, _detail = checks["isolation_claude_code_home"]
        assert ok is False

    def test_the_home_check_fails_for_a_throwaway_home_adapter_when_the_parent_cannot_hold_a_directory(
        self, monkeypatch, tmp_path,
    ):
        _patched_help(monkeypatch, _HELP_TEXT_WITH_FLAGS)
        not_a_directory = tmp_path / "not-a-directory"
        not_a_directory.write_text("x")
        import tempfile as _tempfile
        monkeypatch.setattr(_tempfile, "gettempdir", lambda: str(not_a_directory))
        adapter = _ThrowawayHomeAdapter(claude_path="claude")
        checks = {name: (ok, detail)
                  for name, ok, detail in isolation_doctor_checks(adapter, provider_id="claude_code")}
        ok, _detail = checks["isolation_claude_code_home"]
        assert ok is False

    def test_the_record_check_fails_for_a_missing_record(self, monkeypatch):
        _patched_help(monkeypatch, _HELP_TEXT_WITH_FLAGS)

        class _MissingRecordAdapter(ClaudeCliReferenceAdapter):
            def isolation(self):
                declared = super().isolation()
                return dataclasses.replace(declared, adr_ref="docs/adr/9999-does-not-exist.md")

        adapter = _MissingRecordAdapter(claude_path="claude")
        checks = {name: (ok, detail)
                  for name, ok, detail in isolation_doctor_checks(adapter, provider_id="claude_code")}
        ok, detail = checks["isolation_claude_code_record"]
        assert ok is False
        assert "is missing or has no status line" in detail

    def test_a_declaration_that_does_not_apply_answers_one_passing_check(self):
        adapter = ClaudeCliReferenceAdapter(
            claude_path="claude", config={"claude_cli.customizations": True})
        checks = isolation_doctor_checks(adapter, provider_id="claude_code")
        assert len(checks) == 1
        name, ok, _detail = checks[0]
        assert name == "isolation_claude_code"
        assert ok is True

    def test_declared_isolations_refusal_fails_the_declaration_check(self):
        checks = isolation_doctor_checks(_NarrowAdapter(), provider_id="claude_code")
        assert len(checks) == 1
        name, ok, detail = checks[0]
        assert name == "isolation_claude_code_declaration"
        assert ok is False
        assert "claude-cli" in detail


class _NarrowAdapter:
    """A real-world case: an installed adapter missing `isolation()` entirely."""

    adapter_id = "claude-cli"

    def __init__(self, **settings):
        pass


def test_read_tool_help_answers_none_for_an_executable_that_does_not_exist(tmp_path):
    missing = str(tmp_path / "does-not-exist-binary")
    assert read_tool_help(missing, None) is None
