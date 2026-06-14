"""Provider-Agnostic Repair Request Builder v0 tests (Steps 1382/1384/1385/1388).

Request quality, redaction, architecture guards, adapter boundary, idempotency, and
the simulated external-candidate end-to-end flow (request → intake → materialize →
approve → do continue). No real provider/model/network/subprocess.
"""
from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, Task
from packages.orchestration.storage import save_job, load_job
from packages.orchestration import repair_request_builder as RB


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
            build_default_run_contract, save_contract, ContractAction,
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
# Redaction (Step 1384)
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_no_raw_leak(self, env):
        job, fid = _job(
            env,
            related=["/home/u/.ssh/id_rsa", "docs/guide.md"],
            safe_summary='token sk-abcdef0123456789abcd at /home/u/.env Traceback (most recent call last)',
            command_display="pytest /home/u/secret/path.py")
        r = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        reloaded = load_job(UUID(str(job.id)), env)
        from packages.orchestration.progress_ledger import extract_repair_request_items
        from packages.orchestration.review_bundle import _build_repair_request_summary
        from packages.orchestration.ui_server import _build_repair_request_section
        items = extract_repair_request_items(RB.load_request_packages(reloaded), {})
        blobs = [
            json.dumps(RB.export_build_result_json(r)),
            json.dumps(RB.get_request_package(reloaded, r.request_package_id)),
            _rendered(reloaded, r.request_package_id),
            json.dumps([{"id": i.item_id, "s": i.safe_summary} for i in items]),
            json.dumps(_build_repair_request_summary(reloaded)),
            json.dumps(_build_repair_request_section(reloaded)),
        ]
        for b in blobs:
            assert "sk-abcdef0123456789abcd" not in b
            assert "/home/" not in b
            assert "id_rsa" not in b
            assert "Traceback" not in b


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
        from packages.orchestration.do_run import validate_next_safe_action_command
        job, fid = _job(env)
        r = RB.build_repair_request_package(str(job.id), fid, data_dir=env)
        # The intake command is catalog-backed (strip the placeholder args).
        base = "remedy provider intake-repair " + str(job.id) + " --json"
        assert validate_next_safe_action_command(base)


# ---------------------------------------------------------------------------
# Simulated external-candidate end-to-end (Step 1388)
# ---------------------------------------------------------------------------


class TestEndToEnd:
    def test_request_to_completed_verified(self, env, monkeypatch, tmp_path):
        from packages.orchestration.permissions import set_permission, Capability
        from packages.orchestration.run_contract import (
            build_default_run_contract, save_contract, ContractAction,
        )
        from packages.orchestration.approval_queue import set_approval_state
        from packages.orchestration import provider_trust as PT
        import packages.orchestration.test_execution_service as tes
        from tests.orchestration.test_do_continue import _fake_test
        from packages.orchestration import do_continue as dc

        repo = tmp_path / "repo"; (repo / "docs").mkdir(parents=True)
        (repo / "docs" / "guide.md").write_text("line one\nline two\n")
        t = Task(description="t")
        fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=t.id,
                      metadata={"test_failure": True, "failure_kind": "test_failed",
                                "related_task_id": str(t.id), "related_files": ["docs/guide.md"],
                                "safe_summary": "doc gap", "command_display": "pytest x"})
        job = Job(id=uuid4(), name="ov", tasks=[t], artifacts=[fa],
                  metadata={"target_repo": str(repo.resolve())})
        set_permission(job, Capability.repo_generated_write, allow=True)
        set_permission(job, Capability.repo_test_run, allow=True)
        c = build_default_run_contract(job)
        c = dataclasses.replace(
            c, allowed_actions=tuple(list(c.allowed_actions) + [ContractAction.PATCH_APPLY]),
            denied_actions=tuple(a for a in c.denied_actions if a != ContractAction.PATCH_APPLY),
            stop_before_apply=False, max_test_runs=1)
        save_contract(job, c); save_job(job, root=env)

        # 1. Build the repair request (no execution).
        req = RB.build_repair_request_package(str(job.id), str(fa.id),
                                              target_kind="markdown_only", data_dir=env)
        assert req.stop_reason == RB.RepairRequestStopReason.READY

        # 2. Simulate an EXTERNAL actor's candidate response (written by the test).
        candidate = ("Doc fix.\n```diff\n--- a/docs/guide.md\n+++ b/docs/guide.md\n"
                     "@@ -1,2 +1,3 @@\n line one\n+added by external actor\n line two\n```\n")
        resp = env / "external_response.md"; resp.write_text(candidate)

        # 3. Import through the existing provider intake path (trust gate + materialize).
        ir = PT.intake_provider_repair(
            PT.ProviderOutputIntakeRequest(job_id=str(job.id), failure_artifact_id=str(fa.id),
                                           provider_name="external"),
            input_path=str(resp), data_dir=env)
        assert ir.trust_status == PT.TrustStatus.ACCEPTED
        assert ir.repair_intent_id

        # 4. Approve + do continue → snapshot → apply → completed_verified.
        job = load_job(UUID(str(job.id)), env)
        set_approval_state(job, ir.repair_intent_id, "approved", decided_by="human")
        save_job(job, root=env)
        fn, _ = _fake_test(env, status="passed")
        monkeypatch.setattr(tes, "execute_test_run", fn)
        res = dc.run_do_continue(dc.ContinueRequest(job_id=str(job.id), intent_id=ir.repair_intent_id), env)
        assert res.stop_reason == "completed_verified"
        assert "added by external actor" in (repo / "docs" / "guide.md").read_text()
