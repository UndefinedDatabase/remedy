"""F10 (round 9) — the F012 marker changes ABSENCE semantics ONLY.

`run_manifest_required_v` answers exactly one question: is a MISSING manifest allowed? A pre-F012
job never recorded one, so its absence is legacy/uncovered — readable, not corrupt.

It answers nothing about a manifest that IS there. An unmarked job whose evidence directory
contains manifest artifacts gets the full trust chain: strict decode, canonical bytes, the exact
allowlist, hash-bound artifacts. Skipping that because a marker is absent would mean copying
unverified bytes into an Evidence bundle — the marker is not a permission to trust.
"""
from __future__ import annotations

import json
import subprocess

import pytest

from packages.orchestration.job_evidence import _write_run_manifest_export
from packages.orchestration.pingpong_job import (
    _persist_job,
    job_evidence_dir,
    load_job_plan,
    parse_job_file,
    run_job,
)
from packages.orchestration.run_manifest import (
    MANIFEST_FILENAME,
    MANIFEST_INDEX_FILENAME,
    MANIFESTS_SUBDIR,
)


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=r, check=True)
    return r


def _prov():
    from packages.orchestration.pingpong_provider import FakeProvider
    return FakeProvider(pass_on_round=1, fail_on_round=99)


def _completed_job(repo):
    job = parse_job_file("# Job: legacy\n\n## Task 1\nx\n\nAcceptance:\n- y\n", str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    return load_job_plan(job.job_id)


def _unmark(job):
    """Make the job look pre-F012 — the marker gone, the manifest tree still on disk."""
    job.run_manifest_required_v = 0
    _persist_job(job)
    reloaded = load_job_plan(job.job_id)
    assert reloaded.run_manifest_required_v == 0    # the marker really is gone on disk
    return reloaded


def _export(job, out_base):
    written: dict = {}
    failures: list = []
    notes: list = []
    _write_run_manifest_export(job, str(out_base), written, failures, notes)
    return written, failures, notes


# --------------------------------------------------------------------------- absence


class TestTheMarkerGovernsAbsence:
    def test_an_unmarked_job_with_no_manifest_is_legacy_not_corrupt(
            self, data_root, repo, tmp_path):
        job = _completed_job(repo)
        ev = job_evidence_dir(job.job_id)
        for p in (ev / MANIFEST_FILENAME, ev / MANIFEST_INDEX_FILENAME):
            p.unlink()
        for d in (ev / MANIFESTS_SUBDIR).iterdir():
            for f in sorted(d.rglob("*"), reverse=True):
                f.unlink() if f.is_file() else f.rmdir()
            d.rmdir()
        (ev / MANIFESTS_SUBDIR).rmdir()

        _w, failures, notes = _export(_unmark(job), tmp_path / "out1")
        assert failures == []
        assert any("legacy" in n for n in notes)

    def test_a_marked_job_with_no_manifest_is_blocking(self, data_root, repo, tmp_path):
        job = _completed_job(repo)
        ev = job_evidence_dir(job.job_id)
        (ev / MANIFEST_FILENAME).unlink()
        _w, failures, _n = _export(job, tmp_path / "out2")
        assert failures, "a marked terminal job with no manifest must block"


# --------------------------------------------------------------------------- presence


class TestAPresentTreeIsAlwaysValidated:
    def test_an_unmarked_job_with_a_clean_tree_still_exports_it(
            self, data_root, repo, tmp_path):
        """Present and valid: the bytes are verified, then copied. The marker is irrelevant."""
        job = _unmark(_completed_job(repo))
        written, failures, _n = _export(job, tmp_path / "out3")
        assert failures == []
        assert MANIFEST_FILENAME in written and MANIFEST_INDEX_FILENAME in written

    def test_an_unmarked_job_with_a_tampered_mirror_is_an_integrity_failure(
            self, data_root, repo, tmp_path):
        """THE finding: an absent marker must not buy a corrupt tree a free pass."""
        job = _unmark(_completed_job(repo))
        ev = job_evidence_dir(job.job_id)
        (ev / MANIFEST_FILENAME).write_bytes(b'{"job_id": "tampered"}')
        written, failures, _n = _export(job, tmp_path / "out4")
        assert failures, "a present-but-malformed tree was trusted because the marker was absent"
        assert written == {}, "unverified bytes must never reach the bundle"

    def test_an_unmarked_job_with_a_noncanonical_index_is_an_integrity_failure(
            self, data_root, repo, tmp_path):
        job = _unmark(_completed_job(repo))
        ev = job_evidence_dir(job.job_id)
        idx = json.loads((ev / MANIFEST_INDEX_FILENAME).read_text())
        (ev / MANIFEST_INDEX_FILENAME).write_bytes(json.dumps(idx, indent=4).encode())
        _w, failures, _n = _export(job, tmp_path / "out5")
        assert failures

    def test_an_unmarked_job_with_a_mishashed_call_artifact_is_an_integrity_failure(
            self, data_root, repo, tmp_path):
        job = _unmark(_completed_job(repo))
        ev = job_evidence_dir(job.job_id)
        artifacts = sorted((ev / MANIFESTS_SUBDIR).rglob("calls/*.json"))
        assert artifacts, "the fixture run recorded no call artifacts"
        artifacts[0].write_bytes(b'{"swapped": true}')
        written, failures, _n = _export(job, tmp_path / "out6")
        assert failures
        assert written == {}

    def test_an_unmarked_job_with_a_missing_index_is_an_integrity_failure(
            self, data_root, repo, tmp_path):
        """A mirror with no index is a broken tree, marker or not."""
        job = _unmark(_completed_job(repo))
        (job_evidence_dir(job.job_id) / MANIFEST_INDEX_FILENAME).unlink()
        _w, failures, _n = _export(job, tmp_path / "out7")
        assert failures

    def test_an_unmarked_job_with_an_undeclared_episode_is_an_integrity_failure(
            self, data_root, repo, tmp_path):
        job = _unmark(_completed_job(repo))
        ev = job_evidence_dir(job.job_id)
        (ev / MANIFESTS_SUBDIR / "ep-smuggled").mkdir()
        (ev / MANIFESTS_SUBDIR / "ep-smuggled" / MANIFEST_FILENAME).write_bytes(b"{}")
        _w, failures, _n = _export(job, tmp_path / "out8")
        assert failures
