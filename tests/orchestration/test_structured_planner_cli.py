"""F005 Finding 4/5/6 — the real plan-job-local CLI path uses the structured
PlannerPlan schema natively, with one parse retry, honest parse classification,
prompt traces per call, and no silent fallback. Ollama is never contacted."""
from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from packages.core.models import Job, RunState
from packages.orchestration.storage import save_job

VALID_PLAN = json.dumps({
    "schema_v": "pp1", "summary": "plan it",
    "proposed_tasks": [{"task_type": "implement", "description": "do the thing"}],
})


class _FakePlanner:
    """Stand-in for OllamaPlanner. Records native calls; never hits the network."""

    def __init__(self, raw_outputs=None, *, has_plan_raw=True):
        self.model = "fake-model"
        self._raw = list(raw_outputs or [VALID_PLAN])
        self._i = 0
        self.raw_calls = []          # (prompt, schema) per plan_raw call
        self.legacy_called = False
        if not has_plan_raw:
            # Simulate a provider WITHOUT the structured capability.
            del self.__class__.plan_raw  # type: ignore[attr-defined]

    def plan_raw(self, prompt, *, schema):
        self.raw_calls.append((prompt, schema))
        out = self._raw[min(self._i, len(self._raw) - 1)]
        self._i += 1
        return out

    def plan(self, prompt):
        self.legacy_called = True
        from packages.orchestration.planner_models import PlannerOutput, ProposedTask
        return PlannerOutput(summary="legacy", proposed_tasks=[
            ProposedTask(task_type="legacy", description="legacy path")])


def _make_job(tmp_path, monkeypatch) -> Job:
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    job = Job(name="test", state=RunState.PENDING)
    save_job(job)
    return job


def _run(job_id):
    from apps.cli.commands.job import _cmd_plan_job_local
    _cmd_plan_job_local(str(job_id))


def _events(tmp_path, job_id):
    from packages.orchestration.run_log import read_run_events
    d = tmp_path / "job_logs" / str(job_id)
    # Exclude prompt_trace.jsonl — the run log is the <run_id>.jsonl file.
    files = [f for f in d.glob("*.jsonl") if f.name != "prompt_trace.jsonl"] if d.exists() else []
    return read_run_events(files[0]) if files else []


def _plan_traces(tmp_path, job_id):
    p = tmp_path / "job_logs" / str(job_id) / "prompt_trace.jsonl"
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def _patch_planner(planner):
    return patch("packages.providers.ollama_planner.provider.OllamaPlanner",
                 return_value=planner)


class TestStructuredPlannerCli:
    def test_structured_is_the_default_and_uses_plan_raw(self, tmp_path, monkeypatch):
        monkeypatch.delenv("REMEDY_PLANNER_FREETEXT", raising=False)
        job = _make_job(tmp_path, monkeypatch)
        planner = _FakePlanner([VALID_PLAN])
        with _patch_planner(planner):
            _run(job.id)
        assert planner.raw_calls, "structured mode did not call plan_raw"
        assert planner.legacy_called is False

    def test_plannerplan_schema_with_schema_v_pp1_passed_to_format(self, tmp_path, monkeypatch):
        job = _make_job(tmp_path, monkeypatch)
        planner = _FakePlanner([VALID_PLAN])
        with _patch_planner(planner):
            _run(job.id)
        _prompt, schema = planner.raw_calls[0]
        props = schema.get("properties", {})
        assert "schema_v" in props
        assert "schema_v" in schema.get("required", [])
        # the pp1 tag is pinned in the schema
        assert "pp1" in json.dumps(schema)

    def test_first_invalid_then_valid_recovers_with_one_retry(self, tmp_path, monkeypatch):
        job = _make_job(tmp_path, monkeypatch)
        planner = _FakePlanner(["not json", VALID_PLAN])
        with _patch_planner(planner):
            _run(job.id)
        assert len(planner.raw_calls) == 2
        names = [e.get("event") for e in _events(tmp_path, job.id)]
        assert "planning_completed" in names

    def test_two_invalid_outputs_stop_as_parse(self, tmp_path, monkeypatch):
        job = _make_job(tmp_path, monkeypatch)
        planner = _FakePlanner(["bad1", "bad2", "bad3"])
        with _patch_planner(planner), pytest.raises(SystemExit):
            _run(job.id)
        assert len(planner.raw_calls) == 2  # never a third call
        failed = [e for e in _events(tmp_path, job.id) if e["event"] == "planning_failed"]
        assert failed and failed[-1].get("metadata", {}).get("error_category") == "parse"

    def test_compatibility_flag_uses_legacy_path(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_PLANNER_FREETEXT", "1")
        job = _make_job(tmp_path, monkeypatch)
        planner = _FakePlanner([VALID_PLAN])
        with _patch_planner(planner):
            _run(job.id)
        assert planner.legacy_called is True
        assert planner.raw_calls == []

    def test_no_silent_fallback_when_structured_capability_absent(self, tmp_path, monkeypatch):
        monkeypatch.delenv("REMEDY_PLANNER_FREETEXT", raising=False)
        job = _make_job(tmp_path, monkeypatch)

        class _NoRawPlanner:
            model = "fake-model"
            def plan(self, prompt):
                raise AssertionError("legacy plan must not be called")

        with _patch_planner(_NoRawPlanner()), pytest.raises(SystemExit):
            _run(job.id)
        failed = [e for e in _events(tmp_path, job.id) if e["event"] == "planning_failed"]
        assert failed and failed[-1].get("metadata", {}).get("error_category") == "config"

    def test_planner_prompt_traces_initial_and_retry(self, tmp_path, monkeypatch):
        job = _make_job(tmp_path, monkeypatch)
        planner = _FakePlanner(["bad", VALID_PLAN])
        with _patch_planner(planner):
            _run(job.id)
        traces = _plan_traces(tmp_path, job.id)
        assert len(traces) == 2, f"expected 2 planner traces, got {len(traces)}"
        assert all(t["schema_v"] == "pp1" for t in traces)
        assert traces[0]["prompt_kind"] == "plan"
        assert traces[1]["prompt_kind"] == "plan-retry"
        # native mode: the full schema is not duplicated into the prompt text
        assert all('"$defs"' not in t.get("prompt_text_redacted", "") for t in traces)

    def test_planner_traces_persist_even_on_parse_exhaustion(self, tmp_path, monkeypatch):
        job = _make_job(tmp_path, monkeypatch)
        planner = _FakePlanner(["bad1", "bad2"])
        with _patch_planner(planner), pytest.raises(SystemExit):
            _run(job.id)
        traces = _plan_traces(tmp_path, job.id)
        assert len(traces) == 2
        assert traces[1]["prompt_kind"] == "plan-retry"


class TestPlannerTraceMatchesSentPrompt:
    def test_trace_hash_matches_prompt_sent_to_plan_raw(self, tmp_path, monkeypatch):
        import hashlib
        monkeypatch.delenv("REMEDY_PLANNER_FREETEXT", raising=False)
        job = _make_job(tmp_path, monkeypatch)
        planner = _FakePlanner(["bad", VALID_PLAN])
        with _patch_planner(planner):
            _run(job.id)
        traces = _plan_traces(tmp_path, job.id)
        sent_prompts = [prompt for (prompt, _schema) in planner.raw_calls]
        assert len(traces) == len(sent_prompts) == 2
        for trace, sent in zip(traces, sent_prompts):
            assert trace["prompt_sha256"] == hashlib.sha256(sent.encode()).hexdigest()
        # native mode: the effective prompt is not the bare full schema
        assert all('"$defs"' not in p for p in sent_prompts)


# ---------------------------------------------------------------------------
# F005 Finding 2 — every REAL structured Planner call is traced BEFORE it runs,
# so the trace survives a provider/network exception. Fake planners only.
# ---------------------------------------------------------------------------

class _RaisingPlanner(_FakePlanner):
    """Fake planner whose plan_raw raises on the given 1-based attempts."""

    def __init__(self, raw_outputs=None, *, raise_on=()):
        super().__init__(raw_outputs)
        self._raise_on = set(raise_on)

    def plan_raw(self, prompt, *, schema):
        self.raw_calls.append((prompt, schema))
        n = len(self.raw_calls)
        if n in self._raise_on:
            raise RuntimeError("network down")
        out = self._raw[min(n - 1, len(self._raw) - 1)]
        return out


class TestPlannerTracedBeforeCall:
    def test_1_first_call_succeeds_one_call_one_trace(self, tmp_path, monkeypatch):
        monkeypatch.delenv("REMEDY_PLANNER_FREETEXT", raising=False)
        job = _make_job(tmp_path, monkeypatch)
        planner = _FakePlanner([VALID_PLAN])
        with _patch_planner(planner):
            _run(job.id)
        traces = _plan_traces(tmp_path, job.id)
        assert len(planner.raw_calls) == 1 and len(traces) == 1
        assert traces[0]["schema_v"] == "pp1"
        assert traces[0]["prompt_kind"] == "plan"

    def test_2_invalid_then_retry_succeeds(self, tmp_path, monkeypatch):
        job = _make_job(tmp_path, monkeypatch)
        planner = _FakePlanner(["bad", VALID_PLAN])
        with _patch_planner(planner):
            _run(job.id)
        traces = _plan_traces(tmp_path, job.id)
        assert len(planner.raw_calls) == 2 and len(traces) == 2
        assert [t["prompt_kind"] for t in traces] == ["plan", "plan-retry"]
        assert all(t["schema_v"] == "pp1" for t in traces)

    def test_3_invalid_then_retry_raises_both_traces_persist(self, tmp_path, monkeypatch):
        job = _make_job(tmp_path, monkeypatch)
        planner = _RaisingPlanner(["bad", VALID_PLAN], raise_on=(2,))
        with _patch_planner(planner), pytest.raises(SystemExit):
            _run(job.id)
        traces = _plan_traces(tmp_path, job.id)
        assert len(planner.raw_calls) == 2, "two real provider calls"
        assert len(traces) == 2, "both traces persisted despite the exception"
        assert [t["prompt_kind"] for t in traces] == ["plan", "plan-retry"]
        assert all(t["schema_v"] == "pp1" for t in traces)

    def test_4_initial_call_raises_trace_persists_and_provider_class(self, tmp_path, monkeypatch):
        job = _make_job(tmp_path, monkeypatch)
        planner = _RaisingPlanner([VALID_PLAN], raise_on=(1,))
        with _patch_planner(planner), pytest.raises(SystemExit):
            _run(job.id)
        traces = _plan_traces(tmp_path, job.id)
        assert len(planner.raw_calls) == 1, "one real provider call"
        assert len(traces) == 1, "its trace persists even though plan_raw raised"
        assert traces[0]["schema_v"] == "pp1"
        failed = [e for e in _events(tmp_path, job.id) if e["event"] == "planning_failed"]
        cat = failed[-1].get("metadata", {}).get("error_category")
        assert cat == "RuntimeError"      # provider error class, NOT parse
        assert cat != "parse"

    def test_5_trace_hashes_equal_the_prompts_sent(self, tmp_path, monkeypatch):
        import hashlib
        job = _make_job(tmp_path, monkeypatch)
        planner = _RaisingPlanner(["bad", VALID_PLAN], raise_on=(2,))
        with _patch_planner(planner), pytest.raises(SystemExit):
            _run(job.id)
        traces = _plan_traces(tmp_path, job.id)
        sent = [p for (p, _s) in planner.raw_calls]
        assert len(traces) == len(sent) == 2
        for trace, prompt in zip(traces, sent):
            assert trace["prompt_sha256"] == hashlib.sha256(prompt.encode()).hexdigest()

    def test_6_missing_capability_makes_no_call_and_no_trace(self, tmp_path, monkeypatch):
        monkeypatch.delenv("REMEDY_PLANNER_FREETEXT", raising=False)
        job = _make_job(tmp_path, monkeypatch)

        class _NoRawPlanner:
            model = "fake-model"
            def plan(self, prompt):
                raise AssertionError("legacy plan must not be called")

        with _patch_planner(_NoRawPlanner()), pytest.raises(SystemExit):
            _run(job.id)
        assert _plan_traces(tmp_path, job.id) == [], "no provider call -> no trace"


class TestPlannerTraceCarriesItsSegmentManifest:
    """F115 wiring guard: a planner trace with an empty manifest fails HERE."""

    def test_every_plan_trace_names_the_segments_it_sent(self, tmp_path, monkeypatch):
        from packages.orchestration.prompt_segments import SegmentStabilityRank

        job = _make_job(tmp_path, monkeypatch)
        planner = _FakePlanner(["bad", VALID_PLAN])
        with _patch_planner(planner):
            _run(job.id)
        traces = _plan_traces(tmp_path, job.id)
        assert len(traces) == 2
        for trace in traces:
            assert trace["segment_manifest"], "planner trace carries no manifest"
            first = trace["segment_manifest"][0]
            assert first["name"] == "planner_job_prompt"
            assert first["rank"] == int(SegmentStabilityRank.TASK)
            # The schema tail sits outside the registry (DECISION F105 D9): the
            # manifest covers a strict prefix of the prompt actually sent.
            assert 0 < trace["segment_manifest_chars"] < trace["prompt_chars"]

    def test_the_cli_hands_the_planner_composition_down(self):
        import inspect

        import apps.cli.commands.job as job_cmd

        source = inspect.getsource(job_cmd)
        assert "on_prompt_composed=_plan_compositions.append" in source
        assert "composed_prompt=_plan_compositions[-1]" in source
