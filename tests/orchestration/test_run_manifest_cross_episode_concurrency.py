"""F1 (round 11) — every append for one job is serialized, preflight through postcondition.

The atomic directory rename only serializes writers racing for the SAME episode name. Two writers
publishing DIFFERENT episode ids never collide on a name at all: each reads the chain, each
computes "the next ordinal is 2", and each succeeds — leaving `ep2a` and `ep2b` both claiming
ordinal 2 and a canonical loader that rejects the result. Reproduced exactly that way.

So the whole state transition is held under ONE per-job advisory lock (`flock`), which the kernel
releases when the holder's fd closes — on return, on exception, and on process death. Readers
never take it: they validate canonical state instead, so a wedged writer can never block
verification.
"""
from __future__ import annotations

import dataclasses
import hashlib
import os
import threading

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration import run_manifest as RM
from packages.orchestration.run_manifest import (
    APPEND_LOCK_NAME,
    CONTROL_SUBDIR,
    MANIFESTS_SUBDIR,
    ManifestError,
    append_claim,
    canonical_artifact_ref,
    load_latest_manifest_verified,
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
def ev(tmp_path):
    d = tmp_path / "ev"
    d.mkdir()
    write_run_manifest(d, _ep("ep1", 1), root=tmp_path)
    return d


def _episodes(ev):
    return sorted(p.name for p in (ev / MANIFESTS_SUBDIR).iterdir())


def _run_writers(ev, tmp_path, manifests, *, gate_after_preflight=True):
    """Run writers concurrently, optionally forcing them all to preflight before any publishes —
    the exact interleaving that produced two ordinal-2 episodes."""
    results: dict[str, str] = {}
    barrier = threading.Barrier(len(manifests), timeout=10) if gate_after_preflight else None
    real = RM.load_verified_canonical_chain_for_write

    def _gated(*a, **kw):
        out = real(*a, **kw)
        if barrier is not None:
            try:
                barrier.wait()
            except Exception:
                pass          # the lock means only one writer reaches here at a time
        return out

    RM.load_verified_canonical_chain_for_write = _gated
    try:
        threads = []
        for m in manifests:
            def _go(m=m):
                try:
                    write_run_manifest(ev, m, root=tmp_path)
                    results[m.episode_id] = "success"
                except Exception as exc:
                    results[m.episode_id] = type(exc).__name__
            t = threading.Thread(target=_go)
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=60)
    finally:
        RM.load_verified_canonical_chain_for_write = real
    return results


# --------------------------------------------------------------------------- the finding


class TestTwoEpisodeIdsCannotClaimOneOrdinal:
    def test_the_reproduced_race(self, ev, tmp_path):
        """THE finding: both writers succeeded and the chain had a duplicate ordinal 2."""
        results = _run_writers(ev, tmp_path, [
            _ep("ep2a", 2, prev="ep1", prior=("ep1",)),
            _ep("ep2b", 2, prev="ep1", prior=("ep1",)),
        ])
        assert sorted(results.values()) == ["ManifestError", "success"], results
        assert len(_episodes(ev)) == 2, _episodes(ev)
        assert validate_index_and_tree(ev, job_id="j") == []
        latest = load_latest_manifest_verified(ev, job_id="j")
        assert latest.episode_ordinal == 2

    def test_three_parallel_append_writers_leave_one_contiguous_chain(self, ev, tmp_path):
        results = _run_writers(ev, tmp_path, [
            _ep("ep2a", 2, prev="ep1", prior=("ep1",)),
            _ep("ep2b", 2, prev="ep1", prior=("ep1",)),
            _ep("ep2c", 2, prev="ep1", prior=("ep1",)),
        ])
        assert list(results.values()).count("success") == 1, results
        assert validate_index_and_tree(ev, job_id="j") == []
        episodes = _episodes(ev)
        assert len(episodes) == 2, episodes

    def test_the_loser_publishes_nothing_at_all(self, ev, tmp_path):
        results = _run_writers(ev, tmp_path, [
            _ep("ep2a", 2, prev="ep1", prior=("ep1",)),
            _ep("ep2b", 2, prev="ep1", prior=("ep1",)),
        ])
        loser = [eid for eid, r in results.items() if r != "success"][0]
        assert not (ev / MANIFESTS_SUBDIR / loser).exists()

    def test_a_serialized_second_append_still_succeeds(self, ev, tmp_path):
        """Serialization is not refusal: the second writer just has to take its turn, see the
        real chain, and be ordinal 3."""
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        write_run_manifest(ev, _ep("ep3", 3, prev="ep2", prior=("ep1", "ep2")), root=tmp_path)
        assert validate_index_and_tree(ev, job_id="j") == []
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep3"


# --------------------------------------------------------------------------- the claim itself


class TestTheAppendClaim:
    def test_the_lock_lives_outside_the_canonical_namespace(self, ev, tmp_path):
        """A lock file inside `run_manifests/` would be an undeclared member of the very tree it
        protects."""
        assert (ev / CONTROL_SUBDIR / APPEND_LOCK_NAME).exists()
        assert CONTROL_SUBDIR not in _episodes(ev)
        assert validate_index_and_tree(ev, job_id="j") == []

    def test_the_lock_never_enters_the_verified_tree_or_an_export(self, ev, tmp_path):
        from packages.orchestration.run_manifest import build_verified_manifest_tree
        files, problems = build_verified_manifest_tree(ev, job_id="j")
        assert problems == []
        assert not any(CONTROL_SUBDIR in k or "lock" in k for k in files), sorted(files)

    def test_the_claim_is_released_after_an_exception(self, ev, tmp_path):
        """A crash-safe lock is the only kind worth having: if a failed append kept the claim,
        the job could never be written again."""
        with pytest.raises(RuntimeError):
            with append_claim(ev, root=tmp_path):
                raise RuntimeError("boom")
        # the very next append proceeds immediately
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep2"

    def test_a_failed_write_releases_the_claim(self, ev, tmp_path):
        with pytest.raises(ManifestError):
            write_run_manifest(ev, _ep("ep2", 9, prev="ep1", prior=("ep1",)), root=tmp_path)
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        assert validate_index_and_tree(ev, job_id="j") == []

    def test_a_dead_holders_claim_does_not_persist(self, ev, tmp_path):
        """`flock` is released by the kernel when the fd closes, so a process that died holding
        it leaves nothing behind to clean up."""
        import packages.common.secure_fs as _fs

        ctl = _fs.anchor_destination(ev / CONTROL_SUBDIR, tmp_path, error_cls=ManifestError,
                                     noun="ctl", create=True)
        try:
            fd = _fs.exclusive_lock_fd(APPEND_LOCK_NAME, ctl, timeout_sec=5)
            os.close(fd)          # the holder "dies" without unlocking
        finally:
            os.close(ctl)
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep2"

    def test_a_held_claim_times_out_with_a_bounded_diagnostic(self, ev, tmp_path):
        """A wedged holder must surface as a diagnosable error, never a hang."""
        import packages.common.secure_fs as _fs

        ctl = _fs.anchor_destination(ev / CONTROL_SUBDIR, tmp_path, error_cls=ManifestError,
                                     noun="ctl", create=True)
        held = _fs.exclusive_lock_fd(APPEND_LOCK_NAME, ctl, timeout_sec=5)
        try:
            with pytest.raises(ManifestError) as exc:
                with append_claim(ev, root=tmp_path, timeout_sec=0.2):
                    pass
            assert "did not become available" in str(exc.value)
        finally:
            _fs.release_lock_fd(held)
            os.close(ctl)
        # ...and once the holder lets go, the next append proceeds
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)

    def test_readers_never_block_on_a_held_claim(self, ev, tmp_path):
        """Verification must never depend on a writer's good behaviour."""
        with append_claim(ev, root=tmp_path):
            assert validate_index_and_tree(ev, job_id="j") == []
            assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep1"

    def test_no_starvation_across_serial_appends(self, ev, tmp_path):
        """Bounded conditions: every writer that takes its turn eventually gets one."""
        results = _run_writers(ev, tmp_path, [
            _ep("ep2a", 2, prev="ep1", prior=("ep1",)),
            _ep("ep2b", 2, prev="ep1", prior=("ep1",)),
        ], gate_after_preflight=False)
        assert len(results) == 2, results          # both ran; neither hung
        assert "success" in results.values()
