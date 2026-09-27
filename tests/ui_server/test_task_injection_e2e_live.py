"""F028 R9 T003 — the injection end to end through the real CLI, a live write door and
the command line, both answers to `job.inject`'s draft carried to their effects
(DECISIONS F028 D2, D5, D6 and D8).

Structured like `test_task_veto_e2e_live.py`'s own live class — `@pytest.mark.subprocess`,
a real UI server started in a thread, and a real POST through `HTTPConnection` — and this
file keeps its OWN copies of that file's `_make_repo`, server-start, POST, job-data,
GET-json and events-since helpers, per that file's own header rule, rather than importing
them.

An approved two-task plan A then B (B depending on A), saved directly, exactly as
`_save_approved_diamond_job` saves its own diamond there — an injection is gated on the
plan being approved and the job-markdown door `test_pause_e2e_live.py` uses never produces
one. Two tests: (a) THE DOOR PATH drafts and confirms an injection through `job.inject` and
`job.inject-confirm`, folds it into the same job's next run, and reads its provenance back
from the job record, the edit log, the run log, the dashboard, the events stream and the
final report; (b) THE COMMAND LINE PATH runs the same shape through
`apps.cli.grouped.main(["job", "inject", ..., "--yes", "--json"])` in the test's own
process.
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

INJECT_TEXT = "Add a task that double-checks the docs before we call this job done"

#: One valid `task_injection_draft_v1` object, the shape `injection_call_fn`'s real
#: planner would answer — `files_hint` names "docs/README.md", the file both plan tasks
#: below name too, and the fixture repo holds.
_DRAFT_TITLE = "Double-check the docs"
_DRAFT_GOAL = "verify the docs are accurate before the job ends"
_DRAFT_ACCEPTANCE = "the docs read correctly"
_DRAFT_RATIONALE = "the operator asked for one more check on the docs"

#: DECISION F028 D2 (4) — the clause the report appends to an injected task's own line.
ORIGIN_CLAUSE = " — added by you while the job ran"


def _injection_draft_json() -> str:
    return json.dumps({
        "schema_v": "task_injection_draft_v1",
        "title": _DRAFT_TITLE,
        "goal": _DRAFT_GOAL,
        "acceptance": [_DRAFT_ACCEPTANCE],
        "est_tokens_band": "S",
        "files_hint": ["docs/README.md"],
        "rationale": _DRAFT_RATIONALE,
    })


def _fake_injection_call_fn(prompt: str, attempt: int) -> str:
    return _injection_draft_json()


def _task(tid: str, deps: list[str]) -> dict:
    # `files_hint` names "docs/README.md", the file the fixture repo holds and the one
    # `FakeProvider`'s own default `builder_files` writes — the same pairing
    # `test_task_veto_e2e_live.py`'s own `_task` uses.
    return {
        "id": tid, "title": f"Build {tid}", "goal": f"goal of {tid}",
        "acceptance": [f"{tid} works"], "depends_on": deps,
        "est_tokens_band": "S", "files_hint": ["docs/README.md"],
    }


def _save_approved_two_task_job(root: Path, repo_path: Path) -> str:
    """An APPROVED two-task plan, saved directly (mirrors
    `test_task_veto_e2e_live.py`'s `_save_approved_diamond_job`): A; B depending on A."""
    tasks = [_task("A", []), _task("B", ["A"])]
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": tasks})
    body = plan.model_dump()
    body["_approval"] = "approved"
    body["_normalization"] = []
    body[APPROVED_PLAN_HASH_KEY] = plan_content_hash(body)
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = JobPlan(job_title="F028 R9 live e2e", task_plan=body, tasks=mapped,
                 repo_path=str(repo_path))
    save_job_plan(job, root)
    return job.job_id


# ---------------------------------------------------------------------------
# Helpers — own copies of test_task_veto_e2e_live.py's, per that file's header rule
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
    `test_task_veto_e2e_live.py`'s own helper exactly."""
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


def _make_repo(tmp_path: Path, name: str) -> Path:
    repo = tmp_path / name
    (repo / "docs").mkdir(parents=True)
    (repo / "README.md").write_text("# Demo\n")
    (repo / "docs" / "README.md").write_text("# Docs\n")
    return repo


# ---------------------------------------------------------------------------
# Helpers new to THIS file — the run log's own task_injected events and the report
# ---------------------------------------------------------------------------


def _run_log_task_injected_events(data_dir: Path, job_id: str) -> list[dict]:
    """Every `task_injected` event, read from disk across every run-log file this job's
    runs produced."""
    out: list[dict] = []
    log_dir = run_log_dir(job_id, data_dir)
    for jsonl in sorted(log_dir.glob("*.jsonl")) if log_dir.is_dir() else []:
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            raw = json.loads(line)
            if raw.get("event") == "task_injected":
                out.append(raw)
    return out


def _report_markdown(repo_root: Path, env: dict, job_id: str) -> str:
    """The `report` section of `job show <id> --full`, read from a real subprocess
    (DECISION F261 D10: the run report is what a `job run` job shows)."""
    show = subprocess.run(
        [sys.executable, "-m", "apps.cli.main", "job", "show", job_id, "--full", "--json"],
        cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
    assert show.returncode == 0, f"job show exited {show.returncode}: {show.stderr}"
    shown = json.loads(show.stdout)
    report_section = shown["sections"]["report"]
    assert report_section["ok"] is True, report_section
    return report_section["data"]["run_report"]["markdown"]


@pytest.mark.subprocess
class TestTaskInjectionE2ELive:
    def test_the_door_path_drafts_confirms_and_folds_the_injection(
            self, tmp_path, monkeypatch):
        import packages.orchestration.task_injection as ti
        monkeypatch.setattr(ti, "injection_call_fn", lambda: _fake_injection_call_fn)

        repo_root = Path(__file__).resolve().parents[2]
        repo = _make_repo(tmp_path, "repo")

        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()

        job_id = _save_approved_two_task_job(data_dir, repo)
        env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))

        # --- run 1: the task cap pauses the job after A ----------------------
        run1 = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id,
             "--builder-provider", "fake", "--reviewer-provider", "fake", "--tasks", "1"],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
        assert run1.returncode == 0, f"run 1 exited {run1.returncode}: {run1.stderr}"

        paused = _job_data(data_dir, job_id)
        assert paused["status"] == "paused"
        assert _by_planned(paused, "A")["status"] == "applied_to_job_workspace"
        assert _by_planned(paused, "B")["status"] == "pending"
        a_task_id = _by_planned(paused, "A")["task_id"]

        # --- the injection, through a live write door -------------------------
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            status, body = _post(port, token, "job.inject", job_id=job_id,
                                 nonce="n-inject-a",
                                 args={"text": INJECT_TEXT, "after": a_task_id})
            assert status == 200, body
            assert body["outcome"] == "drafted", body
            assert body["placement"]["depends_on"] == ["A"], body["placement"]
            assert body["placement"]["basis"] == "stated", body["placement"]
            confirm_token = body["confirm_token"]

            status, body = _post(port, token, "job.inject-confirm", job_id=job_id,
                                 nonce="n-inject-confirm-a",
                                 args={"confirm_token": confirm_token})
            assert status == 200, body
            assert body["outcome"] == "confirmed", body

            dashboard = _get_json(port, token, job_id, "dashboard")
            assert not any(t["origin"] == "human_injected" for t in dashboard["tasks"]), \
                dashboard["tasks"]
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

        # --- run 2: uncapped, through the real CLI, folds the injection --------
        run2 = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id, "--tasks", "0"],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
        assert run2.returncode == 0, f"run 2 exited {run2.returncode}: {run2.stderr}"

        completed = _job_data(data_dir, job_id)
        assert completed["status"] == "completed"
        assert len(completed["tasks"]) == 3
        assert all(t["status"] == "applied_to_job_workspace" for t in completed["tasks"]), \
            completed["tasks"]

        injected = next(
            t for t in completed["tasks"]
            if (t.get("inputs", {}).get("plan") or {}).get("origin") == "human_injected")
        injected_task_id = injected["task_id"]
        assert injected["inputs"]["plan"]["plan_rationale"] == (
            "placed after A because you named it")

        edit_log = completed["task_plan"]["_edits"]
        last_edit = edit_log[-1]
        assert last_edit["command"] == "plan_add_task"
        assert last_edit["injection"]["task_id"] == injected_task_id
        assert last_edit["injection"]["confirmed_unseen"] is False

        injected_events = _run_log_task_injected_events(data_dir, job_id)
        assert len(injected_events) == 1, injected_events
        assert injected_events[0]["outcome"] == "applied"
        assert injected_events[0]["task_id"] == injected_task_id

        # --- the run report, through a real subprocess `job show --full` -------
        markdown = _report_markdown(repo_root, env, job_id)
        matching = [line for line in markdown.splitlines() if ORIGIN_CLAUSE in line]
        assert len(matching) == 1, (markdown, matching)
        assert matching[0].startswith(f"- `{injected_task_id[:8]}`")

        # --- through a live door again: the dashboard and the events stream ----
        os.environ["REMEDY_DATA_DIR"] = str(data_dir)
        try:
            port, token = _start_ui_server_for_job(job_id, tmp_path)
            dashboard = _get_json(port, token, job_id, "dashboard")
            by_id = {t["id"]: t for t in dashboard["tasks"]}
            assert by_id[injected_task_id]["origin"] == "human_injected"
            for tid, item in by_id.items():
                if tid != injected_task_id:
                    assert item["origin"] == "", (tid, item)

            events = _all_events_since(port, token, job_id)
            injected_frames = [e for e in events if e.get("event") == "task_injected"]
            assert len(injected_frames) == 1, events
        finally:
            os.environ.pop("REMEDY_DATA_DIR", None)

    def test_the_command_line_path_yes_confirms_unseen(self, tmp_path, monkeypatch, capsys):
        import packages.orchestration.task_injection as ti
        monkeypatch.setattr(ti, "injection_call_fn", lambda: _fake_injection_call_fn)

        repo_root = Path(__file__).resolve().parents[2]
        repo = _make_repo(tmp_path, "repo2")

        data_dir = tmp_path / "remedy_data2"
        data_dir.mkdir()

        job_id = _save_approved_two_task_job(data_dir, repo)
        env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))

        # --- run 1: the task cap pauses the job after A, as in (a) -------------
        run1 = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id,
             "--builder-provider", "fake", "--reviewer-provider", "fake", "--tasks", "1"],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
        assert run1.returncode == 0, f"run 1 exited {run1.returncode}: {run1.stderr}"

        paused = _job_data(data_dir, job_id)
        assert paused["status"] == "paused"

        # --- the injection, through `remedy job inject --yes`, in this process --
        from apps.cli import grouped

        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        try:
            grouped.main(["job", "inject", job_id, INJECT_TEXT, "--yes", "--json"])
        except SystemExit as exc:
            raise AssertionError(f"job inject --yes exited {exc.code}") from exc

        stdout = capsys.readouterr().out
        lines = [line for line in stdout.splitlines() if line.strip()]
        assert len(lines) == 1, stdout
        envelope = json.loads(lines[0])
        assert envelope["ok"] is True, envelope
        assert "draft" in envelope, envelope
        assert "confirmation" in envelope, envelope
        assert envelope["confirmation"]["outcome"] == "confirmed", envelope

        # --- run 2: uncapped, through the real CLI, folds the injection --------
        run2 = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id, "--tasks", "0"],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
        assert run2.returncode == 0, f"run 2 exited {run2.returncode}: {run2.stderr}"

        completed = _job_data(data_dir, job_id)
        assert completed["status"] == "completed"
        assert len(completed["tasks"]) == 3
        assert all(t["status"] == "applied_to_job_workspace" for t in completed["tasks"]), \
            completed["tasks"]

        injected = next(
            t for t in completed["tasks"]
            if (t.get("inputs", {}).get("plan") or {}).get("origin") == "human_injected")
        injected_task_id = injected["task_id"]

        edit_log = completed["task_plan"]["_edits"]
        last_edit = edit_log[-1]
        assert last_edit["command"] == "plan_add_task"
        assert last_edit["injection"]["task_id"] == injected_task_id
        assert last_edit["injection"]["confirmed_unseen"] is True

        markdown = _report_markdown(repo_root, env, job_id)
        matching = [line for line in markdown.splitlines() if ORIGIN_CLAUSE in line]
        assert len(matching) == 1, (markdown, matching)
        assert matching[0].startswith(f"- `{injected_task_id[:8]}`")
