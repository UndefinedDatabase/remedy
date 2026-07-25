"""F5 (round 13) + F1 (round 14) — a run's ledger history across Episodes.

Round 13 closed the invention hole: episode 2's ledger for a run could contain an entry saying
`call_id=ghost-prior, episode_id=ep1` — a call in no ep1 manifest, no ep1 call artifact and no ep1
ledger — and the published reference validated, because every check only asked "is ep1 a known
prior?". History was a claim nobody read back.

Round 14 closes what round 13's rule still allowed. Round 13 compared the entry PREFIX, so a
later episode could EXTEND a run that had already published `complete=true, terminal_state=completed`
— and change its terminal state on the way. Three facts forbid that: the ledger says it is the
complete account, the terminal state says the run ended, and published Evidence is immutable.

The model now matches production exactly. Verified against a real stop-then-resume:

    ep1  T001 run=f5962555  completed complete=True  2 entries
    ep2  T001 run=f5962555  completed complete=True  2 entries   <- byte-identical repeat
    ep2  T002 run=9ae434c5  completed complete=True  2 entries   <- new work, NEW run id

`PingPongResult.run_id` is a fresh `uuid4().hex[:16]` per execution, so later work is always a new
run. A terminal ledger is frozen whole; a later episode repeats it byte-for-byte as immutable
prior history, and carries its own new ledgers alongside.

No single Manifest can prove any of this, which is why the rule lives in the canonical chain
validator, where the whole chain is in hand.
"""
from __future__ import annotations

import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    CallLedgerEntryV1,
    _bind_artifact_refs,
    validate_ledger_chain,
)


def _chain():
    """Production's shape: ep1 finishes a run; ep2 REPEATS that terminal ledger byte-for-byte as
    prior history (and would carry any new work under a new run id)."""
    from packages.orchestration.run_manifest import (
        DISPATCH_PRIOR_EPISODE,
        EXPECT_PRIOR_EPISODE,
        CallExpectationV1,
        TaskCallExpectationV1,
    )
    ep1 = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(seq=1),)))
    lg = ep1.call_ledgers[0]
    ep2 = _bind_artifact_refs(T._mk(episode_id="ep2", calls=()))
    # Round 15 (F1): ep1 APPLIED T001, so ep2 must carry it as `prior_episode` naming the same
    # run and the same frozen ledger. Repeating ep1's `executed` expectation would claim the task
    # ran twice — which the resume loop makes impossible.
    ep2 = dataclasses.replace(
        ep2, prior_episode_ids=("ep1",), previous_episode_id="ep1", episode_ordinal=2,
        call_ledgers=ep1.call_ledgers,          # the exact frozen object
        call_expectation=CallExpectationV1(tasks=(TaskCallExpectationV1(
            task_id=lg.task_id, expectation=EXPECT_PRIOR_EPISODE, run_id=lg.run_id,
            finalized_calls_sha256=lg.sha256(), ledger_ref=lg.ref(),
            task_status_at_finalization="applied_to_job_workspace",
            dispatch_state=DISPATCH_PRIOR_EPISODE),)))
    return ep1, ep2


def _relg(ep2, ledger):
    return dataclasses.replace(ep2, call_ledgers=(ledger,))


def _probs(ep1, ep2):
    return validate_ledger_chain([ep1, ep2])


# --------------------------------------------------------------------------- the good shape


class TestALegitimateHistory:
    def test_a_byte_identical_repeat_is_accepted(self):
        ep1, ep2 = _chain()
        assert _probs(ep1, ep2) == []

    def test_a_single_episode_chain_is_fine(self):
        ep1, _ep2 = _chain()
        assert validate_ledger_chain([ep1]) == []

    def test_new_work_under_a_new_run_id_is_independent(self):
        """The production answer to "the run continued": it did not — a new run began."""
        ep1, ep2 = _chain()
        newrun = T._call(seq=2, role="reviewer", run="r-new")
        ep2b = _bind_artifact_refs(T._mk(episode_id="ep2", calls=(newrun,)))
        merged = dataclasses.replace(
            ep2b, prior_episode_ids=("ep1",), previous_episode_id="ep1", episode_ordinal=2,
            call_ledgers=ep1.call_ledgers + ep2b.call_ledgers)
        assert _probs(ep1, merged) == []

    def test_two_episodes_with_different_runs_never_interact(self):
        ep1 = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(run="r-ep1"),)))
        ep2 = _bind_artifact_refs(T._mk(episode_id="ep2", calls=(T._call(run="r-ep2"),)))
        ep2 = dataclasses.replace(ep2, prior_episode_ids=("ep1",), previous_episode_id="ep1",
                                  episode_ordinal=2)
        assert _probs(ep1, ep2) == []


# --------------------------------------------------------------------------- F1 finality


class TestATerminalLedgerIsFrozen:
    def test_the_reproduced_case(self):
        """ep1: completed/complete/[Call 1]. ep2 reused the run: failed/complete/[Call 1, Call 2].
        Both validated; the whole chain was accepted."""
        ep1, ep2 = _chain()
        lg = ep1.call_ledgers[0]
        extra = CallLedgerEntryV1(per_run_sequence=2, call_id="calls/reviewer/round-01/attempt",
                                  episode_id="ep2", role="reviewer", round=1, kind="attempt",
                                  prepared_input_fingerprint="a" * 64, ok=True)
        forged = dataclasses.replace(lg, terminal_state="failed",
                                     entries=lg.entries + (extra,))
        probs = _probs(ep1, _relg(ep2, forged))
        assert any("frozen" in p and "new run id" in p for p in probs), probs

    def test_a_complete_completed_ledger_cannot_extend(self):
        ep1, ep2 = _chain()
        lg = ep1.call_ledgers[0]
        extra = CallLedgerEntryV1(per_run_sequence=2, call_id="calls/reviewer/round-01/attempt",
                                  episode_id="ep2", role="reviewer", round=1, kind="attempt",
                                  prepared_input_fingerprint="b" * 64, ok=True)
        assert _probs(ep1, _relg(ep2, dataclasses.replace(lg, entries=lg.entries + (extra,))))

    def test_a_complete_stopped_ledger_cannot_extend(self):
        ep1 = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(seq=1),)))
        stopped = dataclasses.replace(ep1.call_ledgers[0], terminal_state="stopped")
        ep1 = dataclasses.replace(ep1, call_ledgers=(stopped,))
        ep2 = dataclasses.replace(
            _bind_artifact_refs(T._mk(episode_id="ep2", calls=())),
            prior_episode_ids=("ep1",), previous_episode_id="ep1", episode_ordinal=2)
        extra = CallLedgerEntryV1(per_run_sequence=2, call_id="calls/reviewer/round-01/attempt",
                                  episode_id="ep2", role="reviewer", round=1, kind="attempt",
                                  prepared_input_fingerprint="c" * 64, ok=True)
        assert _probs(ep1, _relg(ep2, dataclasses.replace(
            stopped, entries=stopped.entries + (extra,))))

    @pytest.mark.parametrize("state", ["failed", "blocked", "stopped", "skipped"])
    def test_the_terminal_state_cannot_change(self, state):
        ep1, ep2 = _chain()
        assert _probs(ep1, _relg(ep2, dataclasses.replace(
            ep1.call_ledgers[0], terminal_state=state)))

    def test_complete_cannot_change(self):
        ep1, ep2 = _chain()
        assert _probs(ep1, _relg(ep2, dataclasses.replace(
            ep1.call_ledgers[0], complete=False)))

    def test_the_header_cannot_change(self):
        """The whole object is frozen — not merely its entries."""
        ep1, ep2 = _chain()
        assert _probs(ep1, _relg(ep2, dataclasses.replace(
            ep1.call_ledgers[0], job_id="another-job")))


# --------------------------------------------------------------------------- the tampers


class TestALaterLedgerCannotRewriteHistory:
    def test_it_cannot_invent_a_prior_call(self):
        """Round 13's reproduction, still refused."""
        ep1, ep2 = _chain()
        ghost = CallLedgerEntryV1(per_run_sequence=1, call_id="calls/builder/round-01/ghost",
                                  episode_id="ep1", role="builder", round=1, kind="attempt",
                                  prepared_input_fingerprint="a" * 64, ok=True)
        assert _probs(ep1, _relg(ep2, dataclasses.replace(
            ep1.call_ledgers[0], entries=(ghost,))))

    @pytest.mark.parametrize("field,value", [
        ("role", "reviewer"), ("round", 7), ("kind", "parse-retry"),
        ("prepared_input_fingerprint", "b" * 64), ("ok", False),
        ("call_id", "calls/builder/round-99/attempt"),
    ])
    def test_it_cannot_alter_a_prior_entry(self, field, value):
        ep1, ep2 = _chain()
        lg = ep1.call_ledgers[0]
        altered = dataclasses.replace(lg, entries=(
            dataclasses.replace(lg.entries[0], **{field: value}),) + lg.entries[1:])
        assert _probs(ep1, _relg(ep2, altered)), f"{field} drifted without being caught"

    def test_it_cannot_remove_a_prior_entry(self):
        ep1, ep2 = _chain()
        lg = ep1.call_ledgers[0]
        assert _probs(ep1, _relg(ep2, dataclasses.replace(lg, entries=())))

    def test_it_cannot_reorder_prior_entries(self):
        ep1 = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(
            T._call(seq=1), T._call(seq=2, role="reviewer"))))
        ep2 = dataclasses.replace(
            _bind_artifact_refs(T._mk(episode_id="ep2", calls=())),
            prior_episode_ids=("ep1",), previous_episode_id="ep1", episode_ordinal=2,
            call_ledgers=ep1.call_ledgers, call_expectation=ep1.call_expectation)
        assert _probs(ep1, ep2) == []
        lg = ep1.call_ledgers[0]
        a, b = lg.entries
        swapped = dataclasses.replace(lg, entries=(
            dataclasses.replace(b, per_run_sequence=1),
            dataclasses.replace(a, per_run_sequence=2)))
        assert _probs(ep1, _relg(ep2, swapped))

    def test_a_prior_entry_must_resolve_to_a_real_prior_manifest_call(self):
        ep1, ep2 = _chain()
        lg = ep1.call_ledgers[0]
        unknown = dataclasses.replace(lg.entries[0], episode_id="ep-nobody-heard-of")
        assert _probs(ep1, _relg(ep2, dataclasses.replace(lg, entries=(unknown,))))


# --------------------------------------------------------------------------- the seam


class TestTheRuleLandsAtTheChainSeam:
    def test_the_canonical_chain_validator_enforces_finality(self):
        """Not a unit-test-only rule: the whole-chain validator refuses it."""
        from packages.orchestration.run_manifest import _validate_episode_graph
        ep1, ep2 = _chain()
        lg = ep1.call_ledgers[0]
        extra = CallLedgerEntryV1(per_run_sequence=2, call_id="calls/reviewer/round-01/attempt",
                                  episode_id="ep2", role="reviewer", round=1, kind="attempt",
                                  prepared_input_fingerprint="d" * 64, ok=True)
        bad = _relg(ep2, dataclasses.replace(lg, entries=lg.entries + (extra,)))
        assert _validate_episode_graph({"ep1": ep1, "ep2": bad})
        assert _validate_episode_graph({"ep1": ep1, "ep2": ep2}) == []
