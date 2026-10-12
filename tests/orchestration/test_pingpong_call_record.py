"""Tests for packages.orchestration.pingpong_call_record — F058 T002, the disclosure in a
call's own fields of the run record (DECISION F058 D3).
"""

from __future__ import annotations

from packages.orchestration.model_failover import FailoverDisclosure, FailoverLinkAttempt
from packages.orchestration.pingpong_call_record import _session_fields, parked_session_refs
from packages.orchestration.pingpong_provider import BuilderOutput


class TestSessionFieldsFailoverDisclosure:
    def test_no_disclosure_is_exactly_the_four_keys(self):
        out = BuilderOutput()
        assert set(_session_fields(out)) == {
            "session_id", "resume_used", "resume_session_ref", "resume_fallback",
        }

    def test_a_real_disclosure_adds_failover_equal_to_its_to_json(self):
        attempt = FailoverLinkAttempt(position=1, provider="claude-cli", model="opus", error="")
        disclosure = FailoverDisclosure(
            role="builder",
            intended_provider="claude-cli",
            intended_model="sonnet",
            primary_error="provider_error: ConnectionError: connection refused",
            attempts=(attempt,),
            used=attempt,
        )
        out = BuilderOutput()
        out.failover_disclosure = disclosure

        fields = _session_fields(out)
        assert set(fields) == {
            "session_id", "resume_used", "resume_session_ref", "resume_fallback", "failover",
        }
        assert fields["failover"] == disclosure.to_json()

    def test_an_attribute_that_is_not_a_disclosure_adds_no_key(self):
        out = BuilderOutput()
        out.failover_disclosure = {"reason": "not a real disclosure"}

        assert set(_session_fields(out)) == {
            "session_id", "resume_used", "resume_session_ref", "resume_fallback",
        }


class TestParkedSessionRefsFailover:
    """T003, DECISION F058 D4 (3): a session a backup opened is never offered back."""

    _SERVED = {"used": {"position": 1, "provider": "claude-cli", "model": "opus", "error": ""}}

    def test_a_round_a_backup_served_clears_the_roles_earlier_session(self):
        record = {"rounds": [
            {"builder": {"session_id": "b-1"}},
            {"builder": {"session_id": "b-2", "failover": self._SERVED}},
        ]}
        assert parked_session_refs(record) == {}

    def test_a_later_round_with_no_failover_sets_the_session_again(self):
        record = {"rounds": [
            {"builder": {"session_id": "b-1"}},
            {"builder": {"session_id": "b-2", "failover": self._SERVED}},
            {"builder": {"session_id": "b-3"}},
        ]}
        assert parked_session_refs(record) == {"builder": "b-3"}

    def test_a_failover_that_ran_out_keeps_the_session_as_today(self):
        record = {"rounds": [
            {"builder": {"session_id": "b-1"}},
            {"builder": {"session_id": "b-2", "failover": {"used": None}}},
        ]}
        assert parked_session_refs(record) == {"builder": "b-2"}
