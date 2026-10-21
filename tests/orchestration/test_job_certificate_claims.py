"""The claims a certificate states, derived from member bytes (F060, DECISION F060 D3)."""
from __future__ import annotations

import json

import pytest

from packages.orchestration.job_certificate_claims import (
    cost_claims_from_member,
    dod_summary_from_member,
    regression_status_from_member,
)

STARTED = "2026-10-01T00:00:00+00:00"
GOOD_ACTUALS = {
    "schema_version": "2.0.0", "provider_call_count": 2, "actual_call_count": 2,
    "unmeasured_call_count": 0, "total_tokens": 10, "actual_sources": ["pingpong_actuals"],
    "started_at": STARTED, "measured_cost_usd": 0.5, "priced_call_count": 2,
    "unpriced_call_count": 0,
}


def _member(obj) -> bytes:
    return json.dumps(obj).encode("utf-8")


def test_cost_claims_of_no_member_are_none_and_empty():
    assert cost_claims_from_member(None) == (None, [])


def test_cost_claims_of_a_good_member_are_its_cost_and_its_sources():
    data = _member({"budget_actuals": GOOD_ACTUALS, "first_running_at": STARTED})
    assert cost_claims_from_member(data) == ("$0.5000", ["pingpong_actuals"])


@pytest.mark.parametrize("data", [
    pytest.param(b"\xff\xfe", id="not-utf8"),
    pytest.param(b"{not json", id="not-json"),
    pytest.param(b"[1, 2]", id="not-an-object"),
    pytest.param(b'{"first_running_at": null}', id="no-budget-actuals"),
    pytest.param(_member({"budget_actuals": {"schema_version": "9.9.9"},
                          "first_running_at": None}), id="actuals-refused-by-the-decoder"),
])
def test_cost_claims_of_a_malformed_member_are_none_and_empty(data):
    assert cost_claims_from_member(data) == (None, [])


def test_dod_summary_of_no_member_is_none():
    assert dod_summary_from_member(None) is None


@pytest.mark.parametrize("data", [
    pytest.param(b"\xff\xfe", id="not-utf8"),
    pytest.param(b"{not json", id="not-json"),
    pytest.param(b"[1, 2]", id="not-an-object"),
])
def test_dod_summary_of_a_malformed_member_is_none(data):
    assert dod_summary_from_member(data) is None


def test_dod_summary_counts_three_checks_of_which_two_passed():
    data = _member({"released": True, "checks": [
        {"status": "passed"}, {"status": "failed"}, {"status": "passed"}]})
    assert dod_summary_from_member(data) == {"released": True, "check_count": 3, "passed_count": 2}


def test_dod_summary_without_a_checks_list_counts_none():
    assert dod_summary_from_member(_member({"released": False, "checks": "x"})) == {
        "released": False, "check_count": 0, "passed_count": 0}
    assert dod_summary_from_member(b"{}") == {
        "released": False, "check_count": 0, "passed_count": 0}


def test_a_released_value_that_is_truthy_but_not_a_bool_reads_true():
    assert dod_summary_from_member(_member({"released": "yes", "checks": []}))["released"] is True


def test_regression_status_of_no_member_is_none():
    assert regression_status_from_member(None) is None


@pytest.mark.parametrize("data", [
    pytest.param(b"\xff\xfe", id="not-utf8"),
    pytest.param(b"{not json", id="not-json"),
    pytest.param(b'["passed"]', id="not-an-object"),
    pytest.param(b"{}", id="no-test-status"),
])
def test_regression_status_of_a_malformed_member_is_none(data):
    assert regression_status_from_member(data) is None


def test_regression_status_of_a_good_member_is_its_test_status():
    assert regression_status_from_member(b'{"test_status": "passed"}') == "passed"
