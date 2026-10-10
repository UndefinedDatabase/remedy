"""Tokens by kind per recorded provider call and per landed change (F302 T004, DECISION F302 D4).

The corpus is run records written under a temporary data root in the shape `run_pingpong` writes
`result.json`; nothing here reads the operator's data root.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.call_tokens import (
    TOKEN_KINDS,
    RecordedCall,
    recorded_calls,
    summarize_call_tokens,
)


def _usage(i, o, cc, cr):
    return {"input_tokens": i, "output_tokens": o, "cache_creation_input_tokens": cc,
            "cache_read_input_tokens": cr}


def _run(root: Path, run_id: str, *, job_id="", finished="2026-10-10T03:00:00+00:00", attempts=()):
    folder = root / "runs" / run_id
    folder.mkdir(parents=True)
    (folder / "result.json").write_text(json.dumps({
        "run_id": run_id, "job_id": job_id, "finished_at": finished,
        "provider_evidence": {"provider_attempts": list(attempts)}}))


def _attempt(role, usage, provider="claude-cli"):
    return {"role": role, "provider": provider, "usage": usage}


class TestRecordedCalls:
    def test_each_attempt_is_one_call_with_its_four_figures(self, tmp_path):
        _run(tmp_path, "r1", job_id="j1", attempts=[_attempt("builder", _usage(12, 4000, 40000, 300000)),
                                                     _attempt("reviewer", _usage(6, 3000, 31000, 93000))])
        calls = recorded_calls(root=tmp_path)
        assert calls == [
            RecordedCall("r1", "j1", "builder", "claude-cli",
                         {"input": 12, "output": 4000, "cache_creation": 40000, "cache_read": 300000}),
            RecordedCall("r1", "j1", "reviewer", "claude-cli",
                         {"input": 6, "output": 3000, "cache_creation": 31000, "cache_read": 93000}),
        ]

    @pytest.mark.parametrize("usage", [None, {}, _usage(1, 2, None, 4), _usage(1, 2, 3, "4"),
                                       _usage(1, 2, 3, -1), _usage(1, 2, 3, True)])
    def test_a_call_without_four_whole_figures_is_unmeasured(self, tmp_path, usage):
        _run(tmp_path, "r1", attempts=[_attempt("builder", usage)])
        assert recorded_calls(root=tmp_path)[0].tokens is None

    def test_no_run_store_is_no_call(self, tmp_path):
        assert recorded_calls(root=tmp_path) == []

    def test_a_torn_record_hides_no_other(self, tmp_path):
        (tmp_path / "runs" / "r0").mkdir(parents=True)
        (tmp_path / "runs" / "r0" / "result.json").write_text("{not json")
        _run(tmp_path, "r1", attempts=[_attempt("builder", _usage(1, 2, 3, 4))])
        assert [c.run_id for c in recorded_calls(root=tmp_path)] == ["r1"]

    def test_the_job_filter_keeps_that_jobs_runs(self, tmp_path):
        _run(tmp_path, "r1", job_id="j1", attempts=[_attempt("builder", _usage(1, 2, 3, 4))])
        _run(tmp_path, "r2", job_id="j2", attempts=[_attempt("builder", _usage(1, 2, 3, 4))])
        assert [c.run_id for c in recorded_calls(job_id="j2", root=tmp_path)] == ["r2"]

    def test_since_keeps_the_runs_that_finished_at_or_after_it(self, tmp_path):
        _run(tmp_path, "r1", finished="2026-10-09T23:59:59+00:00", attempts=[_attempt("builder", None)])
        _run(tmp_path, "r2", finished="2026-10-10T00:00:00+00:00", attempts=[_attempt("builder", None)])
        _run(tmp_path, "r3", finished="", attempts=[_attempt("builder", None)])
        assert [c.run_id for c in recorded_calls(since="2026-10-10", root=tmp_path)] == ["r2"]
        assert [c.run_id for c in recorded_calls(since="2026-10-10T00:00:00Z", root=tmp_path)] == ["r2"]
        assert len(recorded_calls(root=tmp_path)) == 3


def _call(role, tokens, *, job="j1", provider="claude-cli"):
    return RecordedCall("r", job, role, provider, tokens)


def _t(i, o, cc, cr):
    return {"input": i, "output": o, "cache_creation": cc, "cache_read": cr}


class TestTheSummary:
    def test_figures_by_role_and_provider_with_their_means_per_call(self):
        calls = [_call("builder", _t(10, 100, 1000, 10000)), _call("builder", _t(20, 300, 3000, 30000)),
                 _call("reviewer", _t(5, 50, 500, 5000)), _call("builder", None)]
        summary = summarize_call_tokens(calls, landed=lambda job: False)
        builder = summary["groups"][0]
        assert (builder["role"], builder["provider"], builder["calls"], builder["measured_calls"]) == (
            "builder", "claude-cli", 3, 2)
        assert builder["tokens"] == _t(30, 400, 4000, 40000)
        assert builder["per_call"] == _t(15, 200, 2000, 20000)
        assert (builder["total_tokens"], builder["per_call_total"]) == (44430, 22215)
        assert [g["role"] for g in summary["groups"]] == ["builder", "reviewer"]
        assert summary["all"]["calls"] == 4 and summary["all"]["measured_calls"] == 3

    def test_providers_are_kept_apart(self):
        calls = [_call("builder", _t(1, 1, 1, 1)), _call("builder", _t(1, 1, 1, 1), provider="ollama")]
        assert [(g["role"], g["provider"]) for g in summarize_call_tokens(
            calls, landed=lambda job: False)["groups"]] == [("builder", "claude-cli"), ("builder", "ollama")]

    def test_nothing_measured_is_unmeasured_never_zero(self):
        summary = summarize_call_tokens([_call("builder", None)], landed=lambda job: True)
        assert summary["all"]["tokens"] is None and summary["all"]["per_call"] is None
        assert summary["all"]["per_call_total"] is None
        assert summary["per_landed_change"] is None and summary["per_landed_change_total"] is None

    def test_a_landed_change_carries_every_measured_call_of_the_set(self):
        calls = [_call("builder", _t(10, 100, 1000, 10000), job="landed"),
                 _call("builder", _t(30, 300, 3000, 30000), job="not-landed"),
                 _call("reviewer", _t(2, 20, 200, 2000), job="")]
        summary = summarize_call_tokens(calls, landed=lambda job: job == "landed")
        assert summary["landed_changes"] == 1 and summary["landed_jobs"] == ["landed"]
        assert summary["per_landed_change"] == _t(42, 420, 4200, 42000)
        assert summary["per_landed_change_total"] == 46662

    def test_two_landed_jobs_halve_it(self):
        calls = [_call("builder", _t(10, 10, 10, 10), job="a"), _call("builder", _t(30, 30, 30, 30), job="b")]
        summary = summarize_call_tokens(calls, landed=lambda job: True)
        assert summary["landed_changes"] == 2
        assert summary["per_landed_change"] == _t(20, 20, 20, 20)

    def test_no_landed_job_has_no_figure_per_landed_change(self):
        summary = summarize_call_tokens([_call("builder", _t(1, 1, 1, 1))], landed=lambda job: False)
        assert summary["landed_changes"] == 0 and summary["per_landed_change"] is None

    def test_the_kinds_are_the_four_a_call_reports(self):
        assert TOKEN_KINDS == ("input", "output", "cache_creation", "cache_read")
