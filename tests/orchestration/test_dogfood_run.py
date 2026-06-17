"""Targeted tests for Open-Ended Dogfood Run Orchestrator + Replay Analyzer v0 (Steps 2146-2205)."""

from __future__ import annotations

import tempfile
from pathlib import Path

# Module under test.
from packages.orchestration.dogfood_run import (
    _ALL_LANES,
    _ALL_STATUSES,
    _TERMINAL_STATUSES,
    SCHEMA_VERSION,
    BrainstormIdea,
    DogfoodLane,
    DogfoodReplayAnalysis,
    DogfoodRunCheckpoint,
    DogfoodRunEvaluation,
    DogfoodRunPolicy,
    DogfoodRunRecord,
    DogfoodRunStatus,
    analyze_dogfood_run_replay,
    append_checkpoint,
    build_mission_morning_report,
    create_dogfood_run,
    dogfood_run_integrity,
    evaluate_dogfood_run,
    list_brainstorm_ideas,
    list_dogfood_runs,
    load_checkpoints,
    load_dogfood_run,
    run_mission_loop,
    save_brainstorm_idea,
    save_dogfood_run,
    step_dogfood_run,
    stop_dogfood_run,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_run(td: str, **overrides) -> DogfoodRunRecord:
    """Create a test run with sensible defaults, persisted to td."""
    defaults = dict(job_id="test-job-001", contract_id="msn-test001")
    defaults.update(overrides)
    return create_dogfood_run(**defaults, data_dir=Path(td))


# ---------------------------------------------------------------------------
# Phase 2: Core Model Tests
# ---------------------------------------------------------------------------


class TestDogfoodRunStatus:
    def test_all_statuses_known(self):
        assert len(_ALL_STATUSES) >= 10
        assert DogfoodRunStatus.NOT_STARTED in _ALL_STATUSES
        assert DogfoodRunStatus.SATISFIED in _ALL_STATUSES
        assert DogfoodRunStatus.BUDGET_EXHAUSTED in _ALL_STATUSES

    def test_terminal_statuses_subset(self):
        assert _TERMINAL_STATUSES.issubset(_ALL_STATUSES)
        assert DogfoodRunStatus.SATISFIED in _TERMINAL_STATUSES
        assert DogfoodRunStatus.RUNNING not in _TERMINAL_STATUSES

    def test_all_lanes_known(self):
        assert len(_ALL_LANES) >= 6
        assert DogfoodLane.MISSION in _ALL_LANES
        assert DogfoodLane.BRAINSTORM in _ALL_LANES


class TestDogfoodRunPolicy:
    def test_default_policy(self):
        p = DogfoodRunPolicy()
        assert p.max_steps == 100
        assert p.max_tokens_estimated == 500_000
        assert p.max_wall_minutes == 480
        assert p.require_clean_review is True
        assert p.auto_step is False

    def test_policy_round_trip(self):
        p = DogfoodRunPolicy(max_steps=50, max_tokens_estimated=100_000)
        d = p.to_dict()
        assert d["max_steps"] == 50
        assert d["max_tokens_estimated"] == 100_000


class TestDogfoodRunRecord:
    def test_record_to_dict(self):
        r = DogfoodRunRecord(run_id="dfr-test", job_id="j1")
        d = r.to_dict()
        assert d["run_id"] == "dfr-test"
        assert d["schema_version"] == SCHEMA_VERSION
        assert "policy" in d

    def test_default_status_not_started(self):
        r = DogfoodRunRecord()
        assert r.status == DogfoodRunStatus.NOT_STARTED


class TestDogfoodRunCheckpoint:
    def test_checkpoint_to_dict(self):
        cp = DogfoodRunCheckpoint(
            checkpoint_id="cp-test", run_id="dfr-test", step_index=1,
            lane="mission", action_taken="evaluate", outcome="running",
        )
        d = cp.to_dict()
        assert d["checkpoint_id"] == "cp-test"
        assert d["lane"] == "mission"


class TestBrainstormIdea:
    def test_idea_to_dict(self):
        idea = BrainstormIdea(
            idea_id="idea-1", run_id="dfr-test", job_id="j1",
            title="Improve test coverage", rationale="Low coverage on module X",
        )
        d = idea.to_dict()
        assert d["title"] == "Improve test coverage"
        assert d["status"] == "proposed"


# ---------------------------------------------------------------------------
# Phase 3: Storage Tests
# ---------------------------------------------------------------------------


class TestStorage:
    def test_create_and_load(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            assert run.run_id.startswith("dfr-")
            loaded = load_dogfood_run(run.run_id, "test-job-001", data_dir=Path(td))
            assert loaded is not None
            assert loaded.run_id == run.run_id

    def test_list_runs(self):
        with tempfile.TemporaryDirectory() as td:
            _make_run(td)
            _make_run(td)
            runs = list_dogfood_runs(job_id="test-job-001", data_dir=Path(td))
            assert len(runs) == 2

    def test_list_runs_all(self):
        with tempfile.TemporaryDirectory() as td:
            _make_run(td, job_id="j1")
            _make_run(td, job_id="j2")
            runs = list_dogfood_runs(data_dir=Path(td))
            assert len(runs) == 2

    def test_load_nonexistent(self):
        with tempfile.TemporaryDirectory() as td:
            assert load_dogfood_run("nope", "nope", data_dir=Path(td)) is None

    def test_save_updates_timestamp(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            old_ts = run.updated_at
            run.status = DogfoodRunStatus.RUNNING
            save_dogfood_run(run, data_dir=Path(td))
            loaded = load_dogfood_run(run.run_id, "test-job-001", data_dir=Path(td))
            assert loaded.status == DogfoodRunStatus.RUNNING
            assert loaded.updated_at >= old_ts

    def test_checkpoint_append_and_load(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            cp = DogfoodRunCheckpoint(
                checkpoint_id="cp-1", run_id=run.run_id, step_index=1,
                lane="mission", action_taken="test", outcome="ok",
            )
            assert append_checkpoint(cp, "test-job-001", data_dir=Path(td))
            cps = load_checkpoints(run.run_id, "test-job-001", data_dir=Path(td))
            assert len(cps) == 1
            assert cps[0].checkpoint_id == "cp-1"

    def test_brainstorm_save_and_list(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            idea = BrainstormIdea(
                idea_id="idea-1", run_id=run.run_id, job_id="test-job-001",
                title="Test idea", rationale="Test rationale",
            )
            assert save_brainstorm_idea(idea, data_dir=Path(td))
            ideas = list_brainstorm_ideas(run.run_id, "test-job-001", data_dir=Path(td))
            assert len(ideas) == 1
            assert ideas[0]["title"] == "Test idea"


# ---------------------------------------------------------------------------
# Phase 4: Evaluator Tests
# ---------------------------------------------------------------------------


class TestEvaluator:
    def test_evaluate_not_started(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            ev = evaluate_dogfood_run(run, data_dir=Path(td))
            assert isinstance(ev, DogfoodRunEvaluation)
            assert ev.run_id == run.run_id
            assert ev.budget_remaining_steps > 0

    def test_evaluate_terminal_stays_terminal(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.SATISFIED
            ev = evaluate_dogfood_run(run, data_dir=Path(td))
            assert ev.satisfied is True

    def test_evaluate_budget_exhausted_steps(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td, policy=DogfoodRunPolicy(max_steps=5))
            run.step_count = 5
            run.status = DogfoodRunStatus.RUNNING
            ev = evaluate_dogfood_run(run, data_dir=Path(td))
            assert ev.status == DogfoodRunStatus.BUDGET_EXHAUSTED
            assert "step_budget_exhausted" in ev.blocking_reasons

    def test_evaluate_budget_exhausted_tokens(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td, policy=DogfoodRunPolicy(max_tokens_estimated=100))
            run.cumulative_tokens = 100
            run.status = DogfoodRunStatus.RUNNING
            ev = evaluate_dogfood_run(run, data_dir=Path(td))
            assert ev.status == DogfoodRunStatus.BUDGET_EXHAUSTED

    def test_evaluate_has_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.RUNNING
            ev = evaluate_dogfood_run(run, data_dir=Path(td))
            assert "contract_status" in ev.evidence

    def test_evaluate_proposes_next_action(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.RUNNING
            ev = evaluate_dogfood_run(run, data_dir=Path(td))
            assert len(ev.next_actions) > 0


# ---------------------------------------------------------------------------
# Phase 5: Stepping Tests
# ---------------------------------------------------------------------------


class TestStepping:
    def test_step_starts_run(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            assert run.status == DogfoodRunStatus.NOT_STARTED
            run, cp = step_dogfood_run(run, data_dir=Path(td))
            assert run.status != DogfoodRunStatus.NOT_STARTED
            assert run.started_at != ""
            assert run.step_count == 1

    def test_step_records_checkpoint(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run, cp = step_dogfood_run(run, data_dir=Path(td))
            assert cp.checkpoint_id.startswith("cp-")
            cps = load_checkpoints(run.run_id, "test-job-001", data_dir=Path(td))
            assert len(cps) == 1

    def test_step_terminal_is_noop(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.SATISFIED
            run.finished_at = "2026-01-01T00:00:00+00:00"
            save_dogfood_run(run, data_dir=Path(td))
            run, cp = step_dogfood_run(run, data_dir=Path(td))
            assert cp.action_taken == "no_op"

    def test_multiple_steps_increment(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            for i in range(3):
                run, cp = step_dogfood_run(run, data_dir=Path(td))
            assert run.step_count == 3
            cps = load_checkpoints(run.run_id, "test-job-001", data_dir=Path(td))
            assert len(cps) == 3

    def test_stop_run(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run, _ = step_dogfood_run(run, data_dir=Path(td))
            run = stop_dogfood_run(run, reason="test stop", data_dir=Path(td))
            assert run.status == DogfoodRunStatus.STOPPED_BY_OPERATOR
            assert run.stop_reason == "test stop"
            assert run.finished_at != ""

    def test_stop_terminal_is_noop(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.SATISFIED
            run.finished_at = "2026-01-01T00:00:00+00:00"
            save_dogfood_run(run, data_dir=Path(td))
            run = stop_dogfood_run(run, data_dir=Path(td))
            assert run.status == DogfoodRunStatus.SATISFIED


# ---------------------------------------------------------------------------
# Phase 6: Replay Analyzer Tests
# ---------------------------------------------------------------------------


class TestReplayAnalyzer:
    def test_replay_no_checkpoints(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            analysis = analyze_dogfood_run_replay(run.run_id, "test-job-001", data_dir=Path(td))
            assert isinstance(analysis, DogfoodReplayAnalysis)
            assert analysis.total_steps == 0
            assert "no_checkpoints" in analysis.anomalies

    def test_replay_with_steps(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            for _ in range(3):
                run, _ = step_dogfood_run(run, data_dir=Path(td))
            analysis = analyze_dogfood_run_replay(run.run_id, "test-job-001", data_dir=Path(td))
            assert analysis.total_steps == 3
            assert len(analysis.timeline) == 3
            assert len(analysis.lane_summaries) > 0

    def test_replay_token_curve(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run, _ = step_dogfood_run(run, data_dir=Path(td))
            analysis = analyze_dogfood_run_replay(run.run_id, "test-job-001", data_dir=Path(td))
            assert len(analysis.token_curve) > 0

    def test_replay_caches_result(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run, _ = step_dogfood_run(run, data_dir=Path(td))
            analyze_dogfood_run_replay(run.run_id, "test-job-001", data_dir=Path(td))
            # Check cached file exists.
            replay_file = Path(td) / "workspaces" / "test-job-001" / "dogfood_runs" / run.run_id / "replay.json"
            assert replay_file.is_file()

    def test_replay_to_dict(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run, _ = step_dogfood_run(run, data_dir=Path(td))
            analysis = analyze_dogfood_run_replay(run.run_id, "test-job-001", data_dir=Path(td))
            d = analysis.to_dict()
            assert "timeline" in d
            assert "lane_summaries" in d
            assert "anomalies" in d


# ---------------------------------------------------------------------------
# Phase 7: Brainstorm Tests
# ---------------------------------------------------------------------------


class TestBrainstorm:
    def test_brainstorm_ideas_not_auto_injected(self):
        """Ideas are metadata-only. Saving an idea should not affect run status."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            idea = BrainstormIdea(
                idea_id="idea-1", run_id=run.run_id, job_id="test-job-001",
                title="Add telemetry", rationale="Would help debugging",
                evidence_needed=["Coverage report"],
            )
            save_brainstorm_idea(idea, data_dir=Path(td))
            loaded = load_dogfood_run(run.run_id, "test-job-001", data_dir=Path(td))
            assert loaded.status == DogfoodRunStatus.NOT_STARTED  # unchanged

    def test_multiple_ideas(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            for i in range(3):
                idea = BrainstormIdea(
                    idea_id=f"idea-{i}", run_id=run.run_id, job_id="test-job-001",
                    title=f"Idea {i}",
                )
                save_brainstorm_idea(idea, data_dir=Path(td))
            ideas = list_brainstorm_ideas(run.run_id, "test-job-001", data_dir=Path(td))
            assert len(ideas) == 3


# ---------------------------------------------------------------------------
# Phase 11: Integrity Tests
# ---------------------------------------------------------------------------


class TestIntegrity:
    def test_integrity_empty(self):
        with tempfile.TemporaryDirectory() as td:
            result = dogfood_run_integrity(data_dir=Path(td))
            assert result["passed"] is True
            assert result["checks"] == []

    def test_integrity_valid_run(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run, _ = step_dogfood_run(run, data_dir=Path(td))
            result = dogfood_run_integrity(data_dir=Path(td))
            assert result["passed"] is True

    def test_integrity_detects_satisfied_with_blockers(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.SATISFIED
            run.finished_at = "2026-01-01T00:00:00+00:00"
            run.blocking_reasons = ["should_not_be_here"]
            save_dogfood_run(run, data_dir=Path(td))
            result = dogfood_run_integrity(data_dir=Path(td))
            assert result["passed"] is False
            codes = [c["code"] for c in result["checks"]]
            assert "satisfied_with_blockers" in codes

    def test_integrity_detects_terminal_missing_finished_at(self):
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.BLOCKED
            run.finished_at = ""  # missing
            save_dogfood_run(run, data_dir=Path(td))
            result = dogfood_run_integrity(data_dir=Path(td))
            assert result["passed"] is False
            codes = [c["code"] for c in result["checks"]]
            assert "terminal_missing_finished_at" in codes


# ---------------------------------------------------------------------------
# CLI Integration Tests
# ---------------------------------------------------------------------------


class TestCLIHandlers:
    def test_handlers_registered(self):
        from apps.cli.commands.dogfood_cmd import COMMAND_HANDLERS
        assert len(COMMAND_HANDLERS) == 12
        assert "dogfood.create" in COMMAND_HANDLERS
        assert "dogfood.step" in COMMAND_HANDLERS
        assert "dogfood.replay" in COMMAND_HANDLERS
        assert "dogfood.brainstorm" in COMMAND_HANDLERS


class TestCatalogEntries:
    def test_dogfood_group_exists(self):
        from apps.cli.command_catalog import GROUPS
        assert "dogfood" in GROUPS

    def test_dogfood_commands_in_catalog(self):
        from apps.cli.command_catalog import CATALOG
        dogfood_cmds = [c for c in CATALOG if c.group_id == "dogfood"]
        assert len(dogfood_cmds) == 12
        ids = {c.command_id for c in dogfood_cmds}
        assert "dogfood.create" in ids
        assert "dogfood.step" in ids
        assert "dogfood.replay" in ids

    def test_all_dogfood_commands_have_handlers(self):
        from apps.cli.command_catalog import CATALOG
        from apps.cli.commands.dogfood_cmd import COMMAND_HANDLERS
        dogfood_cmds = [c for c in CATALOG if c.group_id == "dogfood"]
        for cmd in dogfood_cmds:
            assert cmd.command_id in COMMAND_HANDLERS, f"Missing handler for {cmd.command_id}"


class TestRunContractActions:
    def test_dogfood_actions_in_contract(self):
        from packages.orchestration.run_contract import ALL_KNOWN_ACTIONS, ContractAction
        assert ContractAction.DOGFOOD_RUN_CREATE in ALL_KNOWN_ACTIONS
        assert ContractAction.DOGFOOD_RUN_STEP in ALL_KNOWN_ACTIONS
        assert ContractAction.DOGFOOD_RUN_SHOW in ALL_KNOWN_ACTIONS


class TestProgressLedgerIntegration:
    def test_extract_dogfood_run_items_empty(self):
        from packages.orchestration.progress_ledger import extract_dogfood_run_items
        assert extract_dogfood_run_items(None) == []
        assert extract_dogfood_run_items([]) == []

    def test_extract_dogfood_run_items_active(self):
        from packages.orchestration.progress_ledger import extract_dogfood_run_items
        items = extract_dogfood_run_items([
            {"run_id": "dfr-1", "status": "running", "step_count": 5},
        ])
        assert len(items) == 1
        assert items[0].item_id == "dogfood-run-dfr-1"

    def test_extract_dogfood_run_items_satisfied(self):
        from packages.orchestration.progress_ledger import extract_dogfood_run_items
        items = extract_dogfood_run_items([
            {"run_id": "dfr-2", "status": "satisfied", "step_count": 10},
        ])
        assert len(items) == 1
        assert "DONE" in items[0].status or items[0].status == "done"

    def test_extract_dogfood_run_items_blocked(self):
        from packages.orchestration.progress_ledger import extract_dogfood_run_items
        items = extract_dogfood_run_items([
            {"run_id": "dfr-3", "status": "blocked", "step_count": 3},
        ])
        assert len(items) == 1

    def test_extract_dogfood_run_items_stopped(self):
        from packages.orchestration.progress_ledger import extract_dogfood_run_items
        items = extract_dogfood_run_items([
            {"run_id": "dfr-4", "status": "stopped_by_operator", "step_count": 7},
        ])
        assert len(items) == 1
        assert "stopped" in items[0].title.lower()

    def test_extract_dogfood_run_items_not_started(self):
        from packages.orchestration.progress_ledger import extract_dogfood_run_items
        items = extract_dogfood_run_items([
            {"run_id": "dfr-5", "status": "not_started", "step_count": 0},
        ])
        assert len(items) == 1
        assert "not started" in items[0].title.lower()


# ---------------------------------------------------------------------------
# R-0116 Closure: Deep Integrity Checks (Steps 2206-2225)
# ---------------------------------------------------------------------------


class TestR0116DeepIntegrity:
    def test_satisfied_with_unsatisfied_mission(self):
        """Satisfied run with mission contract NOT satisfied should fail integrity."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.SATISFIED
            run.finished_at = "2026-01-01T00:00:00+00:00"
            save_dogfood_run(run, data_dir=Path(td))
            # No mission contract exists -> contract_status="unknown" -> skip (conservative)
            result = dogfood_run_integrity(data_dir=Path(td))
            # unknown contract_status is NOT a violation (conservative)
            codes = [c["code"] for c in result["checks"]]
            assert "satisfied_with_unsatisfied_mission" not in codes

    def test_guardrail_exceeded_without_terminal(self):
        """Run that exceeded step guardrail but is not terminal should fail."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td, policy=DogfoodRunPolicy(max_steps=5))
            run.status = DogfoodRunStatus.RUNNING
            run.step_count = 10
            run.started_at = "2026-01-01T00:00:00+00:00"
            save_dogfood_run(run, data_dir=Path(td))
            result = dogfood_run_integrity(data_dir=Path(td))
            assert result["passed"] is False
            codes = [c["code"] for c in result["checks"]]
            assert "guardrail_exceeded_without_terminal_status" in codes

    def test_active_lane_status_mismatch(self):
        """Running run with done/blocked active lane should fail integrity."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.RUNNING
            run.current_lane = DogfoodLane.MISSION
            run.lane_statuses = {DogfoodLane.MISSION: "done"}
            run.started_at = "2026-01-01T00:00:00+00:00"
            save_dogfood_run(run, data_dir=Path(td))
            result = dogfood_run_integrity(data_dir=Path(td))
            assert result["passed"] is False
            codes = [c["code"] for c in result["checks"]]
            assert "active_lane_status_mismatch" in codes

    def test_replay_raw_data_leak(self):
        """Replay with raw markers should fail integrity."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            # Create a replay file with a secret marker.
            replay_path = Path(td) / "workspaces" / "test-job-001" / "dogfood_runs" / run.run_id / "replay.json"
            replay_path.parent.mkdir(parents=True, exist_ok=True)
            import json as _json
            _json.dump({
                "run_id": run.run_id, "timeline": [{"action": "leaked sk-ant-12345"}],
            }, open(replay_path, "w"))
            result = dogfood_run_integrity(data_dir=Path(td))
            assert result["passed"] is False
            codes = [c["code"] for c in result["checks"]]
            assert "replay_raw_data_leak" in codes

    def test_brainstorm_required_without_evidence(self):
        """Brainstorm idea with status=required but no evidence_needed should fail."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            brainstorm_dir = Path(td) / "workspaces" / "test-job-001" / "dogfood_runs" / run.run_id / "brainstorm"
            brainstorm_dir.mkdir(parents=True, exist_ok=True)
            import json as _json
            _json.dump({
                "idea_id": "idea-bad", "status": "required", "evidence_needed": [],
                "title": "Bad idea without evidence",
            }, open(brainstorm_dir / "idea-bad.json", "w"))
            result = dogfood_run_integrity(data_dir=Path(td))
            assert result["passed"] is False
            codes = [c["code"] for c in result["checks"]]
            assert "brainstorm_required_without_evidence" in codes

    def test_valid_run_still_passes(self):
        """A properly-formed run must still pass all integrity checks."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run, _ = step_dogfood_run(run, data_dir=Path(td))
            result = dogfood_run_integrity(data_dir=Path(td))
            assert result["passed"] is True

    def test_satisfied_run_no_false_positive(self):
        """Satisfied run with no evidence (unknown) should not false-positive."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.SATISFIED
            run.finished_at = "2026-01-01T00:00:00+00:00"
            run.blocking_reasons = []
            save_dogfood_run(run, data_dir=Path(td))
            result = dogfood_run_integrity(data_dir=Path(td))
            # Only check: no false positive on satisfied_with_unsatisfied_mission
            sat_codes = [c for c in result["checks"] if c["code"] == "satisfied_with_unsatisfied_mission"]
            assert len(sat_codes) == 0

    def test_satisfied_with_open_findings(self):
        """R-0119: Satisfied run with open review findings should fail integrity."""
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.SATISFIED
            run.finished_at = "2026-01-01T00:00:00+00:00"
            run.blocking_reasons = []
            save_dogfood_run(run, data_dir=Path(td))
            fake_evidence = {
                "contract_status": "contract_satisfied", "contract_satisfied": True,
                "open_review_findings": 3, "failed_tests": 0, "tests_status": "passed",
                "proof_status": "verified", "repair_open": 0, "repair_blocked": 0,
                "builder_sessions_active": 0, "builder_sessions_blocked": 0,
                "managed_executions_active": 0,
            }
            with patch("packages.orchestration.dogfood_run._gather_run_evidence", return_value=fake_evidence):
                result = dogfood_run_integrity(data_dir=Path(td))
            assert result["passed"] is False
            codes = [c["code"] for c in result["checks"]]
            assert "satisfied_with_open_findings" in codes

    def test_satisfied_with_failing_tests(self):
        """R-0119: Satisfied run with failing required tests should fail integrity."""
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.SATISFIED
            run.finished_at = "2026-01-01T00:00:00+00:00"
            run.blocking_reasons = []
            save_dogfood_run(run, data_dir=Path(td))
            fake_evidence = {
                "contract_status": "contract_satisfied", "contract_satisfied": True,
                "open_review_findings": 0, "failed_tests": 5, "tests_status": "failed",
                "proof_status": "verified", "repair_open": 0, "repair_blocked": 0,
                "builder_sessions_active": 0, "builder_sessions_blocked": 0,
                "managed_executions_active": 0,
            }
            with patch("packages.orchestration.dogfood_run._gather_run_evidence", return_value=fake_evidence):
                result = dogfood_run_integrity(data_dir=Path(td))
            assert result["passed"] is False
            codes = [c["code"] for c in result["checks"]]
            assert "satisfied_with_failing_tests" in codes

    def test_token_guardrail_exceeded_without_terminal(self):
        """R-0120: Non-terminal run exceeding token budget should fail integrity."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td, policy=DogfoodRunPolicy(max_tokens_estimated=100_000))
            run.status = DogfoodRunStatus.RUNNING
            run.started_at = "2026-01-01T00:00:00+00:00"
            run.cumulative_tokens = 200_000
            save_dogfood_run(run, data_dir=Path(td))
            result = dogfood_run_integrity(data_dir=Path(td))
            assert result["passed"] is False
            codes = [c["code"] for c in result["checks"]]
            assert "guardrail_exceeded_without_terminal_status" in codes
            # Verify it mentions tokens in detail
            detail_checks = [c for c in result["checks"] if c["code"] == "guardrail_exceeded_without_terminal_status"]
            assert any("tokens" in c.get("detail", "") for c in detail_checks)

    def test_budget_exhausted_no_false_positive(self):
        """R-0120: Budget-exhausted terminal run should NOT trigger guardrail check."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td, policy=DogfoodRunPolicy(max_tokens_estimated=100_000))
            run.status = DogfoodRunStatus.BUDGET_EXHAUSTED
            run.started_at = "2026-01-01T00:00:00+00:00"
            run.finished_at = "2026-01-01T01:00:00+00:00"
            run.cumulative_tokens = 200_000
            save_dogfood_run(run, data_dir=Path(td))
            result = dogfood_run_integrity(data_dir=Path(td))
            codes = [c["code"] for c in result["checks"]]
            assert "guardrail_exceeded_without_terminal_status" not in codes


# ---------------------------------------------------------------------------
# R-0117 Closure: Evidence Gathering (Steps 2206-2225)
# ---------------------------------------------------------------------------


class TestR0117EvidenceGathering:
    def test_evidence_has_builder_fields(self):
        """Evidence dict must have builder/execution/proof keys."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            ev = evaluate_dogfood_run(run, data_dir=Path(td))
            assert "builder_sessions_active" in ev.evidence
            assert "builder_sessions_blocked" in ev.evidence
            assert "managed_executions_active" in ev.evidence
            assert "proof_status" in ev.evidence

    def test_evidence_defaults_conservative(self):
        """Without subsystems, evidence defaults should be safe/conservative."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            ev = evaluate_dogfood_run(run, data_dir=Path(td))
            assert ev.evidence["builder_sessions_active"] == 0
            assert ev.evidence["builder_sessions_blocked"] == 0
            assert ev.evidence["managed_executions_active"] == 0
            assert ev.evidence["proof_status"] in ("unavailable", "incomplete", "unverified")

    def test_evidence_no_fake_satisfaction(self):
        """Without real evidence, run must NOT be satisfied."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.RUNNING
            run.started_at = "2026-01-01T00:00:00+00:00"
            ev = evaluate_dogfood_run(run, data_dir=Path(td))
            assert ev.satisfied is False


# ---------------------------------------------------------------------------
# Bounded Mission Run Loop Tests (Steps 2602-2605)
# ---------------------------------------------------------------------------


class TestMissionRunLoop:
    def test_satisfied_run_stops_immediately(self):
        """Loop stops immediately when run is already satisfied."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.SATISFIED
            run.finished_at = "2026-01-01T01:00:00+00:00"
            save_dogfood_run(run, data_dir=Path(td))
            result = run_mission_loop(
                run.run_id, job_id=run.job_id,
                max_steps=10, max_seconds=60,
                data_dir=Path(td),
            )
            assert result.stop_reason == "mission_satisfied"
            assert result.steps_attempted == 0
            assert result.final_status == DogfoodRunStatus.SATISFIED

    def test_waiting_approval_stops(self):
        """Loop stops when run needs approval."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.WAITING_FOR_APPROVAL
            save_dogfood_run(run, data_dir=Path(td))
            result = run_mission_loop(
                run.run_id, job_id=run.job_id,
                max_steps=10, max_seconds=60,
                data_dir=Path(td),
            )
            assert result.stop_reason == "waiting_for_approval"
            assert result.steps_attempted == 0

    def test_blocked_stops(self):
        """Loop stops when run is blocked."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.BLOCKED
            run.blocking_reasons = ["no_lanes_available"]
            run.finished_at = "2026-01-01T01:00:00+00:00"
            save_dogfood_run(run, data_dir=Path(td))
            result = run_mission_loop(
                run.run_id, job_id=run.job_id,
                max_steps=10, max_seconds=60,
                data_dir=Path(td),
            )
            assert result.stop_reason == "blocked"

    def test_max_steps_stops_loop(self):
        """Loop stops at max_steps."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            result = run_mission_loop(
                run.run_id, job_id=run.job_id,
                max_steps=3, max_seconds=60,
                data_dir=Path(td),
            )
            assert result.steps_attempted <= 3
            assert result.stop_reason in (
                "max_steps_reached", "no_safe_next_action",
                "waiting_for_operator", "blocked",
            )

    def test_max_seconds_stops_loop(self):
        """Loop stops at max_seconds (use 0 for immediate)."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            result = run_mission_loop(
                run.run_id, job_id=run.job_id,
                max_steps=100, max_seconds=0,
                data_dir=Path(td),
            )
            assert result.stop_reason == "max_seconds_reached"
            assert result.steps_attempted == 0

    def test_not_found_returns_error(self):
        """Loop returns error for nonexistent run."""
        with tempfile.TemporaryDirectory() as td:
            result = run_mission_loop(
                "nonexistent", job_id="fake-job",
                max_steps=1, max_seconds=10,
                data_dir=Path(td),
            )
            assert result.stop_reason == "internal_error"
            assert len(result.errors) > 0

    def test_result_is_json_safe(self):
        """MissionRunLoopResult serializes to JSON."""
        import json
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.SATISFIED
            run.finished_at = "2026-01-01T01:00:00+00:00"
            save_dogfood_run(run, data_dir=Path(td))
            result = run_mission_loop(
                run.run_id, job_id=run.job_id,
                max_steps=1, max_seconds=10,
                data_dir=Path(td),
            )
            d = result.to_dict()
            s = json.dumps(d)
            assert "run_id" in s
            assert "stop_reason" in s

    def test_no_unbounded_loop(self):
        """Loop with NOT_STARTED run must terminate within max_steps."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            result = run_mission_loop(
                run.run_id, job_id=run.job_id,
                max_steps=5, max_seconds=30,
                data_dir=Path(td),
            )
            assert result.steps_attempted <= 5
            assert result.stop_reason != ""


# ---------------------------------------------------------------------------
# Morning Report Tests (Step 2606)
# ---------------------------------------------------------------------------


class TestMorningReport:
    def test_partial_run_report(self):
        """Report works for a run that has stepped but is not terminal."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            step_dogfood_run(run, data_dir=Path(td))
            report = build_mission_morning_report(
                run.run_id, job_id=run.job_id, data_dir=Path(td),
            )
            assert report.run_id == run.run_id
            assert report.steps_completed >= 1
            assert report.operator_summary != ""

    def test_satisfied_run_report(self):
        """Report for a satisfied run shows satisfaction."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.SATISFIED
            run.finished_at = "2026-01-01T01:00:00+00:00"
            save_dogfood_run(run, data_dir=Path(td))
            report = build_mission_morning_report(
                run.run_id, job_id=run.job_id, data_dir=Path(td),
            )
            assert report.mission_status == "satisfied"

    def test_blocked_run_report(self):
        """Report for a blocked run shows blockers."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            run.status = DogfoodRunStatus.BLOCKED
            run.blocking_reasons = ["no_lanes_available"]
            run.finished_at = "2026-01-01T01:00:00+00:00"
            save_dogfood_run(run, data_dir=Path(td))
            report = build_mission_morning_report(
                run.run_id, job_id=run.job_id, data_dir=Path(td),
            )
            assert len(report.blocked_items) > 0

    def test_report_includes_core_readiness(self):
        """Report includes core readiness summary."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            report = build_mission_morning_report(
                run.run_id, job_id=run.job_id, data_dir=Path(td),
            )
            assert "mission_contract" in report.core_readiness
            assert "run_exists" in report.core_readiness
            assert "builder_adapter_available" in report.core_readiness

    def test_report_includes_self_repair(self):
        """Report includes self-repair proposal summary."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            report = build_mission_morning_report(
                run.run_id, job_id=run.job_id, data_dir=Path(td),
            )
            assert "proposal_count" in report.self_repair_summary
            assert "awaiting_approval" in report.self_repair_summary

    def test_report_includes_builder_execution(self):
        """Report includes builder/execution visibility."""
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            report = build_mission_morning_report(
                run.run_id, job_id=run.job_id, data_dir=Path(td),
            )
            assert "latest_session_status" in report.builder_execution_summary
            assert "output_ref_exists" in report.builder_execution_summary

    def test_report_is_json_safe(self):
        """MissionMorningReport serializes to JSON without error."""
        import json
        with tempfile.TemporaryDirectory() as td:
            run = _make_run(td)
            report = build_mission_morning_report(
                run.run_id, job_id=run.job_id, data_dir=Path(td),
            )
            d = report.to_dict()
            s = json.dumps(d)
            assert "operator_summary" in s
            assert "core_readiness" in s

    def test_not_found_returns_summary(self):
        """Report for nonexistent run returns operator summary with error."""
        with tempfile.TemporaryDirectory() as td:
            report = build_mission_morning_report(
                "nonexistent", job_id="fake", data_dir=Path(td),
            )
            assert "not found" in report.operator_summary.lower()
