"""A live fake job renders identically to the committed demo recording
(DECISION F019 D6). Plans and runs a job on the fake builder/reviewer
providers in a scratch repo (no network, no model), reads its before-run
dashboard task list and its `events-since` frames the way the UI server
serves them, and compares both — projected the way the module docstring on
`apps/ui/src/components/graph/brainDemoRecording.ts` describes — against the
COMMITTED recording. Since `rebuildBrainModel` is a pure function of the
seeds' (rank, status, title) and the rows' (seq, kind, outcome, task), equal
projections mean equal models up to ids.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RECORDING_PATH = (
    REPO_ROOT / "apps" / "ui" / "src" / "components" / "graph" / "brainDemoRecording.ts"
)
CLI = [sys.executable, "-m", "apps.cli.main"]
ORDER = "fix src/main.py and update README.md"


def _env(data_dir: Path) -> dict[str, str]:
    return {
        **os.environ,
        "PYTHONPATH": str(REPO_ROOT),
        "REMEDY_DATA_DIR": str(data_dir),
    }


def _run(cmd: list[str], *, cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=str(cwd), env=env, stdin=subprocess.DEVNULL,
        capture_output=True, text=True, timeout=30,
    )


def _git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "--allow-empty", "-m", "init", "-q"],
        check=True, capture_output=True,
        env={
            **os.environ,
            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
        },
    )
    return repo


def _page_events(job) -> list[dict]:
    """Page `_build_events_since_json` exactly as the cursor endpoint does:
    from cursor "0" until a page adds nothing new."""
    from packages.orchestration.ui_server import _build_events_since_json

    frames: list[dict] = []
    cursor = "0"
    while True:
        page = _build_events_since_json(job, cursor)
        new_frames = page["events"]
        frames.extend(new_frames)
        new_cursor = page["cursor"]
        if new_cursor == cursor or not new_frames:
            break
        cursor = new_cursor
    return frames


_TASK_FIELD_RE = re.compile(r'\b(id|label|state):\s*"([^"]*)"')
_FRAME_RE = re.compile(
    r'event:\s*\{\s*seq:\s*(\d+),\s*event:\s*"([^"]*)",\s*timestamp:\s*"[^"]*",\s*'
    r'outcome:\s*"([^"]*)",\s*task_id:\s*"([^"]*)"\s*\}'
)


def _parse_recording() -> tuple[list[tuple[str, str, str]], list[tuple[int, str, str, str]]]:
    """Read the COMMITTED recording as TEXT and pull out, by regex:
    - tasks: (id, label, state) triples, in BRAIN_DEMO_TASKS's own order;
    - frames: (seq, event, outcome, task_id) tuples, in BRAIN_DEMO_FRAMES's
      own order (the frame's INNER event object — the flat shape
      `_build_events_since_json` itself serves)."""
    text = RECORDING_PATH.read_text()
    tasks_block_start = text.index("BRAIN_DEMO_TASKS")
    frames_block_start = text.index("BRAIN_DEMO_FRAMES")
    tasks_text = text[tasks_block_start:frames_block_start]
    frames_text = text[frames_block_start:]

    fields = _TASK_FIELD_RE.findall(tasks_text)
    tasks: list[tuple[str, str, str]] = []
    current: dict[str, str] = {}
    for name, value in fields:
        if name == "id" and current:
            tasks.append((current["id"], current["label"], current["state"]))
            current = {}
        current[name] = value
    if current:
        tasks.append((current["id"], current["label"], current["state"]))

    frames = [
        (int(seq), event, outcome, task_id)
        for seq, event, outcome, task_id in _FRAME_RE.findall(frames_text)
    ]
    return tasks, frames


def test_live_fake_job_renders_identically_to_the_demo_recording(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    env = _env(data_dir)
    repo = _git_repo(tmp_path)

    init_result = _run([*CLI, "init"], cwd=repo, env=env)
    assert init_result.returncode == 0, init_result.stderr

    plan_result = _run([*CLI, "do", ORDER, "--no-llm", "--plan-only", "--json"], cwd=repo, env=env)
    assert plan_result.returncode == 0, plan_result.stderr
    plan_payload = json.loads(plan_result.stdout)
    job_id = plan_payload["job_ids"][0]

    # In-process reads need REMEDY_DATA_DIR in THIS process's environment too
    # — the CLI subprocess env above does not reach `load_job_plan` here.
    # monkeypatch keeps that scoped to this test, unlike os.environ[...] = ...,
    # which would leak into every later test in the same worker process.
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.ui_server import _build_dashboard

    job_before = load_job_plan(job_id)
    assert job_before is not None
    live_tasks_before = _build_dashboard(job_before)["tasks"]

    run_result = _run(
        [*CLI, "job", "run", job_id, "--builder-provider", "fake", "--reviewer-provider", "fake", "--json"],
        cwd=repo, env=env,
    )
    assert run_result.returncode == 0, run_result.stderr

    job_after = load_job_plan(job_id)
    assert job_after is not None
    live_frames = _page_events(job_after)

    recording_tasks, recording_frames = _parse_recording()

    # --- before-run task list: (title, status) == recording's (label, state) ---
    live_before_tuples = [(t["title"], t["status"]) for t in live_tasks_before]
    recording_before_tuples = [(label, state) for _id, label, state in recording_tasks]
    assert live_before_tuples == recording_before_tuples
    # The fake planner's titles are pending before anything ran.
    assert all(status == "pending" for _title, status in live_before_tuples)

    # --- frames, projected against each side's OWN task-id order -----------
    live_task_ids = [t["id"] for t in live_tasks_before]
    recording_task_ids = [task_id for task_id, _label, _state in recording_tasks]

    live_projected = [
        (f["seq"], f["event"], f["outcome"], live_task_ids.index(f["task_id"]))
        for f in live_frames
    ]
    recording_projected = [
        (seq, event, outcome, recording_task_ids.index(task_id))
        for seq, event, outcome, task_id in recording_frames
    ]
    assert live_projected == recording_projected

    # --- every live frame's key set is exactly this, no more, no less ------
    expected_keys = {"seq", "event", "timestamp", "outcome", "task_id"}
    for f in live_frames:
        assert set(f.keys()) == expected_keys
