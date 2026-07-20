"""F12 — a missing/symlinked resumable workspace is INCOMPLETE, never "same inputs"."""
from __future__ import annotations

import os
import subprocess

import pytest

from packages.orchestration.pingpong_job import (
    job_evidence_dir,
    load_job_plan,
    parse_job_file,
    run_job,
)
from packages.orchestration.run_manifest import (
    build_current_candidate,
    diff_manifests,
    load_latest_manifest_verified,
)


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "remedy_data"; root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"; r.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=r, check=True)
    return r


def _prov():
    from packages.orchestration.pingpong_provider import FakeProvider
    return FakeProvider(pass_on_round=1, fail_on_round=99)


def _stopped_zero_call_job(repo):
    from packages.orchestration.safe_points import request_stop
    job = parse_job_file("# Job: w\n\n## Task 1\nx\n\nAcceptance:\n- y\n", str(repo))
    request_stop(job.job_id, "operator requested stop", "cli")
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    return job.job_id


def _check(job_id):
    ev = job_evidence_dir(job_id)
    ref = load_latest_manifest_verified(ev, job_id=job_id)
    job = load_job_plan(job_id)
    cand = build_current_candidate(ref, job)
    return diff_manifests(ref, cand), cand


class TestResumableWorkspace:
    def test_missing_workspace_is_never_same(self, data_root, repo):
        job_id = _stopped_zero_call_job(repo)
        job = load_job_plan(job_id)
        # the stopped job names a workspace that is now gone
        job.job_workspace_path = "/nonexistent/workspace/for/this/job"
        from packages.orchestration.pingpong_job import _persist_job
        _persist_job(job)
        diff, cand = _check(job_id)
        assert cand.coverage.status == "incomplete"
        # F11 (round 11): a path outside the canonical worktree root is refused as an ESCAPE —
        # a stronger verdict than "missing", and still never "same inputs".
        assert any("outside the canonical worktree root" in p
                   for p in cand.coverage.problems), cand.coverage.problems
        assert diff["same_inputs"] is not True
        assert diff["verification_complete"] is False

    def test_symlinked_workspace_is_refused(self, data_root, repo, tmp_path):
        job_id = _stopped_zero_call_job(repo)
        job = load_job_plan(job_id)
        target = tmp_path / "elsewhere"; target.mkdir()
        link = tmp_path / "ws_link"
        os.symlink(str(target), str(link))
        job.job_workspace_path = str(link)
        from packages.orchestration.pingpong_job import _persist_job
        _persist_job(job)
        diff, cand = _check(job_id)
        assert cand.coverage.status == "incomplete"
        assert any("symlinked or resolves outside" in p
                   for p in cand.coverage.problems), cand.coverage.problems
        assert diff["same_inputs"] is not True

    def test_existing_workspace_equality_stays_honest(self, data_root, repo):
        job_id = _stopped_zero_call_job(repo)
        diff, cand = _check(job_id)
        # the real workspace still exists → its CURRENT tree is proven, no workspace problem
        assert not any("workspace" in p for p in cand.coverage.problems)
