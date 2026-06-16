"""Trusted Provider Patch Materialization v0 tests (Steps 1353/1355/1361).

Conversion (unified diff / JSON ops), private storage, verification, applyable
intent creation, idempotency, do_continue apply compatibility, redaction, and
architecture guards (no provider SDK / network / subprocess / apply imports).
"""
from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.core.models import Artifact, ArtifactKind, Job, Task
from packages.orchestration import provider_patch_material as PM
from packages.orchestration import provider_trust as PT
from packages.orchestration.storage import load_job, save_job


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"; d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    return d


def _job(data_dir, *, related=("docs/guide.md",)):
    t = Task(description="t")
    fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=t.id,
                  metadata={"test_failure": True, "failure_kind": "test_failed",
                            "related_task_id": str(t.id), "related_files": list(related),
                            "safe_summary": "boom"})
    job = Job(id=uuid4(), name="ov", tasks=[t], artifacts=[fa], metadata={"target_repo": "."})
    save_job(job, root=data_dir)
    return job, str(fa.id)


def _md_diff(path="docs/guide.md"):
    return (f"Fix docs.\n```diff\n--- a/{path}\n+++ b/{path}\n"
            f"@@ -1,2 +1,3 @@\n line one\n+new helpful line\n line two\n```\n")


def _intake(job, data_dir, text, fid=""):
    p = data_dir / f"in-{uuid4().hex[:6]}.md"; p.write_text(text)
    req = PT.ProviderOutputIntakeRequest(job_id=str(job.id), failure_artifact_id=fid,
                                         provider_name="claude")
    return PT.intake_provider_repair(req, input_path=str(p), data_dir=data_dir)


# ---------------------------------------------------------------------------
# Conversion (Steps 1339-1340)
# ---------------------------------------------------------------------------


class TestConversion:
    def test_md_modify_supported(self):
        ext = PM.materialize_unified_diff_to_structured_patch(
            "--- a/docs/x.md\n+++ b/docs/x.md\n@@ -1 +1,2 @@\n a\n+b\n")
        assert ext.ok and ext.action == "modify" and ext.target_path == "docs/x.md"
        assert ext.added_lines == ["b"]

    def test_md_create_supported(self):
        ext = PM.materialize_unified_diff_to_structured_patch(
            "--- /dev/null\n+++ b/docs/new.md\n@@ -0,0 +1,2 @@\n+line a\n+line b\n")
        assert ext.ok and ext.action == "create"
        assert ext.added_lines == ["line a", "line b"]

    def test_source_file_unsupported(self):
        ext = PM.materialize_unified_diff_to_structured_patch(
            "--- a/src/app.py\n+++ b/src/app.py\n@@ -1 +1 @@\n-a\n+b\n")
        assert not ext.ok and ext.reason == "non_markdown_target"

    def test_delete_unsupported(self):
        ext = PM.materialize_unified_diff_to_structured_patch(
            "--- a/docs/x.md\n+++ /dev/null\n@@ -1 +0,0 @@\n-a\n")
        assert not ext.ok and ext.reason == "delete_unsupported"

    def test_rename_unsupported(self):
        ext = PM.materialize_unified_diff_to_structured_patch(
            "rename from docs/a.md\nrename to docs/b.md\n")
        assert not ext.ok and ext.reason == "rename_unsupported"

    def test_binary_unsupported(self):
        ext = PM.materialize_unified_diff_to_structured_patch("GIT binary patch\n...\n")
        assert not ext.ok and ext.reason == "binary_patch"

    def test_multi_file_unsupported(self):
        ext = PM.materialize_unified_diff_to_structured_patch(
            "--- a/docs/a.md\n+++ b/docs/a.md\n@@ -1 +1 @@\n+x\n"
            "--- a/docs/b.md\n+++ b/docs/b.md\n@@ -1 +1 @@\n+y\n")
        assert not ext.ok and ext.reason == "not_single_target"

    def test_json_ops_supported(self):
        ext = PM.materialize_structured_operations(
            [{"path": "docs/notes.md", "op": "modify", "content": ["a", "b"]}])
        assert ext.ok and ext.action == "modify" and ext.added_lines == ["a", "b"]

    def test_json_ops_source_unsupported(self):
        ext = PM.materialize_structured_operations(
            [{"path": "src/x.py", "op": "modify", "content": ["a"]}])
        assert not ext.ok


# ---------------------------------------------------------------------------
# Materialization + storage + verification + idempotency
# ---------------------------------------------------------------------------


class TestMaterialization:
    def test_accepted_md_materializes_applyable_intent(self, env):
        from packages.orchestration.approval_queue import APPROVAL_PENDING, get_patch_intent
        from packages.orchestration.patch_apply import _extract_proposed_lines
        job, fid = _job(env)
        r = _intake(job, env, _md_diff(), fid=fid)
        assert r.trust_status == PT.TrustStatus.ACCEPTED
        assert r.material_state == PM.MaterialState.MATERIALIZED
        assert r.repair_intent_id
        reloaded = load_job(UUID(str(job.id)), env)
        intent = get_patch_intent(reloaded, r.repair_intent_id)
        assert intent is not None and intent["state"] == APPROVAL_PENDING
        # The materialized artifact carries the apply-extractable format.
        art = next(a for a in reloaded.artifacts if (a.metadata or {}).get("provider_material_v0"))
        assert _extract_proposed_lines(art.content) == ["new helpful line"]

    def test_source_accepted_but_not_materialized(self, env):
        job, fid = _job(env, related=("src/app.py",))
        text = ("Fix.\n```diff\n--- a/src/app.py\n+++ b/src/app.py\n@@ -1 +1 @@\n-a\n+b\n```\n")
        r = _intake(job, env, text, fid=fid)
        assert r.trust_status == PT.TrustStatus.ACCEPTED
        assert r.material_state == PM.MaterialState.UNSUPPORTED
        assert not r.repair_intent_id  # no intent for unsupported shape

    def test_private_storage_and_hash(self, env):
        job, fid = _job(env)
        r = _intake(job, env, _md_diff(), fid=fid)
        mdir = env / "workspaces" / str(job.id) / "provider_patch_material" / r.material_id
        assert (mdir / "patch.diff").exists()
        assert (mdir / "manifest.sha256").exists()
        assert (mdir / "material.json").exists()
        # Manifest (public-safe) carries no raw diff.
        manifest = json.loads((mdir / "material.json").read_bytes())
        assert "@@" not in json.dumps(manifest)

    def test_verification_passes(self, env):
        job, fid = _job(env)
        r = _intake(job, env, _md_diff(), fid=fid)
        v = PM.verify_provider_patch_material(str(job.id), r.material_id, env)
        assert v.ok, v.checks

    def test_verification_detects_tamper(self, env):
        job, fid = _job(env)
        r = _intake(job, env, _md_diff(), fid=fid)
        patch = env / "workspaces" / str(job.id) / "provider_patch_material" / r.material_id / "patch.diff"
        patch.write_text("tampered")
        v = PM.verify_provider_patch_material(str(job.id), r.material_id, env)
        assert not v.ok and not v.checks["hash_matches"]

    def test_idempotent_same_candidate(self, env):
        job, fid = _job(env)
        r1 = _intake(job, env, _md_diff(), fid=fid)
        r2 = _intake(load_job(UUID(str(job.id)), env), env, _md_diff(), fid=fid)
        assert r1.material_id == r2.material_id
        reloaded = load_job(UUID(str(job.id)), env)
        materials = PM.load_materials(reloaded)
        assert len(materials) == 1  # no duplicate material


# ---------------------------------------------------------------------------
# do_continue apply compatibility (Steps 1342/1361)
# ---------------------------------------------------------------------------


class TestApplyCompatibility:
    def test_approve_then_do_continue_applies(self, env, monkeypatch, tmp_path):
        import packages.orchestration.test_execution_service as tes
        from packages.orchestration import do_continue as dc
        from packages.orchestration.approval_queue import set_approval_state
        from packages.orchestration.permissions import Capability, set_permission
        from packages.orchestration.run_contract import (
            ContractAction,
            build_default_run_contract,
            save_contract,
        )
        from tests.orchestration.test_do_continue import _fake_test

        repo = tmp_path / "repo"; (repo / "docs").mkdir(parents=True)
        (repo / "docs" / "guide.md").write_text("line one\nline two\n")
        t = Task(description="t")
        fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=t.id,
                      metadata={"test_failure": True, "failure_kind": "test_failed",
                                "related_task_id": str(t.id), "related_files": ["docs/guide.md"],
                                "safe_summary": "boom"})
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

        r = _intake(job, env, _md_diff(), fid=str(fa.id))
        assert r.repair_intent_id
        job = load_job(UUID(str(job.id)), env)
        set_approval_state(job, r.repair_intent_id, "approved", decided_by="human")
        save_job(job, root=env)

        fn, _ = _fake_test(env, status="passed")
        monkeypatch.setattr(tes, "execute_test_run", fn)
        res = dc.run_do_continue(dc.ContinueRequest(job_id=str(job.id), intent_id=r.repair_intent_id), env)
        assert res.stop_reason == "completed_verified"
        assert res.snapshot_id  # snapshot mandatory
        assert "new helpful line" in (repo / "docs" / "guide.md").read_text()


# ---------------------------------------------------------------------------
# Redaction (Step 1353)
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_no_raw_leak_across_surfaces(self, env):
        # An accepted candidate cannot carry secrets (trust gate rejects them), but
        # materialization surfaces + the manifest must still expose no raw diff/source.
        job, fid = _job(env)
        r = _intake(job, env, _md_diff(), fid=fid)
        reloaded = load_job(UUID(str(job.id)), env)
        from packages.orchestration.progress_ledger import extract_provider_material_items
        from packages.orchestration.provider_patch_material import get_material, load_materials
        from packages.orchestration.review_bundle import _build_provider_material_summary
        from packages.orchestration.ui_server import _build_provider_trust_section
        items = extract_provider_material_items(load_materials(reloaded))
        blobs = [
            json.dumps(PT.export_intake_result_json(r)),
            json.dumps(get_material(reloaded, r.material_id)),
            json.dumps([{"id": i.item_id, "s": i.safe_summary} for i in items]),
            json.dumps(_build_provider_material_summary(reloaded)),
            json.dumps(_build_provider_trust_section(reloaded)),
        ]
        for b in blobs:
            assert "@@ " not in b           # no raw hunk header
            assert "+++ " not in b
            assert "diff --git" not in b
            assert "/home/" not in b
            assert "Traceback" not in b

    def test_secret_diff_rejected_no_material(self, env):
        job, fid = _job(env)
        text = ("Fix.\n```diff\n--- a/docs/guide.md\n+++ b/docs/guide.md\n@@ -1 +1,2 @@\n a\n"
                '+token = "ghp_abcdefghijklmnopqrstuvwxyz0123"\n```\n')
        r = _intake(job, env, text, fid=fid)
        assert r.trust_status == PT.TrustStatus.REJECTED
        assert not r.repair_intent_id and not r.material_id
        reloaded = load_job(UUID(str(job.id)), env)
        assert PM.load_materials(reloaded) == {}


# ---------------------------------------------------------------------------
# Architecture guards (Step 1355)
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    SRC = Path("packages/orchestration/provider_patch_material.py").read_text()

    def _imports(self):
        return [ln for ln in self.SRC.splitlines()
                if ln.strip().startswith(("import ", "from "))]

    def test_no_network_or_subprocess(self):
        for ln in self._imports():
            for bad in ("subprocess", "socket", "requests", "httpx", "urllib", "http.client"):
                assert bad not in ln
        assert "import subprocess" not in self.SRC
        assert "shell=True" not in self.SRC

    def test_no_provider_sdk(self):
        for ln in self._imports():
            low = ln.lower()
            for bad in ("ollama", "anthropic", "openai", "claude", "litellm"):
                assert bad not in low

    def test_no_apply_or_test_exec_imports(self):
        for ln in self._imports():
            assert "patch_apply" not in ln
            assert "source_apply" not in ln
            assert "test_execution_service" not in ln
            assert "do_continue" not in ln

    def test_accepted_intent_resolvable_and_catalog_backed(self, env):
        from packages.orchestration.approval_queue import get_patch_intent
        from packages.orchestration.do_run import validate_next_safe_action_command
        job, fid = _job(env)
        r = _intake(job, env, _md_diff(), fid=fid)
        reloaded = load_job(UUID(str(job.id)), env)
        assert get_patch_intent(reloaded, r.repair_intent_id) is not None
        assert validate_next_safe_action_command(r.next_safe_action)
