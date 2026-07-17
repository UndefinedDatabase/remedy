"""F3/F4 — recovery of the derived mirror/index from the IMMUTABLE episode records.

The immutable per-episode manifest + its artifacts are the source of truth; the root mirror and
run_manifest_index.json are derived projections. A crash that leaves the derived projection
missing/partial must be recoverable purely from the immutable episodes, and a partial
publication must converge on retry (so an F011 stop is never stuck pending forever).
"""
from __future__ import annotations

import json

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    MANIFEST_FILENAME,
    MANIFEST_INDEX_FILENAME,
    ManifestError,
    load_episode_record_for_recovery,
    load_latest_manifest_verified,
    rebuild_manifest_mirror_and_index_from_canonical_episodes,
    write_run_manifest,
)


def _ep(episode_id, ordinal, *, prev="", prior=(), status="completed"):
    from packages.orchestration.run_manifest import (
        CallCoverage, COVERAGE_COMPLETE, RunManifestV1, job_input_definition_sha256,
    )
    return RunManifestV1(
        job_id="j", episode_id=episode_id, created_at=f"2026-07-15T00:0{ordinal}:00+00:00",
        status=status, episode_snapshot=T._wrap(episode_id=episode_id),
        job_input_sha256=job_input_definition_sha256(T._snap().job_input),   # F6 bound
        calls=(),
        coverage=CallCoverage(status=COVERAGE_COMPLETE),
        # F6 (round 10): a zero-call episode must PROVE zero calls were expected.
        call_expectation=T._zero_call_proof(),
        prior_episode_ids=tuple(prior), episode_ordinal=ordinal, previous_episode_id=prev)


def _two_episode_tree(ev):
    ev.mkdir()
    write_run_manifest(ev, _ep("ep1", 1), root=ev)
    write_run_manifest(ev, _ep("ep2", 2, prev="ep1", prior=("ep1",)), root=ev)


class TestRecoveryLoader:
    def test_episode_loads_without_index_or_mirror(self, tmp_path):
        ev = tmp_path / "ev"
        _two_episode_tree(ev)
        (ev / MANIFEST_INDEX_FILENAME).unlink()          # derived index gone
        (ev / MANIFEST_FILENAME).unlink()                # derived mirror gone
        # the immutable episode still loads through the recovery path
        m = load_episode_record_for_recovery(ev, "ep2", expected_job_id="j")
        assert m.episode_id == "ep2" and m.episode_ordinal == 2
        # ...but the strict reader still REJECTS the inconsistent chain
        with pytest.raises(ManifestError):
            load_latest_manifest_verified(ev, job_id="j")


class TestRebuild:
    def test_rebuild_missing_index_from_episodes(self, tmp_path):
        ev = tmp_path / "ev"
        _two_episode_tree(ev)
        (ev / MANIFEST_INDEX_FILENAME).unlink()
        (ev / MANIFEST_FILENAME).unlink()
        latest = rebuild_manifest_mirror_and_index_from_canonical_episodes(
            ev, root=ev, job_id="j")
        assert latest == "ep2"
        # the derived projection is restored and the strict reader now accepts it
        idx = json.loads((ev / MANIFEST_INDEX_FILENAME).read_text())
        assert idx["latest_episode_id"] == "ep2"
        assert [e["episode_id"] for e in idx["episodes"]] == ["ep1", "ep2"]
        m = load_latest_manifest_verified(ev, job_id="j")
        assert m.episode_id == "ep2"

    def test_rebuild_refuses_a_non_contiguous_set(self, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, _ep("ep1", 1), root=ev)
        # F1 (round 10): the writer refuses to CREATE this set, so the fixture plants it — the
        # rebuild must still refuse to guess a chain out of it.
        from packages.orchestration.run_manifest import MANIFESTS_SUBDIR
        m3 = _ep("ep3", 3, prev="ep1", prior=("ep1",))
        ep = ev / MANIFESTS_SUBDIR / "ep3"
        (ep / "calls").mkdir(parents=True, exist_ok=True)
        (ep / MANIFEST_FILENAME).write_bytes(m3.canonical_bytes())
        (ev / MANIFEST_INDEX_FILENAME).unlink()
        with pytest.raises(ManifestError):
            rebuild_manifest_mirror_and_index_from_canonical_episodes(ev, root=ev, job_id="j")


class TestPartialPublicationConverges:
    def _finished_stopped_job(self, data_root, repo):
        from packages.orchestration.pingpong_job import (
            job_evidence_dir,
            load_job_plan,
            parse_job_file,
            run_job,
        )
        from packages.orchestration.pingpong_provider import FakeProvider
        from packages.orchestration.safe_points import request_stop

        job = parse_job_file("# Job: r\n\n## Task 1\nx\n\nAcceptance:\n- y\n", str(repo))
        request_stop(job.job_id, "operator requested stop", "cli")
        run_job(job.job_id, builder_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                reviewer_provider=FakeProvider(pass_on_round=1, fail_on_round=99),
                repair_rounds=0)
        return job.job_id, job_evidence_dir(job.job_id), load_job_plan

    def test_missing_index_recovers_on_retry(self, data_root, repo):
        job_id, ev, load_job_plan = self._finished_stopped_job(data_root, repo)
        # Simulate a crash during index publication: episode + mirror present, index gone.
        (ev / MANIFEST_INDEX_FILENAME).unlink()
        # A production re-finalization of the same episode recovers the derived projection.
        from packages.orchestration.pingpong_job import _write_run_manifest_record
        job = load_job_plan(job_id)
        ok = _write_run_manifest_record(job, status="stopped",
                                        episode_id=job.active_episode_id,
                                        stop_request_id=job.stop_request_id)
        assert ok and not job.run_manifest_error
        assert (ev / MANIFEST_INDEX_FILENAME).is_file()
        m = load_latest_manifest_verified(ev, job_id=job_id)
        assert m.status == "stopped"


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def repo(tmp_path):
    import subprocess
    r = tmp_path / "repo"
    r.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=r, check=True)
    return r
