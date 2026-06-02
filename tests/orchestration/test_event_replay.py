"""Tests: event replay model and checkpoint detection."""
from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

import pytest


def _write_events(tmp_path, job_id, events):
    runs_dir = tmp_path / "runs" / str(job_id)
    runs_dir.mkdir(parents=True, exist_ok=True)
    with open(runs_dir / "run.jsonl", "w") as f:
        for e in events:
            if "timestamp" not in e:
                e["timestamp"] = "2026-06-01T00:00:00Z"
            f.write(json.dumps(e) + "\n")


class TestReplayEmpty:
    def test_empty_job_degraded(self, tmp_path):
        from packages.orchestration.event_replay import replay_job
        r = replay_job(str(uuid4()), str(tmp_path))
        assert r.degraded is True
        assert r.degraded_reason == "no_events"
        assert r.current_stage == "unknown"
        assert r.event_count == 0


class TestReplayFixtureSuccess:
    def test_fixture_success_replay(self, tmp_path):
        from packages.orchestration.event_replay import replay_job
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {"goal": "fix"}},
            {"event": "source_context_injected", "metadata": {"file_count": 3, "estimated_tokens": 500}},
            {"event": "autorun_builder_completed", "metadata": {"provider": "fixture"}},
            {"event": "builder_patch_parsed", "metadata": {"parse_success": True}},
            {"event": "builder_bridge_intent_approved", "metadata": {"intent_id": "i-1"}},
            {"event": "patch_intent_applied", "metadata": {}},
            {"event": "test_run_completed", "metadata": {"exit_code": 0, "passed": True}},
            {"event": "proof_collected", "metadata": {"content_hash": "h1"}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        assert r.degraded is False
        assert r.event_count == 8
        assert r.provider == "fixture"
        assert r.current_stage == "proof_collected"
        assert r.source_context["injected"] is True
        assert r.tests["passed"] is True
        assert r.approval["status"] == "approved"
        assert r.stop_reason == ""


class TestReplayApprovalRequired:
    def test_approval_pending_replay(self, tmp_path):
        from packages.orchestration.event_replay import replay_job
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "autorun_builder_completed", "metadata": {"provider": "ollama"}},
            {"event": "builder_patch_parsed", "metadata": {"parse_success": True}},
            {"event": "structured_patch_intent_created", "metadata": {"intent_kind": "file_ops"}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        assert r.approval.get("status") == "pending"
        assert r.current_stage == "structured_patch_created"


class TestReplayParseFailed:
    def test_parse_failed_replay(self, tmp_path):
        from packages.orchestration.event_replay import replay_job
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "autorun_builder_completed", "metadata": {"provider": "ollama"}},
            {"event": "builder_patch_parsed", "metadata": {
                "parse_success": False, "error_kind": "prose_only",
                "stop_reason": "provider_output_prose_only",
            }},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        assert r.stop_reason == "provider_output_prose_only"
        assert r.structured_patch["parse_success"] is False


class TestReplayRepairLoop:
    def test_repair_loop_replay(self, tmp_path):
        from packages.orchestration.event_replay import replay_job
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "repair_loop_cycle_started", "metadata": {"cycle": 2, "max_cycles": 3}},
            {"event": "repair_loop_stopped", "metadata": {"reason": "repair_budget_exhausted"}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        assert r.repair["used"] is True
        assert r.repair["cycle"] == 2
        assert r.stop_reason == "repair_budget_exhausted"


class TestReplayNoRawLeaks:
    def test_no_raw_content(self, tmp_path):
        from packages.orchestration.event_replay import replay_job, export_replay_json
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {"goal": "fix SECRET_KEY bug"}},
            {"event": "builder_patch_parsed", "metadata": {
                "parse_success": True, "output_hash": "h1",
                "raw_output": "def hello(): return SECRET_KEY",
            }},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        r_json = json.dumps(export_replay_json(r))
        assert "SECRET_KEY" not in r_json
        assert "def hello" not in r_json


class TestCheckpoints:
    def test_fixture_success_checkpoints(self, tmp_path):
        from packages.orchestration.event_replay import replay_job, find_checkpoints
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "source_context_injected", "metadata": {"file_count": 2, "estimated_tokens": 300}},
            {"event": "autorun_builder_completed", "metadata": {"provider": "fixture"}},
            {"event": "builder_patch_parsed", "metadata": {"parse_success": True}},
            {"event": "builder_bridge_intent_approved", "metadata": {"intent_id": "i-1"}},
            {"event": "patch_intent_applied", "metadata": {}},
            {"event": "test_run_completed", "metadata": {"exit_code": 0, "passed": True}},
            {"event": "proof_collected", "metadata": {}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        cps = find_checkpoints(r)
        kinds = [c.kind for c in cps]
        assert "context_ready" in kinds
        assert "approval_recorded" in kinds
        assert "source_apply_proven" in kinds
        assert "tests_passed" in kinds

    def test_approval_pending_checkpoint_blocked(self, tmp_path):
        from packages.orchestration.event_replay import replay_job, find_checkpoints
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "source_context_injected", "metadata": {"file_count": 1}},
            {"event": "builder_patch_parsed", "metadata": {"parse_success": True}},
            {"event": "structured_patch_intent_created", "metadata": {}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        cps = find_checkpoints(r)
        intent_cp = next(c for c in cps if c.kind == "patch_intent_created")
        assert intent_cp.safe_to_resume is False
        assert intent_cp.blocked_reason == "approval_pending"

    def test_tests_failed_checkpoint(self, tmp_path):
        from packages.orchestration.event_replay import replay_job, find_checkpoints
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "source_context_injected", "metadata": {}},
            {"event": "builder_patch_parsed", "metadata": {"parse_success": True}},
            {"event": "builder_bridge_intent_approved", "metadata": {"intent_id": "i-1"}},
            {"event": "patch_intent_applied", "metadata": {}},
            {"event": "test_run_completed", "metadata": {"exit_code": 1, "passed": False}},
            {"event": "repair_loop_cycle_started", "metadata": {"cycle": 1, "max_cycles": 3}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        cps = find_checkpoints(r)
        fail_cp = next(c for c in cps if c.kind == "tests_failed")
        assert fail_cp.safe_to_resume is True

    def test_next_command_catalog_valid(self, tmp_path):
        from apps.cli.command_catalog import CATALOG
        from packages.orchestration.event_replay import replay_job, find_checkpoints
        catalog_groups = {c.group_id for c in CATALOG}

        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "source_context_injected", "metadata": {}},
            {"event": "builder_patch_parsed", "metadata": {"parse_success": True}},
            {"event": "builder_bridge_intent_approved", "metadata": {"intent_id": "i-1"}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        cps = find_checkpoints(r)
        for cp in cps:
            if cp.next_command:
                parts = cp.next_command.split()
                assert parts[0] == "remedy"
                assert parts[1] in catalog_groups or parts[1] == "do"


class TestResumeDryRun:
    def test_dry_run_from_approved(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.event_replay import resume_dry_run
        from packages.core.models import Job, RunState
        jid = uuid4()
        job = Job(id=jid, name="test", state=RunState.COMPLETED)
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "source_context_injected", "metadata": {}},
            {"event": "builder_patch_parsed", "metadata": {"parse_success": True}},
            {"event": "builder_bridge_intent_approved", "metadata": {"intent_id": "i-1"}},
        ]
        _write_events(tmp_path, str(jid), events)
        dr = resume_dry_run(job, f"{jid}-approved", str(tmp_path))
        assert dr.can_resume is True
        assert dr.would_run_stage == "source_apply"

    def test_dry_run_checkpoint_not_found(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.event_replay import resume_dry_run
        from packages.core.models import Job, RunState
        jid = uuid4()
        job = Job(id=jid, name="test", state=RunState.COMPLETED)
        dr = resume_dry_run(job, "nonexistent", str(tmp_path))
        assert dr.can_resume is False
        assert dr.blocked_reason == "checkpoint_not_found"

    def test_dry_run_not_resumable(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.event_replay import resume_dry_run
        from packages.core.models import Job, RunState
        jid = uuid4()
        job = Job(id=jid, name="test", state=RunState.COMPLETED)
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "autorun_provider_error", "metadata": {"stop_reason": "provider_unavailable"}},
        ]
        _write_events(tmp_path, str(jid), events)
        dr = resume_dry_run(job, f"{jid}-stopped", str(tmp_path))
        assert dr.can_resume is False
