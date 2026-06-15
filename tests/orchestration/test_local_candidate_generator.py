"""Unit + integration tests for Automated Local Candidate Generator v0 (Steps 1628-1635).

The generator is DISABLED by default, loopback-only, routing-gated, and routes ALL output through
quarantine → Trust Gate → Verification → Materialization. It never creates an intent directly,
never approves/applies, never calls the network/subprocess/SDK, and never breaks deterministic flow
when the model is absent. No raw prompt/output/secrets/paths leak. Tests use an injected fake
transport — no real Ollama.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from packages.orchestration.local_candidate_generator import (
    LocalCandidateGenerationRequest, LocalCandidateGenerationStopReason, LocalCandidateStatus,
    load_local_candidate_config, check_local_candidate_availability,
    run_local_candidate_generation, export_local_candidate_result_json,
    list_local_candidate_runs,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

_SAFE_CAND = json.dumps({
    "summary": "Add note", "rationale": "addresses the documentation gap",
    "target_files": ["docs/note.md"],
    "structured_operations": [{"op": "create", "path": "docs/note.md", "content": "hello"}],
})


def _tx(output: str, *, status: int = 200, oversized: bool = False, timeout: bool = False):
    def transport(method, url, body, t):
        if timeout:
            raise TimeoutError("slow")
        if oversized:
            return (200, b"x" * (64 * 1024 + 50))
        return (status, json.dumps({"response": output}).encode())
    return transport


def _make_job(data_dir, *, related=("docs/note.md",), with_pkg=True, failed_repair=True):
    from packages.core.models import Job, Artifact, ArtifactKind, RunState
    from packages.orchestration.storage import save_job
    fa = Artifact(name="tf", content="x", kind=ArtifactKind.VERIFICATION, task_id=None,
                  metadata={"test_failure": True, "related_files": list(related),
                            "test_command": "pytest"})
    meta = {"target_repo": "."}
    if failed_repair:
        meta["repair_attempts_v1"] = {"a1": {"attempt_id": "a1", "failure_artifact_id": str(fa.id),
                                             "status": "tested_failed"}}
    job = Job(id=uuid4(), name="lc", user_prompt="x", state=RunState.RUNNING,
              artifacts=[fa], metadata=meta)
    if with_pkg:
        job.metadata["repair_request_packages_v0"] = {
            "rp1": {"request_package_id": "rp1", "job_id": str(job.id),
                    "failure_artifact_id": str(fa.id), "target_kind": "docs",
                    "sections": [{"title": "Goal", "body": "fix docs", "files": ["docs/note.md"]}]}}
    save_job(job, root=data_dir)
    return str(job.id), str(fa.id)


@pytest.fixture()
def env(tmp_path, monkeypatch):
    d = tmp_path / "data"
    d.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(d))
    rv = tmp_path / "review.md"
    rv.write_text("## Verdict\nPASS\n")
    monkeypatch.setenv("REMEDY_REVIEW_FILE", str(rv))
    # advisor disabled so routing doesn't divert to local_advisor
    for k in ("REMEDY_LOCAL_ADVISOR_ENABLED", "REMEDY_LOCAL_ADVISOR_ENDPOINT",
              "REMEDY_LOCAL_ADVISOR_MODEL"):
        monkeypatch.delenv(k, raising=False)
    return d


def _enable(monkeypatch, *, endpoint="http://127.0.0.1:11434", model="qwen"):
    monkeypatch.setenv("REMEDY_LOCAL_CANDIDATE_GENERATOR_ENABLED", "1")
    monkeypatch.setenv("REMEDY_LOCAL_CANDIDATE_GENERATOR_ENDPOINT", endpoint)
    monkeypatch.setenv("REMEDY_LOCAL_CANDIDATE_GENERATOR_MODEL", model)


def _req(jid, fid="", **kw):
    return LocalCandidateGenerationRequest(
        request_package_id=kw.pop("request_package_id", "rp1"), job_id=jid,
        failure_artifact_id=fid, **kw)


# ---------------------------------------------------------------------------
# Step 1611 / 1629 — config + endpoint safety
# ---------------------------------------------------------------------------


class TestConfigEndpointSafety:
    def test_disabled_by_default(self, env):
        assert load_local_candidate_config().enabled is False
        a = check_local_candidate_availability()
        assert a["available"] is False
        assert a["stop_reason"] == LocalCandidateGenerationStopReason.DISABLED

    def test_external_endpoint_rejected(self, env, monkeypatch):
        _enable(monkeypatch, endpoint="http://evil.example.com:11434")
        a = check_local_candidate_availability()
        assert a["available"] is False
        assert a["endpoint_label"] == "blocked:non-loopback"
        assert "evil.example.com" not in json.dumps(a)

    def test_file_scheme_rejected(self, env, monkeypatch):
        _enable(monkeypatch, endpoint="file:///etc/passwd")
        a = check_local_candidate_availability()
        assert a["available"] is False

    def test_localhost_accepted(self, env, monkeypatch):
        _enable(monkeypatch, endpoint="http://localhost:11434")
        a = check_local_candidate_availability(transport=_tx(_SAFE_CAND))
        assert a["available"] is True

    def test_timeout_safe(self, env, monkeypatch):
        _enable(monkeypatch)
        jid, fid = _make_job(env)
        res = run_local_candidate_generation(_req(jid, fid), data_dir=env, transport=_tx("", timeout=True))
        assert res.status == LocalCandidateStatus.UNAVAILABLE
        assert res.stop_reason == LocalCandidateGenerationStopReason.TIMEOUT

    def test_oversized_safe(self, env, monkeypatch):
        _enable(monkeypatch)
        jid, fid = _make_job(env)
        res = run_local_candidate_generation(_req(jid, fid), data_dir=env, transport=_tx("", oversized=True))
        assert res.status == LocalCandidateStatus.UNAVAILABLE
        assert res.stop_reason == LocalCandidateGenerationStopReason.OVERSIZED

    def test_model_missing_safe(self, env, monkeypatch):
        _enable(monkeypatch)
        jid, fid = _make_job(env)
        res = run_local_candidate_generation(_req(jid, fid), data_dir=env, transport=_tx("", status=404))
        assert res.status == LocalCandidateStatus.UNAVAILABLE
        assert res.stop_reason == LocalCandidateGenerationStopReason.MODEL_MISSING

    def test_disabled_generate_safe_noop(self, env):
        jid, fid = _make_job(env)
        res = run_local_candidate_generation(_req(jid, fid), data_dir=env, transport=_tx(_SAFE_CAND))
        assert res.status == LocalCandidateStatus.DISABLED


# ---------------------------------------------------------------------------
# Step 1617 — routing gate
# ---------------------------------------------------------------------------


class TestRoutingGate:
    def test_no_request_package_blocks(self, env, monkeypatch):
        _enable(monkeypatch)
        jid, fid = _make_job(env, with_pkg=False)
        res = run_local_candidate_generation(
            LocalCandidateGenerationRequest(request_package_id="missing", job_id=jid, failure_artifact_id=fid),
            data_dir=env, transport=_tx(_SAFE_CAND))
        assert res.status == LocalCandidateStatus.BLOCKED
        assert res.stop_reason == LocalCandidateGenerationStopReason.NO_REQUEST_PACKAGE

    def test_routing_not_selected_blocks(self, env, monkeypatch):
        # No failure/no failed-repair → deterministic route dominates → routing won't pick local gen.
        _enable(monkeypatch)
        jid, fid = _make_job(env, failed_repair=False)
        res = run_local_candidate_generation(_req(jid, fid), data_dir=env, transport=_tx(_SAFE_CAND))
        assert res.status == LocalCandidateStatus.BLOCKED
        assert res.stop_reason == LocalCandidateGenerationStopReason.ROUTING_NOT_SELECTED


# ---------------------------------------------------------------------------
# Step 1630 — trust pipeline
# ---------------------------------------------------------------------------


class TestTrustPipeline:
    def test_safe_output_to_pending_intent(self, env, monkeypatch):
        _enable(monkeypatch)
        jid, fid = _make_job(env)
        res = run_local_candidate_generation(_req(jid, fid), data_dir=env, transport=_tx(_SAFE_CAND))
        assert res.status == LocalCandidateStatus.INTENT_PENDING_APPROVAL
        assert res.linkage.quarantine_id and res.linkage.trust_report_id
        assert res.linkage.verification_id and res.linkage.intent_id
        assert res.next_safe_action == f"remedy patch approve {jid} {res.linkage.intent_id} --json"

    def test_secret_output_trust_rejected_no_echo(self, env, monkeypatch):
        _enable(monkeypatch)
        jid, fid = _make_job(env)
        bad = ("Fix.\n```diff\n--- a/docs/note.md\n+++ b/docs/note.md\n@@ -1 +1,2 @@\n a\n"
               '+token = "ghp_abcdefghijklmnopqrstuvwxyz0123"\n```\n')
        res = run_local_candidate_generation(_req(jid, fid), data_dir=env, transport=_tx(bad))
        assert not res.linkage.intent_id
        assert res.status in (LocalCandidateStatus.TRUST_REJECTED, LocalCandidateStatus.NEEDS_REVIEW,
                              LocalCandidateStatus.VERIFICATION_REJECTED)
        assert "ghp_" not in json.dumps(export_local_candidate_result_json(res))

    def test_overclaim_output_no_intent(self, env, monkeypatch):
        _enable(monkeypatch)
        jid, fid = _make_job(env)
        bad = json.dumps({
            "summary": "Add note", "rationale": "I applied this and all tests passed",
            "target_files": ["docs/note.md"],
            "structured_operations": [{"op": "create", "path": "docs/note.md", "content": "hi"}]})
        res = run_local_candidate_generation(_req(jid, fid), data_dir=env, transport=_tx(bad))
        assert not res.linkage.intent_id
        assert res.status in (LocalCandidateStatus.NEEDS_REVIEW, LocalCandidateStatus.VERIFICATION_REJECTED)
        assert "all tests passed" not in json.dumps(export_local_candidate_result_json(res))


# ---------------------------------------------------------------------------
# Step 1628 — idempotency
# ---------------------------------------------------------------------------


class TestIdempotency:
    def test_reuse_unless_new(self, env, monkeypatch):
        _enable(monkeypatch)
        jid, fid = _make_job(env)
        r1 = run_local_candidate_generation(_req(jid, fid), data_dir=env, transport=_tx(_SAFE_CAND))
        r2 = run_local_candidate_generation(_req(jid, fid), data_dir=env, transport=_tx(_SAFE_CAND))
        assert r2.status == LocalCandidateStatus.REUSED or r2.generation_id == r1.generation_id

    def test_pending_intent_blocks_new(self, env, monkeypatch):
        _enable(monkeypatch)
        jid, fid = _make_job(env)
        run_local_candidate_generation(_req(jid, fid), data_dir=env, transport=_tx(_SAFE_CAND))
        # A pending intent now exists → a forced-new generation is blocked.
        res = run_local_candidate_generation(_req(jid, fid, new=True), data_dir=env, transport=_tx(_SAFE_CAND))
        assert res.status == LocalCandidateStatus.BLOCKED
        assert res.stop_reason == LocalCandidateGenerationStopReason.PENDING_INTENT


# ---------------------------------------------------------------------------
# Step 1632 — redaction
# ---------------------------------------------------------------------------


class TestRedaction:
    def test_no_raw_in_result_or_manifest(self, env, monkeypatch):
        _enable(monkeypatch)
        jid, fid = _make_job(env)
        secretish = json.dumps({
            "summary": "x", "rationale": "/home/u/.ssh/id_rsa Traceback (most recent call last):",
            "target_files": ["docs/note.md"],
            "structured_operations": [{"op": "create", "path": "docs/note.md", "content": "hi"}]})
        res = run_local_candidate_generation(_req(jid, fid), data_dir=env, transport=_tx(secretish))
        blob = json.dumps(export_local_candidate_result_json(res))
        for bad in ("/home/u/.ssh/id_rsa", "Traceback"):
            assert bad not in blob
        # Run manifest (public-ish) carries hashes/counts only — no raw.
        for r in list_local_candidate_runs(env):
            mblob = json.dumps(r)
            assert "/home/u/.ssh/id_rsa" not in mblob and "Traceback" not in mblob


# ---------------------------------------------------------------------------
# Step 1633 — architecture guards
# ---------------------------------------------------------------------------


class TestArchitectureGuards:
    def _code(self):
        import re
        src = Path("packages/orchestration/local_candidate_generator.py").read_text()
        # Remove all triple-quoted spans (module + function docstrings, incl. inline-closing)
        # and full-line comments, so prose can't false-positive the guards.
        src = re.sub(r'"""[\s\S]*?"""', "", src)
        return "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))

    def test_no_forbidden_imports(self):
        code = self._code()
        for bad in ("import requests", "import httpx", "import openai", "import anthropic",
                    "import subprocess", "shell=True", "selenium", "playwright"):
            assert bad not in code, f"forbidden token: {bad}"

    def test_no_apply_or_approval(self):
        code = self._code()
        for bad in ("source_apply", "patch_apply", "apply_patch", "approve_intent",
                    "create_pr", "git commit", "git push", "add_patch_intent",
                    "add_proposed_task", ".tasks.append"):
            assert bad not in code, f"forbidden execution token: {bad}"

    def test_export_has_no_raw_fields(self):
        from packages.orchestration.local_candidate_generator import LocalCandidateGenerationResult
        d = export_local_candidate_result_json(LocalCandidateGenerationResult(generation_id="g", job_id="j"))
        for forbidden in ("prompt_text", "raw", "output_text", "diff", "source", "stdout", "stderr"):
            assert forbidden not in d

    def test_goes_through_intake(self):
        # The module must route output through intake_provider_repair (trust+verification), not
        # construct intents directly.
        code = self._code()
        assert "intake_provider_repair" in code
        assert "materialize_accepted_candidate" not in code  # never bypasses intake to materialize
