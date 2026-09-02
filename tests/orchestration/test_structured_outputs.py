"""F005 T002/T003 — enforced structured-output engine, reviewer and planner.

Every scenario is deterministic and driven by fake providers / recorded outputs.
No provider tokens are spent.
"""
from __future__ import annotations

import json

import pytest

from packages.orchestration.pingpong_provider import _parse_reviewer_structured
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


# ---------------------------------------------------------------------------
# F005 Finding 2 — hard single-retry ceiling (boolean, not an integer knob)
# ---------------------------------------------------------------------------

class TestHardRetryCeiling:
    def test_retry_disabled_makes_one_call(self):
        call_fn, n = _fake(["bad", "bad2"])
        o = run_structured_call(ReviewVerdict, "p", call_fn, allow_parse_retry=False)
        assert n["n"] == 1 and not o.ok and o.error_class == PARSE_ERROR_CLASS

    def test_retry_enabled_makes_at_most_two_calls(self):
        call_fn, n = _fake(["bad", "bad2", "bad3"])
        run_structured_call(ReviewVerdict, "p", call_fn, allow_parse_retry=True)
        assert n["n"] == 2

    def test_truthy_non_bool_is_clamped_to_one_retry(self):
        # A caller that tries to smuggle a larger value cannot get 3+ calls.
        call_fn, n = _fake(["b", "b", "b", "b", "b", "b"])
        run_structured_call(ReviewVerdict, "p", call_fn, allow_parse_retry=5)
        assert n["n"] == 2

    def test_no_public_integer_retry_knob(self):
        import inspect
        sig = inspect.signature(run_structured_call)
        assert "max_parse_retries" not in sig.parameters
        assert sig.parameters["allow_parse_retry"].annotation in (bool, "bool")


# ---------------------------------------------------------------------------
# F005 Finding 3 — native schema mode: short instruction, no duplicated schema
# ---------------------------------------------------------------------------

class TestNativeSchemaMode:
    def test_native_prompt_has_short_instruction_not_full_schema(self):
        from packages.orchestration.structured_outputs import native_schema_prompt
        p = native_schema_prompt("review this")
        assert p.startswith("review this")
        assert "schema-compliant" in p
        assert '"$defs"' not in p and '"properties"' not in p  # no full schema

    def test_native_run_does_not_embed_full_schema(self):
        seen = {}
        def cap(prompt, attempt):
            seen["prompt"] = prompt
            return VALID_REVIEW
        run_structured_call(ReviewVerdict, "BASE", cap, native_schema=True)
        assert '"$defs"' not in seen["prompt"]
        assert "schema-compliant" in seen["prompt"]

    def test_claude_cli_native_schema_argv(self):
        from packages.orchestration.pingpong_provider import build_claude_cli_args
        from packages.orchestration.schemas import to_json_schema_str
        sch = to_json_schema_str(ReviewVerdict)
        argv = build_claude_cli_args("claude", "prompt", json_schema=sch)
        assert "--json-schema" in argv
        assert argv[argv.index("--json-schema") + 1] == sch
        # default path never passes it
        assert "--json-schema" not in build_claude_cli_args("claude", "prompt")
        # stream mode still supports it
        assert "--json-schema" in build_claude_cli_args("claude", "p", stream_evidence=True, json_schema=sch)


# ---------------------------------------------------------------------------
# F005 Finding 6 — reviewer parse exhaustion carries a stable error_class
# ---------------------------------------------------------------------------

class TestReviewerErrorClass:
    def test_structured_parse_failure_sets_error_class_parse(self):
        out = _parse_reviewer_structured('{"schema_v":"rv1","verdict":"nope"}', 1, 1, provider="fake")
        assert out.error_class == "parse"
        assert out.error.startswith("malformed_output:")  # human-readable detail kept

    def test_valid_review_has_no_error_class(self):
        out = _parse_reviewer_structured(VALID_REVIEW, 1, 1, provider="fake")
        assert out.error_class == ""


# ---------------------------------------------------------------------------
# F005 Finding 5 — reviewer prompt-trace count == reviewer provider attempts
# ---------------------------------------------------------------------------

class TestReviewerParseRetryTraces:
    def test_recoverable_reviewer_parse_failure_makes_two_traces(self, tmp_path, monkeypatch):
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_provider import ReviewerOutput

        class _FlakyReviewer:
            """Returns a classified parse failure once, then a valid verdict."""
            def __init__(self):
                self.calls = 0
            def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):
                self.calls += 1
                if self.calls == 1:
                    return ReviewerOutput(
                        verdict="blocked",
                        error="malformed_output: verdict: Field required",
                        error_class="parse",
                        parse_hint="verdict: Field required",
                        schema_v="rv1",
                        raw_text="not json",
                        provider="fake",
                    )
                return ReviewerOutput(
                    verdict="pass", confidence="high", summary="ok",
                    schema_v="rv1", provider="fake",
                )

        reviewer = _FlakyReviewer()
        result = run_pingpong(
            "test goal", str(tmp_path),
            builder_name="fake", reviewer_name="fake",
            reviewer_provider=reviewer,
            max_rounds=1,
        )

        assert reviewer.calls == 2, "expected exactly one reviewer parse retry"
        assert result.reviewer_parse_retry_count == 1

        rev_traces = [t for t in result.prompt_traces if t.role == "reviewer"]
        assert len(rev_traces) == 2, f"reviewer traces {len(rev_traces)} != 2 attempts"
        assert all(t.schema_v == "rv1" for t in rev_traces)
        kinds = [t.prompt_kind for t in rev_traces]
        assert kinds[0] in ("review", "re-review")
        assert kinds[1] == "review-parse-retry"


# ---------------------------------------------------------------------------
# F005 Finding 5 — prompt trace hash-matches the exact prompt sent to _call
# F005 Finding 4 — failed structured attempt + valid retry reconcile 2/2/2
# ---------------------------------------------------------------------------

class _RecordingReviewer:
    """Records the exact prompt strings it receives; returns scripted outputs."""
    def __init__(self, outputs):
        self.prompts = []
        self._outputs = outputs
        self._i = 0
    def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume: str | None = None):
        self.prompts.append(prompt)
        out = self._outputs[min(self._i, len(self._outputs) - 1)]
        self._i += 1
        return out


class TestReviewerPromptTraceHashEquality:
    def test_initial_and_retry_traces_hash_match_sent_prompts(self, tmp_path, monkeypatch):
        import hashlib
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_provider import ReviewerOutput

        outputs = [
            ReviewerOutput(verdict="blocked", error="malformed_output: verdict: Field required",
                           error_class="parse", parse_hint="verdict: Field required",
                           schema_v="rv1", raw_text="bad", provider="fake",
                           usage_actuals={"input_tokens": 40, "output_tokens": 4,
                                          "total_cost_usd": 0.001, "parse_source": "claude_cli_json"}),
            ReviewerOutput(verdict="pass", confidence="high", summary="ok", schema_v="rv1",
                           provider="fake",
                           usage_actuals={"input_tokens": 42, "output_tokens": 5,
                                          "total_cost_usd": 0.0011, "parse_source": "claude_cli_json"}),
        ]
        reviewer = _RecordingReviewer(outputs)
        result = run_pingpong("goal", str(tmp_path), builder_name="fake",
                              reviewer_name="fake", reviewer_provider=reviewer, max_rounds=1)

        assert len(reviewer.prompts) == 2  # initial + one parse retry
        rev_traces = [t for t in result.prompt_traces if t.role == "reviewer"]
        assert len(rev_traces) == 2
        for trace, sent in zip(rev_traces, reviewer.prompts):
            assert trace.prompt_sha256 == hashlib.sha256(sent.encode()).hexdigest()
            assert trace.prompt_chars == len(sent)

    def test_two_call_usage_reconciles(self, tmp_path, monkeypatch):
        monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
        from packages.orchestration.pingpong_loop import run_pingpong
        from packages.orchestration.pingpong_provider import ReviewerOutput

        outputs = [
            ReviewerOutput(verdict="blocked", error="malformed_output: exhausted",
                           error_class="parse", parse_hint="exhausted", schema_v="rv1",
                           provider="fake",
                           usage_actuals={"input_tokens": 50, "output_tokens": 5,
                                          "total_cost_usd": 0.001, "parse_source": "claude_cli_json"}),
            ReviewerOutput(verdict="pass", confidence="high", summary="ok", schema_v="rv1",
                           provider="fake",
                           usage_actuals={"input_tokens": 60, "output_tokens": 6,
                                          "total_cost_usd": 0.002, "parse_source": "claude_cli_json"}),
        ]
        reviewer = _RecordingReviewer(outputs)
        result = run_pingpong("goal", str(tmp_path), builder_name="fake",
                              reviewer_name="fake", reviewer_provider=reviewer, max_rounds=1)

        rev_attempts = [a for a in result.provider_attempts if a.role == "reviewer"]
        assert len(rev_attempts) == 2, "failed structured call + retry = 2 provider attempts"
        assert all(a.usage_actuals is not None for a in rev_attempts)
        assert result.reviewer_parse_retry_count == 1
        # both a failed and a successful call carry cost
        costs = [a.usage_actuals["total_cost_usd"] for a in rev_attempts]
        assert costs == [0.001, 0.002]


# ---------------------------------------------------------------------------
# F005 Finding 2 — one prompt trace per ACTUAL structured Reviewer call
# ---------------------------------------------------------------------------

def _timeout_out():
    from packages.orchestration.pingpong_provider import ReviewerOutput
    return ReviewerOutput(verdict="blocked", error="provider_error: TimeoutExpired",
                          provider="fake", schema_v="rv1")


def _bad_parse_out():
    from packages.orchestration.pingpong_provider import ReviewerOutput
    return ReviewerOutput(verdict="blocked",
                          error="malformed_output: verdict: Field required",
                          error_class="parse", parse_hint="verdict: Field required",
                          schema_v="rv1", raw_text="bad", provider="fake")


def _good_out():
    from packages.orchestration.pingpong_provider import ReviewerOutput
    return ReviewerOutput(verdict="pass", confidence="high", summary="ok",
                          schema_v="rv1", provider="fake")


def _provider_err_out():
    from packages.orchestration.pingpong_provider import ReviewerOutput
    return ReviewerOutput(verdict="blocked", error="provider_error: auth failed",
                          error_class="provider_error", provider="fake", schema_v="rv1")


def _run_loop(tmp_path, outputs, monkeypatch):
    """Run one pingpong round with a scripted, prompt-recording reviewer."""
    monkeypatch.delenv("REMEDY_REVIEWER_FREETEXT", raising=False)
    import packages.orchestration.pingpong_loop as pl
    monkeypatch.setattr(pl._time, "sleep", lambda *_a, **_k: None)  # no backoff wait
    reviewer = _RecordingReviewer(outputs)
    result = pl.run_pingpong("goal", str(tmp_path), builder_name="fake",
                             reviewer_name="fake", reviewer_provider=reviewer,
                             max_rounds=1)
    traces = [t for t in result.prompt_traces if t.role == "reviewer"]
    attempts = [a for a in result.provider_attempts if a.role == "reviewer"]
    return result, reviewer, traces, attempts


class TestReviewerTraceEqualsAttempts:
    def test_1_transport_retry_then_success(self, tmp_path, monkeypatch):
        result, rev, traces, attempts = _run_loop(
            tmp_path, [_timeout_out(), _good_out()], monkeypatch)
        assert len(attempts) == 2 and len(traces) == 2
        assert len(rev.prompts) == 2
        # one LOGICAL review prompt, sent twice
        assert rev.prompts[0] == rev.prompts[1]
        assert [t.phase for t in traces] == ["review", "review"]
        assert [t.is_transport_retry for t in traces] == [False, True]
        assert [t.transport_attempt for t in traces] == [1, 2]
        assert result.reviewer_parse_retry_count == 0

    def test_2_parse_retry_then_success(self, tmp_path, monkeypatch):
        result, rev, traces, attempts = _run_loop(
            tmp_path, [_bad_parse_out(), _good_out()], monkeypatch)
        assert len(attempts) == 2 and len(traces) == 2
        assert [t.phase for t in traces] == ["review", "parse-retry"]
        assert traces[1].is_transport_retry is False
        assert result.reviewer_parse_retry_count == 1

    def test_3_parse_retry_times_out_once_then_succeeds(self, tmp_path, monkeypatch):
        result, rev, traces, attempts = _run_loop(
            tmp_path, [_bad_parse_out(), _timeout_out(), _good_out()], monkeypatch)
        assert len(attempts) == 3 and len(traces) == 3
        assert [t.phase for t in traces] == ["review", "parse-retry", "parse-retry"]
        # the final attempt is BOTH the parse phase and a transport retry
        assert traces[2].is_transport_retry is True
        assert traces[2].transport_attempt == 2
        # still exactly ONE logical parse retry
        assert result.reviewer_parse_retry_count == 1
        assert sum(1 for a in attempts if a.is_parse_retry) == 2  # both parse-phase calls

    def test_4_no_retry_single_attempt_single_trace(self, tmp_path, monkeypatch):
        result, rev, traces, attempts = _run_loop(tmp_path, [_good_out()], monkeypatch)
        assert len(attempts) == 1 and len(traces) == 1
        assert traces[0].phase == "review" and traces[0].transport_attempt == 1
        assert result.reviewer_parse_retry_count == 0

    def test_5_every_trace_hash_matches_the_sent_prompt(self, tmp_path, monkeypatch):
        import hashlib
        _result, rev, traces, attempts = _run_loop(
            tmp_path, [_bad_parse_out(), _timeout_out(), _good_out()], monkeypatch)
        assert len(traces) == len(rev.prompts) == len(attempts)
        for trace, sent in zip(traces, rev.prompts):
            assert trace.prompt_sha256 == hashlib.sha256(sent.encode()).hexdigest()
            assert trace.prompt_chars == len(sent)

    def test_all_traces_carry_schema_v(self, tmp_path, monkeypatch):
        _r, _rev, traces, _a = _run_loop(
            tmp_path, [_bad_parse_out(), _timeout_out(), _good_out()], monkeypatch)
        assert all(t.schema_v == "rv1" for t in traces)

    def test_provider_error_does_not_consume_the_parse_retry(self, tmp_path, monkeypatch):
        # An ordinary provider error is retried as transport, never as a parse retry.
        result, _rev, traces, attempts = _run_loop(
            tmp_path, [_provider_err_out(), _provider_err_out(), _provider_err_out()],
            monkeypatch)
        assert result.reviewer_parse_retry_count == 0
        assert all(t.phase == "review" for t in traces)
        assert len(traces) == len(attempts)
