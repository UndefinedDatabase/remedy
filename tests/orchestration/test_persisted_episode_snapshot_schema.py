"""F5/F10 — persisted JobPlan episode snapshots are untrusted disk state."""
from __future__ import annotations

import subprocess

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.manifest_schema import SchemaError
from packages.orchestration.pingpong_job import (
    _episode_snapshot_bound_ok,
    load_job_plan,
    parse_job_file,
    run_job,
)
from packages.orchestration.run_manifest import decode_episode_snapshot_v1


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


class TestStrictSnapshotDecoding:
    @pytest.mark.parametrize("label,mutate", [
        ("string boolean", lambda d: d["input"].__setitem__("remedy_dirty", "false")),
        ("string integer", lambda d: d.__setitem__("snapshot_v", "1")),
        ("unknown wrapper field", lambda d: d.__setitem__("EXTRA", "CANARY")),
        ("unknown input field",
         lambda d: d["input"].__setitem__("EXTRA_SECRET", "CANARY-/home/alice")),
        ("unknown worktree field",
         lambda d: d["input"]["remedy_worktree"].__setitem__("X", "/home/alice")),
    ])
    def test_malformed_persisted_snapshot_is_rejected(self, label, mutate):
        d = T._wrap(episode_id="ep").to_json()
        mutate(d)
        with pytest.raises(SchemaError):
            decode_episode_snapshot_v1(d)


class TestBoundOkUsesTheStrictDecoder:
    def test_malformed_persisted_snapshot_is_never_bound_ok(self, data_root, repo):
        from packages.orchestration.pingpong_job import _persist_job
        job = parse_job_file("# Job: s\n\n## Task 1\nx\n\nAcceptance:\n- y\n", str(repo))
        run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(),
                repair_rounds=0)
        reloaded = load_job_plan(job.job_id)
        # a clean persisted snapshot IS bound-ok
        assert _episode_snapshot_bound_ok(reloaded) is True
        # tamper the persisted snapshot: a string boolean must never coerce to bound-ok
        reloaded.input_snapshot["input"]["remedy_dirty"] = "false"
        _persist_job(reloaded)
        again = load_job_plan(job.job_id)
        assert _episode_snapshot_bound_ok(again) is False

    def test_foreign_episode_snapshot_is_not_bound_ok(self, data_root, repo):
        from packages.orchestration.pingpong_job import _persist_job
        job = parse_job_file("# Job: s2\n\n## Task 1\nx\n\nAcceptance:\n- y\n", str(repo))
        run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(),
                repair_rounds=0)
        reloaded = load_job_plan(job.job_id)
        reloaded.input_snapshot["episode_id"] = "someoneelse"
        _persist_job(reloaded)
        assert _episode_snapshot_bound_ok(load_job_plan(job.job_id)) is False


class TestFullValidityPredicate:
    def test_is_ok_validates_the_nested_input(self):
        # F10: a wrapper whose SHAPE is fine but whose nested snapshot carries a raw secret
        # is NOT ok — the wrapper-only predicate is not a trust decision.
        bad = T._snap(config=[{"key": "api_token", "value": "sk-ant-SUPERSECRETKEY123456",
                               "source": "env"}])
        w = T._wrap(bad, episode_id="ep")
        assert w.wrapper_shape_is_valid() is True
        assert w.is_ok() is False

    def test_is_ok_true_for_a_clean_snapshot(self):
        assert T._wrap(episode_id="ep").is_ok() is True
