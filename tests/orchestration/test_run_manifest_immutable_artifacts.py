"""F2/F3 (round 12) — a published Episode's members are IMMUTABLE, and history is never recomputed.

Two reproductions drove this:

* publish an episode, delete its Call artifact, retry the episode → the retry SUCCEEDED, the
  artifact was recreated and the canonical loader went green again. Episodes are published
  atomically as complete directories, so a missing artifact afterwards is not a partial write —
  it is corruption, tamper or storage loss, and silently recreating it erases the only evidence
  that anything went wrong;

* `ep1`, then `ep2`, then an exact retry of `ep1` → `ManifestError: ep2 references unknown prior
  ep1; ordinals [2] are not contiguous`. The writer excluded the candidate episode before
  validating the chain, and excluding an OLDER episode breaks all the history built on it.

So: a private unpublished stage may be rebuilt or discarded; a published episode is verified and
never repaired; and an exact retry of any episode — latest or not — is a no-op.
"""
from __future__ import annotations

import dataclasses
import hashlib

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    LEDGERS_SUBDIR,
    MANIFEST_FILENAME,
    MANIFEST_INDEX_FILENAME,
    MANIFESTS_SUBDIR,
    ManifestConflictError,
    ManifestError,
    canonical_artifact_ref,
    load_latest_manifest_verified,
    read_index,
    validate_index_and_tree,
    write_run_manifest,
)


def _ep(episode_id, ordinal, *, prev="", prior=(), variant=""):
    # Round 13 (F5): a per-EPISODE run id — production re-runs a task under a NEW run when
    # a job resumes, so two episodes never share a run while each ledger lists only its own
    # call. (One run that legitimately spans episodes carries the earlier entries forward;
    # `validate_ledger_chain` holds it to that.)
    # Round 15 (F1): each work-doing episode is F011's stop-then-resume — the stopped
    # episode's task waits at `pending` and the resume starts a NEW run. A chain of
    # COMPLETED episodes each executing the same task cannot occur: a completed job is
    # done, and the resume loop `continue`s past an applied task.
    m = T._mk(episode_id=episode_id, job_input_variant=variant, status="stopped",
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
def ev(tmp_path):
    d = tmp_path / "ev"
    d.mkdir()
    write_run_manifest(d, _ep("ep1", 1), root=tmp_path)
    return d


def _artifact(ev, eid="ep1"):
    return sorted((ev / MANIFESTS_SUBDIR / eid / "calls").glob("*.json"))[0]


def _ledger(ev, eid="ep1"):
    return sorted((ev / MANIFESTS_SUBDIR / eid / LEDGERS_SUBDIR).glob("*.json"))[0]


# --------------------------------------------------------------------------- F2


class TestPublishedMembersAreNeverRepaired:
    def test_a_missing_call_artifact_blocks_the_retry(self, ev, tmp_path):
        """THE finding: the retry recreated it and the loader went green."""
        art = _artifact(ev)
        art.unlink()
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        assert "missing call artifact" in str(exc.value)
        assert not art.exists(), "the writer recreated an immutable published artifact"

    def test_a_missing_ledger_artifact_blocks_the_retry(self, ev, tmp_path):
        led = _ledger(ev)
        led.unlink()
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        assert "ledger" in str(exc.value)
        assert not led.exists()

    def test_a_tampered_call_artifact_blocks_and_is_left_as_found(self, ev, tmp_path):
        art = _artifact(ev)
        tampered = b'{"tampered": true}'
        art.write_bytes(tampered)
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        assert art.read_bytes() == tampered, "the writer overwrote the evidence of a tamper"

    def test_a_tampered_ledger_blocks_and_is_left_as_found(self, ev, tmp_path):
        led = _ledger(ev)
        tampered = b'{"ledger_v": 1}'
        led.write_bytes(tampered)
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        assert led.read_bytes() == tampered

    def test_a_missing_PRIOR_episode_artifact_blocks(self, ev, tmp_path):
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        _artifact(ev, "ep1").unlink()
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep3", 3, prev="ep2", prior=("ep1", "ep2")),
                               root=tmp_path)
        assert not (ev / MANIFESTS_SUBDIR / "ep3").exists()

    def test_exact_existing_bytes_converge(self, ev, tmp_path):
        before = _artifact(ev).read_bytes()
        write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)      # exact same content
        assert _artifact(ev).read_bytes() == before
        assert validate_index_and_tree(ev, job_id="j") == []

    def test_a_failed_retry_writes_nothing_into_the_episode(self, ev, tmp_path):
        art = _artifact(ev)
        art.unlink()
        before = sorted(p.name for p in (ev / MANIFESTS_SUBDIR / "ep1").rglob("*"))
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        after = sorted(p.name for p in (ev / MANIFESTS_SUBDIR / "ep1").rglob("*"))
        assert before == after, "a failed retry wrote into a published episode"

    def test_a_conflicting_retry_never_overwrites(self, ev, tmp_path):
        before = (ev / MANIFESTS_SUBDIR / "ep1" / MANIFEST_FILENAME).read_bytes()
        with pytest.raises(ManifestConflictError):
            write_run_manifest(ev, _ep("ep1", 1, variant="-different"), root=tmp_path)
        assert (ev / MANIFESTS_SUBDIR / "ep1" / MANIFEST_FILENAME).read_bytes() == before


# --------------------------------------------------------------------------- F3


class TestNonLatestEpisodeRetryIsANoOp:
    def test_the_reproduced_case(self, ev, tmp_path):
        """ep1, ep2, then an exact retry of ep1 — which used to report that ep2 referenced an
        unknown prior, because the writer had excluded ep1 from ep1's own chain."""
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)       # no-op
        assert validate_index_and_tree(ev, job_id="j") == []
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep2"

    def test_a_retry_of_the_oldest_of_three_episodes(self, ev, tmp_path):
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        write_run_manifest(ev, _ep("ep3", 3, prev="ep2", prior=("ep1", "ep2")), root=tmp_path)
        write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        assert validate_index_and_tree(ev, job_id="j") == []
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep3"

    def test_an_old_episode_retry_never_changes_latest(self, ev, tmp_path):
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        before = (ev / MANIFEST_INDEX_FILENAME).read_bytes()
        write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        assert (ev / MANIFEST_INDEX_FILENAME).read_bytes() == before
        assert read_index(ev)["latest_episode_id"] == "ep2"

    def test_an_old_episode_retry_does_not_recompute_its_ordinal(self, ev, tmp_path):
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        idx = read_index(ev)
        assert [(e["episode_id"], e["episode_ordinal"]) for e in idx["episodes"]] == \
            [("ep1", 1), ("ep2", 2)]

    def test_a_conflicting_old_episode_retry_blocks(self, ev, tmp_path):
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        with pytest.raises(ManifestConflictError):
            write_run_manifest(ev, _ep("ep1", 1, variant="-different"), root=tmp_path)
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep2"

    def test_a_retry_over_a_damaged_prior_chain_blocks(self, ev, tmp_path):
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        _artifact(ev, "ep2").write_bytes(b'{"tampered": true}')
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)

    def test_a_retry_repairs_only_the_derived_projections(self, ev, tmp_path):
        """A crash between the episode and its projections is the ONE thing a retry rebuilds —
        derived state, never an immutable member."""
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        ep2_bytes = (ev / MANIFESTS_SUBDIR / "ep2" / MANIFEST_FILENAME).read_bytes()
        (ev / MANIFEST_INDEX_FILENAME).unlink()
        write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)        # the old-episode retry
        assert (ev / MANIFEST_INDEX_FILENAME).exists(), "the projection was not recovered"
        assert (ev / MANIFESTS_SUBDIR / "ep2" / MANIFEST_FILENAME).read_bytes() == ep2_bytes
        assert validate_index_and_tree(ev, job_id="j") == []
