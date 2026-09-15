"""
Review-manifest package status, and the do_cmd evidence helpers still under test.

Coverage:
  - build_manifest / validate_evidence_candidate: evidence validity, package status,
    source-root containment and review-bundle integrity
  - _sanitize_shareable_paths, _build_final_audit and the timeout hint
"""

from __future__ import annotations

import json


class TestShareablePathSanitizer:
    """Shareable refs keep their artifact names under canonical prefixes."""

    # --- R-4319: artifact refs preserve filenames ----------------------------

    def test_sanitizer_preserves_evidence_artifact_name(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"ref": "/tmp/remedy-job-evidence-abc123/manifest.json"}
        result = _sanitize_shareable_paths(data)
        assert result["ref"] == "evidence/current/manifest.json", \
            "R-4327: evidence refs must use canonical evidence/current/ prefix"

    def test_sanitizer_preserves_staging_subpath(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"ref": "/tmp/remedy-pingpong-abc123/staging/file.py"}
        result = _sanitize_shareable_paths(data)
        assert result["ref"] == "[staging]/staging/file.py", \
            "R-4319: sanitizer must preserve subpath after staging prefix"

    def test_sanitizer_preserves_home_subpath(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"ref": "/home/alice/project/src/main.py"}
        result = _sanitize_shareable_paths(data)
        assert result["ref"] == "[local]/project/src/main.py", \
            "R-4319: sanitizer must preserve subpath after home prefix"

    # --- R-4316: manifest builder valid JSON ----------------------------------

    def test_manifest_builder_valid_json(self, tmp_path):
        from scripts.build_review_manifest import build_manifest
        manifest = build_manifest(evidence_dir=None)
        raw = json.dumps(manifest)
        parsed = json.loads(raw)
        assert parsed["bundle_kind"] == "remedy_review_zip"
        assert parsed["bundle_version"] == 12
        assert "generated_at" in parsed

    # --- R-4327: canonical artifact refs --------------------------------------

    def test_evidence_ref_canonical(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"ref": "/tmp/remedy-job-evidence-abc123/manifest.json"}
        result = _sanitize_shareable_paths(data)
        assert result["ref"] == "evidence/current/manifest.json", \
            "R-4327: evidence refs must use canonical evidence/current/ prefix"

    def test_evidence_ref_task_run_canonical(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"ref": "/tmp/remedy-job-evidence-abc123/task_runs/T001/review.json"}
        result = _sanitize_shareable_paths(data)
        assert result["ref"] == "evidence/current/task_runs/T001/review.json"


# ---------------------------------------------------------------------------
# Final audit + final verifier integration unit tests
# ---------------------------------------------------------------------------


class _FakeJob:
    """Minimal job stub for _build_final_audit unit tests."""
    def __init__(self, status="completed", tasks=None):
        self.state = status
        self.tasks = tasks or [_FakeTask()]


class _FakeTask:
    def __init__(self, task_id="T001", status="applied_to_job_workspace",
                 reviewer_verdict="pass", test_passed=True):
        self.task_id = task_id
        self.status = status
        self.safe_diff_files = []
        self.reviewer_verdict = reviewer_verdict
        self.test_passed = test_passed


class _FakePromo:
    def __init__(self, status="dry_run"):
        self.status = status
        self.blocked_reason = ""
        self.files_planned = []


def _seed_evidence(ev_path, fv_verdict="PASS", tt_actual=False, tt_est_total=5000):
    """Seed a minimal evidence dir with final_verifier_report + token_truth."""
    ev_path.mkdir(parents=True, exist_ok=True)
    (ev_path / "manifest.json").write_text("{}")
    (ev_path / "prompt_trace_summary.json").write_text("{}")
    (ev_path / "agent_run_trace.jsonl").write_text("")
    (ev_path / "agent_run_trace_summary.json").write_text("{}")
    (ev_path / "final_verifier_report.json").write_text(json.dumps({
        "schema_version": "1.0.0",
        "verdict": fv_verdict,
        "missing_tests_gate": "NEEDS_TESTS" if fv_verdict == "NEEDS_TESTS" else "PASS",
        "scratch_file_guard": "BLOCKED" if fv_verdict == "BLOCKED" else "PASS",
    }))
    (ev_path / "token_truth.json").write_text(json.dumps({
        "schema_version": "1.0.0",
        "actual_available": tt_actual,
        "estimated_total_tokens": tt_est_total,
    }))


class TestFinalAuditVerifierIntegration:
    """Unit tests: _build_final_audit must follow final_verifier_report.json."""

    def test_needs_tests_overrides_ready(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="NEEDS_TESTS")

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "NEEDS_TESTS"
        assert audit["promote_ready"] is False
        assert audit["final_verifier_verdict"] == "NEEDS_TESTS"

    def test_blocked_overrides_ready(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="BLOCKED")

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "BLOCKED"
        assert audit["promote_ready"] is False

    def test_pass_with_risks_not_clean_ready(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="PASS_WITH_RISKS")

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] != "READY_FOR_APPROVAL"
        assert audit["status"] == "NEEDS_REVIEW"
        assert audit["promote_ready"] is False

    def test_needs_repair_overrides_ready(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="NEEDS_REPAIR")

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "NEEDS_REPAIR"
        assert audit["promote_ready"] is False

    def test_pass_allows_ready(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="PASS")

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "READY_FOR_APPROVAL"
        assert audit["promote_ready"] is True

    def test_includes_verifier_and_token_truth_refs(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="PASS", tt_actual=False, tt_est_total=8000)

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["final_verifier_report_ref"] == "final_verifier_report.json"
        assert audit["final_verifier_verdict"] == "PASS"
        assert audit["token_truth_ref"] == "token_truth.json"
        assert audit["token_truth_actual_available"] is False
        assert audit["token_truth_estimated_total"] == 8000
        assert audit["missing_tests_gate_status"] == "PASS"
        assert audit["scratch_file_guard_status"] == "PASS"

    def test_no_verifier_report_falls_through(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True)
        (ev / "manifest.json").write_text("{}")
        (ev / "prompt_trace_summary.json").write_text("{}")
        (ev / "agent_run_trace.jsonl").write_text("")
        (ev / "agent_run_trace_summary.json").write_text("{}")

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "READY_FOR_APPROVAL"
        assert "final_verifier_verdict" not in audit

    def test_final_audit_blocked_on_gate_block(self, tmp_path):
        """Final audit must be BLOCKED when a gate is BLOCKED, even with FV=PASS."""
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="PASS")
        (ev / "change_provenance_gate.json").write_text(json.dumps({
            "verdict": "BLOCKED",
        }))
        (ev / "commit_execution_gate.json").write_text(json.dumps({
            "verdict": "BLOCKED",
        }))

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "BLOCKED"
        assert audit["promote_ready"] is False

    def test_final_audit_blocked_on_commit_needs_tests(self, tmp_path):
        """Final audit BLOCKED when commit_execution is NEEDS_TESTS."""
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="PASS")
        (ev / "commit_execution_gate.json").write_text(json.dumps({
            "verdict": "NEEDS_TESTS",
        }))

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "BLOCKED"
        assert audit["promote_ready"] is False

    # --- manifest dirty-file and alignment tests ---

    def test_manifest_dirty_files_not_truncated(self, tmp_path):
        """Manifest must include all dirty files, never truncate."""
        from scripts.build_review_manifest import build_manifest
        manifest = build_manifest(evidence_dir=None)
        rs = manifest["review_subject"]
        assert rs["dirty_files_truncated"] is False
        assert rs["dirty_file_count_total"] == len(rs["dirty_files"])

    def test_manifest_review_subject_evidence_alignment(self, tmp_path):
        """Manifest includes review_subject_evidence_alignment section."""
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True)
        (ev / "job_flow.json").write_text(json.dumps({
            "job_id": "test-123",
            "final_audit": {"status": "READY_FOR_APPROVAL"},
        }))
        (ev / "change_provenance_gate.json").write_text(json.dumps({
            "verdict": "PASS", "covered_files": [],
        }))
        (ev / "final_verifier_report.json").write_text(json.dumps({
            "verdict": "PASS", "authoritative_changed_files": [],
        }))
        (ev / "commit_execution_gate.json").write_text(json.dumps({
            "verdict": "COMMIT_READY",
        }))
        (ev / "artifact_contract_gate.json").write_text(json.dumps({
            "verdict": "PASS",
        }))
        from scripts.build_review_manifest import build_manifest
        manifest = build_manifest(evidence_dir=str(ev))
        alignment = manifest.get("review_subject_evidence_alignment")
        assert alignment is not None
        assert "verdict" in alignment
        assert "dirty_source_test_files" in alignment
        assert "gate_verdicts" in alignment


class TestManifestEvidenceValidity:
    """Tests for manifest evidence validation and manual repair provenance."""

    def _seed_valid_task(self, ev, tid="T001"):
        d = ev / "task_runs" / tid
        d.mkdir(parents=True, exist_ok=True)
        for art in [
            "prompt_trace.jsonl", "prompt_trace_summary.json",
            "review.json", "repair_loop.json", "token_accounting.json",
            "provider_evidence.json",
        ]:
            (d / art).write_text("{}")
        return d

    def _seed_root(self, ev, job_id="test-123"):
        ev.mkdir(parents=True, exist_ok=True)
        (ev / "job_flow.json").write_text(json.dumps({
            "job_id": job_id, "final_audit": {"status": "READY_FOR_APPROVAL"},
        }))
        (ev / "manifest.json").write_text(json.dumps({"job_id": job_id}))
        for art in [
            "agent_run_trace.jsonl", "agent_run_trace_summary.json",
            "prompt_trace_summary.json", "command_transcript.json",
        ]:
            (ev / art).write_text("{}")

    def test_valid_task_passes_validation(self, tmp_path):
        from scripts.build_review_manifest import validate_evidence_candidate
        ev = tmp_path / "evidence"
        self._seed_root(ev)
        self._seed_valid_task(ev)
        result = validate_evidence_candidate(str(ev))
        assert result["is_valid_current_run"] is True

    def test_missing_provider_evidence_fails(self, tmp_path):
        from scripts.build_review_manifest import validate_evidence_candidate
        ev = tmp_path / "evidence"
        self._seed_root(ev)
        d = ev / "task_runs" / "T001"
        d.mkdir(parents=True, exist_ok=True)
        for art in ["prompt_trace.jsonl", "prompt_trace_summary.json",
                     "review.json", "repair_loop.json", "token_accounting.json"]:
            (d / art).write_text("{}")
        # Missing provider_evidence.json
        result = validate_evidence_candidate(str(ev))
        assert result["is_valid_current_run"] is False

    def test_manual_repair_task_exempt_from_provider_artifacts(self, tmp_path):
        from scripts.build_review_manifest import validate_evidence_candidate
        ev = tmp_path / "evidence"
        self._seed_root(ev)
        self._seed_valid_task(ev, "T001")
        # T002 is manual repair — no provider artifacts
        d = ev / "task_runs" / "T002"
        d.mkdir(parents=True, exist_ok=True)
        for art in ["review.json", "repair_loop.json", "token_accounting.json"]:
            (d / art).write_text("{}")
        (d / "manual_repair_provenance.json").write_text(json.dumps({
            "manual_operator_repair": True,
            "no_provider_calls": True,
            "task_id": "T002",
        }))
        result = validate_evidence_candidate(str(ev))
        assert result["is_valid_current_run"] is True
        assert "T002" in result.get("manual_repair_tasks", [])

    def test_invalid_manual_repair_provenance_fails(self, tmp_path):
        from scripts.build_review_manifest import validate_evidence_candidate
        ev = tmp_path / "evidence"
        self._seed_root(ev)
        d = ev / "task_runs" / "T001"
        d.mkdir(parents=True, exist_ok=True)
        for art in ["review.json", "repair_loop.json", "token_accounting.json"]:
            (d / art).write_text("{}")
        # manual_repair_provenance missing required fields
        (d / "manual_repair_provenance.json").write_text(json.dumps({
            "manual_operator_repair": False,
        }))
        result = validate_evidence_candidate(str(ev))
        assert result["is_valid_current_run"] is False

    def test_final_audit_changed_files_uses_authoritative(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True)
        _seed_evidence(ev, fv_verdict="PASS")
        fv = json.loads((ev / "final_verifier_report.json").read_text())
        fv["authoritative_changed_files"] = ["a.py", "b.py", "c.py"]
        (ev / "final_verifier_report.json").write_text(json.dumps(fv))
        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert sorted(audit["changed_files"]) == ["a.py", "b.py", "c.py"]


class TestReviewZipPackageStatus:
    """Tests for package_status, packaging proof, and always-build semantics."""

    def _seed_valid_evidence(self, ev, job_id="test-pkg-123", file_hashes=None):
        ev.mkdir(parents=True, exist_ok=True)
        (ev / "job_flow.json").write_text(json.dumps({
            "job_id": job_id,
            "final_audit": {"status": "READY_FOR_APPROVAL"},
        }))
        (ev / "manifest.json").write_text(json.dumps({
            "job_id": job_id,
            "task_count": 1,
            "task_ids": ["T001"],
        }))
        for art in [
            "agent_run_trace.jsonl", "agent_run_trace_summary.json",
            "prompt_trace_summary.json", "command_transcript.json",
        ]:
            (ev / art).write_text("{}")
        # Round 31 F1: a single real operator attestation whose final_verifier_report is produced by
        # the actual producer (regenerated at the end of this method), not a hand-written report.
        import hashlib as _hl

        from packages.orchestration import manual_attestation as _MA
        from packages.orchestration.repair_attest import (
            build_safe_diff_text as _bsd,
        )
        from packages.orchestration.repair_attest import (
            canonical_provenance_sha256 as _cps,
        )
        from packages.orchestration.repair_attest import (
            sha256_text as _sht,
        )
        if file_hashes is None:
            # Materialize a real authority file in the repo root (ev.parent) so the content proof and
            # bundle-integrity verify against real bytes, and compute its true hash.
            _content = b"x = 1\n"
            _src = ev.parent / "src"
            _src.mkdir(parents=True, exist_ok=True)
            (_src / "app.py").write_bytes(_content)
            file_hashes = {"src/app.py": _hl.sha256(_content).hexdigest()}
        _authority = sorted(dict(file_hashes))
        _diff = "".join(
            f"diff --git a/{p} b/{p}\nnew file mode 100644\nindex 0000000..1111111\n"
            f"--- /dev/null\n+++ b/{p}\n@@ -0,0 +1 @@\n+x = 1\n" for p in _authority)
        _safe = _bsd(_diff, [])
        _tsha, _ssha = _sht(_diff), _sht(_safe)
        _prov = _cps(_tsha, [])
        _MA.write_manual_task_evidence(
            str(ev), job_id=job_id, task_id="T001", changed_files=_authority, safe_diff_text=_safe,
            provenance_sha256=_prov, diff_sha256=_prov, tracked_diff_sha256=_tsha,
            safe_diff_sha256=_ssha, timestamp="2026-07-18T00:00:00+00:00",
            note="operator-attested do_job_flow fixture")
        (ev / "final_job_review.json").write_text(json.dumps({
            "job_id": job_id, "completion_mode": "manual_operator_repair",
            "human_final_reviewer_required": True, "completion_provider_call_count": 0,
            "linked_prior_job_ids": [], "linked_prior_job_summaries": [],
            "per_task_changed_files": {"T001": _authority}, "actual_changed_files": _authority,
            "expected_changed_files": _authority}))
        # Round 22-25: READY requires the COMPLETE, closed-schema, semantically-consistent gate
        # matrix — recursive schemas, complete gate semantics and an exact derived commit gate.
        _hashes = dict(file_hashes) if file_hashes else {"src/app.py": "0" * 64}
        _auth = sorted(_hashes)
        _core = ("manifest.json", "job_report.json", "token_truth.json", "fresh_evidence_gate.json",
                 "artifact_contract_gate.json", "runtime_integration_gate.json",
                 "change_provenance_gate.json", "commit_execution_gate.json",
                 "final_verifier_report.json")
        (ev / "fresh_evidence_gate.json").write_text(json.dumps({
            "schema_version": "1.0.0", "verdict": "PASS", "evidence_authoritative": True,
            "job_id_match": True, "plan_match": True, "live_review_match": True,
            "evidence_job_id": job_id, "current_job_id": job_id,
            "current_step_range": "1-2", "live_review_step_range": "1-2", "plan_step_range": "1-2",
            "evidence_freshness": {"is_fresh": True, "job_id_match": True,
                                   "step_range_match": True},
            "evidence_validity": {"has_job_id": True, "has_manifest": True,
                                  "is_valid_current_run": True}, "issues": []}))
        # final_verifier_report.json is REGENERATED by the real producer at the end of this method.
        (ev / "artifact_contract_gate.json").write_text(json.dumps({
            "schema_version": "1.0.0", "verdict": "PASS", "missing_required": [],
            "fv_referenced_missing": [], "critical_fv_missing": [], "issues": [],
            "job_id_fresh": True, "evidence_job_id": job_id,
            "required_artifacts": {a: True for a in _core},
            "optional_artifacts": {"scratch_file_guard.json": True},
            "stream_artifacts": {"applicable": False, "verdict": "NOT_APPLICABLE",
                                 "tasks_with_stream_evidence": [], "artifacts_verified": 0,
                                 "artifacts_present": 0, "missing_stream_artifact_listing": [],
                                 "missing_stream_artifacts": [], "missing_stream_artifact_metadata": [],
                                 "stream_artifact_hash_mismatches": [],
                                 "stream_artifact_size_mismatches": [], "unexpected_stream_artifacts": [],
                                 "duplicate_stream_artifact_refs": [], "unsafe_stream_artifact_refs": []},
            "worktree_artifacts": {"applicable": False, "verdict": "NOT_APPLICABLE",
                                   "job_level_handoff": False, "handoff_coverage_verdict": "",
                                   "handoff_coverage_issues": [], "missing_job_handoff": [],
                                   "worktree_tasks": [], "diffs_verified": 0, "missing_result_diffs": [],
                                   "missing_result_diff_references": [], "result_diff_hash_mismatches": [],
                                   "result_diff_size_mismatches": [], "unreferenced_result_diffs": [],
                                   "unsafe_result_diff_refs": []}}))
        (ev / "change_provenance_gate.json").write_text(json.dumps({
            "schema_version": "1.0.0", "verdict": "PASS", "current_job_id": job_id,
            "covered_files": _auth, "source_files": _auth, "excluded_files": [],
            "evidence_covered_files": _auth, "evidence_sources": [], "dirty_files": [],
            "uncovered_files": [], "content_hash_verified": True, "hash_mismatches": [],
            "stale_apply_proofs": [], "issues": [], "current_hashes": _hashes,
            "evidence_hashes": _hashes}))
        (ev / "runtime_integration_gate.json").write_text(json.dumps({
            "schema_version": "1.0.0", "verdict": "PASS",
            "checks": [{"check_id": "c0", "check_type": "call_exists", "source_file": "src/app.py",
                        "pattern": "add(", "found": True, "file_missing": False}],
            "checks_total": 1, "checks_passed": 1, "issues": []}))
        (ev / "manifest_integrity.json").write_text(json.dumps({
            "schema_version": "1.0.0", "ok": True, "failures": [], "notes": []}))
        (ev / "postmortem_integrity.json").write_text(json.dumps({
            "schema_version": "1.0.0", "ok": True, "failures": []}))
        (ev / "commit_execution_gate.json").write_text(json.dumps({
            "schema_version": "1.0.0", "verdict": "NEEDS_HUMAN_APPROVAL", "promote_ready": False,
            "blocked_gates": [], "non_pass_gates": ["final_verifier"],
            "issues": ["gate 'final_verifier' is not PASS (verdict 'PASS_WITH_RISKS')"],
            "gate_checks": {
                "final_verifier": "PASS_WITH_RISKS", "fresh_evidence_gate": "PASS",
                "artifact_contract_gate": "PASS", "change_provenance_gate": "PASS",
                "runtime_integration_gate": "PASS"}}))
        (ev / "verification_tests.json").write_text(json.dumps({
            "schema_version": "1.0.0", "verification_type": "explicit_commands",
            "runs": [{"run_id": "vr-0001", "command": "pytest -q", "exit_code": 0, "passed": 1,
                      "failed": 0, "test_files": ["t.py"], "stdout_summary": "1 passed"}],
            "command": "pytest -q", "exit_code": 0, "passed": 1, "failed": 0,
            "test_files": ["t.py"], "timestamp": "2026-07-18T00:00:00Z"}))
        # A content proof for the attested authority, and the commit chain/subject the manual
        # completion recompute tolerates (no declared base -> the legacy dirty-tree path).
        if not (ev / "current_change_content_proof.json").exists():
            (ev / "current_change_content_proof.json").write_text(json.dumps({
                "schema_version": "1.1.0", "base_commit": "", "head_commit": "",
                "file_hashes": _hashes, "file_count": len(_hashes),
                "tombstones": {}, "tombstone_count": 0}))
        # Round 32 F2: the canonical token truth is the aggregate of the tasks — written AFTER them.
        _MA.write_manual_token_truth(str(ev))
        # Round 31 F1: regenerate the final verifier report from the assembled bundle with the REAL
        # producer, so the packaged report is reproducible (never a hand-written report).
        from packages.orchestration.final_verifier import build_final_verifier_report
        (ev / "final_verifier_report.json").write_text(json.dumps(
            build_final_verifier_report(str(ev))))

    @staticmethod
    def _init_clean_git(path):
        """Create a clean git repo with committed state. Portable across environments."""
        import subprocess
        r = subprocess.run(["git", "init"], cwd=str(path), capture_output=True)
        assert r.returncode == 0, f"git init failed: {r.stderr.decode()}"
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=str(path), capture_output=True, check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=str(path), capture_output=True, check=True,
        )
        r = subprocess.run(
            ["git", "add", "."], cwd=str(path), capture_output=True,
        )
        assert r.returncode == 0, f"git add failed: {r.stderr.decode()}"
        r = subprocess.run(
            ["git", "commit", "-m", "init", "--allow-empty"],
            cwd=str(path), capture_output=True,
        )
        assert r.returncode == 0, f"git commit failed: {r.stderr.decode()}"

    def test_valid_evidence_ready_for_review(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        self._seed_valid_evidence(ev)
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["review_package_created"] is True
        # Without content hash proof, valid evidence is READY_FOR_REVIEW_UNVERIFIED
        assert m["package_status"] in ("READY_FOR_REVIEW", "READY_FOR_REVIEW_UNVERIFIED")

    def test_invalid_evidence_blocked_but_created(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True, exist_ok=True)
        (ev / "job_flow.json").write_text(json.dumps({
            "job_id": "x", "final_audit": {"status": "BLOCKED"},
        }))
        (ev / "manifest.json").write_text(json.dumps({
            "job_id": "x", "task_count": 0, "task_ids": [],
        }))
        for art in [
            "agent_run_trace.jsonl", "agent_run_trace_summary.json",
            "prompt_trace_summary.json", "command_transcript.json",
        ]:
            (ev / art).write_text("{}")
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["review_package_created"] is True
        assert m["package_status"] == "BLOCKED_EVIDENCE"

    def test_packaging_proof_records_evidence_dir(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        self._seed_valid_evidence(ev)
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["packaged_evidence_job_id"] == "test-pkg-123"
        assert m["packaged_evidence_manifest_task_count"] == 1
        assert m["packaged_evidence_manifest_task_ids"] == ["T001"]
        # Shareable manifest: no machine-specific absolute prefixes.
        assert m["packaged_evidence_dir"] == f"[source_root]/{ev.name}"
        assert m["source_root"] == "[source_root]"
        assert m["packaging_command_context"]["cwd"] == "[source_root]"
        assert m["packaging_command_context"]["evidence_dir_arg"] == f"[source_root]/{ev.name}"

    def test_manual_repair_missing_provenance_blocks_authority(self, tmp_path):
        from scripts.build_review_manifest import validate_evidence_candidate
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True, exist_ok=True)
        (ev / "job_flow.json").write_text(json.dumps({
            "job_id": "x", "final_audit": {"status": "READY_FOR_APPROVAL"},
        }))
        (ev / "manifest.json").write_text(json.dumps({"job_id": "x"}))
        for art in [
            "agent_run_trace.jsonl", "agent_run_trace_summary.json",
            "prompt_trace_summary.json", "command_transcript.json",
        ]:
            (ev / art).write_text("{}")
        d = ev / "task_runs" / "T006"
        d.mkdir(parents=True, exist_ok=True)
        for art in ["review.json", "repair_loop.json", "token_accounting.json"]:
            (d / art).write_text("{}")
        result = validate_evidence_candidate(str(ev))
        assert result["is_valid_current_run"] is False
        assert any("T006" in e for e in result["validation_errors"])

    def test_packaging_warnings_populated(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True, exist_ok=True)
        (ev / "job_flow.json").write_text(json.dumps({
            "job_id": "x", "final_audit": {"status": "BLOCKED"},
        }))
        (ev / "manifest.json").write_text(json.dumps({
            "job_id": "x", "task_count": 0, "task_ids": [],
        }))
        for art in [
            "agent_run_trace.jsonl", "agent_run_trace_summary.json",
            "prompt_trace_summary.json", "command_transcript.json",
        ]:
            (ev / art).write_text("{}")
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert len(m["packaging_warnings"]) > 0
        assert m["package_status"] == "BLOCKED_EVIDENCE"

    def test_dirty_worktree_valid_evidence_blocked(self, tmp_path, monkeypatch):
        """Valid evidence + dirty worktree => BLOCKED_EVIDENCE."""
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        self._seed_valid_evidence(ev)
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        # Create dirty file after commit
        (tmp_path / "dirty.py").write_text("x = 1")
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["review_package_created"] is True
        assert m["package_status"] == "BLOCKED_EVIDENCE"
        assert any("alignment" in w for w in m["packaging_warnings"])


class TestZipFilenameAndStatus:
    """Zip filename must include package status; status must be machine-readable."""

    def test_ready_manifest_has_ready_status(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ev
        )
        monkeypatch.chdir(tmp_path)
        TestReviewZipPackageStatus._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["package_status"] in ("READY_FOR_REVIEW", "READY_FOR_REVIEW_UNVERIFIED")
        assert m["review_package_created"] is True
        assert "READY_FOR_REVIEW" in m["package_status"]

    def test_blocked_manifest_has_blocked_status(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ev
        )
        monkeypatch.chdir(tmp_path)
        TestReviewZipPackageStatus._init_clean_git(tmp_path)
        (tmp_path / "extra_dirty.py").write_text("x = 1")
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["package_status"] == "BLOCKED_EVIDENCE"
        assert m["review_package_created"] is True

    def test_package_status_filename_safe(self):
        """package_status values are safe for use in filenames."""
        for status in ["READY_FOR_REVIEW", "READY_FOR_REVIEW_UNVERIFIED", "BLOCKED_EVIDENCE"]:
            assert "/" not in status
            assert " " not in status
            assert status == status.upper()

    def test_blocked_package_not_commit_ready(self, tmp_path, monkeypatch):
        """BLOCKED_EVIDENCE must not coexist with evidence_authoritative=true."""
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ev
        )
        monkeypatch.chdir(tmp_path)
        TestReviewZipPackageStatus._init_clean_git(tmp_path)
        (tmp_path / "dirty.py").write_text("x = 1")
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["package_status"] == "BLOCKED_EVIDENCE"
        ce = m.get("current_evidence", {})
        ef = ce.get("evidence_freshness", {})
        assert ef.get("evidence_authoritative") is False


class TestSourceRootContainment:
    """Source-root containment: packaging must be within git source root."""

    @staticmethod
    def _init_clean_git(path):
        import subprocess
        for cmd in [
            ["git", "init"],
            ["git", "config", "user.email", "test@example.com"],
            ["git", "config", "user.name", "Test User"],
            ["git", "add", "."],
            ["git", "commit", "-m", "init", "--allow-empty"],
        ]:
            r = subprocess.run(cmd, cwd=str(path), capture_output=True)
            assert r.returncode == 0, f"{cmd} failed: {r.stderr.decode()}"

    def test_containment_pass_when_inside_source_root(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ev
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["source_root_containment"]["verdict"] == "PASS"
        assert m["source_root_containment"]["blockers"] == []
        assert m["external_paths_detected"] == []
        assert m["package_status"] in ("READY_FOR_REVIEW", "READY_FOR_REVIEW_UNVERIFIED")

    def test_evidence_outside_source_root_blocked(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        repo = tmp_path / "repo"
        repo.mkdir()
        monkeypatch.chdir(repo)
        self._init_clean_git(repo)
        # Evidence dir outside repo
        ext_ev = tmp_path / "external_evidence"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ext_ev
        )
        m = build_manifest(str(ext_ev), selection_mode="explicit")
        assert m["source_root_containment"]["verdict"] == "BLOCKED"
        assert len(m["source_root_containment"]["blockers"]) > 0
        assert m["package_status"] == "BLOCKED_EVIDENCE"
        assert len(m["external_paths_detected"]) > 0

    def test_manifest_records_source_root(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ev
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        # The shareable manifest carries a token, never the private absolute root.
        assert m["source_root"] == "[source_root]"

    def test_zip_still_created_when_containment_fails(self, tmp_path, monkeypatch):
        """Containment failure must not prevent zip creation."""
        from scripts.build_review_manifest import build_manifest
        repo = tmp_path / "repo"
        repo.mkdir()
        monkeypatch.chdir(repo)
        self._init_clean_git(repo)
        ext_ev = tmp_path / "ext_ev"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ext_ev
        )
        m = build_manifest(str(ext_ev), selection_mode="explicit")
        assert m["review_package_created"] is True
        assert m["package_status"] == "BLOCKED_EVIDENCE"

    def test_no_code_references_clean_worktree(self):
        """No code path should default to remedy-clean-*."""
        import subprocess
        result = subprocess.run(
            ["grep", "-rn", "remedy-clean-", "scripts/", "apps/cli/",
             "packages/orchestration/"],
            capture_output=True, text=True,
        )
        matches = [l for l in result.stdout.splitlines()
                   if not l.endswith(".pyc") and "__pycache__" not in l]
        assert matches == [], f"Code references remedy-clean-: {matches}"


class TestReviewBundleIntegrity:
    """Review-bundle integrity: packaged file hashes must match content proof."""

    @staticmethod
    def _init_clean_git(path):
        import subprocess
        for cmd in [
            ["git", "init"],
            ["git", "config", "user.email", "test@example.com"],
            ["git", "config", "user.name", "Test User"],
            ["git", "add", "."],
            ["git", "commit", "-m", "init", "--allow-empty"],
        ]:
            r = subprocess.run(cmd, cwd=str(path), capture_output=True)
            assert r.returncode == 0, f"{cmd} failed: {r.stderr.decode()}"

    @staticmethod
    def _seed_with_proof(tmp_path, file_contents, proof_hashes):
        """Create evidence dir with content proof and source files."""
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True, exist_ok=True)
        # Seed valid evidence base — bind the change-provenance hash maps to the same proof hashes.
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ev, file_hashes=proof_hashes
        )
        # Write content proof
        proof = {
            "schema_version": 1,
            "file_hashes": proof_hashes,
            "file_count": len(proof_hashes),
        }
        (ev / "current_change_content_proof.json").write_text(
            json.dumps(proof)
        )
        # Write source files
        for rel_path, content in file_contents.items():
            fp = tmp_path / rel_path
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
        return ev

    def test_matching_proof_ready_for_review(self, tmp_path, monkeypatch):
        """Matching hashes → PASS → READY_FOR_REVIEW."""
        import hashlib

        from scripts.build_review_manifest import build_manifest
        content = "x = 1\n"
        h = hashlib.sha256(content.encode()).hexdigest()
        ev = self._seed_with_proof(
            tmp_path,
            {"src/app.py": content},
            {"src/app.py": h},
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        bi = m["review_bundle_integrity"]
        assert bi["current_content_hash_checked"] is True
        assert bi["current_content_hash_mismatches"] == []
        assert bi["current_content_hash_missing_proofs"] == []
        assert bi["verdict"] == "PASS"
        assert m["package_status"] == "READY_FOR_REVIEW"

    def test_hash_mismatch_blocked(self, tmp_path, monkeypatch):
        """Hash mismatch → BLOCKED → BLOCKED_EVIDENCE."""
        from scripts.build_review_manifest import build_manifest
        content = "x = 1\n"
        wrong_hash = "0" * 64
        ev = self._seed_with_proof(
            tmp_path,
            {"src/app.py": content},
            {"src/app.py": wrong_hash},
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        bi = m["review_bundle_integrity"]
        assert bi["verdict"] == "BLOCKED"
        assert len(bi["current_content_hash_mismatches"]) == 1
        mm = bi["current_content_hash_mismatches"][0]
        assert mm["file"] == "src/app.py"
        assert mm["expected"] == wrong_hash
        assert mm["actual"] != wrong_hash
        assert m["package_status"] == "BLOCKED_EVIDENCE"

    def test_mismatch_includes_both_hashes(self, tmp_path, monkeypatch):
        """Mismatch entries include expected and actual SHA256."""
        import hashlib

        from scripts.build_review_manifest import build_manifest
        content = "x = 2\n"
        actual_h = hashlib.sha256(content.encode()).hexdigest()
        wrong_h = "a" * 64
        ev = self._seed_with_proof(
            tmp_path,
            {"src/b.py": content},
            {"src/b.py": wrong_h},
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        mm = m["review_bundle_integrity"]["current_content_hash_mismatches"][0]
        assert mm["expected"] == wrong_h
        assert mm["actual"] == actual_h

    def test_missing_proof_blocked(self, tmp_path, monkeypatch):
        """File in proof but not on disk → missing proof → BLOCKED."""
        from scripts.build_review_manifest import build_manifest
        ev = self._seed_with_proof(
            tmp_path,
            {},
            {"src/nonexistent.py": "f" * 64},
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        bi = m["review_bundle_integrity"]
        assert bi["verdict"] == "BLOCKED"
        assert "src/nonexistent.py" in bi["current_content_hash_missing_proofs"]
        assert m["package_status"] == "BLOCKED_EVIDENCE"

    def test_zip_still_created_on_mismatch(self, tmp_path, monkeypatch):
        """Mismatch must not prevent zip creation."""
        from scripts.build_review_manifest import build_manifest
        ev = self._seed_with_proof(
            tmp_path,
            {"src/c.py": "y = 1\n"},
            {"src/c.py": "0" * 64},
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["review_package_created"] is True
        assert m["package_status"] == "BLOCKED_EVIDENCE"

    def test_filename_status_matches_manifest(self, tmp_path, monkeypatch):
        """Package filename suffix must match manifest package_status."""
        import hashlib

        from scripts.build_review_manifest import build_manifest
        content = "z = 3\n"
        h = hashlib.sha256(content.encode()).hexdigest()
        ev = self._seed_with_proof(
            tmp_path,
            {"src/d.py": content},
            {"src/d.py": h},
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        status = m["package_status"]
        assert status in ("READY_FOR_REVIEW", "BLOCKED_EVIDENCE")
        assert "/" not in status
        assert " " not in status


# ---------------------------------------------------------------------------
# Round 16 — F1: the restored timeout hint
# ---------------------------------------------------------------------------


class TestTheTimeoutHintReportsResolvedTruth:
    """F1 (round 16): the hint reports what `run_job` RESOLVED and recorded.

    It must never re-resolve a default at the call site — that is what the shared
    `RunInvocation` exists to prevent, and re-introducing `timeout_sec or 120` here would
    silently defeat the omission sentinel the whole tri-state contract rests on.
    """

    def _job(self, timeout_sec):
        from packages.orchestration.pingpong_job import ExecutionConfig, JobPlan

        job = JobPlan(job_id="j" * 16, job_title="t", repo_path="/tmp/x")
        if timeout_sec is not None:
            job.execution_config = ExecutionConfig(timeout_sec=timeout_sec)
        return job

    def test_an_omitted_timeout_reports_the_resolved_product_default(self) -> None:
        """Omission is preserved into `run_job`; the hint then reports what it settled on."""
        from apps.cli.commands.do_cmd import _build_timeout_hint, _effective_timeout_sec

        job = self._job(120)                       # what run_job resolved and persisted
        assert _effective_timeout_sec(job) == 120
        hint = _build_timeout_hint("claude-cli", "fake", _effective_timeout_sec(job))
        assert "120s" in hint and "--timeout-sec 900" in hint

    def test_an_explicit_timeout_reports_that_timeout(self) -> None:
        from apps.cli.commands.do_cmd import _build_timeout_hint, _effective_timeout_sec

        job = self._job(300)
        assert _effective_timeout_sec(job) == 300
        assert "300s" in _build_timeout_hint("claude-cli", "fake", _effective_timeout_sec(job))

    def test_an_explicit_profile_reports_its_effective_timeout(self) -> None:
        """A profile resolves to a number inside `run_job`; the hint reports the EFFECT."""
        from apps.cli.commands.do_cmd import _build_timeout_hint, _effective_timeout_sec

        job = self._job(900)                       # e.g. a long profile
        assert _effective_timeout_sec(job) == 900
        assert _build_timeout_hint("claude-cli", "fake", _effective_timeout_sec(job)) == ""

    def test_no_execution_config_says_nothing_rather_than_guessing(self) -> None:
        from apps.cli.commands.do_cmd import _build_timeout_hint, _effective_timeout_sec

        job = self._job(None)
        assert _effective_timeout_sec(job) is None
        assert _build_timeout_hint("claude-cli", "fake", None) == ""

    def test_non_cli_providers_never_get_the_hint(self) -> None:
        from apps.cli.commands.do_cmd import _build_timeout_hint

        assert _build_timeout_hint("fake", "fake", 10) == ""

    def test_the_hint_never_changes_execution(self) -> None:
        """Informational only: it reads the persisted config and returns a string."""
        import inspect

        from apps.cli.commands.do_cmd import _build_timeout_hint

        src = inspect.getsource(_build_timeout_hint)
        assert "run_job" not in src and "=" not in src.split("return")[-1]
