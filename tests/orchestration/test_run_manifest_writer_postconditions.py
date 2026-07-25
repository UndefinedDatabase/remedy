"""F13 (round 9) — a SUCCESSFUL write or recovery implies IMMEDIATE canonical readability.

Writer success is a promise, not a hope: whenever `write_run_manifest` or a recovery rebuild
returns without raising, the tree it leaves behind must satisfy every canonical-read invariant
right then. The class of bug this closes is "the writer reported idempotent success while the
canonical loader rejected what was on disk".

One shared invariant matrix runs after EVERY writer and recovery path, so a future path cannot
be added with weaker postconditions than the rest.
"""
from __future__ import annotations

import contextlib
import dataclasses
import os

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    COVERAGE_COMPLETE,
    MANIFEST_FILENAME,
    MANIFEST_INDEX_FILENAME,
    MANIFESTS_SUBDIR,
    MODE_PUBLISHED_REFERENCE,
    STAGING_SUBDIR,
    ManifestConflictError,
    ManifestError,
    build_verified_manifest_tree,
    canonical_index_bytes,
    decode_index_v1,
    load_index_verified,
    load_latest_manifest_verified,
    rebuild_manifest_mirror_and_index_from_canonical_episodes,
    validate_index_and_tree,
    validate_run_manifest,
    write_run_manifest,
)


@contextlib.contextmanager
def _publish_winner_at_rename(ev, winner):
    """Another writer wins the episode-directory race: its COMPLETE episode appears at the
    destination name the moment our rename runs. Placed with plain file ops — re-entering the
    writer would block on the per-job append claim this process already holds (F1)."""
    import os as _os

    real = _os.rename

    def _race(src, dst, *, src_dir_fd=None, dst_dir_fd=None):
        if dst == winner.episode_id:
            wp = ev / MANIFESTS_SUBDIR / winner.episode_id
            (wp / "calls").mkdir(parents=True, exist_ok=True)
            for c in winner.calls:
                (wp / c.artifact).write_bytes(c.canonical_artifact_bytes())
            if winner.call_ledgers:                     # F1 (round 12): a COMPLETE episode
                (wp / "call_ledgers").mkdir(exist_ok=True)
                for lg in winner.call_ledgers:
                    (wp / lg.ref()).write_bytes(lg.canonical_bytes())
            (wp / MANIFEST_FILENAME).write_bytes(winner.canonical_bytes())
            raise FileExistsError(17, "File exists")
        return real(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)

    _os.rename = _race
    try:
        yield
    finally:
        _os.rename = real


@contextlib.contextmanager
def _publish_incomplete_winner_at_rename(ev, winner):
    """Another writer wins the destination with our exact manifest and NO calls/ — the F3
    (round 11) hazard: same manifest, incomplete tree."""
    import os as _os

    real = _os.rename

    def _race(src, dst, *, src_dir_fd=None, dst_dir_fd=None):
        if dst == winner.episode_id:
            wp = ev / MANIFESTS_SUBDIR / winner.episode_id
            wp.mkdir(parents=True, exist_ok=True)
            (wp / MANIFEST_FILENAME).write_bytes(winner.canonical_bytes())
            raise FileExistsError(17, "File exists")
        return real(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)

    _os.rename = _race
    try:
        yield
    finally:
        _os.rename = real


# --------------------------------------------------------------------------- the matrix


def assert_canonically_readable(ev, *, job_id="j", expect_latest=None):
    """THE shared postcondition. Every writer/recovery success must satisfy all of it."""
    # 1. the canonical latest loader succeeds
    latest = load_latest_manifest_verified(ev, job_id=job_id)
    if expect_latest is not None:
        assert latest.episode_id == expect_latest, "latest episode is not the published one"

    # 2. the verified tree has ZERO problems (chain, hashes, allowlist, anchored reads)
    assert validate_index_and_tree(ev, job_id=job_id) == []
    files, problems = build_verified_manifest_tree(ev, job_id=job_id)
    assert problems == [], problems

    # 3. the root mirror is byte-for-byte the latest episode record
    ep_rel = f"{MANIFESTS_SUBDIR}/{latest.episode_id}/{MANIFEST_FILENAME}"
    assert files[MANIFEST_FILENAME] == files[ep_rel]
    assert files[MANIFEST_FILENAME] == latest.canonical_bytes()

    # 4. the stored index bytes are the canonical encoding of the index they decode to
    raw = files[MANIFEST_INDEX_FILENAME]
    assert raw == canonical_index_bytes(decode_index_v1(raw))
    index, root_fd = load_index_verified(ev)          # the anchored reader agrees
    os.close(root_fd)
    assert index["latest_episode_id"] == latest.episode_id

    # 5. every call artifact is present, canonically named and hash-bound
    for c in latest.calls:
        assert files[f"{MANIFESTS_SUBDIR}/{latest.episode_id}/{c.artifact}"] \
            == c.canonical_artifact_bytes()

    # 6. a published terminal reference has COMPLETE coverage and passes reference validation
    if latest.status in ("completed", "stopped"):
        assert latest.coverage.status == COVERAGE_COMPLETE
        # F6 (round 10): zero calls is only ever complete when the record PROVES zero expected.
        if not latest.calls:
            assert latest.call_expectation.expects_zero_calls()
    assert validate_run_manifest(latest, mode=MODE_PUBLISHED_REFERENCE) == []

    # 7. F4 (round 10): NO undeclared file exists anywhere in the canonical namespace, and no
    # staging leftover survived a successful publication.
    declared = set(files)
    for path in sorted((ev / MANIFESTS_SUBDIR).rglob("*")):
        if path.is_dir():
            continue
        rel = str(path.relative_to(ev))
        assert rel in declared, f"undeclared file in the canonical namespace: {rel}"
    stage = ev / STAGING_SUBDIR
    assert not stage.exists() or list(stage.iterdir()) == [], "staging leftovers survived"
    return latest


def assert_failure_changed_nothing(ev, before_latest, before_index_bytes):
    """The postcondition of a FAILED operation: no new canonical episode, no advanced
    projection, no contamination, and the pending F011 stop stays retryable."""
    latest = load_latest_manifest_verified(ev, job_id="j")
    assert latest.episode_id == before_latest, "a failed write advanced the latest episode"
    assert (ev / MANIFEST_INDEX_FILENAME).read_bytes() == before_index_bytes
    assert validate_index_and_tree(ev, job_id="j") == []
    stage = ev / STAGING_SUBDIR
    assert not stage.exists() or list(stage.iterdir()) == [], "a failed write left staging behind"


def _ep(episode_id, ordinal, *, prev="", prior=(), status="completed", calls=None,
        job_input_variant=""):
    m = T._mk(episode_id=episode_id, status=status, job_input_variant=job_input_variant,
              calls=calls if calls is not None else ())
    return dataclasses.replace(m, episode_ordinal=ordinal, previous_episode_id=prev,
                               prior_episode_ids=tuple(prior),
                               created_at=f"2026-07-15T00:0{ordinal}:00+00:00")


def _with_calls(episode_id, ordinal, **kw):
    """Round 15 (F1): an episode that DOES WORK is F011's stop-then-resume — the task waits at
    `pending` under a per-episode run, and the resume starts a new one. Two COMPLETED episodes
    executing the same task is a shape production cannot produce."""
    import hashlib

    from packages.orchestration.run_manifest import canonical_artifact_ref

    kw.setdefault("status", "stopped")
    m = _ep(episode_id, ordinal, calls=(T._call(run=f"r-{episode_id}"),), **kw)
    if m.status == "stopped":
        m = dataclasses.replace(m, stop_request_id=f"stop-{episode_id}")
    bound = []
    for c in m.calls:
        c = dataclasses.replace(c, artifact=canonical_artifact_ref(c.identity))
        bound.append(dataclasses.replace(
            c, artifact_sha256=hashlib.sha256(c.canonical_artifact_bytes()).hexdigest()))
    return dataclasses.replace(m, calls=tuple(bound))


@pytest.fixture
def ev(tmp_path):
    d = tmp_path / "ev"
    d.mkdir()
    return d


# --------------------------------------------------------------------------- writer paths


class TestWriterPostconditions:
    def test_first_write(self, ev, tmp_path):
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        assert_canonically_readable(ev, expect_latest="ep1")

    def test_idempotent_retry(self, ev, tmp_path):
        m = _with_calls("ep1", 1)
        write_run_manifest(ev, m, root=tmp_path)
        before = (ev / MANIFESTS_SUBDIR / "ep1" / MANIFEST_FILENAME).read_bytes()
        write_run_manifest(ev, m, root=tmp_path)          # exact same content again
        after = (ev / MANIFESTS_SUBDIR / "ep1" / MANIFEST_FILENAME).read_bytes()
        assert before == after                            # immutable record untouched
        assert_canonically_readable(ev, expect_latest="ep1")

    def test_concurrent_create_convergence(self, ev, tmp_path, monkeypatch):
        """Two writers publish the SAME episode; one loses the publication race and takes the
        existing-record path. Both must converge on ONE canonical readable tree.

        F4 (round 10): the race is decided at the atomic directory RENAME — the only moment the
        canonical episode name comes into existence — so that is where the test injects it.
        """
        import os as _os

        m = _with_calls("ep1", 1)
        real_rename = _os.rename
        state = {"raced": False}

        def _lose_the_race(src, dst, *, src_dir_fd=None, dst_dir_fd=None):
            if not state["raced"] and dst == "ep1":
                state["raced"] = True
                # the OTHER writer publishes the identical episode first
                real_rename(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)
                raise FileExistsError(17, "File exists")
            return real_rename(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)

        monkeypatch.setattr(_os, "rename", _lose_the_race)
        write_run_manifest(ev, m, root=tmp_path)
        assert state["raced"]
        monkeypatch.undo()
        assert_canonically_readable(ev, expect_latest="ep1")

    def test_stop_retry(self, ev, tmp_path):
        """F011: a stop publication that is retried (e.g. after a crash between steps) must
        converge, never stick pending."""
        m = dataclasses.replace(_with_calls("ep1", 1, status="stopped"),
                                stop_request_id="stop-abc")
        write_run_manifest(ev, m, root=tmp_path)
        (ev / MANIFEST_INDEX_FILENAME).unlink()           # crash after the episode, before index
        write_run_manifest(ev, m, root=tmp_path)          # the retry
        latest = assert_canonically_readable(ev, expect_latest="ep1")
        assert latest.status == "stopped" and latest.stop_request_id == "stop-abc"

    def test_second_episode_append(self, ev, tmp_path):
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        latest = assert_canonically_readable(ev, expect_latest="ep2")
        assert latest.previous_episode_id == "ep1"


# --------------------------------------------------------------------------- recovery paths


class TestRecoveryPostconditions:
    def test_root_mirror_repair(self, ev, tmp_path):
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        (ev / MANIFEST_FILENAME).unlink()                 # derived mirror lost
        rebuild_manifest_mirror_and_index_from_canonical_episodes(ev, job_id="j", root=tmp_path)
        assert_canonically_readable(ev, expect_latest="ep1")

    def test_index_repair(self, ev, tmp_path):
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        (ev / MANIFEST_INDEX_FILENAME).unlink()           # derived index lost
        rebuild_manifest_mirror_and_index_from_canonical_episodes(ev, job_id="j", root=tmp_path)
        assert_canonically_readable(ev, expect_latest="ep2")


# --------------------------------------------------------------------------- the negative


class TestFailureLeavesNoFalseSuccess:
    def test_a_conflicting_republish_raises_and_the_tree_stays_readable(self, ev, tmp_path):
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        # a DIFFERENT job input under the same episode id — a genuine content conflict
        conflicting = _with_calls("ep1", 1, job_input_variant="-changed")
        with pytest.raises(ManifestConflictError):
            write_run_manifest(ev, conflicting, root=tmp_path)
        assert_canonically_readable(ev, expect_latest="ep1")     # unchanged and still canonical


# --------------------------------------------------------------------------- F10 (round 10)


def _index_bytes(ev):
    return (ev / MANIFEST_INDEX_FILENAME).read_bytes()


class TestAppendPostconditions:
    """Every APPEND path — the ones that succeed and the ones that must not."""

    def test_append_to_a_valid_chain(self, ev, tmp_path):
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        assert_canonically_readable(ev, expect_latest="ep2")

    def test_append_with_a_duplicate_ordinal_changes_nothing(self, ev, tmp_path):
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        before = _index_bytes(ev)
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep2", 1), root=tmp_path)
        assert_failure_changed_nothing(ev, "ep1", before)

    def test_append_with_a_skipped_predecessor_changes_nothing(self, ev, tmp_path):
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        before = _index_bytes(ev)
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep3", 3, prev="ep1", prior=("ep1",)), root=tmp_path)
        assert_failure_changed_nothing(ev, "ep1", before)

    def test_append_with_an_unknown_prior_changes_nothing(self, ev, tmp_path):
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        before = _index_bytes(ev)
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep-ghost", "ep1")),
                               root=tmp_path)
        assert_failure_changed_nothing(ev, "ep1", before)

    def test_append_over_a_tampered_prior_artifact_changes_nothing(self, ev, tmp_path):
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        before = _index_bytes(ev)
        art = sorted((ev / MANIFESTS_SUBDIR / "ep1" / "calls").glob("*.json"))[0]
        original = art.read_bytes()
        art.write_bytes(b'{"tampered": true}')
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        assert not (ev / MANIFESTS_SUBDIR / "ep2").exists()
        assert (ev / MANIFEST_INDEX_FILENAME).read_bytes() == before
        art.write_bytes(original)                      # undo the tamper...
        assert_canonically_readable(ev, expect_latest="ep1")   # ...and it reads clean again

    def test_append_over_a_missing_prior_artifact_changes_nothing(self, ev, tmp_path):
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        before = _index_bytes(ev)
        sorted((ev / MANIFESTS_SUBDIR / "ep1" / "calls").glob("*.json"))[0].unlink()
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        assert not (ev / MANIFESTS_SUBDIR / "ep2").exists()
        assert (ev / MANIFEST_INDEX_FILENAME).read_bytes() == before


class TestRacePostconditions:
    def test_an_identical_concurrent_writer_converges(self, ev, tmp_path, monkeypatch):
        import os as _os
        m = _with_calls("ep1", 1)
        real = _os.rename
        state = {"raced": False}

        def _race(src, dst, *, src_dir_fd=None, dst_dir_fd=None):
            if not state["raced"] and dst == "ep1":
                state["raced"] = True
                real(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)
                raise FileExistsError(17, "File exists")
            return real(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)

        monkeypatch.setattr(_os, "rename", _race)
        write_run_manifest(ev, m, root=tmp_path)
        monkeypatch.undo()
        assert state["raced"]
        assert_canonically_readable(ev, expect_latest="ep1")

    def test_a_conflicting_concurrent_writer_leaves_the_winner_intact(self, ev, tmp_path):
        """F1 (round 11): the winner is placed DIRECTLY, because a nested `write_run_manifest`
        would now block on this job's append claim — which is the point of the claim."""
        winner = _with_calls("ep1", 1)
        loser = _with_calls("ep1", 1, job_input_variant="-other")
        with _publish_winner_at_rename(ev, winner):
            with pytest.raises(ManifestConflictError):
                write_run_manifest(ev, loser, root=tmp_path)
        # the winner's tree was never touched; publish it properly and it reads clean
        write_run_manifest(ev, winner, root=tmp_path)
        latest = assert_canonically_readable(ev, expect_latest="ep1")
        assert latest.job_input_sha256 == winner.job_input_sha256

    def test_a_lost_artifact_race_on_the_staging_path_publishes_nothing(self, ev, tmp_path):
        """F2 (round 12): the artifact race lives only on the PRIVATE staging path now — a
        published episode's artifacts are immutable and are never rewritten."""
        import packages.common.secure_fs as _fs

        m = _with_calls("ep1", 1)
        real = _fs.write_file_atomically

        def _lose(dir_fd, name, data, **kw):
            if kw.get("create_only") and name.endswith(".json") and "builder" in name:
                real(dir_fd, name, b'{"someone": "else"}', **{**kw, "create_only": False})
                return False
            return real(dir_fd, name, data, **kw)

        _fs.write_file_atomically = _lose
        try:
            with pytest.raises(ManifestError):
                write_run_manifest(ev, m, root=tmp_path)
        finally:
            _fs.write_file_atomically = real
        assert not (ev / MANIFEST_INDEX_FILENAME).exists()
        stage = ev / STAGING_SUBDIR
        assert not stage.exists() or list(stage.iterdir()) == []

    def test_a_missing_published_artifact_is_never_repaired(self, ev, tmp_path):
        m = _with_calls("ep1", 1)
        write_run_manifest(ev, m, root=tmp_path)
        art = sorted((ev / MANIFESTS_SUBDIR / "ep1" / "calls").glob("*.json"))[0]
        art.unlink()
        with pytest.raises(ManifestError):
            write_run_manifest(ev, m, root=tmp_path)
        assert not art.exists()


class TestRecoveryAfterPartialStaging:
    def test_a_crashed_staging_tree_does_not_block_recovery(self, ev, tmp_path):
        """A crash mid-publication leaves a private staging tree. It is outside the canonical
        namespace, so the next write and the canonical loader both ignore it."""
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        stage = ev / STAGING_SUBDIR / "ep2.123.abcdef"
        (stage / "calls").mkdir(parents=True)
        (stage / MANIFEST_FILENAME).write_bytes(b'{"half": "written"}')
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        latest = load_latest_manifest_verified(ev, job_id="j")
        assert latest.episode_id == "ep2"
        assert validate_index_and_tree(ev, job_id="j") == []


class TestStopRetryAfterEachPublicationWindow:
    """F011: a stop publication must converge whichever window the crash fell in — the pending
    stop stays retryable, never stuck."""

    def _stopped(self):
        return dataclasses.replace(_with_calls("ep1", 1, status="stopped"),
                                   stop_request_id="stop-abc")

    def test_retry_after_the_episode_was_published(self, ev, tmp_path):
        m = self._stopped()
        write_run_manifest(ev, m, root=tmp_path)
        write_run_manifest(ev, m, root=tmp_path)          # the retry
        latest = assert_canonically_readable(ev, expect_latest="ep1")
        assert latest.status == "stopped" and latest.stop_request_id == "stop-abc"

    def test_retry_after_the_index_was_lost(self, ev, tmp_path):
        m = self._stopped()
        write_run_manifest(ev, m, root=tmp_path)
        (ev / MANIFEST_INDEX_FILENAME).unlink()
        write_run_manifest(ev, m, root=tmp_path)
        assert_canonically_readable(ev, expect_latest="ep1")

    def test_retry_after_the_mirror_was_lost(self, ev, tmp_path):
        m = self._stopped()
        write_run_manifest(ev, m, root=tmp_path)
        (ev / MANIFEST_FILENAME).unlink()
        write_run_manifest(ev, m, root=tmp_path)
        assert_canonically_readable(ev, expect_latest="ep1")

    def test_retry_after_an_artifact_was_lost_reports_corruption(self, ev, tmp_path):
        """F2 (round 12): a stop retry converges through every publication window — but a LOST
        published artifact is not a window, it is corruption. The retry says so instead of
        quietly rebuilding the evidence and calling the tree green."""
        m = self._stopped()
        write_run_manifest(ev, m, root=tmp_path)
        sorted((ev / MANIFESTS_SUBDIR / "ep1" / "calls").glob("*.json"))[0].unlink()
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, m, root=tmp_path)
        assert "missing call artifact" in str(exc.value)


# --------------------------------------------------------------------------- F12 (round 11)


class TestRound11Postconditions:
    """The operations round 11 added to the matrix. Each SUCCESS is immediately canonically
    readable; each FAILURE advances nothing."""

    def test_an_incomplete_same_id_winner_is_refused(self, ev, tmp_path):
        """A winner carrying our exact manifest and NO calls/ is not "the same episode"."""
        winner = _with_calls("ep1", 1)
        with _publish_incomplete_winner_at_rename(ev, winner):
            with pytest.raises(ManifestConflictError):
                write_run_manifest(ev, winner, root=tmp_path)
        # nothing was repaired into the winner, and no projection was advanced
        assert not (ev / MANIFEST_INDEX_FILENAME).exists()
        assert not list((ev / MANIFESTS_SUBDIR / "ep1" / "calls").glob("*")) \
            if (ev / MANIFESTS_SUBDIR / "ep1" / "calls").exists() else True

    def test_a_complete_same_id_winner_converges(self, ev, tmp_path):
        winner = _with_calls("ep1", 1)
        with _publish_winner_at_rename(ev, winner):
            write_run_manifest(ev, winner, root=tmp_path)     # identical content converges
        assert_canonically_readable(ev, expect_latest="ep1")

    def test_a_retry_over_a_damaged_prior_chain_advances_nothing(self, ev, tmp_path):
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        m2 = _ep("ep2", 2, prev="ep1", prior=("ep1",))
        write_run_manifest(ev, m2, root=tmp_path)
        before = (ev / MANIFEST_INDEX_FILENAME).read_bytes()
        sorted((ev / MANIFESTS_SUBDIR / "ep1" / "calls").glob("*.json"))[0].write_bytes(b"{}")
        with pytest.raises(ManifestError):
            write_run_manifest(ev, m2, root=tmp_path)          # the idempotent retry
        assert (ev / MANIFEST_INDEX_FILENAME).read_bytes() == before

    def test_an_append_over_an_extra_prior_artifact_advances_nothing(self, ev, tmp_path):
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        before = (ev / MANIFEST_INDEX_FILENAME).read_bytes()
        (ev / MANIFESTS_SUBDIR / "ep1" / "calls" / "EXTRA.json").write_bytes(b"{}")
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        assert not (ev / MANIFESTS_SUBDIR / "ep2").exists()
        assert (ev / MANIFEST_INDEX_FILENAME).read_bytes() == before

    def test_every_success_leaves_a_lifecycle_valid_expectation(self, ev, tmp_path):
        latest = None
        write_run_manifest(ev, _with_calls("ep1", 1), root=tmp_path)
        latest = assert_canonically_readable(ev, expect_latest="ep1")
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        latest = assert_canonically_readable(ev, expect_latest="ep2")
        from packages.orchestration.run_manifest import validate_call_expectation
        assert validate_call_expectation(
            latest.call_expectation, status=latest.status,
            capture_phase=latest.episode_snapshot.capture_phase,
            stop_request_id=latest.stop_request_id, calls=latest.calls,
            declared_task_ids=[t["task_id"]
                               for t in latest.episode_snapshot.input.job_input["tasks"]]) == []
