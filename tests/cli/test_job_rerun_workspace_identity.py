"""F8 (round 12) — ONE canonical workspace identity format.

The reference recorded a 40-hex git TREE OBJECT in `episode_start_workspace_tree`; the candidate
recorded a 64-hex content DIGEST in the same field; and the logical projection compared the field
directly. So an otherwise identical workspace produced blocking drift and different logical
hashes — two different kinds of thing had been sharing one field name.

Only one of them can be recomputed read-only (computing a git tree WRITES objects — see F11,
round 11), so that is the one the identity uses: the typed `episode_start_workspace_identity`.
`episode_start_workspace_tree` stays as provenance and is never the comparison.
"""
from __future__ import annotations

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
    build_current_candidate,
    diff_manifests,
    load_latest_manifest_verified,
)


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


def _prov():
    from packages.orchestration.pingpong_provider import FakeProvider
    return FakeProvider(pass_on_round=1, fail_on_round=99)


_JOB = "# Job: id\n\n## Task 1\nx\n\nAcceptance:\n- y\n"


@pytest.fixture
def live(data_root, repo):
    """A finished job pointed at a REAL live workspace under the canonical root."""
    job = parse_job_file(_JOB, str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    j = load_job_plan(job.job_id)
    ref = load_latest_manifest_verified(job_evidence_dir(j.job_id), job_id=j.job_id)
    ws = repo / ".remedy-wt" / "job-live"
    ws.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "worktree", "add", "-q", "--detach", str(ws)], cwd=repo,
                   check=True, capture_output=True)
    j.job_workspace_path = str(ws)
    _persist_job(j)
    return load_job_plan(j.job_id), ref, ws


# --------------------------------------------------------------------------- the finding


class TestNoFalseWorkspaceDrift:
    def test_the_reproduced_case(self, live):
        """An identical workspace used to produce blocking drift on
        `episode_start_workspace_tree`, purely because the two sides recorded different KINDS of
        hash into it."""
        job, ref, _ws = live
        cand = build_current_candidate(ref, job)
        diff = diff_manifests(ref, cand)
        fields = [b["field"] for b in diff["blocking"]]
        assert "episode_start_workspace_tree" not in fields, fields
        assert "episode_start_workspace_identity" not in fields, fields

    def test_an_unchanged_stopped_workspace_shows_no_drift(self, live):
        job, ref, _ws = live
        assert diff_manifests(ref, build_current_candidate(ref, job))["blocking"] == []

    def test_a_mutated_workspace_shows_blocking_drift(self, live):
        job, ref, ws = live
        clean = build_current_candidate(ref, job)
        assert diff_manifests(ref, clean)["blocking"] == []
        (ws / "someone_changed_this.txt").write_text("drift")
        dirty = build_current_candidate(ref, job)
        fields = [b["field"] for b in diff_manifests(ref, dirty)["blocking"]]
        assert "episode_start_workspace_identity" in fields, fields


# --------------------------------------------------------------------------- one format


class TestOneCanonicalIdentityFormat:
    def test_reference_and_candidate_use_the_same_digest_format(self, live):
        job, ref, _ws = live
        cand = build_current_candidate(ref, job)
        r = ref.episode_snapshot.input.episode_start_workspace_identity
        c = cand.episode_snapshot.input.episode_start_workspace_identity
        assert set(r) == set(c)
        assert len(r["digest"]) == len(c["digest"]) == 64      # both the strict content digest

    def test_the_tree_field_is_provenance_only(self, live):
        """A 40-hex git tree object and a 64-hex content digest are different things; the
        candidate never writes one where the reference holds the other."""
        job, ref, _ws = live
        cand = build_current_candidate(ref, job)
        assert len(ref.episode_snapshot.input.episode_start_workspace_tree) == 40
        assert cand.episode_snapshot.input.episode_start_workspace_tree == \
            ref.episode_snapshot.input.episode_start_workspace_tree

    def test_the_logical_projection_carries_the_typed_identity(self, live):
        job, ref, _ws = live
        proj = ref.logical_input_projection()
        assert "episode_start_workspace_identity" in proj
        assert "episode_start_workspace_tree" not in proj

    def test_equal_identities_project_equally(self, live):
        """The workspace's contribution to the logical identity must be identical on both sides
        when the workspace is. (The rest of the projection legitimately moves — creating the
        worktree changes the target repo's own content.)"""
        job, ref, _ws = live
        cand = build_current_candidate(ref, job)
        assert ref.logical_input_projection()["episode_start_workspace_identity"] == \
            cand.logical_input_projection()["episode_start_workspace_identity"]


# --------------------------------------------------------------------------- one read


class TestTheCandidateReadsTheWorkspaceExactlyOnce:
    def test_one_inspection_per_candidate(self, live, monkeypatch):
        job, ref, _ws = live
        import packages.orchestration.run_manifest as RM

        calls = {"n": 0}
        real = RM.inspect_contained_workspace_identity

        def _count(*a, **k):
            calls["n"] += 1
            return real(*a, **k)

        monkeypatch.setattr(RM, "inspect_contained_workspace_identity", _count)
        build_current_candidate(ref, job)
        assert calls["n"] == 1, f"the candidate inspected the workspace {calls['n']} times"
