"""F1/F2 (round 17) — task truth depends on the EPISODE the record lives in.

The round-16 truth table took `episode_status` and `episode_phase` and never read them, so it
judged every task by one global status set. That set is the STOPPED/worked baseline — the widest
an expectation is ever allowed, because a stop legitimately leaves a run `pending` (F011's
mid-flight call finishes) or `blocked`/`failed` (a post-run gate). A COMPLETED episode is
narrower: `run_job` sets `completed` only when EVERY task is applied or skipped, so an `executed`
or `prior_episode` task in one CANNOT be pending/running/failed/blocked. Reproduced: a fully
artifact-bound completed published reference accepted `executed` + each of those four.

F2 is the cross-episode half: the lifecycle chain froze a completed run's id, ledger ref and
ledger hash — but not the STATUS it finished under. So a later `prior_episode` record could keep
the same run and ledger while rewriting `applied_to_job_workspace` into `failed`. The status a
task completed under is part of what completed.
"""
from __future__ import annotations

import dataclasses
import itertools

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    DISPATCH_PRIOR_EPISODE,
    DISPATCH_THIS_EPISODE,
    EXPECT_EXECUTED,
    EXPECT_PRIOR_EPISODE,
    MODE_PUBLISHED_REFERENCE,
    PHASE_PRE_WORK_STOP,
    PHASE_WORKED,
    CallExpectationV1,
    TaskCallExpectationV1,
    _allowed_statuses_for,
    _bind_artifact_refs,
    validate_run_manifest,
    validate_task_expectation_truth,
    validate_task_lifecycle_chain,
)


def _executed_te(status, **kw):
    base = dict(task_id="T001", expectation=EXPECT_EXECUTED, run_id="rT001",
                expected_call_count=1, observed_call_count=1,
                finalized_calls_sha256="a" * 64, ledger_ref="call_ledgers/x.json",
                task_status_at_finalization=status, dispatch_state=DISPATCH_THIS_EPISODE)
    base.update(kw)
    return TaskCallExpectationV1(**base)


# --------------------------------------------------------------------------- F1: completed


class TestCompletedWorkedIsNarrow:
    def _forge(self, status):
        base = _bind_artifact_refs(T._mk(status="completed", calls=(T._call(),)))
        lg = base.call_ledgers[0]
        te = _executed_te(status, finalized_calls_sha256=lg.sha256(), ledger_ref=lg.ref())
        m = dataclasses.replace(base, call_expectation=CallExpectationV1(
            episode_phase=PHASE_WORKED, tasks=(te,)))
        return validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE)

    @pytest.mark.parametrize("status", ["pending", "running", "failed", "blocked"])
    def test_a_completed_executed_task_with_a_non_terminal_status_blocks(self, status):
        probs = self._forge(status)
        assert any("impossible task record" in p for p in probs), (status, probs)

    @pytest.mark.parametrize("status", ["passed", "applied_to_job_workspace"])
    def test_a_completed_executed_task_that_actually_completed_passes(self, status):
        assert self._forge(status) == []

    def test_the_context_helper_is_tight_for_completed_worked(self):
        for exp in (EXPECT_EXECUTED, EXPECT_PRIOR_EPISODE):
            allowed = _allowed_statuses_for(exp, "completed", PHASE_WORKED)
            assert allowed == {"passed", "applied_to_job_workspace"}

    def test_the_context_helper_stays_permissive_for_stopped_worked(self):
        """A stop can leave any of these — that is F011, and it must not regress."""
        allowed = _allowed_statuses_for(EXPECT_EXECUTED, "stopped", PHASE_WORKED)
        assert {"pending", "failed", "blocked"} <= allowed


class TestStoppedWorkedStaysValid:
    """The permissive states production really produces in a stop must remain legal."""

    def _stopped(self, status, expectation=EXPECT_EXECUTED):
        te = _executed_te(status, expectation=expectation)
        return validate_task_expectation_truth(te, episode_status="stopped",
                                               episode_phase=PHASE_WORKED)

    @pytest.mark.parametrize("status", ["pending", "blocked", "failed", "running",
                                        "passed", "applied_to_job_workspace"])
    def test_a_stopped_executed_task_accepts_the_f011_states(self, status):
        assert self._stopped(status) == []


class TestEveryPairPerContext:
    """Allowed pairs are decided per (episode_status, episode_phase), not globally."""

    @pytest.mark.parametrize("episode_status,phase", [
        ("completed", PHASE_WORKED), ("stopped", PHASE_WORKED),
    ])
    @pytest.mark.parametrize("status", ["pending", "running", "passed",
                                        "applied_to_job_workspace", "blocked", "failed"])
    def test_executed_status_matrix(self, episode_status, phase, status):
        te = _executed_te(status)
        probs = validate_task_expectation_truth(te, episode_status=episode_status,
                                                episode_phase=phase)
        allowed = _allowed_statuses_for(EXPECT_EXECUTED, episode_status, phase)
        assert (probs == []) == (status in allowed), (episode_status, status, probs)


# --------------------------------------------------------------------------- F2: prior status


class TestAPriorEpisodeCannotRewriteStatus:
    def _chain(self, later_status):
        ep1 = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(),)))
        lg = ep1.call_ledgers[0]
        te1 = _executed_te("applied_to_job_workspace",
                           finalized_calls_sha256=lg.sha256(), ledger_ref=lg.ref())
        ep1 = dataclasses.replace(ep1, call_expectation=CallExpectationV1(tasks=(te1,)))
        ep2 = dataclasses.replace(
            _bind_artifact_refs(T._mk(episode_id="ep2", calls=())),
            prior_episode_ids=("ep1",), previous_episode_id="ep1", episode_ordinal=2)
        te2 = dataclasses.replace(te1, expectation=EXPECT_PRIOR_EPISODE,
                                  dispatch_state=DISPATCH_PRIOR_EPISODE,
                                  task_status_at_finalization=later_status)
        ep2 = dataclasses.replace(ep2, call_expectation=CallExpectationV1(tasks=(te2,)))
        return validate_task_lifecycle_chain([ep1, ep2])

    @pytest.mark.parametrize("status", ["pending", "running", "failed", "blocked"])
    def test_a_prior_applied_task_cannot_become_non_terminal(self, status):
        probs = self._chain(status)
        assert any("terminal status is frozen" in p for p in probs), (status, probs)

    def test_exact_status_repetition_passes(self):
        assert self._chain("applied_to_job_workspace") == []

    def test_the_run_and_ledger_are_still_frozen_too(self):
        """F2 adds to the round-15 rule, it does not replace it: run/ledger stay bound."""
        ep1 = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(),)))
        lg = ep1.call_ledgers[0]
        te1 = _executed_te("applied_to_job_workspace",
                           finalized_calls_sha256=lg.sha256(), ledger_ref=lg.ref())
        ep1 = dataclasses.replace(ep1, call_expectation=CallExpectationV1(tasks=(te1,)))
        ep2 = dataclasses.replace(
            _bind_artifact_refs(T._mk(episode_id="ep2", calls=())),
            prior_episode_ids=("ep1",), previous_episode_id="ep1", episode_ordinal=2)
        # same status, but a rewritten run id
        te2 = dataclasses.replace(te1, expectation=EXPECT_PRIOR_EPISODE,
                                  dispatch_state=DISPATCH_PRIOR_EPISODE, run_id="rOTHER")
        ep2 = dataclasses.replace(ep2, call_expectation=CallExpectationV1(tasks=(te2,)))
        assert validate_task_lifecycle_chain([ep1, ep2])
