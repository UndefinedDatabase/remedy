"""Harness invocations and model turns are different measured values (operator amendment amend1014c, R3).

Synthetic Pi JSONL through the fake `pi` process; the counts are read back from the call records
and compared with the event stream, never from a prose sentence.
"""
from __future__ import annotations

import json
from types import SimpleNamespace

import packages.orchestration.do_summary as DS
from packages.orchestration import data_paths
from packages.orchestration.pi_events import parse_pi_events, summarize_pi_events
from packages.orchestration.pi_provider import PI_DEFAULT_MODEL, PiProvider
from packages.orchestration.pi_turn_counts import pi_turns_for_job, pi_turns_in_run
from tests.orchestration.test_pi_provider import _event, fake_pi, workspace  # noqa: F401 (fixtures)


def _turn(n: int, *, inp: int, out: int, stop: str = "toolUse") -> str:
    return _event({"type": "message_end", "message": {
        "role": "assistant", "provider": "ollama", "model": PI_DEFAULT_MODEL,
        "content": [{"type": "text", "text": f"turn {n}"}], "stopReason": stop,
        "usage": {"input": inp, "output": out, "cacheRead": 5, "cacheWrite": 0, "totalTokens": inp + out + 5}}})


def _stream(turns: list[tuple[int, int]], *, retries: int = 0) -> list[str]:
    lines = [_event({"type": "agent_start"})]
    for _ in range(retries):
        lines.append(_event({"type": "auto_retry_start"}))
    for n, (inp, out) in enumerate(turns, start=1):
        lines.append(_turn(n, inp=inp, out=out, stop="stop" if n == len(turns) else "toolUse"))
    return lines + [_event({"type": "agent_settled", "aborted": False})]


def _run(fake_pi, workspace, tmp_path, stream, run_id="run-1"):
    fake_pi.behave(stdout=stream)
    provider = PiProvider(role="builder", cwd=str(workspace), evidence_dir=str(data_paths.run_dir(run_id)))
    return provider, provider.build("x")


def test_three_assistant_messages_are_three_turns_with_their_own_summed_usage_and_one_invocation(fake_pi, workspace, tmp_path):
    stream = _stream([(100, 10), (200, 20), (300, 30)])
    summary = summarize_pi_events(parse_pi_events("".join(stream).encode()))
    assert summary.model_turns == 3 and summary.usage["input"] == 600 and summary.usage["output"] == 60

    _provider, out = _run(fake_pi, workspace, tmp_path, stream)

    assert out.usage_actuals["model_turns"] == 3 and out.usage_actuals["input_tokens"] == 600
    assert out.usage_actuals["output_tokens"] == 60                      # summed once, not per turn again
    assert pi_turns_in_run("run-1") == {"builder": {"invocations": 1, "model_turns": 3}}


def test_a_retry_stream_counts_every_completed_turn_once(fake_pi, workspace, tmp_path):
    _provider, out = _run(fake_pi, workspace, tmp_path, _stream([(10, 1), (10, 1), (10, 1), (10, 1)], retries=2))
    assert out.usage_actuals["model_turns"] == 4
    assert pi_turns_in_run("run-1")["builder"]["model_turns"] == 4


def test_a_zero_turn_failed_invocation_is_zero_turns_one_invocation_and_no_invented_usage(fake_pi, workspace, tmp_path):
    fake_pi.behave(stdout=["not json\n"], exit=1)
    provider = PiProvider(role="builder", cwd=str(workspace), evidence_dir=str(data_paths.run_dir("run-2")))
    out = provider.build("x")
    assert out.error and out.usage_actuals is None
    assert pi_turns_in_run("run-2") == {"builder": {"invocations": 1, "model_turns": 0}}


def test_runs_of_a_job_add_up_and_a_run_counted_twice_counts_once(fake_pi, workspace, tmp_path):
    _run(fake_pi, workspace, tmp_path, _stream([(1, 1), (1, 1)]), "run-a")
    _run(fake_pi, workspace, tmp_path, _stream([(1, 1)]), "run-b")
    assert pi_turns_for_job(["run-a", "run-b", "run-a"]) == {"builder": {"invocations": 2, "model_turns": 3}}
    assert pi_turns_for_job(["run-without-pi"]) == {}


def _ctx():
    project = SimpleNamespace(id="p")
    return SimpleNamespace(cost_mirrors={"job-1": {"ledger_mirrored": True}}, projects=None, project=project)


def test_the_do_summary_json_and_text_carry_both_counts_and_never_a_bare_call_count(fake_pi, workspace, tmp_path, monkeypatch):
    _run(fake_pi, workspace, tmp_path, _stream([(100, 10), (100, 10), (100, 10)]), "run-s")
    row = SimpleNamespace(bucket="builder", calls=1, tokens_in=300, tokens_out=30, cache_read=15, cost_usd=None)
    other = SimpleNamespace(bucket="planner", calls=2, tokens_in=1, tokens_out=1, cache_read=None, cost_usd=None)
    import packages.orchestration.pingpong_job as PJ
    import packages.orchestration.token_ledger as TL
    monkeypatch.setattr(TL, "query_cost", lambda **kw: SimpleNamespace(rows=[row, other]))
    monkeypatch.setattr(PJ, "load_job_plan", lambda job_id: SimpleNamespace(run_refs=["run-s"], project_id="p"))

    summary = DS.do_cost_summary(_ctx())
    roles = {r["role"]: r for r in summary["roles"]}

    assert (roles["builder"]["harness_invocations"], roles["builder"]["model_turns"]) == (1, 3)
    assert (roles["planner"]["harness_invocations"], roles["planner"]["model_turns"]) == (2, None)
    assert all("calls" not in r for r in summary["roles"])
    text = "\n".join(DS.do_cost_summary_lines(summary))
    assert "(1 harness invocation, 3 model turns)" in text
    assert "(2 harness invocations; model turns not reported)" in text
    assert "call(s)" not in text
    json.dumps(summary)                                                   # machine-readable as is


def test_the_digest_and_the_mission_cockpit_read_the_same_turn_records(fake_pi, workspace, tmp_path, monkeypatch):
    import packages.orchestration.client_digest as CD
    import packages.orchestration.mission_cockpit as MC
    import packages.orchestration.pingpong_job as PJ

    _run(fake_pi, workspace, tmp_path, _stream([(1, 1), (1, 1)]), "run-d")
    monkeypatch.setattr(PJ, "load_job_plan", lambda job_id: SimpleNamespace(run_refs=["run-d"]))

    assert CD._pi_model_turns(["run-d"]) == 2
    assert CD._pi_model_turns(["run-with-no-pi-record"]) is None
    assert MC._order_model_turns(["job-1"]) == 2
    assert MC._order_usage([], None) == {
        "harness_invocations": None, "model_turns": None,
        "tokens": {"input": None, "output": None, "cache_read": None, "cache_creation": None}}
