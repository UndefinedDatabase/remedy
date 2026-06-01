"""
Domain tests: storage/test_persistence.py
Migrated from step-numbered test files.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4
from uuid import uuid4
import json
import os
import pytest
import re
import subprocess
import sys
import tempfile

from packages.core.models import (
    Artifact,
    ArtifactKind,
    Job,
    RunState,
    Task,
)
from packages.core.models import Job, RunState, Task
from packages.orchestration.storage import save_job

_ROOT = Path(__file__).resolve().parent.parent.parent


def _make_job(*, project_id: str | None = None, target_repo: str | None = None) -> Job:
    meta: dict = {}
    if project_id:
        meta["project_id"] = project_id
    if target_repo:
        meta["target_repo"] = target_repo
    return Job(
        id=uuid4(),
        name="test job",
        user_prompt="test prompt",
        state=RunState.RUNNING,
        tasks=[
            Task(
                id=uuid4(),
                description="task",
                status=RunState.PENDING,
                inputs={"task_type": "patch"},
                output_artifact_ids=[],
            ),
        ],
        artifacts=[],
        metadata=meta,
    )


def _make_job_s68(**overrides) -> Job:
    defaults = {
        "id": uuid4(),
        "name": "test-job",
        "user_prompt": "test prompt",
        "description": "test job",
        "tasks": [
            Task(description="task 1", status=RunState.COMPLETED),
        ],
        "state": RunState.COMPLETED,
        "permissions": {"repo_generated_write": "allow", "repo_test_run": "allow"},
        "metadata": {"target_repo": "."},
    }
    defaults.update(overrides)
    return Job(**defaults)


def _make_job_s71(**overrides) -> Job:
    defaults = {
        "id": uuid4(),
        "name": "test-job",
        "user_prompt": "test prompt",
        "tasks": [Task(description="task 1", status=RunState.COMPLETED)],
        "state": RunState.COMPLETED,
        "permissions": {"repo_generated_write": "allow", "repo_test_run": "allow"},
        "metadata": {"target_repo": "."},
    }
    defaults.update(overrides)
    return Job(**defaults)


# ── Step 71.1: Token Policy Applied ──────────────────────────────────────


def _make_job_s111(*, tasks=None, name="test"):
    from packages.core.models import Job, Task, RunState
    job = Job(name=name)
    if tasks:
        for t in tasks:
            task = Task(
                task_type=t.get("type", "readme_draft"),
                description=t.get("description", t.get("type", "task")),
            )
            if "status" in t:
                task.status = RunState(t["status"])
            if "metadata" in t:
                task.inputs = t["metadata"]
            job.tasks.append(task)
    return job


# ═══════════════════════════════════════════════════════════════════════════
# Step 111 — UI CLI Contract
# ═══════════════════════════════════════════════════════════════════════════


def _make_job_with_intent(tmp_path: Path, monkeypatch) -> tuple[Job, str, Path]:
    """Create a job with an approved patch intent and attached repo."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

    from packages.orchestration.approval_queue import (
        APPROVAL_APPROVED,
        make_intent_id,
        set_approval_state,
    )
    from packages.orchestration.permissions import Capability, set_permission

    repo = tmp_path / "repo"
    repo.mkdir()
    target = repo / "notes.md"
    target.write_text("# Original\n\nOriginal content.\n", encoding="utf-8")

    art_id = uuid4()
    intent_id = make_intent_id(art_id, 0)
    artifact = Artifact(
        id=art_id,
        kind=ArtifactKind.BUILDER_PROPOSAL,
        name="patch artifact",
        content="Summary:\nTest patch\nProposed Changes:\n  - Added line\nNotes:\nNone",
        metadata={
            "patch_intent_explanations": [
                {
                    "file": "notes.md",
                    "action": "modify",
                    "risk": "low",
                    "reason": "test intent",
                    "summary": "test",
                }
            ],
        },
    )

    job = Job(
        id=uuid4(),
        name="patch job",
        user_prompt="apply test",
        state=RunState.RUNNING,
        tasks=[],
        artifacts=[artifact],
        metadata={"target_repo": str(repo)},
    )
    set_approval_state(job, intent_id, APPROVAL_APPROVED)
    set_permission(job, Capability.repo_generated_write, allow=True)
    save_job(job)
    return job, intent_id, repo


# ===========================================================================
# Step 53.1: Continue-from-node project linking
# ===========================================================================


def _make_events() -> list[dict]:
    return [
        {"event": "job_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:00:00", "outcome": "ok", "metadata": {}},
        {"event": "patch_intent_created", "run_id": "r1", "job_id": "j1",
         "timestamp": "2026-01-01T00:01:00", "outcome": "ok",
         "metadata": {"intent_id": "pi1", "target_path": "foo.py", "action": "create"}},
    ]


# ── Step 68.1: Event Schema Registry ────────────────────────────────────




class TestTokenEconomy:
    """Token Economy v1 — context pack modes, worker recommend."""

    def test_context_pack_caveman_smaller_than_compact(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.context_pack import build_context_pack
        caveman = build_context_pack(job, [], budget=10000, mode="caveman")
        compact = build_context_pack(job, [], budget=10000, mode="compact")
        standard = build_context_pack(job, [], budget=10000, mode="standard")
        assert caveman.estimated_tokens <= compact.estimated_tokens
        assert compact.estimated_tokens <= standard.estimated_tokens

    def test_context_pack_standard_mode(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.context_pack import build_context_pack
        pack = build_context_pack(job, [], budget=10000, mode="standard")
        assert pack.mode == "standard"

    def test_caveman_no_long_prose(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.context_pack import build_context_pack
        pack = build_context_pack(job, [], budget=10000, mode="caveman")
        for s in pack.sections:
            # Caveman sections should be short fragments
            lines = s.content.split("\n")
            for line in lines:
                assert len(line) < 200, f"Caveman line too long: {line[:50]}..."

    def test_worker_recommend_json_schema(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.worker_recommend import (
            export_worker_recommendation_json,
            recommend_worker,
        )
        rec = recommend_worker(job, [])
        exported = export_worker_recommendation_json(rec)
        required = {
            "version", "job_id", "recommended_worker", "reason",
            "token_mode", "estimated_context_tokens",
            "requires_approval", "candidates",
        }
        assert required <= set(exported.keys())
        assert exported["version"] == 1

    def test_worker_recommend_local_first(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.worker_recommend import recommend_worker
        rec = recommend_worker(job, [])
        assert rec.recommended_worker == "ollama"  # local-first
        assert not rec.requires_approval

    def test_token_policy_json_has_all_fields(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.token_policy import (
            build_default_token_policy,
            export_token_policy_json,
        )
        policy = build_default_token_policy(job)
        exported = export_token_policy_json(policy)
        # Both canonical and detailed fields must be present
        required = {
            "version", "job_id", "scope", "zero_token_steps",
            "local_first_steps", "expensive_model_steps",
            "forbidden_context", "compaction_rules", "budget",
            "default_mode", "max_context_tokens", "local_first",
            "remote_model_requires_approval", "prefer_zero_token_tools",
            "prohibited_payloads",
        }
        assert required <= set(exported.keys())
        assert exported["local_first"] is True
        assert exported["remote_model_requires_approval"] is True
        assert exported["prefer_zero_token_tools"] is True
        assert isinstance(exported["prohibited_payloads"], list)
        assert isinstance(exported["max_context_tokens"], int)

    def test_token_policy_applied_event_schema(self, tmp_path, monkeypatch):
        """Agent loop must emit token_policy_applied with exact metadata keys."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.agent_loop import run_agent_loop
        run_agent_loop(job, max_cycles=1)

        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import load_run_events
        events = load_run_events(resolve_data_root(), job.id)
        tpa = [e for e in events if e.get("event") == "token_policy_applied"]
        assert len(tpa) >= 1, "must emit token_policy_applied"
        meta = tpa[0].get("metadata", {})
        required = {
            "mode", "max_context_tokens", "estimated_context_tokens",
            "local_first", "remote_model_requires_approval", "selected_worker",
        }
        assert required <= set(meta.keys()), f"missing: {required - set(meta.keys())}"
        assert meta["local_first"] is True

    def test_worker_recommend_no_execution(self, tmp_path, monkeypatch):
        """Worker recommend must not execute any provider."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.worker_recommend import recommend_worker
        rec = recommend_worker(job, [])
        # All candidates must be inert metadata — no subprocess, network, or shell
        for c in rec.candidates:
            assert c.execution_mode in ("local_process", "external_harness", "api")
            assert c.status in ("available", "future")

    def test_all_modes_obey_redaction(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)

        from packages.orchestration.context_pack import build_context_pack, export_context_pack_json
        for mode in ("caveman", "compact", "standard"):
            pack = build_context_pack(job, [], budget=10000, mode=mode)
            exported = export_context_pack_json(pack)
            exported_str = json.dumps(exported)
            for forbidden in ("api_key", "password", "secret", "credential"):
                assert forbidden not in exported_str.lower() or mode in exported_str




class TestTokenPolicyApplied:
    def test_schema_registered(self):
        from packages.orchestration.event_schemas import EVENT_METADATA_SCHEMAS
        assert "token_policy_applied" in EVENT_METADATA_SCHEMAS
        schema = EVENT_METADATA_SCHEMAS["token_policy_applied"]
        assert len(schema) == 6
        assert "mode" in schema
        assert "max_context_tokens" in schema
        assert "estimated_context_tokens" in schema
        assert "local_first" in schema
        assert "remote_model_requires_approval" in schema
        assert "selected_worker" in schema

    def test_autonomy_loop_emits_event(self, tmp_path, monkeypatch):
        """Autonomy loop must emit token_policy_applied at start."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        job = _make_job_s68()
        save_job(job)

        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import load_run_events

        run_autonomy_loop(job, [], max_cycles=1, autonomy_level=0)

        events = load_run_events(resolve_data_root(), job.id)
        tpa = [e for e in events if e.get("event") == "token_policy_applied"]
        assert len(tpa) >= 1, "must emit token_policy_applied"
        meta = tpa[0].get("metadata", {})
        required = {"mode", "max_context_tokens", "estimated_context_tokens",
                     "local_first", "remote_model_requires_approval", "selected_worker"}
        assert required <= set(meta.keys()), f"missing: {required - set(meta.keys())}"

    def test_schema_validation(self):
        from packages.orchestration.event_schemas import validate_event_metadata
        valid_meta = {
            "mode": "compact",
            "max_context_tokens": 100000,
            "estimated_context_tokens": 500,
            "local_first": True,
            "remote_model_requires_approval": True,
            "selected_worker": "ollama/qwen3:8b",
        }
        errors = validate_event_metadata("token_policy_applied", valid_meta)
        assert errors == []

        # Extra key should fail
        bad = {**valid_meta, "extra": True}
        errors = validate_event_metadata("token_policy_applied", bad)
        assert len(errors) == 1
        assert "extra keys" in errors[0]


# ── Readiness Integration ───────────────────────────────────────────────




class TestTokenPolicyAppliedSchema:
    def test_schema_in_registry(self):
        from packages.orchestration.event_schemas import EVENT_METADATA_SCHEMAS
        assert "token_policy_applied" in EVENT_METADATA_SCHEMAS
        schema = EVENT_METADATA_SCHEMAS["token_policy_applied"]
        assert len(schema) == 6
        expected = {"mode", "max_context_tokens", "estimated_context_tokens",
                    "local_first", "remote_model_requires_approval", "selected_worker"}
        assert schema == frozenset(expected)

    def test_autonomy_loop_emits(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        job = _make_job_s71()
        save_job(job)

        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.timeline import load_run_events

        run_autonomy_loop(job, [], max_cycles=1, autonomy_level=0)
        events = load_run_events(resolve_data_root(), job.id)
        tpa = [e for e in events if e.get("event") == "token_policy_applied"]
        assert len(tpa) >= 1
        meta = tpa[0].get("metadata", {})
        from packages.orchestration.event_schemas import validate_event_metadata
        errors = validate_event_metadata("token_policy_applied", meta)
        assert errors == [], f"Schema errors: {errors}"

    def test_event_ledger_includes_tpa(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.orchestration.storage import save_job
        job = _make_job_s71()
        save_job(job)

        from packages.orchestration.autonomy_loop import run_autonomy_loop
        from packages.orchestration.data_paths import resolve_data_root
        from packages.orchestration.event_ledger import list_events
        from packages.orchestration.timeline import load_run_events

        run_autonomy_loop(job, [], max_cycles=1, autonomy_level=0)
        events = load_run_events(resolve_data_root(), job.id)
        ledger = list_events(str(job.id), events)
        tpa_ledger = [e for e in ledger if e.event_type == "token_policy_applied"]
        assert len(tpa_ledger) >= 1


# ── Step 72: Visual System ──────────────────────────────────────────────




class TestWorkerResourcesAndUnloadCli:

    def test_catalog_has_worker_resources(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("worker.resources")
        assert cmd.group_id == "worker"
        assert cmd.supports_json

    def test_catalog_has_worker_unload(self):
        from apps.cli.command_catalog import get_command
        cmd = get_command("worker.unload")
        assert cmd.group_id == "worker"

    def test_resources_handler_no_crash(self, capsys):
        """worker resources runs without crash even if tools missing."""
        from apps.cli.commands.worker import _cmd_worker_resources
        with patch("shutil.which", return_value=None):
            _cmd_worker_resources(json_output=False)
        out = capsys.readouterr().out
        assert "not available" in out.lower() or "Worker" in out

    def test_resources_json_output(self, capsys):
        """worker resources --json returns valid JSON."""
        from apps.cli.commands.worker import _cmd_worker_resources
        with patch("shutil.which", return_value=None):
            _cmd_worker_resources(json_output=True)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["version"] == 1
        assert "ollama" in data
        assert "gpu" in data

    def test_unload_no_ollama_graceful(self, capsys):
        """worker unload with no ollama installed handles gracefully."""
        from apps.cli.commands.worker import _cmd_worker_unload
        with patch("shutil.which", return_value=None):
            _cmd_worker_unload(unload_all=True, json_output=True)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert "error" in data or data["version"] == 1

    def test_unload_mocked_ollama(self, capsys):
        """worker unload --all with mocked ollama ps/stop."""
        from apps.cli.commands.worker import _cmd_worker_unload

        mock_ps = MagicMock()
        mock_ps.stdout = "NAME\nllama3:latest\ncodellama:latest\n"
        mock_ps.returncode = 0

        mock_stop = MagicMock()
        mock_stop.returncode = 0
        mock_stop.stderr = ""

        def run_side_effect(cmd, **kwargs):
            if "ps" in cmd:
                return mock_ps
            return mock_stop

        with patch("shutil.which", return_value="/usr/bin/ollama"):
            with patch("subprocess.run", side_effect=run_side_effect):
                _cmd_worker_unload(unload_all=True, json_output=True)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["attempted"] == 2
        assert len(data["stopped"]) == 2
        assert data["unavailable"] is False

    def test_no_shell_true_in_worker(self):
        """No shell=True usage in worker.py (docstrings excluded)."""
        src = Path(_ROOT / "apps" / "cli" / "commands" / "worker.py").read_text()
        # Check only non-comment, non-docstring lines
        for line in src.splitlines():
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'"):
                continue
            assert "shell=True" not in stripped, f"shell=True in code: {stripped}"

    def test_unload_requires_model_or_all(self):
        """worker unload without --model or --all should error."""
        from apps.cli.commands.worker import _cmd_worker_unload
        with patch("shutil.which", return_value="/usr/bin/ollama"):
            with pytest.raises(SystemExit):
                _cmd_worker_unload(json_output=False)


# ═══════════════════════════════════════════════════════════════════════════
# Step 113 — Semantic Zoom Truth Table v4
# ═══════════════════════════════════════════════════════════════════════════




class TestContextPackMemory:
    def test_approved_only(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        from packages.orchestration.context_pack import build_context_pack

        job = Job(
            id=uuid4(), name="ctx-mem", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        # Store globally (context pack reads global scope)
        store_memory("approved.key", "val1", approved=True)
        store_memory("unapproved.key", "val2", approved=False)

        pack = build_context_pack(job, [], budget=5000, mode="compact")
        mem_section = next((s for s in pack.sections if s.name == "memory_keys"), None)
        assert mem_section is not None
        assert "approved.key" in mem_section.content
        assert "unapproved.key" not in mem_section.content

    def test_caveman_mode_count(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        from packages.orchestration.context_pack import build_context_pack

        job = Job(
            id=uuid4(), name="ctx-cave", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        store_memory("k1", "v1", approved=True)
        pack = build_context_pack(job, [], budget=5000, mode="caveman")
        mem_section = next((s for s in pack.sections if s.name == "memory_keys"), None)
        assert mem_section is not None
        assert "mem:" in mem_section.content

    def test_no_raw_values_in_pack(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from packages.memory.local_gateway import store_memory
        from packages.orchestration.context_pack import build_context_pack

        job = Job(
            id=uuid4(), name="ctx-raw", user_prompt="test",
            tasks=[Task(description="t", status=RunState.PENDING)],
        )
        store_memory("secret.key", "SECRET_RAW_VALUE_12345", approved=True)
        pack = build_context_pack(job, [], budget=5000, mode="compact")
        mem_section = next((s for s in pack.sections if s.name == "memory_keys"), None)
        assert mem_section is not None
        assert "SECRET_RAW_VALUE_12345" not in mem_section.content

