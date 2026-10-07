"""F287 R9 — a relaunch through `remedy job run` resumes the parked `claude-cli`
session, and names a declined resume (R-1163).

Round 8's block ordered this same test without `--repair-rounds` on the
fake-provider relaunch; that relaunch inherited the parked run's persisted
`repair_rounds=0` (`packages/orchestration/pingpong_job.py::run_job`'s
``if repair_rounds is not None:`` branch), and the fake reviewer's
`pass_on_round=2` default could never pass within that budget, so the job
ended `blocked` instead of `completed` (full account in `.agent/handoff.md`,
round 8). This round's block adds `--repair-rounds 1` to that one call;
everything else is unchanged.

Both tests here drive Remedy the way an operator does: by typing
`remedy job run`, which pauses mid-build, and then `remedy job run` again,
which resumes. Every call goes through `run_cli_in_process` — the real CLI
dispatcher, never `run_job` directly and never a subprocess.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import patch

from packages.orchestration import pingpong_provider
from packages.orchestration.pingpong_job import JOB_COMPLETED, JOB_PAUSED, parse_job_file
from tests.cli.in_process_cli import run_cli_in_process
from tests.orchestration import test_relaunch_session_resume as _relaunch_tests
from tests.orchestration.test_job_stop_integration import _ONE_TASK_JOB

_PARKED_RUN_ARGS = [
    "--builder-provider", "claude-cli", "--reviewer-provider", "claude-cli",
    "--builder-model", "claude-sonnet-4-6", "--reviewer-model", "claude-sonnet-4-6",
    "--repair-rounds", "0", "--json",
]


def _setup(tmp_path: Path, monkeypatch):
    """Shared setup for both tests: an isolated data root, a git target
    holding `README.md` and `docs/README.md`, the one-task job, the CLI
    environment, and the `claude-cli` stand-in whose `interrupt` is the
    CLI's own pause command."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))

    target = tmp_path / "target"
    target.mkdir()
    (target / "README.md").write_text("# demo\n")
    (target / "docs").mkdir()
    (target / "docs" / "README.md").write_text("# docs\n")
    _relaunch_tests.TestAParkedClaudeCliTaskResumesOnRelaunch._init_git_repo(target)

    job = parse_job_file(_ONE_TASK_JOB, str(target))
    env = dict(os.environ)
    stand_in, calls = _relaunch_tests.TestAParkedClaudeCliTaskResumesOnRelaunch._make_stand_in(
        lambda: run_cli_in_process(
            ["job", "pause", job.job_id, "--reason", "mid-build pause"], cwd=target, env=env))
    return job, target, env, stand_in, calls


class TestARelaunchThroughJobRunResumesTheParkedSession:
    """R-1163: the parked run is the same `claude-cli` invocation for both
    tests; only the relaunch differs, so each test re-parks for itself."""

    def test_the_relaunch_on_claude_cli_resumes_the_parked_session(
            self, tmp_path, monkeypatch):
        job, target, env, stand_in, calls = _setup(tmp_path, monkeypatch)

        with patch.object(pingpong_provider, "_guarded_cli_run", side_effect=stand_in), \
             patch.object(pingpong_provider.ClaudeCliProvider, "_get_claude_path",
                          lambda self: "/fake/claude"), \
             patch.object(pingpong_provider.ClaudeCliProvider, "_resolve_version",
                          lambda self: "1.0.0 (test)"):
            parked = run_cli_in_process(
                ["job", "run", job.job_id, *_PARKED_RUN_ARGS], cwd=target, env=env)
            assert parked.returncode == 0, parked.stderr
            parked_payload = json.loads(parked.stdout)
            assert parked_payload["status"] == JOB_PAUSED
            parked_run_id = parked_payload["tasks"][0]["run_id"]

            relaunch = run_cli_in_process(
                ["job", "run", job.job_id, *_PARKED_RUN_ARGS], cwd=target, env=env)
            assert relaunch.returncode == 0, relaunch.stderr
            relaunch_payload = json.loads(relaunch.stdout)
            assert relaunch_payload["status"] == JOB_COMPLETED
            relaunch_run_id = relaunch_payload["tasks"][0]["run_id"]

            show = run_cli_in_process(
                ["run", "show", relaunch_run_id, "--json"], cwd=target, env=env)

        assert show.returncode == 0, show.stderr
        record = json.loads(show.stdout)
        parked_builder_session = next(
            c["session_id"] for c in calls if c["role"] == "builder")
        assert record["resumed_from_run_id"] == parked_run_id
        assert record["rounds"][0]["builder"]["resume_used"] is True
        assert record["rounds"][0]["builder"]["resume_session_ref"] == parked_builder_session
        assert record["resume_declined"] == {}

    def test_the_relaunch_on_a_provider_that_cannot_resume_names_the_decline(
            self, tmp_path, monkeypatch):
        job, target, env, stand_in, calls = _setup(tmp_path, monkeypatch)

        with patch.object(pingpong_provider, "_guarded_cli_run", side_effect=stand_in), \
             patch.object(pingpong_provider.ClaudeCliProvider, "_get_claude_path",
                          lambda self: "/fake/claude"), \
             patch.object(pingpong_provider.ClaudeCliProvider, "_resolve_version",
                          lambda self: "1.0.0 (test)"):
            parked = run_cli_in_process(
                ["job", "run", job.job_id, *_PARKED_RUN_ARGS], cwd=target, env=env)
            assert parked.returncode == 0, parked.stderr
            parked_payload = json.loads(parked.stdout)
            assert parked_payload["status"] == JOB_PAUSED
            parked_run_id = parked_payload["tasks"][0]["run_id"]

            # No model flags; an omitted --repair-rounds would read the parked
            # run's persisted 0 back (R-1163's round-8 failure) — the fake
            # reviewer needs a second round to pass by default.
            relaunch = run_cli_in_process(
                ["job", "run", job.job_id,
                 "--builder-provider", "fake", "--reviewer-provider", "fake",
                 "--repair-rounds", "1", "--json"],
                cwd=target, env=env)
            assert relaunch.returncode == 0, relaunch.stderr
            relaunch_payload = json.loads(relaunch.stdout)
            assert relaunch_payload["status"] == JOB_COMPLETED
            relaunch_run_id = relaunch_payload["tasks"][0]["run_id"]

            show = run_cli_in_process(
                ["run", "show", relaunch_run_id, "--json"], cwd=target, env=env)

        assert show.returncode == 0, show.stderr
        record = json.loads(show.stdout)
        assert record["resumed_from_run_id"] == parked_run_id
        assert record["rounds"][0]["builder"]["resume_used"] is False
        assert record["resume_declined"] == {
            "builder": "the fake provider cannot resume a session"}
