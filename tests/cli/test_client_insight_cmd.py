"""F311 R3 C6 — `remedy client now` and `remedy client insight <job>`, the insight's twins
(DECISION F311 D1), driving the real command line as tests/cli/test_client_interface.py drives
`remedy client story`.

Every `remedy` call here is a subprocess, so its `cwd`, its `REMEDY_DATA_DIR` and its
`REMEDY_OLLAMA_HOST` are exactly a real client's; the host is pointed at a closed local port, so
`job_insight.model_server_state`'s one probe reaches no real model server.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from packages.common.secure_fs import durable_write_json
from packages.core.models import RunState
from packages.orchestration import data_paths
from packages.orchestration.pingpong_job import TASK_RUNNING, JobPlan, TaskEntry, save_job_plan
from packages.orchestration.worker_pulse import WORKER_PULSE_VERSION

REPO_ROOT = Path(__file__).resolve().parents[2]
#: A port nothing listens on, so the probe `model_server_state` makes refuses at once.
_CLOSED_OLLAMA_HOST = "http://127.0.0.1:9"


def _subprocess_env(data_root: Path) -> dict[str, str]:
    """A fresh copy of `os.environ`, read at call time: never a module-level snapshot, which would
    freeze before a test's own data root is known."""
    return {**os.environ, "PYTHONPATH": str(REPO_ROOT), "REMEDY_DATA_DIR": str(data_root),
           "REMEDY_OLLAMA_HOST": _CLOSED_OLLAMA_HOST}


def _remedy(args: list[str], cwd: Path, data_root: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", *args],
        cwd=str(cwd), capture_output=True, text=True, env=_subprocess_env(data_root), timeout=60)
    return result.returncode, result.stdout


def _running_job(data_root: Path, monkeypatch, *, job_id: str | None = None) -> str:
    """A saved RUNNING job with one running task, on DATA_ROOT."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_root))
    kwargs = {"job_id": job_id} if job_id is not None else {}
    job = JobPlan(job_title="insight-cmd-job", tasks=[TaskEntry(title="write", status=TASK_RUNNING)],
                 state=RunState.RUNNING, **kwargs)
    save_job_plan(job)
    return str(job.job_id)


def _write_pulse(job_id: str, *, stream: list) -> None:
    """A fresh worker pulse for JOB_ID, its own folder already resolved by `REMEDY_DATA_DIR`."""
    now = datetime.now(timezone.utc)
    started = (now - timedelta(seconds=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
    last = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    path = data_paths.worker_pulse_path(job_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    durable_write_json(path, {
        "version": WORKER_PULSE_VERSION, "job_id": job_id, "bound_at": started,
        "role": "builder", "provider": "pi", "model": "m", "round": 1,
        "call_kind": "attempt", "call_started_at": started, "call_ended_at": None,
        "last_output_at": last, "stream": stream,
    })


def test_now_json_answers_the_saved_running_jobs_entry_with_phase_worker_and_stall_reason(
    tmp_path, monkeypatch,
):
    data_root = tmp_path / "data"
    job_id = _running_job(data_root, monkeypatch)
    _write_pulse(job_id, stream=[])

    code, out = _remedy(["client", "now", "--json"], tmp_path, data_root)

    assert code == 0, out
    body = json.loads(out)
    assert body["ok"] is True
    [entry] = body["jobs"]
    assert entry["job"] == job_id
    assert entry["phase"] == "build"
    assert entry["worker"] == {"role": "builder", "provider": "pi", "model": "m"}
    # The model server is unreachable by this test's own design, so a Pi worker reads that reason.
    assert entry["stall_reason"] == "model_unreachable" and entry["stalled"] is True
    assert body["model_server"]["state"] == "unreachable"


def test_insight_by_prefix_json_with_lines_2_answers_the_last_two_stream_entries_and_advice(
    tmp_path, monkeypatch,
):
    data_root = tmp_path / "data"
    job_id = _running_job(data_root, monkeypatch)
    stream = [{"at": f"t{n}", "role": "builder", "kind": "system", "text": str(n)} for n in range(5)]
    _write_pulse(job_id, stream=stream)

    code, out = _remedy(["client", "insight", job_id[:8], "--json", "--lines", "2"], tmp_path, data_root)

    assert code == 0, out
    body = json.loads(out)
    assert body["ok"] is True
    assert body["job"] == job_id
    assert [entry["text"] for entry in body["stream"]] == ["3", "4"]
    # Unreachable by this test's own design: a Pi worker reads model_unreachable, advice wait/stop.
    assert body["advice"] == ["wait", "stop"]


def test_lines_abc_answers_the_defaults_slice(tmp_path, monkeypatch):
    data_root = tmp_path / "data"
    job_id = _running_job(data_root, monkeypatch)
    stream = [{"at": f"t{n}", "role": "builder", "kind": "system", "text": str(n)} for n in range(3)]
    _write_pulse(job_id, stream=stream)

    code, out = _remedy(["client", "insight", job_id, "--json", "--lines", "abc"], tmp_path, data_root)

    assert code == 0, out
    body = json.loads(out)
    assert [entry["text"] for entry in body["stream"]] == ["0", "1", "2"]


def test_an_unknown_id_is_invalid_job_id_exit_1(tmp_path):
    data_root = tmp_path / "data"

    code, out = _remedy(["client", "insight", "deadbeefdeadbeef", "--json"], tmp_path, data_root)

    assert code == 1, out
    body = json.loads(out)
    assert (body["ok"], body["error"]) == (False, "invalid_job_id")


def test_an_ambiguous_prefix_exits_2_with_ambiguous_job_id(tmp_path, monkeypatch):
    data_root = tmp_path / "data"
    _running_job(data_root, monkeypatch, job_id="aaaaaaaa00000001")
    _running_job(data_root, monkeypatch, job_id="aaaaaaaa00000002")

    code, out = _remedy(["client", "insight", "aaaaaaaa", "--json"], tmp_path, data_root)

    assert code == 2, out
    body = json.loads(out)
    assert (body["ok"], body["error"]) == (False, "ambiguous_job_id")
    assert body["matches"] == ["aaaaaaaa00000001", "aaaaaaaa00000002"]


def test_the_human_lines_match_c5s_wording(tmp_path, monkeypatch):
    data_root = tmp_path / "data"
    job_id = _running_job(data_root, monkeypatch)
    _write_pulse(job_id, stream=[])

    now_code, now_out = _remedy(["client", "now"], tmp_path, data_root)
    insight_code, insight_out = _remedy(["client", "insight", job_id], tmp_path, data_root)

    assert now_code == 0, now_out
    assert now_out == "1 job(s) running, 0 order(s) waiting, model server unreachable\n"
    assert insight_code == 0, insight_out
    # The model server is unreachable by this test's own design: a Pi worker reads that reason.
    assert insight_out == f"Job {job_id}: build, stalled (model_unreachable), advice: wait, stop\n"
