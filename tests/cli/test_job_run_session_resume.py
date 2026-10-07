"""R-1163 (F287): a relaunch typed as `remedy job run` resumes the parked `claude-cli`
session, and names a resume that a provider declined.

The hardening stage's acceptance audit found that every proof of F287 called `run_job`,
`run_pingpong` or `resume_declined_reasons` from test code. These tests use Remedy the way an
operator does, through the command-line dispatcher (`run_cli_in_process`, never `run_job` and
never a subprocess): `remedy job run` starts a `claude-cli` job on a git target; the stand-in for
the `claude` child types `remedy job pause` during the first builder call, so the job parks; a
second `remedy job run` relaunches it; and `remedy run show --json` reads the relaunch's record.
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

            # No model flags. An omitted --repair-rounds would read the parked
            # run's 0 back from the job's saved config, and the `fake` reviewer
            # passes only on its second call.
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
