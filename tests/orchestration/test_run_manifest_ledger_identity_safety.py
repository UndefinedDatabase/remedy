"""F6 (round 13) — Ledger entry identities are path- and secret-safe.

Reproduced: a prior ledger entry with `call_id = "/home/alice/SUPERSECRET"` validated as a
published reference, and its bytes went into the canonical record — `/home/alice` sitting in the
Evidence, ready to be exported.

The two ids answer different questions and get the established rule for each:

* `call_id` is a path-SHAPED reference to the call's evidence directory
  (`calls/<role>/round-NN/<kind>`, a shape shared with F010). It is NOT a single component —
  every real call Remedy makes contains separators, so a "no separators" rule would refuse all of
  them. It is bounded, traversal-free, relative-only, backslash-free, control-char-free.
* `episode_id` IS a single component.

Both then go through the SAME secret and path scanners every other stored F012 value uses — the
established redactor and scrubber, not a new weaker regex.
"""
from __future__ import annotations

import dataclasses

import pytest

import tests.orchestration.test_run_manifest as T
from packages.orchestration.run_manifest import (
    MAX_LEDGER_ROUND,
    MAX_LEDGER_SEQUENCE,
    MODE_PUBLISHED_REFERENCE,
    _bind_artifact_refs,
    safe_call_ref,
    validate_run_call_ledger,
    validate_run_manifest,
)


@pytest.fixture
def base():
    return _bind_artifact_refs(T._mk(calls=(T._call(seq=1),)))


def _entry_probs(base, **change):
    lg = base.call_ledgers[0]
    forged = dataclasses.replace(
        lg, entries=(dataclasses.replace(lg.entries[0], **change),))
    return validate_run_call_ledger(forged)


# --------------------------------------------------------------------------- call_id


class TestTheCallIdRule:
    def test_the_real_production_shape_is_accepted(self, base):
        """The rule must not refuse what Remedy actually records.

        Production call ids are path-shaped (`calls/builder/round-01/attempt` — verified against
        a real fake-provider run); the fixtures use short ids. Both are legal refs, and a
        component-only rule would have refused every real one.
        """
        assert safe_call_ref("calls/builder/round-01/attempt")
        assert safe_call_ref("calls/reviewer/round-01/parse-retry")
        assert validate_run_call_ledger(base.call_ledgers[0]) == []
        assert _entry_probs(base, call_id="calls/builder/round-01/attempt") == []

    @pytest.mark.parametrize("cid", [
        "/home/alice/SUPERSECRET",              # THE reproduction: absolute
        "../../etc/passwd",                     # traversal
        "calls/../../../etc/shadow",            # traversal mid-ref
        "calls\\windows\\attempt",              # backslash
        "calls/round\x00/attempt",              # control character
        "",                                     # empty
        "c" * 5000,                             # unbounded
    ])
    def test_an_unsafe_call_id_blocks(self, base, cid):
        probs = _entry_probs(base, call_id=cid)
        assert any("call_id" in p for p in probs), (cid, probs)

    def test_the_unsafe_call_id_blocks_the_whole_published_reference(self, base):
        lg = base.call_ledgers[0]
        te = base.call_expectation.tasks[0]
        forged_lg = dataclasses.replace(lg, entries=(
            dataclasses.replace(lg.entries[0], call_id="/home/alice/SUPERSECRET"),))
        m = dataclasses.replace(base, call_ledgers=(forged_lg,),
                                call_expectation=dataclasses.replace(
                                    base.call_expectation, tasks=(dataclasses.replace(
                                        te, finalized_calls_sha256=forged_lg.sha256(),
                                        ledger_ref=forged_lg.ref()),)))
        assert validate_run_manifest(m, mode=MODE_PUBLISHED_REFERENCE) != []

    def test_the_rule_is_shared_with_the_call_identity(self):
        """F8: one rule, one definition — the identity validator and the ledger ask the same
        question, so they can never drift apart."""
        from packages.orchestration.run_manifest import validate_call_identity
        from packages.orchestration.call_identity import CallIdentity
        ident = CallIdentity(job_id="j", task_id="T001", run_id="r1", sequence=1,
                             role="builder", round=1, kind="attempt",
                             call_id="/home/alice/SUPERSECRET", episode_id="ep")
        assert any("call_id" in p for p in validate_call_identity(ident))
        assert not safe_call_ref("/home/alice/SUPERSECRET")


# --------------------------------------------------------------------------- episode_id


class TestTheEpisodeIdRule:
    @pytest.mark.parametrize("eid", [
        "../../etc/passwd", "/home/alice", "ep/sub", "ep\\sub", "", "e" * 500,
    ])
    def test_an_unsafe_episode_id_blocks(self, base, eid):
        probs = _entry_probs(base, episode_id=eid)
        assert any("episode_id" in p for p in probs), (eid, probs)

    def test_a_real_episode_id_passes(self, base):
        assert _entry_probs(base, episode_id="0a84d5d9ce0c4328") == []


# --------------------------------------------------------------------------- the scanners


class TestSecretAndPathCanaries:
    def test_a_secret_canary_in_a_call_id_never_reaches_the_export(self, base):
        """The established redactor is the detector — no new weaker regex."""
        probs = _entry_probs(base, call_id="calls/builder/round-01/token=SECRETVALUE123456")
        assert probs, "a secret canary validated"

    def test_an_absolute_home_path_canary_blocks(self, base):
        """THE reproduction's value. The scanner's job is a RAW LOCAL path, which is what an
        absolute one is."""
        from packages.orchestration.run_manifest import _contains_local_path
        assert _contains_local_path("/home/alice/SUPERSECRET")
        assert _entry_probs(base, call_id="/home/alice/SUPERSECRET")

    def test_a_ref_that_merely_reads_like_a_path_is_now_refused_by_the_grammar(self, base):
        """Round 13 recorded honestly that `calls/home/alice/attempt` was ACCEPTED: it is a
        relative ref, and "not absolute" was the whole rule. Round 14's closed grammar refuses
        it for the real reason — `home` is not a role and `alice` is not `round-NN`. The ref
        must NAME a call, not merely fail to be dangerous."""
        probs = _entry_probs(base, call_id="calls/home/alice/attempt")
        assert probs
        assert any("role" in p for p in probs), probs

    def test_the_canary_bytes_never_enter_canonical_output(self, base):
        """The point of the rule: an unsafe value is refused BEFORE it can be published."""
        lg = base.call_ledgers[0]
        forged = dataclasses.replace(lg, entries=(
            dataclasses.replace(lg.entries[0], call_id="/home/alice/SUPERSECRET"),))
        assert validate_run_call_ledger(forged), "the record would have been published"
        # The bytes exist only in the rejected in-memory object — never in a published tree.
        assert b"/home/alice" in forged.canonical_bytes()
        assert b"/home/alice" not in base.canonical_bytes()


# --------------------------------------------------------------------------- slash-command false-positive (R-0083)


class TestSlashCommandFalsePositive:
    """_contains_local_path must not flag single-segment slash-command tokens
    while still catching real absolute paths."""

    @pytest.mark.parametrize("value", [
        "chore(workflow): add /review-remedy command",
        "add /build-remedy-large command",
        "docs: /help mention",
    ])
    def test_slash_command_tokens_are_safe(self, value):
        from packages.orchestration.run_manifest import _contains_local_path
        assert not _contains_local_path(value), f"false positive on: {value!r}"

    @pytest.mark.parametrize("value", [
        "/home/user/x",
        "touch /etc/passwd",
        "log at /var/log/app.log",
        "ship to /Users",
        "mount /snap",
        "backup /Volumes",
    ])
    def test_real_paths_still_flagged(self, value):
        """Container-mount names (/workspace, /data) stay neutralized — they are
        not standard OS root dirs and the accepted residual from R-0083."""
        from packages.orchestration.run_manifest import _contains_local_path
        assert _contains_local_path(value), f"missed real path in: {value!r}"


# --------------------------------------------------------------------------- bounds


class TestBoundedNumbers:
    @pytest.mark.parametrize("value", [0, -1, MAX_LEDGER_ROUND + 1, True, "1", 1.5])
    def test_an_out_of_bounds_round_blocks(self, base, value):
        assert any("round" in p for p in _entry_probs(base, round=value))

    @pytest.mark.parametrize("value", [0, -1, MAX_LEDGER_SEQUENCE + 1, True])
    def test_an_out_of_bounds_sequence_blocks(self, base, value):
        assert _entry_probs(base, per_run_sequence=value)

    @pytest.mark.parametrize("role", ["../evil", "admin", ""])
    def test_role_is_a_closed_enum(self, base, role):
        assert any("role" in p for p in _entry_probs(base, role=role))

    @pytest.mark.parametrize("kind", ["../evil", "invented", ""])
    def test_kind_is_a_closed_enum(self, base, kind):
        assert any("kind" in p for p in _entry_probs(base, kind=kind))

    @pytest.mark.parametrize("fp", ["", "ABC" * 21 + "D", "z" * 64, "a" * 63])
    def test_the_fingerprint_is_exact_lowercase_sha256(self, base, fp):
        assert any("fingerprint" in p for p in _entry_probs(base, prepared_input_fingerprint=fp))
