"""F1/F2 (round 10) — an append validates the COMPLETE existing canonical chain first.

Writer success is a claim about the whole tree, not about one file. Before round 10 the writer
read individual episode records but never validated the SET, so it would happily report success
and leave behind a chain its own canonical loader rejects on the very next read — duplicate
ordinals, a skipped predecessor, or a prior episode whose call artifact had been tampered with
since it was published.

The append preflight is therefore: load every existing immutable episode, strict-decode it,
require canonical bytes, verify EVERY declared artifact of EVERY episode, enforce the exact
episode-root allowlist, check job ownership, unique ids/ordinals, contiguity 1..N and the exact
linear history — and only then check that the candidate extends that chain exactly. Nothing is
published until all of it holds.
"""
from __future__ import annotations

import dataclasses
import hashlib

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    MANIFEST_FILENAME,
    MANIFEST_INDEX_FILENAME,
    MANIFESTS_SUBDIR,
    ManifestError,
    canonical_artifact_ref,
    load_latest_manifest_verified,
    read_index,
    validate_index_and_tree,
    write_run_manifest,
)


def _ep(episode_id, ordinal, *, prev="", prior=(), calls=None, variant=""):
    # Round 13 (F5): a per-EPISODE run id — production re-runs a task under a NEW run when
    # a job resumes, so two episodes never share a run while each ledger lists only its own
    # call. (One run that legitimately spans episodes carries the earlier entries forward;
    # `validate_ledger_chain` holds it to that.)
    m = T._mk(episode_id=episode_id, job_input_variant=variant,
              calls=calls if calls is not None else (T._call(run=f"r-{episode_id}"),))
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


def _artifact(ev, episode_id="ep1"):
    return sorted((ev / MANIFESTS_SUBDIR / episode_id / "calls").glob("*.json"))[0]


def _assert_nothing_was_published(ev, latest="ep1"):
    """The failed append must leave the PREVIOUS canonical state exactly as it was."""
    assert not (ev / MANIFESTS_SUBDIR / "ep2").exists(), "a rejected episode was created"
    assert read_index(ev)["latest_episode_id"] == latest, "the index advanced on a failure"
    assert (ev / MANIFEST_FILENAME).read_bytes() == \
        (ev / MANIFESTS_SUBDIR / latest / MANIFEST_FILENAME).read_bytes()


# --------------------------------------------------------------------------- F1 chain shape


class TestCandidateMustExtendTheChainExactly:
    def test_a_valid_append_succeeds(self, ev, tmp_path):
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        assert validate_index_and_tree(ev, job_id="j") == []
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep2"

    def test_duplicate_ordinal_blocks_before_publication(self, ev, tmp_path):
        """THE finding: the second write reported success, and the resulting tree was rejected
        for duplicate ordinals the moment anyone read it."""
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, _ep("ep2", 1), root=tmp_path)
        assert "ordinal" in str(exc.value)
        _assert_nothing_was_published(ev)
        assert validate_index_and_tree(ev, job_id="j") == []

    def test_noncontiguous_ordinal_blocks(self, ev, tmp_path):
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, _ep("ep2", 3, prev="ep1", prior=("ep1",)), root=tmp_path)
        assert "ordinal" in str(exc.value)
        _assert_nothing_was_published(ev)

    def test_skipped_immediate_predecessor_blocks(self, ev, tmp_path):
        """Ordinal is right, but it names the wrong predecessor."""
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, _ep("ep2", 2, prev="", prior=("ep1",)), root=tmp_path)
        assert "previous" in str(exc.value)
        _assert_nothing_was_published(ev)

    def test_unknown_prior_episode_blocks(self, ev, tmp_path):
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep-ghost", "ep1")),
                               root=tmp_path)
        assert "priors" in str(exc.value)
        _assert_nothing_was_published(ev)

    def test_missing_prior_history_blocks(self, ev, tmp_path):
        """An episode that drops its history is refused (the record's own coherence rule fires
        first here — either way, nothing is published)."""
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=()), root=tmp_path)
        assert "prior" in str(exc.value)
        _assert_nothing_was_published(ev)

    def test_history_missing_an_earlier_episode_blocks(self, ev, tmp_path):
        """A third episode whose priors skip ep1: coherent on its own, wrong against the chain."""
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, _ep("ep3", 3, prev="ep2", prior=("ep2",)), root=tmp_path)
        assert "prior" in str(exc.value)
        assert not (ev / MANIFESTS_SUBDIR / "ep3").exists()

    def test_a_foreign_job_episode_in_the_tree_blocks(self, ev, tmp_path):
        """Ownership is part of the preflight: an episode of another job sitting in this tree
        means the tree is not what it claims to be."""
        foreign = dataclasses.replace(_ep("ep2", 2, prev="ep1", prior=("ep1",)),
                                      job_id="someone-else")
        ep = ev / MANIFESTS_SUBDIR / "ep2"
        (ep / "calls").mkdir(parents=True)
        (ep / MANIFEST_FILENAME).write_bytes(foreign.canonical_bytes())
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, _ep("ep3", 3, prev="ep2", prior=("ep1", "ep2")),
                               root=tmp_path)
        assert "job_id" in str(exc.value) or "expected" in str(exc.value)


# --------------------------------------------------------------------------- F2 old artifacts


class TestAppendValidatesEveryPreviousArtifact:
    def _append(self, ev, tmp_path):
        return write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)

    def test_tampered_prior_artifact_blocks(self, ev, tmp_path):
        """THE finding: appending over a tampered old artifact reported success, and the
        resulting chain failed artifact validation immediately."""
        _artifact(ev).write_bytes(b'{"tampered": true}')
        with pytest.raises(ManifestError) as exc:
            self._append(ev, tmp_path)
        assert "artifact" in str(exc.value)
        assert not (ev / MANIFESTS_SUBDIR / "ep2").exists()

    def test_sha_mismatched_prior_artifact_blocks(self, ev, tmp_path):
        """Canonically-shaped bytes that simply are not the recorded ones."""
        other = T._call(fp="a-different-prompt")
        _artifact(ev).write_bytes(other.canonical_artifact_bytes())
        with pytest.raises(ManifestError) as exc:
            self._append(ev, tmp_path)
        assert "artifact" in str(exc.value)

    def test_noncanonical_prior_artifact_blocks(self, ev, tmp_path):
        """Same content, re-serialized by a well-meaning tool: the bytes are no longer the ones
        the hash covers."""
        import json
        a = _artifact(ev)
        a.write_bytes(json.dumps(json.loads(a.read_text()), indent=4).encode())
        with pytest.raises(ManifestError):
            self._append(ev, tmp_path)

    def test_missing_prior_artifact_blocks(self, ev, tmp_path):
        _artifact(ev).unlink()
        with pytest.raises(ManifestError) as exc:
            self._append(ev, tmp_path)
        assert "artifact" in str(exc.value)
        assert not (ev / MANIFESTS_SUBDIR / "ep2").exists()

    def test_extra_undeclared_prior_artifact_blocks(self, ev, tmp_path):
        (_artifact(ev).parent / "0002-smuggled.json").write_bytes(b"{}")
        with pytest.raises(ManifestError):
            self._append(ev, tmp_path)

    def test_symlinked_prior_calls_dir_blocks(self, ev, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        calls = _artifact(ev).parent
        for f in calls.iterdir():
            f.unlink()
        calls.rmdir()
        calls.symlink_to(outside)
        with pytest.raises(ManifestError):
            self._append(ev, tmp_path)
        assert not (ev / MANIFESTS_SUBDIR / "ep2").exists()

    def test_a_clean_chain_appends_and_stays_clean(self, ev, tmp_path):
        self._append(ev, tmp_path)
        assert validate_index_and_tree(ev, job_id="j") == []
        # and the SECOND append re-validates both prior episodes
        write_run_manifest(ev, _ep("ep3", 3, prev="ep2", prior=("ep1", "ep2")), root=tmp_path)
        assert validate_index_and_tree(ev, job_id="j") == []
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep3"

    def test_a_tampered_artifact_two_episodes_back_still_blocks(self, ev, tmp_path):
        """Every prior episode is preflighted — not just the immediate predecessor."""
        self._append(ev, tmp_path)
        _artifact(ev, "ep1").write_bytes(b'{"tampered": true}')
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep3", 3, prev="ep2", prior=("ep1", "ep2")),
                               root=tmp_path)
        assert not (ev / MANIFESTS_SUBDIR / "ep3").exists()


# --------------------------------------------------------------------------- diagnosis


class TestABrokenTreeIsNotExtendedButStaysReadable:
    def test_the_broken_tree_remains_for_diagnosis(self, ev, tmp_path):
        """A refused append must not 'repair' or delete anything: the operator still needs to
        see exactly what broke."""
        a = _artifact(ev)
        a.write_bytes(b'{"tampered": true}')
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        assert a.read_bytes() == b'{"tampered": true}'      # untouched, diagnosable
        assert (ev / MANIFEST_INDEX_FILENAME).exists()
        problems = validate_index_and_tree(ev, job_id="j")
        assert any("artifact" in p for p in problems), problems
