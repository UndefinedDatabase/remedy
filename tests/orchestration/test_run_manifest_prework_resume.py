"""F5 (round 12) — a pre-work Stop on a RESUMED job may carry proven prior tasks.

The ordinary scenario: episode 1 completes T001; a resume is requested; a stop is already pending
before any new work starts. `_collect_calls()` correctly classifies T001 as `prior_episode` — and
the lifecycle validator then rejected the whole manifest, because `stopped/pre_work_stop` permitted
only `not_dispatched`. A normal resume-then-stop could not be published at all.

The matrix now says what actually happens: a pre-work stop on a resumed job carries
`prior_episode` tasks (each proven against the canonical chain) alongside `not_dispatched` ones,
zero current-episode calls, and its stop request.
"""
from __future__ import annotations

import dataclasses
import subprocess

import pytest

from packages.orchestration.pingpong_job import load_job_plan, parse_job_file, run_job
from packages.orchestration.run_manifest import (
    COVERAGE_COMPLETE,
    COVERAGE_INCOMPLETE,
    EXPECT_NOT_DISPATCHED,
    EXPECT_PRIOR_EPISODE,
    MODE_PUBLISHED_REFERENCE,
    PHASE_PRE_WORK_STOP,
    EpisodeInputSnapshotV1,
    build_input_snapshot,
    build_run_manifest,
    validate_run_manifest,
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


_ONE = "# Job: pw\n\n## Task 1\nx\n\nAcceptance:\n- y\n"
_TWO = _ONE + "\n## Task 2\nz\n\nAcceptance:\n- w\n"


def _ran(repo, text=_ONE):
    job = parse_job_file(text, str(repo))
    run_job(job.job_id, builder_provider=_prov(), reviewer_provider=_prov(), repair_rounds=0)
    return load_job_plan(job.job_id)


def _prework_stop_manifest(job, *, episode_id, priors, ordinals, previous):
    """The episode a resume-then-pre-work-stop actually finalizes."""
    job.active_episode_id = episode_id
    snap = build_input_snapshot(job, inspect_target=False, probe_versions=False)
    wrapper = EpisodeInputSnapshotV1(
        snapshot_v=1, episode_id=episode_id, captured_at="2026-07-16T00:00:00+00:00",
        capture_phase=PHASE_PRE_WORK_STOP, status="ok", problems=(), input=snap)
    return build_run_manifest(
        job, status="stopped", episode_id=episode_id,
        created_at="2026-07-16T00:00:00+00:00", episode_snapshot=wrapper,
        owned_episode_id=episode_id, stop_request_id="stop-1",
        prior_episode_ids=tuple(priors), prior_episode_ordinals=ordinals,
        episode_ordinal=len(priors) + 1, previous_episode_id=previous)


# --------------------------------------------------------------------------- the finding


class TestPreWorkStopOnAResumedJob:
    def test_the_reproduced_case(self, data_root, repo):
        """One prior episode, one completed task, a stop before any new work."""
        job = _ran(repo)
        ep1 = job.active_episode_id
        m = _prework_stop_manifest(job, episode_id="ep2", priors=(ep1,),
                                   ordinals={ep1: 1}, previous=ep1)
        assert [t.expectation for t in m.call_expectation.tasks] == [EXPECT_PRIOR_EPISODE]
        assert m.calls == ()
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        assert validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE) == [], \
            "a normal pre-work resume could not be published"

    def test_one_prior_task_and_one_remaining_task(self, data_root, repo):
        from packages.orchestration.pingpong_job import TASK_PENDING, TaskEntry

        job = _ran(repo)
        ep1 = job.active_episode_id
        job.tasks.append(TaskEntry(task_id="T002", source_heading_number=2, title="t2",
                                   body="b", acceptance="a", status=TASK_PENDING))
        m = _prework_stop_manifest(job, episode_id="ep2", priors=(ep1,),
                                   ordinals={ep1: 1}, previous=ep1)
        got = {t.task_id: t.expectation for t in m.call_expectation.tasks}
        assert got == {"T001": EXPECT_PRIOR_EPISODE, "T002": EXPECT_NOT_DISPATCHED}
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems

    def test_multiple_prior_episodes(self, data_root, repo):
        job = _ran(repo)
        ep1 = job.active_episode_id
        m = _prework_stop_manifest(job, episode_id="ep3", priors=(ep1, "ep2"),
                                   ordinals={ep1: 1, "ep2": 2}, previous="ep2")
        assert [t.expectation for t in m.call_expectation.tasks] == [EXPECT_PRIOR_EPISODE]
        assert m.coverage.status == COVERAGE_COMPLETE, m.coverage.problems
        assert validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE) == []

    def test_every_prior_task_names_a_real_prior_episode_and_ledger(self, data_root, repo):
        job = _ran(repo)
        ep1 = job.active_episode_id
        m = _prework_stop_manifest(job, episode_id="ep2", priors=(ep1,),
                                   ordinals={ep1: 1}, previous=ep1)
        te = m.call_expectation.tasks[0]
        assert te.run_id == job.tasks[0].run_id
        assert len(te.finalized_calls_sha256) == 64
        lg = next(x for x in m.call_ledgers if x.task_id == "T001")
        assert te.ledger_ref == lg.ref()
        assert all(e.episode_id == ep1 for e in lg.entries), \
            "a prior task's ledger must name the episode that actually made the calls"

    def test_an_unknown_prior_episode_blocks(self, data_root, repo):
        """"It happened earlier" is a claim, and a claim about an episode nobody has heard of is
        not history."""
        job = _ran(repo)
        m = _prework_stop_manifest(job, episode_id="ep2", priors=("ep-imaginary",),
                                   ordinals={"ep-imaginary": 1}, previous="ep-imaginary")
        assert m.coverage.status == COVERAGE_INCOMPLETE
        assert "not a known episode" in "; ".join(m.coverage.problems)

    def test_no_task_may_be_executed_in_a_pre_work_stop(self, data_root, repo):
        """A pre-work stop did no work by definition — an executed task in one would mean the
        stop did not happen before work."""
        from packages.orchestration.run_manifest import (
            EXPECT_EXECUTED,
            CallExpectationV1,
            TaskCallExpectationV1,
        )
        job = _ran(repo)
        ep1 = job.active_episode_id
        m = _prework_stop_manifest(job, episode_id="ep2", priors=(ep1,),
                                   ordinals={ep1: 1}, previous=ep1)
        forged = dataclasses.replace(m, call_expectation=CallExpectationV1(
            episode_phase=PHASE_PRE_WORK_STOP,
            tasks=(TaskCallExpectationV1(
                task_id="T001", expectation=EXPECT_EXECUTED, run_id="r",
                expected_call_count=1, observed_call_count=0,
                finalized_calls_sha256="a" * 64, ledger_ref="call_ledgers/T001-r.json",
                task_status_at_finalization="applied_to_job_workspace",
                dispatch_state="dispatched_this_episode"),)))
        probs = validate_run_manifest(forged, mode=MODE_PUBLISHED_REFERENCE)
        assert any("cannot happen" in p for p in probs), probs

    def test_an_idempotent_stop_retry_is_stable(self, data_root, repo):
        job = _ran(repo)
        ep1 = job.active_episode_id
        first = _prework_stop_manifest(job, episode_id="ep2", priors=(ep1,),
                                       ordinals={ep1: 1}, previous=ep1)
        second = _prework_stop_manifest(load_job_plan(job.job_id), episode_id="ep2",
                                        priors=(ep1,), ordinals={ep1: 1}, previous=ep1)
        assert first.call_expectation == second.call_expectation
        assert first.call_ledgers == second.call_ledgers
