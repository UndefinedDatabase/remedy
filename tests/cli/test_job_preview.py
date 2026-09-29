"""`remedy job preview-start` and `remedy job preview-stop` (F041 T002, DECISION F041 D3).

The runtime verbs are replaced by a scripted stand-in on the command module, so these tests pin
what the command answers for each ending of the preview, not the harness itself.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from apps.cli.commands import job_preview_cmd
from apps.cli.commands.job_preview_cmd import COMMAND_HANDLERS, _cmd_job_preview
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.preview_control import VerbResult, load_preview

SERVED = VerbResult(True, {"ok": True, "url": "http://127.0.0.1:5173/", "port": 5173})
PROBED = VerbResult(True, {"ok": True, "url": "http://127.0.0.1:5173/", "port": 5173})
STOPPED = VerbResult(True, {"ok": True})
NO_RUNTIME = VerbResult(False, {"ok": False, "error": "runtime_config_error",
                                "message": "no runtime detected"})
BAD_PROBE = VerbResult(False, {"ok": False, "error": "runtime_not_ready",
                               "message": "health status 500"})


@pytest.fixture
def job(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    project = tmp_path / "project"
    project.mkdir()
    plan = JobPlan(job_title="f041-preview-cli-job", user_prompt="preview",
                   tasks=[TaskEntry(title="t")], repo_path=str(project))
    save_job_plan(plan)
    return plan


def _script(monkeypatch, **answers):
    calls: list[tuple[str, Path]] = []

    def runner(verb, root):
        calls.append((verb, root))
        return answers[verb]

    monkeypatch.setattr(job_preview_cmd, "run_runtime_verb", runner)
    return calls


def _json(capsys) -> dict:
    return json.loads(capsys.readouterr().out)


def test_both_commands_are_registered():
    assert set(COMMAND_HANDLERS) == {"job.preview-start", "job.preview-stop"}


def test_a_start_that_probes_answers_the_link(job, monkeypatch, capsys):
    calls = _script(monkeypatch, serve=SERVED, probe=PROBED)
    _cmd_job_preview(str(job.job_id), "start", json_output=True)
    data = _json(capsys)
    assert [verb for verb, _ in calls] == ["serve", "probe"]
    assert (data["ok"], data["job_id"], data["state"], data["url"], data["port"]) == (
        True, str(job.job_id), "live", "http://127.0.0.1:5173/", 5173)


def test_a_start_the_probe_refuses_exits_1_with_no_link(job, monkeypatch, capsys):
    _script(monkeypatch, serve=SERVED, probe=BAD_PROBE, stop=STOPPED)
    with pytest.raises(SystemExit) as exit_info:
        _cmd_job_preview(str(job.job_id), "start", json_output=True)
    assert exit_info.value.code == 1
    data = _json(capsys)
    assert (data["ok"], data["error"], data["state"], data["url"]) == (
        False, "preview_failed", "failed", "")
    assert data["message"] == "started but health check failed: health status 500"


def test_a_project_without_a_runtime_exits_1_as_not_applicable(job, monkeypatch, capsys):
    _script(monkeypatch, serve=NO_RUNTIME)
    with pytest.raises(SystemExit) as exit_info:
        _cmd_job_preview(str(job.job_id), "start", json_output=True)
    assert exit_info.value.code == 1
    data = _json(capsys)
    assert (data["error"], data["state"], data["message"]) == (
        "preview_not_applicable", "not_applicable", "no runtime detected")


def test_a_stop_answers_stopped(job, monkeypatch, capsys):
    _script(monkeypatch, serve=SERVED, probe=PROBED, stop=STOPPED)
    _cmd_job_preview(str(job.job_id), "start", json_output=True)
    capsys.readouterr()
    _cmd_job_preview(str(job.job_id), "stop", json_output=False)
    assert capsys.readouterr().out == f"The preview of job {job.job_id} is stopped.\n"
    assert load_preview(str(job.job_id))["state"] == "stopped"


def test_the_text_answer_names_the_link(job, monkeypatch, capsys):
    _script(monkeypatch, serve=SERVED, probe=PROBED)
    _cmd_job_preview(str(job.job_id), "start", json_output=False)
    assert capsys.readouterr().out == (
        f"The preview of job {job.job_id} is live at http://127.0.0.1:5173/.\n")


def test_an_unknown_job_exits_3(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    calls = _script(monkeypatch)
    with pytest.raises(SystemExit) as exit_info:
        _cmd_job_preview("0123456789abcdef0123456789abcdef", "start", json_output=True)
    assert exit_info.value.code == 3
    assert _json(capsys)["error"] == "job_not_found"
    assert calls == []
