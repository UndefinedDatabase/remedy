"""F315 T002, DECISION F315 D2 — the worker adapter slot and the loop that follows it.

The command line installs the adapter registry into the slot, and every claude-cli call the loop
makes takes its command line from the installed adapter. These tests replace the installed adapter
and watch the provider and the ping-pong loop follow it.
"""
from __future__ import annotations

import dataclasses
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

from packages.contracts.adapter_contract import HttpInvocation, InvocationOptions, WorkerIsolation
from packages.orchestration import worker_adapter_slot as slot
from packages.orchestration.claude_cli_command import build_claude_cli_args
from packages.orchestration.pingpong_loop import run_pingpong
from packages.orchestration.pingpong_provider import ClaudeCliProvider
from packages.orchestration.worker_adapter_slot import (
    WorkerAdapterNotInstalled,
    adapter_child_env,
    adapter_cli_argv,
    adapter_isolation_record,
    adapter_usage_actuals,
    install_worker_adapters,
    installed_worker_adapter,
)
from packages.providers.adapters.adapter_registry import WORKER_ADAPTERS_BY_REF
from packages.providers.adapters.claude_cli_reference import ClaudeCliReferenceAdapter

MARKER = "--remedy-f315-marker"
_PASS = {"verdict": "pass", "findings": [], "confidence": "high", "summary": "ok"}


class _MarkingAdapter(ClaudeCliReferenceAdapter):
    """The reference adapter, with every role it built for recorded and a marker on its argv."""

    roles: list[str] = []

    def build_invocation(self, role, prompt_parts, options):
        _MarkingAdapter.roles.append(role)
        built = super().build_invocation(role, prompt_parts, options)
        return type(built)(argv=(*built.argv, MARKER))


class _HttpAdapter(ClaudeCliReferenceAdapter):
    def build_invocation(self, role, prompt_parts, options):
        return HttpInvocation(method="POST", url="http://127.0.0.1:9", body={})


def _fake_claude(tmp_path: Path, result_text: str) -> tuple[Path, Path]:
    """A `claude` on PATH that logs its argv, one JSON list per line, and answers `result_text`."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log = tmp_path / "argv.jsonl"
    payload = json.dumps({"type": "result", "is_error": False, "result": result_text})
    script = bin_dir / "claude"
    script.write_text(
        f"#!{sys.executable}\nimport json, sys\n"
        f"open({str(log)!r}, 'a').write(json.dumps(sys.argv[1:]) + '\\n')\n"
        f"print({payload!r})\n")
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    return bin_dir, log


def _logged(log: Path) -> list[list[str]]:
    """Every logged call but the provider's own `--version` probe, which no adapter builds."""
    calls = [json.loads(line) for line in log.read_text().splitlines()]
    return [call for call in calls if call != ["--version"]]


@pytest.fixture
def marking_adapter(monkeypatch):
    _MarkingAdapter.roles = []
    monkeypatch.setitem(slot._INSTALLED_WORKER_ADAPTERS, "claude-cli", _MarkingAdapter)
    return _MarkingAdapter


def test_the_test_process_finds_the_registry_installed():
    assert slot._INSTALLED_WORKER_ADAPTERS == WORKER_ADAPTERS_BY_REF


def test_the_command_line_installs_the_registry_before_a_command_runs(monkeypatch, capsys):
    from apps.cli.grouped import main

    monkeypatch.setattr(slot, "_INSTALLED_WORKER_ADAPTERS", {})
    try:
        main(["worker", "list", "--json"])
    except SystemExit as exc:
        assert exc.code in (0, None)
    assert slot._INSTALLED_WORKER_ADAPTERS == WORKER_ADAPTERS_BY_REF
    assert '"claude_code"' in capsys.readouterr().out


def test_install_replaces_what_was_installed(monkeypatch):
    monkeypatch.setattr(slot, "_INSTALLED_WORKER_ADAPTERS", {"old": ClaudeCliReferenceAdapter})
    install_worker_adapters({"claude-cli": _MarkingAdapter})
    assert slot._INSTALLED_WORKER_ADAPTERS == {"claude-cli": _MarkingAdapter}


def test_an_empty_slot_raises_and_the_provider_reports_it(monkeypatch, tmp_path):
    monkeypatch.setattr(slot, "_INSTALLED_WORKER_ADAPTERS", {})
    with pytest.raises(WorkerAdapterNotInstalled, match="'claude-cli'"):
        installed_worker_adapter("claude-cli")
    bin_dir, log = _fake_claude(tmp_path, "built")
    monkeypatch.setenv("PATH", str(bin_dir))
    out = ClaudeCliProvider().build("do it")
    assert out.error.startswith("provider_error: WorkerAdapterNotInstalled")
    assert not log.exists()


def test_installed_adapter_receives_its_settings(monkeypatch):
    seen = {}

    def factory(**settings):
        seen.update(settings)
        return ClaudeCliReferenceAdapter(**settings)

    monkeypatch.setitem(slot._INSTALLED_WORKER_ADAPTERS, "claude-cli", factory)
    installed_worker_adapter("claude-cli", claude_path="/x/claude", write_mode="allowed-tools",
                             streaming=True)
    assert seen == {"claude_path": "/x/claude", "write_mode": "allowed-tools", "streaming": True}


@pytest.mark.parametrize(("role", "write_mode", "expected_mode"), [
    ("builder", "allowed-tools", "allowed-tools"),
    ("builder", "none", "none"),
    ("reviewer", "none", "none"),
])
@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize(("json_schema", "resume"), [
    ("", ""), ('{"properties":{"a":{"type":"string"}},"type":"object"}', "sess-1"),
])
def test_adapter_argv_equals_the_command_line_builder(
        role, write_mode, expected_mode, streaming, json_schema, resume):
    argv = adapter_cli_argv(
        "claude-cli", role, "the prompt", model="claude-x", json_schema=json_schema, resume=resume,
        claude_path="/bin/claude", write_mode=write_mode, streaming=streaming)
    assert argv == build_claude_cli_args(
        "/bin/claude", "the prompt", write_mode=expected_mode, model="claude-x",
        stream_evidence=streaming, json_schema=json_schema, resume_session=resume,
    ) + ["--setting-sources", "project,local", "--strict-mcp-config"]
    assert isinstance(argv, list)


def test_a_command_line_is_required_of_the_adapter(monkeypatch):
    monkeypatch.setitem(slot._INSTALLED_WORKER_ADAPTERS, "claude-cli", _HttpAdapter)
    with pytest.raises(TypeError, match="HttpInvocation"):
        adapter_cli_argv("claude-cli", "builder", "p", model="")


def test_options_reach_the_adapter_unchanged(monkeypatch):
    seen: list[InvocationOptions] = []

    class _Recording(ClaudeCliReferenceAdapter):
        def build_invocation(self, role, prompt_parts, options):
            seen.append(options)
            return super().build_invocation(role, prompt_parts, options)

    monkeypatch.setitem(slot._INSTALLED_WORKER_ADAPTERS, "claude-cli", _Recording)
    adapter_cli_argv("claude-cli", "reviewer", "p", model="m", json_schema='{"a":1}', resume="s-2")
    adapter_cli_argv("claude-cli", "builder", "p", model="")
    assert seen == [
        InvocationOptions(model="m", output_schema={"a": 1}, resume_ref="s-2"),
        InvocationOptions(model="", output_schema=None, resume_ref=None),
    ]


@pytest.mark.parametrize("structured", [False, True])
def test_the_provider_spawns_the_adapters_command_line(
        marking_adapter, monkeypatch, tmp_path, structured):
    if not structured:
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
    bin_dir, log = _fake_claude(tmp_path, json.dumps(_PASS))
    monkeypatch.setenv("PATH", str(bin_dir))
    provider = ClaudeCliProvider()
    provider.build("build it")
    provider.review("review it")
    assert marking_adapter.roles == ["builder", "reviewer"]
    calls = _logged(log)
    assert len(calls) == 2
    assert all(call[-1] == MARKER for call in calls)
    assert ("--json-schema" in calls[1]) is structured


@pytest.mark.parametrize("structured", [False, True])
def test_the_streaming_provider_spawns_the_adapters_streamed_command_line(
        marking_adapter, monkeypatch, tmp_path, structured):
    if not structured:
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
    bin_dir, log = _fake_claude(tmp_path, json.dumps(_PASS))
    monkeypatch.setenv("PATH", str(bin_dir))
    provider = ClaudeCliProvider(stream_evidence=True, stream_evidence_dir=str(tmp_path / "streams"))
    provider.build("build it")
    provider.review("review it")
    assert marking_adapter.roles == ["builder", "reviewer"]
    calls = _logged(log)
    assert len(calls) == 2
    assert all(call[-1] == MARKER and "stream-json" in call for call in calls)
    assert ("--json-schema" in calls[1]) is structured


_USAGE = {"input_tokens": 11, "output_tokens": 5, "cache_read_input_tokens": 0,
          "cache_creation_input_tokens": 0}


@pytest.mark.parametrize(("raw", "reason"), [
    (json.dumps({"type": "result", "is_error": False, "result": "r", "usage": _USAGE}), "ok"),
    (json.dumps({"type": "result", "is_error": True, "result": "r", "usage": _USAGE}), "is_error"),
    (json.dumps({"type": "result", "is_error": False, "result": "r"}), "usage_missing"),
    ("plain text, not json", "parse_failed"),
    ("", "empty_input"),
])
def test_adapter_usage_answers_the_adapters_usage_or_the_reason_it_has_none(raw, reason):
    actuals, got = adapter_usage_actuals("claude-cli", raw)
    assert got == reason
    assert (actuals is not None) is (reason == "ok")
    if actuals is not None:
        assert (actuals.input_tokens, actuals.output_tokens) == (11, 5)


def test_the_provider_takes_its_usage_from_the_installed_adapter(monkeypatch, tmp_path):
    mapped: list[str] = []

    class _Halving(ClaudeCliReferenceAdapter):
        def map_usage(self, raw):
            mapped.append(raw)
            usage = super().map_usage(raw)
            return dataclasses.replace(
                usage, actuals=dataclasses.replace(usage.actuals, input_tokens=1, output_tokens=2))

    monkeypatch.setitem(slot._INSTALLED_WORKER_ADAPTERS, "claude-cli", _Halving)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    payload = json.dumps({"type": "result", "is_error": False, "result": "built", "usage": _USAGE})
    script = bin_dir / "claude"
    script.write_text(f"#!{sys.executable}\nprint({payload!r})\n")
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    monkeypatch.setenv("PATH", str(bin_dir))
    out = ClaudeCliProvider().build("build it")
    assert len(mapped) == 1
    assert (out.usage_actuals["input_tokens"], out.usage_actuals["output_tokens"]) == (1, 2)
    assert out.tokens_used == 3


def test_a_claude_cli_job_runs_its_calls_through_the_installed_adapter(
        marking_adapter, monkeypatch, tmp_path):
    monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
    bin_dir, log = _fake_claude(tmp_path, json.dumps(_PASS))
    monkeypatch.setenv("PATH", f"{bin_dir}:/usr/bin:/bin")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# demo\n")
    for argv in (["init", "-q"], ["add", "-A"],
                 ["-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init"]):
        subprocess.run(["git", "-C", str(repo), *argv], check=True)
    run_pingpong("Fix README", str(repo), builder_name="claude-cli", reviewer_name="claude-cli",
                 max_rounds=1)
    assert "builder" in marking_adapter.roles and "reviewer" in marking_adapter.roles
    calls = _logged(log)
    assert calls and all(call[-1] == MARKER for call in calls)


# -- adapter_child_env: DECISION F152 D3 (3), the declared, cleaned environment ----------------


def test_adapter_child_env_drops_an_unlisted_variable_and_keeps_path(monkeypatch):
    monkeypatch.setenv("REMEDY_F152_LEAK_PROBE", "leaked")
    env = adapter_child_env("claude-cli", config={})
    assert env is not None
    assert "REMEDY_F152_LEAK_PROBE" not in env
    assert env["PATH"] == os.environ["PATH"]


def test_adapter_child_env_is_none_with_customizations_true():
    assert adapter_child_env("claude-cli", config={"claude_cli.customizations": True}) is None


def test_adapter_child_env_refuses_a_throwaway_home_declaration(monkeypatch):
    class _ThrowawayAdapter(ClaudeCliReferenceAdapter):
        def isolation(self):
            return WorkerIsolation(
                method="clean_env", adr_ref="docs/adr/0002-claude-cli-worker-isolation.md",
                env_allowlist=("PATH",), throwaway_home=True)

        # WHY: an adapter overriding isolation() must still declare a sandbox default of its own
        # kind to stay a WorkerAdapter (DECISION F162 D4 (1)); this fixture borrows the reference
        # adapter's, having none of its own to test.
        def sandbox_default(self):
            return super().sandbox_default()

    monkeypatch.setitem(slot._INSTALLED_WORKER_ADAPTERS, "claude-cli", _ThrowawayAdapter)
    with pytest.raises(ValueError, match="declares throwaway_home"):
        adapter_child_env("claude-cli")


class _NarrowAdapter:
    """A real-world case: an installed adapter missing `isolation()` (and every other newer
    member), the shape F157/F151's own reduced-capability test doubles used to use.
    `adapter_child_env`/`adapter_isolation_record` must raise `TypeError` on it rather than run
    such a worker call with no declared isolation at all (R-1456, DECISION F152 D4 (1))."""

    adapter_id = "claude-cli"

    def __init__(self, **settings):
        pass


def test_adapter_child_env_raises_for_an_adapter_without_isolation(monkeypatch):
    monkeypatch.setitem(slot._INSTALLED_WORKER_ADAPTERS, "claude-cli", _NarrowAdapter)
    with pytest.raises(TypeError, match="claude-cli"):
        adapter_child_env("claude-cli")


def test_adapter_isolation_record_raises_for_an_adapter_without_isolation(monkeypatch):
    monkeypatch.setitem(slot._INSTALLED_WORKER_ADAPTERS, "claude-cli", _NarrowAdapter)
    with pytest.raises(TypeError, match="claude-cli"):
        adapter_isolation_record("claude-cli")


def _env_logging_claude(tmp_path: Path) -> tuple[Path, Path]:
    """A `claude` on PATH that appends one JSON line per run, holding its own argv and its
    environment's sorted NAMES, never a value (R-1459): the provider's own `--version` probe and
    a streamed build both run through this stand-in, and only a per-run log, read back by argv,
    tells the two calls apart."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log = tmp_path / "env_names.jsonl"
    payload = json.dumps({"type": "result", "is_error": False, "result": "ok"})
    script = bin_dir / "claude"
    script.write_text(
        f"#!{sys.executable}\nimport json, os, sys\n"
        "line = json.dumps({'argv': sys.argv[1:], 'names': sorted(os.environ)})\n"
        f"open({str(log)!r}, 'a').write(line + '\\n')\n"
        f"print({payload!r})\n")
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    return bin_dir, log


@pytest.mark.parametrize("streaming", [False, True])
def test_the_real_child_drops_the_planted_variable_and_keeps_path(monkeypatch, tmp_path, streaming):
    monkeypatch.setenv("REMEDY_F152_LEAK_PROBE", "leaked")
    bin_dir, log = _env_logging_claude(tmp_path)
    monkeypatch.setenv("PATH", str(bin_dir))
    stream_dir = str(tmp_path / "streams") if streaming else None
    provider = ClaudeCliProvider(stream_evidence=streaming, stream_evidence_dir=stream_dir)
    provider.build("build it")
    calls = [json.loads(line) for line in log.read_text().splitlines()]
    build_call = next(call for call in calls if "-p" in call["argv"])
    assert "REMEDY_F152_LEAK_PROBE" not in build_call["names"]
    assert "PATH" in build_call["names"]
    assert ("stream-json" in build_call["argv"]) is streaming
