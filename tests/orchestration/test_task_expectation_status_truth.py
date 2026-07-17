"""F2 (round 16) — ONE closed task-status / expectation truth table.

Round 12 stored BOTH facts on purpose: what this episode expected of a task
(`expectation`) and what the JobPlan recorded about it (`task_status_at_finalization`).
Storing both is what makes a contradiction visible instead of normalized away. But nothing ever
compared them, so a published reference could say:

    expectation = skipped          # "this task was never dispatched"
    task_status_at_finalization = applied_to_job_workspace   # "...it ran and its work landed"

Reproduced: all four of `skipped` + {pending, applied_to_job_workspace, passed, failed} passed
published-reference validation, and a forged `skipped + applied` manifest was written and read
back. Two facts, sealed together, flatly disagreeing, and no boundary asked.

The matrix below is derived from `_collect_calls`'s REAL behaviour — not from taste. Every pair
is enumerated, allowed and forbidden alike, because a truth table nobody enumerates is how the
gap survived twelve rounds.
"""
from __future__ import annotations

import dataclasses
import itertools

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    DISPATCH_NEVER,
    DISPATCH_PRIOR_EPISODE,
    DISPATCH_THIS_EPISODE,
    EXPECT_DISPATCHED_NO_CALLS,
    EXPECT_EXECUTED,
    EXPECT_FAILED_PRE_DISPATCH,
    EXPECT_NOT_DISPATCHED,
    EXPECT_PRIOR_EPISODE,
    EXPECT_SKIPPED,
    MODE_PUBLISHED_REFERENCE,
    VALID_TASK_EXPECTATIONS,
    VALID_TASK_STATUSES,
    CallExpectationV1,
    TaskCallExpectationV1,
    _bind_artifact_refs,
    validate_run_manifest,
    validate_task_expectation_truth,
)

#: The exact allowed pairs. Anything not listed here must be refused.
_ALLOWED = {
    EXPECT_SKIPPED: {"skipped"},
    EXPECT_NOT_DISPATCHED: {"pending"},
    EXPECT_FAILED_PRE_DISPATCH: {"failed", "blocked"},
    EXPECT_EXECUTED: {"passed", "applied_to_job_workspace", "running", "pending",
                      "failed", "blocked"},
    EXPECT_PRIOR_EPISODE: {"passed", "applied_to_job_workspace", "running", "pending",
                           "failed", "blocked"},
    EXPECT_DISPATCHED_NO_CALLS: {"failed", "blocked", "pending", "running"},
}

_NO_RUN = {EXPECT_SKIPPED, EXPECT_NOT_DISPATCHED, EXPECT_FAILED_PRE_DISPATCH}


def _te(expectation, status, **kw):
    """A task record shaped the way production shapes it for that expectation."""
    if expectation in _NO_RUN:
        base = dict(run_id="", finalized_calls_sha256="", ledger_ref="",
                    dispatch_state=DISPATCH_NEVER)
    else:
        base = dict(run_id="rT001", finalized_calls_sha256="a" * 64,
                    ledger_ref="call_ledgers/x.json",
                    dispatch_state=(DISPATCH_PRIOR_EPISODE
                                    if expectation == EXPECT_PRIOR_EPISODE
                                    else DISPATCH_THIS_EPISODE))
    base.update(kw)
    return TaskCallExpectationV1(task_id="T001", expectation=expectation,
                                 task_status_at_finalization=status, **base)


# --------------------------------------------------------------------------- the whole matrix


class TestEveryPairFollowsOneClosedMatrix:
    @pytest.mark.parametrize("expectation,status",
                             sorted(itertools.product(sorted(VALID_TASK_EXPECTATIONS),
                                                      sorted(VALID_TASK_STATUSES))))
    def test_the_exhaustive_matrix(self, expectation, status):
        """All 42 pairs. Allowed ones pass; every other one is refused."""
        probs = validate_task_expectation_truth(_te(expectation, status))
        if status in _ALLOWED[expectation]:
            assert probs == [], f"{expectation} + {status} should be legal: {probs}"
        else:
            assert any("impossible task record" in p for p in probs), \
                f"{expectation} + {status} was accepted"

    def test_the_matrix_covers_every_expectation(self):
        assert set(_ALLOWED) == set(VALID_TASK_EXPECTATIONS)

    def test_no_status_is_silently_normalized(self):
        """The record keeps BOTH facts — a contradiction is reported, never tidied away."""
        te = _te(EXPECT_SKIPPED, "applied_to_job_workspace")
        assert validate_task_expectation_truth(te)
        assert te.expectation == EXPECT_SKIPPED
        assert te.task_status_at_finalization == "applied_to_job_workspace"


# --------------------------------------------------------------------------- the reproduction


class TestTheReproducedForgeries:
    @pytest.mark.parametrize("status", ["pending", "applied_to_job_workspace", "passed",
                                        "failed"])
    def test_skipped_plus_a_worked_status_blocks_in_a_published_reference(self, status):
        """THE finding, end to end through `validate_run_manifest`."""
        base = _bind_artifact_refs(T._mk(calls=()))
        m = dataclasses.replace(base, call_expectation=CallExpectationV1(
            tasks=(_te(EXPECT_SKIPPED, status),)))
        probs = validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE)
        assert any("impossible task record" in p for p in probs), probs

    def test_the_valid_skipped_record_still_passes(self):
        base = _bind_artifact_refs(T._mk(calls=()))
        m = dataclasses.replace(base, call_expectation=CallExpectationV1(
            tasks=(_te(EXPECT_SKIPPED, "skipped"),)))
        assert validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE) == []

    def test_a_forged_skipped_applied_manifest_cannot_be_written(self, tmp_path):
        """Not just the typed validator: the WRITER refuses it too."""
        from packages.orchestration.run_manifest import ManifestError, write_run_manifest

        base = _bind_artifact_refs(T._mk(calls=()))
        m = dataclasses.replace(base, call_expectation=CallExpectationV1(
            tasks=(_te(EXPECT_SKIPPED, "applied_to_job_workspace"),)))
        ev = tmp_path / "ev"
        ev.mkdir()
        with pytest.raises(ManifestError) as exc:
            write_run_manifest(ev, m, root=tmp_path)
        assert "impossible task record" in str(exc.value)


# --------------------------------------------------------------------------- the valid forms


class TestTheFormsProductionEmits:
    def test_a_valid_applied_executed_record_passes(self):
        assert validate_task_expectation_truth(
            _te(EXPECT_EXECUTED, "applied_to_job_workspace")) == []

    def test_a_valid_prior_episode_record_passes(self):
        assert validate_task_expectation_truth(
            _te(EXPECT_PRIOR_EPISODE, "applied_to_job_workspace")) == []

    def test_f011s_mid_flight_stop_is_legal(self):
        """The call in flight finished, so the run holds work while the task waits at pending."""
        assert validate_task_expectation_truth(_te(EXPECT_EXECUTED, "pending")) == []

    def test_a_post_run_gate_failure_is_legal(self):
        """Production reaches blocked/failed AFTER a successful run — completion gate, target
        guard, workspace apply. Forbidding it would refuse real records."""
        assert validate_task_expectation_truth(_te(EXPECT_EXECUTED, "blocked")) == []
        assert validate_task_expectation_truth(_te(EXPECT_EXECUTED, "failed")) == []

    def test_dispatched_no_calls_cannot_be_passed_or_applied(self):
        """Those two are only reachable THROUGH a finalized call."""
        for status in ("passed", "applied_to_job_workspace"):
            assert validate_task_expectation_truth(
                _te(EXPECT_DISPATCHED_NO_CALLS, status))


# --------------------------------------------------------------------------- the other facts


class TestTheRunAndDispatchFactsMustAgreeToo:
    @pytest.mark.parametrize("expectation", sorted(_NO_RUN))
    def test_a_pre_dispatch_expectation_may_not_own_a_run(self, expectation):
        status = sorted(_ALLOWED[expectation])[0]
        probs = validate_task_expectation_truth(_te(expectation, status, run_id="rT001"))
        assert any("decided before dispatch" in p for p in probs), probs

    @pytest.mark.parametrize("expectation", sorted(_NO_RUN))
    def test_a_pre_dispatch_expectation_may_not_seal_a_ledger(self, expectation):
        status = sorted(_ALLOWED[expectation])[0]
        probs = validate_task_expectation_truth(
            _te(expectation, status, ledger_ref="call_ledgers/x.json"))
        assert any("seals a call ledger" in p for p in probs), probs

    @pytest.mark.parametrize("expectation", sorted(_NO_RUN))
    def test_a_pre_dispatch_expectation_must_say_never_dispatched(self, expectation):
        status = sorted(_ALLOWED[expectation])[0]
        probs = validate_task_expectation_truth(
            _te(expectation, status, dispatch_state=DISPATCH_THIS_EPISODE))
        assert any("dispatch state" in p for p in probs), probs

    def test_an_expectation_with_a_run_may_not_say_never_dispatched(self):
        probs = validate_task_expectation_truth(
            _te(EXPECT_EXECUTED, "passed", dispatch_state=DISPATCH_NEVER))
        assert any("never dispatched" in p for p in probs), probs

    def test_prior_episode_may_not_claim_this_episode_dispatched_it(self):
        probs = validate_task_expectation_truth(
            _te(EXPECT_PRIOR_EPISODE, "passed", dispatch_state=DISPATCH_THIS_EPISODE))
        assert any("this episode dispatched it" in p for p in probs), probs

    def test_executed_may_not_claim_a_prior_episode_dispatched_it(self):
        probs = validate_task_expectation_truth(
            _te(EXPECT_EXECUTED, "passed", dispatch_state=DISPATCH_PRIOR_EPISODE))
        assert any("a prior episode dispatched it" in p for p in probs), probs


# --------------------------------------------------------------------------- closed inputs


class TestTheInputsThemselvesAreClosed:
    def test_a_missing_status_cannot_be_checked_and_blocks(self):
        """An absent status is not "unknown, so fine" — it is a record that cannot be verified."""
        probs = validate_task_expectation_truth(_te(EXPECT_SKIPPED, ""))
        assert any("records no task_status_at_finalization" in p for p in probs), probs

    @pytest.mark.parametrize("status", ["applied", "APPLIED_TO_JOB_WORKSPACE", "done",
                                        "../evil", "completed"])
    def test_an_unsupported_status_blocks(self, status):
        probs = validate_task_expectation_truth(_te(EXPECT_EXECUTED, status))
        assert any("unsupported task status" in p for p in probs), probs

    def test_an_unsupported_expectation_blocks(self):
        probs = validate_task_expectation_truth(_te(EXPECT_EXECUTED, "passed").__class__(
            task_id="T001", expectation="invented", task_status_at_finalization="passed"))
        assert any("unsupported expectation" in p for p in probs), probs

    def test_the_status_vocabulary_matches_the_jobplan(self):
        """A6: not a parallel taxonomy — exactly the JobPlan's own TASK_* constants."""
        from packages.orchestration import pingpong_job as PJ

        assert VALID_TASK_STATUSES == {PJ.TASK_PENDING, PJ.TASK_RUNNING, PJ.TASK_PASSED,
                                       PJ.TASK_APPLIED, PJ.TASK_BLOCKED, PJ.TASK_FAILED,
                                       PJ.TASK_SKIPPED}
