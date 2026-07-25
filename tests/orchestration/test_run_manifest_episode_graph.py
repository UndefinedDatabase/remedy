"""F5/F6/F1 — episode ordering, prior-episode DAG, and mandatory episode-snapshot capture.

* F5: episodes carry a NON-TIME ordinal; the latest is the max-ordinal episode, so re-pointing
  the index at an older episode (a rollback) is detected even if its timestamp is newer.
* F6: the prior-episode references must form a DAG that respects the ordinal order — no self,
  cycle, future/equal-ordinal, unknown or duplicate edge survives validation.
* F1: the episode-start input snapshot is typed, episode-owned and MANDATORY — a failed capture
  is blocking and is never papered over by a terminal re-probe.
"""
from __future__ import annotations

import json

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    COVERAGE_COMPLETE,
    MANIFEST_FILENAME,
    MANIFEST_INDEX_FILENAME,
    CallCoverage,
    EpisodeInputSnapshotV1,
    ManifestError,
    RunManifestV1,
    _validate_episode_graph,
    build_run_manifest,
    decode_episode_snapshot_v1,
    load_latest_manifest_verified,
    validate_index_and_tree,
    validate_run_manifest,
    write_run_manifest,
)


def _bound_hash():
    from packages.orchestration.run_manifest import job_input_definition_sha256
    return job_input_definition_sha256(T._snap().job_input)


def _ep(episode_id, ordinal, *, prev="", prior=(), status="completed"):
    return RunManifestV1(
        job_id="j", episode_id=episode_id, created_at=f"2026-07-15T00:0{ordinal}:00+00:00",
        status=status, episode_snapshot=T._wrap(episode_id=episode_id),
        job_input_sha256=_bound_hash(),                     # F6: bound to the embedded def
        calls=(), coverage=CallCoverage(status=COVERAGE_COMPLETE),
        call_expectation=T._zero_call_proof(),
        prior_episode_ids=tuple(prior), episode_ordinal=ordinal, previous_episode_id=prev)


# --------------------------------------------------------------------------- F5


def _plant_episode(ev, m):
    """Place an episode's canonical bytes on disk WITHOUT the writer.

    F1 (round 10): the writer now refuses to create a broken chain at all, so a test that wants
    to prove the READER also rejects one has to be a stronger adversary than the writer — it
    plants the bytes itself and re-derives the index by hand.
    """
    from packages.orchestration.run_manifest import (
        MANIFESTS_SUBDIR,
        canonical_index_bytes,
        decode_run_manifest_v1,
    )
    ep = ev / MANIFESTS_SUBDIR / m.episode_id
    (ep / "calls").mkdir(parents=True, exist_ok=True)
    (ep / MANIFEST_FILENAME).write_bytes(m.canonical_bytes())
    # rebuild the index over every planted episode, mirroring the writer's derivation
    eps = []
    for d in sorted((ev / MANIFESTS_SUBDIR).iterdir()):
        raw = (d / MANIFEST_FILENAME).read_bytes()
        eps.append(decode_run_manifest_v1(raw))
    eps.sort(key=lambda x: x.episode_ordinal)
    latest = eps[-1]
    index = {"index_v": 1, "latest_episode_id": latest.episode_id,
             "episodes": [{"episode_id": e.episode_id, "episode_ordinal": e.episode_ordinal,
                           "previous_episode_id": e.previous_episode_id, "status": e.status,
                           "created_at": e.created_at,
                           "record_sha256": e.record_sha256()} for e in eps]}
    (ev / MANIFEST_INDEX_FILENAME).write_bytes(canonical_index_bytes(index))
    (ev / MANIFEST_FILENAME).write_bytes(latest.canonical_bytes())


class TestEpisodeOrdinalRollback:
    def test_two_episodes_validate_clean(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, _ep("ep1", 1), root=ev)
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=ev)
        assert validate_index_and_tree(ev, job_id="j") == []
        idx = json.loads((ev / MANIFEST_INDEX_FILENAME).read_text())
        assert idx["latest_episode_id"] == "ep2"      # max ordinal, not newest timestamp

    def test_rollback_latest_to_older_episode_is_rejected(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, _ep("ep1", 1), root=ev)
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=ev)
        # Tamper: re-point latest at the OLDER, lower-ordinal episode — and RE-CANONICALIZE
        # the bytes, so the rollback rule itself is proven rather than the byte-canonicality
        # rule catching a lazy tamperer first.
        from packages.orchestration.run_manifest import canonical_index_bytes
        idx = json.loads((ev / MANIFEST_INDEX_FILENAME).read_text())
        idx["latest_episode_id"] = "ep1"
        (ev / MANIFEST_INDEX_FILENAME).write_bytes(canonical_index_bytes(idx))
        probs = validate_index_and_tree(ev, job_id="j")
        assert any("rollback" in p or "max-ordinal" in p for p in probs), probs

    def test_the_writer_refuses_to_append_a_duplicate_ordinal(self, tmp_path):
        """F1 (round 10): the append preflight validates the COMPLETE chain, so a duplicate
        ordinal is refused BEFORE any mirror/index is published — not discovered afterwards."""
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, _ep("ep1", 1), root=ev)
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, _ep("ep2", 1), root=ev)
        assert "ordinal" in str(exc.value)
        # ...and the published chain is untouched and still readable.
        assert validate_index_and_tree(ev, job_id="j") == []
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep1"

    def test_duplicate_ordinals_are_rejected(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, _ep("ep1", 1), root=ev)
        _plant_episode(ev, _ep("ep2", 1))        # planted behind the writer's back
        probs = validate_index_and_tree(ev, job_id="j")
        assert any("ordinal" in p for p in probs), probs

    def test_the_writer_refuses_to_skip_an_ordinal(self, tmp_path):
        """F1: an append that skips its immediate predecessor is refused at the write."""
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, _ep("ep1", 1), root=ev)
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, _ep("ep3", 3, prev="ep1", prior=("ep1",)), root=ev)
        assert "ordinal" in str(exc.value)
        assert validate_index_and_tree(ev, job_id="j") == []

    def test_non_contiguous_ordinals_are_rejected(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, _ep("ep1", 1), root=ev)
        _plant_episode(ev, _ep("ep3", 3, prev="ep1", prior=("ep1",)))
        probs = validate_index_and_tree(ev, job_id="j")
        assert any("contiguous" in p for p in probs), probs


# --------------------------------------------------------------------------- F6


class TestPriorEpisodeGraph:
    def test_self_reference_is_rejected(self):
        m = _ep("ep1", 1, prior=("ep1",))
        assert any("itself" in p or "self" in p for p in _validate_episode_graph({"ep1": m}))

    def test_unknown_prior_is_rejected(self):
        m = _ep("ep2", 2, prev="", prior=("ghost",))
        probs = _validate_episode_graph({"ep2": m})
        assert any("unknown prior" in p for p in probs), probs

    def test_future_ordinal_prior_is_rejected(self):
        a = _ep("ep1", 1, prior=("ep2",))    # ep1 points FORWARD to ep2
        b = _ep("ep2", 2)
        probs = _validate_episode_graph({"ep1": a, "ep2": b})
        assert any("not strictly earlier" in p or "cycle" in p for p in probs), probs

    def test_cycle_is_rejected(self):
        # Two episodes that (illegally) reference each other.
        a = _ep("ep1", 1, prior=("ep2",))
        b = _ep("ep2", 2, prev="ep1", prior=("ep1", "ep1"))  # also duplicate edge
        probs = _validate_episode_graph({"ep1": a, "ep2": b})
        assert probs  # a mix of duplicate / future / cycle problems, but never silent


class TestManifestOrdinalValidation:
    def test_ordinal_below_one_is_invalid(self):
        m = _ep("ep1", 0)
        assert any("episode_ordinal" in p for p in validate_run_manifest(m))

    def test_previous_must_be_a_prior(self):
        m = _ep("ep2", 2, prev="epX", prior=("ep1",))
        assert any("previous_episode_id is not among prior" in p
                   for p in validate_run_manifest(m))

    def test_first_episode_may_not_have_a_previous(self):
        m = _ep("ep1", 1, prev="ep0", prior=("ep0",))
        assert any("first episode" in p for p in validate_run_manifest(m))


# ----------------------------------------------------------------------- F8 (order)


class TestExactHistory:
    def test_skipping_immediate_predecessor_is_rejected(self):
        # ep3 (ord 3) whose previous points at ep1 instead of ep2 — an incomplete history.
        a = _ep("ep1", 1)
        b = _ep("ep2", 2, prev="ep1", prior=("ep1",))
        c = _ep("ep3", 3, prev="ep1", prior=("ep1", "ep2"))
        probs = _validate_episode_graph({"ep1": a, "ep2": b, "ep3": c})
        assert any("immediate predecessor" in p for p in probs), probs

    def test_out_of_order_prior_list_is_rejected(self):
        a = _ep("ep1", 1)
        b = _ep("ep2", 2, prev="ep1", prior=("ep1",))
        # ep3 lists priors in the wrong (descending) order.
        c = _ep("ep3", 3, prev="ep2", prior=("ep2", "ep1"))
        probs = _validate_episode_graph({"ep1": a, "ep2": b, "ep3": c})
        assert any("ascending history" in p for p in probs), probs


# ----------------------------------------------------------------------- F9/F10


class TestJobPlanIndexCrosscheck:
    def _job(self, episodes, status="completed", active=""):
        class _J:
            run_manifest_episodes = episodes
        _J.status = status
        _J.active_episode_id = active
        return _J()

    def _idx(self, episodes, latest):
        return {"index_v": 1, "latest_episode_id": latest, "episodes": episodes}

    def _run_xcheck(self, job, index):
        from packages.orchestration.job_evidence import (
            _crosscheck_job_episodes_vs_index,
        )
        return _crosscheck_job_episodes_vs_index(job, index)

    def _e(self, eid, ordinal, *, status="completed", created="t", prev=""):
        return {"episode_id": eid, "episode_ordinal": ordinal, "status": status,
                "created_at": created, "previous_episode_id": prev}

    def test_clean_agreement(self):
        eps = [self._e("ep1", 1, created="t1")]
        assert self._run_xcheck(self._job(eps), self._idx(eps, "ep1")) == []

    def test_created_at_mismatch_blocks(self):
        job_eps = [self._e("ep1", 1, created="X")]
        idx_eps = [self._e("ep1", 1, created="Y")]
        probs = self._run_xcheck(self._job(job_eps), self._idx(idx_eps, "ep1"))
        assert any("created_at" in p for p in probs), probs

    def test_previous_mismatch_blocks(self):
        job_eps = [self._e("ep2", 2, prev="epX")]
        idx_eps = [self._e("ep2", 2, prev="ep1")]
        probs = self._run_xcheck(self._job(job_eps), self._idx(idx_eps, "ep2"))
        assert any("previous_episode_id" in p for p in probs), probs

    def test_latest_mismatch_blocks(self):
        idx_eps = [self._e("ep1", 1), self._e("ep2", 2)]
        # index latest points at the LOWER-ordinal episode
        probs = self._run_xcheck(self._job(idx_eps), self._idx(idx_eps, "ep1"))
        assert any("latest" in p or "max-ordinal" in p for p in probs), probs

    def test_duplicate_jobplan_episode_blocks(self):
        job_eps = [self._e("ep1", 1), self._e("ep1", 1)]
        idx_eps = [self._e("ep1", 1)]
        probs = self._run_xcheck(self._job(job_eps), self._idx(idx_eps, "ep1"))
        assert any("duplicate" in p for p in probs), probs

    def test_index_only_episode_blocks(self):
        probs = self._run_xcheck(
            self._job([self._e("ep1", 1)]),
            self._idx([self._e("ep1", 1), self._e("ep2", 2)], "ep2"))
        assert any("index-only" in p for p in probs), probs


class TestCanonicalOrderDerivation:
    def test_next_ordinal_and_previous_come_from_the_index(self, tmp_path):
        from packages.orchestration.run_manifest import (
            read_canonical_episode_order,
            write_run_manifest,
        )
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, _ep("ep1", 1), root=ev)
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=ev)
        order = read_canonical_episode_order(ev, job_id="j")
        assert [e["episode_id"] for e in order] == ["ep1", "ep2"]      # ascending
        assert order[-1]["episode_ordinal"] == 2                        # next would be 3
        assert order[-1]["previous_episode_id"] == "ep1"


# --------------------------------------------------------------------------- F1


class TestMandatoryEpisodeSnapshot:
    def test_failed_capture_is_blocking_not_reprobed(self):
        # A caller that lost the snapshot (a failed capture) cannot build a manifest — the
        # finalizer never re-probes a fresh terminal snapshot to hide it.
        class _Job:
            job_id = "j"
            tasks = []
        with pytest.raises(ManifestError):
            build_run_manifest(_Job(), status="completed", episode_id="ep",
                               created_at="t", episode_snapshot=None)

    def test_wrapper_round_trips_and_reports_status(self):
        w = T._wrap(episode_id="ep")
        again = decode_episode_snapshot_v1(w.to_json())
        assert again.is_ok() and again.episode_id == "ep"
        failed = EpisodeInputSnapshotV1(
            snapshot_v=1, episode_id="ep", captured_at="2026-07-15T00:00:00+00:00",
            capture_phase="episode_start", status="failed", problems=("boom",), input=None)
        assert not failed.is_ok()
        assert decode_episode_snapshot_v1(failed.to_json()).problems == ("boom",)
