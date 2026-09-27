"""F288 R3 C5 (R-1075): re-capture `apps/ui/src/components/graph/brainDemoRecording.ts`.

Runs a real job on the fake builder/reviewer providers in a scratch repo and
data root under `.remedy-wt/f288-r3-worker/`, exactly as the module's own
docstring describes and as `tests/ui_server/test_brain_demo_recording_live.py`
verifies against: `init`, then `do "fix src/main.py and update README.md"
--no-llm --plan-only --json`, then the dashboard's `tasks` read before the
run, then `job run <job id> --builder-provider fake --reviewer-provider fake
--json`, then every frame `_build_events_since_json` serves from cursor 0.
Reuses `_git_repo`, `_env` and `_page_events` from the live test file by
import, so the two capture routes can never silently diverge.

Writes the regenerated `BRAIN_DEMO_JOB_ID`, `BRAIN_DEMO_TASKS` and
`BRAIN_DEMO_FRAMES` blocks straight into the recording module, and updates the
docstring's capture date — the three are GENERATED here, never hand-typed.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tests.ui_server.test_brain_demo_recording_live import (  # noqa: E402
    _env,
    _git_repo,
    _page_events,
)

CLI = [sys.executable, "-m", "apps.cli.main"]
ORDER = "fix src/main.py and update README.md"
RECORDING_PATH = (
    REPO_ROOT / "apps" / "ui" / "src" / "components" / "graph" / "brainDemoRecording.ts"
)
WORK_DIR = REPO_ROOT / ".remedy-wt" / "f288-r3-worker" / "capture"


def _run(cmd: list[str], *, cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=str(cwd), env=env, stdin=subprocess.DEVNULL,
        capture_output=True, text=True, timeout=30,
    )


def _ts_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _ts_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return _ts_string(value)
    if isinstance(value, (int, float)):
        return str(value)
    raise TypeError(f"unhandled scalar type for {value!r}")


def _render_task_item(task: dict[str, object]) -> str:
    fields = (
        "id", "label", "state", "kind", "checked", "muted", "nodeId",
        "testStatus", "proofStatus", "applyStatus",
    )
    lines = ["  {"]
    for field in fields:
        lines.append(f"    {field}: {_ts_scalar(task[field])},")
    lines.append("  },")
    return "\n".join(lines)


def _render_tasks_block(tasks: list[dict[str, object]]) -> str:
    body = "\n".join(_render_task_item(t) for t in tasks)
    return (
        "export const BRAIN_DEMO_TASKS: readonly RemedyTaskItem[] = [\n"
        f"{body}\n"
        "];"
    )


def _render_envelope(envelope: dict[str, object]) -> str:
    parts = []
    for key, value in envelope.items():
        if isinstance(value, dict):
            inner = ", ".join(f"{k}: {_render_json_value(v)}" for k, v in value.items())
            parts.append(f"{key}: {{ {inner} }}")
        else:
            parts.append(f"{key}: {_ts_scalar(value)}")
    return "{ " + ", ".join(parts) + " }"


def _render_json_value(value: object) -> str:
    if isinstance(value, list):
        return "[" + ", ".join(_render_json_value(v) for v in value) + "]"
    if isinstance(value, dict):
        inner = ", ".join(f"{k}: {_render_json_value(v)}" for k, v in value.items())
        return "{ " + inner + " }"
    return _ts_scalar(value)


def _render_frames_block(frames: list[dict[str, object]]) -> str:
    lines = ["export const BRAIN_DEMO_FRAMES: readonly BrainStreamFrame[] = ["]
    for envelope in frames:
        seq = envelope["seq"]
        lines.append(f"  {{ seq: {seq}, event: {_render_envelope(envelope)} }},")
    lines.append("];")
    return "\n".join(lines)


def main() -> None:
    if WORK_DIR.exists():
        shutil.rmtree(WORK_DIR)
    WORK_DIR.mkdir(parents=True)

    data_dir = WORK_DIR / "data"
    env = _env(data_dir)
    repo = _git_repo(WORK_DIR)

    init_result = _run([*CLI, "init"], cwd=repo, env=env)
    assert init_result.returncode == 0, init_result.stderr

    plan_result = _run(
        [*CLI, "do", ORDER, "--no-llm", "--plan-only", "--json"], cwd=repo, env=env,
    )
    assert plan_result.returncode == 0, plan_result.stderr
    plan_payload = json.loads(plan_result.stdout)
    job_id = plan_payload["job_ids"][0]

    os.environ["REMEDY_DATA_DIR"] = str(data_dir)
    from packages.orchestration.pingpong_job import load_job_plan
    from packages.orchestration.ui_server import _build_dashboard

    job_before = load_job_plan(job_id)
    assert job_before is not None
    raw_tasks_before = _build_dashboard(job_before)["tasks"]

    run_result = _run(
        [*CLI, "job", "run", job_id, "--builder-provider", "fake",
         "--reviewer-provider", "fake", "--json"],
        cwd=repo, env=env,
    )
    assert run_result.returncode == 0, run_result.stderr

    job_after = load_job_plan(job_id)
    assert job_after is not None
    live_frames = _page_events(job_after)

    # normalizeDashboardPayload's mapping (apps/ui/src/api/remedyApi.ts), for a
    # freshly planned task before any run: state stays "pending" (normalizeState
    # falls through to its default for that word), kind defaults to "task" (the
    # raw dashboard task carries none), checked is false (verified/accepted are
    # both false pre-run), muted is true (state is "pending"), nodeId mirrors
    # id (related_node_id === id), and testStatus/proofStatus/applyStatus pass
    # through unchanged because ui_server.py's own defaults for a fresh task
    # ("none", "none", "not_applied") are non-empty strings.
    demo_tasks = [
        {
            "id": t["id"],
            "label": t["title"],
            "state": t["status"],
            "kind": "task",
            "checked": False,
            "muted": t["status"] == "pending",
            "nodeId": t.get("related_node_id") or t["id"],
            "testStatus": t.get("test_status") or "none",
            "proofStatus": t.get("proof_status") or "none",
            "applyStatus": t.get("apply_status") or "not_applied",
        }
        for t in raw_tasks_before
    ]

    tasks_block = _render_tasks_block(demo_tasks)
    frames_block = _render_frames_block(live_frames)
    job_id_line = f'export const BRAIN_DEMO_JOB_ID = {_ts_string(str(job_id))};'

    text = RECORDING_PATH.read_text()

    text = re.sub(
        r'export const BRAIN_DEMO_JOB_ID = "[^"]*";',
        job_id_line, text, count=1,
    )
    text = re.sub(
        r'export const BRAIN_DEMO_TASKS: readonly RemedyTaskItem\[\] = \[.*?\n\];',
        tasks_block, text, count=1, flags=re.DOTALL,
    )
    text = re.sub(
        r'export const BRAIN_DEMO_FRAMES: readonly BrainStreamFrame\[\] = \[.*?\n\];',
        frames_block, text, count=1, flags=re.DOTALL,
    )
    today = date.today().isoformat()
    text = re.sub(r"Captured on \d{4}-\d{2}-\d{2}", f"Captured on {today}", text, count=1)

    RECORDING_PATH.write_text(text)

    shutil.rmtree(WORK_DIR)

    print(f"job_id={job_id}")
    print(f"tasks={len(demo_tasks)}")
    print(f"frames={len(live_frames)}")
    print(f"capture_date={today}")


if __name__ == "__main__":
    main()
