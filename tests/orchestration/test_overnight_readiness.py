"""Bounded Overnight Preparation v0 tests (Steps 1246-1267).

Readiness truth (no event-only proof), redaction, and architecture guards for the
read-only overnight preparation layer. No execution, no mutation.
"""
from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.storage import save_job, load_job
from packages.orchestration import overnight_readiness as OV
from packages.orchestration import repair_loop as RL


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def _job(data_dir, *, tasks=True, perms=True):
    t = [Task(description="t")] if tasks else []
    job = Job(id=uuid4(), name="ov", tasks=t, metadata={"target_repo": "."},
              permissions={"repo_generated_write": "allow", "repo_test_run": "allow"} if perms else {})
    save_job(job, root=data_dir)
    return job


def _add_failure(data_dir, job, *, resolved=False, related_files=None, safe_summary="fail"):
    t = job.tasks[0]
    fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=t.id,
                  metadata={"test_failure": True, "failure_kind": "test_failed",
                            "related_test_run_id": "tr", "related_apply_id": "ap",
                            "related_task_id": str(t.id), "exit_code": 1,
                            "safe_summary": safe_summary, "related_files": related_files or [],
                            **({"failure_resolved": True} if resolved else {})})
    job.artifacts.append(fa)
    save_job(job, root=data_dir)
    return str(fa.id)


# ---------------------------------------------------------------------------
# Policy (1247)
# ---------------------------------------------------------------------------


class TestPolicy:
    def test_default_is_report_only(self):
        p = OV.default_overnight_policy()
        assert p.allow_apply is False and p.allow_repair_apply is False
        assert p.allow_provider is False and p.allow_revert is False
        assert p.max_cycles == 0
        assert p.execution_enabled is False

    def test_execution_enabled_requires_cycles_and_apply(self):
        p = OV.BoundedOvernightPolicy(max_cycles=1, allow_apply=True)
        assert p.execution_enabled is True


# ---------------------------------------------------------------------------
# Readiness truth (1265)
# ---------------------------------------------------------------------------


class TestReadinessTruth:
    def test_default_policy_never_unattended(self, env):
        job = _job(env)
        rep = OV.build_overnight_readiness(str(job.id), env)
        assert rep.ready is True
        assert rep.can_run_unattended is False  # default policy is report-only

    def test_event_only_does_not_make_unattended(self, env):
        from packages.orchestration.timeline import append_run_event
        job = _job(env)
        # Inject events claiming snapshot/test/proof — must not change durable truth.
        for ev in ("snapshot_create_completed", "test_run_completed", "proof_collected"):
            append_run_event(env, UUID(str(job.id)), event=ev, metadata={"exit_code": 0})
        rep = OV.build_overnight_readiness(str(job.id), env)
        assert rep.can_run_unattended is False
        snap = next(i for i in rep.checklist if i.id == "snapshot_verified")
        assert snap.status != "done"  # no durable verified snapshot

    def test_verified_durable_snapshot_counts(self, env, monkeypatch):
        # Run a real do_continue cycle to create a verified durable apply.
        from tests.orchestration.test_do_continue import make_continue_job, _fake_test
        import packages.orchestration.test_execution_service as tes
        from packages.orchestration import do_continue as dc
        repo = env.parent / "repo"; repo.mkdir(exist_ok=True)
        job, iid = make_continue_job(env, repo)
        fn, _ = _fake_test(env, status="passed")
        monkeypatch.setattr(tes, "execute_test_run", fn)
        dc.run_do_continue(dc.ContinueRequest(job_id=str(job.id)), env)
        rep = OV.build_overnight_readiness(str(job.id), env)
        assert rep.evidence_summary["verified_snapshots"] >= 1
        snap = next(i for i in rep.checklist if i.id == "snapshot_verified")
        assert snap.status == "done"

    def test_unresolved_failure_blocks_unattended(self, env):
        job = _job(env)
        _add_failure(env, job)
        rep = OV.build_overnight_readiness(str(job.id), env)
        assert "unresolved_failures" in rep.blockers
        assert rep.can_run_unattended is False

    def test_repair_pending_blocks_unattended(self, env):
        job = _job(env)
        fa = _add_failure(env, job)
        job2 = load_job(UUID(str(job.id)), env)
        att = RL.RepairAttempt(attempt_id="a1", job_id=str(job.id), failure_artifact_id=fa,
                               repair_intent_id="ri-1", status="approval_required",
                               source="cli_v1", created_at="t")
        RL.save_repair_attempt(job2, att)
        rep = OV.build_overnight_readiness(str(job.id), env)
        assert "repair_pending_approval" in rep.blockers
        na = rep.next_action
        assert na.command == f"remedy patch approve {job.id} ri-1"

    def test_no_command_for_missing_entity(self, env):
        job = _job(env)  # no intents, no failures
        rep = OV.build_overnight_readiness(str(job.id), env)
        # Must not suggest approve/continue/repair when nothing exists.
        assert "approve" not in rep.next_action.command
        assert "do continue" not in rep.next_action.command
        assert "repair propose" not in rep.next_action.command

    def test_provider_not_supported(self, env):
        job = _job(env)
        rep = OV.build_overnight_readiness(str(job.id), env)
        prov = next(c for c in rep.capabilities if c.name == "can_provider_build")
        assert prov.status == "not_supported"

    def test_overnight_capability_blocked_by_default(self, env):
        job = _job(env)
        rep = OV.build_overnight_readiness(str(job.id), env)
        ovr = next(c for c in rep.capabilities if c.name == "can_run_overnight")
        assert ovr.status == "blocked"

    def test_next_actions_catalog_backed(self, env):
        from packages.orchestration.do_run import validate_next_safe_action_command
        job = _job(env)
        fa = _add_failure(env, job)
        rep = OV.build_overnight_readiness(str(job.id), env)
        assert validate_next_safe_action_command(rep.next_action.command)


# ---------------------------------------------------------------------------
# Plan (1256) — dry-run only
# ---------------------------------------------------------------------------


class TestPlan:
    def test_default_plan_would_not_run(self, env):
        job = _job(env)
        plan = OV.build_overnight_plan(str(job.id), env)
        assert plan.would_run is False  # default policy is report-only

    def test_missing_job_safe(self, env):
        plan = OV.build_overnight_plan(str(uuid4()), env)
        assert plan.would_run is False
        assert "unsupported_state" in plan.stop_points


# ---------------------------------------------------------------------------
# Redaction (1266)
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_no_raw_leak(self, env):
        job = _job(env)
        _add_failure(env, job, related_files=["/home/u/.env", "/etc/passwd"],
                     safe_summary="token=sk-secret-123 Traceback (most recent call last)")
        rep = OV.build_overnight_readiness(str(job.id), env)
        blobs = [
            json.dumps(OV.export_readiness_json(rep)),
            json.dumps(OV.export_plan_json(OV.build_overnight_plan(str(job.id), env))),
            OV.render_overnight_report_markdown(OV.build_overnight_report(str(job.id), env)),
        ]
        for b in blobs:
            assert "/home/" not in b
            assert "/etc/passwd" not in b
            assert "Traceback" not in b
            assert "sk-secret-123" not in b
            assert "diff --git" not in b


# ---------------------------------------------------------------------------
# Architecture guards (1267)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    SRC = Path("packages/orchestration/overnight_readiness.py").read_text()

    def _imports(self):
        return [ln for ln in self.SRC.splitlines()
                if ln.strip().startswith(("import ", "from "))]

    def test_no_apply_service_import(self):
        for ln in self._imports():
            assert "patch_apply" not in ln
            assert "source_apply" not in ln

    def test_no_test_execution(self):
        for ln in self._imports():
            assert "test_execution_service" not in ln
        assert "execute_test_run" not in self.SRC

    def test_no_repair_propose_call(self):
        assert "run_repair_attempt" not in self.SRC

    def test_no_provider_or_subprocess(self):
        # No provider/ollama/subprocess IMPORTS (the word may appear in safe
        # "deferred" reason strings).
        for ln in self._imports():
            assert "ollama" not in ln.lower()
            assert "provider" not in ln.lower()
            assert "subprocess" not in ln
        assert "import subprocess" not in self.SRC

    def test_no_shell_true(self):
        assert "shell=True" not in self.SRC

    def test_read_only_no_save_job(self):
        # Read-only: the readiness layer must not persist the job.
        assert "save_job(" not in self.SRC
