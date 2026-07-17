"""F11 (round 12) — bounded, safe cleanup of crashed private staging directories.

Crash debris is already invisible to every canonical reader (that is the point of staging living
outside the namespace), so this is hygiene, not correctness. Which is exactly why it is written to
fail safe: deleting an ACTIVE writer's stage would destroy an episode mid-publication, and that is
far worse than leaving a directory behind.

The bound: only the exact staging name format, only under the append claim, only when the owning
PID is gone AND the stage is old, never a symlink, never a canonical episode, and a cleanup
failure is swallowed rather than allowed to break the caller's real work.
"""
from __future__ import annotations

import dataclasses
import hashlib
import os
import time

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    MANIFESTS_SUBDIR,
    STAGING_SUBDIR,
    canonical_artifact_ref,
    cleanup_abandoned_stages,
    validate_index_and_tree,
    write_run_manifest,
)


def _ep(episode_id, ordinal, *, prev="", prior=()):
    # Round 13 (F5): a per-EPISODE run id — production re-runs a task under a NEW run when
    # a job resumes, so two episodes never share a run while each ledger lists only its own
    # call. (One run that legitimately spans episodes carries the earlier entries forward;
    # `validate_ledger_chain` holds it to that.)
    m = T._mk(episode_id=episode_id, calls=(T._call(run=f"r-{episode_id}"),))
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


def _stage(ev, name, *, age_seconds=0):
    p = ev / STAGING_SUBDIR / name
    (p / "calls").mkdir(parents=True, exist_ok=True)
    (p / "run_manifest.json").write_bytes(b'{"half": "written"}')
    if age_seconds:
        old = time.time() - age_seconds
        os.utime(p, (old, old))
    return p


def _stages(ev):
    root = ev / STAGING_SUBDIR
    return sorted(p.name for p in root.iterdir()) if root.exists() else []


_DEAD_PID = 999_999_998          # a pid that is not running


class TestOnlyAbandonedStagesAreRemoved:
    def test_a_stale_stage_from_a_dead_writer_is_removed(self, ev, tmp_path):
        _stage(ev, f"ep2.{_DEAD_PID}.abcdef0123456789", age_seconds=48 * 3600)
        removed = cleanup_abandoned_stages(ev, root=tmp_path)
        assert removed == [f"ep2.{_DEAD_PID}.abcdef0123456789"]
        assert _stages(ev) == []

    def test_an_ACTIVE_writers_stage_is_never_removed(self, ev, tmp_path):
        """The owning process is alive — its stage is an episode in flight, not debris."""
        name = f"ep2.{os.getpid()}.abcdef0123456789"
        _stage(ev, name, age_seconds=48 * 3600)
        assert cleanup_abandoned_stages(ev, root=tmp_path) == []
        assert _stages(ev) == [name]

    def test_a_fresh_stage_is_never_removed(self, ev, tmp_path):
        name = f"ep2.{_DEAD_PID}.abcdef0123456789"
        _stage(ev, name)                                  # brand new
        assert cleanup_abandoned_stages(ev, root=tmp_path) == []
        assert _stages(ev) == [name]

    def test_a_foreign_name_is_never_touched(self, ev, tmp_path):
        """Only the exact staging format is ours to reason about."""
        (ev / STAGING_SUBDIR).mkdir(exist_ok=True)
        (ev / STAGING_SUBDIR / "someone-elses-directory").mkdir()
        assert cleanup_abandoned_stages(ev, root=tmp_path) == []
        assert "someone-elses-directory" in _stages(ev)

    def test_a_symlinked_stage_is_never_followed_or_removed(self, ev, tmp_path):
        outside = tmp_path / "outside"
        outside.mkdir()
        (outside / "precious.txt").write_text("do not delete me")
        (ev / STAGING_SUBDIR).mkdir(exist_ok=True)
        link = ev / STAGING_SUBDIR / f"ep2.{_DEAD_PID}.abcdef0123456789"
        os.symlink(str(outside), str(link))
        old = time.time() - 48 * 3600
        os.utime(link, (old, old), follow_symlinks=False)
        assert cleanup_abandoned_stages(ev, root=tmp_path) == []
        assert (outside / "precious.txt").exists()

    def test_cleanup_never_touches_the_canonical_namespace(self, ev, tmp_path):
        _stage(ev, f"ep2.{_DEAD_PID}.abcdef0123456789", age_seconds=48 * 3600)
        before = sorted(p.name for p in (ev / MANIFESTS_SUBDIR).iterdir())
        cleanup_abandoned_stages(ev, root=tmp_path)
        assert sorted(p.name for p in (ev / MANIFESTS_SUBDIR).iterdir()) == before
        assert validate_index_and_tree(ev, job_id="j") == []

    def test_cleanup_is_bounded(self, ev, tmp_path):
        from packages.orchestration.run_manifest import STAGING_CLEANUP_MAX_ITEMS
        for i in range(STAGING_CLEANUP_MAX_ITEMS + 10):
            _stage(ev, f"ep{i}.{_DEAD_PID}.abcdef012345678{i % 10}", age_seconds=48 * 3600)
        removed = cleanup_abandoned_stages(ev, root=tmp_path)
        assert len(removed) <= STAGING_CLEANUP_MAX_ITEMS

    def test_no_staging_dir_at_all_is_not_an_error(self, tmp_path):
        d = tmp_path / "empty"
        d.mkdir()
        assert cleanup_abandoned_stages(d, root=tmp_path) == []

    def test_a_write_still_succeeds_with_debris_present(self, ev, tmp_path):
        """Hygiene must never break the caller's real work."""
        _stage(ev, f"ep9.{_DEAD_PID}.abcdef0123456789", age_seconds=48 * 3600)
        write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=tmp_path)
        assert validate_index_and_tree(ev, job_id="j") == []
        assert _stages(ev) == [], "the write's hygiene pass left debris behind"
