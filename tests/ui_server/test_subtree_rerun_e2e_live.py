"""F029 T003 — the subtree rerun end to end through the real CLI, a live write
door and the command line, both attempts to a middle task and its dependent
read back from the job record, git, the run log, the dashboard, the run
records and the final report (DECISIONS F029 D1, D2, D3, D4, D5 and D6).

Structured like `test_task_injection_e2e_live.py`'s own live class —
`@pytest.mark.subprocess`, a real UI server started in a thread, real POSTs
through `HTTPConnection`, and real `python -m apps.cli.main` subprocesses —
and this file keeps its OWN copies of that file's `_start_ui_server_for_job`,
`_post`, `_job_data`, `_get_json`, `_by_planned`, `_all_events_since` and
`_report_markdown` helpers, per that file's own header rule, rather than
importing them.

An approved three-task plan A; B depending on A; C depending on B, saved
directly, exactly as `_save_approved_two_task_job` saves its own two — over a
REAL git repository, since `_create_job_workspace` in `pingpong_job.py`
chooses worktree mode only for one, and a rerun is refused outside it. Two
tests: (a) THE DOOR PATH reruns B and its dependent C through
`job.rerun-subtree` behind the cost preview, once refused for confirmation
and once prepared with a model override, proves the reset by git tree hash,
folds the second run through the real CLI, and reads the two attempts back
from the job record, the moved stream evidence, the run log, the dashboard,
the run records and the final report; (b) THE COMMAND LINE PATH runs the
same shape through `apps.cli.grouped.main(["job", "rerun-subtree", ...,
"--yes", "--json"])` in the test's own process.
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import subprocess
import sys
import threading
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.orchestration import pingpong_job as PJ
from packages.orchestration.data_paths import (
    job_evidence_dir,
    job_record_path,
    run_dir,
    run_log_dir,
)
from packages.orchestration.job_plan import (
    APPROVED_PLAN_HASH_KEY,
    map_task_plan_to_tasks,
    plan_content_hash,
)
from packages.orchestration.pingpong_job import JobPlan, save_job_plan
from packages.orchestration.schemas.models import TaskPlan
from packages.orchestration.task_deliverables import record_llm_task_deliverables

CSRF_HEADER = "X-Remedy-CSRF"

#: Two module constants `_MODEL_OVERRIDE_RE` accepts (`subtree_rerun.py`) —
#: one per test, so a failure never mistakes one attempt's model for the other's.
MODEL_M = "rerun-model-x1"
MODEL_M2 = "rerun-model-y2"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=str(repo), capture_output=True,
                          text=True, check=True).stdout


def _make_repo(tmp_path: Path, name: str) -> Path:
    """A REAL git repository — one file, one commit — since `_create_job_workspace`
    chooses worktree isolation mode only for one, and a rerun is refused
    outside it."""
    repo = tmp_path / name
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@e.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "config", "commit.gpgsign", "false")
    (repo / "base.txt").write_text("base\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "init")
    return repo


def _task(tid: str, deps: list[str]) -> dict:
    # `files_hint` names "docs/README.md", the fake builder's own default
    # `builder_files` writes for every task, whichever task runs it — the
    # same pairing `test_task_injection_e2e_live.py`'s own `_task` uses.
    return {
        "id": tid, "title": f"Build {tid}", "goal": f"goal of {tid}",
        "acceptance": [f"{tid} works"], "depends_on": deps,
        "est_tokens_band": "S", "files_hint": ["docs/README.md"],
    }


def _save_approved_three_task_job(root: Path, repo_path: Path) -> str:
    """An APPROVED three-task plan, saved directly (mirrors
    `test_task_injection_e2e_live.py`'s `_save_approved_two_task_job`): A; B
    depending on A; C depending on B."""
    tasks = [_task("A", []), _task("B", ["A"]), _task("C", ["B"])]
    plan = TaskPlan.model_validate({"schema_v": "task_plan_v1", "tasks": tasks})
    body = plan.model_dump()
    body["_approval"] = "approved"
    body["_normalization"] = []
    body[APPROVED_PLAN_HASH_KEY] = plan_content_hash(body)
    mapped = map_task_plan_to_tasks(plan)
    record_llm_task_deliverables(mapped)
    job = JobPlan(job_title="F029 R7 live e2e", task_plan=body, tasks=mapped,
                 repo_path=str(repo_path))
    save_job_plan(job, root)
    return job.job_id


# ---------------------------------------------------------------------------
# Helpers — own copies of test_task_injection_e2e_live.py's, per that file's
# header rule
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
    `test_task_injection_e2e_live.py`'s own helper exactly."""
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


# ---------------------------------------------------------------------------
# Helpers new to THIS file — the sha256 tree map and the run log's own
# subtree_rerun_prepared events
# ---------------------------------------------------------------------------


def _sha256_tree(root: Path) -> dict[str, str]:
    """sha256 of every file under *root*, keyed by its path relative to *root* —
    the byte-level proof that an earlier run's directory was never touched."""
    out: dict[str, str] = {}
    if not root.exists():
        return out
    for path in sorted(root.rglob("*")):
        if path.is_file():
            out[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


def _run_log_subtree_rerun_prepared_events(data_dir: Path, job_id: str) -> list[dict]:
    """Every `subtree_rerun_prepared` event, read from disk across every run-log
    file this job's runs produced."""
    out: list[dict] = []
    log_dir = run_log_dir(job_id, data_dir)
    for jsonl in sorted(log_dir.glob("*.jsonl")) if log_dir.is_dir() else []:
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            raw = json.loads(line)
            if raw.get("event") == "subtree_rerun_prepared":
                out.append(raw)
    return out


@pytest.mark.subprocess
class TestSubtreeRerunE2ELive:
    def test_the_door_path_reruns_a_middle_task_end_to_end(self, tmp_path, monkeypatch):
        repo_root = Path(__file__).resolve().parents[2]
        repo = _make_repo(tmp_path, "repo")

        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()

        job_id = _save_approved_three_task_job(data_dir, repo)
        env = dict(os.environ, REMEDY_DATA_DIR=str(data_dir), PYTHONPATH=str(repo_root))

        # --- run 1: all three tasks, through the real CLI ---------------------
        run1 = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id,
             "--builder-provider", "fake", "--reviewer-provider", "fake", "--tasks", "0"],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
        assert run1.returncode == 0, f"run 1 exited {run1.returncode}: {run1.stderr}"

        completed = _job_data(data_dir, job_id)
        assert completed["status"] == "completed"
        for planned_id in ("A", "B", "C"):
            t = _by_planned(completed, planned_id)
            assert t["status"] == "applied_to_job_workspace", (planned_id, t)
            assert t["attempt"] == 1, (planned_id, t)
            assert t["attempts"] == [], (planned_id, t)

        a1, b1, c1 = (_by_planned(completed, p) for p in ("A", "B", "C"))
        a_id, b_id, c_id = a1["task_id"], b1["task_id"], c1["task_id"]
        a_run_id_1, a_commit_1 = a1["run_id"], a1["worktree_commit"]
        b_run_id_1, b_commit_1 = b1["run_id"], b1["worktree_commit"]

        # THE step-1 SHA256 MAP — B's attempt-1 run directory, before anything
        # is rerun, so a later comparison proves it was never touched.
        before_hashes = _sha256_tree(run_dir(b_run_id_1, data_dir))
        assert before_hashes

        # --- the rerun, through a live write door -------------------------
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))

        # `run_job` writes stream evidence only when asked to, and
        # `test_subtree_rerun_prepare.py` plants the same kind of marker to
        # prove the move — this run never asked, so the marker is planted by
        # hand.
        stream_dir = PJ._task_stream_dir(job_id, b_id)
        stream_dir.mkdir(parents=True)
        (stream_dir / "marker.txt").write_text("stream marker")

        # `resolve_confirm_above_usd` ignores a threshold that is not above
        # zero, so this near-zero value guarantees `needs_confirmation` on the
        # first POST whatever the subtree's real estimate turns out to be.
        monkeypatch.setenv("REMEDY_COST_PREVIEW_CONFIRM_ABOVE_USD", "0.000001")

        port, token = _start_ui_server_for_job(job_id, tmp_path)

        status, body = _post(port, token, "job.rerun-subtree", job_id=job_id,
                             nonce="n-rerun-1",
                             args={"task_id": b_id, "model": MODEL_M})
        assert status == 200, body
        assert body["outcome"] == "needs_confirmation", body
        assert body["subtree"] == [b_id, c_id], body
        assert _job_data(data_dir, job_id)["status"] == "completed"

        status, body = _post(port, token, "job.rerun-subtree", job_id=job_id,
                             nonce="n-rerun-2",
                             args={"task_id": b_id, "model": MODEL_M, "confirm_cost": True})
        assert status == 200, body
        assert body["outcome"] == "prepared", body
        assert body["root_task_id"] == b_id, body
        assert body["subtree"] == [b_id, c_id], body
        assert body["exact"] is True, body
        assert body["pre_task_tree_equal"] is True, body
        assert body["model"] == {
            "override": MODEL_M, "configured": "", "reason": "human_override"}, body
        run_command = f"remedy job run {job_id}"
        assert body["run_command"] == run_command, body
        base_commit = body["base_commit"]
        reset_commit = body["reset_commit"]

        # --- THE TREE-HASH PROOF, with git on the fixture repository itself ---
        assert _git(repo, "rev-parse", f"{b_commit_1}^").strip() == base_commit
        assert (_git(repo, "rev-parse", f"{reset_commit}^{{tree}}").strip()
               == _git(repo, "rev-parse", f"{base_commit}^{{tree}}").strip())
        job_branch = _job_data(data_dir, job_id)["worktree"]["branch"]
        ancestor = subprocess.run(
            ["git", "merge-base", "--is-ancestor", b_commit_1, job_branch],
            cwd=str(repo), capture_output=True, text=True)
        assert ancestor.returncode == 0, ancestor.stderr

        # --- the job record -------------------------------------------------
        paused = _job_data(data_dir, job_id)
        assert paused["status"] == "paused"
        assert len(paused["reruns"]) == 1
        rerun_record = paused["reruns"][0]
        assert rerun_record["base_commit"] == base_commit
        assert rerun_record["reset_commit"] == reset_commit
        assert rerun_record["exact"] is True
        assert rerun_record["pre_task_tree_equal"] is True
        assert rerun_record["proof"]["paths_equal"] is True
        assert rerun_record["proof"]["tree_equals_base"] is True

        new_b, new_c, new_a = (_by_planned(paused, p) for p in ("B", "C", "A"))
        assert new_b["status"] == "pending" and new_b["attempt"] == 2
        assert len(new_b["attempts"]) == 1
        assert new_b["model_override"] == MODEL_M
        assert new_b["attempts"][0]["worktree_commit"] == b_commit_1
        assert new_b["attempts"][0]["run_id"] == b_run_id_1
        assert new_b["attempts"][0]["stream_evidence"] == f"rerun_attempts/{b_id}/attempt-1"

        assert new_c["status"] == "pending" and new_c["attempt"] == 2
        assert len(new_c["attempts"]) == 1
        assert new_c["model_override"] == MODEL_M

        assert new_a["attempt"] == 1 and new_a["attempts"] == []
        assert new_a["run_id"] == a_run_id_1
        assert new_a["worktree_commit"] == a_commit_1

        # --- the marker, moved -----------------------------------------------
        moved = (job_evidence_dir(job_id, data_dir) / "rerun_attempts"
                / b_id / "attempt-1" / "marker.txt")
        assert moved.read_text() == "stream marker"
        assert not stream_dir.exists()

        # --- the run log, the dashboard and the events stream -----------------
        events = _run_log_subtree_rerun_prepared_events(data_dir, job_id)
        assert len(events) == 1, events
        assert events[0]["task_id"] == b_id
        assert events[0]["metadata"]["exact"] is True
        assert events[0]["metadata"]["model_override"] == MODEL_M

        dashboard = _get_json(port, token, job_id, "dashboard")
        by_id = {t["id"]: t for t in dashboard["tasks"]}
        assert by_id[b_id]["attempt"] == 2 and len(by_id[b_id]["attempts"]) == 1
        assert by_id[c_id]["attempt"] == 2 and len(by_id[c_id]["attempts"]) == 1
        assert by_id[a_id]["attempt"] == 1

        frames = _all_events_since(port, token, job_id)
        prepared_frames = [e for e in frames if e.get("event") == "subtree_rerun_prepared"]
        assert len(prepared_frames) == 1, frames

        # --- run 2: uncapped, through the real CLI, folds the rerun -----------
        run2 = subprocess.run(
            [sys.executable, "-m", "apps.cli.main", "job", "run", job_id, "--tasks", "0"],
            cwd=str(repo_root), env=env, capture_output=True, text=True, timeout=120)
        assert run2.returncode == 0, f"run 2 exited {run2.returncode}: {run2.stderr}"

        completed2 = _job_data(data_dir, job_id)
        assert completed2["status"] == "completed"
        new_a2 = _by_planned(completed2, "A")
        assert new_a2["run_id"] == a_run_id_1
        assert new_a2["worktree_commit"] == a_commit_1

        new_b2, new_c2 = (_by_planned(completed2, p) for p in ("B", "C"))
        for entry, old_run_id, old_commit in (
            (new_b2, b_run_id_1, b_commit_1),
            (new_c2, c1["run_id"], c1["worktree_commit"]),
        ):
            assert entry["status"] == "applied_to_job_workspace", entry
            assert entry["attempt"] == 2, entry
            assert len(entry["attempts"]) == 1, entry
            assert entry["run_id"] != old_run_id and entry["run_id"]
            assert entry["worktree_commit"] != old_commit and entry["worktree_commit"]
            assert entry["model_override"] == MODEL_M

        # --- THE RUN RECORDS, through pingpong_loop.load_run -------------------
        from packages.orchestration.pingpong_loop import load_run

        b_run_2 = load_run(new_b2["run_id"])
        assert b_run_2["provider_evidence"]["builder_configured_model"] == MODEL_M
        c_run_2 = load_run(new_c2["run_id"])
        assert c_run_2["provider_evidence"]["builder_configured_model"] == MODEL_M

        b_run_1 = load_run(b_run_id_1)
        assert b_run_1["provider_evidence"]["builder_configured_model"] != MODEL_M

        after_hashes = _sha256_tree(run_dir(b_run_id_1, data_dir))
        assert after_hashes == before_hashes

        # --- THE REPORT, through job show --full --json -------------------
        markdown = _report_markdown(repo_root, env, job_id)
        lines = markdown.splitlines()
        b_line = next(line for line in lines if line.startswith(f"- `{b_id[:8]}`"))
        assert b_line.endswith(f" — attempt 2, run on {MODEL_M}"), b_line
        c_line = next(line for line in lines if line.startswith(f"- `{c_id[:8]}`"))
        assert c_line.endswith(f" — attempt 2, run on {MODEL_M}"), c_line
        a_line = next(line for line in lines if line.startswith(f"- `{a_id[:8]}`"))
        assert " — attempt" not in a_line, a_line
