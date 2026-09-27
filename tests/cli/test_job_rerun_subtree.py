"""F029 T002, DECISION F029 D3 — `remedy job rerun-subtree`.

Modelled on `test_job_veto.py`: the CLI handler is proved through the real argv
dispatcher, over the three-task job of `test_subtree_rerun_prepare.py`'s
end-to-end harness, run to `completed`. The estimate and the preparation
themselves are proved in `tests/orchestration/test_subtree_rerun_prepare.py`;
this file proves the CLI's wrapping: the task-argument resolution, the cost
preview it shows before anything is touched, the exit code each refusal maps
to, and the JSON envelope.
"""
from __future__ import annotations

import json
from pathlib import Path

from packages.core.models import RunState
from packages.orchestration import worktrees as W
from packages.orchestration.data_paths import job_record_path
from packages.orchestration.pingpong_job import job_worktree_id, load_job_plan, save_job_plan
from tests.orchestration.test_subtree_rerun_prepare import (  # noqa: F401 - reused fixture/helpers
    _run_three_task_job,
    isolate_data_root,
    repo,
)


def _run(argv: list[str], capsys) -> tuple[int, str]:
    from apps.cli.grouped import main

    try:
        code = main(argv)
    except SystemExit as exc:
        code = exc.code
    return (code or 0), capsys.readouterr().out


def _completed_job(repo_path, monkeypatch):
    job = _run_three_task_job(repo_path, monkeypatch)
    assert job.state == "completed"
    return job


class TestRerunSubtreeJSON:
    def test_yes_json_prepares_the_rerun_with_estimate_and_run_command(self, repo, monkeypatch, capsys):
        job = _completed_job(repo, monkeypatch)
        job_id = job.job_id

        code, out = _run(
            ["job", "rerun-subtree", job_id, "T002", "--yes", "--json"], capsys)

        assert code == 0
        body = json.loads(out)
        assert body["ok"] is True
        assert body["subtree"] == ["T002", "T003"]
        assert body["run_command"] == f"remedy job run {job_id}"
        assert set(body["estimate"]) == {"band_usd_low", "band_usd_high", "basis"}

    def test_model_override_reaches_the_record(self, repo, monkeypatch, capsys):
        job = _completed_job(repo, monkeypatch)
        job_id = job.job_id

        code, out = _run(
            ["job", "rerun-subtree", job_id, "T002", "--model", "rerun-model", "--yes", "--json"],
            capsys)

        assert code == 0
        body = json.loads(out)
        assert body["model"]["override"] == "rerun-model"


class TestRerunSubtreeHuman:
    def test_last_line_is_the_run_command(self, repo, monkeypatch, capsys):
        job = _completed_job(repo, monkeypatch)
        job_id = job.job_id

        code, out = _run(["job", "rerun-subtree", job_id, "T002", "--yes"], capsys)

        assert code == 0
        lines = out.strip().splitlines()
        assert lines[-1] == f"Run it with: remedy job run {job_id}"
        assert f"Rerun rerun-1 prepared for job {job_id}" in out


class TestRerunSubtreeConfirmation:
    def test_without_yes_non_tty_is_confirmation_required(self, repo, monkeypatch, capsys):
        job = _completed_job(repo, monkeypatch)
        job_id = job.job_id
        before = job_record_path(job_id).read_bytes()

        code, out = _run(["job", "rerun-subtree", job_id, "T002", "--json"], capsys)

        assert code == 2
        body = json.loads(out)
        assert body["error"] == "confirmation_required"
        assert job_record_path(job_id).read_bytes() == before

    def test_a_declined_prompt_changes_nothing(self, repo, monkeypatch, capsys):
        from apps.cli import cost_preview_confirm

        job = _completed_job(repo, monkeypatch)
        job_id = job.job_id
        before = job_record_path(job_id).read_bytes()
        monkeypatch.setattr(cost_preview_confirm, "_stdin_is_a_tty", lambda: True)
        monkeypatch.setattr("builtins.input", lambda *a, **k: "n")

        code, out = _run(["job", "rerun-subtree", job_id, "T002"], capsys)

        assert code == 0
        assert "Cancelled. Nothing was changed." in out
        assert job_record_path(job_id).read_bytes() == before


class TestRerunSubtreeRefusalExitCodes:
    def test_unknown_task_exits_2_with_no_preview_printed(self, repo, monkeypatch, capsys):
        job = _completed_job(repo, monkeypatch)
        job_id = job.job_id

        code, out = _run(
            ["job", "rerun-subtree", job_id, "no-such-task", "--json"], capsys)

        assert code == 2
        body = json.loads(out)
        assert body["error"] == "unknown_task"
        assert "estimated" not in out

    def test_model_invalid_exits_2(self, repo, monkeypatch, capsys):
        job = _completed_job(repo, monkeypatch)
        job_id = job.job_id

        code, out = _run(
            ["job", "rerun-subtree", job_id, "T002", "--model", "bad model!", "--yes", "--json"],
            capsys)

        assert code == 2
        assert json.loads(out)["error"] == "model_invalid"

    def test_job_running_exits_3(self, repo, monkeypatch, capsys):
        job = _completed_job(repo, monkeypatch)
        job.state = RunState.RUNNING
        save_job_plan(job)

        code, out = _run(
            ["job", "rerun-subtree", job.job_id, "T002", "--yes", "--json"], capsys)

        assert code == 3
        assert json.loads(out)["error"] == "job_running"

    def test_interleaved_exits_3_with_facts(self, repo, monkeypatch, capsys):
        job = _completed_job(repo, monkeypatch)
        job_id = job.job_id

        # A hand-made commit outside the subtree touches a path the subtree owns.
        handle = W.create(job_worktree_id(job_id), job.repo_path)
        (Path(handle.path) / "task2.txt").write_text("hand edit\n")
        message = f"manual edit\n\n{W.REMEDY_JOB_TRAILER}: {job_id}\n"
        sha = W.commit_job_worktree(handle.path, message)
        W.remove(handle, keep_branch=True)

        reloaded = load_job_plan(job_id)
        reloaded.worktree_head = sha
        save_job_plan(reloaded)

        code, out = _run(
            ["job", "rerun-subtree", job_id, "T002", "--yes", "--json"], capsys)

        assert code == 3
        body = json.loads(out)
        assert body["error"] == "interleaved"
        assert "interleaving" in body["facts"]

    def test_a_job_that_does_not_exist_exits_one(self, capsys):
        code, out = _run(
            ["job", "rerun-subtree", "0123456789abcdef", "T001", "--json"], capsys)
        assert code == 1
        assert json.loads(out)["error"] == "invalid_job_id"
