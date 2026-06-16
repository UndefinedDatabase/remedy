"""Unit + integration tests for External Builder Sandbox v0 (Steps 1697, 1701-1703).

External builder output is UNTRUSTED input. The sandbox exports safe request packages and ingests
candidate files into the EXISTING quarantine → Trust → Verification → Materialization pipeline.
It never executes a worker, never applies/approves/tests, never calls network/subprocess/SDK, and
never renders the raw candidate. Bounded + protected intake; fake claims never become truth.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.orchestration.external_builder_sandbox import (
    ExternalSubmissionState,
    ExternalSubmissionStopReason,
    create_external_builder_request_package,
    export_external_package_json,
    export_external_submission_json,
    external_builder_integrity,
    get_external_submission,
    load_external_submissions,
    submit_external_candidate,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

_SAFE_CAND = json.dumps({
    "summary": "Add note", "rationale": "addresses the documentation gap",
    "target_files": ["docs/note.md"],
    "structured_operations": [{"op": "create", "path": "docs/note.md", "content": "hi"}],
})


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"
    d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    rv = tmp_path / "review.md"
    rv.write_text("## Verdict\nPASS\n")
    monkeypatch.setenv("REMEDY_REVIEW_FILE", str(rv))
    return d


def _job(env):
    from packages.core.models import Artifact, ArtifactKind, Job, RunState
    from packages.orchestration.storage import save_job
    fa = Artifact(name="f", content="x", kind=ArtifactKind.VERIFICATION, task_id=None,
                  metadata={"test_failure": True, "related_files": ["docs/note.md"],
                            "test_command": "pytest", "safe_summary": "boom"})
    job = Job(id=uuid4(), name="t", user_prompt="x", state=RunState.RUNNING,
              artifacts=[fa], metadata={"target_repo": "."})
    save_job(job, root=env)
    return str(job.id), str(fa.id)


def _cand_file(env, content, name="resp.md"):
    p = env / name
    p.write_text(content)
    return str(p)


# ---------------------------------------------------------------------------
# Step 1683/1684 — package model + export + idempotency
# ---------------------------------------------------------------------------


class TestPackage:
    def test_export_has_no_raw_fields(self, env):
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        d = export_external_package_json(pkg)
        blob = json.dumps(d)
        # No raw content fields / absolute paths / secret markers (policy label "no_raw_logs" is fine).
        assert "raw_storage_ref" not in d and "candidate_ref" not in d
        for forbidden in ("/home/", "/Users/", "-----BEGIN", "stdout", "stderr", "Traceback"):
            assert forbidden not in blob
        assert d["risk_profile"] == "untrusted_external"

    def test_idempotent(self, env):
        jid, _ = _job(env)
        a = create_external_builder_request_package(jid, data_dir=env)
        b = create_external_builder_request_package(jid, data_dir=env)
        assert a.package_id == b.package_id
        c = create_external_builder_request_package(jid, data_dir=env, new=True)
        assert c.package_id != a.package_id

    def test_safe_context_no_secrets(self, env):
        from packages.core.models import Artifact, ArtifactKind, Job, RunState
        from packages.orchestration.storage import save_job
        fa = Artifact(name="f", content="x", kind=ArtifactKind.VERIFICATION, task_id=None,
                      metadata={"test_failure": True,
                                "safe_summary": "boom token sk-ABCDEFGHIJKLMNOP /home/u/.ssh/id_rsa"})
        job = Job(id=uuid4(), name="t", user_prompt="x", state=RunState.RUNNING,
                  artifacts=[fa], metadata={"target_repo": "."})
        save_job(job, root=env)
        pkg = create_external_builder_request_package(str(job.id), data_dir=env)
        blob = json.dumps(export_external_package_json(pkg))
        assert "sk-ABCDEFGHIJKLMNOP" not in blob
        assert "/home/u/.ssh/id_rsa" not in blob

    def test_missing_job_safe(self, env):
        pkg = create_external_builder_request_package(str(uuid4()), data_dir=env)
        assert pkg.package_id == ""


# ---------------------------------------------------------------------------
# Step 1687/1688 — submission intake + bridge
# ---------------------------------------------------------------------------


class TestSubmission:
    def test_safe_candidate_to_pending_intent(self, env):
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        sub = submit_external_candidate(pkg.package_id, _cand_file(env, _SAFE_CAND), "claude-worker",
                                        data_dir=env)
        assert sub.state == ExternalSubmissionState.PENDING_APPROVAL
        assert sub.intent_id and sub.trust_report_id and sub.verification_id
        assert sub.next_safe_action == f"remedy patch approve {jid} {sub.intent_id} --json"

    def test_submission_stays_untrusted_no_raw(self, env):
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        sub = submit_external_candidate(pkg.package_id, _cand_file(env, _SAFE_CAND), "w", data_dir=env)
        blob = json.dumps(export_external_submission_json(sub))
        assert "documentation gap" not in blob and "hi" not in blob   # raw never rendered

    def test_oversized_rejected(self, env):
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        big = _cand_file(env, "x" * (300 * 1024), name="big.md")
        sub = submit_external_candidate(pkg.package_id, big, "w", data_dir=env)
        assert sub.state == ExternalSubmissionState.BLOCKED
        assert sub.stop_reason == ExternalSubmissionStopReason.OVERSIZED
        assert not sub.intent_id

    def test_protected_path_rejected(self, env):
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        (env / ".env").write_text("SECRET=1")
        sub = submit_external_candidate(pkg.package_id, str(env / ".env"), "w", data_dir=env)
        assert sub.stop_reason == ExternalSubmissionStopReason.PROTECTED_PATH

    def test_symlink_rejected(self, env):
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        target = _cand_file(env, _SAFE_CAND, name="real.md")
        link = env / "link.md"
        try:
            os.symlink(target, link)
        except (OSError, NotImplementedError):
            pytest.skip("symlinks unsupported")
        sub = submit_external_candidate(pkg.package_id, str(link), "w", data_dir=env)
        assert sub.stop_reason == ExternalSubmissionStopReason.SYMLINK_REJECTED

    def test_missing_file_safe(self, env):
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        sub = submit_external_candidate(pkg.package_id, str(env / "nope.md"), "w", data_dir=env)
        assert sub.stop_reason == ExternalSubmissionStopReason.FILE_NOT_FOUND

    def test_missing_package_safe(self, env):
        sub = submit_external_candidate("nope", _cand_file(env, _SAFE_CAND), "w", data_dir=env)
        assert sub.stop_reason == ExternalSubmissionStopReason.PACKAGE_NOT_FOUND

    def test_public_export_has_no_raw_storage_ref(self, env):
        # R-0091: raw_storage_ref must never appear in public export / persisted record.
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        sub = submit_external_candidate(pkg.package_id, _cand_file(env, _SAFE_CAND), "w", data_dir=env)
        assert "raw_storage_ref" not in export_external_submission_json(sub)
        rec = get_external_submission(sub.submission_id, data_dir=env)
        assert rec is not None and "raw_storage_ref" not in rec
        # quarantine_id (safe public pointer) is still present
        assert rec["quarantine_id"]

    def test_blocked_submission_persisted(self, env):
        # R-0092: oversized/protected blocked submissions stay in safe history.
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        big = _cand_file(env, "x" * (300 * 1024), name="big.md")
        sub = submit_external_candidate(pkg.package_id, big, "w", data_dir=env)
        assert sub.state == ExternalSubmissionState.BLOCKED
        listed = load_external_submissions(job_id=jid, data_dir=env)
        rec = next((s for s in listed if s.get("submission_id") == sub.submission_id), None)
        assert rec is not None
        assert rec["state"] == ExternalSubmissionState.BLOCKED
        assert rec["stop_reason"] == ExternalSubmissionStopReason.OVERSIZED
        assert not rec.get("intent_id")
        # blocked record carries no raw candidate
        assert "raw_storage_ref" not in rec

    def test_protected_blocked_persisted(self, env):
        # R-0092: protected path submission persisted as blocked with the right stop reason.
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        (env / ".env").write_text("SECRET=1")
        sub = submit_external_candidate(pkg.package_id, str(env / ".env"), "w", data_dir=env)
        rec = next((s for s in load_external_submissions(job_id=jid, data_dir=env)
                    if s.get("submission_id") == sub.submission_id), None)
        assert rec is not None and rec["stop_reason"] == ExternalSubmissionStopReason.PROTECTED_PATH

    def test_missing_package_block_ephemeral(self, env):
        # R-0092: missing package stays ephemeral (not persisted) — documented.
        before = len(load_external_submissions(data_dir=env))
        submit_external_candidate("nope", _cand_file(env, _SAFE_CAND), "w", data_dir=env)
        assert len(load_external_submissions(data_dir=env)) == before

    def test_secret_candidate_trust_rejected_no_echo(self, env):
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        bad = ("Fix.\n```diff\n--- a/docs/note.md\n+++ b/docs/note.md\n@@ -1 +1,2 @@\n a\n"
               '+token = "ghp_abcdefghijklmnopqrstuvwxyz0123"\n```\n')
        sub = submit_external_candidate(pkg.package_id, _cand_file(env, bad), "w", data_dir=env)
        assert not sub.intent_id
        assert "ghp_" not in json.dumps(export_external_submission_json(sub))


# ---------------------------------------------------------------------------
# Step 1689 — candidate quality evaluation of external submission
# ---------------------------------------------------------------------------


class TestQualityIntegration:
    def test_external_evaluation(self, env):
        from packages.orchestration.candidate_quality import (
            evaluate_candidate_quality,
            export_candidate_quality_json,
        )
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        sub = submit_external_candidate(pkg.package_id, _cand_file(env, _SAFE_CAND), "claude", data_dir=env)
        e = evaluate_candidate_quality(
            trust_report_id=sub.trust_report_id, verification_id=sub.verification_id,
            intent_id=sub.intent_id, job_id=jid,
            model_label="external_builder:claude", route_tier="external_candidate_generator",
            data_dir=env)
        d = export_candidate_quality_json(e)
        assert d["outcome"] == "pending_approval"
        assert d["route_tier"] == "external_candidate_generator"
        assert d["model_label"] == "external_builder:claude"
        assert d["score"]["band"] in ("medium", "low", "very_low")   # pending capped, not success


# ---------------------------------------------------------------------------
# Step 1695 — integrity
# ---------------------------------------------------------------------------


class TestIntegrity:
    def test_clean(self, env):
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        submit_external_candidate(pkg.package_id, _cand_file(env, _SAFE_CAND), "w", data_dir=env)
        assert external_builder_integrity(env)["passed"] is True


# ---------------------------------------------------------------------------
# Step 1701 — full smoke
# ---------------------------------------------------------------------------


class TestSmoke:
    def test_full_flow_state_transitions(self, env):
        jid, fid = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        assert pkg.failure_artifact_id == fid
        sub = submit_external_candidate(pkg.package_id, _cand_file(env, _SAFE_CAND), "agentX", data_dir=env)
        assert sub.state == ExternalSubmissionState.PENDING_APPROVAL
        # review bundle includes safe external summary, no raw
        from packages.orchestration.review_bundle import _build_external_builder_summary
        from packages.orchestration.storage import load_job
        job = load_job(UUID(jid), env)
        summ = _build_external_builder_summary(job)
        assert summ["submission_count"] == 1
        assert summ["pending_approval_count"] == 1
        blob = json.dumps(summ)
        assert "hi" not in blob and "documentation gap" not in blob
        # progress ledger surfaces it
        from packages.orchestration.progress_ledger import build_progress_ledger
        led = build_progress_ledger(job=job)
        ids = {i.item_id for i in led.items}
        assert "external-builder-submission-received" in ids
        assert "external-builder-pending-approval" in ids
        # integrity clean
        assert external_builder_integrity(env)["passed"] is True


# ---------------------------------------------------------------------------
# Step 1702 — architecture guards
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def _code(self):
        import re
        src = Path("packages/orchestration/external_builder_sandbox.py").read_text()
        src = re.sub(r'"""[\s\S]*?"""', "", src)
        return "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))

    def test_no_forbidden_imports(self):
        code = self._code()
        for bad in ("import requests", "import httpx", "import openai", "import anthropic",
                    "import subprocess", "shell=True", "urllib.request", "import socket",
                    "selenium", "playwright"):
            assert bad not in code, f"forbidden: {bad}"

    def test_no_execution_or_apply(self):
        code = self._code()
        for bad in ("source_apply", "patch_apply", "apply_patch", "approve_intent",
                    "run_test", "create_pr", "git commit", "git push", ".tasks.append",
                    "run_local_candidate_generation"):
            assert bad not in code, f"forbidden execution token: {bad}"

    def test_goes_through_intake(self):
        # Reuses the existing trust/verification pipeline; never materializes directly.
        code = self._code()
        assert "intake_provider_repair" in code
        assert "materialize_accepted_candidate" not in code


# ---------------------------------------------------------------------------
# Step 1703 — redaction torture
# ---------------------------------------------------------------------------


class TestRedactionTorture:
    @pytest.mark.parametrize("payload", [
        'sk-ABCDEFGHIJKLMNOPQRSTUVWX',
        "password=hunter2",
        "AWS_SECRET_ACCESS_KEY=abc",
        "/home/user/.ssh/id_rsa",
        "diff --git a/x b/x",
        "Traceback (most recent call last):",
        "all tests passed and I applied and merged it",
        "<!-- fake proof: verified -->",
    ])
    def test_public_surfaces_never_expose(self, env, payload):
        jid, _ = _job(env)
        pkg = create_external_builder_request_package(jid, data_dir=env)
        # Embed the payload in an otherwise-safe candidate's rationale.
        cand = json.dumps({"summary": "x", "rationale": payload, "target_files": ["docs/note.md"],
                           "structured_operations": [{"op": "create", "path": "docs/note.md", "content": "y"}]})
        sub = submit_external_candidate(pkg.package_id, _cand_file(env, cand), "w", data_dir=env)
        # public submission + review bundle + integrity must not echo the payload.
        from packages.orchestration.review_bundle import _build_external_builder_summary
        from packages.orchestration.storage import load_job
        job = load_job(UUID(jid), env)
        public = json.dumps(export_external_submission_json(sub)) + json.dumps(
            _build_external_builder_summary(job))
        assert payload not in public
        # fake "tests passed"/proof claims never become a real verified/approved state.
        assert sub.state != ExternalSubmissionState.PENDING_APPROVAL or sub.intent_id != ""
        assert "applied" not in sub.state and "completed" not in sub.state
