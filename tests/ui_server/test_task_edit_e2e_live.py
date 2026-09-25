"""F026 R4 S6 — the live end-to-end: a planned job fails through the CLI, is
edited through the real door, is relaunched through the CLI, and its new
trace and its ledger show the edit and the second run.

Structured like `test_pause_e2e_live.py`'s own live classes — `@pytest.mark.subprocess`,
a real UI server started in a thread, and a real POST through `HTTPConnection` — and
this file keeps its OWN copies of that file's server-start and POST helpers, per
that file's own header rule, rather than importing them. The plan itself is saved
directly (mirroring `tests/orchestration/test_task_edit_runtime.py`'s `_save_job`),
an APPROVED two-task plan rather than a job markdown file, because a runtime task
edit is gated on the plan being approved (DECISION F026 D1) and the job-markdown
door test_pause_e2e_live.py uses never produces one.
"""
from __future__ import annotations

import json
import os
import secrets
import subprocess
import sys
import threading
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.orchestration.data_paths import job_record_path, run_dir
from packages.orchestration.job_plan import APPROVED_PLAN_HASH_KEY, map_task_plan_to_tasks, plan_content_hash
from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables

CSRF_HEADER = "X-Remedy-CSRF"

_OLD_MARKER = "OLDTASKEDITMARKERF026"
_NEW_MARKER = "NEWTASKEDITMARKERF026"


def _task(tid: str, deps: list[str], goal: str, acceptance: list[str]) -> dict:
    # `files_hint` names "docs/README.md", the file the fixture repo holds and
    # the one `FakeProvider`'s own default `builder_files` writes — the same
    # pairing `tests/orchestration/test_task_edit_runtime.py`'s trace-proof
    # fixture uses.
    return {
        "id": tid, "title": f"Build {tid}", "goal": goal, "acceptance": acceptance,
        "depends_on": deps, "est_tokens_band": "S", "files_hint": ["docs/README.md"],
    }


def _save_approved_two_task_job(root: Path, repo_path: Path) -> str:
    """An APPROVED two-task plan, saved directly (mirrors
    `test_task_edit_runtime.py`'s `_save_job`): T1 carries the OLD marker in
    its goal and acceptance, T2 depends on T1."""
    tasks = [
        _task("T1", [], f"{_OLD_MARKER} goal", [f"{_OLD_MARKER} acceptance"]),
        _task("T2", ["T1"], "goal of T2", ["T2 works"]),
    ]
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": tasks})
    body = plan.model_dump()
    body["_approval"] = "approved"
    body["_normalization"] = []
    body[APPROVED_PLAN_HASH_KEY] = plan_content_hash(body)
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = JobPlan(job_title="F026 R4 live e2e", task_plan=body, tasks=mapped,
                 repo_path=str(repo_path))
    save_job_plan(job, root)
    return job.job_id


# ---------------------------------------------------------------------------
# Helpers — own copies of test_pause_e2e_live.py's, per that file's header rule
# ---------------------------------------------------------------------------


def _start_ui_server_for_job(job_id: str, tmp_path: Path) -> tuple[int, str]:
    """Start a real UI server for `job_id` in a thread and return `(port, token)`."""
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


def _job_data(data_dir: Path, job_id: str) -> dict:
    return json.loads(job_record_path(job_id, data_dir).read_text())


# ---------------------------------------------------------------------------
# Helpers new to THIS file — S6's paged events-since read
# ---------------------------------------------------------------------------


def _get_events_since(port: int, token: str, job_id: str, cursor: str) -> dict:
    conn = HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        conn.request("GET", f"/api/jobs/{job_id}/events-since?token={token}&cursor={cursor}")
        resp = conn.getresponse()
        assert resp.status == 200
        return json.loads(resp.read())
    finally:
        conn.close()


def _all_events_since(port: int, token: str, job_id: str) -> list[dict]:
    """Every event `events-since` will hand back, paged from cursor 0 —
    `_build_events_since_json` caps one page at 50, so a job with more events
    than that needs more than one request to read them all."""
    events: list[dict] = []
    cursor = "0"
    while True:
        body = _get_events_since(port, token, job_id, cursor)
        events.extend(body["events"])
        next_cursor = body["cursor"]
        if next_cursor == cursor or not body["events"]:
            break
        cursor = next_cursor
    return events


@pytest.mark.subprocess
class TestTaskEditE2ELive:
    def test_fail_edit_through_the_door_relaunch_reads_the_trace_and_the_fan(self, tmp_path):
        repo_root = Path(__file__).resolve().parents[2]
        repo = tmp_path / "repo"
        (repo / "docs").mkdir(parents=True)
        (repo / "README.md").write_text("# Demo\n")
        (repo / "docs" / "README.md").write_text("# Docs\n")

        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()

        job_id = _save_approved_two_task_job(data_dir, repo)
        env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))

        # --- run 1: fails through the real CLI, in a subprocess -------------
        run1 = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id,
             "--builder-provider", "fake", "--reviewer-provider", "fake",
             "--max-rounds", "1", "--repair-rounds", "0"],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
        assert run1.returncode == 0, f"run 1 exited {run1.returncode}: {run1.stderr}"

        blocked = _job_data(data_dir, job_id)
        assert blocked["status"] == "blocked"
        by_planned = {t["inputs"]["plan"]["planned_id"]: t for t in blocked["tasks"]}
        t1_blocked, t2_blocked = by_planned["T1"], by_planned["T2"]
        assert t1_blocked["status"] == "blocked"
        assert t2_blocked["status"] == "skipped"
        t1_task_id = t1_blocked["task_id"]
        t2_task_id = t2_blocked["task_id"]
        old_run_id = t1_blocked["run_id"]
        assert old_run_id

        # --- the edit, through the real door --------------------------------
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            status, body = _post(
                port, token, "job.edit-task", job_id=job_id, nonce="n-edit-t1",
                args={"task_id": t1_task_id,
                      "fields": {"goal": f"{_NEW_MARKER} goal",
                                "acceptance": [f"{_NEW_MARKER} acceptance"]},
                      "expected_version": 1})
            assert status == 200, body
            assert body["spec_version"] == 2, body
            assert t2_task_id in body["restored"], body
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

        # --- run 2: the relaunch, through the real CLI ----------------------
        run2 = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id,
             "--max-rounds", "3", "--repair-rounds", "2"],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
        assert run2.returncode == 0, f"run 2 exited {run2.returncode}: {run2.stderr}"

        done = _job_data(data_dir, job_id)
        assert done["status"] == "completed"
        assert all(t["status"] == "applied_to_job_workspace" for t in done["tasks"])
        assert done["error"] == ""

        done_t1 = next(t for t in done["tasks"] if t["task_id"] == t1_task_id)
        new_run_id = done_t1["run_id"]
        assert new_run_id and new_run_id != old_run_id

        # --- the trace: the new run carries the edit, the old run keeps OLD -
        new_trace_text = (run_dir(new_run_id, data_dir) / "prompt_trace.jsonl").read_text(
            encoding="utf-8")
        new_builder_entries = [
            json.loads(line) for line in new_trace_text.splitlines() if line.strip()
        ]
        new_builder_entries = [e for e in new_builder_entries if e.get("role") == "builder"]
        assert new_builder_entries
        for entry in new_builder_entries:
            assert _NEW_MARKER in entry["prompt_text_redacted"]
            assert _OLD_MARKER not in entry["prompt_text_redacted"]

        old_trace_text = (run_dir(old_run_id, data_dir) / "prompt_trace.jsonl").read_text(
            encoding="utf-8")
        assert _OLD_MARKER in old_trace_text

        # --- the fan: the live server's events-since holds two starts -------
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            events = _all_events_since(port, token, job_id)
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

        started_for_t1 = [
            e for e in events
            if e.get("event") == "task_run_started" and e.get("task_id") == t1_task_id
        ]
        assert len(started_for_t1) == 2, events
