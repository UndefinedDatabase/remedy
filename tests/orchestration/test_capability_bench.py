"""Tests for the capability bench record schema (F082 T001).

Also the R-0407 regression: ``gauntlet_runner.measure_tokens`` must count the
token keys ``orchestrator_loop.measure_call_cost`` really writes, or every
measured gauntlet run records a false zero.
"""
from __future__ import annotations

import json
from typing import Any

from packages.orchestration.capability_bench import (
    POSTMORTEM_CLASS_ABSENT,
    BenchRecord,
    build_bench_record,
)
from packages.orchestration.gauntlet_runner import measure_tokens


def a_body(**overrides: Any) -> dict[str, Any]:
    """A recorded run.json body of the shape `gauntlet_runner._evidence_body` writes."""
    body: dict[str, Any] = {
        "gauntlet_run_version": 1,
        "order_id": "g01-cold-start",
        "kind": "cold_start",
        "terminal_status": "done",
        "wall_seconds": 12.5,
        "postmortems": [],
        "tokens": {"in": 1200, "out": 340},
    }
    body.update(overrides)
    return body


class _Verdict:
    """The one attribute the bench reads off `gauntlet_evaluator.RunVerdict`."""

    def __init__(self, flawless: bool) -> None:
        self.flawless = flawless


def test_full_body_populates_every_field() -> None:
    record = build_bench_record(
        evidence_body=a_body(postmortems=[{"failure_class": "verify_failed"}]),
        series="nightly", verdict=_Verdict(True))
    assert record == BenchRecord(
        order_id="g01-cold-start", series="nightly", passed=True,
        cost={"in": 1200, "out": 340}, wall_s=12.5, repair_rounds=None,
        postmortem_classes=("verify_failed",))


def test_body_without_tokens_key_gives_cost_none() -> None:
    body = a_body()
    del body["tokens"]
    body["tokens_source"] = "unmeasured"
    record = build_bench_record(evidence_body=body, series="nightly",
                                verdict=_Verdict(False))
    assert record.cost is None
    assert record.passed is False


def test_two_failure_classes_yield_both_in_first_seen_order() -> None:
    body = a_body(postmortems=[{"failure_class": "verify_failed"},
                               {"failure_class": "provider_error"},
                               {"failure_class": "verify_failed"},
                               {"failure_class": ""}])
    record = build_bench_record(evidence_body=body, series="nightly", verdict=None)
    assert record.postmortem_classes == (
        "verify_failed", "provider_error", POSTMORTEM_CLASS_ABSENT)


def test_repair_rounds_is_none_because_no_source_exists() -> None:
    record = build_bench_record(evidence_body=a_body(), series="nightly",
                                verdict=_Verdict(True))
    assert record.repair_rounds is None


def test_to_json_round_trips_with_sorted_keys() -> None:
    record = build_bench_record(evidence_body=a_body(), series="nightly",
                                verdict=_Verdict(True))
    body = record.to_json()
    assert list(body) == sorted(body)
    assert json.loads(json.dumps(body)) == body
    rebuilt = BenchRecord(**{**body,
                            "postmortem_classes": tuple(body["postmortem_classes"])})
    assert rebuilt.to_json() == body


def test_measure_tokens_counts_the_input_output_spelling_r0407() -> None:
    entries = [{"cost": {"usage": {"input_tokens": 111, "output_tokens": 222}}}]
    assert measure_tokens(entries) == {"in": 111, "out": 222}


def test_measure_tokens_still_counts_the_prompt_completion_spelling_r0407() -> None:
    entries = [{"cost": {"usage": {"prompt_tokens": 7, "completion_tokens": 9}}}]
    assert measure_tokens(entries) == {"in": 7, "out": 9}
