"""Provider-Agnostic Repair Request Builder v0 tests (Steps 1382/1384/1385/1388).

Request quality, redaction, architecture guards, adapter boundary and idempotency.
No real provider/model/network/subprocess.

Remedy deliberately has no end-to-end flow test here any more: F275 T001 deleted the
Provider Trust Gate and its `provider intake-repair` command, so the request → intake
→ materialize → approve → do continue round trip the old test drove no longer exists
(R-0868).
"""
from __future__ import annotations

import dataclasses
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, Task
from packages.orchestration import repair_request_builder as RB
from packages.orchestration.storage import load_job, save_job


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def _job(data_dir, *, related=("docs/guide.md",), safe_summary="assertion failed",
         command_display="pytest tests/x.py"):
    t = Task(description="t")
    fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=t.id,
                  metadata={"test_failure": True, "failure_kind": "test_failed",
                            "related_task_id": str(t.id), "related_test_run_id": "tr",
                            "related_apply_id": "ap", "related_files": list(related),
                            "exit_code": 1, "safe_summary": safe_summary,
                            "command_display": command_display})
    job = Job(id=uuid4(), name="ov", tasks=[t], artifacts=[fa], metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return job, str(fa.id)


def _rendered(job, rpid):
    pkg = RB.get_request_package(job, rpid)
    sections = [RB.RepairRequestSection(**s) for s in pkg["sections"]]
    obj = {k: v for k, v in pkg.items() if k != "sections"}
    return RB.render_request_markdown(RB.RepairRequestPackage(sections=sections, **obj))


# ---------------------------------------------------------------------------
# Builder basics
# ---------------------------------------------------------------------------


class TestBuilder:
    def test_ready_and_stored(self, env):
        job, fid = _job(env)
        r = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        assert r.stop_reason == RB.RepairRequestStopReason.READY
        assert r.request_package_id and r.generator_record_id
        assert (env / "workspaces" / str(job.id) / "repair_request_packages"
                / r.request_package_id / "request.md").exists()

    def test_idempotent(self, env):
        job, fid = _job(env)
        r1 = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        r2 = RB.build_repair_request_package(str(load_job(UUID(str(job.id)), env).id), fid, data_dir=env)
        assert r1.request_package_id == r2.request_package_id
        assert len(RB.load_request_packages(load_job(UUID(str(job.id)), env))) == 1

    def test_new_forces_fresh(self, env):
        job, fid = _job(env)
        r1 = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        r2 = RB.build_repair_request_package(str(load_job(UUID(str(job.id)), env).id), fid, new=True, data_dir=env)
        assert r1.request_package_id != r2.request_package_id

    def test_missing_job(self, env):
        r = RB.build_repair_request_package(str(uuid4()), str(uuid4()), data_dir=env)
        assert r.stop_reason == RB.RepairRequestStopReason.JOB_NOT_FOUND
        assert not r.request_package_id

    def test_contract_blocked(self, env):
        from packages.orchestration.run_contract import (
            ContractAction,
            build_default_run_contract,
            save_contract,
        )
        job, fid = _job(env)
        c = build_default_run_contract(job)
        c = dataclasses.replace(
            c, allowed_actions=tuple(a for a in c.allowed_actions
                                     if a != ContractAction.PREPARE_REPAIR_REQUEST))
        save_contract(job, c); save_job(job, root=env)
        r = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        assert r.stop_reason == RB.RepairRequestStopReason.CONTRACT_BLOCKED
        assert not r.request_package_id


# ---------------------------------------------------------------------------
# Request quality (Step 1382)
# ---------------------------------------------------------------------------


class TestRequestQuality:
    def test_contains_required_schema(self, env):
        job, fid = _job(env)
        r = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        text = _rendered(load_job(UUID(str(job.id)), env), r.request_package_id)
        assert "unified_diff" in text and "target_files" in text and "patch_format" in text

    def test_says_one_candidate(self, env):
        job, fid = _job(env)
        r = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        text = _rendered(load_job(UUID(str(job.id)), env), r.request_package_id)
        assert "EXACTLY ONE" in text

    def test_says_no_apply_or_test_claims(self, env):
        job, fid = _job(env)
        r = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        text = _rendered(load_job(UUID(str(job.id)), env), r.request_package_id).lower()
        assert "applied or tested" in text

    def test_says_relative_paths_only(self, env):
        job, fid = _job(env)
        r = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        text = _rendered(load_job(UUID(str(job.id)), env), r.request_package_id).lower()
        assert "relative" in text and "no absolute" in text

    def test_says_no_secrets_protected(self, env):
        job, fid = _job(env)
        r = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        text = _rendered(load_job(UUID(str(job.id)), env), r.request_package_id).lower()
        assert "secret" in text and "protected" in text

    def test_includes_safe_failure_summary(self, env):
        job, fid = _job(env, safe_summary="parser drops trailing newline")
        r = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        text = _rendered(load_job(UUID(str(job.id)), env), r.request_package_id)
        assert "parser drops trailing newline" in text

    def test_no_subscription_account_ide_assumption(self, env):
        # Provider-agnostic: request must not require any subscription/account/IDE.
        job, fid = _job(env)
        r = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        text = _rendered(load_job(UUID(str(job.id)), env), r.request_package_id).lower()
        for bad in ("subscription", "claude max", "account required", "vs code", "jetbrains"):
            assert bad not in text


# ---------------------------------------------------------------------------
# Adapter boundary (Steps 1374-1375)
# ---------------------------------------------------------------------------


class TestAdapterBoundary:
    def test_manual_adapter_describes_no_execution(self):
        ad = RB.ManualCandidateGeneratorAdapter("external")
        d = ad.describe()
        assert d.execution_mode == RB.CandidateGeneratorCapability.MANUAL
        assert d.supports_execution is False
        assert ad.supports_execution() is False

    def test_execute_raises_unavailable(self):
        ad = RB.ManualCandidateGeneratorAdapter()
        with pytest.raises(RB.CandidateGeneratorExecutionUnavailable):
            ad.execute()

    def test_adapter_build_request(self, env):
        job, fid = _job(env)
        ad = RB.ManualCandidateGeneratorAdapter("external")
        r = ad.build_request(str(job.id), fid, data_dir=env)
        assert r.stop_reason == RB.RepairRequestStopReason.READY


# ---------------------------------------------------------------------------
# Architecture guards (Step 1385)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    SRC = Path("packages/orchestration/repair_request_builder.py").read_text()

    def _imports(self):
        return [ln for ln in self.SRC.splitlines()
                if ln.strip().startswith(("import ", "from "))]

    def test_no_network_or_subprocess(self):
        for ln in self._imports():
            for bad in ("subprocess", "socket", "requests", "httpx", "urllib", "http.client", "selenium", "playwright"):
                assert bad not in ln
        assert "import subprocess" not in self.SRC
        assert "shell=True" not in self.SRC

    def test_no_provider_sdk(self):
        for ln in self._imports():
            low = ln.lower()
            for bad in ("ollama", "anthropic", "openai", "litellm", "import claude"):
                assert bad not in low

    def test_no_apply_test_or_intent_creation(self):
        for ln in self._imports():
            assert "patch_apply" not in ln
            assert "test_execution_service" not in ln
            assert "provider_patch_material" not in ln  # no materialization/intent here
        # No direct call to provider intake from request generation.
        assert "intake_provider_repair" not in self.SRC

    def test_next_action_catalog_backed(self, env):
        # Both halves matter. The two DEAD commands must be absent from every step the
        # builder emits (F275 T001 deleted them), and every command that IS still named
        # must resolve in the shipped catalog.
        from packages.orchestration.do_run import validate_next_safe_action_command
        job, fid = _job(env)
        r = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        steps = "\n".join(r.next_steps)
        assert "provider intake-repair" not in steps
        assert "provider trust-show" not in steps
        named = [c for c in ("remedy patch approve", "remedy do continue")
                 if c in steps]
        assert named, "the surviving steps must still name at least one live command"
        for cmd in named:
            assert validate_next_safe_action_command(f"{cmd} {job.id} --json")
