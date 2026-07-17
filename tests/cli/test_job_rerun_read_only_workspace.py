"""F11 (round 11) — `--check-manifest` inspects the workspace CONTAINED and READ-ONLY.

Two independent reproductions drove this:

* a persisted workspace path whose FINAL component looked normal but whose PARENT was a symlink
  to an outside repository — the check followed it, read that repository, and still reported
  complete coverage;
* `git object count before check: 3` → `after: 5`. The check ran `git add -A` + `git write-tree`,
  which writes blobs and tree objects into the repository it is inspecting and can fire clean
  filters. A check that mutates the thing it checks is not a check.

Now: resolve through the canonical worktree root with anchored no-follow traversal (every
component verified, parents included), then compare the STRICT read-only content identity — the
same digest every other worktree uses, built from git plumbing only.
"""
from __future__ import annotations

import os
import subprocess

import pytest

from packages.orchestration.pingpong_job import (
    _persist_job,
    job_evidence_dir,
    load_job_plan,
    parse_job_file,
    run_job,
)
from packages.orchestration.run_manifest import (
    COVERAGE_INCOMPLETE,
    build_current_candidate,
    contained_workspace_path,
    load_latest_manifest_verified,
)


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


def _git_repo(path, content="# demo"):
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(f"git init -q && git config user.email t@t && git config user.name t "
                   f"&& echo '{content}' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=path, check=True)
    return path


@pytest.fixture
def repo(tmp_path):
    return _git_repo(tmp_path / "repo")


def _prov():
    from packages.orchestration.pingpong_provider import FakeProvider
    return FakeProvider(pass_on_round=1, fail_on_round=99)


_JOB = "# Job: ro\n\n## Task 1\nx\n\nAcceptance:\n- y\n"


@pytest.fixture
def job_and_ref(data_root, repo):
    job = parse_job_file(_JOB, str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    j = load_job_plan(job.job_id)
    ref = load_latest_manifest_verified(job_evidence_dir(j.job_id), job_id=j.job_id)
    return j, ref


def _live_workspace(repo, name="job-live"):
    """A real workspace under the canonical `.remedy-wt/` root."""
    ws = repo / ".remedy-wt" / name
    ws.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "worktree", "add", "-q", "--detach", str(ws)], cwd=repo,
                   check=True, capture_output=True)
    return ws


def _point_at(job, path):
    job.job_workspace_path = str(path)
    _persist_job(job)
    return load_job_plan(job.job_id)


# --------------------------------------------------------------------------- containment


class TestContainment:
    def test_a_parent_symlink_escape_is_refused(self, job_and_ref, repo, tmp_path):
        """THE finding: one symlinked PARENT walked the check into another repository."""
        job, ref = job_and_ref
        outside = _git_repo(tmp_path / "outside_repo", content="SECRET-OUTSIDE-CONTENT")
        wt_root = repo / ".remedy-wt"
        wt_root.mkdir(exist_ok=True)
        os.symlink(str(outside), str(wt_root / "evilparent"))
        (outside / "job-x").mkdir(exist_ok=True)
        job = _point_at(job, wt_root / "evilparent" / "job-x")   # normal final component

        cand = build_current_candidate(ref, job)
        assert cand.coverage.status == COVERAGE_INCOMPLETE
        assert any("symlinked or resolves outside" in p for p in cand.coverage.problems), \
            cand.coverage.problems

    def test_the_outside_repository_is_never_read(self, job_and_ref, repo, tmp_path):
        job, ref = job_and_ref
        outside = _git_repo(tmp_path / "outside_repo", content="SECRET-OUTSIDE-CONTENT")
        wt_root = repo / ".remedy-wt"
        wt_root.mkdir(exist_ok=True)
        os.symlink(str(outside), str(wt_root / "evilparent"))
        (outside / "job-x").mkdir(exist_ok=True)
        job = _point_at(job, wt_root / "evilparent" / "job-x")
        cand = build_current_candidate(ref, job)
        wid = cand.episode_snapshot.input.episode_start_workspace_identity
        assert wid["status"] != "ok"
        assert not wid["digest"], "an escaping workspace must never be digested"

    def test_a_workspace_outside_the_canonical_root_is_refused(self, job_and_ref, tmp_path):
        job, ref = job_and_ref
        elsewhere = _git_repo(tmp_path / "elsewhere")
        job = _point_at(job, elsewhere)
        cand = build_current_candidate(ref, job)
        assert cand.coverage.status == COVERAGE_INCOMPLETE
        assert any("outside the canonical worktree root" in p
                   for p in cand.coverage.problems), cand.coverage.problems

    def test_a_symlinked_final_component_is_refused(self, job_and_ref, repo, tmp_path):
        job, ref = job_and_ref
        outside = _git_repo(tmp_path / "outside2")
        wt_root = repo / ".remedy-wt"
        wt_root.mkdir(exist_ok=True)
        os.symlink(str(outside), str(wt_root / "job-link"))
        job = _point_at(job, wt_root / "job-link")
        cand = build_current_candidate(ref, job)
        assert any("symlinked or resolves outside" in p for p in cand.coverage.problems)

    def test_a_contained_workspace_resolves(self, repo):
        ws = _live_workspace(repo)
        path, state = contained_workspace_path(ws, repo)
        assert state == "ok" and path is not None

    def test_the_persisted_path_is_not_its_own_trust_root(self, repo, tmp_path):
        """The path is a claim. It is checked against the canonical root, not believed."""
        outside = _git_repo(tmp_path / "outside3")
        path, state = contained_workspace_path(outside, repo)
        assert path is None and state == "escapes"


# --------------------------------------------------------------------------- read-only


class TestTheCheckIsReadOnly:
    def _snapshot_repo_state(self, repo, ws):
        objects = sorted(str(p.relative_to(repo)) for p in (repo / ".git" / "objects").rglob("*"))
        refs = sorted(str(p.relative_to(repo)) for p in (repo / ".git" / "refs").rglob("*"))
        index = (repo / ".git" / "index").read_bytes() if (repo / ".git" / "index").exists() \
            else b""
        files = sorted(str(p.relative_to(ws)) for p in ws.rglob("*") if ".git" not in str(p))
        logs = sorted(str(p.relative_to(repo)) for p in (repo / ".git" / "logs").rglob("*")) \
            if (repo / ".git" / "logs").exists() else []
        return objects, refs, index, files, logs

    def test_the_check_changes_nothing(self, job_and_ref, repo):
        """THE finding: `git object count before: 3 → after: 5`."""
        job, ref = job_and_ref
        ws = _live_workspace(repo)
        (ws / "uncommitted.txt").write_text("real uncommitted work")
        job = _point_at(job, ws)

        before = self._snapshot_repo_state(repo, ws)
        build_current_candidate(ref, job)
        after = self._snapshot_repo_state(repo, ws)

        assert before[0] == after[0], "the git object database changed"
        assert before[1] == after[1], "refs changed"
        assert before[2] == after[2], "the git index changed"
        assert before[3] == after[3], "working files changed"
        assert before[4] == after[4], "reflogs changed"

    def test_no_clean_filter_is_invoked(self, job_and_ref, repo):
        """`git add` runs clean filters. The identity uses plumbing that does not."""
        job, ref = job_and_ref
        ws = _live_workspace(repo)
        marker = repo / "clean_filter_ran"
        (ws / ".gitattributes").write_text("* filter=canary\n")
        subprocess.run(["git", "config", "filter.canary.clean",
                        f"sh -c 'touch {marker}; cat'"], cwd=ws, check=True)
        (ws / "content.txt").write_text("data")
        job = _point_at(job, ws)

        build_current_candidate(ref, job)
        assert not marker.exists(), "a clean filter ran during a read-only check"

    def test_the_check_still_produces_a_real_identity(self, job_and_ref, repo):
        """Read-only must not mean blind: the current workspace is genuinely digested."""
        job, ref = job_and_ref
        ws = _live_workspace(repo)
        job = _point_at(job, ws)
        cand = build_current_candidate(ref, job)
        wid = cand.episode_snapshot.input.episode_start_workspace_identity
        assert wid["status"] == "ok"
        assert len(wid["digest"]) == 64
        assert wid["dirty"] is False

    def test_workspace_drift_is_still_detected(self, job_and_ref, repo):
        """The whole point of inspecting it: a mutated workspace must look different."""
        job, ref = job_and_ref
        ws = _live_workspace(repo)
        job = _point_at(job, ws)
        clean = build_current_candidate(ref, job).episode_snapshot.input
        (ws / "drifted.txt").write_text("someone changed the workspace")
        dirty = build_current_candidate(ref, job).episode_snapshot.input
        assert clean.episode_start_workspace_identity["digest"] != \
            dirty.episode_start_workspace_identity["digest"]
        assert dirty.episode_start_workspace_identity["dirty"] is True

    def test_the_check_makes_no_provider_call(self, job_and_ref, repo, monkeypatch):
        job, ref = job_and_ref
        ws = _live_workspace(repo)
        job = _point_at(job, ws)

        import packages.orchestration.pingpong_provider as _pp

        calls = {"n": 0}
        real = getattr(_pp.FakeProvider, "build")

        def _count(self, *a, **k):
            calls["n"] += 1
            return real(self, *a, **k)

        monkeypatch.setattr(_pp.FakeProvider, "build", _count)
        build_current_candidate(ref, job)
        assert calls["n"] == 0
