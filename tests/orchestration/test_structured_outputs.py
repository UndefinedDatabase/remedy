"""F005 T002/T003 — enforced structured-output engine, reviewer and planner.

Every scenario is deterministic and driven by fake providers / recorded outputs.
No provider tokens are spent.
"""
from __future__ import annotations

import json

import pytest

from packages.orchestration.schemas import (
    PARSE_ERROR_CLASS,
    PlannerPlan,
    ReviewVerdict,
)
from packages.orchestration.structured_outputs import (
    build_schema_prompt,
    planner_structured_enabled,
    reviewer_structured_enabled,
    run_structured_call,
)
from packages.orchestration.structured_planner import (
    StructuredParseError,
    make_structured_planner,
)
from packages.orchestration.pingpong_provider import _parse_reviewer_structured

VALID_REVIEW = json.dumps({
    "schema_v": "rv1", "verdict": "pass", "findings": [],
    "confidence": "high", "summary": "ok",
})
VALID_PLAN = json.dumps({
    "schema_v": "pp1", "summary": "s",
    "proposed_tasks": [{"task_type": "implement", "description": "d"}],
})


def _fake(sequence):
    """A fake raw-text provider returning ``sequence[attempt]``; counts calls."""
    calls = {"n": 0, "prompts": []}

    def _call(prompt, attempt):
        calls["prompts"].append(prompt)
        calls["n"] += 1
        return sequence[attempt]

    return _call, calls


# ---------------------------------------------------------------------------
# Ten deterministic structured-output scenarios — none unclassified
# ---------------------------------------------------------------------------

# Each: (model, [output per attempt], expect_ok, expect_calls)
_SCENARIOS = [
    ("valid review, first try", ReviewVerdict, [VALID_REVIEW], True, 1),
    ("valid planner, first try", PlannerPlan, [VALID_PLAN], True, 1),
    ("review missing required field", ReviewVerdict,
     ['{"schema_v":"rv1","confidence":"high","summary":"x"}'] * 2, False, 2),
    ("review wrong enum", ReviewVerdict,
     ['{"schema_v":"rv1","verdict":"maybe","confidence":"high","summary":"x"}'] * 2, False, 2),
    ("review wrong type", ReviewVerdict,
     ['{"schema_v":"rv1","verdict":"pass","confidence":"high","summary":5}'] * 2, False, 2),
    ("review unsupported schema_v", ReviewVerdict,
     ['{"schema_v":"rv9","verdict":"pass","confidence":"high","summary":"x"}'] * 2, False, 2),
    ("review extra field forbidden", ReviewVerdict,
     ['{"schema_v":"rv1","verdict":"pass","confidence":"high","summary":"x","boom":1}'] * 2, False, 2),
    ("planner empty tasks", PlannerPlan,
     ['{"schema_v":"pp1","summary":"s","proposed_tasks":[]}'] * 2, False, 2),
    ("review not JSON", ReviewVerdict, ["totally not json"] * 2, False, 2),
    ("review recovers on retry", ReviewVerdict, ["garbage", VALID_REVIEW], True, 2),
    ("planner recovers on retry", PlannerPlan, ["nope", VALID_PLAN], True, 2),
]


class TestTenDeterministicScenarios:
    @pytest.mark.parametrize("name,model,outputs,ok,calls", _SCENARIOS,
                             ids=[s[0] for s in _SCENARIOS])
    def test_scenario(self, name, model, outputs, ok, calls):
        call_fn, counter = _fake(outputs)
        outcome = run_structured_call(model, "base prompt", call_fn)
        assert outcome.ok is ok, (name, outcome.hint)
        assert counter["n"] == calls, f"{name}: made {counter['n']} calls, expected {calls}"
        if not ok:
            # Every failure is CLASSIFIED as parse — never unclassified.
            assert outcome.error_class == PARSE_ERROR_CLASS
            assert outcome.hint, "a parse failure must carry a hint"
        else:
            assert outcome.value is not None
            assert outcome.error_class == ""

    def test_no_scenario_is_unclassified(self):
        for name, model, outputs, ok, _ in _SCENARIOS:
            call_fn, _ = _fake(outputs)
            outcome = run_structured_call(model, "p", call_fn)
            classified = outcome.ok or outcome.error_class == PARSE_ERROR_CLASS
            assert classified, f"{name} produced an unclassified result"


# ---------------------------------------------------------------------------
# Retry semantics — at most one, never more; the retry carries only the hint
# ---------------------------------------------------------------------------

class TestParseRetrySemantics:
    def test_exactly_one_retry_then_stop(self):
        # Three bad outputs available, but only two calls may ever be made.
        call_fn, counter = _fake(["bad1", "bad2", "bad3"])
        outcome = run_structured_call(ReviewVerdict, "p", call_fn)
        assert counter["n"] == 2, "engine must stop after exactly one parse retry"
        assert not outcome.ok and outcome.error_class == PARSE_ERROR_CLASS
        assert outcome.parse_retried is True

    def test_valid_first_time_makes_no_retry(self):
        call_fn, counter = _fake([VALID_REVIEW])
        outcome = run_structured_call(ReviewVerdict, "p", call_fn)
        assert counter["n"] == 1 and outcome.parse_retried is False

    def test_retry_prompt_carries_only_the_hint_not_the_bad_text(self):
        call_fn, counter = _fake(["nonsense-bad-text", VALID_REVIEW])
        run_structured_call(ReviewVerdict, "BASE", call_fn)
        retry_prompt = counter["prompts"][1]
        assert "Your previous response was invalid" in retry_prompt
        assert "nonsense-bad-text" not in retry_prompt  # the bad text is not echoed

    def test_schema_v_recorded_per_call(self):
        seen = []
        call_fn, _ = _fake(["bad", VALID_REVIEW])
        run_structured_call(ReviewVerdict, "p", call_fn,
                            on_call=lambda attempt, sv, is_pr, prompt: seen.append((attempt, sv)))
        assert seen == [(1, "rv1"), (2, "rv1")]

    def test_call_log_counts_the_retry(self):
        call_fn, _ = _fake(["bad", VALID_REVIEW])
        outcome = run_structured_call(ReviewVerdict, "p", call_fn)
        assert len(outcome.call_log) == 2  # provider-call accounting includes the retry
        assert outcome.call_log[0]["is_parse_retry"] is False
        assert outcome.call_log[1]["is_parse_retry"] is True


# ---------------------------------------------------------------------------
# Prompt shape — the schema (with schema_v) is always sent
# ---------------------------------------------------------------------------

class TestSchemaPrompt:
    def test_prompt_includes_schema_v_and_schema(self):
        p = build_schema_prompt(ReviewVerdict, "review this")
        assert "schema_v=rv1" in p
        assert '"verdict"' in p  # the JSON schema itself is present
        assert p.startswith("review this")

    def test_planner_prompt_includes_schema_v(self):
        assert "schema_v=pp1" in build_schema_prompt(PlannerPlan, "plan this")


# ---------------------------------------------------------------------------
# Reviewer structured parser -> ReviewerOutput mapping
# ---------------------------------------------------------------------------

class TestReviewerStructuredMapping:
    def test_valid_maps_to_reviewer_output(self):
        out = _parse_reviewer_structured(VALID_REVIEW, 12, 7, provider="fake")
        assert out.verdict == "pass"
        assert out.schema_v == "rv1"
        assert not out.error

    def test_invalid_is_classified_parse_with_hint(self):
        out = _parse_reviewer_structured('{"schema_v":"rv1","verdict":"nope"}', 1, 1, provider="fake")
        assert out.error.startswith("malformed_output:")  # loop parse-retry key
        assert out.parse_hint
        assert out.schema_v == "rv1"

    def test_findings_are_mapped(self):
        raw = json.dumps({
            "schema_v": "rv1", "verdict": "needs_repair",
            "findings": [{"id": "F1", "severity": "high", "file": "a.py",
                          "summary": "bug", "required_fix": "fix it"}],
            "confidence": "medium", "summary": "one bug",
        })
        out = _parse_reviewer_structured(raw, 1, 1, provider="fake")
        assert out.verdict == "needs_repair"
        assert out.findings[0].id == "F1" and out.findings[0].severity == "high"


# ---------------------------------------------------------------------------
# Structured planner wrapper
# ---------------------------------------------------------------------------

class TestStructuredPlanner:
    def test_valid_plan_maps_to_planner_output(self):
        cp = make_structured_planner(lambda p, a: VALID_PLAN)
        out = cp("plan it")
        assert out.summary == "s"
        assert out.proposed_tasks[0].task_type == "implement"

    def test_recovers_on_single_retry(self):
        call_fn, counter = _fake(["bad", VALID_PLAN])
        out = make_structured_planner(call_fn)("plan")
        assert out.summary == "s" and counter["n"] == 2

    def test_two_invalid_raises_classified_parse_error(self):
        call_fn, counter = _fake(["bad", "worse", "never"])
        with pytest.raises(StructuredParseError) as ei:
            make_structured_planner(call_fn)("plan")
        assert ei.value.error_class == PARSE_ERROR_CLASS
        assert ei.value.calls == 2  # exactly one retry
        assert counter["n"] == 2


# ---------------------------------------------------------------------------
# Compatibility flags
# ---------------------------------------------------------------------------

class TestCompatibilityFlags:
    def test_reviewer_structured_on_by_default(self, monkeypatch):
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        assert reviewer_structured_enabled() is True

    def test_reviewer_freetext_flag_disables_structured(self, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
        assert reviewer_structured_enabled() is False

    def test_planner_structured_on_by_default(self, monkeypatch):
        monkeypatch.delenv("REMEDY_PLANNER_FREETEXT", raising=False)
        assert planner_structured_enabled() is True

    def test_planner_freetext_flag_disables_structured(self, monkeypatch):
        monkeypatch.setenv("REMEDY_PLANNER_FREETEXT", "true")
        assert planner_structured_enabled() is False


# ---------------------------------------------------------------------------
# Prompt trace records schema_v for the reviewer call
# ---------------------------------------------------------------------------

class TestPromptTraceSchemaV:
    def test_reviewer_trace_schema_v_present_in_structured_mode(self, monkeypatch):
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        from packages.orchestration.pingpong_loop import _reviewer_schema_v
        from packages.orchestration.prompt_trace import build_trace_entry, trace_entry_to_dict
        entry = build_trace_entry(prompt_text="review", role="reviewer",
                                  schema_v=_reviewer_schema_v())
        assert trace_entry_to_dict(entry)["schema_v"] == "rv1"

    def test_reviewer_trace_schema_v_blank_in_compat_mode(self, monkeypatch):
        monkeypatch.setenv("REMEDY_REVIEWER_FREETEXT", "1")
        from packages.orchestration.pingpong_loop import _reviewer_schema_v
        assert _reviewer_schema_v() == ""

