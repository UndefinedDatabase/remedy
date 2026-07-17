"""F5 (round 13) — a run's ledger history is CONTINUOUS across Episodes.

The reproduction: episode 2's ledger for a run carried an entry saying `call_id=ghost-prior,
episode_id=ep1` — a call present in no ep1 manifest, no ep1 call artifact and no ep1 ledger. The
later published reference validated, because every existing check only ever asked "is ep1 a known
prior?". Nobody read history back.

No single Manifest can prove this, which is exactly why it was missed: the rule belongs to the
CANONICAL CHAIN. `_validate_episode_graph` is where the whole chain is in hand, so the rule lands
there — and every seam that proves a chain (writer preflight, writer postcondition, recovery, the
canonical loader, the verified tree builder, the Evidence export) reaches it.

The shape being defended is production's, not an invention: a real pre-work stop on a resumed job
carries the prior episode's entries FIRST, in order, in the same run's ledger.
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
    """ep1 runs a task; ep2 is a later episode whose ledger carries ep1's entry as history."""
    ep1 = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(seq=1),)))
    ep2 = _bind_artifact_refs(T._mk(episode_id="ep2", calls=(T._call(seq=2, role="reviewer"),)))
    ep2 = dataclasses.replace(ep2, prior_episode_ids=("ep1",), previous_episode_id="ep1",
                              episode_ordinal=2)
    prior = dataclasses.replace(ep1.call_ledgers[0].entries[0], episode_id="ep1")
    own = dataclasses.replace(ep2.call_ledgers[0].entries[0], per_run_sequence=2)
    ep2 = dataclasses.replace(ep2, call_ledgers=(
        dataclasses.replace(ep2.call_ledgers[0], entries=(prior, own)),))
    return ep1, ep2, prior, own


def _with(ep2, entries):
    return dataclasses.replace(ep2, call_ledgers=(
        dataclasses.replace(ep2.call_ledgers[0], entries=entries),))


def _probs(ep1, ep2):
    return validate_ledger_chain([ep1, ep2])


# --------------------------------------------------------------------------- the good shape


class TestALegitimateHistory:
    def test_an_exact_extension_is_accepted(self):
        ep1, ep2, _p, _o = _chain()
        assert _probs(ep1, ep2) == []

    def test_an_identical_ledger_is_accepted(self):
        """A run that made no new calls repeats its ledger unchanged — not an extension, but
        not a contradiction either."""
        ep1, ep2, prior, _own = _chain()
        assert _probs(ep1, _with(ep2, (prior,))) == []

    def test_a_single_episode_chain_is_fine(self):
        ep1, _ep2, _p, _o = _chain()
        assert validate_ledger_chain([ep1]) == []

    def test_two_episodes_with_different_runs_never_interact(self):
        """A resumed episode re-runs its task under a NEW run — its ledger owes the earlier run
        nothing, because it is a different run."""
        ep1 = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(T._call(run="r-ep1"),)))
        ep2 = _bind_artifact_refs(T._mk(episode_id="ep2", calls=(T._call(run="r-ep2"),)))
        ep2 = dataclasses.replace(ep2, prior_episode_ids=("ep1",), previous_episode_id="ep1",
                                  episode_ordinal=2)
        assert _probs(ep1, ep2) == []


# --------------------------------------------------------------------------- the tampers


class TestALaterLedgerCannotRewriteHistory:
    def test_it_cannot_invent_a_prior_call(self):
        """THE reproduction."""
        ep1, ep2, _prior, own = _chain()
        ghost = CallLedgerEntryV1(per_run_sequence=1, call_id="ghost-prior", episode_id="ep1",
                                  role="builder", round=1, kind="attempt",
                                  prepared_input_fingerprint="a" * 64, ok=True)
        probs = _probs(ep1, _with(ep2, (ghost, own)))
        assert any("no episode in the canonical chain published that call" in p
                   for p in probs), probs

    def test_it_cannot_alter_a_prior_call_id(self):
        ep1, ep2, prior, own = _chain()
        probs = _probs(ep1, _with(ep2, (dataclasses.replace(
            prior, call_id="calls/builder/round-99/attempt"), own)))
        assert probs

    @pytest.mark.parametrize("field,value", [
        ("role", "reviewer"), ("round", 7), ("kind", "parse-retry"),
    ])
    def test_it_cannot_alter_a_prior_role_round_or_kind(self, field, value):
        ep1, ep2, prior, own = _chain()
        probs = _probs(ep1, _with(ep2, (dataclasses.replace(prior, **{field: value}), own)))
        assert any("does not extend" in p for p in probs), probs

    def test_it_cannot_alter_a_prior_fingerprint(self):
        ep1, ep2, prior, own = _chain()
        probs = _probs(ep1, _with(ep2, (dataclasses.replace(
            prior, prepared_input_fingerprint="b" * 64), own)))
        assert any("does not extend" in p for p in probs), probs

    def test_it_cannot_alter_a_prior_result(self):
        ep1, ep2, prior, own = _chain()
        probs = _probs(ep1, _with(ep2, (dataclasses.replace(prior, ok=False), own)))
        assert any("does not extend" in p for p in probs), probs

    def test_it_cannot_remove_a_prior_entry(self):
        ep1, ep2, _prior, own = _chain()
        probs = _probs(ep1, _with(ep2, (dataclasses.replace(own, per_run_sequence=1),)))
        assert any("cannot shrink" in p or "does not extend" in p for p in probs), probs

    def test_it_cannot_reorder_prior_entries(self):
        """Two prior calls, swapped: every entry still resolves, the order does not."""
        ep1 = _bind_artifact_refs(T._mk(episode_id="ep1", calls=(
            T._call(seq=1), T._call(seq=2, role="reviewer"))))
        ep2 = _bind_artifact_refs(T._mk(episode_id="ep2", calls=(
            T._call(seq=3, role="builder", rnd=2, fp="p2"),)))
        ep2 = dataclasses.replace(ep2, prior_episode_ids=("ep1",), previous_episode_id="ep1",
                                  episode_ordinal=2)
        a, b = (dataclasses.replace(e, episode_id="ep1") for e in ep1.call_ledgers[0].entries)
        own = dataclasses.replace(ep2.call_ledgers[0].entries[0], per_run_sequence=3)
        good = _with(ep2, (a, b, own))
        assert _probs(ep1, good) == []
        swapped = (dataclasses.replace(b, per_run_sequence=1),
                   dataclasses.replace(a, per_run_sequence=2), own)
        assert any("does not extend" in p for p in _probs(ep1, swapped and _with(ep2, swapped)))

    def test_it_cannot_attribute_a_prior_call_to_the_wrong_episode(self):
        ep1, ep2, prior, own = _chain()
        probs = _probs(ep1, _with(ep2, (dataclasses.replace(prior, episode_id="ep2"), own)))
        assert probs

    def test_a_prior_entry_must_resolve_to_a_real_prior_manifest_call(self):
        """"It happened earlier" is a claim; a claim about a call nobody published is not one."""
        ep1, ep2, _prior, own = _chain()
        unknown = CallLedgerEntryV1(per_run_sequence=1, call_id="calls/builder/round-01/attempt",
                                    episode_id="ep-nobody-heard-of", role="builder", round=1,
                                    kind="attempt", prepared_input_fingerprint="c" * 64, ok=True)
        assert _probs(ep1, _with(ep2, (unknown, own)))


# --------------------------------------------------------------------------- the seam


class TestTheRuleLandsAtTheChainSeam:
    def test_the_canonical_chain_validator_enforces_continuity(self, tmp_path):
        """Not a unit-test-only rule: the whole-chain validator refuses it on disk."""
        from packages.orchestration.run_manifest import (
            _validate_episode_graph,
        )
        ep1, ep2, _prior, own = _chain()
        ghost = CallLedgerEntryV1(per_run_sequence=1, call_id="ghost", episode_id="ep1",
                                  role="builder", round=1, kind="attempt",
                                  prepared_input_fingerprint="a" * 64, ok=True)
        bad = _with(ep2, (ghost, own))
        assert _validate_episode_graph({"ep1": ep1, "ep2": bad})
        assert _validate_episode_graph({"ep1": ep1, "ep2": ep2}) == []
