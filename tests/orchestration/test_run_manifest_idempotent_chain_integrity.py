"""F2/F3/F4/F5 (round 11) — every writer path validates the COMPLETE existing chain.

Round 10 gave the new-append path a full preflight and left the idempotent path with almost none.
So retrying an unchanged episode over a chain whose PRIOR artifact had since been tampered with
returned success, and the canonical loader then rejected the very tree the writer had just blessed.
Success has to mean the same thing on every path or it means nothing.

Every path — first episode, append, idempotent retry, concurrent convergence, Stop retry,
recovery, Root/Index repair — now goes through `load_verified_canonical_chain_for_write`, and the
projections are written only from the resulting `VerifiedCanonicalChain`.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    MANIFEST_FILENAME,
    MANIFEST_INDEX_FILENAME,
    MANIFESTS_SUBDIR,
    ManifestConflictError,
    ManifestError,
    VerifiedCanonicalChain,
    _mirror_and_index,
    canonical_artifact_ref,
    load_latest_manifest_verified,
    load_verified_canonical_chain_for_write,
    read_index,
    rebuild_manifest_mirror_and_index_from_canonical_episodes,
    validate_index_and_tree,
    write_run_manifest,
)


def _ep(episode_id, ordinal, *, prev="", prior=()):
    # Round 13 (F5): a per-EPISODE run id — production re-runs a task under a NEW run when
    # a job resumes, so two episodes never share a run while each ledger lists only its own
    # call. (One run that legitimately spans episodes carries the earlier entries forward;
    # `validate_ledger_chain` holds it to that.)
    # Round 15 (F1): a multi-episode chain in which each episode DOES WORK is F011's
    # stop-then-resume: the stopped episode's task waits at `pending` and the resume
    # starts a NEW run. A chain of COMPLETED episodes each executing the same task is a
    # shape production cannot produce -- a completed job is done, and the resume loop
    # `continue`s past an applied task rather than running it again.
    m = T._mk(episode_id=episode_id, status="stopped",
              calls=(T._call(run=f"r-{episode_id}"),))
    m = dataclasses.replace(m, stop_request_id=f"stop-{episode_id}")
    bound = []
    for c in m.calls:
        c = dataclasses.replace(c, artifact=canonical_artifact_ref(c.identity))
        bound.append(dataclasses.replace(
            c, artifact_sha256=hashlib.sha256(c.canonical_artifact_bytes()).hexdigest()))
    return dataclasses.replace(m, calls=tuple(bound), episode_ordinal=ordinal,
                               previous_episode_id=prev, prior_episode_ids=tuple(prior),
                               created_at=f"2026-07-15T00:0{ordinal}:00+00:00")


@pytest.fixture
def two_episodes(tmp_path):
    ev = tmp_path / "ev"
    ev.mkdir()
    write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
    write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
    return ev


def _artifact(ev, eid):
    return sorted((ev / MANIFESTS_SUBDIR / eid / "calls").glob("*.json"))[0]


def _index_bytes(ev):
    return (ev / MANIFEST_INDEX_FILENAME).read_bytes()


# --------------------------------------------------------------------------- F2


class TestIdempotentRetryValidatesTheWholeChain:
    def test_retry_over_a_tampered_prior_artifact_blocks(self, two_episodes, tmp_path):
        """THE finding: the idempotent ep2 retry returned success while ep1's artifact was
        already broken, and the loader rejected the tree immediately afterwards."""
        _artifact(two_episodes, "ep1").write_bytes(b'{"tampered": true}')
        before = _index_bytes(two_episodes)
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(two_episodes, _ep("ep2", 2, prev="ep1", prior=("ep1",)),
                               root=tmp_path)
        assert "artifact" in str(exc.value)
        assert _index_bytes(two_episodes) == before        # nothing advanced

    def test_retry_over_a_missing_prior_artifact_blocks(self, two_episodes, tmp_path):
        _artifact(two_episodes, "ep1").unlink()
        with pytest.raises(ManifestError):
            write_run_manifest(two_episodes, _ep("ep2", 2, prev="ep1", prior=("ep1",)),
                               root=tmp_path)

    def test_retry_over_an_extra_prior_artifact_blocks(self, two_episodes, tmp_path):
        (_artifact(two_episodes, "ep1").parent / "EXTRA.json").write_bytes(b"{}")
        with pytest.raises(ManifestError):
            write_run_manifest(two_episodes, _ep("ep2", 2, prev="ep1", prior=("ep1",)),
                               root=tmp_path)

    def test_retry_over_an_extra_artifact_in_ITS_OWN_episode_blocks(self, tmp_path):
        """THE second finding: `ep1/calls/EXTRA.json` + an ep1 retry returned success, and the
        loader rejected the undeclared artifact."""
        ev = tmp_path / "ev"
        ev.mkdir()
        m = _ep("ep1", 1)
        write_run_manifest(ev, m, root=tmp_path)
        (_artifact(ev, "ep1").parent / "EXTRA.json").write_bytes(b"{}")
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, m, root=tmp_path)
        assert "undeclared" in str(exc.value) or "complete canonical episode" in str(exc.value)

    def test_retry_over_a_tampered_prior_MANIFEST_blocks(self, two_episodes, tmp_path):
        (two_episodes / MANIFESTS_SUBDIR / "ep1" / MANIFEST_FILENAME).write_bytes(b'{"x": 1}')
        with pytest.raises(ManifestError):
            write_run_manifest(two_episodes, _ep("ep2", 2, prev="ep1", prior=("ep1",)),
                               root=tmp_path)

    def test_a_clean_idempotent_retry_still_converges(self, two_episodes, tmp_path):
        write_run_manifest(two_episodes, _ep("ep2", 2, prev="ep1", prior=("ep1",)),
                           root=tmp_path)
        assert validate_index_and_tree(two_episodes, job_id="j") == []
        assert load_latest_manifest_verified(two_episodes, job_id="j").episode_id == "ep2"

    def test_an_idempotent_retry_does_NOT_restore_its_own_missing_artifact(self, tmp_path):
        """F2 (round 12): episodes publish atomically as complete directories, so a missing
        artifact afterwards is corruption, tamper or storage loss — never a partial write.
        Recreating it would erase the only evidence that something went wrong."""
        ev = tmp_path / "ev"
        ev.mkdir()
        m = _ep("ep1", 1)
        write_run_manifest(ev, m, root=tmp_path)
        art = _artifact(ev, "ep1")
        art.unlink()
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, m, root=tmp_path)
        assert "missing call artifact" in str(exc.value)
        assert not art.exists(), "the writer recreated an immutable published artifact"

    def test_a_conflicting_own_artifact_blocks_the_retry(self, tmp_path):
        """An immutable artifact whose bytes changed is corruption — verified, never overwritten."""
        ev = tmp_path / "ev"
        ev.mkdir()
        m = _ep("ep1", 1)
        write_run_manifest(ev, m, root=tmp_path)
        tampered = b'{"someone": "else"}'
        _artifact(ev, "ep1").write_bytes(tampered)
        with pytest.raises(ManifestError):
            write_run_manifest(ev, m, root=tmp_path)
        assert _artifact(ev, "ep1").read_bytes() == tampered, "the writer overwrote it"


# --------------------------------------------------------------------------- new append


class TestNewAppendOverABrokenChainPublishesNothing:
    def test_nothing_is_published(self, two_episodes, tmp_path):
        _artifact(two_episodes, "ep1").write_bytes(b'{"tampered": true}')
        before = _index_bytes(two_episodes)
        with pytest.raises(ManifestError):
            write_run_manifest(two_episodes,
                               _ep("ep3", 3, prev="ep2", prior=("ep1", "ep2")), root=tmp_path)
        assert not (two_episodes / MANIFESTS_SUBDIR / "ep3").exists()
        assert _index_bytes(two_episodes) == before
        assert read_index(two_episodes)["latest_episode_id"] == "ep2"


# --------------------------------------------------------------------------- recovery


class TestRecoveryUsesTheSameValidation:
    def test_index_repair_validates_the_whole_chain(self, two_episodes, tmp_path):
        (two_episodes / MANIFEST_INDEX_FILENAME).unlink()
        _artifact(two_episodes, "ep1").write_bytes(b'{"tampered": true}')
        with pytest.raises(ManifestError):
            rebuild_manifest_mirror_and_index_from_canonical_episodes(
                two_episodes, root=tmp_path, job_id="j")
        assert not (two_episodes / MANIFEST_INDEX_FILENAME).exists()   # nothing was derived

    def test_a_clean_index_repair_succeeds_and_is_readable(self, two_episodes, tmp_path):
        (two_episodes / MANIFEST_INDEX_FILENAME).unlink()
        latest = rebuild_manifest_mirror_and_index_from_canonical_episodes(
            two_episodes, root=tmp_path, job_id="j")
        assert latest == "ep2"
        assert validate_index_and_tree(two_episodes, job_id="j") == []


# --------------------------------------------------------------------------- F4 the type


class TestProjectionsComeOnlyFromAVerifiedChain:
    def test_the_projection_writer_refuses_an_unverified_set(self, two_episodes, tmp_path):
        """A loose dict of episode dataclasses proves nothing about how it was obtained."""
        with pytest.raises(ManifestError) as exc:
            _mirror_and_index(two_episodes, {"ep1": _ep("ep1", 1)}, root=tmp_path)
        assert "VerifiedCanonicalChain" in str(exc.value)

    def test_the_verified_chain_is_produced_by_the_shared_loader(self, two_episodes):
        chain = load_verified_canonical_chain_for_write(two_episodes, job_id="j")
        assert isinstance(chain, VerifiedCanonicalChain)
        assert chain.ordinals == [1, 2]
        assert chain.latest.episode_id == "ep2"

    def test_the_shared_loader_refuses_a_broken_chain(self, two_episodes):
        _artifact(two_episodes, "ep1").write_bytes(b'{"tampered": true}')
        with pytest.raises(ManifestError):
            load_verified_canonical_chain_for_write(two_episodes, job_id="j")

    def test_the_shared_loader_refuses_a_foreign_episode(self, two_episodes):
        with pytest.raises(ManifestError):
            load_verified_canonical_chain_for_write(two_episodes, job_id="another-job")

    def test_no_chain_yet_is_not_an_error(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        assert load_verified_canonical_chain_for_write(ev, job_id="j") is None


# --------------------------------------------------------------------------- F4 postcondition


class TestPostPublicationRevalidation:
    def test_a_successful_write_is_immediately_canonically_readable(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        assert validate_index_and_tree(ev, job_id="j") == []
        latest = load_latest_manifest_verified(ev, job_id="j")
        assert (ev / MANIFEST_FILENAME).read_bytes() == latest.canonical_bytes()

    def test_the_index_describes_exactly_the_verified_chain(self, two_episodes):
        index = read_index(two_episodes)
        assert [e["episode_id"] for e in index["episodes"]] == ["ep1", "ep2"]
        assert index["latest_episode_id"] == "ep2"
        chain = load_verified_canonical_chain_for_write(two_episodes, job_id="j")
        assert [m.episode_id for m in chain.ordered()] == ["ep1", "ep2"]

    def test_a_postcondition_failure_is_raised_not_swallowed(self, tmp_path, monkeypatch):
        """If the tree the writer just published is not readable, the write must FAIL — a
        writer that reports success over an unreadable tree is the whole bug class."""
        import packages.orchestration.run_manifest as RM

        ev = tmp_path / "ev"
        ev.mkdir()
        monkeypatch.setattr(RM, "validate_index_and_tree",
                            lambda *a, **k: ["injected postcondition failure"])
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        assert "writer postcondition failed" in str(exc.value)
