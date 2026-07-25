"""F2/F5 (round 14) — the Ledger SET is exactly what the record accounts for.

Every individual ledger could be perfectly formed while the SET carried a passenger. Reproduced:
adding

    task_id=GHOST, run_id=ghostrun, terminal_state=completed, complete=true, entries=[]

to an otherwise valid Manifest was accepted by `validate_run_manifest`, `write_run_manifest`, the
canonical loader AND the verified tree. The GHOST task appeared in no embedded
JobInputDefinition, no CallExpectation and no Manifest Call. Nothing asked what it was doing
there, because every check walked FROM the ledgers OUTWARD ("is this ledger's expectation ok?")
instead of asking whether the ledgers were exactly the ones the record explains.

The contract is set equality in BOTH directions:

    expected_ledger_keys = {(task_id, run_id) for each CallExpectation task owning a run}
    actual_ledger_keys  == expected_ledger_keys
"""
from __future__ import annotations

import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    DISPATCH_THIS_EPISODE,
    EXPECT_EXECUTED,
    MODE_PUBLISHED_REFERENCE,
    CallExpectationV1,
    ManifestError,
    RunCallLedgerV1,
    TaskCallExpectationV1,
    _bind_artifact_refs,
    load_latest_manifest_verified,
    validate_index_and_tree,
    validate_ledger_set,
    validate_run_manifest,
    write_run_manifest,
)


@pytest.fixture
def base():
    return _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(seq=1),)))


def _probs(m):
    return validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE)


def _ghost(task_id="GHOST", run_id="ghostrun"):
    return RunCallLedgerV1(job_id="j", task_id=task_id, run_id=run_id,
                           terminal_state="completed", complete=True, entries=())


# --------------------------------------------------------------------------- the reproduction


class TestAGhostLedgerBlocks:
    def test_the_reproduced_case(self, base):
        assert _probs(base) == []
        forged = dataclasses.replace(base, call_ledgers=base.call_ledgers + (_ghost(),))
        probs = _probs(forged)
        assert probs, "a ghost ledger was accepted"
        assert any("accounted for by no call_expectation" in p for p in probs), probs

    def test_the_writer_refuses_a_ghost_ledger(self, base, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        forged = dataclasses.replace(base, call_ledgers=base.call_ledgers + (_ghost(),))
        with pytest.raises(ManifestError):
            write_run_manifest(ev, forged, root=tmp_path)

    def test_a_ledger_for_an_undeclared_job_input_task_blocks(self, base):
        """The task must be in the immutable embedded definition — the record of what this
        episode was actually given."""
        lg = base.call_ledgers[0]
        te = base.call_expectation.tasks[0]
        undeclared = dataclasses.replace(lg, task_id="T999", run_id="r999")
        forged = dataclasses.replace(
            base, call_ledgers=base.call_ledgers + (undeclared,),
            call_expectation=CallExpectationV1(tasks=te.__class__ and (
                te, TaskCallExpectationV1(
                    task_id="T999", expectation=EXPECT_EXECUTED, run_id="r999",
                    expected_call_count=0, observed_call_count=0,
                    finalized_calls_sha256=undeclared.sha256(), ledger_ref=undeclared.ref(),
                    task_status_at_finalization="applied_to_job_workspace",
                    dispatch_state=DISPATCH_THIS_EPISODE))))
        probs = _probs(forged)
        assert any("declared 0 time(s) in the embedded job input definition" in p
                   for p in probs), probs


class TestSetEqualityInBothDirections:
    def test_an_unreferenced_extra_zero_entry_ledger_blocks(self, base):
        extra = _ghost(task_id="T001", run_id="r-unreferenced")
        forged = dataclasses.replace(base, call_ledgers=base.call_ledgers + (extra,))
        assert any("accounted for by no call_expectation" in p for p in _probs(forged))

    def test_a_missing_expected_ledger_blocks(self, base):
        forged = dataclasses.replace(base, call_ledgers=())
        probs = _probs(forged)
        assert any("carries no ledger for it" in p or "no such ledger" in p for p in probs), probs

    def test_a_duplicate_ledger_key_blocks(self, base):
        lg = base.call_ledgers[0]
        forged = dataclasses.replace(base, call_ledgers=(lg, lg))
        assert any("two call ledgers for" in p for p in _probs(forged))

    def test_the_exact_matching_sets_pass(self, base):
        expected = {(t.task_id, t.run_id) for t in base.call_expectation.tasks if t.run_id}
        actual = {(lg.task_id, lg.run_id) for lg in base.call_ledgers}
        assert expected == actual
        assert validate_ledger_set(base) == []
        assert _probs(base) == []


class TestTheLifecycleStatesThatLegitimatelyOwnLedgers:
    def test_a_dispatched_no_calls_ledger_passes(self, base):
        """A run that existed and finalized nothing is a real state — it owns a sealed
        zero-entry ledger, and the set contract must not refuse it."""
        from packages.orchestration.run_manifest import EXPECT_DISPATCHED_NO_CALLS
        lg = base.call_ledgers[0]
        empty = dataclasses.replace(lg, entries=())
        m = dataclasses.replace(
            base, calls=(), call_ledgers=(empty,),
            call_expectation=CallExpectationV1(tasks=(TaskCallExpectationV1(
                task_id=lg.task_id, expectation=EXPECT_DISPATCHED_NO_CALLS, run_id=lg.run_id,
                finalized_calls_sha256=empty.sha256(), ledger_ref=empty.ref(),
                task_status_at_finalization="failed",
                dispatch_state=DISPATCH_THIS_EPISODE),)))
        assert validate_ledger_set(m) == []

    def test_a_prior_episode_expectation_ledger_passes(self, base):
        from packages.orchestration.run_manifest import (
            DISPATCH_PRIOR_EPISODE,
            EXPECT_PRIOR_EPISODE,
        )
        lg = base.call_ledgers[0]
        m = dataclasses.replace(
            base, episode_id="ep2", calls=(), call_ledgers=(lg,),
            prior_episode_ids=("ep1",), previous_episode_id="ep1", episode_ordinal=2,
            call_expectation=CallExpectationV1(tasks=(TaskCallExpectationV1(
                task_id=lg.task_id, expectation=EXPECT_PRIOR_EPISODE, run_id=lg.run_id,
                finalized_calls_sha256=lg.sha256(), ledger_ref=lg.ref(),
                task_status_at_finalization="applied_to_job_workspace",
                dispatch_state=DISPATCH_PRIOR_EPISODE),)))
        assert validate_ledger_set(m) == []

    def test_a_task_without_run_ownership_owns_no_ledger(self, base):
        """An expectation with no run cannot expect a ledger, and a ledger cannot appear for it."""
        from packages.orchestration.run_manifest import EXPECT_NOT_DISPATCHED
        m = dataclasses.replace(
            base, calls=(), call_ledgers=(),
            call_expectation=CallExpectationV1(tasks=(TaskCallExpectationV1(
                task_id="T001", expectation=EXPECT_NOT_DISPATCHED, run_id="",
                task_status_at_finalization="pending"),)))
        assert validate_ledger_set(m) == []
        stray = dataclasses.replace(m, call_ledgers=(_ghost(task_id="T001", run_id="rX"),))
        assert validate_ledger_set(stray)


# --------------------------------------------------------------------------- the seams


class TestEverySeamEnforcesTheSet:
    def test_a_clean_manifest_publishes_and_reads_back(self, base, tmp_path):
        ev = tmp_path / "ev"
        ev.mkdir()
        write_run_manifest(ev, base, root=tmp_path)
        assert validate_index_and_tree(ev, job_id="j") == []
        assert load_latest_manifest_verified(ev, job_id="j").episode_id == "ep1"

    def test_the_set_validator_is_reachable_as_one_shared_contract(self, base):
        """F5: one validator, not a rule re-stated per seam."""
        forged = dataclasses.replace(base, call_ledgers=base.call_ledgers + (_ghost(),))
        assert validate_ledger_set(forged)
        assert validate_run_manifest(forged, mode=MODE_PUBLISHED_REFERENCE)
