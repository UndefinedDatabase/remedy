"""F013 T002 — intake module: LLM + heuristic paths, truncation, evidence."""
from __future__ import annotations

import json

from packages.orchestration.intake import (
    _MAX_PROMPT_MISSION_CHARS,
    MAX_CLARIFICATIONS,
    _extract_context_refs,
    _first_sentence,
    heuristic_intake,
    run_intake,
)
from packages.orchestration.schemas import JOB_INTAKE_SCHEMA_V

_VALID_INTAKE = {
    "schema_v": "ji1",
    "goal": "Add pagination to the user list endpoint.",
    "context_refs": ["src/api/users.py"],
    "constraints": ["No breaking API changes"],
    "acceptance_hints": ["GET /users?page=2 returns page 2"],
    "truncated_input": False,
    "clarifications": [],
}


def _make_call_fn(*responses: str):
    """Stateful fake provider returning responses in order."""
    state = {"idx": 0}

    def _call(prompt: str, attempt: int) -> str:
        i = state["idx"]
        state["idx"] += 1
        return responses[i] if i < len(responses) else responses[-1]

    return _call


class TestHeuristicIntake:
    def test_source_is_heuristic(self):
        r = heuristic_intake("Fix the login bug.")
        assert r.source == "heuristic"
        assert r.calls == 0

    def test_goal_is_first_sentence(self):
        r = heuristic_intake("Fix the login bug. Then add tests.")
        assert r.value.goal == "Fix the login bug."

    def test_goal_newline_separator(self):
        r = heuristic_intake("Fix the login bug\nThen add tests.")
        assert r.value.goal == "Fix the login bug"

    def test_goal_long_text_capped(self):
        r = heuristic_intake("x" * 300)
        assert len(r.value.goal) <= 200

    def test_context_refs_extracted(self):
        r = heuristic_intake("Update src/api/users.py and docs/pagination.md")
        assert "src/api/users.py" in r.value.context_refs
        assert "docs/pagination.md" in r.value.context_refs

    def test_context_refs_deduped(self):
        r = heuristic_intake("Fix src/main.py, then recheck src/main.py")
        assert r.value.context_refs.count("src/main.py") == 1

    def test_empty_lists_by_default(self):
        r = heuristic_intake("Fix the bug.")
        assert r.value.constraints == []
        assert r.value.acceptance_hints == []
        assert r.value.clarifications == []

    def test_truncated_input_flag(self):
        long_mission = "x" * (_MAX_PROMPT_MISSION_CHARS + 100)
        r = heuristic_intake(long_mission)
        assert r.value.truncated_input is True

    def test_short_mission_not_truncated(self):
        r = heuristic_intake("Short mission.")
        assert r.value.truncated_input is False

    def test_schema_v_is_ji1(self):
        r = heuristic_intake("Test.")
        assert r.value.schema_v == "ji1"
        assert r.schema_v == JOB_INTAKE_SCHEMA_V


class TestRunIntakeValid:
    def test_valid_response(self):
        r = run_intake("Add pagination", _make_call_fn(json.dumps(_VALID_INTAKE)))
        assert r.source == "llm"
        assert r.value.goal == _VALID_INTAKE["goal"]
        assert r.calls == 1
        assert r.error_hint == ""

    def test_retry_then_valid(self):
        r = run_intake(
            "Add pagination",
            _make_call_fn("not json", json.dumps(_VALID_INTAKE)),
        )
        assert r.source == "llm"
        assert r.calls == 2

    def test_call_log_recorded(self):
        r = run_intake("Add pagination", _make_call_fn(json.dumps(_VALID_INTAKE)))
        assert len(r.call_log) == 1
        assert r.call_log[0]["ok"] is True


class TestRunIntakeFailure:
    def test_double_failure_falls_to_heuristic(self):
        r = run_intake("Add pagination", _make_call_fn("bad", "still bad"))
        assert r.source == "heuristic"
        assert r.error_hint != ""
        assert r.calls == 2

    def test_provider_error_falls_to_heuristic(self):
        def _explode(prompt: str, attempt: int) -> str:
            raise ConnectionError("provider down")

        r = run_intake("Add pagination", _explode)
        assert r.source == "heuristic"
        assert r.error_hint == "provider error"

    def test_heuristic_fallback_has_goal(self):
        r = run_intake("Fix the login bug.", _make_call_fn("bad", "bad"))
        assert r.value.goal  # non-empty


class TestClarificationTruncation:
    def _make_intake_with_n_clarifications(self, n: int) -> dict:
        return {
            **_VALID_INTAKE,
            "clarifications": [
                {"question": f"q{i}", "default_answer": f"a{i}", "impact": f"i{i}"}
                for i in range(n)
            ],
        }

    def test_within_limit_unchanged(self):
        payload = self._make_intake_with_n_clarifications(3)
        r = run_intake("test", _make_call_fn(json.dumps(payload)))
        assert len(r.value.clarifications) == 3
        assert r.value.dropped_clarifications == 0

    def test_over_limit_truncated(self):
        payload = self._make_intake_with_n_clarifications(8)
        r = run_intake("test", _make_call_fn(json.dumps(payload)))
        assert len(r.value.clarifications) == MAX_CLARIFICATIONS
        assert r.value.dropped_clarifications == 3

    def test_exactly_at_limit(self):
        payload = self._make_intake_with_n_clarifications(MAX_CLARIFICATIONS)
        r = run_intake("test", _make_call_fn(json.dumps(payload)))
        assert len(r.value.clarifications) == MAX_CLARIFICATIONS
        assert r.value.dropped_clarifications == 0

    def test_kept_clarifications_are_first_five(self):
        payload = self._make_intake_with_n_clarifications(8)
        r = run_intake("test", _make_call_fn(json.dumps(payload)))
        questions = [c.question for c in r.value.clarifications]
        assert questions == [f"q{i}" for i in range(MAX_CLARIFICATIONS)]


class TestOnCallHook:
    def test_hook_fires(self):
        calls = []

        def hook(attempt, schema_v, is_retry, prompt):
            calls.append((attempt, schema_v, is_retry))

        run_intake("test", _make_call_fn(json.dumps(_VALID_INTAKE)), on_call=hook)
        assert len(calls) == 1
        assert calls[0] == (1, "ji1", False)

    def test_hook_fires_on_retry(self):
        calls = []

        def hook(attempt, schema_v, is_retry, prompt):
            calls.append((attempt, is_retry))

        run_intake("test", _make_call_fn("bad", json.dumps(_VALID_INTAKE)), on_call=hook)
        assert len(calls) == 2
        assert calls[0] == (1, False)
        assert calls[1] == (2, True)


class TestFirstSentence:
    def test_period_space(self):
        assert _first_sentence("Hello world. More text.") == "Hello world."

    def test_newline(self):
        assert _first_sentence("Hello world\nMore text") == "Hello world"

    def test_no_separator(self):
        assert _first_sentence("Hello world") == "Hello world"

    def test_empty(self):
        assert _first_sentence("") == ""

    def test_whitespace_only(self):
        assert _first_sentence("   ") == ""


class TestExtractContextRefs:
    def test_file_paths(self):
        refs = _extract_context_refs("look at src/api/users.py")
        assert "src/api/users.py" in refs

    def test_bare_filename(self):
        refs = _extract_context_refs("check README.md")
        assert "README.md" in refs

    def test_no_false_positives_on_prose(self):
        refs = _extract_context_refs("This is a sentence about nothing.")
        assert refs == []

    def test_multiple_refs(self):
        refs = _extract_context_refs("fix src/a.py and lib/b.ts")
        assert len(refs) == 2
