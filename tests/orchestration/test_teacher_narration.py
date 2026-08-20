"""Tests for teacher narration — Stage 1 of the teacher role (F255 T002).

The load-bearing properties are DETERMINISM (two passes are byte-identical),
ZERO COST (no model, no network, no writer) and HONESTY (an event outside the
enumerated set is narrated as unrecognised, never invented and never raised).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from packages.orchestration import teacher_narration
from packages.orchestration.teacher_narration import (
    NARRATED_EVENTS,
    UNKNOWN_FIELD,
    UNRECOGNISED_TEMPLATE,
    narrate_run_event,
    narrate_run_events,
)


def _event(name: str, **fields: object) -> dict[str, object]:
    base: dict[str, object] = {
        "event": name,
        "job_id": "job-1",
        "run_id": "run-1",
        "timestamp": "2026-08-21T00:00:00Z",
    }
    base.update(fields)
    return base


class TestEnumeratedSet:
    @pytest.mark.parametrize("name", sorted(NARRATED_EVENTS))
    def test_every_enumerated_event_narrates_without_the_unrecognised_text(self, name):
        sentence = narrate_run_event(_event(name, task_id="t1", outcome="changed",
                                            message="because"))
        assert sentence
        assert "no narration for" not in sentence

    @pytest.mark.parametrize("name", sorted(NARRATED_EVENTS))
    def test_no_template_leaves_an_unfilled_placeholder(self, name):
        sentence = narrate_run_event(_event(name))
        assert "{" not in sentence and "}" not in sentence

    def test_the_set_holds_the_events_a_job_lives_through(self):
        # Pinned by EXPECTED LITERAL: a test that reads the mapping it is meant
        # to freeze can never fail, however wrong that mapping becomes.
        assert sorted(NARRATED_EVENTS) == [
            "job_created",
            "planning_completed",
            "planning_failed",
            "planning_started",
            "task_run_completed",
            "task_run_failed",
            "task_run_noop",
            "task_run_started",
            "verification_failed",
            "verification_passed",
            "workspace_materialized",
        ]


class TestUnrecognisedEvents:
    @pytest.mark.parametrize("name", ["nope", "builder_completed", ""])
    def test_an_event_outside_the_set_is_narrated_as_unrecognised(self, name):
        assert narrate_run_event(_event(name)) == UNRECOGNISED_TEMPLATE.format(event=name)

    def test_an_unrecognised_event_invents_no_description(self):
        sentence = narrate_run_event(_event("mystery_event"))
        assert "mystery_event" in sentence
        assert sentence == UNRECOGNISED_TEMPLATE.format(event="mystery_event")

    @pytest.mark.parametrize("broken", [{}, {"event": None}, {"event": 7},
                                        {"event": ["not", "a", "string"]}])
    def test_a_malformed_event_never_raises(self, broken):
        assert isinstance(narrate_run_event(broken), str)


class TestMissingFields:
    def test_an_absent_template_field_renders_as_unknown(self):
        sentence = narrate_run_event(_event("task_run_started"))
        assert UNKNOWN_FIELD in sentence

    def test_a_present_field_is_used_verbatim(self):
        sentence = narrate_run_event(_event("task_run_started", task_id="task-42"))
        assert "task-42" in sentence
        assert UNKNOWN_FIELD not in sentence


class TestDeterminism:
    def test_two_passes_over_one_run_log_are_byte_identical(self):
        events = [_event(name, task_id="t1", outcome="changed", message="m")
                  for name in sorted(NARRATED_EVENTS)] + [_event("unlisted")]
        first = narrate_run_events(events)
        second = narrate_run_events(events)
        assert first == second
        assert "\n".join(first).encode() == "\n".join(second).encode()

    def test_the_callers_order_is_preserved(self):
        events = [_event("verification_passed"), _event("job_created")]
        assert narrate_run_events(events) == [
            NARRATED_EVENTS["verification_passed"],
            NARRATED_EVENTS["job_created"],
        ]

    def test_an_empty_run_log_narrates_to_nothing(self):
        assert narrate_run_events([]) == []


class TestZeroCostGuards:
    def test_the_module_reaches_no_model_network_or_writer(self):
        source = Path(teacher_narration.__file__).read_text(encoding="utf-8")
        body = "\n".join(line for line in source.split("\n")
                         if not line.lstrip().startswith("#"))
        for banned in ("requests", "httpx", "socket", "subprocess", "openai",
                       "ollama", "RunLogWriter", "open(", "write_text"):
            assert banned not in body, banned

    def test_narration_needs_no_data_dir_and_opens_nothing(self):
        # The module takes events, never a path: the read stays with the
        # production reader, which is what keeps the teacher read-only.
        import inspect

        for fn in (narrate_run_event, narrate_run_events):
            params = list(inspect.signature(fn).parameters)
            assert params in (["event"], ["events"]), params
