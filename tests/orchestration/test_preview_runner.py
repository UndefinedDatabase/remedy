"""F041 T002 — the runtime verb runner a preview uses (DECISION F041 D3).

One test runs the real command line against an empty folder, where `remedy runtime serve`
refuses before it starts anything; the others replace the child process to pin how an envelope,
a silent child and a hung child are read.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration import preview_runner
from packages.orchestration.preview_control import VerbResult
from packages.orchestration.preview_runner import (
    RUNTIME_VERBS,
    VERB_TIMEOUT_SECONDS,
    run_runtime_verb,
    runtime_verb_argv,
)


def test_the_argv_is_the_harness_command_line(tmp_path):
    assert RUNTIME_VERBS == ("serve", "probe", "stop")
    assert runtime_verb_argv("serve", tmp_path) == [
        sys.executable, "-m", "apps.cli.main", "runtime", "serve", "--repo", str(tmp_path),
        "--json"]
    with pytest.raises(ValueError):
        runtime_verb_argv("restart", tmp_path)


def test_serving_an_empty_folder_answers_the_harness_config_refusal(tmp_path):
    result = run_runtime_verb("serve", tmp_path)
    assert result.ok is False
    assert result.payload["error"] == "runtime_config_error"
    assert result.payload["ok"] is False


def _fake_run(stdout: str, returncode: int, seen: list):
    def run(argv, **kwargs):
        seen.append((argv, kwargs))
        return subprocess.CompletedProcess(argv, returncode, stdout=stdout, stderr="")
    return run


def test_an_ok_envelope_at_exit_zero_is_ok(monkeypatch, tmp_path):
    seen: list = []
    monkeypatch.setattr(preview_runner.subprocess, "run",
                        _fake_run('{"ok": true, "url": "http://127.0.0.1:1/", "port": 1}', 0, seen))
    assert run_runtime_verb("probe", tmp_path) == VerbResult(
        True, {"ok": True, "url": "http://127.0.0.1:1/", "port": 1})
    [(argv, kwargs)] = seen
    assert argv == runtime_verb_argv("probe", tmp_path)
    assert kwargs["timeout"] == VERB_TIMEOUT_SECONDS == 180
    assert kwargs["capture_output"] is True


def test_an_ok_envelope_at_a_nonzero_exit_is_not_ok(monkeypatch, tmp_path):
    monkeypatch.setattr(preview_runner.subprocess, "run", _fake_run('{"ok": true}', 4, []))
    assert run_runtime_verb("probe", tmp_path).ok is False


@pytest.mark.parametrize("stdout", ["", "not json", "[1, 2]"])
def test_a_child_that_answers_no_envelope_is_a_failure(monkeypatch, tmp_path, stdout):
    monkeypatch.setattr(preview_runner.subprocess, "run", _fake_run(stdout, 3, []))
    assert run_runtime_verb("serve", tmp_path) == VerbResult(
        False, {"error": "runtime_error", "message": "runtime serve answered no envelope (exit 3)"})


def test_a_hung_child_is_a_failure_naming_the_bound(monkeypatch, tmp_path):
    def hang(argv, **kwargs):
        raise subprocess.TimeoutExpired(argv, kwargs["timeout"])
    monkeypatch.setattr(preview_runner.subprocess, "run", hang)
    assert run_runtime_verb("serve", tmp_path) == VerbResult(
        False, {"error": "runtime_error",
                "message": "runtime serve did not answer within 180 seconds"})


def test_the_child_runs_from_the_remedy_checkout(monkeypatch, tmp_path):
    seen: list = []
    monkeypatch.setattr(preview_runner.subprocess, "run", _fake_run('{"ok": true}', 0, seen))
    run_runtime_verb("stop", tmp_path)
    assert Path(seen[0][1]["cwd"]) == Path(preview_runner.__file__).resolve().parents[2]
