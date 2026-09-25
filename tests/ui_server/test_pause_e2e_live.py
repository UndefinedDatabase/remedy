"""F025 R7 T003 — DECISION F025 D5: the end-to-end pause/resume proof.

A live job is paused mid-build through the real HTTP door, parked, relaunched
through the real `remedy job run` (`python3 -m apps.cli.main job run <id>`, run
as an actual subprocess — not `run_job()` called in-process, because the
operator's own resume is the CLI's), and compared with an UNPAUSED CONTROL run
of the SAME job file: the normalized `_export_job` record, every workspace
file's bytes, and the ordered task-level event names (pause/resume events
excluded, since those are exactly what the two runs legitimately differ by).

Structured exactly like `test_pause_door_live.py`'s `TestJobScopeLiveDoor` and
`TestTaskScopeLiveDoor` — this file keeps its OWN copies of that file's
helpers, per that file's own header rule, rather than importing them. The one
behavioral difference from that file's `_RUNNER`: the fake provider here keeps
`create_provider("fake")`'s OWN defaults (`fail_on_round=1, pass_on_round=2` —
round 1 fails review, round 2 repairs and passes) and the CLI's own repair
rounds (`run_job`'s product default of 2, since neither a CLI flag nor a
persisted config overrides it) — never the door test's `pass_on_round=1,
fail_on_round=99, repair_rounds=0` shortcut, because DECISION F025 D5's control
run must behave exactly as an operator's unpaused `remedy job run` would.
"""
from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
import textwrap
import threading
import time
from http.client import HTTPConnection
from pathlib import Path
from typing import Any

import psutil
import pytest

from packages.orchestration.data_paths import job_record_path

CSRF_HEADER = "X-Remedy-CSRF"

_THREE_TASK_JOB = """\
# Job: Live E2E Pause Test

## Task 1
Add module one.

Acceptance:
- module exists

## Task 2
Add module two.

Acceptance:
- module exists

## Task 3
Add module three.

Acceptance:
- module exists
"""

#: Per-call sleep, long enough that an HTTP POST issued the instant the
#: metafile appears reliably lands while a call is in flight; short enough
#: that G5's mutation tool and G3's "twice more" re-runs stay fast even with
#: the real fake defaults' extra repair round per task.
_CALL_SLEEP_S = 0.3

#: SlowProvider adds ONLY a per-call sleep to `FakeProvider`'s OWN defaults —
#: no `pass_on_round`/`fail_on_round` override, unlike the door test's runner.
#: `run_job` is called BY NAME (`builder_name="fake"`), never by an injected
#: object, and with no `repair_rounds` kwarg (resolves to the product default
#: of 2) — exactly `_cmd_job_run`'s own path when no CLI flag is given. This
#: matters beyond style: `run_pingpong` calls `create_provider(name)` FRESH
#: FOR EVERY TASK when given a name instead of an object (`pingpong_job.py`'s
#: `builder_provider`/`reviewer_provider` params, left at their `None`
#: default, are only ever set by an INJECTED object — the CLI relaunch never
#: passes one). An object handed to `builder_provider=` instead, as the door
#: test's runner does, is reused for EVERY task in that one process, so its
#: build/review counters accumulate ACROSS tasks — after task 1 spends two
#: review calls to pass, task 2 and 3 pass on their first, needing no repair
#: at all. The real CLI relaunch, one task at a time from a `None` default,
#: gives every task ITS OWN fresh provider and its own round 1. Only
#: `create_provider` itself is monkeypatched (to add the sleep) — the
#: fresh-instance-per-task CONTRACT is left exactly as production has it — so
#: this runner's own single unpaused pass reproduces the SAME per-task round
#: count DECISION F025 D5's control needs to match a relaunched one.
_RUNNER = """\
import sys, time
from pathlib import Path
sys.path.insert(0, {repo!r})
from packages.orchestration.pingpong_job import parse_job_file, run_job
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration import pingpong_loop


class SlowFakeProvider(FakeProvider):
    '''A provider whose calls take real time, with `create_provider("fake")`'s
    OWN pass/fail rounds — nothing here knows anything about a pause.'''

    def build(self, prompt, **kwargs):
        time.sleep({sleep!r})
        return super().build(prompt, **kwargs)

    def review(self, prompt, **kwargs):
        time.sleep({sleep!r})
        return super().review(prompt, **kwargs)


_real_create_provider = pingpong_loop.create_provider


def _slow_create_provider(name, **kwargs):
    if name == "fake":
        return SlowFakeProvider()
    return _real_create_provider(name, **kwargs)


pingpong_loop.create_provider = _slow_create_provider

job = parse_job_file(Path({job_file!r}).read_text(), {target!r})
with Path({metafile!r}).open("w") as f:
    f.write(job.job_id + chr(10))
    for task in job.tasks:
        f.write(task.task_id + chr(10))

final = run_job(job.job_id, builder_name="fake", reviewer_name="fake")
print("FINAL:" + final.state, flush=True)
"""


# ---------------------------------------------------------------------------
# Helpers — own copies of test_pause_door_live.py's, per that file's header
# ---------------------------------------------------------------------------


def _test_owned_children(baseline_pids: set[int], tmp_path: Path) -> list[psutil.Process]:
    """Children this TEST is responsible for — nobody else's. Mirrors
    `test_pause_door_live.py`'s own helper of the same name exactly."""
    owned: list[psutil.Process] = []
    for child in psutil.Process().children(recursive=True):
        try:
            if child.pid in baseline_pids:
                continue
            if child.status() == psutil.STATUS_ZOMBIE:
                continue
            marker = str(tmp_path)
            cwd = ""
            with contextlib.suppress(psutil.Error):
                cwd = child.cwd() or ""
            cmdline = ""
            with contextlib.suppress(psutil.Error):
                cmdline = " ".join(child.cmdline())
            if marker in cwd or marker in cmdline:
                owned.append(child)
        except psutil.NoSuchProcess:
            continue
    return owned


def _start_ui_server_for_job(job_id: str, tmp_path: Path) -> tuple[int, str]:
    """Start a real UI server for `job_id` in a thread and return `(port, token)`.

    Mirrors `test_pause_door_live.py`'s helper of the same name and purpose —
    each live test file owns its own copy, the established convention here.
    """
    import secrets

    from packages.orchestration.ui_server import start_ui_server

    info_file = str(tmp_path / f"server_info_{secrets.token_hex(4)}.json")
    token = secrets.token_urlsafe(16)

    def run():
        try:
            start_ui_server(job_id, host="127.0.0.1", port=0, token=token,
                            open_browser=False, info_file=info_file)
        except (SystemExit, KeyboardInterrupt):
            pass

    from tests.ui_server.server_start import wait_for_server_info

    t = threading.Thread(target=run, daemon=True)
    t.start()
    return wait_for_server_info(info_file, t)["port"], token


def _post(port: int, token: str, command: str, *, job_id: str, nonce: str,
         args: dict | None = None) -> tuple[int, dict]:
    payload: dict = {"command": command, "client_nonce": nonce}
    if args is not None:
        payload["args"] = args
    conn = HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        conn.request("POST", f"/api/jobs/{job_id}/commands",
                     body=json.dumps(payload),
                     headers={"Authorization": f"Bearer {token}",
                              CSRF_HEADER: token,
                              "Content-Type": "application/json"})
        resp = conn.getresponse()
        return resp.status, json.loads(resp.read())
    finally:
        conn.close()


def _events(data_root: Path, job_id: str, event: str) -> list[dict]:
    runs = data_root / "job_logs" / job_id
    out: list[dict] = []
    for f in sorted(runs.glob("*.jsonl")) if runs.is_dir() else []:
        for line in f.read_text().splitlines():
            if line.strip():
                raw = json.loads(line)
                if raw.get("event") == event:
                    out.append(raw)
    return out


def _job_data(data_dir: Path, job_id: str) -> dict:
    return json.loads(job_record_path(job_id, data_dir).read_text())


# ---------------------------------------------------------------------------
# Helpers new to THIS file — DECISION F025 D5's control comparison
# ---------------------------------------------------------------------------


def _run_control(repo_root: Path, target: Path, data_dir: Path, tmp_path: Path,
                 label: str) -> str:
    """Run the SAME job file straight through, unpaused, by the SAME first
    runner — DECISION F025 D5's control. Returns the control job's id."""
    job_file = tmp_path / f"{label}_job.md"
    job_file.write_text(_THREE_TASK_JOB)
    metafile = tmp_path / f"{label}_meta.txt"
    script = tmp_path / f"{label}_runner.py"
    script.write_text(textwrap.dedent(_RUNNER).format(
        repo=str(repo_root), job_file=str(job_file), target=str(target),
        metafile=str(metafile), sleep=_CALL_SLEEP_S))

    env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))
    proc = subprocess.run([sys.executable, str(script)], env=env,
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, f"control runner exited {proc.returncode}: {proc.stderr}"
    assert "FINAL:completed" in proc.stdout, proc.stdout
    return metafile.read_text().splitlines()[0]


#: DECISION F025 D5 clause 3 — the removed-field list, written ONCE, each
#: entry carrying its reason. Applied by `_normalized_export` below to BOTH
#: the paused-then-relaunched job's export and the unpaused control's export
#: before they are compared whole. Every key named here is either unique in
#: `_export_job`'s shape or is popped from the ONE nested dict named beside
#: it, so nothing else the export carries is touched.
E4_REMOVED_FIELDS: list[tuple[str, str]] = [
    ("job_id", "the job id: `parse_job_file` mints a fresh one on every parse"),
    ("job_workspace_path", "a path containing the job id (`staging_<job id prefix>`)"),
    ("created_at", "a timestamp"),
    ("finished_at", "a timestamp"),
    ("first_running_at", "a timestamp"),
    ("budget_actuals", "carries the run's wall-clock started_at, a timestamp"),
    ("run_refs", "run references"),
    ("run_manifest.path", "a path containing the job id"),
    ("run_manifest.created_at", "a timestamp"),
    ("run_manifest.active_episode_id", "a run manifest episode field"),
    ("run_manifest.episode_start_workspace_tree", "a run manifest episode field"),
    ("run_manifest.input_snapshot", "a run manifest episode field"),
    ("run_manifest.input_snapshot_error", "a run manifest episode field"),
    ("run_manifest.episodes", "the run manifest's episodes"),
    ("run_manifest.error", "a run manifest episode field: the manifest's "
                           "per-episode call-expectation check reads a "
                           "relaunch's second episode against a task that "
                           "made its calls in the FIRST one and reports it "
                           "short, which a single-episode control never does"),
    ("tasks[].run_id", "a run id"),
    ("tasks[].task_start_tree_ref", "a run reference"),
    ("tasks[].task_start_recorded_at", "a timestamp"),
    ("tasks[].output_artifact_ids", "artifact ids"),
    ("tasks[].apply_manifest.run_id", "a run id"),
    ("tasks[].proof_summary.run_id", "a run id"),
    ("tasks[].apply_manifest.applied_file_proofs[].run_id", "a run id"),
    ("artifacts[].id", "an artifact id"),
    ("*_source", "a run reference: every config provenance label "
                 "(`execution_config`'s and the job's own `repair_rounds_source`) "
                 "reads 'persisted' after a relaunch and 'default' for a "
                 "single control run, for a value that is otherwise identical"),
]


def _strip_generic_keys(obj: Any, keys: set[str]) -> None:
    """Recursively pop every dict key in `keys`, or ending in `_source`
    (`execution_config`'s and the job's own `repair_rounds_source`: a RUN
    REFERENCE naming whether this run's config came from an earlier run's
    persisted state or the product default — a relaunch always reads
    "persisted" where a single control run reads "default", for a value that
    is otherwise identical), wherever either is nested."""
    if isinstance(obj, dict):
        for k in list(obj.keys()):
            if k in keys or k.endswith("_source"):
                obj.pop(k)
            else:
                _strip_generic_keys(obj[k], keys)
    elif isinstance(obj, list):
        for item in obj:
            _strip_generic_keys(item, keys)


def _normalized_export(job_id: str, data_dir: Path) -> dict:
    """`_export_job`, with E4_REMOVED_FIELDS's fields removed."""
    from packages.orchestration.pingpong_job import _export_job, load_job_plan

    os.environ["REMEDY_DATA_DIR"] = str(data_dir)
    try:
        job = load_job_plan(job_id)
        assert job is not None, f"job {job_id} not found under {data_dir}"
        payload = json.loads(json.dumps(_export_job(job)))
    finally:
        os.environ.pop("REMEDY_DATA_DIR", None)

    # Keys that are unique across the whole export (never legitimately meant
    # to survive comparison wherever they appear).
    generic_keys = {
        "job_id", "job_workspace_path", "created_at", "finished_at",
        "first_running_at", "budget_actuals", "run_refs", "run_id",
        "task_start_tree_ref", "task_start_recorded_at",
        "output_artifact_ids",
    }
    _strip_generic_keys(payload, generic_keys)

    # `created_at` is already gone via `generic_keys` above (it recurses).
    run_manifest = payload.get("run_manifest") or {}
    for key in ("path", "active_episode_id", "episode_start_workspace_tree",
                "input_snapshot", "input_snapshot_error", "episodes", "error"):
        run_manifest.pop(key, None)

    for artifact in payload.get("artifacts") or []:
        artifact.pop("id", None)

    return payload


def _workspace_bytes(path: str) -> dict[str, bytes]:
    root = Path(path)
    out: dict[str, bytes] = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(root))] = p.read_bytes()
    return out


#: E4's "ordered list of task-level event names with the pause and resume
#: events removed" — a task-level event is one `RunLogWriter.log` recorded
#: with a `task_id`; job-scope `job_paused`/`job_resumed` never carry one, and
#: task-scope `task_paused`/`task_resumed` do, so they are named explicitly.
_PAUSE_RESUME_EVENT_NAMES = {"job_paused", "job_resumed", "task_paused", "task_resumed"}


def _task_level_event_names(data_dir: Path, job_id: str) -> list[str]:
    """Ordered by each event's OWN `timestamp` field, never by which of the
    job's several run-log files (one per process — one per episode) a line
    happens to sit in: `new_run_id()` is a random UUID4, not a chronological
    one, so sorting the *files* by name (as `_events` above does, safely,
    since it only ever COUNTS a named event) would silently interleave a
    relaunch's episode ahead of the run it resumed.

    A JOB-SCOPE park's own `_log_task_started`/`_log_task_rounds` calls
    already ran for the task that was mid-call when the pause landed — S1's
    "every call already in flight finishes" — before that task rolled back
    to `pending` and ran again, in full, once relaunched. Its ABANDONED
    attempt's events are exactly what the park discards along with the
    attempt itself (nothing in the final export or the final workspace
    reflects it either — `_normalized_export` and `_workspace_bytes` only
    ever see the task's FINAL, committed run), so only the events from each
    task id's LAST `task_run_started` onward are kept — the same "final
    state only" principle the rest of E4's comparison already applies,
    carried into the ordered event list. A control task, started exactly
    once, is untouched by this filter."""
    runs = data_dir / "job_logs" / job_id
    records: list[dict] = []
    for f in sorted(runs.glob("*.jsonl")) if runs.is_dir() else []:
        for line in f.read_text().splitlines():
            if line.strip():
                records.append(json.loads(line))
    records.sort(key=lambda raw: raw.get("timestamp", ""))

    task_records = [r for r in records
                    if r.get("task_id") and r.get("event") not in _PAUSE_RESUME_EVENT_NAMES]
    last_start_index: dict[str, int] = {}
    for i, r in enumerate(task_records):
        if r["event"] == "task_run_started":
            last_start_index[r["task_id"]] = i
    final_attempt_only = [
        r for i, r in enumerate(task_records)
        if i >= last_start_index.get(r["task_id"], 0)
    ]
    return [r["event"] for r in final_attempt_only]


def _assert_matches_control(data_dir: Path, job_id: str, control_id: str) -> None:
    """DECISION F025 D5 clause 3 — EQUALITY, whole: the normalized export,
    every workspace file's bytes, and the ordered task-level event names."""
    actual = _normalized_export(job_id, data_dir)
    expected = _normalized_export(control_id, data_dir)
    assert actual == expected

    os.environ["REMEDY_DATA_DIR"] = str(data_dir)
    try:
        from packages.orchestration.pingpong_job import load_job_plan
        actual_job = load_job_plan(job_id)
        control_job = load_job_plan(control_id)
    finally:
        os.environ.pop("REMEDY_DATA_DIR", None)
    assert _workspace_bytes(actual_job.job_workspace_path) == \
        _workspace_bytes(control_job.job_workspace_path)

    assert _task_level_event_names(data_dir, job_id) == \
        _task_level_event_names(data_dir, control_id)


# ---------------------------------------------------------------------------
# E3 JOB SCOPE
# ---------------------------------------------------------------------------


@pytest.mark.subprocess
class TestJobScopeE2ELive:
    def test_pause_relaunch_through_the_cli_matches_an_unpaused_control(self, tmp_path):
        repo_root = Path(__file__).resolve().parents[2]
        target = tmp_path / "repo"
        target.mkdir()
        (target / "README.md").write_text("# demo\n")
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()

        job_file = tmp_path / "job.md"
        job_file.write_text(_THREE_TASK_JOB)
        metafile = tmp_path / "meta.txt"
        script = tmp_path / "runner.py"
        script.write_text(textwrap.dedent(_RUNNER).format(
            repo=str(repo_root), job_file=str(job_file), target=str(target),
            metafile=str(metafile), sleep=_CALL_SLEEP_S))

        env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))
        baseline = {c.pid for c in psutil.Process().children(recursive=True)}
        proc = subprocess.Popen([sys.executable, str(script)], env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        try:
            deadline = time.monotonic() + 60.0
            while time.monotonic() < deadline:
                if metafile.is_file() and metafile.read_text().strip():
                    break
                assert proc.poll() is None, "the runner exited before writing its metafile"
                time.sleep(0.02)
            else:
                pytest.fail("the runner never wrote its metafile within 60s")
            job_id = metafile.read_text().splitlines()[0]

            # Wait for task 1 to complete (durably applied) before pausing, so
            # the pause lands during task 2's own call — one already in flight.
            deadline = time.monotonic() + 90.0
            while time.monotonic() < deadline:
                job_json = job_record_path(job_id, data_dir)
                if job_json.is_file():
                    statuses = [t["status"] for t in json.loads(job_json.read_text() or "{}")
                               .get("tasks", [])]
                    if statuses and statuses[0] == "applied_to_job_workspace":
                        break
                assert proc.poll() is None, "the runner exited before task 1 completed"
                time.sleep(0.02)
            else:
                pytest.fail("task 1 never completed within 90s")

            task1_run_id = _job_data(data_dir, job_id)["tasks"][0]["run_id"]

            os.environ["REMEDY_DATA_DIR"] = str(data_dir)
            try:
                port, token = _start_ui_server_for_job(job_id, tmp_path)
                status, body = _post(port, token, "job.pause", job_id=job_id,
                                     nonce="n-pause")
                assert status == 200, body
                assert body["outcome"] == "requested", body
            finally:
                os.environ.pop("REMEDY_DATA_DIR", None)

            out, err = proc.communicate(timeout=120)
            assert proc.returncode == 0, f"runner exited {proc.returncode}: {err}"
            assert "FINAL:paused" in out, out
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=30)

        data = _job_data(data_dir, job_id)
        assert data["status"] == "paused"
        assert data["pause"]["scope"] == "job"
        assert not psutil.pid_exists(proc.pid) or \
            psutil.Process(proc.pid).status() == psutil.STATUS_ZOMBIE
        assert _test_owned_children(baseline, tmp_path) == []

        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            status, body = _post(port, token, "job.unpause", job_id=job_id,
                                 nonce="n-unpause")
            assert status == 200, body
            assert body["outcome"] == "parked", body
            relaunch = body["next"]
            assert relaunch == f"remedy job run {job_id}", body
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

        # "Running that command" — the real CLI, as a subprocess, exactly the
        # way the operator would type it (DECISION F025 D5 clause 1).
        relaunch_env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir),
                            PYTHONPATH=str(repo_root))
        relaunch_proc = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id],
            cwd=str(repo_root), env=relaunch_env, capture_output=True, text=True,
            timeout=120)
        assert relaunch_proc.returncode == 0, (
            f"relaunch exited {relaunch_proc.returncode}: {relaunch_proc.stderr}")

        resumed = _job_data(data_dir, job_id)
        assert resumed["status"] == "completed"
        assert len(_events(data_dir, job_id, "job_resumed")) == 1
        # The task finished before the park keeps its run id — never run again.
        assert resumed["tasks"][0]["run_id"] == task1_run_id
        assert _test_owned_children(baseline, tmp_path) == []

        control_id = _run_control(repo_root, target, data_dir, tmp_path, "job_scope_control")
        _assert_matches_control(data_dir, job_id, control_id)


# ---------------------------------------------------------------------------
# E3 TASK SCOPE
# ---------------------------------------------------------------------------


@pytest.mark.subprocess
class TestTaskScopeE2ELive:
    def test_pause_relaunch_through_the_cli_matches_an_unpaused_control(self, tmp_path):
        repo_root = Path(__file__).resolve().parents[2]
        target = tmp_path / "repo"
        target.mkdir()
        (target / "README.md").write_text("# demo\n")
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()

        job_file = tmp_path / "job.md"
        job_file.write_text(_THREE_TASK_JOB)
        metafile = tmp_path / "meta.txt"
        script = tmp_path / "runner.py"
        script.write_text(textwrap.dedent(_RUNNER).format(
            repo=str(repo_root), job_file=str(job_file), target=str(target),
            metafile=str(metafile), sleep=_CALL_SLEEP_S))

        env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))
        proc = subprocess.Popen([sys.executable, str(script)], env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True)
        try:
            deadline = time.monotonic() + 60.0
            while time.monotonic() < deadline:
                if metafile.is_file() and len(metafile.read_text().splitlines()) >= 4:
                    break
                assert proc.poll() is None, "the runner exited before writing its metafile"
                time.sleep(0.02)
            else:
                pytest.fail("the runner never wrote its metafile within 60s")
            lines = metafile.read_text().splitlines()
            job_id, task_ids = lines[0], lines[1:4]
            third_task_id = task_ids[2]

            os.environ["REMEDY_DATA_DIR"] = str(data_dir)
            try:
                port, token = _start_ui_server_for_job(job_id, tmp_path)
                # Named WHILE task 1 runs — "before it starts": the third task
                # is never dispatched at all.
                status, body = _post(port, token, "job.pause", job_id=job_id,
                                     nonce="n-pause-task", args={"task": third_task_id})
                assert status == 200, body
                assert (body["outcome"], body["task_id"]) == ("paused", third_task_id), body
            finally:
                os.environ.pop("REMEDY_DATA_DIR", None)

            out, err = proc.communicate(timeout=120)
            assert proc.returncode == 0, f"runner exited {proc.returncode}: {err}"
            assert "FINAL:paused" in out, out
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=30)

        data = _job_data(data_dir, job_id)
        assert data["status"] == "paused"
        assert data["pause"]["scope"] == "task"
        statuses = [t["status"] for t in data["tasks"]]
        assert statuses[2] == "pending"

        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            status, body = _post(port, token, "job.unpause", job_id=job_id,
                                 nonce="n-unpause-task", args={"task": third_task_id})
            assert status == 200, body
            assert (body["outcome"], body["task_id"]) == ("released", third_task_id), body
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

        relaunch_env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir),
                            PYTHONPATH=str(repo_root))
        relaunch_proc = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id],
            cwd=str(repo_root), env=relaunch_env, capture_output=True, text=True,
            timeout=120)
        assert relaunch_proc.returncode == 0, (
            f"relaunch exited {relaunch_proc.returncode}: {relaunch_proc.stderr}")

        resumed = _job_data(data_dir, job_id)
        assert resumed["status"] == "completed"
        assert all(t["status"] == "applied_to_job_workspace" for t in resumed["tasks"])

        control_id = _run_control(repo_root, target, data_dir, tmp_path, "task_scope_control")
        _assert_matches_control(data_dir, job_id, control_id)
