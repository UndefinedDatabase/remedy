"""F4 — persisted RUN records are untrusted: strict-decode before manifest collection."""
from __future__ import annotations

import json
import subprocess

import pytest

from packages.orchestration.pingpong_job import load_job_plan, parse_job_file, run_job
from packages.orchestration.run_manifest import (
    COVERAGE_INCOMPLETE,
    build_input_snapshot,
    build_run_manifest,
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


def _run(repo):
    job = parse_job_file("# Job: p\n\n## Task 1\nx\n\nAcceptance:\n- y\n", str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    return load_job_plan(job.job_id)


def _run_json_path(job):
    from packages.orchestration.data_paths import run_dir
    return run_dir(job.tasks[0].run_id) / "result.json"


def _tamper(job, mutate):
    p = _run_json_path(job)
    d = json.loads(p.read_text())
    mutate(d["finalized_calls"][0])
    p.write_text(json.dumps(d))


def _collect(job):
    from packages.orchestration.run_manifest import EpisodeInputSnapshotV1
    snap = build_input_snapshot(job, inspect_target=False, probe_versions=False)
    wrapper = EpisodeInputSnapshotV1(
        snapshot_v=1, episode_id=job.active_episode_id,
        captured_at="2026-07-16T00:00:00+00:00", capture_phase="episode_start",
        status="ok", problems=(), input=snap)
    return build_run_manifest(job, status="completed", episode_id=job.active_episode_id,
                              created_at="2026-07-16T00:00:00+00:00",
                              episode_snapshot=wrapper,
                              owned_episode_id=job.active_episode_id)


class TestPersistedRunRecordIsUntrusted:
    def test_string_boolean_ok_is_rejected(self, data_root, repo):
        job = _run(repo)
        _tamper(job, lambda c: c.__setitem__("ok", "false"))
        m = _collect(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert any("invalid finalized-call record" in p for p in m.coverage.problems)
        # never coerced into a valid manifest call
        assert not any(c.ok is True and c.identity.task_id == "T001" for c in m.calls) \
            or len(m.calls) < 2

    def test_string_sequence_is_rejected(self, data_root, repo):
        job = _run(repo)
        _tamper(job, lambda c: c["identity"].__setitem__("sequence", "1"))
        m = _collect(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert any("invalid finalized-call record" in p for p in m.coverage.problems)

    def test_unknown_prepared_input_field_is_rejected(self, data_root, repo):
        job = _run(repo)
        _tamper(job, lambda c: c["prepared_input"].__setitem__(
            "secret_note", "/home/alice SUPERSECRET"))
        m = _collect(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert any("invalid finalized-call record" in p for p in m.coverage.problems)

    def test_unknown_call_field_is_rejected(self, data_root, repo):
        job = _run(repo)
        _tamper(job, lambda c: c.__setitem__("EXTRA", "CANARY"))
        m = _collect(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE

    def test_malformed_fingerprint_is_rejected(self, data_root, repo):
        job = _run(repo)
        _tamper(job, lambda c: c.__setitem__("fingerprint", "x" * 300))
        m = _collect(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE

    def test_a_clean_run_record_collects_completely(self, data_root, repo):
        job = _run(repo)
        m = _collect(job)
        assert m.coverage.status == "complete" and m.calls
