"""F157 round 6, DECISION F157 D3 (6) — the reduced-capability end-to-end.

A one-task job, run through the real `job.run` command handler
(`COMMAND_HANDLERS["job.run"]`) exactly as the command line would: once with a reduced
claude-cli adapter installed for `"claude-cli"` (the reference adapter's own declared
`json_schema` answered False), once with the registry's reference adapter left installed. The
reduced run's evidence file, job report and run report must name exactly the degradation the
register predicts (`reviewer_schema_gate` as `schema_in_prompt`); the control run must name none.
"""
from __future__ import annotations

import dataclasses
import json
import subprocess
import types
from pathlib import Path

import pytest

from apps.cli.commands.run_report_cmd import _cmd_run_show
from packages.contracts.adapter_contract import AdapterCapabilities
from packages.contracts.capability_matrix import CAPABILITY_DEGRADATIONS_FIELD
from packages.orchestration import data_paths
from packages.orchestration import worker_adapter_slot as slot
from packages.orchestration.capability_evidence import task_capability_degradations
from packages.orchestration.job_report import format_job_report_text
from packages.orchestration.pingpong_job import load_job_plan, parse_job_file
from packages.providers.adapters.claude_cli_reference import ClaudeCliReferenceAdapter

# Reused from tests/orchestration/test_job_task_runner.py, which already exposes them as
# module-level helpers for exactly this real-CLI-handler dispatch (block C2, F157 R6).
from tests.orchestration.test_job_task_runner import _TWO_TASK_JOB, _make_args, _run_job_handler

# Unique to the legacy, schema-in-prompt reviewer call — the reviewer's always-present system
# prompt already says "Return ONLY valid JSON...", so that line alone cannot discriminate the
# two paths; this one can, because only `_REVIEWER_JSON_SCHEMA` carries it.
_SCHEMA_IN_PROMPT_MARKER = "Your entire response must be exactly one JSON object with this structure:"

_PASSING_VERDICT = {"verdict": "pass", "findings": [], "confidence": "high", "summary": "ok"}


# WHY: the two fixtures `_run_job_handler` needs, copied rather than imported across test files
# (small helpers, block C2) — an isolated data root and a tiny demo repo for the job to target.
@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch):
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def demo_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\nA demo project.\n")
    (repo / "src").mkdir()
    (repo / "src" / "main.py").write_text("def hello():\n    return 'hello'\n")
    (repo / "docs").mkdir()
    (repo / "docs" / "README.md").write_text("# Docs\n")
    return repo


# WHY: the reference adapter with its own declared `json_schema` answered False, built with
# `dataclasses.replace` over the reference adapter's own declaration (DECISION F157 D3 (6)).
class _ReducedJsonSchemaAdapter(ClaudeCliReferenceAdapter):
    """The reference adapter, with `json_schema` degraded and every other capability untouched."""

    def capabilities(self, model: str) -> AdapterCapabilities:
        return dataclasses.replace(super().capabilities(model), json_schema=False)


def _install_fake_claude_cli(monkeypatch) -> list[list[str]]:
    """Replace `_guarded_cli_run`, shaped as `test_job_task_runner._install_fake_claude_cli` is,
    and return the list every command it receives is appended to.

    Answers `--version`, the builder's call, the reviewer's native call with a top-level
    `structured_output`, and the reviewer's schema-in-prompt call with the passing verdict as a
    JSON string in `result` — discriminated by "Reviewer" in the prompt text (how the reviewer's
    always-present `_REVIEWER_SYSTEM` prompt is composed) and, among reviewer calls, by whether
    the call's own argv carries `--json-schema` (native) or not (schema-in-prompt).
    """
    import packages.orchestration.pingpong_provider as provider_mod

    calls: list[list[str]] = []

    def _fake_guarded_cli_run(cmd, timeout_sec, cwd):
        calls.append(list(cmd))
        if "--version" in cmd:
            return subprocess.CompletedProcess(cmd, 0, "1.0.0-fake\n", "")
        prompt = cmd[2] if len(cmd) > 2 else ""
        is_reviewer = "Reviewer" in prompt
        payload = {
            "type": "result", "is_error": False,
            "session_id": "sess-fake-f157-r6", "total_cost_usd": 0.0, "num_turns": 1,
            "duration_ms": 1,
            "usage": {"input_tokens": 1, "cache_creation_input_tokens": 0,
                      "cache_read_input_tokens": 0, "output_tokens": 1},
        }
        if is_reviewer:
            if "--json-schema" in cmd:
                payload["structured_output"] = {"schema_v": "rv1", **_PASSING_VERDICT}
            else:
                payload["result"] = json.dumps(_PASSING_VERDICT)
        else:
            payload["result"] = "Builder made changes\n- docs/README.md updated"
        return subprocess.CompletedProcess(cmd, 0, json.dumps(payload) + "\n", "")

    monkeypatch.setattr(provider_mod, "_guarded_cli_run", _fake_guarded_cli_run)
    return calls


def _reviewer_calls(calls: list[list[str]]) -> list[list[str]]:
    return [c for c in calls if "--version" not in c and len(c) > 2 and "Reviewer" in c[2]]


def _run_one_task_job(demo_repo: Path) -> types.SimpleNamespace:
    """Parse the two-task job and run its first task through the real CLI handler."""
    job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
    args = _make_args(
        job_id=job.job_id, builder_provider="claude-cli", reviewer_provider="claude-cli",
        max_tasks="1",
    )
    _run_job_handler(args)
    return job


def test_reduced_adapter_names_its_degradation_in_evidence_and_both_reports(
    isolate_data_root, demo_repo, monkeypatch, capsys,
):
    monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
    monkeypatch.setitem(slot._INSTALLED_WORKER_ADAPTERS, "claude-cli", _ReducedJsonSchemaAdapter)
    calls = _install_fake_claude_cli(monkeypatch)

    job = _run_one_task_job(demo_repo)
    capsys.readouterr()  # discard the handler's own JSON answer

    reloaded = load_job_plan(job.job_id)
    task = reloaded.tasks[0]

    expected = [{
        "feature_key": "reviewer_schema_gate", "mode": "degraded",
        "strategy": "schema_in_prompt", "missing": ["json_schema"],
    }]
    assert task_capability_degradations(reloaded.job_id, task.task_id, task.run_id) == expected

    decisions_path = data_paths.run_dir(task.run_id) / "capability_decisions.jsonl"
    lines = decisions_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["role"] == "reviewer"
    modes_by_key = {d["feature_key"]: d["mode"] for d in record["decisions"]}
    assert modes_by_key == {"reviewer_schema_gate": "degraded", "parked_session_resume": "native"}

    reviewer_calls = _reviewer_calls(calls)
    assert reviewer_calls
    assert all("--json-schema" not in c for c in reviewer_calls)
    assert any(_SCHEMA_IN_PROMPT_MARKER in c[2] for c in reviewer_calls)

    report_text = format_job_report_text(reloaded)
    assert "      Degradations: reviewer_schema_gate as schema_in_prompt" in report_text

    _cmd_run_show(task.run_id)
    assert "Degradations: reviewer_schema_gate as schema_in_prompt" in capsys.readouterr().out

    _cmd_run_show(task.run_id, json_output=True)
    shown = json.loads(capsys.readouterr().out)
    assert shown[CAPABILITY_DEGRADATIONS_FIELD] == expected


def test_registry_adapter_names_no_degradation_in_either_report(
    isolate_data_root, demo_repo, monkeypatch, capsys,
):
    monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
    calls = _install_fake_claude_cli(monkeypatch)

    job = _run_one_task_job(demo_repo)
    capsys.readouterr()  # discard the handler's own JSON answer

    reloaded = load_job_plan(job.job_id)
    task = reloaded.tasks[0]

    assert task_capability_degradations(reloaded.job_id, task.task_id, task.run_id) == []
    assert not (data_paths.run_dir(task.run_id) / "capability_decisions.jsonl").exists()

    reviewer_calls = _reviewer_calls(calls)
    assert reviewer_calls
    assert all("--json-schema" in c for c in reviewer_calls)

    assert "Degradations:" not in format_job_report_text(reloaded)

    _cmd_run_show(task.run_id)
    assert "Degradations:" not in capsys.readouterr().out
