"""Tests for packages.orchestration.pingpong_call_record — F058 T002, the disclosure in a
call's own fields of the run record (DECISION F058 D3).
"""

from __future__ import annotations

from packages.orchestration.model_failover import FailoverDisclosure, FailoverLinkAttempt
from packages.orchestration.pingpong_call_record import _session_fields
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
