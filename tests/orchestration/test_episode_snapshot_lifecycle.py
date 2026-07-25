"""F1/F5/F12 — the episode snapshot lifecycle in the REAL run_job() production flow.

* F1: a FAILED mandatory episode-start snapshot HARD-BLOCKS the job before any task or provider
  call — zero provider calls, a durable blocked status carrying the reason, no false "completed".
* F12: a failed episode-start-workspace-tree capture is itself a snapshot failure (never a
  silent empty tree), and blocks the same way.
* F5: a stopped manifest, its embedded snapshot and its calls all name the SAME episode id; the
  stop REQUEST id is separate terminal metadata.
"""
from __future__ import annotations

import subprocess

import pytest

from packages.orchestration import run_manifest as RM
from packages.orchestration import worktrees as W
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_STOPPED,
    job_evidence_dir,
    load_job_plan,
    parse_job_file,
    run_job,
)
from packages.orchestration.run_manifest import (
    decode_episode_snapshot_v1,
    load_latest_manifest_verified,
)

_JOB = "# Job: snap lifecycle\n\n## Task 1\nDo a thing.\n\nAcceptance:\n- done\n"


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=r, check=True)
    return r


class _CountingProvider:
    def __init__(self):
        self.build_calls = 0
        self.review_calls = 0

    @property
    def name(self):
        return "fake"

    def build(self, prompt, **kwargs):
        self.build_calls += 1
        from packages.orchestration.pingpong_provider import FakeProvider
        return FakeProvider(pass_on_round=1, fail_on_round=99).build(prompt, **kwargs)

    def review(self, prompt, **kwargs):
        self.review_calls += 1
        from packages.orchestration.pingpong_provider import FakeProvider
        return FakeProvider(pass_on_round=1, fail_on_round=99).review(prompt, **kwargs)


# --------------------------------------------------------------------------- F1


def test_failed_snapshot_capture_blocks_before_any_provider_call(
        data_root, repo, monkeypatch):
    job = parse_job_file(_JOB, str(repo))
    # Force the episode-start snapshot capture to fail.
    monkeypatch.setattr(RM, "build_input_snapshot",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    prov = _CountingProvider()
    done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov, repair_rounds=0)

    assert prov.build_calls == 0 and prov.review_calls == 0   # zero provider work
    assert done.status == JOB_BLOCKED                         # not running, not completed
    assert done.status != "completed"
    assert done.input_snapshot_error                          # durable reason recorded
    # No terminal manifest was written from a re-probe.
    reloaded = load_job_plan(job.job_id)
    assert reloaded.input_snapshot_error
    assert reloaded.status == JOB_BLOCKED


def test_failed_workspace_tree_capture_is_a_snapshot_failure(data_root, repo, monkeypatch):
    # F12: the episode-start workspace tree cannot be captured → the whole snapshot fails →
    # zero provider work, blocked, and NO silent empty-tree substitution. write_tree is failed
    # ONLY for the episode-start capture (once the workspace has been acquired), so workspace
    # acquisition itself still succeeds and the failure is genuinely the snapshot's.
    import sys
    job = parse_job_file(_JOB, str(repo))
    real_write_tree = W.write_tree
    # The episode-start-tree capture is the FIRST write_tree call made directly from run_job
    # (acquisition's calls come from _acquire_job_workspace; the task-start-tree call comes
    # later). Fail exactly that one, so acquisition succeeds and the failure is the snapshot's.
    state = {"rj": 0}

    def _fail_episode_start_tree(handle, *a, **k):
        if sys._getframe(1).f_code.co_name == "run_job":
            state["rj"] += 1
            if state["rj"] == 1:
                raise RuntimeError("no tree")
        return real_write_tree(handle, *a, **k)

    monkeypatch.setattr(W, "write_tree", _fail_episode_start_tree)
    prov = _CountingProvider()
    done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov, repair_rounds=0)

    assert prov.build_calls == 0 and prov.review_calls == 0
    assert done.status == JOB_BLOCKED
    assert "workspace_tree" in done.input_snapshot_error
    # the empty tree was NOT accepted as a valid snapshot
    reloaded = load_job_plan(job.job_id)
    wrapper = decode_episode_snapshot_v1(reloaded.input_snapshot)
    assert not wrapper.is_ok()


# --------------------------------------------------------------------------- F5


def test_stopped_manifest_snapshot_and_calls_share_one_episode(data_root, repo):
    from packages.orchestration.safe_points import request_stop

    job = parse_job_file(_JOB, str(repo))

    class _StopDuringBuild(_CountingProvider):
        def build(self, prompt, **kwargs):
            request_stop(job.job_id, "operator requested stop", "test")
            return super().build(prompt, **kwargs)

    prov = _StopDuringBuild()
    done = run_job(job.job_id, builder_provider=prov, reviewer_provider=_CountingProvider(),
                   repair_rounds=0)
    assert done.status == JOB_STOPPED

    ref = load_latest_manifest_verified(job_evidence_dir(job.job_id), job_id=job.job_id)
    assert ref.status == "stopped"
    # F5: snapshot episode == manifest episode == active episode; every call shares it.
    assert ref.episode_snapshot.episode_id == ref.episode_id == done.active_episode_id
    for c in ref.calls:
        assert c.identity.episode_id == ref.episode_id
    # F5: the stop REQUEST id is SEPARATE terminal metadata, not the episode id.
    assert ref.stop_request_id and ref.stop_request_id != ref.episode_id
    assert ref.stop_request_id == done.stop_request_id


def test_pre_work_stop_uses_one_coherent_episode(data_root, repo):
    from packages.orchestration.safe_points import request_stop

    job = parse_job_file(_JOB, str(repo))
    request_stop(job.job_id, "operator requested stop", "cli")
    prov = _CountingProvider()
    done = run_job(job.job_id, builder_provider=prov, reviewer_provider=prov, repair_rounds=0)

    assert done.status == JOB_STOPPED
    assert prov.build_calls == 0                     # no work began
    ref = load_latest_manifest_verified(job_evidence_dir(job.job_id), job_id=job.job_id)
    assert ref.episode_snapshot.episode_id == ref.episode_id == done.active_episode_id
    assert ref.episode_snapshot.capture_phase == "pre_work_stop"
    assert ref.stop_request_id == done.stop_request_id
