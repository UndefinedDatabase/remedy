"""F9 (round 21) — ONE real authoritative end-to-end package test.

committed Subject → strict ContentProof → Final-Verifier/Change-Provenance authority → Evidence
staging → build_review_manifest → ArchivePlan → Expectation → Root Manifest → real
make_review_zip.sh → READY_FOR_REVIEW ZIP → ZIP-only hash-chain verification.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

_REQUIRED_SCRIPTS = ("make_review_zip.sh", "build_review_manifest.py", "build_review_zip.py",
                     "build_observability_index.py", "select_review_evidence.py",
                     "stage_review_evidence.py")
_REQUIRED_MODULES = (
    "packages/orchestration/__init__.py", "packages/orchestration/data_paths.py",
    "packages/orchestration/evidence_index.py", "packages/orchestration/review_zip.py",
    "packages/orchestration/archive_plan.py", "packages/orchestration/review_subject.py",
    "packages/orchestration/evidence_inventory.py", "packages/common/__init__.py",
    "packages/common/secure_fs.py", "packages/common/strict_json.py",
)


#: The exact CORE_ARTIFACTS required-artifact key set (round 25 artifact-contract completeness).
_CORE_ARTIFACTS = ("manifest.json", "job_report.json", "token_truth.json",
                   "fresh_evidence_gate.json", "artifact_contract_gate.json",
                   "runtime_integration_gate.json", "change_provenance_gate.json",
                   "commit_execution_gate.json", "final_verifier_report.json")


def _na_section(kind):
    if kind == "stream":
        return {"applicable": False, "verdict": "NOT_APPLICABLE",
                "tasks_with_stream_evidence": [], "artifacts_verified": 0, "artifacts_present": 0,
                "missing_stream_artifact_listing": [], "missing_stream_artifacts": [],
                "missing_stream_artifact_metadata": [], "stream_artifact_hash_mismatches": [],
                "stream_artifact_size_mismatches": [], "unexpected_stream_artifacts": [],
                "duplicate_stream_artifact_refs": [], "unsafe_stream_artifact_refs": []}
    return {"applicable": False, "verdict": "NOT_APPLICABLE", "job_level_handoff": False,
            "handoff_coverage_verdict": "", "handoff_coverage_issues": [], "missing_job_handoff": [],
            "worktree_tasks": [], "diffs_verified": 0, "missing_result_diffs": [],
            "missing_result_diff_references": [], "result_diff_hash_mismatches": [],
            "result_diff_size_mismatches": [], "unreferenced_result_diffs": [],
            "unsafe_result_diff_refs": []}


def _models(actual_null=True):
    return {"builder": None, "reviewer": None} if actual_null else {"builder": "", "reviewer": ""}


def _token_status():
    return {"actual_available": False, "actual_call_count": 0, "actual_completion_tokens": None,
            "actual_coverage_complete": False, "actual_missing_reasons": None,
            "actual_model_verified": False, "actual_models": _models(True),
            "actual_prompt_tokens": None, "actual_total_tokens": None, "builder_estimated_total": 0,
            "cli_version": None, "configured_models": _models(False), "cost_call_count": 0,
            "cost_coverage_complete": False, "cost_coverage_reason": "no_real_provider_calls",
            "estimated_completion_tokens": 0, "estimated_prompt_tokens": 0,
            "estimated_total_tokens": 0, "measurement_confidence": "low",
            "measurement_source": "character_heuristic", "missing_reason": "operator attested",
            "prompt_trace_count": 0, "provider_call_count": 0, "repair_estimated_total": 0,
            "reviewer_estimated_total": 0, "total_cost_usd": None}


def _token_measurement():
    return {"actual_call_count": 0, "actual_coverage_complete": False, "actual_missing_reasons": None,
            "actual_model_verified": False, "actual_models": _models(True), "actual_summary": None,
            "cli_version": None, "configured_models": _models(False), "cost_call_count": 0,
            "cost_coverage_complete": False, "cost_coverage_reason": "no_real_provider_calls",
            "measurement_confidence": "low", "measurement_note": "operator attested",
            "measurement_source": "character_heuristic", "provider_call_count": 0,
            "total_cost_usd": None}


def _complete_gates(authority=None, file_hashes=None, job_id="e2e-job-01", step="1-2"):
    """The complete, closed-schema, semantically-consistent READY gate set (round 25) keyed by
    filename: every field required by the exact RECURSIVE validators and the COMPLETE semantics is
    present and coherent. ``file_hashes`` (path->sha) binds change-provenance hash maps to the
    packaged ContentProof; when omitted a placeholder is used for gate-matrix-only unit tests."""
    authority = sorted(authority or ["src/app.py", "tests_pkg/test_app.py"])
    hashes = dict(file_hashes) if file_hashes is not None else {p: "0" * 64 for p in authority}
    covered = sorted(hashes) if file_hashes is not None else authority
    return {
        # round 26: the COMPLETE final_verifier producer shape — every required field present and
        # fully typed (token_status/token_measurement complete, no ANY).
        "final_verifier_report.json": {
            "schema_version": "1.0.0", "verdict": "PASS_WITH_RISKS",
            "authoritative_changed_files": authority, "changed_files": authority,
            "changed_line_ranges": {}, "also_needs_repair": False,
            "unresolved_findings": [], "test_status": {"ran": True, "passed": 1, "failed": 0},
            "missing_tests_gate": "PASS", "change_source_mismatches": [],
            "review_subject_uncovered_files": [], "content_hash_mismatches": [],
            "postmortem_failures": [], "postmortem_integrity_blocked": False,
            "manifest_integrity_blocked": False,
            "final_job_review_blocked": False, "execution_mode_blocked": False,
            "model_mismatch_blocked": False, "model_needs_repair": False, "missing_evidence": [],
            "execution_mode_findings": [], "final_job_review_findings": [],
            "invocation_args_warnings": [], "model_mismatch_warnings": [],
            "sticky_binding_warnings": [], "report_badges": [], "operator_attested_tasks": [],
            "execution_mode_by_task": {}, "sticky_binding_by_task": {},
            "final_job_review_verdict": "PASS", "recommended_action": "Approve with risks",
            "manual_completion": True, "human_final_reviewer_required": True,
            "artifact_contract_gate": "PASS", "change_provenance_gate": "PASS",
            "fresh_evidence_gate": "PASS", "runtime_integration_gate": "PASS",
            "commit_execution_gate": "BLOCKED",
            "spec_compliance": "PASS", "scratch_file_guard": "PASS", "change_provenance": "PASS",
            "file_set_alignment_status": "PASS", "token_cost_has_critical": False,
            "token_cost_policy_present": True, "token_cost_risk_findings": [],
            "token_status": _token_status(), "token_measurement": _token_measurement(),
            "token_measurement_confidence": "low", "token_measurement_note": "operator attested",
            "token_actual_summary": None,
            "evidence_completeness": {"review_scope_packet": True, "spec_compliance_check": True,
                                      "missing_tests_gate": True, "scratch_file_guard": True,
                                      "token_truth": True, "safe_diff": True, "review_json": True,
                                      "tests_txt": True}},
        "fresh_evidence_gate.json": {
            "schema_version": "1.0.0", "verdict": "PASS", "evidence_authoritative": True,
            "job_id_match": True, "plan_match": True, "live_review_match": True,
            "evidence_job_id": job_id, "current_job_id": job_id,
            "current_step_range": step, "live_review_step_range": step, "plan_step_range": step,
            "evidence_freshness": {"is_fresh": True, "job_id_match": True,
                                   "step_range_match": True},
            "evidence_validity": {"has_job_id": True, "has_manifest": True,
                                  "is_valid_current_run": True}, "issues": []},
        "artifact_contract_gate.json": {
            "schema_version": "1.0.0", "verdict": "PASS", "missing_required": [],
            "fv_referenced_missing": [], "critical_fv_missing": [], "issues": [],
            "job_id_fresh": True, "evidence_job_id": job_id,
            "required_artifacts": {a: True for a in _CORE_ARTIFACTS},
            "optional_artifacts": {"scratch_file_guard.json": True},
            "stream_artifacts": _na_section("stream"), "worktree_artifacts": _na_section("worktree")},
        "change_provenance_gate.json": {
            "schema_version": "1.0.0", "verdict": "PASS", "current_job_id": job_id,
            "covered_files": covered, "source_files": covered, "excluded_files": [],
            "evidence_covered_files": covered, "evidence_sources": [], "dirty_files": [],
            "uncovered_files": [], "content_hash_verified": True, "hash_mismatches": [],
            "stale_apply_proofs": [], "issues": [], "current_hashes": hashes,
            "evidence_hashes": hashes},
        "runtime_integration_gate.json": {
            "schema_version": "1.0.0", "verdict": "PASS",
            "checks": [{"check_id": f"c{i}", "check_type": "call_exists",
                        "source_file": "src/app.py", "pattern": "add(", "found": True,
                        "file_missing": False} for i in range(3)],
            "checks_total": 3, "checks_passed": 3, "issues": []},
        "manifest_integrity.json": {"schema_version": "1.0.0", "ok": True, "failures": [],
                                    "notes": []},
        "postmortem_integrity.json": {"schema_version": "1.0.0", "ok": True, "failures": []},
        "commit_execution_gate.json": {
            "schema_version": "1.0.0", "verdict": "NEEDS_HUMAN_APPROVAL", "promote_ready": False,
            "blocked_gates": [], "non_pass_gates": ["final_verifier"],
            "issues": ["gate 'final_verifier' is not PASS (verdict 'PASS_WITH_RISKS')"],
            "gate_checks": {"final_verifier": "PASS_WITH_RISKS", "fresh_evidence_gate": "PASS",
                            "artifact_contract_gate": "PASS", "change_provenance_gate": "PASS",
                            "runtime_integration_gate": "PASS"}},
    }


def _run(cmd, cwd, env=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=180,
                          env={**os.environ, **(env or {})})


def _git(repo, *args, env=None):
    e = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
         "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t", **(env or {})}
    return _run(["git", *args], repo, e)


def _build_repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    for name in _REQUIRED_SCRIPTS:
        shutil.copy2(REPO_ROOT / "scripts" / name, repo / "scripts" / name)
    # The full package tree is resolved from the real repo via PYTHONPATH (see _run), so the
    # temp repo carries only scripts + the reviewed source — no partial `packages/` to shadow it.
    _git(repo, "init", "-q")
    (repo / "README.md").write_text("# base\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    base = _git(repo, "rev-parse", "HEAD").stdout.strip()
    # feature commit: one source + one test file
    (repo / "src").mkdir()
    (repo / "src" / "app.py").write_text("def add(a, b):\n    return a + b\n")
    (repo / "tests_pkg").mkdir()
    (repo / "tests_pkg" / "test_app.py").write_text("def test_add():\n    assert True\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "feature")
    head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    return repo, base, head


def _write_evidence(repo, base, head, ev):
    """Build a faithful evidence dir (OUTSIDE the git repo so it never pollutes the dirty set):
    real resolved Subject + aligned strict Proof + gates."""
    import sys
    sys.path.insert(0, str(REPO_ROOT))
    from packages.orchestration.repair_attest import is_attestable_source
    from packages.orchestration.review_subject import resolve_review_subject

    subject = resolve_review_subject(str(repo), base)
    authority = sorted({f.path for f in subject.files if is_attestable_source(f.path)})

    (ev / "task_runs" / "t1").mkdir(parents=True)
    (ev / "review_subject.json").write_text(json.dumps(subject.to_json(), indent=2, sort_keys=True))
    file_hashes = {p: hashlib.sha256((repo / p).read_bytes()).hexdigest() for p in authority}
    (ev / "current_change_content_proof.json").write_text(json.dumps({
        "schema_version": "1.1.0", "base_commit": base, "head_commit": head,
        "file_hashes": file_hashes, "file_count": len(file_hashes),
        "tombstones": {}, "tombstone_count": 0}, indent=2, sort_keys=True))
    (ev / "review_commit_chain.json").write_text(json.dumps({
        "chain_v": 1, "base_commit": base, "head_commit": head, "commits": []}, sort_keys=True))
    # F1/F2 (round 23-25): the complete READY gate matrix, semantically consistent, with the
    # change-provenance hash maps bound to the packaged ContentProof file hashes.
    for name, body in _complete_gates(authority, file_hashes).items():
        (ev / name).write_text(json.dumps(body, indent=2, sort_keys=True))
    # root + task artifacts so the manifest treats the run as valid
    (ev / "job_flow.json").write_text('{"job_id":"e2e","final_audit":{"status":"pass"}}')
    for f in ("manifest.json", "agent_run_trace.jsonl", "agent_run_trace_summary.json",
              "prompt_trace_summary.json", "command_transcript.json"):
        (ev / f).write_text("{}")
    for f in ("prompt_trace.jsonl", "prompt_trace_summary.json", "review.json", "repair_loop.json",
              "token_accounting.json", "provider_evidence.json"):
        (ev / "task_runs" / "t1" / f).write_text("{}")
    return ev, subject, authority


class TestAuthoritativeEndToEnd:
    def test_committed_subject_to_ready_zip_with_raw_byte_chain(self, tmp_path):
        repo, base, head = _build_repo(tmp_path)
        ev, subject, authority = _write_evidence(repo, base, head, tmp_path / "evidence")
        proc = _run(["bash", "scripts/make_review_zip.sh", "--evidence-dir", str(ev)],
                    repo, {"REMEDY_REVIEW_BASE": base, "PYTHONPATH": str(REPO_ROOT)})
        assert proc.returncode == 0, proc.stdout + proc.stderr
        zips = sorted(repo.glob("remedy-review-*.zip"))
        assert zips, proc.stdout
        z = zips[-1]

        # F6/F7 — the filename status equals the packaged manifest status.
        assert "READY_FOR_REVIEW" in z.name, proc.stdout

        with zipfile.ZipFile(z) as zf:
            names = set(zf.namelist())
            for n in ("evidence/current/review_subject.json",
                      "evidence/current/current_change_content_proof.json",
                      "evidence/current/review_commit_chain.json",
                      "evidence/current/review_archive_plan.json",
                      "evidence/current/review_zip_expectation.json",
                      ".review_zip_manifest.json"):
                assert n in names, n
            subject_b = zf.read("evidence/current/review_subject.json")
            proof_b = zf.read("evidence/current/current_change_content_proof.json")
            chain_b = zf.read("evidence/current/review_commit_chain.json")
            plan = json.loads(zf.read("evidence/current/review_archive_plan.json"))
            expect = json.loads(zf.read("evidence/current/review_zip_expectation.json"))
            manifest = json.loads(zf.read(".review_zip_manifest.json"))

        subject_sha = hashlib.sha256(subject_b).hexdigest()
        chain_sha = hashlib.sha256(chain_b).hexdigest()
        proof_sha = hashlib.sha256(proof_b).hexdigest()
        chain = manifest["package_hash_chain"]

        # F2 — plan/expectation/manifest subject sha ALL equal the packaged Subject bytes' sha.
        assert plan["review_subject_sha256"] == subject_sha
        assert expect["review_subject_sha256"] == subject_sha
        assert chain["review_subject_sha256"] == subject_sha
        # F4 — commit-chain sha equals the packaged bytes.
        assert chain["commit_chain_sha256"] == chain_sha
        # F2 — content-proof sha equals the packaged bytes.
        assert chain["content_proof_sha256"] == proof_sha
        # F6/F7 — the manifest's own package status is READY.
        assert manifest["package_status"] == "READY_FOR_REVIEW"
        # authority equality reflected in the plan
        auth_members = sorted(m["archive_path"] for m in plan["repository_members"]
                              if m["authoritative"])
        assert auth_members == authority
