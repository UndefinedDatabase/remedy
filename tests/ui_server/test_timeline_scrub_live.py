"""F024 T003 — the live end-to-end of the scrubber: a real job's ledger, scrubbed by the real
timeline modules (DECISION F024 D5).

T5_F024.md's DONE is that scrubbing any position renders exactly the reducer state of that
prefix. The modules that do it are TypeScript and goldened by vitest on fixtures; this test is
where they meet a REAL ledger. It plans and runs a fake-provider job in a scratch repository (no
network, no model), pages its `events-since` frames exactly as the UI does, and runs
`apps/ui/src/components/timeline/scrubLive.test.ts` with that ledger handed in through a scratch
vitest config's `define`, so the scrubbed state, the phases and the track are checked at every
position of a ledger the product itself wrote. vitest is gitignored and absent from a fresh
worktree, so the test skips there, naming the missing binary, as `test_test_runner.py`'s vitest
node does.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import pytest

from tests.ui_server.test_brain_demo_recording_live import CLI, ORDER, _env, _git_repo, _page_events, _run

REPO_ROOT = Path(__file__).resolve().parents[2]
UI_ROOT = REPO_ROOT / "apps" / "ui"
VITEST = UI_ROOT / "node_modules" / ".bin" / "vitest"
LIVE_TEST = UI_ROOT / "src" / "components" / "timeline" / "scrubLive.test.ts"


@pytest.mark.skipif(
    not VITEST.is_file(),
    reason="apps/ui/node_modules/.bin/vitest is absent (gitignored, never in a fresh worktree)",
)
def test_a_live_jobs_ledger_scrubs_to_exactly_each_prefix(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    env = _env(data_dir)
    repo = _git_repo(tmp_path)
    assert _run([*CLI, "init"], cwd=repo, env=env).returncode == 0
    plan = _run([*CLI, "do", ORDER, "--no-llm", "--plan-only", "--json"], cwd=repo, env=env)
    assert plan.returncode == 0, plan.stderr
    job_id = json.loads(plan.stdout)["job_ids"][0]
    run = _run([*CLI, "job", "run", job_id, "--builder-provider", "fake", "--reviewer-provider", "fake", "--json"],
               cwd=repo, env=env)
    assert run.returncode == 0, run.stderr

    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    from packages.orchestration.pingpong_job import load_job_plan

    job = load_job_plan(job_id)
    frames = _page_events(job)
    assert frames, "the fake job logged no event, so there is nothing to scrub"
    tasks = [{"id": t.task_id, "status": "pending", "rank": rank} for rank, t in enumerate(job.tasks)]
    payload = json.dumps({"jobId": job_id, "tasks": tasks, "frames": frames})

    # `define` takes code: the payload travels as a JavaScript string literal.
    config = tmp_path / "vitest.scrub-live.config.mjs"
    config.write_text(
        "export default {\n"
        f"  root: {json.dumps(str(UI_ROOT))},\n"
        f"  cacheDir: {json.dumps(str(tmp_path / 'vite-cache'))},\n"
        f"  define: {{ __REMEDY_SCRUB_LIVE__: {json.dumps(json.dumps(payload))} }},\n"
        f"  test: {{ environment: \"node\", include: [{json.dumps(str(LIVE_TEST))}] }},\n"
        "};\n",
        encoding="utf-8",
    )
    result = subprocess.run([str(VITEST), "run", "--config", str(config)], cwd=str(UI_ROOT),
                            capture_output=True, text=True, timeout=120)
    out = result.stdout + result.stderr
    assert result.returncode == 0, out
    # vitest colours its summary wherever `CI` is set, as on the hosted runner (R-1048).
    counts = re.search(r"Tests\s+(\d+) passed \((\d+)\)", re.sub(r"\x1b\[[0-9;]*m", "", out))
    assert counts, out
    assert counts.group(1) == counts.group(2) == "5", f"every live check must run and pass:\n{out}"
