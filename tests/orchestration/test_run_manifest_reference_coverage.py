"""F1/F14 (round 9) — PUBLISHED REFERENCE vs CURRENT CANDIDATE coverage.

A manifest that is STORED as a terminal (completed/stopped) reference is a claim about a run
that already finished: its call coverage must be COMPLETE. Nothing may be published, and nothing
may be read back, that says "this run completed" and "I do not know all of its calls" at once —
that combination is corruption, and it is refused by the CANONICAL LOADER itself, not by a
second Evidence-only rule layered on top.

A CURRENT CANDIDATE is the opposite: it is reconstructed from live state and may legitimately be
incomplete, which `remedy job rerun --check-manifest` reports as exit 5.
"""
from __future__ import annotations

import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    COVERAGE_COMPLETE,
    COVERAGE_INCOMPLETE,
    MODE_CURRENT_CANDIDATE,
    MODE_PREPUBLICATION,
    MODE_PUBLISHED_REFERENCE,
    CallCoverage,
    ManifestError,
    load_latest_manifest_verified,
    validate_run_manifest,
    write_run_manifest,
)


def _bind(call):
    """A published reference must BIND every call to its stored input artifact (F1). The ref and
    the bytes come from PRODUCTION helpers, so the fixture cannot drift from the real rule. The
    binding is stamped AFTER the manifest fixes each call's episode id, because the artifact
    bytes carry that identity."""
    import hashlib

    from packages.orchestration.run_manifest import canonical_artifact_ref

    call = dataclasses.replace(call, artifact=canonical_artifact_ref(call.identity))
    return dataclasses.replace(
        call, artifact_sha256=hashlib.sha256(call.canonical_artifact_bytes()).hexdigest())


def _complete(status="completed"):
    m = T._mk(episode_id="ep1", status=status)
    return dataclasses.replace(m, calls=tuple(_bind(c) for c in m.calls))


def _incomplete(status="completed", problems=("prompt not reconstructable",)):
    return dataclasses.replace(
        _complete(status=status),
        coverage=CallCoverage(status=COVERAGE_INCOMPLETE, problems=tuple(problems)))


class TestPublishedTerminalReferenceNeedsCompleteCoverage:
    @pytest.mark.parametrize("status", ["completed", "stopped"])
    def test_incomplete_terminal_reference_is_rejected(self, status):
        m = _incomplete(status=status)
        if status == "stopped":
            m = dataclasses.replace(m, stop_request_id="stop-1")
        probs = validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE)
        assert any("complete call coverage" in p for p in probs), probs

    def test_complete_terminal_reference_is_accepted(self):
        assert validate_run_manifest(_complete(), mode=MODE_PUBLISHED_REFERENCE) == []

    def test_a_published_reference_requires_every_call_bound_to_an_artifact(self):
        """Complete coverage is not enough: a reference whose calls have no stored input
        artifact cannot be verified against, so it is not a reference."""
        m = T._mk(episode_id="ep1")          # calls with no artifact ref
        probs = validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE)
        assert any("artifact" in p for p in probs), probs

    def test_the_writer_refuses_to_publish_an_incomplete_terminal_reference(
            self, tmp_path):
        """The defect this closes: the writer published an incomplete `completed` manifest that
        the loader then had to accept. Refuse at the WRITE."""
        ev = tmp_path / "ev"
        ev.mkdir()
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _incomplete(), root=tmp_path)

    def test_a_stored_incomplete_terminal_manifest_fails_the_canonical_loader(
            self, tmp_path):
        """Even if bytes reach disk some other way (an older writer, a tamper), the CANONICAL
        LOADER refuses them — exit 1 (integrity), never exit 5 (incomplete candidate)."""
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, T._mk(episode_id="ep1"), root=tmp_path)
        # rewrite the stored episode with incomplete coverage, canonically encoded
        bad = _incomplete()
        from packages.orchestration.run_manifest import (
            MANIFEST_FILENAME,
            MANIFESTS_SUBDIR,
        )
        (ev / MANIFESTS_SUBDIR / "ep1" / MANIFEST_FILENAME).write_bytes(bad.canonical_bytes())
        (ev / MANIFEST_FILENAME).write_bytes(bad.canonical_bytes())
        with pytest.raises(ManifestError) as exc:
            load_latest_manifest_verified(ev, job_id="j")
        assert "coverage" in str(exc.value).lower()


class TestCurrentCandidateMayBeIncomplete:
    def test_incomplete_candidate_is_valid(self):
        """A candidate is reconstructed from live state; incomplete coverage is a reportable
        FACT (exit 5), not corruption."""
        assert validate_run_manifest(_incomplete(), mode=MODE_CURRENT_CANDIDATE) == []

    def test_an_incomplete_candidate_still_needs_a_bounded_problem(self):
        m = _incomplete(problems=())
        probs = validate_run_manifest(m, mode=MODE_CURRENT_CANDIDATE)
        assert any("problem" in p for p in probs), probs

    def test_a_complete_candidate_must_not_carry_problems(self):
        m = dataclasses.replace(
            _complete(), coverage=CallCoverage(status=COVERAGE_COMPLETE, problems=("huh",)))
        probs = validate_run_manifest(m, mode=MODE_CURRENT_CANDIDATE)
        assert any("problem" in p for p in probs), probs

    def test_prepublication_mode_does_not_apply_the_reference_rule(self):
        """Prepublication validates SHAPE; the reference-coverage rule belongs to publication."""
        assert not any("complete call coverage" in p for p in
                       validate_run_manifest(_incomplete(), mode=MODE_PREPUBLICATION))


class TestZeroCallTerminalCoverage:
    def test_a_real_zero_call_job_publishes_complete_coverage(self, data_root, repo):
        """Zero calls is COMPLETE only because the JobPlan proves zero calls were expected: the
        job was stopped before any work began."""
        from packages.orchestration.pingpong_job import (
            JOB_STOPPED,
            job_evidence_dir,
            parse_job_file,
            run_job,
        )
        from packages.orchestration.safe_points import request_stop

        job = parse_job_file(T._JOB, str(repo))
        request_stop(job.job_id, "operator requested stop", "test")
        done = run_job(job.job_id, builder_provider=T._prov(),
                       reviewer_provider=T._prov(), repair_rounds=0)
        assert done.status == JOB_STOPPED

        ref = load_latest_manifest_verified(job_evidence_dir(job.job_id), job_id=job.job_id)
        assert ref.calls == ()
        assert ref.coverage.status == COVERAGE_COMPLETE
        assert validate_run_manifest(ref, mode=MODE_PUBLISHED_REFERENCE) == []


# the real-run fixtures
data_root = T.data_root
repo = T.repo
