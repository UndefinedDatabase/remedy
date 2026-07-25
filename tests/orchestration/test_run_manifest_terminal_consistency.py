"""F8 — complete TERMINAL JobPlan / index / latest-manifest agreement.

For a terminal (completed/stopped) job, the JobPlan, the index's latest and the latest manifest
must agree on every field; any mismatch is a blocking integrity failure.
"""
from __future__ import annotations

import dataclasses

import tests.orchestration.test_run_manifest as T
from packages.orchestration.job_evidence import _crosscheck_terminal_jobplan_manifest
from packages.orchestration.pingpong_job import JOB_COMPLETED, JOB_STOPPED


class _Job:
    def __init__(self, **kw):
        self.status = kw.get("status", JOB_COMPLETED)
        self.active_episode_id = kw.get("active", "ep1")
        self.run_manifest_created_at = kw.get("created_at", "2026-07-15T00:00:00+00:00")
        self.run_manifest_path = kw.get("path", "run_manifest.json")
        self.stop_request_id = kw.get("stop_request_id", "")
        # F13: a terminal JobPlan must carry its episode summary too.
        self.run_manifest_episodes = kw.get(
            "episodes", [{"episode_id": self.active_episode_id, "episode_ordinal": 1}])


def _latest(status="completed", stop_request_id="", episode_id="ep1"):
    return dataclasses.replace(
        T._mk(episode_id=episode_id, status=status),
        stop_request_id=stop_request_id)


def _index(latest_id="ep1"):
    return {"index_v": 1, "latest_episode_id": latest_id,
            "episodes": [{"episode_id": latest_id, "episode_ordinal": 1}]}


def _run(job, latest, index):
    return _crosscheck_terminal_jobplan_manifest(job, latest, index)


class TestTerminalAgreement:
    def test_clean_completed_agrees(self):
        assert _run(_Job(), _latest(), _index()) == []

    def test_active_differs_from_latest_blocks(self):
        probs = _run(_Job(active="ep2"), _latest(episode_id="ep1"), _index("ep1"))
        assert any("active_episode_id" in p for p in probs), probs

    def test_status_mismatch_blocks(self):
        job = _Job(status=JOB_STOPPED, stop_request_id="req1")
        probs = _run(job, _latest(status="completed"), _index())
        assert any("status" in p for p in probs), probs

    def test_created_at_mismatch_blocks(self):
        probs = _run(_Job(created_at="2026-01-01T00:00:00+00:00"), _latest(), _index())
        assert any("created_at" in p for p in probs), probs

    def test_stopped_request_id_mismatch_blocks(self):
        job = _Job(status=JOB_STOPPED, stop_request_id="reqA")
        latest = _latest(status="stopped", stop_request_id="reqB")
        probs = _run(job, latest, _index())
        assert any("stop_request_id" in p for p in probs), probs

    def test_completed_with_stopped_metadata_blocks(self):
        latest = _latest(status="completed", stop_request_id="reqX")
        # (a completed latest carrying a stop_request_id is itself invalid, but the terminal
        # crosscheck also flags the stopped-only metadata on a completed job)
        probs = _run(_Job(status=JOB_COMPLETED), latest, _index())
        assert any("stopped-only" in p for p in probs), probs

    def test_path_mismatch_blocks(self):
        probs = _run(_Job(path="run_manifests/ep1/run_manifest.json"), _latest(), _index())
        assert any("run_manifest_path" in p for p in probs), probs
