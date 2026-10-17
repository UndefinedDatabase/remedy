"""`pi_loop_limits`: one Pi call's agent loop ends at its turn or input-token cap (exec-1017 D4).

The end-to-end cases run the fake `pi` of `test_pi_provider` inside the real tool sandbox: it writes
its edit, prints a scripted event stream and then sleeps, so only Remedy's own limit can end it early.
"""
from __future__ import annotations

import time
from types import SimpleNamespace

import pytest

from packages.orchestration import pi_loop_limits as PLL
from packages.orchestration.pi_loop_limits import PiLoopLimits, PiLoopWatch
from packages.orchestration.pi_provider import PiProvider
from packages.orchestration.pingpong_loop import provider_failure_status
from tests.orchestration.test_pi_provider import _event, fake_pi, good_stream, workspace  # noqa: F401


def _turn(n_input: int, *, wants_tool: bool) -> list[str]:
    lines = [_event({"type": "message_end", "message": {
        "role": "assistant", "content": [{"type": "text", "text": "" if wants_tool else "done"}],
        "stopReason": "toolUse" if wants_tool else "stop",
        "usage": {"input": n_input, "output": 5, "cacheRead": 0, "cacheWrite": 0, "totalTokens": n_input + 5}}})]
    if wants_tool:
        lines.append(_event({"type": "tool_execution_start", "toolName": "bash"}))
    return lines


def _runaway(turns: int, n_input: int = 1000) -> list[str]:
    """A loop that never stops asking for tools (a model re-reading and re-checking forever)."""
    return [line for _ in range(turns) for line in _turn(n_input, wants_tool=True)]


def _watch(stream: list[str], **limits) -> PiLoopWatch:
    watch = PiLoopWatch(PiLoopLimits(**{"max_turns": 40, "max_input_tokens": 400_000, **limits}))
    for line in stream:
        watch.feed(line.encode())
    return watch


def test_the_loop_trips_only_when_it_has_used_its_turns_and_asks_for_more():
    assert _watch(_runaway(3), max_turns=3).tripped                 # the 3rd answer asks for a 4th turn
    assert not _watch(_runaway(2), max_turns=3).tripped
    final = _runaway(2) + _turn(10, wants_tool=False)               # three turns, the last a final answer
    assert not _watch(final, max_turns=3).tripped


def test_the_loop_trips_on_its_input_tokens_and_the_message_names_the_cap():
    watch = _watch(_runaway(3, n_input=50_000), max_input_tokens=100_000)
    assert watch.tripped == ("the agent loop used 100000 input tokens over 2 turns, at or above its cap "
                             "of 100000 (default), and asked for another tool")


def test_a_malformed_line_never_raises_from_the_pump_thread():
    watch = _watch(["not json\n"] + _runaway(1))
    assert watch.summary().model_turns == 1


def test_the_jobs_tokens_left_lower_the_input_cap(monkeypatch):
    # The operator's own user config may set both caps (the workstation's sets 12 turns and 60,000
    # tokens); this test is about the defaults and the job's tokens left, so no config is read.
    import packages.orchestration.config as config_module
    monkeypatch.setattr(config_module, "get_config", lambda *a, **k: {})
    job = SimpleNamespace(budgets={"max_total_tokens": 30_000}, budget_actuals={"total_tokens": 25_000})
    PLL.bind_job_token_budget(job)
    limits = PLL.pi_loop_limits()
    assert (limits.max_input_tokens, limits.input_source) == (5_000, "job_tokens_left")
    PLL.bind_job_token_budget(SimpleNamespace(budgets=None, budget_actuals={}))
    assert PLL.pi_loop_limits().max_input_tokens == PLL.PI_MAX_INPUT_TOKENS_PER_CALL_DEFAULT


def test_a_capped_loop_ends_budget_exhausted_and_is_never_retried():
    error = "provider_error: pi_loop_limit: the agent loop used its 40 model turns"
    assert provider_failure_status(error) == "budget_exhausted"
    from packages.orchestration.provider_timeouts import is_nonzero_exit_error, is_timeout_error
    assert not is_timeout_error(error) and not is_nonzero_exit_error(error)


@pytest.mark.parametrize("role", ["builder", "reviewer"])
def test_a_runaway_pi_call_is_ended_early_and_keeps_its_work_and_its_usage(fake_pi, workspace, monkeypatch, role):  # noqa: F811
    monkeypatch.setenv("REMEDY_PI_MAX_TURNS_PER_CALL", "2")
    fake_pi.behave(stdout=_runaway(6), edits={"README.md": "appended\n"}, sleep=60)
    provider = PiProvider(role=role, cwd=str(workspace))

    began = time.monotonic()
    out = provider.build("x") if role == "builder" else provider.review("x")

    assert time.monotonic() - began < 30                  # not the fake's 60 s sleep
    if role == "builder":
        # Lab order of 2026-10-17: a capped builder's edits go to review instead of being dropped.
        assert out.error == "" and "Remedy ended this builder loop at its cap" in out.raw_text
    else:
        assert out.error.startswith("provider_error: pi_loop_limit: the agent loop used its 2 model turns")
    assert out.usage_actuals["model_turns"] == 6 and out.usage_actuals["input_tokens"] == 6000
    assert (workspace / "README.md").read_text().endswith("appended\n")      # the work is kept
    evidence = provider.last_evidence
    assert evidence["loop_limits"]["max_turns"] == 2 and evidence["loop_limit_tripped"]
    assert (evidence["model_turns"], evidence["tool_calls"][:2]) == (6, ["bash", "bash"])


def test_an_ordinary_call_is_not_touched_by_the_limits(fake_pi, workspace):  # noqa: F811
    fake_pi.behave(stdout=good_stream(turns=3))
    out = PiProvider(role="builder", cwd=str(workspace)).build("x")
    assert out.error == "" and out.usage_actuals["model_turns"] == 3


def test_a_pi_calls_usage_reaches_the_call_statistics_as_measured(fake_pi, workspace):  # noqa: F811
    """exec-1017 D3: `remedy stats calls --job 84b0cc4272164bb2` read all four Pi calls as unmeasured."""
    from packages.orchestration.call_tokens import _tokens
    from packages.orchestration.pingpong_loop import _attempt_usage_evidence

    out = PiProvider(role="builder", cwd=str(workspace)).build("x")

    evidence = _attempt_usage_evidence(out.usage_actuals)
    assert _tokens(evidence["usage"]) == {"input": 200, "output": 20, "cache_creation": 0, "cache_read": 0}


def test_the_builder_is_told_remedy_runs_the_tests_and_to_stop_after_the_edit():
    from packages.orchestration.pi_provider import _BUILDER_PREAMBLE
    assert "Do NOT run the project's tests" in _BUILDER_PREAMBLE
    assert "then stop" in _BUILDER_PREAMBLE


def test_a_budget_stop_after_the_last_task_is_moot_and_any_other_stop_is_kept():
    """Lab calc order of 2026-10-17: a built, reviewed and passed task was stopped over the token cap."""
    from packages.orchestration.safe_points import moot_budget_stop

    budget = SimpleNamespace(source="budget", reason="budget_exhausted:max_total_tokens")
    operator = SimpleNamespace(source="operator", reason="operator_stop: x")
    assert moot_budget_stop(budget, []) is None
    assert moot_budget_stop(budget, ["next task"]) is budget
    assert moot_budget_stop(operator, []) is operator
    assert moot_budget_stop(None, []) is None


def test_the_reviewer_is_told_the_diff_is_complete_and_not_to_search():
    from packages.orchestration.pi_provider import _REVIEWER_PREAMBLE
    assert "do not list or search" in _REVIEWER_PREAMBLE and "do not run" in _REVIEWER_PREAMBLE
