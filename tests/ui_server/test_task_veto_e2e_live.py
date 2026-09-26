"""F027 R9 T003 LAST — the diamond veto end-to-end through the real CLI and a live
write door, both answers to the replan proposal carried to their effects
(DECISION F027 D9).

Structured like `test_task_edit_e2e_live.py`'s own live classes — `@pytest.mark.subprocess`,
a real UI server started in a thread, and a real POST through `HTTPConnection` — and this
file keeps its OWN copies of that file's plan, server-start, POST and events-since helpers,
per that file's own header rule, rather than importing them.

An approved diamond plan (A; B and C each depending on A; D depending on B and C), saved
directly, exactly as `_save_approved_two_task_job` saves its two-task plan there — a runtime
veto is gated on the plan being approved, and the job-markdown door `test_pause_e2e_live.py`
uses never produces one. Two tests: (a) THE ACCEPT PATH vetoes a task on a job the task cap
paused after its first task, runs it to a blocked end, and settles it by accepting the
reduced scope; (b) THE REPLAN PATH vetoes before any run, runs it to a blocked end, and
answers with a replan instead — a follow-up job that nothing here runs.
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

from packages.orchestration.data_paths import job_record_path, run_log_dir
from packages.orchestration.job_plan import APPROVED_PLAN_HASH_KEY, map_task_plan_to_tasks, plan_content_hash
from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables

CSRF_HEADER = "X-Remedy-CSRF"

#: DECISION F027 D9 (4) — the reason carries `<`, `&` and double quotes, asserted byte
#: for byte everywhere it travels: the door's answer, the dashboard section, the
#: `task_vetoed` event's metadata, the decision's summary and payload, and the report line.
VETO_REASON = 'Duplicates the <auth> work & its "legacy" path'


def _task(tid: str, deps: list[str]) -> dict:
    # `files_hint` names "docs/README.md", the file the fixture repo holds and the one
    # `FakeProvider`'s own default `builder_files` writes — the same pairing
    # `test_task_edit_e2e_live.py`'s own `_task` uses.
    return {
        "id": tid, "title": f"Build {tid}", "goal": f"goal of {tid}",
        "acceptance": [f"{tid} works"], "depends_on": deps,
        "est_tokens_band": "S", "files_hint": ["docs/README.md"],
    }


def _save_approved_diamond_job(root: Path, repo_path: Path) -> str:
    """An APPROVED diamond plan, saved directly (mirrors
    `test_task_edit_e2e_live.py`'s `_save_approved_two_task_job`): A; B and C each
    depending on A; D depending on B and C — plan order A, B, C, D."""
    tasks = [_task("A", []), _task("B", ["A"]), _task("C", ["A"]), _task("D", ["B", "C"])]
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": tasks})
    body = plan.model_dump()
    body["_approval"] = "approved"
    body["_normalization"] = []
    body[APPROVED_PLAN_HASH_KEY] = plan_content_hash(body)
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = JobPlan(job_title="F027 R9 live e2e", task_plan=body, tasks=mapped,
                 repo_path=str(repo_path))
    save_job_plan(job, root)
    return job.job_id


# ---------------------------------------------------------------------------
# Helpers — own copies of test_task_edit_e2e_live.py's, per that file's header rule
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
# Helpers new to THIS file — GET routes, the plan-order lookup and the events page
# ---------------------------------------------------------------------------


def _get_json(port: int, token: str, job_id: str, endpoint: str) -> dict:
    conn = HTTPConnection("127.0.0.1", port, timeout=10)
    try:
        conn.request("GET", f"/api/jobs/{job_id}/{endpoint}?token={token}")
        resp = conn.getresponse()
        assert resp.status == 200
        return json.loads(resp.read())
    finally:
        conn.close()


def _by_planned(job_data: dict, planned_id: str) -> dict:
    for t in job_data["tasks"]:
        if (t.get("inputs", {}).get("plan") or {}).get("planned_id") == planned_id:
            return t
    raise AssertionError(f"no task for planned id {planned_id!r}")


def _all_events_since(port: int, token: str, job_id: str) -> list[dict]:
    """Every event `events-since` will hand back, paged from cursor 0 — mirrors
    `test_task_edit_e2e_live.py`'s own helper exactly."""
    events: list[dict] = []
    cursor = "0"
    while True:
        conn = HTTPConnection("127.0.0.1", port, timeout=10)
        try:
            conn.request("GET", f"/api/jobs/{job_id}/events-since?token={token}&cursor={cursor}")
            resp = conn.getresponse()
            assert resp.status == 200
            body = json.loads(resp.read())
        finally:
            conn.close()
        events.extend(body["events"])
        next_cursor = body["cursor"]
        if next_cursor == cursor or not body["events"]:
            break
        cursor = next_cursor
    return events


def _run_log_reasons(data_dir: Path, job_id: str) -> list[str]:
    """Every `task_vetoed` event's `metadata["reason"]`, read from disk across every
    run-log file this job's runs produced."""
    out: list[str] = []
    log_dir = run_log_dir(job_id, data_dir)
    for jsonl in sorted(log_dir.glob("*.jsonl")) if log_dir.is_dir() else []:
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            raw = json.loads(line)
            if raw.get("event") == "task_vetoed":
                out.append(raw["metadata"]["reason"])
    return out


def _make_repo(tmp_path: Path, name: str) -> Path:
    repo = tmp_path / name
    (repo / "docs").mkdir(parents=True)
    (repo / "README.md").write_text("# Demo\n")
    (repo / "docs" / "README.md").write_text("# Docs\n")
    return repo


@pytest.mark.subprocess
class TestTaskVetoE2ELive:
    def test_the_accept_path_settles_the_reduced_scope(self, tmp_path):
        repo_root = Path(__file__).resolve().parents[2]
        repo = _make_repo(tmp_path, "repo")

        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()

        job_id = _save_approved_diamond_job(data_dir, repo)
        env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))

        # --- run 1: the task cap pauses the job after A --------------------
        run1 = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id,
             "--builder-provider", "fake", "--reviewer-provider", "fake", "--tasks", "1"],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
        assert run1.returncode == 0, f"run 1 exited {run1.returncode}: {run1.stderr}"

        paused = _job_data(data_dir, job_id)
        assert paused["status"] == "paused"
        assert _by_planned(paused, "A")["status"] == "applied_to_job_workspace"
        assert _by_planned(paused, "B")["status"] == "pending"
        assert _by_planned(paused, "C")["status"] == "pending"
        assert _by_planned(paused, "D")["status"] == "pending"
        b_task_id = _by_planned(paused, "B")["task_id"]
        d_task_id = _by_planned(paused, "D")["task_id"]

        # --- the veto for B, through a live write door ----------------------
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            status, body = _post(port, token, "job.veto-task", job_id=job_id,
                                 nonce="n-veto-b",
                                 args={"task_id": b_task_id, "reason": VETO_REASON})
            assert status == 200, body
            assert body["outcome"] == "vetoed", body
            assert body["reason"] == VETO_REASON
            assert body["unreachable"] == [d_task_id]
            actor = body["actor"]

            dashboard = _get_json(port, token, job_id, "dashboard")
            [veto_entry] = dashboard["vetoes"]["tasks"]
            assert veto_entry["reason"] == VETO_REASON
            assert veto_entry["unreachable_task_ids"] == [d_task_id]
            assert b_task_id not in dashboard["vetoes"]["vetoable_task_ids"]

            decisions = _get_json(port, token, job_id, "decisions")["decisions"]
            open_vetoes = [
                d for d in decisions if d["id"].startswith("veto:") and d["status"] == "open"
            ]
            assert len(open_vetoes) == 1, decisions
            [veto_decision] = open_vetoes
            assert veto_decision["type"] == "replan_proposal"
            assert VETO_REASON in veto_decision["safe_summary"]
            decision_id = veto_decision["id"]
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

        # --- run 2: uncapped, through the real CLI, to a blocked end --------
        run2 = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id, "--tasks", "0"],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
        assert run2.returncode == 0, f"run 2 exited {run2.returncode}: {run2.stderr}"
        assert f"Vetoed by {actor}: {VETO_REASON}" in run2.stdout, run2.stdout

        blocked = _job_data(data_dir, job_id)
        assert blocked["status"] == "blocked"
        assert blocked["error"] == (
            f"all_remaining_work_vetoed: vetoed {b_task_id}; unreachable {d_task_id}")
        assert _by_planned(blocked, "A")["status"] == "applied_to_job_workspace"
        assert _by_planned(blocked, "C")["status"] == "applied_to_job_workspace"
        assert _by_planned(blocked, "B")["status"] == "vetoed"
        assert _by_planned(blocked, "D")["status"] == "skipped"
        assert blocked["metadata"]["veto_terminal"] == {
            "vetoed": [b_task_id], "unreachable": [d_task_id], "settled": False,
        }

        # --- the live server: exactly one task_vetoed frame; the accept answer
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            events = _all_events_since(port, token, job_id)
            vetoed_events = [e for e in events if e.get("event") == "task_vetoed"]
            assert len(vetoed_events) == 1, events
            assert vetoed_events[0].get("task_id") == b_task_id

            status, body = _post(
                port, token, "decision.resolve", job_id=job_id, nonce="n-accept",
                args={"decision_id": decision_id, "answer": "accept_reduced_scope"})
            assert status == 200, body
            assert body["outcome"] == "answered"
            assert body["follow_up_job_id"] == ""
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

        # --- run 3: settles the reduced scope --------------------------------
        run3 = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
        assert run3.returncode == 0, f"run 3 exited {run3.returncode}: {run3.stderr}"

        completed = _job_data(data_dir, job_id)
        assert completed["status"] == "completed"
        assert completed["error"] == ""
        assert _by_planned(completed, "B")["status"] == "vetoed"
        assert _by_planned(completed, "D")["status"] == "skipped"
        assert completed["metadata"]["veto_terminal"] == {
            "vetoed": [b_task_id], "unreachable": [d_task_id], "settled": True,
            "answers": {b_task_id: "accept_reduced_scope"},
        }

        assert _run_log_reasons(data_dir, job_id) == [VETO_REASON]

    def test_the_replan_path_creates_a_follow_up_that_nothing_runs(self, tmp_path):
        repo_root = Path(__file__).resolve().parents[2]
        repo = _make_repo(tmp_path, "repo2")

        data_dir = tmp_path / "remedy_data2"
        data_dir.mkdir()

        job_id = _save_approved_diamond_job(data_dir, repo)
        env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))

        planned = _job_data(data_dir, job_id)
        b_task_id = _by_planned(planned, "B")["task_id"]

        # --- the veto for B, through a live write door, before any run ------
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            status, body = _post(port, token, "job.veto-task", job_id=job_id,
                                 nonce="n-veto-b2",
                                 args={"task_id": b_task_id, "reason": VETO_REASON})
            assert status == 200, body
            assert body["outcome"] == "vetoed", body
            request_id = body["request_id"]
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

        # --- run 1: through the real CLI, to a blocked end -------------------
        run1 = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id,
             "--builder-provider", "fake", "--reviewer-provider", "fake"],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
        assert run1.returncode == 0, f"run 1 exited {run1.returncode}: {run1.stderr}"

        blocked = _job_data(data_dir, job_id)
        assert blocked["status"] == "blocked"

        # --- the replan answer, through the live door ------------------------
        decision_id = f"veto:{request_id}"
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            status, body = _post(
                port, token, "decision.resolve", job_id=job_id, nonce="n-replan",
                args={"decision_id": decision_id, "answer": "replan_follow_up"})
            assert status == 200, body
            assert body["outcome"] == "answered"
            follow_up_job_id = body["follow_up_job_id"]
            assert follow_up_job_id

            decisions = _get_json(port, token, job_id, "decisions")["decisions"]
            assert not any(
                d["id"] == decision_id and d["status"] == "open" for d in decisions), decisions
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

        follow_up = _job_data(data_dir, follow_up_job_id)
        assert follow_up["status"] == "pending"
        assert follow_up["tasks"] == []
        replan_of = follow_up["metadata"]["replan_of"]
        assert replan_of["job_id"] == job_id
        assert replan_of["task_id"] == b_task_id
        assert replan_of["request_id"] == request_id
        assert VETO_REASON in follow_up["user_prompt"]

        # --- run 2 of the original: completes; the follow-up stays untouched -
        run2 = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
        assert run2.returncode == 0, f"run 2 exited {run2.returncode}: {run2.stderr}"

        completed = _job_data(data_dir, job_id)
        assert completed["status"] == "completed"
        assert completed["metadata"]["veto_terminal"]["answers"] == {
            b_task_id: "replan_follow_up",
        }

        follow_up_after = _job_data(data_dir, follow_up_job_id)
        assert follow_up_after["status"] == "pending"
        assert follow_up_after["tasks"] == []
