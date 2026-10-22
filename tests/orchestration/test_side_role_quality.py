"""F113 T003b, DECISION F113 D3 — the summary role's frozen spot-check set, the flip to the role's own
model on a failure, the dwell before a passing re-check flips it back, and the lines status prints.

Every model answer comes from a scripted call_fn; the state lives in a temporary data root.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import datetime, timedelta, timezone

import pytest

from packages.orchestration.local_endpoints import LocalEndpoint, LocalEndpointProbes
from packages.orchestration.side_role_quality import (
    OUTCOME_FAILED,
    OUTCOME_PASSED,
    OUTCOME_UNAVAILABLE,
    SPOT_CHECK_DWELL_S,
    SPOT_CHECK_MAX_SECONDS,
    SPOT_CHECK_SET_VERSION,
    SUMMARY_SPOT_CHECKS,
    flip_reason,
    read_quality_state,
    record_spot_check,
    run_spot_check,
    side_role_status_lines,
    side_roles_dir,
)
from packages.orchestration.side_role_routing import ROUTE_FALLBACK, ROUTE_LOCAL, route_side_role

BOX = LocalEndpoint(name="box", base_url="http://127.0.0.1:9", model="muse-glimmer")
T0 = datetime(2026, 10, 22, 8, 0, tzinfo=timezone.utc)
UP = LocalEndpointProbes(list_models=lambda url: ["muse-glimmer:latest"])


@pytest.fixture(autouse=True)
def data_root(monkeypatch, tmp_path):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))


def answering(*, drop: str = "", text: str = "") -> object:
    """A call_fn whose summary names every fact of the case it is asked about, except `drop`."""
    def call_fn(prompt: str, attempt: int) -> str:
        if text:
            return text
        facts = [fact for case in SUMMARY_SPOT_CHECKS for fact in case.facts if fact in prompt and fact != drop]
        return json.dumps({"l1": "The change touches " + ", ".join(facts) + ".", "l2": []})

    return call_fn


def check(call_fn, *, at=T0, seconds=1.0, endpoint=BOX, probes=UP):
    ticks = iter(range(10_000))
    return run_spot_check("summary", endpoint, probes=probes, call_fn=call_fn,
                          clock=lambda: next(ticks) * seconds, now=lambda: at)


class TestTheFrozenSet:
    def test_the_set_is_pinned_to_its_version(self):
        digest = hashlib.sha256(json.dumps([asdict(case) for case in SUMMARY_SPOT_CHECKS]).encode()).hexdigest()
        assert (SPOT_CHECK_SET_VERSION, digest[:16]) == ("summary-spot-check-v1", "fdcef4acb1cf1339")

    def test_every_case_seeds_facts_its_own_diff_carries(self):
        for case in SUMMARY_SPOT_CHECKS:
            assert case.facts and all(any(fact in text for _, text in case.sections) for fact in case.facts)

    def test_the_section_names_carry_no_fact_so_an_echo_cannot_pass(self):
        for case in SUMMARY_SPOT_CHECKS:
            assert not any(fact in path for path, _ in case.sections for fact in case.facts)


class TestTheCheck:
    def test_a_summary_naming_every_seeded_fact_in_time_passes(self):
        record = check(answering())
        assert (record.outcome, record.reason, record.set_version) == (OUTCOME_PASSED, "", SPOT_CHECK_SET_VERSION)
        assert [case.passed for case in record.cases] == [True] * len(SUMMARY_SPOT_CHECKS)
        assert (record.endpoint, record.base_url, record.model, record.checked_at) == (
            "box", "http://127.0.0.1:9", "muse-glimmer", T0.isoformat())

    def test_a_missing_fact_fails_its_case_by_name(self):
        record = check(answering(drop="retry_limit"))
        assert (record.outcome, record.reason) == (OUTCOME_FAILED, "failed cases: removed-setting")
        failed = next(case for case in record.cases if not case.passed)
        assert (failed.missing_facts, failed.reason) == (("retry_limit",), "missing facts: retry_limit")

    def test_a_case_slower_than_the_limit_fails_for_its_time(self):
        record = check(answering(), seconds=SPOT_CHECK_MAX_SECONDS + 1)
        assert record.outcome == OUTCOME_FAILED
        assert all(case.reason.startswith("took ") for case in record.cases)

    def test_an_answer_that_is_no_summary_fails(self):
        record = check(answering(text="not json"))
        assert record.outcome == OUTCOME_FAILED
        assert all(case.reason.startswith("no summary: fallback:") for case in record.cases)

    def test_an_endpoint_that_does_not_answer_is_not_checked(self):
        record = check(answering(), probes=LocalEndpointProbes(list_models=lambda url: []))
        assert (record.outcome, record.cases) == (OUTCOME_UNAVAILABLE, ())
        assert record.reason.startswith("provider_unavailable: local endpoint box")


class TestTheFlip:
    def test_a_failed_check_flips_the_role_and_the_route_follows(self):
        record = check(answering(drop="retry_limit"))
        entry = record_spot_check(record)
        assert (entry["state"], entry["record_id"], entry["since"]) == ("flipped", record.record_id, T0.isoformat())
        reason = flip_reason("summary", BOX)
        assert reason == (f"quality_gate: summary on box (muse-glimmer) failed spot check {record.record_id} "
                          f"at {T0.isoformat()}")
        route = route_side_role("summary", BOX, UP)
        assert (route.route, route.reason) == (ROUTE_FALLBACK, reason)

    def test_a_passing_re_check_inside_the_dwell_keeps_the_flip(self):
        failed = check(answering(drop="retry_limit"))
        record_spot_check(failed)
        early = T0 + timedelta(seconds=SPOT_CHECK_DWELL_S - 1)
        entry = record_spot_check(check(answering(), at=early))
        assert (entry["state"], entry["record_id"]) == ("flipped", failed.record_id)
        assert route_side_role("summary", BOX, UP).route == ROUTE_FALLBACK

    def test_a_passing_re_check_after_the_dwell_flips_it_back(self):
        record_spot_check(check(answering(drop="retry_limit")))
        later = T0 + timedelta(seconds=SPOT_CHECK_DWELL_S)
        passed = check(answering(), at=later)
        entry = record_spot_check(passed)
        assert (entry["state"], entry["record_id"]) == ("local", passed.record_id)
        assert flip_reason("summary", BOX) == ""
        assert route_side_role("summary", BOX, UP).route == ROUTE_LOCAL

    def test_an_unavailable_check_changes_nothing(self):
        record_spot_check(check(answering(drop="retry_limit")))
        before = read_quality_state()
        record_spot_check(check(answering(), at=T0 + timedelta(days=1),
                                probes=LocalEndpointProbes(list_models=lambda url: [])))
        assert read_quality_state() == before

    def test_a_flip_binds_only_the_endpoint_and_model_it_was_checked_on(self):
        record_spot_check(check(answering(drop="retry_limit")))
        assert flip_reason("summary", LocalEndpoint("box", "http://127.0.0.1:9", "other-model")) == ""

    def test_every_check_is_appended_to_the_history(self):
        first = check(answering(drop="retry_limit"))
        second = check(answering(), at=T0 + timedelta(minutes=5))
        record_spot_check(first)
        record_spot_check(second)
        history = (side_roles_dir() / "spot_checks.jsonl").read_text(encoding="utf-8").splitlines()
        assert [json.loads(line)["record_id"] for line in history] == [first.record_id, second.record_id]

    def test_a_state_that_cannot_be_read_keeps_the_role_off_the_endpoint(self):
        side_roles_dir().mkdir(parents=True)
        (side_roles_dir() / "quality_state.json").write_text("{broken", encoding="utf-8")
        assert flip_reason("summary", BOX).startswith("quality_gate: the side-role quality state")
        assert route_side_role("summary", BOX, UP).route == ROUTE_FALLBACK
        (line,) = side_role_status_lines({"summary": BOX})
        assert line.startswith("every mapped side role runs on its own model")


class TestTheStatusLines:
    def test_an_unmapped_project_prints_nothing(self):
        assert side_role_status_lines({}) == []

    def test_each_state_reads_as_one_line(self):
        assert side_role_status_lines({"summary": BOX, "teacher": BOX}) == [
            "summary on box (muse-glimmer): not spot-checked for this endpoint and model yet",
            "teacher on box (muse-glimmer): no spot-check set exists for this role, so it is never checked",
        ]
        failed = check(answering(drop="retry_limit"))
        record_spot_check(failed)
        (line,) = side_role_status_lines({"summary": BOX})
        assert line == (f"summary on box (muse-glimmer): FLIPPED to its own model since {T0.isoformat()} by failed "
                        f"spot check {failed.record_id}; a passing re-check after "
                        f"{(T0 + timedelta(seconds=SPOT_CHECK_DWELL_S)).isoformat()} flips it back")
        passed = check(answering(), at=T0 + timedelta(seconds=SPOT_CHECK_DWELL_S))
        record_spot_check(passed)
        assert side_role_status_lines({"summary": BOX}) == [
            f"summary on box (muse-glimmer): passing since spot check {passed.record_id} at {passed.checked_at}"]
