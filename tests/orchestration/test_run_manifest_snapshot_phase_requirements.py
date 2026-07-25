"""F10 (round 11) — what a Snapshot must carry depends on HOW it was captured.

A completed WORKED manifest was accepted with `job_initial_tree = ""` and with
`episode_start_workspace_tree = ""`. Those are material identities: they decided what the run was
given. An empty string there is not "unknown", it is a hole where an input should be — and a
manifest with a hole in it still claimed to pin the run's inputs.

A pre-work stop or a planning-only episode genuinely has no workspace to identify. That is fine,
and it must be said in a TYPED way — an `unavailable` identity carrying a reason — never by
leaving a blank for the reader to interpret.

A git tree object is also not enough for a read-only comparison (computing one WRITES objects —
see F11), so the snapshot carries `episode_start_workspace_identity`: the same strict content
digest every other worktree uses.
"""
from __future__ import annotations

import dataclasses
import hashlib

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    GIT_OK,
    GIT_UNAVAILABLE,
    MODE_PUBLISHED_REFERENCE,
    PHASE_EPISODE_START,
    PHASE_PLANNING_ONLY,
    PHASE_PRE_WORK_STOP,
    canonical_artifact_ref,
    decode_input_snapshot_v1,
    validate_run_manifest,
    validate_snapshot_phase_identities,
)


def _bind(m):
    bound = []
    for c in m.calls:
        c = dataclasses.replace(c, artifact=canonical_artifact_ref(c.identity))
        bound.append(dataclasses.replace(
            c, artifact_sha256=hashlib.sha256(c.canonical_artifact_bytes()).hexdigest()))
    return dataclasses.replace(m, calls=tuple(bound))


def _worked(**over):
    return validate_run_manifest(
        _bind(T._mk(episode_id="ep1", snap=dataclasses.replace(T._snap(), **over))),
        mode=MODE_PUBLISHED_REFERENCE)


# --------------------------------------------------------------------------- worked


class TestAWorkedEpisodeNeedsEveryMaterialIdentity:
    @pytest.mark.parametrize("field", [
        "remedy_git_sha", "target_base_commit", "job_initial_tree",
        "episode_start_workspace_tree", "job_file_sha256",
    ])
    def test_an_empty_identity_blocks(self, field):
        """THE finding: `job_initial_tree=""` and `episode_start_workspace_tree=""` were both
        accepted on a completed worked manifest."""
        probs = _worked(**{field: ""})
        assert any(f"must record {field}" in p for p in probs), probs

    def test_a_complete_worked_snapshot_passes(self):
        assert _worked() == []

    def test_an_unavailable_workspace_identity_without_a_reason_blocks(self):
        """A worked episode CAN legitimately fail to obtain the identity (a non-git target, a
        workspace already cleaned) — but only when it says so. A blank unavailable is a hole."""
        probs = _worked(episode_start_workspace_identity={
            "status": GIT_UNAVAILABLE, "head": "unavailable", "digest": "",
            "problems": [], "dirty": None})
        assert any("gives no reason" in p for p in probs), probs

    def test_an_unavailable_workspace_identity_with_a_reason_is_accepted(self):
        assert _worked(episode_start_workspace_identity={
            "status": GIT_UNAVAILABLE, "head": "unavailable", "digest": "",
            "problems": ["the target is not a git repository"], "dirty": None}) == []

    def test_an_unsupported_workspace_status_blocks(self):
        probs = _worked(episode_start_workspace_identity={
            "status": "probably-fine", "head": "", "digest": "", "problems": [],
            "dirty": None})
        assert any("supported status" in p for p in probs), probs

    def test_an_ok_identity_without_a_digest_blocks(self):
        probs = _worked(episode_start_workspace_identity={
            "status": GIT_OK, "head": "c" * 40, "digest": "", "problems": [], "dirty": False})
        assert any("carries no digest" in p for p in probs), probs

    def test_the_identity_is_the_strict_worktree_record(self):
        """It must be the SAME shape (and therefore the same digest) as every other worktree
        identity, so a check can compare like with like."""
        snap = T._snap()
        raw = snap.to_json()
        assert set(raw["episode_start_workspace_identity"]) == \
            set(raw["remedy_worktree"])
        # ...and it survives the strict decoder unchanged
        assert decode_input_snapshot_v1(raw).episode_start_workspace_identity == \
            snap.episode_start_workspace_identity


# --------------------------------------------------------------------------- non-worked


class TestNonWorkedPhasesStateUnavailabilityExplicitly:
    @pytest.mark.parametrize("phase", [PHASE_PRE_WORK_STOP, PHASE_PLANNING_ONLY])
    def test_an_unavailable_identity_with_a_reason_is_accepted(self, phase):
        snap = dataclasses.replace(T._snap(), episode_start_workspace_identity={
            "status": GIT_UNAVAILABLE, "head": "unavailable", "digest": "",
            "problems": ["no job workspace is named"], "dirty": None})
        assert validate_snapshot_phase_identities(snap, capture_phase=phase) == []

    @pytest.mark.parametrize("phase", [PHASE_PRE_WORK_STOP, PHASE_PLANNING_ONLY])
    def test_an_unavailable_identity_without_a_reason_blocks(self, phase):
        """An unavailable value must be explained. A blank one is just a blank."""
        snap = dataclasses.replace(T._snap(), episode_start_workspace_identity={
            "status": GIT_UNAVAILABLE, "head": "unavailable", "digest": "",
            "problems": [], "dirty": None})
        probs = validate_snapshot_phase_identities(snap, capture_phase=phase)
        assert any("gives no reason" in p for p in probs), probs

    @pytest.mark.parametrize("phase", [PHASE_PRE_WORK_STOP, PHASE_PLANNING_ONLY])
    def test_an_unsupported_status_blocks(self, phase):
        snap = dataclasses.replace(T._snap(), episode_start_workspace_identity={
            "status": "probably-fine", "head": "", "digest": "", "problems": [], "dirty": None})
        probs = validate_snapshot_phase_identities(snap, capture_phase=phase)
        assert any("not a supported status" in p for p in probs), probs

    @pytest.mark.parametrize("phase", [PHASE_PRE_WORK_STOP, PHASE_PLANNING_ONLY])
    def test_a_non_worked_phase_does_not_demand_a_workspace(self, phase):
        """It never acquired one — demanding it would be inventing an input."""
        snap = dataclasses.replace(
            T._snap(), episode_start_workspace_tree="", job_initial_tree="",
            episode_start_workspace_identity={
                "status": GIT_UNAVAILABLE, "head": "unavailable", "digest": "",
                "problems": ["no job workspace is named"], "dirty": None})
        assert validate_snapshot_phase_identities(snap, capture_phase=phase) == []


# --------------------------------------------------------------------------- production


class TestProductionCapturesTheIdentity:
    def test_a_real_run_records_a_complete_workspace_identity(self, data_root, repo):
        from packages.orchestration.pingpong_job import job_evidence_dir
        from packages.orchestration.run_manifest import load_latest_manifest_verified

        job_id, _res = T._run(T._JOB, repo)
        ref = load_latest_manifest_verified(job_evidence_dir(job_id), job_id=job_id)
        wid = ref.episode_snapshot.input.episode_start_workspace_identity
        assert wid["status"] == GIT_OK
        assert len(wid["digest"]) == 64
        assert ref.episode_snapshot.capture_phase == PHASE_EPISODE_START
        assert validate_run_manifest(ref, mode=MODE_PUBLISHED_REFERENCE) == []

    def test_a_pre_work_stop_states_its_missing_workspace_explicitly(self, data_root, repo):
        from packages.orchestration.pingpong_job import (
            job_evidence_dir,
            parse_job_file,
            run_job,
        )
        from packages.orchestration.run_manifest import load_latest_manifest_verified
        from packages.orchestration.safe_points import request_stop

        job = parse_job_file(T._JOB, str(repo))
        request_stop(job.job_id, "operator requested stop", "test")
        run_job(job.job_id, builder_provider=T._prov(), reviewer_provider=T._prov(),
                repair_rounds=0)
        ref = load_latest_manifest_verified(job_evidence_dir(job.job_id), job_id=job.job_id)
        wid = ref.episode_snapshot.input.episode_start_workspace_identity
        assert wid["status"] != GIT_OK
        assert wid["problems"], "an unavailable identity must say why"
        assert validate_run_manifest(ref, mode=MODE_PUBLISHED_REFERENCE) == []


data_root = T.data_root
repo = T.repo
