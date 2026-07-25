"""F3/F4 (round 10) — episode publication is conflict-safe.

Two writers can reach the same episode at the same time (a retried stop finalization racing the
runner, say). Before round 10 that ended badly in two ways:

* `_write_call_artifacts` ignored the Boolean from its create-only write, so a writer that LOST
  an artifact race carried on and reported success over somebody else's bytes;
* artifacts were written directly into the canonical episode directory BEFORE the episode
  manifest claimed it — so a writer that then lost the manifest race left its own artifact
  sitting inside the winner's episode.

The publication model is now: build the COMPLETE episode under a private staging name outside
the canonical namespace, verify it there, and publish with ONE atomic rename. A loser never had
a name inside the winner's episode to leave anything at.
"""
from __future__ import annotations

import dataclasses
import hashlib
import os

import pytest

import packages.common.secure_fs as _fs
import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    MANIFEST_FILENAME,
    MANIFEST_INDEX_FILENAME,
    MANIFESTS_SUBDIR,
    STAGING_SUBDIR,
    ManifestConflictError,
    ManifestError,
    canonical_artifact_ref,
    load_latest_manifest_verified,
    validate_index_and_tree,
    write_run_manifest,
)


def _ep(episode_id, ordinal, *, calls=None, variant=""):
    # Round 13 (F5): a per-EPISODE run id — production re-runs a task under a NEW run when
    # a job resumes, so two episodes never share a run while each ledger lists only its own
    # call. (One run that legitimately spans episodes carries the earlier entries forward;
    # `validate_ledger_chain` holds it to that.)
    # Round 15 (F1): each work-doing episode is F011's stop-then-resume — the stopped
    # episode's task waits at `pending` and the resume starts a NEW run. A chain of
    # COMPLETED episodes each executing the same task cannot occur: a completed job is
    # done, and the resume loop `continue`s past an applied task.
    m = T._mk(episode_id=episode_id, job_input_variant=variant, status="stopped",
              calls=calls if calls is not None else (T._call(run=f"r-{episode_id}"),))
    m = dataclasses.replace(m, stop_request_id=f"stop-{episode_id}")
    bound = []
    for c in m.calls:
        c = dataclasses.replace(c, artifact=canonical_artifact_ref(c.identity))
        bound.append(dataclasses.replace(
            c, artifact_sha256=hashlib.sha256(c.canonical_artifact_bytes()).hexdigest()))
    return dataclasses.replace(m, calls=tuple(bound), episode_ordinal=ordinal,
                               created_at=f"2026-07-15T00:0{ordinal}:00+00:00")


@pytest.fixture
def ev(tmp_path):
    d = tmp_path / "ev"
    d.mkdir()
    return d


def _calls_dir(ev, episode_id="ep1"):
    return ev / MANIFESTS_SUBDIR / episode_id / "calls"


def _staging_leftovers(ev):
    stage = ev / STAGING_SUBDIR
    return sorted(p.name for p in stage.iterdir()) if stage.exists() else []


# --------------------------------------------------------------------------- F3 artifact race


class TestLostArtifactCreateRaceIsVerified:
    """The create-only write returns False instead of clobbering. That Boolean is the only thing
    between us and reporting success over another writer's bytes.

    F2 (round 12): the race now lives ONLY on the private staging path. There is no
    existing-episode "settlement" any more — a published episode's artifacts are immutable, so a
    retry verifies them and never writes.
    """

    def _stage_race(self, ev, tmp_path, m, race_bytes):
        """Lose the create race for the staged artifact: another writer's bytes land at our
        private staging name first."""
        real = _fs.write_file_atomically
        fired = {"n": 0}

        def _lose(dir_fd, name, data, **kw):
            if kw.get("create_only") and name.endswith(".json") and "builder" in name \
                    and not fired["n"]:
                fired["n"] = 1
                real(dir_fd, name, race_bytes(data), **{**kw, "create_only": False})
                return False
            return real(dir_fd, name, data, **kw)

        _fs.write_file_atomically = _lose
        try:
            write_run_manifest(ev, m, root=tmp_path)
        finally:
            _fs.write_file_atomically = real

    def test_a_lost_staging_artifact_race_is_never_ignored(self, ev, tmp_path):
        """Our own staging name can only collide if the record declares the same artifact twice —
        and the Boolean is checked either way, so it can never pass silently."""
        with pytest.raises(ManifestError) as exc:
            self._stage_race(ev, tmp_path, _ep("ep1", 1), lambda data: data)
        assert "declared more than once" in str(exc.value)
        assert not (ev / MANIFESTS_SUBDIR).exists() or \
            not list((ev / MANIFESTS_SUBDIR).iterdir())

    def test_a_failed_staging_race_publishes_nothing(self, ev, tmp_path):
        with pytest.raises(ManifestError):
            self._stage_race(ev, tmp_path, _ep("ep1", 1), lambda data: b'{"someone": "else"}')
        assert not (ev / MANIFEST_INDEX_FILENAME).exists()
        assert _staging_leftovers(ev) == []

    def test_an_existing_tampered_artifact_blocks_a_retry_and_is_not_overwritten(
            self, ev, tmp_path):
        """F2 (round 12): an immutable artifact whose bytes changed is corruption — the retry
        reports it and leaves it exactly as found."""
        m = _ep("ep1", 1)
        write_run_manifest(ev, m, root=tmp_path)
        art = sorted(_calls_dir(ev).glob("*.json"))[0]
        tampered = b'{"tampered": true}'
        art.write_bytes(tampered)
        with pytest.raises(ManifestError):
            write_run_manifest(ev, m, root=tmp_path)
        assert art.read_bytes() == tampered

    def test_an_exact_published_artifact_converges_idempotently(self, ev, tmp_path):
        m = _ep("ep1", 1)
        write_run_manifest(ev, m, root=tmp_path)
        before = sorted(_calls_dir(ev).glob("*.json"))[0].read_bytes()
        write_run_manifest(ev, m, root=tmp_path)          # exact same content
        assert sorted(_calls_dir(ev).glob("*.json"))[0].read_bytes() == before
        assert validate_index_and_tree(ev, job_id="j") == []


# --------------------------------------------------------------------------- F4 episode race


class _RenameRacer:
    """Let another writer win the atomic publication rename, exactly once.

    F1 (round 11): the winner's episode is placed with plain file ops rather than by re-entering
    `write_run_manifest` — this process already holds the job's append claim, so a nested writer
    would (correctly) block on it. `complete=False` models the nastier case: a winner that has
    our exact manifest and no `calls/` at all.
    """

    def __init__(self, ev, winner, *, complete=True):
        self.ev, self.winner, self.complete = ev, winner, complete
        self.real = os.rename
        self.fired = False

    def _place(self):
        wp = self.ev / MANIFESTS_SUBDIR / self.winner.episode_id
        wp.mkdir(parents=True, exist_ok=True)
        if self.complete:
            (wp / "calls").mkdir(exist_ok=True)
            for c in self.winner.calls:
                (wp / c.artifact).write_bytes(c.canonical_artifact_bytes())
            # F1 (round 12): a COMPLETE episode includes its canonical ledgers.
            if self.winner.call_ledgers:
                (wp / "call_ledgers").mkdir(exist_ok=True)
                for lg in self.winner.call_ledgers:
                    (wp / lg.ref()).write_bytes(lg.canonical_bytes())
        (wp / MANIFEST_FILENAME).write_bytes(self.winner.canonical_bytes())

    def __enter__(self):
        def _race(src, dst, *, src_dir_fd=None, dst_dir_fd=None):
            if not self.fired and dst == self.winner.episode_id:
                self.fired = True
                self._place()
                raise FileExistsError(17, "File exists")
            return self.real(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)
        os.rename = _race
        return self

    def __exit__(self, *exc):
        os.rename = self.real
        return False


class TestConflictingEpisodeWritersDoNotContaminate:
    def test_the_loser_leaves_no_artifact_in_the_winners_episode(self, ev, tmp_path):
        """THE finding: writer A's call artifact stayed inside writer B's episode directory."""
        winner = _ep("ep1", 1, calls=(T._call(),))
        loser = _ep("ep1", 1, calls=(T._call(role="reviewer", seq=1, rnd=2, fp="x"),))
        with _RenameRacer(ev, winner) as racer:
            with pytest.raises(ManifestConflictError):
                write_run_manifest(ev, loser, root=tmp_path)
            assert racer.fired
        names = sorted(p.name for p in _calls_dir(ev).glob("*"))
        assert names == ["0001-builder-round01-attempt.json"], names
        assert not any("reviewer" in n for n in names), "the loser contaminated the winner"

    def test_the_winners_tree_is_canonically_readable_after_the_race(self, ev, tmp_path):
        winner = _ep("ep1", 1, calls=(T._call(),))
        loser = _ep("ep1", 1, calls=(T._call(role="reviewer", seq=1, rnd=2, fp="x"),))
        with _RenameRacer(ev, winner):
            with pytest.raises(ManifestConflictError):
                write_run_manifest(ev, loser, root=tmp_path)
        # The winner's episode is intact; completing ITS publication (projections included)
        # yields a canonically readable tree with only the winner's calls in it.
        write_run_manifest(ev, winner, root=tmp_path)
        assert validate_index_and_tree(ev, job_id="j") == []
        latest = load_latest_manifest_verified(ev, job_id="j")
        assert latest.episode_id == "ep1"
        assert [c.identity.role for c in latest.calls] == ["builder"]

    def test_identical_concurrent_writers_converge(self, ev, tmp_path):
        """Same content on both sides: the loser accepts the winner's record and both callers
        see one canonical tree."""
        m = _ep("ep1", 1)
        with _RenameRacer(ev, m) as racer:
            write_run_manifest(ev, m, root=tmp_path)      # no raise: identical content
            assert racer.fired
        assert validate_index_and_tree(ev, job_id="j") == []
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep1"

    def test_a_failed_race_leaves_no_staging_leftovers(self, ev, tmp_path):
        winner = _ep("ep1", 1, calls=(T._call(),))
        loser = _ep("ep1", 1, calls=(T._call(role="reviewer", seq=1, rnd=2, fp="x"),))
        with _RenameRacer(ev, winner):
            with pytest.raises(ManifestConflictError):
                write_run_manifest(ev, loser, root=tmp_path)
        assert _staging_leftovers(ev) == [], "the loser left its staging directory behind"

    def test_a_successful_publication_leaves_no_staging_leftovers(self, ev, tmp_path):
        write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        assert _staging_leftovers(ev) == []


# --------------------------------------------------------------------------- staging hygiene


class TestStagingIsOutsideTheCanonicalNamespace:
    def test_staging_never_appears_as_an_episode(self, ev, tmp_path):
        """A crash mid-publication must not leave something that reads as an episode. Staging
        lives outside `run_manifests/`, so the exact allowlist never sees it."""
        write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        # simulate a crashed publication: a complete staging tree left behind
        stage = ev / STAGING_SUBDIR / "ep2.999.deadbeef"
        (stage / "calls").mkdir(parents=True)
        (stage / MANIFEST_FILENAME).write_bytes(_ep("ep2", 2).canonical_bytes())

        assert sorted(p.name for p in (ev / MANIFESTS_SUBDIR).iterdir()) == ["ep1"]
        assert validate_index_and_tree(ev, job_id="j") == []
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep1"

    def test_a_crash_leftover_does_not_block_the_next_append(self, ev, tmp_path):
        write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        stage = ev / STAGING_SUBDIR / "ep2.999.deadbeef"
        (stage / "calls").mkdir(parents=True)
        (stage / MANIFEST_FILENAME).write_bytes(b"{}")
        m2 = dataclasses.replace(_ep("ep2", 2), previous_episode_id="ep1",
                                 prior_episode_ids=("ep1",))
        write_run_manifest(ev, m2, root=tmp_path)          # recovery is deterministic
        assert validate_index_and_tree(ev, job_id="j") == []
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep2"

    def test_a_staging_leftover_never_enters_the_export(self, ev, tmp_path):
        from packages.orchestration.run_manifest import build_verified_manifest_tree
        write_run_manifest(ev, _ep("ep1", 1), root=tmp_path)
        stage = ev / STAGING_SUBDIR / "ep9.999.deadbeef"
        (stage / "calls").mkdir(parents=True)
        (stage / "calls" / "smuggled.json").write_bytes(b'{"canary": true}')
        files, problems = build_verified_manifest_tree(ev, job_id="j")
        assert problems == []
        assert not any("staging" in k or "smuggled" in k for k in files), sorted(files)
