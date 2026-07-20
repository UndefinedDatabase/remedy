"""F7/F8/F9 (round 11) — the CallExpectation lifecycle matrix is exact and closed.

A record saying "this run completed" and "this task was never dispatched" is not a record of
anything that happened — the product cannot produce it. `run_job` sets `completed` only when
EVERY task is applied or skipped (a max-tasks boundary PAUSES the job instead, and a paused job
is not a finished run and gets no manifest). A stop is different by design (F011: "the call in
flight finishes, nothing new starts"), so a stopped episode legitimately carries undispatched
tasks and tasks that died before their first call.

Before round 11 all of these validated cleanly:

    completed + planning_only
    stopped + planning_only with an ordinary episode_start snapshot
    planned + worked
    completed + dispatched_no_calls
    completed + not_dispatched
    snapshot pre_work_stop + expectation worked

The matrix below is derived from the committed contract and refuses every one of them.
"""
from __future__ import annotations

import dataclasses
import hashlib

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    EXPECT_DISPATCHED_NO_CALLS,
    EXPECT_EXECUTED,
    EXPECT_NOT_DISPATCHED,
    EXPECT_PRIOR_EPISODE,
    EXPECT_SKIPPED,
    MODE_PUBLISHED_REFERENCE,
    PHASE_EPISODE_START,
    PHASE_PLANNING_ONLY,
    PHASE_PRE_WORK_STOP,
    PHASE_WORKED,
    CallExpectationV1,
    TaskCallExpectationV1,
    canonical_artifact_ref,
    validate_run_manifest,
)

_SEAL = "a" * 64


def _bind(m):
    bound = []
    for c in m.calls:
        c = dataclasses.replace(c, artifact=canonical_artifact_ref(c.identity))
        bound.append(dataclasses.replace(
            c, artifact_sha256=hashlib.sha256(c.canonical_artifact_bytes()).hexdigest()))
    return dataclasses.replace(m, calls=tuple(bound))


#: F4/F1 (round 12): the expectation now also records the persisted lifecycle facts and names
#: the canonical ledger, so the fixture must supply a coherent set.
_WITH_RUN = {"executed", "prior_episode", "dispatched_no_calls"}


#: F2 (round 16): the task status each expectation actually comes with, as `_collect_calls`
#: produces it. The fixture used to hardcode `applied_to_job_workspace` for EVERY expectation, so
#: it asserted that `skipped`+applied and `not_dispatched`+applied were valid published records —
#: the precise contradiction the round-16 truth table refuses. The fixture encoded the bug.
_STATUS_FOR_EXPECTATION = {
    "skipped": "skipped",
    "not_dispatched": "pending",
    "failed_pre_dispatch": "failed",
    "dispatched_no_calls": "failed",
    "executed": "applied_to_job_workspace",
    "prior_episode": "applied_to_job_workspace",
}


def _manifest(*, status, capture, phase, task_expectation, calls=(), stop="",
              run_id="", seal="", expected=0, observed=0, dispatch=None, ledger_ref=None,
              task_status=None):
    from packages.orchestration.run_manifest import (
        DISPATCH_NEVER, DISPATCH_PRIOR_EPISODE, DISPATCH_THIS_EPISODE,
    )
    snap = T._snap()
    wrapper = T._wrap(snap, episode_id="ep1", phase=capture)
    m = _bind(T._mk(episode_id="ep1", status=status, calls=calls))
    if dispatch is None:
        if task_expectation == "prior_episode":
            dispatch = DISPATCH_PRIOR_EPISODE
        elif task_expectation in _WITH_RUN:
            dispatch = DISPATCH_THIS_EPISODE
        else:
            dispatch = DISPATCH_NEVER
    if ledger_ref is None:
        ledger_ref = f"call_ledgers/T001-{run_id}.json" if (run_id and seal) else ""
    return dataclasses.replace(
        m, episode_snapshot=wrapper, stop_request_id=stop,
        call_expectation=CallExpectationV1(
            episode_phase=phase,
            tasks=(TaskCallExpectationV1(
                task_id="T001", expectation=task_expectation, run_id=run_id,
                expected_call_count=expected, observed_call_count=observed,
                finalized_calls_sha256=seal, ledger_ref=ledger_ref,
                task_status_at_finalization=(
                    task_status if task_status is not None
                    else _STATUS_FOR_EXPECTATION.get(task_expectation,
                                                     "applied_to_job_workspace")),
                dispatch_state=dispatch),)))


def _problems(**kw):
    return validate_run_manifest(_manifest(**kw), mode=MODE_PUBLISHED_REFERENCE)


# --------------------------------------------------------------------------- impossible


class TestImpossibleLifecyclesAreRefused:
    def test_completed_plus_planning_only(self):
        probs = _problems(status="completed", capture=PHASE_EPISODE_START,
                          phase=PHASE_PLANNING_ONLY, task_expectation=EXPECT_NOT_DISPATCHED)
        assert any("impossible lifecycle" in p for p in probs), probs

    def test_planned_plus_worked(self):
        probs = _problems(status="planned", capture=PHASE_EPISODE_START, phase=PHASE_WORKED,
                          task_expectation=EXPECT_NOT_DISPATCHED)
        assert any("impossible lifecycle" in p for p in probs), probs

    def test_stopped_plus_planning_only(self):
        probs = _problems(status="stopped", capture=PHASE_EPISODE_START,
                          phase=PHASE_PLANNING_ONLY, task_expectation=EXPECT_NOT_DISPATCHED,
                          stop="s1")
        assert any("impossible lifecycle" in p for p in probs), probs

    def test_completed_plus_dispatched_no_calls(self):
        """A completed job has every task applied or skipped — a task that died before its
        first call means the job did not complete."""
        probs = _problems(status="completed", capture=PHASE_EPISODE_START, phase=PHASE_WORKED,
                          task_expectation=EXPECT_DISPATCHED_NO_CALLS, run_id="r", seal=_SEAL)
        assert any("cannot happen" in p for p in probs), probs

    def test_completed_plus_not_dispatched(self):
        probs = _problems(status="completed", capture=PHASE_EPISODE_START, phase=PHASE_WORKED,
                          task_expectation=EXPECT_NOT_DISPATCHED)
        assert any("cannot happen" in p for p in probs), probs

    def test_a_pre_work_stop_snapshot_with_a_worked_expectation(self):
        probs = _problems(status="stopped", capture=PHASE_PRE_WORK_STOP, phase=PHASE_WORKED,
                          task_expectation=EXPECT_SKIPPED, stop="s1")
        assert any("requires the snapshot capture phase" in p for p in probs), probs

    def test_a_worked_snapshot_with_a_pre_work_stop_expectation(self):
        probs = _problems(status="stopped", capture=PHASE_EPISODE_START,
                          phase=PHASE_PRE_WORK_STOP, task_expectation=EXPECT_NOT_DISPATCHED,
                          stop="s1")
        assert any("requires the snapshot capture phase" in p for p in probs), probs

    def test_a_pre_work_stop_without_a_stop_request(self):
        probs = _problems(status="stopped", capture=PHASE_PRE_WORK_STOP,
                          phase=PHASE_PRE_WORK_STOP, task_expectation=EXPECT_NOT_DISPATCHED)
        assert any("stop request id" in p for p in probs), probs

    def test_a_planning_only_episode_with_a_stop_request(self):
        probs = _problems(status="planned", capture=PHASE_PLANNING_ONLY,
                          phase=PHASE_PLANNING_ONLY, task_expectation=EXPECT_NOT_DISPATCHED,
                          stop="s1")
        assert any("stop request id" in p for p in probs), probs

    def test_a_planning_only_episode_with_calls(self):
        probs = _problems(status="planned", capture=PHASE_PLANNING_ONLY,
                          phase=PHASE_PLANNING_ONLY, task_expectation=EXPECT_EXECUTED,
                          calls=(T._call(),), run_id="rT001", seal=_SEAL, expected=1,
                          observed=1)
        assert any("must record zero calls" in p for p in probs), probs

    def test_a_planning_only_episode_with_an_executed_task(self):
        probs = _problems(status="planned", capture=PHASE_PLANNING_ONLY,
                          phase=PHASE_PLANNING_ONLY, task_expectation=EXPECT_SKIPPED)
        assert any("cannot happen" in p for p in probs), probs


# --------------------------------------------------------------------------- the exact forms


class TestOnlyTheExactFormsPass:
    def test_the_planning_only_form(self):
        assert _problems(status="planned", capture=PHASE_PLANNING_ONLY,
                         phase=PHASE_PLANNING_ONLY,
                         task_expectation=EXPECT_NOT_DISPATCHED) == []

    def test_the_pre_work_stop_form(self):
        assert _problems(status="stopped", capture=PHASE_PRE_WORK_STOP,
                         phase=PHASE_PRE_WORK_STOP,
                         task_expectation=EXPECT_NOT_DISPATCHED, stop="s1") == []

    def test_the_completed_worked_form(self):
        """The real fixture ledger is what the expectation must seal (F1, round 12)."""
        m = _bind(T._mk(episode_id="ep1"))
        assert validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE) == []

    def test_the_completed_all_skipped_form(self):
        assert _problems(status="completed", capture=PHASE_EPISODE_START, phase=PHASE_WORKED,
                         task_expectation=EXPECT_SKIPPED) == []

    @pytest.mark.parametrize("expectation,run_id,seal", [
        (EXPECT_SKIPPED, "", ""),
        (EXPECT_NOT_DISPATCHED, "", ""),
    ])
    def test_the_stopped_worked_states(self, expectation, run_id, seal):
        """A stop can leave any of these behind — and only a stop can."""
        assert _problems(status="stopped", capture=PHASE_EPISODE_START, phase=PHASE_WORKED,
                         task_expectation=expectation, stop="s1", run_id=run_id,
                         seal=seal) == []

    def test_a_stopped_worked_episode_accepts_a_failed_pre_dispatch_task(self):
        """F4 (round 12): failed/blocked BEFORE dispatch is its own truth — no run, no ledger."""
        from packages.orchestration.run_manifest import EXPECT_FAILED_PRE_DISPATCH
        assert _problems(status="stopped", capture=PHASE_EPISODE_START, phase=PHASE_WORKED,
                         task_expectation=EXPECT_FAILED_PRE_DISPATCH, stop="s1") == []


# --------------------------------------------------------------------------- F8 + F9


class TestExpectationTasksMatchTheEmbeddedJobInput:
    def _m(self, tasks, *, job_input=None, calls=()):
        snap = T._snap(job_input=job_input) if job_input else T._snap()
        m = _bind(T._mk(episode_id="ep1", snap=snap, calls=calls))
        return dataclasses.replace(m, call_expectation=CallExpectationV1(
            episode_phase=PHASE_WORKED, tasks=tasks))

    def test_a_ghost_task_blocks(self):
        m = self._m((TaskCallExpectationV1(task_id="GHOST", expectation=EXPECT_SKIPPED),))
        assert any("not exactly the embedded" in p
                   for p in validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE))

    def test_a_ghost_task_blocks_even_when_the_definition_declares_none(self):
        ji = {**T._job_input(), "tasks": []}
        m = self._m((TaskCallExpectationV1(task_id="GHOST", expectation=EXPECT_SKIPPED),),
                    job_input=ji)
        assert any("not exactly the embedded" in p
                   for p in validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE))

    def test_a_missing_task_blocks(self):
        m = self._m(())
        assert any("not exactly the embedded" in p
                   for p in validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE))

    def test_a_duplicated_task_blocks(self):
        m = self._m((TaskCallExpectationV1(task_id="T001", expectation=EXPECT_SKIPPED),
                     TaskCallExpectationV1(task_id="T001", expectation=EXPECT_SKIPPED)))
        assert any("more than once" in p
                   for p in validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE))


class TestRunIdAndCountBinding:
    def test_a_wrong_run_id_blocks(self):
        """THE finding: expectation.run_id = WRONG while the call's run_id was real."""
        probs = _problems(status="completed", capture=PHASE_EPISODE_START, phase=PHASE_WORKED,
                          task_expectation=EXPECT_EXECUTED, calls=(T._call(),),
                          run_id="WRONG-RUN", seal=_SEAL, expected=1, observed=1)
        assert any("were recorded under" in p for p in probs), probs

    def test_an_executed_task_must_name_a_run(self):
        probs = _problems(status="completed", capture=PHASE_EPISODE_START, phase=PHASE_WORKED,
                          task_expectation=EXPECT_EXECUTED, calls=(T._call(),),
                          run_id="", seal=_SEAL, expected=1, observed=1)
        assert any("names no run id" in p for p in probs), probs

    def test_an_executed_task_must_seal_its_ledger(self):
        probs = _problems(status="completed", capture=PHASE_EPISODE_START, phase=PHASE_WORKED,
                          task_expectation=EXPECT_EXECUTED, calls=(T._call(),),
                          run_id="rT001", seal="", expected=1, observed=1)
        assert any("ledger seal" in p for p in probs), probs

    def test_a_skipped_task_must_not_name_a_run(self):
        """F4 (round 12): a task cannot be both never dispatched and the owner of a run."""
        probs = _problems(status="completed", capture=PHASE_EPISODE_START, phase=PHASE_WORKED,
                          task_expectation=EXPECT_SKIPPED, run_id="r")
        assert any("never dispatched and the owner of a run" in p for p in probs), probs

    def test_an_inexact_expected_count_blocks(self):
        """"At least N" plus "N found" can only ever agree with itself."""
        probs = _problems(status="completed", capture=PHASE_EPISODE_START, phase=PHASE_WORKED,
                          task_expectation=EXPECT_EXECUTED, calls=(T._call(),),
                          run_id="rT001", seal=_SEAL, expected=2, observed=1)
        assert any("expected exactly 2" in p for p in probs), probs

    def test_an_inexact_observed_count_blocks(self):
        probs = _problems(status="completed", capture=PHASE_EPISODE_START, phase=PHASE_WORKED,
                          task_expectation=EXPECT_EXECUTED, calls=(T._call(),),
                          run_id="rT001", seal=_SEAL, expected=1, observed=5)
        assert any("records 5 observed" in p for p in probs), probs


# --------------------------------------------------------------------------- production


class TestProductionProducesOnlyValidLifecycles:
    def test_a_real_completed_run(self, data_root, repo):
        from packages.orchestration.pingpong_job import job_evidence_dir
        from packages.orchestration.run_manifest import load_latest_manifest_verified

        job_id, _res = T._run(T._JOB, repo)
        ref = load_latest_manifest_verified(job_evidence_dir(job_id), job_id=job_id)
        assert ref.status == "completed"
        assert ref.call_expectation.episode_phase == PHASE_WORKED
        assert ref.episode_snapshot.capture_phase == PHASE_EPISODE_START
        assert [t.expectation for t in ref.call_expectation.tasks] == [EXPECT_EXECUTED]
        assert validate_run_manifest(ref, mode=MODE_PUBLISHED_REFERENCE) == []

    def test_a_real_pre_work_stop(self, data_root, repo):
        from packages.orchestration.pingpong_job import (
            job_evidence_dir, parse_job_file, run_job,
        )
        from packages.orchestration.run_manifest import load_latest_manifest_verified
        from packages.orchestration.safe_points import request_stop

        job = parse_job_file(T._JOB, str(repo))
        request_stop(job.job_id, "operator requested stop", "test")
        run_job(job.job_id, builder_provider=T._prov(), reviewer_provider=T._prov(),
                repair_rounds=0)
        ref = load_latest_manifest_verified(job_evidence_dir(job.job_id), job_id=job.job_id)
        assert ref.status == "stopped"
        assert ref.episode_snapshot.capture_phase == PHASE_PRE_WORK_STOP
        assert ref.call_expectation.episode_phase == PHASE_PRE_WORK_STOP
        assert ref.stop_request_id
        assert validate_run_manifest(ref, mode=MODE_PUBLISHED_REFERENCE) == []


data_root = T.data_root
repo = T.repo
