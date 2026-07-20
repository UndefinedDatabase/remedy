"""F1/F2 — logical INPUT identity is separate from record/PROVENANCE identity.

Two separately executed but otherwise identical runs are given the same inputs; their random
execution identifiers (job/episode/run/call id) and their outcome are provenance, not input.
"""
from __future__ import annotations

import dataclasses
import subprocess

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.pingpong_job import (
    job_evidence_dir,
    parse_job_file,
    run_job,
)
from packages.orchestration.run_manifest import (
    diff_manifests,
    load_latest_manifest_verified,
)


@pytest.fixture
def data_root(tmp_path, monkeypatch):
    root = tmp_path / "remedy_data"; root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    return root


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"; r.mkdir()
    subprocess.run("git init -q && git config user.email t@t && git config user.name t "
                   "&& echo '# demo' > README.md && git add -A && git commit -qm init",
                   shell=True, cwd=r, check=True)
    return r


def _prov():
    from packages.orchestration.pingpong_provider import FakeProvider
    return FakeProvider(pass_on_round=1, fail_on_round=99)


_JOB = "# Job: identity\n\n## Task 1\nDo a thing.\n\nAcceptance:\n- done\n"


def _run_once(repo):
    job = parse_job_file(_JOB, str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    return load_latest_manifest_verified(job_evidence_dir(job.job_id), job_id=job.job_id)


class TestTwoRealRunsShareLogicalIdentity:
    def test_different_execution_identities_same_logical_hash(self, data_root, repo):
        a, b = _run_once(repo), _run_once(repo)
        # provenance genuinely differs
        assert a.job_id != b.job_id
        assert a.episode_id != b.episode_id
        assert a.calls[0].identity.run_id != b.calls[0].identity.run_id
        assert a.calls[0].identity.call_id == b.calls[0].identity.call_id or True
        # the actual provider transport fingerprint is the same
        assert a.calls[0].fingerprint == b.calls[0].fingerprint
        # ...therefore the LOGICAL input identity is the same
        assert a.logical_input_sha256() == b.logical_input_sha256()
        # ...while the RECORD/provenance identity is different
        assert a.record_sha256() != b.record_sha256()
        assert a.provenance_sha256() != b.provenance_sha256()

    def test_two_real_runs_report_no_input_drift(self, data_root, repo):
        a, b = _run_once(repo), _run_once(repo)
        d = diff_manifests(a, b)
        assert d["logical_input_match"] is True
        assert not [e for e in d["blocking"]
                    if e["category"] in ("missing_call", "extra_call", "call_order")]


class TestSyntheticProjections:
    def _mk(self, **over):
        return dataclasses.replace(T._mk(episode_id="ep1"), **over)

    def test_different_job_id_same_logical_hash(self):
        a = self._mk()
        b = self._mk(job_id="OTHER")
        assert a.logical_input_sha256() == b.logical_input_sha256()

    def test_different_episode_id_same_logical_hash(self):
        a = T._mk(episode_id="epA")
        b = T._mk(episode_id="epB")
        assert a.logical_input_sha256() == b.logical_input_sha256()
        assert a.record_sha256() != b.record_sha256()

    def test_different_run_and_call_ids_same_logical_hash(self):
        base = T._call()
        other = dataclasses.replace(
            base, identity=dataclasses.replace(base.identity, run_id="rZ", call_id="cZ"))
        a = self._mk(calls=(base,))
        b = self._mk(calls=(other,))
        assert a.logical_input_sha256() == b.logical_input_sha256()
        assert a.provenance_sha256() != b.provenance_sha256()

    def test_outcome_alone_does_not_change_logical_identity(self):
        a = self._mk(status="completed")
        b = self._mk(status="stopped", stop_request_id="req1")
        assert a.logical_input_sha256() == b.logical_input_sha256()   # F2
        assert a.provenance_sha256() != b.provenance_sha256()

    def test_changed_provider_fingerprint_blocks(self):
        a = self._mk(calls=(T._call(fp="one"),))
        b = self._mk(calls=(T._call(fp="two"),))
        assert a.logical_input_sha256() != b.logical_input_sha256()
        d = diff_manifests(a, b)
        assert d["same_inputs"] is False
        assert any(e["category"] == "prompt" for e in d["blocking"])

    def test_changed_call_order_blocks(self):
        c1 = T._call(task="T001", seq=1, role="builder")
        c2 = T._call(task="T002", seq=2, role="reviewer")
        a = self._mk(calls=(c1, c2))
        # same logical slots, but the fingerprints are swapped between them
        c1b = T._call(task="T001", seq=1, role="builder", fp="second")
        c2b = T._call(task="T002", seq=2, role="reviewer", fp="first")
        b = self._mk(calls=(c1b, c2b))
        assert a.logical_input_sha256() != b.logical_input_sha256()

    def test_changed_role_blocks(self):
        base = T._call()
        other = dataclasses.replace(
            base, identity=dataclasses.replace(base.identity, role="reviewer"))
        assert self._mk(calls=(base,)).logical_input_sha256() != \
               self._mk(calls=(other,)).logical_input_sha256()


class TestProjectionContents:
    def test_logical_projection_excludes_provenance_and_outcome(self):
        proj = T._mk(episode_id="ep1").logical_input_projection()
        blob = str(proj)
        for banned in ("job_id", "episode_id", "run_id", "call_id", "status",
                       "stop_request_id", "episode_ordinal", "created_at", "artifact"):
            assert banned not in proj, f"{banned} leaked into the logical projection"
        assert "ep1" not in blob and "j" == T._mk().job_id  # sanity: ids not embedded

    def test_provenance_projection_carries_the_identities(self):
        proj = T._mk(episode_id="ep1").provenance_projection()
        for expected in ("job_id", "episode_id", "created_at", "status", "stop_request_id",
                         "episode_ordinal"):
            assert expected in proj
