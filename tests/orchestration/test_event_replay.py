"""Tests: event replay model and checkpoint detection."""
from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4


def _write_events(tmp_path, job_id, events):
    runs_dir = tmp_path / "job_logs" / str(job_id)
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
        from packages.orchestration.event_replay import export_replay_json, replay_job
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
        from packages.orchestration.event_replay import find_checkpoints, replay_job
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
        from packages.orchestration.event_replay import find_checkpoints, replay_job
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

    def test_tests_failed_checkpoint_blocked(self, tmp_path):
        from packages.orchestration.event_replay import find_checkpoints, replay_job
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
        assert fail_cp.safe_to_resume is False
        assert fail_cp.blocked_reason == "resume_mode_not_implemented"

    def test_context_ready_inspectable_not_resumable(self, tmp_path):
        from packages.orchestration.event_replay import find_checkpoints, replay_job
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "source_context_injected", "metadata": {"file_count": 2}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        cps = find_checkpoints(r)
        ctx_cp = next(c for c in cps if c.kind == "context_ready")
        assert ctx_cp.safe_to_resume is False
        assert ctx_cp.status == "inspectable"
        assert ctx_cp.blocked_reason == "resume_mode_not_implemented"

    def test_approval_recorded_blocked_missing_patch(self, tmp_path):
        from packages.orchestration.event_replay import find_checkpoints, replay_job
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
        approved_cp = next(c for c in cps if c.kind == "approval_recorded")
        assert approved_cp.safe_to_resume is False
        assert approved_cp.blocked_reason == "missing_patch_payload"

    def test_source_apply_proven_resumable(self, tmp_path):
        from packages.orchestration.event_replay import find_checkpoints, replay_job
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "source_context_injected", "metadata": {}},
            {"event": "builder_patch_parsed", "metadata": {"parse_success": True}},
            {"event": "builder_bridge_intent_approved", "metadata": {"intent_id": "i-1"}},
            {"event": "patch_intent_applied", "metadata": {}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        cps = find_checkpoints(r)
        applied_cp = next(c for c in cps if c.kind == "source_apply_proven")
        assert applied_cp.safe_to_resume is True
        assert applied_cp.resume_mode == "from_apply"

    def test_next_command_catalog_valid(self, tmp_path):
        import re

        from apps.cli.command_catalog import CATALOG
        from packages.orchestration.event_replay import find_checkpoints, replay_job
        catalog_subs = {(c.group_id, c.subcommand) for c in CATALOG}

        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "source_context_injected", "metadata": {}},
            {"event": "builder_patch_parsed", "metadata": {"parse_success": True}},
            {"event": "builder_bridge_intent_approved", "metadata": {"intent_id": "i-1"}},
            {"event": "patch_intent_applied", "metadata": {}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        cps = find_checkpoints(r)
        for cp in cps:
            if cp.next_command:
                m = re.match(r"remedy\s+(\w+)\s+(\w[\w-]*)", cp.next_command)
                assert m, f"Cannot parse command: {cp.next_command}"
                group, sub = m.group(1), m.group(2)
                assert (group, sub) in catalog_subs, (
                    f"Command 'remedy {group} {sub}' not in catalog "
                    f"(from checkpoint {cp.kind})"
                )


class TestR12001Regression:
    """R-12001: resume must not claim success for no-op behavior."""

    def test_from_approval_not_resumable(self, tmp_path):
        from packages.orchestration.event_replay import find_checkpoints, replay_job
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
        approved = next(c for c in cps if c.kind == "approval_recorded")
        assert approved.safe_to_resume is False, (
            "R-12001: from_approval must not be safe_to_resume=True "
            "unless patch payload is persisted and recoverable"
        )

    def test_no_resumed_true_for_unimplemented_mode(self, tmp_path):
        from packages.orchestration.event_replay import find_checkpoints, replay_job
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "source_context_injected", "metadata": {"file_count": 1}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        cps = find_checkpoints(r)
        for cp in cps:
            if cp.blocked_reason == "resume_mode_not_implemented":
                assert cp.safe_to_resume is False


class TestCheckpointDataContract:
    def test_from_approval_shows_missing_data(self, tmp_path):
        from packages.orchestration.event_replay import export_checkpoints_json, find_checkpoints, replay_job
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "builder_patch_parsed", "metadata": {"parse_success": True}},
            {"event": "builder_bridge_intent_approved", "metadata": {"intent_id": "i-1"}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        cps = find_checkpoints(r)
        approved = next(c for c in cps if c.kind == "approval_recorded")
        assert "structured_patch_payload" in approved.missing_data
        assert approved.resume_mode_supported is False
        exported = export_checkpoints_json(cps)
        approved_j = next(c for c in exported if c["kind"] == "approval_recorded")
        assert "missing_data" in approved_j
        assert "required_data" in approved_j

    def test_from_apply_shows_requirements(self, tmp_path):
        from packages.orchestration.event_replay import find_checkpoints, replay_job
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "patch_intent_applied", "metadata": {}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        cps = find_checkpoints(r)
        applied = next(c for c in cps if c.kind == "source_apply_proven")
        assert "repo_path" in applied.required_data
        assert "test_candidate" in applied.required_data
        assert applied.resume_mode_supported is True

    def test_tests_failed_shows_repair_missing(self, tmp_path):
        from packages.orchestration.event_replay import find_checkpoints, replay_job
        jid = str(uuid4())
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "patch_intent_applied", "metadata": {}},
            {"event": "test_run_completed", "metadata": {"exit_code": 1, "passed": False}},
        ]
        _write_events(tmp_path, jid, events)
        r = replay_job(jid, str(tmp_path))
        cps = find_checkpoints(r)
        fail_cp = next(c for c in cps if c.kind == "tests_failed")
        assert "repair_context" in fail_cp.missing_data
        assert fail_cp.resume_mode_supported is False


class TestDryRunValidation:
    def test_dry_run_no_permission_blocked(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job, RunState
        from packages.orchestration.event_replay import resume_dry_run
        jid = uuid4()
        job = Job(id=jid, name="test", state=RunState.COMPLETED, permissions={})
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "patch_intent_applied", "metadata": {}},
        ]
        _write_events(tmp_path, str(jid), events)
        dr = resume_dry_run(job, f"{jid}-applied", str(tmp_path))
        assert dr.can_resume is False
        assert dr.blocked_reason == "permission_denied"

    def test_dry_run_no_repo_blocked(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job, RunState
        from packages.orchestration.event_replay import resume_dry_run
        from packages.orchestration.permissions import Capability, set_permission
        jid = uuid4()
        job = Job(id=jid, name="test", state=RunState.COMPLETED, metadata={})
        set_permission(job, Capability.repo_test_run, allow=True)
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "patch_intent_applied", "metadata": {}},
        ]
        _write_events(tmp_path, str(jid), events)
        dr = resume_dry_run(job, f"{jid}-applied", str(tmp_path))
        assert dr.can_resume is False
        assert dr.blocked_reason == "missing_repo_path"

    def test_dry_run_creates_no_events(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job, RunState
        from packages.orchestration.event_replay import resume_dry_run
        from packages.orchestration.timeline import load_run_events
        jid = uuid4()
        job = Job(id=jid, name="test", state=RunState.COMPLETED, permissions={})
        events = [{"event": "autorun_started", "metadata": {}}]
        _write_events(tmp_path, str(jid), events)
        before = load_run_events(tmp_path, str(jid))
        resume_dry_run(job, f"{jid}-applied", str(tmp_path))
        after = load_run_events(tmp_path, str(jid))
        assert len(after) == len(before)


class TestDocsExist:
    def test_resume_docs_exist(self):
        doc = Path("docs/guides/resume.md")
        assert doc.is_file()
        content = doc.read_text()
        assert "from_apply" in content
        assert "missing_patch_payload" in content
        assert "dry-run" in content.lower()
        assert "read-only" in content.lower()

    def test_resume_docs_commands_catalog_valid(self):
        import re

        from apps.cli.command_catalog import CATALOG
        catalog_subs = {(c.group_id, c.subcommand) for c in CATALOG}

        doc = Path("docs/guides/resume.md")
        content = doc.read_text()
        for m in re.finditer(r"remedy\s+(\w+)\s+(\w[\w-]*)", content):
            group, sub = m.group(1), m.group(2)
            if group == "do":
                continue
            assert (group, sub) in catalog_subs, f"Unknown command: remedy {group} {sub}"


class TestResumeDryRun:
    def test_dry_run_from_approved_blocked(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job, RunState
        from packages.orchestration.event_replay import resume_dry_run
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
        assert dr.can_resume is False
        assert dr.blocked_reason == "missing_patch_payload"

    def test_dry_run_from_apply_resumable(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job, RunState
        from packages.orchestration.event_replay import resume_dry_run
        from packages.orchestration.permissions import Capability, set_permission
        jid = uuid4()
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "pyproject.toml").write_text("[tool.pytest.ini_options]\n")
        (repo / "tests").mkdir()
        (repo / "tests" / "test_x.py").write_text("def test_x(): pass\n")
        job = Job(id=jid, name="test", state=RunState.COMPLETED,
                  metadata={"target_repo": str(repo)})
        set_permission(job, Capability.repo_test_run, allow=True)
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "source_context_injected", "metadata": {}},
            {"event": "builder_patch_parsed", "metadata": {"parse_success": True}},
            {"event": "builder_bridge_intent_approved", "metadata": {"intent_id": "i-1"}},
            {"event": "patch_intent_applied", "metadata": {}},
        ]
        _write_events(tmp_path, str(jid), events)
        dr = resume_dry_run(job, f"{jid}-applied", str(tmp_path))
        assert dr.can_resume is True
        assert dr.would_run_stage == "test_run"

    def test_dry_run_checkpoint_not_found(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job, RunState
        from packages.orchestration.event_replay import resume_dry_run
        jid = uuid4()
        job = Job(id=jid, name="test", state=RunState.COMPLETED)
        dr = resume_dry_run(job, "nonexistent", str(tmp_path))
        assert dr.can_resume is False
        assert dr.blocked_reason == "checkpoint_not_found"

    def test_dry_run_not_resumable(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.core.models import Job, RunState
        from packages.orchestration.event_replay import resume_dry_run
        jid = uuid4()
        job = Job(id=jid, name="test", state=RunState.COMPLETED)
        events = [
            {"event": "autorun_started", "metadata": {}},
            {"event": "autorun_provider_error", "metadata": {"stop_reason": "provider_unavailable"}},
        ]
        _write_events(tmp_path, str(jid), events)
        dr = resume_dry_run(job, f"{jid}-stopped", str(tmp_path))
        assert dr.can_resume is False
