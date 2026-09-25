"""F023 T003 — the live end-to-end of the zoom's evidence: a real job's stream and its run
reports agree on every round the L2 run detail and the L3 panel read (DECISION F023 D7).

The run detail tells a review run's round by counting the `task_round_completed` frames its
task logged since its last `task_run_started` (`runPlaceOf` in
`apps/ui/src/components/graph/runDetailModel.ts`), and reads that round's facts from the rounds
route (`packages/orchestration/run_rounds_view.py`, DECISION F023 D3), which serves the run
report the task record points at. Both halves are goldened on their own; this test is the one
place they meet on a real run: it plans and runs a fake-provider job in a scratch repository
(no network, no model), pages its `events-since` frames exactly as the UI does, and checks, task
by task, that the round the stream implies is a round the report holds, with the verdict the
stream announced.
"""
from __future__ import annotations

import json

from tests.ui_server.test_brain_demo_recording_live import CLI, ORDER, _env, _git_repo, _page_events, _run


def test_a_live_jobs_stream_and_run_reports_agree_on_every_round(tmp_path, monkeypatch):
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
    from packages.orchestration.ui_server import _build_task_run_rounds_json

    job = load_job_plan(job_id)
    frames = _page_events(job)
    checked = 0
    for task in job.tasks:
        own = [f for f in frames if f["task_id"] == task.task_id]
        starts = [f["seq"] for f in own if f["event"] == "task_run_started"]
        assert starts, f"task {task.task_id} never started"
        # The run detail's rule: the rounds logged since the task's LAST start.
        rounds_logged = [f for f in own if f["event"] == "task_round_completed" and f["seq"] > starts[-1]]
        envelope = _build_task_run_rounds_json(job, task.task_id)
        assert envelope["available"] is True, envelope
        assert envelope["run_id"] == task.run_id
        assert [r["round"] for r in envelope["rounds"]] == list(range(1, len(rounds_logged) + 1))
        for number, frame in enumerate(rounds_logged, start=1):
            facts = envelope["rounds"][number - 1]
            if frame["outcome"] != "no_review":
                assert facts["reviewer"]["verdict"] == frame["outcome"], (task.task_id, number)
            assert facts["duration_ms"] is not None and facts["duration_ms"] >= 0
            assert isinstance(facts["builder"]["tokens_used"], int)
        checked += len(rounds_logged)
    assert checked > 0, "the fake job logged no round, so nothing was compared"
