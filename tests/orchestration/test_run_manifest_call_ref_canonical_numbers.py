"""F2 (round 15) — a call ref's numbers have exactly ONE text form.

Round 14 closed the grammar but parsed the two numbers with `int()`, and `int()` reads one number
many ways. So every one of these was accepted:

    round-01     round-001     round-000001        <- three names for round 1
    attempt-01   attempt-001   attempt-000001      <- three names for attempt 1
    attempt-00                                     <- index 0, which is not a call

The ref is precisely the name F010's post-mortems, F012's manifests and F140's replay are supposed
to AGREE on. An alias set breaks that the moment two of them spell it differently — and nothing
would have noticed, because each spelling parsed to the same integer.

The canonical form is what production always emitted (`f"{n:02d}"`): pad to two digits below ten,
plain above. It was only ever the reader that accepted more. Canonicality is decided by
RECONSTRUCTION — the ref must equal what its own parts rebuild.
"""
from __future__ import annotations

import pytest

from packages.orchestration.call_identity import (
    canonical_call_number,
    parse_canonical_call_number,
)
from packages.orchestration.run_manifest import (
    canonical_call_ref,
    parse_call_ref,
    safe_call_ref,
)

# --------------------------------------------------------------------------- the formatter


class TestTheCanonicalFormatter:
    @pytest.mark.parametrize("value,text", [
        (1, "01"), (2, "02"), (9, "09"), (10, "10"), (11, "11"), (99, "99"),
        (100, "100"), (101, "101"), (1000, "1000"),
    ])
    def test_the_required_table(self, value, text):
        assert canonical_call_number(value) == text

    @pytest.mark.parametrize("bad", [0, -1, -100, True, False, 1.5, "1", None])
    def test_only_positive_integers_have_a_form(self, bad):
        with pytest.raises(ValueError):
            canonical_call_number(bad)

    def test_the_formatter_and_parser_round_trip(self):
        for n in list(range(1, 130)) + [999, 1000]:
            assert parse_canonical_call_number(canonical_call_number(n)) == n

    @pytest.mark.parametrize("text,value", [
        ("01", 1), ("09", 9), ("10", 10), ("99", 99), ("100", 100),
    ])
    def test_the_parser_accepts_the_canonical_text(self, text, value):
        assert parse_canonical_call_number(text) == value

    @pytest.mark.parametrize("text", [
        "001", "000001", "0001",           # padded aliases of 1
        "010", "0010",                     # padded aliases of 10
        "00", "0", "000",                  # zero is not a call
        "1", "9",                          # unpadded below ten
        "", "a", "1a", " 1", "1 ", "+1", "-1", "1.0",
    ])
    def test_the_parser_refuses_every_alias_and_non_number(self, text):
        assert parse_canonical_call_number(text) is None


# --------------------------------------------------------------------------- the refs


class TestCanonicalRefsPass:
    @pytest.mark.parametrize("cid", [
        "calls/builder/round-01/attempt",
        "calls/reviewer/round-09/parse-retry",
        "calls/builder/round-10/attempt",
        "calls/builder/round-99/attempt",
        "calls/builder/round-100/attempt",
        "streams/builder/round-01/attempt-01",
        "streams/reviewer/round-02/parse-retry-03",
        "streams/builder/round-10/attempt-99",
        "streams/builder/round-100/attempt-100",
    ])
    def test_it_passes(self, cid):
        assert safe_call_ref(cid), cid

    def test_round_10_and_100_parse_to_their_real_numbers(self):
        assert parse_call_ref("calls/builder/round-10/attempt")[0]["round"] == 10
        assert parse_call_ref("calls/builder/round-100/attempt")[0]["round"] == 100

    def test_index_10_and_100_parse_to_their_real_numbers(self):
        assert parse_call_ref("streams/builder/round-01/attempt-10")[0]["index"] == 10
        assert parse_call_ref("streams/builder/round-01/attempt-100")[0]["index"] == 100


class TestNumericAliasesBlock:
    @pytest.mark.parametrize("cid", [
        "calls/builder/round-001/attempt",
        "calls/builder/round-000001/attempt",
        "calls/builder/round-0001/attempt",
        "calls/builder/round-010/attempt",
    ])
    def test_a_padded_round_blocks(self, cid):
        assert not safe_call_ref(cid), f"{cid} is an alias of a canonical round"

    @pytest.mark.parametrize("cid", [
        "streams/builder/round-01/attempt-001",
        "streams/builder/round-01/attempt-000001",
        "streams/builder/round-01/attempt-010",
    ])
    def test_a_padded_index_blocks(self, cid):
        assert not safe_call_ref(cid), f"{cid} is an alias of a canonical index"

    @pytest.mark.parametrize("cid", [
        "streams/builder/round-01/attempt-00",
        "streams/builder/round-01/attempt-0",
        "streams/builder/round-01/attempt-000",
    ])
    def test_index_zero_blocks(self, cid):
        assert not safe_call_ref(cid), "index 0 is not a call"

    @pytest.mark.parametrize("cid", [
        "calls/builder/round-00/attempt", "calls/builder/round-0/attempt",
    ])
    def test_round_zero_blocks(self, cid):
        assert not safe_call_ref(cid)

    def test_the_error_names_the_canonical_form(self):
        _f, probs = parse_call_ref("calls/builder/round-001/attempt")
        assert any("canonical" in p for p in probs), probs

    def test_the_aliases_would_all_have_parsed_to_the_same_call(self):
        """Why it matters: without the rule these are one call under three names."""
        for alias in ("round-001", "round-000001"):
            assert not safe_call_ref(f"calls/builder/{alias}/attempt")
        assert safe_call_ref("calls/builder/round-01/attempt")


# --------------------------------------------------------------------------- reconstruction


class TestCanonicalityIsDecidedByReconstruction:
    def test_a_ref_must_equal_what_its_parts_rebuild(self):
        assert canonical_call_ref(namespace="calls", role="builder", round=1,
                                  kind="attempt") == "calls/builder/round-01/attempt"
        assert canonical_call_ref(namespace="streams", role="reviewer", round=2,
                                  kind="parse-retry",
                                  index=3) == "streams/reviewer/round-02/parse-retry-03"

    @pytest.mark.parametrize("cid", [
        "calls/builder/round-01/attempt", "streams/builder/round-01/attempt-01",
        "calls/builder/round-100/attempt", "streams/reviewer/round-02/parse-retry-03",
    ])
    def test_every_accepted_ref_rebuilds_to_itself(self, cid):
        fields, probs = parse_call_ref(cid)
        assert probs == []
        assert canonical_call_ref(**fields) == cid


# --------------------------------------------------------------------------- production


class TestProductionOnlyEmitsCanonicalRefs:
    def test_the_fallback_synthesizer_is_canonical_at_every_round(self):
        from packages.orchestration.pingpong_loop import shared_call_id

        class NoStream:
            stream_call_id = ""

        for role in ("builder", "reviewer"):
            for kind in ("attempt", "parse-retry"):
                for rnd in (1, 2, 9, 10, 11, 99, 100, 101):
                    cid = shared_call_id(NoStream(), role, rnd, kind)
                    assert safe_call_ref(cid), cid
                    assert parse_call_ref(cid)[0]["round"] == rnd

    def test_the_stream_allocator_uses_the_shared_formatter(self):
        """The stream directory name IS the call ref F010 and F012 both record."""
        import inspect

        from packages.orchestration import pingpong_provider
        src = inspect.getsource(pingpong_provider._ClaudeStreamMixin
                               if hasattr(pingpong_provider, "_ClaudeStreamMixin")
                               else pingpong_provider)
        assert "canonical_call_number" in src
        assert ":02d}/{self._stream_kind}-{idx:02d}" not in src

    def test_the_generators_and_the_validator_share_one_rule(self):
        import inspect

        from packages.orchestration import pingpong_loop
        assert "canonical_call_number" in inspect.getsource(pingpong_loop.shared_call_id)
