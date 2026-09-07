"""F5 (round 10) — only a KNOWN prior episode may excuse a call from this episode's manifest.

A resume legitimately publishes none of an earlier episode's calls. But "this call says it
belongs to another episode" is a claim the call makes about itself, and before round 10 the
collector simply believed it: any unrecognised episode id made the call disappear, and the
manifest then reported COMPLETE coverage over the remainder. Evidence that vanishes because it
named something nobody has heard of is the opposite of coverage.

Exclusion now requires proof against the canonical chain:
  * the episode EXISTS in the chain;
  * its ordinal is strictly lower than this episode's;
  * it appears in THIS episode's exact `prior_episode_ids`;
  * the call's remaining job/task/run lineage is valid.

Anything else is a blocking coverage problem. And an excluded prior call still occupies its
position in its RUN's sequence, because the run counted it.
"""
from __future__ import annotations

import json
import subprocess

import pytest

from packages.orchestration.pingpong_job import load_job_plan, parse_job_file, run_job
from packages.orchestration.run_manifest import (
    COVERAGE_COMPLETE,
    COVERAGE_INCOMPLETE,
    EXPECT_PRIOR_EPISODE,
    EpisodeInputSnapshotV1,
    build_input_snapshot,
    build_run_manifest,
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


def _job(repo):
    job = parse_job_file("# Job: mem\n\n## Task 1\nx\n\nAcceptance:\n- y\n", str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    return load_job_plan(job.job_id)


def _run_path(job):
    from packages.orchestration.data_paths import run_dir
    return run_dir(job.tasks[0].run_id) / "result.json"


def _set_episode(job, index, episode_id):
    p = _run_path(job)
    d = json.loads(p.read_text())
    d["finalized_calls"][index]["identity"]["episode_id"] = episode_id
    p.write_text(json.dumps(d))
    return len(d["finalized_calls"])


def _collect(job, **chain):
    snap = build_input_snapshot(job, inspect_target=False, probe_versions=False)
    wrapper = EpisodeInputSnapshotV1(
        snapshot_v=1, episode_id=job.active_episode_id,
        captured_at="2026-07-16T00:00:00+00:00", capture_phase="episode_start",
        status="ok", problems=(), input=snap)
    return build_run_manifest(job, status="completed", episode_id=job.active_episode_id,
                              created_at="2026-07-16T00:00:00+00:00",
                              episode_snapshot=wrapper,
                              owned_episode_id=job.active_episode_id, **chain)


#: This episode is ordinal 2 and legitimately follows `ep-1`.
_CHAIN = dict(prior_episode_ordinals={"ep-1": 1}, prior_episode_ids=("ep-1",),
              episode_ordinal=2)


# --------------------------------------------------------------------------- unknown episodes


class TestUnprovableMembershipIsBlocking:
    def test_an_unknown_episode_is_reported(self, data_root, repo):
        """THE finding: the call was excluded and coverage said complete."""
        job = _job(repo)
        _set_episode(job, -1, "EPISODE-NOBODY-HAS-HEARD-OF")
        m = _collect(job, **_CHAIN)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "not a known episode" in "; ".join(m.coverage.problems)

    def test_an_unknown_episode_with_no_chain_at_all_is_reported(self, data_root, repo):
        """The first episode has no priors, so NOTHING can be excused as history."""
        job = _job(repo)
        _set_episode(job, -1, "ep-imaginary")
        m = _collect(job)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "not a known episode" in "; ".join(m.coverage.problems)

    def test_a_future_ordinal_episode_is_reported(self, data_root, repo):
        """A call from an episode that comes after this one cannot be this one's history."""
        job = _job(repo)
        _set_episode(job, -1, "ep-future")
        m = _collect(job, prior_episode_ordinals={"ep-future": 7},
                     prior_episode_ids=("ep-future",), episode_ordinal=2)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "not strictly earlier" in "; ".join(m.coverage.problems)

    def test_an_equal_ordinal_episode_is_reported(self, data_root, repo):
        job = _job(repo)
        _set_episode(job, -1, "ep-sibling")
        m = _collect(job, prior_episode_ordinals={"ep-sibling": 2},
                     prior_episode_ids=("ep-sibling",), episode_ordinal=2)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "not strictly earlier" in "; ".join(m.coverage.problems)

    def test_a_known_earlier_episode_that_is_not_listed_as_a_prior_is_reported(
            self, data_root, repo):
        """Known and earlier is not enough — it must be in THIS episode's exact history."""
        job = _job(repo)
        _set_episode(job, -1, "ep-unlisted")
        m = _collect(job, prior_episode_ordinals={"ep-unlisted": 1}, prior_episode_ids=(),
                     episode_ordinal=2)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "does not list among its priors" in "; ".join(m.coverage.problems)

    def test_an_empty_episode_id_is_reported(self, data_root, repo):
        job = _job(repo)
        _set_episode(job, -1, "")
        m = _collect(job, **_CHAIN)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "empty episode_id" in "; ".join(m.coverage.problems)

    def test_a_malformed_call_is_not_laundered_by_a_valid_prior_episode(
            self, data_root, repo):
        """Lineage is verified BEFORE membership, so "it belongs to an earlier episode" can
        never become a way to smuggle a broken record past the collector."""
        job = _job(repo)
        p = _run_path(job)
        d = json.loads(p.read_text())
        d["finalized_calls"][-1]["identity"]["episode_id"] = "ep-1"    # a REAL prior
        d["finalized_calls"][-1]["identity"]["job_id"] = "someone-elses-job"
        p.write_text(json.dumps(d))
        m = _collect(job, **_CHAIN)
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "job_id" in "; ".join(m.coverage.problems)


# --------------------------------------------------------------------------- valid history


class TestProvenPriorEpisodeCallsAreExcluded:
    def test_a_known_listed_earlier_episode_call_is_excluded(self, data_root, repo):
        job = _job(repo)
        n = _set_episode(job, 0, "ep-1")
        m = _collect(job, **_CHAIN)
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        assert len(m.calls) == n - 1
        assert all(c.identity.episode_id == job.active_episode_id for c in m.calls)

    def test_an_excluded_call_is_never_restamped(self, data_root, repo):
        job = _job(repo)
        _set_episode(job, 0, "ep-1")
        m = _collect(job, **_CHAIN)
        assert "ep-1" not in json.dumps([c.to_json() for c in m.calls])
        # the persisted record is untouched — collection never writes back
        d = json.loads(_run_path(job).read_text())
        assert d["finalized_calls"][0]["identity"]["episode_id"] == "ep-1"

    def test_an_excluded_prior_call_still_counts_toward_the_run_sequence(
            self, data_root, repo):
        """The stored sequence is per-RUN and counts every call the run made, across episodes.
        If exclusion rewound the counter, the surviving calls would look mis-sequenced."""
        job = _job(repo)
        n = _set_episode(job, 0, "ep-1")          # the run's position 1 belongs to ep-1
        assert n >= 2
        m = _collect(job, **_CHAIN)
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        # position 2 still verifies at its stored in-run position and is published
        assert len(m.calls) == n - 1

    def test_a_task_whose_work_was_all_prior_is_recorded_as_prior_episode(
            self, data_root, repo):
        """Zero calls HERE, and the record says why — the work happened earlier."""
        job = _job(repo)
        p = _run_path(job)
        d = json.loads(p.read_text())
        for c in d["finalized_calls"]:
            c["identity"]["episode_id"] = "ep-1"
        p.write_text(json.dumps(d))
        m = _collect(job, **_CHAIN)
        assert m.calls == ()
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        assert [t.expectation for t in m.call_expectation.tasks] == [EXPECT_PRIOR_EPISODE]
        assert m.call_expectation.expects_zero_calls()
