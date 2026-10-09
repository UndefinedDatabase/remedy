"""F253 round 23 — `remedy client run <job> [--json]` reads the run the supervisor started for a
job as a record of its own (DECISION F253 D20), as `remedy client order` reads an order.

Every `remedy` call here is a subprocess, so its `cwd` and its `REMEDY_DATA_DIR` are exactly a real
client's. Each run is started through `RunLauncher` on a scratch data root with a stand-in
`argv_for`, a small script that prints one envelope and exits 0; no real provider and no real
`remedy job run` is involved.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan
from packages.orchestration.serve_paths import serve_paths
from packages.orchestration.serve_runs import RunLauncher

REPO_ROOT = Path(__file__).resolve().parents[2]

#: A stand-in for `remedy job run`: prints one envelope and exits 0 at once. The job id is its
#: first argument, so the run's command line names the job.
_ENDED_RUN_CHILD = (
    'import json, sys; print(json.dumps({"ok": True, "job_id": sys.argv[1], "stand_in": True}))')


def _subprocess_env(data_root: Path) -> dict[str, str]:
    """A fresh copy of `os.environ`, read at call time: never a module-level snapshot, which would
    freeze before a test's own data root is known."""
    return {**os.environ, "PYTHONPATH": str(REPO_ROOT), "REMEDY_DATA_DIR": str(data_root)}


def _remedy(args: list[str], cwd: Path, data_root: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", *args],
        cwd=str(cwd), capture_output=True, text=True, env=_subprocess_env(data_root), timeout=60)
    return result.returncode, result.stdout


def _saved_job(data_root: Path, monkeypatch) -> str:
    """The full id of a job saved on DATA_ROOT, so a prefix of it can be looked up."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))
    job = JobPlan(job_title="client-run-job", user_prompt="Client run prompt",
                  tasks=[TaskEntry(title="Write a page")])
    save_job_plan(job)
    return str(job.job_id)


def _start_ended_run(data_root: Path, job_id: str) -> None:
    """Start the stand-in run of JOB_ID and wait until its end is recorded."""
    launcher = RunLauncher(
        serve_paths(data_root),
        argv_for=lambda job: [sys.executable, "-c", _ENDED_RUN_CHILD, job])
    launcher.start(job_id)
    assert launcher.wait(job_id, timeout=30) == 0


def test_the_answer_names_an_ended_runs_keys_and_values(tmp_path, monkeypatch):
    data_root = tmp_path / "data"
    job_id = _saved_job(data_root, monkeypatch)
    _start_ended_run(data_root, job_id)

    code, out = _remedy(["client", "run", job_id, "--json"], tmp_path, data_root)

    assert code == 0, out
    body = json.loads(out)
    assert body["ok"] is True
    assert body["job_id"] == job_id
    assert body["state"] == "ended"
    assert body["exit_code"] == 0
    assert body["started_at"] and body["ended_at"]
    assert Path(body["out_log"]).name == f"{job_id}.out"
    assert body["answer"] == {"ok": True, "job_id": job_id, "stand_in": True}


def test_a_job_prefix_answers_as_the_full_id_does(tmp_path, monkeypatch):
    data_root = tmp_path / "data"
    job_id = _saved_job(data_root, monkeypatch)
    _start_ended_run(data_root, job_id)

    full_code, full_out = _remedy(["client", "run", job_id, "--json"], tmp_path, data_root)
    prefix_code, prefix_out = _remedy(["client", "run", job_id[:8], "--json"], tmp_path, data_root)

    assert (full_code, prefix_code) == (0, 0), (full_out, prefix_out)
    assert json.loads(prefix_out) == json.loads(full_out)


def test_a_saved_job_with_no_run_record_is_run_not_found(tmp_path, monkeypatch):
    data_root = tmp_path / "data"
    job_id = _saved_job(data_root, monkeypatch)

    code, out = _remedy(["client", "run", job_id, "--json"], tmp_path, data_root)

    assert code == 3, out
    body = json.loads(out)
    assert (body["ok"], body["error"]) == (False, "run_not_found")
    assert job_id in body["message"]


@pytest.mark.parametrize("bad_value", ["00000000-0000-4000-8000-000000000000", "../x", "zz"])
def test_an_unknown_full_id_or_a_value_that_is_no_id_is_run_not_found(tmp_path, bad_value):
    data_root = tmp_path / "data"

    code, out = _remedy(["client", "run", bad_value, "--json"], tmp_path, data_root)

    assert code == 3, out
    body = json.loads(out)
    assert (body["ok"], body["error"]) == (False, "run_not_found")
    assert bad_value in body["message"]


def test_the_summary_without_json_names_the_state(tmp_path, monkeypatch):
    data_root = tmp_path / "data"
    job_id = _saved_job(data_root, monkeypatch)
    _start_ended_run(data_root, job_id)

    code, out = _remedy(["client", "run", job_id], tmp_path, data_root)

    assert code == 0, out
    assert f"Run of job {job_id}: ended" in out
