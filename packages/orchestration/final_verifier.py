"""Final verifier report — deterministic, read-only verification summary.

Aggregates every gate and evidence artifact produced for a job into a single
final verdict. Pure orchestration logic: no provider calls, no target-repo
mutation, no job state mutation. The report is built only from files already on
disk, so the same evidence dir always yields the same report.

Reads (all optional — missing inputs degrade gracefully):
    job_report.json / job_flow.json
    self_run_observability_index.json
    scratch_file_guard.json
    prompt_trace_summary.json
    task_runs/<task_id>/review_scope_packet.json
    task_runs/<task_id>/spec_compliance_check.json
    task_runs/<task_id>/missing_tests_gate.json
    task_runs/<task_id>/scratch_file_guard.json
    task_runs/<task_id>/review.json
    task_runs/<task_id>/repair_loop.json
    task_runs/<task_id>/tests.txt
    task_runs/<task_id>/token_accounting.json
    task_runs/<task_id>/safe.diff

Public API:
    build_final_verifier_report(evidence_dir) -> dict
    write_final_verifier_report(evidence_dir, written) -> None
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"

_SAFE_TASK_ID_RE = re.compile(r"^T\d{3,}$")

# pytest-style result counters, e.g. "3 passed", "1 failed".
_PASSED_RE = re.compile(r"(\d+)\s+passed", re.IGNORECASE)
_FAILED_RE = re.compile(r"(\d+)\s+(?:failed|error[s]?)", re.IGNORECASE)

_RECOMMENDED_ACTION = {
    "PASS": "Approve and promote.",
    "PASS_WITH_RISKS": "Approve with risks; review missing optional evidence before promoting.",
    "NEEDS_TESTS": "Run the missing tests before promoting.",
    "NEEDS_REPAIR": "Resolve the open findings before promoting.",
    "BLOCKED": "Blocked: resolve gate violations before promoting.",
}


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        return ""


def _read_gate_verdict(base: Path, filename: str) -> str:
    """Return the ``verdict`` string from a job-level gate JSON, or "" if absent."""
    data = _read_json(base / filename)
    if isinstance(data, dict):
        return str(data.get("verdict", "") or "")
    return ""


def _task_ids(base: Path) -> list[str]:
    """Return sorted, safe task IDs that have a task_runs/<id>/ directory."""
    runs = base / "task_runs"
    if not runs.is_dir():
        return []
    ids = [
        child.name
        for child in runs.iterdir()
        if child.is_dir() and _SAFE_TASK_ID_RE.fullmatch(child.name)
    ]
    return sorted(ids)


def _normalize(path: str) -> str:
    p = path.replace("\\", "/").strip()
    while p.startswith("./"):
        p = p[2:]
    return p


def _diff_paths(diff_text: str) -> set[str]:
    """Extract file paths from unified diff headers."""
    _PATH_RE = re.compile(r"^[+-]{3}\s+[ab]/(.+)$")
    files: set[str] = set()
    for line in diff_text.splitlines():
        m = _PATH_RE.match(line)
        if m:
            p = m.group(1).strip()
            if p and p != "/dev/null":
                files.add(_normalize(p))
    return files


def _collect_changes(base: Path, task_ids: list[str]) -> tuple[list[str], dict[str, Any]]:
    changed_files: set[str] = set()
    range_acc: dict[str, list[Any]] = {}
    for tid in task_ids:
        packet = _read_json(base / "task_runs" / tid / "review_scope_packet.json")
        if not isinstance(packet, dict):
            continue
        for f in packet.get("changed_files") or []:
            changed_files.add(str(f))
        for f, ranges in (packet.get("changed_line_ranges") or {}).items():
            acc = range_acc.setdefault(str(f), [])
            for r in ranges or []:
                if r not in acc:
                    acc.append(r)
    changed_line_ranges: dict[str, Any] = {
        f: sorted(acc, key=lambda r: r if isinstance(r, list) else [r])
        for f, acc in range_acc.items()
    }
    return sorted(changed_files), changed_line_ranges


_OPERATIONAL_PREFIXES = (".agent/", ".data/", "remedy-job-evidence", "run_transcript")
_OPERATIONAL_SUFFIXES = (".log", ".zip", ".tar", ".gz", ".pyc", ".pyo")


def _is_source_for_alignment(path: str) -> bool:
    """Filter out operational/excluded files from authoritative set."""
    if any(path.startswith(p) for p in _OPERATIONAL_PREFIXES):
        return False
    if any(path.endswith(s) for s in _OPERATIONAL_SUFFIXES):
        return False
    if any(sub in path for sub in ("__pycache__", "htmlcov/", ".coverage")):
        return False
    return True


def _collect_authoritative_changed_files(base: Path, task_ids: list[str]) -> list[str]:
    """Union changed files from all evidence sources, excluding operational files."""
    files: set[str] = set()

    for tid in task_ids:
        packet = _read_json(base / "task_runs" / tid / "review_scope_packet.json")
        if isinstance(packet, dict):
            for f in packet.get("changed_files") or []:
                files.add(_normalize(str(f)))
        safe_diff = base / "task_runs" / tid / "safe.diff"
        if safe_diff.exists():
            files |= _diff_paths(_read_text(safe_diff))

    ws_diff = base / "workspace.diff"
    if ws_diff.exists():
        files |= _diff_paths(_read_text(ws_diff))

    apply_json = _read_json(base / "workspace_apply.json")
    if isinstance(apply_json, list):
        for entry in apply_json:
            if isinstance(entry, dict):
                manifest = entry.get("apply_manifest")
                if isinstance(manifest, dict):
                    for f in manifest.get("applied_files") or []:
                        files.add(_normalize(str(f)))

    cp_gate = _read_json(base / "change_provenance_gate.json")
    if isinstance(cp_gate, dict):
        for f in cp_gate.get("covered_files") or []:
            files.add(_normalize(str(f)))

    return sorted(f for f in files if _is_source_for_alignment(f))


def _file_set_alignment(
    base: Path,
    authoritative_files: list[str],
    review_scope_files: list[str],
) -> dict[str, Any]:
    """Compare authoritative changed files against review scope changed files."""
    auth_set = set(authoritative_files)
    scope_set = set(review_scope_files)

    cp_gate = _read_json(base / "change_provenance_gate.json")
    cp_present = isinstance(cp_gate, dict) and cp_gate.get("verdict")
    cp_covered = set()
    cp_hash_mismatches: list[dict[str, str]] = []
    if cp_present:
        cp_covered = {_normalize(str(f)) for f in (cp_gate.get("covered_files") or [])}
        cp_hash_mismatches = cp_gate.get("hash_mismatches") or []

    in_auth_not_scope = sorted(auth_set - scope_set)
    in_scope_not_auth = sorted(scope_set - auth_set)

    uncovered = sorted(auth_set - cp_covered) if cp_present else []

    mismatches: list[str] = []
    blocking: list[str] = []

    if in_auth_not_scope:
        mismatches.append(
            f"authoritative files not in review_scope: {in_auth_not_scope}"
        )
    if in_scope_not_auth:
        mismatches.append(
            f"review_scope files not in authoritative set: {in_scope_not_auth}"
        )
    if uncovered:
        blocking.append(
            f"authoritative files not covered by change_provenance: {uncovered}"
        )
        mismatches.append(blocking[-1])

    has_hash_mismatches = bool(cp_hash_mismatches)
    if has_hash_mismatches:
        blocking.append(
            f"content hash mismatches: {[m['file'] for m in cp_hash_mismatches]}"
        )
        mismatches.append(blocking[-1])

    if blocking:
        status = "BLOCKED"
    elif mismatches:
        status = "PASS_WITH_RISKS"
    else:
        status = "PASS"

    return {
        "authoritative_changed_files": authoritative_files,
        "change_source_mismatches": mismatches,
        "review_subject_uncovered_files": uncovered,
        "content_hash_mismatches": cp_hash_mismatches,
        "file_set_alignment_status": status,
    }


def _aggregate_gate(base: Path, task_ids: list[str], filename: str, key: str,
                    severity: dict[str, int], default: str) -> str:
    """Return the worst per-task gate status for the given evidence file."""
    worst = default
    worst_rank = severity.get(default, 0)
    for tid in task_ids:
        data = _read_json(base / "task_runs" / tid / filename)
        if not isinstance(data, dict):
            continue
        status = str(data.get(key, "") or "")
        rank = severity.get(status, 0)
        if rank > worst_rank:
            worst_rank = rank
            worst = status
    return worst


def _scratch_status(base: Path, task_ids: list[str]) -> str:
    severity = {"PASS": 0, "BLOCKED": 2}
    worst = "PASS"
    worst_rank = 0
    job_level = _read_json(base / "scratch_file_guard.json")
    candidates: list[Any] = [job_level]
    for tid in task_ids:
        candidates.append(_read_json(base / "task_runs" / tid / "scratch_file_guard.json"))
    for data in candidates:
        if not isinstance(data, dict):
            continue
        rank = severity.get(str(data.get("guard_status", "") or ""), 0)
        if rank > worst_rank:
            worst_rank = rank
            worst = "BLOCKED"
    return worst


def _collect_unresolved_findings(base: Path, task_ids: list[str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for tid in task_ids:
        review = _read_json(base / "task_runs" / tid / "review.json")
        # Map finding id -> latest detail seen across review rounds.
        detail_by_id: dict[str, dict[str, Any]] = {}
        last_round_findings: list[dict[str, Any]] = []
        final_verdict = ""
        if isinstance(review, dict):
            final_verdict = str(review.get("final_verdict", "") or "")
            for rnd in review.get("reviews") or []:
                if not isinstance(rnd, dict):
                    continue
                round_findings = rnd.get("findings") or []
                last_round_findings = [f for f in round_findings if isinstance(f, dict)]
                for f in last_round_findings:
                    fid = str(f.get("id", "") or "")
                    if fid:
                        detail_by_id[fid] = f

        repair = _read_json(base / "task_runs" / tid / "repair_loop.json")
        open_ids: list[str] = []
        if isinstance(repair, dict):
            open_ids = [str(i) for i in (repair.get("open_findings") or [])]

        if open_ids:
            for fid in open_ids:
                detail = detail_by_id.get(fid, {})
                findings.append({
                    "task_id": tid,
                    "finding_id": fid,
                    "severity": str(detail.get("severity", "") or ""),
                    "file": str(detail.get("file", "") or ""),
                    "summary": str(detail.get("summary", "") or ""),
                })
        elif final_verdict and final_verdict != "pass":
            for f in last_round_findings:
                findings.append({
                    "task_id": tid,
                    "finding_id": str(f.get("id", "") or ""),
                    "severity": str(f.get("severity", "") or ""),
                    "file": str(f.get("file", "") or ""),
                    "summary": str(f.get("summary", "") or ""),
                })
    return findings


def _aggregate_test_status(base: Path, task_ids: list[str]) -> dict[str, Any]:
    ran = False
    passed = 0
    failed = 0
    for tid in task_ids:
        text = _read_text(base / "task_runs" / tid / "tests.txt")
        if not text.strip():
            continue
        for m in _PASSED_RE.finditer(text):
            passed += int(m.group(1))
            ran = True
        for m in _FAILED_RE.finditer(text):
            failed += int(m.group(1))
            ran = True
    return {"ran": ran, "passed": passed, "failed": failed}


def _token_status(base: Path, task_ids: list[str]) -> dict[str, Any]:
    truth = _read_json(base / "token_truth.json")
    if isinstance(truth, dict) and truth.get("schema_version"):
        return {
            "actual_available": bool(truth.get("actual_available", False)),
            "actual_prompt_tokens": truth.get("actual_prompt_tokens"),
            "actual_completion_tokens": truth.get("actual_completion_tokens"),
            "actual_total_tokens": truth.get("actual_total_tokens"),
            "estimated_prompt_tokens": truth.get("estimated_prompt_tokens", 0),
            "estimated_completion_tokens": truth.get("estimated_completion_tokens", 0),
            "estimated_total_tokens": truth.get("estimated_total_tokens", 0),
            "measurement_source": truth.get("measurement_source", ""),
            "measurement_confidence": truth.get("measurement_confidence", ""),
            "missing_reason": truth.get("missing_reason"),
            "builder_estimated_total": truth.get("builder_estimated_total", 0),
            "reviewer_estimated_total": truth.get("reviewer_estimated_total", 0),
            "repair_estimated_total": truth.get("repair_estimated_total", 0),
            "provider_call_count": truth.get("provider_call_count", 0),
        }
    actual_available = False
    estimated = 0
    for tid in task_ids:
        acc = _read_json(base / "task_runs" / tid / "token_accounting.json")
        if not isinstance(acc, dict):
            continue
        if acc.get("actual_tokens_available") or acc.get("kind") == "actual":
            actual_available = True
        for field in (
            "builder_prompt_tokens_estimated",
            "reviewer_prompt_tokens_estimated",
            "repair_prompt_tokens_estimated",
        ):
            val = acc.get(field)
            if isinstance(val, (int, float)):
                estimated += int(val)
    trace = _read_json(base / "prompt_trace_summary.json")
    if isinstance(trace, dict):
        total = trace.get("total_prompt_tokens_estimated")
        if isinstance(total, (int, float)) and total:
            estimated = int(total)
    return {
        "actual_available": actual_available,
        "estimated_prompt_tokens": estimated,
    }


def _evidence_completeness(base: Path, task_ids: list[str]) -> dict[str, bool]:
    def all_tasks_have(filename: str) -> bool:
        if not task_ids:
            return False
        return all((base / "task_runs" / tid / filename).exists() for tid in task_ids)

    scratch = (base / "scratch_file_guard.json").exists() or all_tasks_have(
        "scratch_file_guard.json"
    )
    return {
        "review_scope_packet": all_tasks_have("review_scope_packet.json"),
        "spec_compliance_check": all_tasks_have("spec_compliance_check.json"),
        "missing_tests_gate": all_tasks_have("missing_tests_gate.json"),
        "scratch_file_guard": scratch,
        "token_truth": (base / "token_truth.json").exists(),
        "safe_diff": all_tasks_have("safe.diff"),
        "review_json": all_tasks_have("review.json"),
        "tests_txt": all_tasks_have("tests.txt"),
    }


def build_final_verifier_report(evidence_dir: str) -> dict[str, Any]:
    """Build a deterministic final verifier report from evidence artifacts."""
    base = Path(evidence_dir) if evidence_dir else Path(".")
    task_ids = _task_ids(base)

    review_scope_files, changed_line_ranges = _collect_changes(base, task_ids)
    authoritative_changed_files = _collect_authoritative_changed_files(base, task_ids)
    changed_files = authoritative_changed_files
    file_alignment = _file_set_alignment(base, authoritative_changed_files, review_scope_files)

    missing_tests_gate = _aggregate_gate(
        base, task_ids, "missing_tests_gate.json", "gate_status",
        {"PASS": 0, "NEEDS_TESTS": 2}, "PASS",
    )
    spec_compliance = _aggregate_gate(
        base, task_ids, "spec_compliance_check.json", "verdict",
        {"PASS": 0, "FAIL": 1, "BLOCKED": 2}, "PASS",
    )
    scratch_file_guard = _scratch_status(base, task_ids)

    fresh_evidence_gate = _read_gate_verdict(base, "fresh_evidence_gate.json")
    artifact_contract_gate = _read_gate_verdict(base, "artifact_contract_gate.json")
    runtime_integration_gate = _read_gate_verdict(base, "runtime_integration_gate.json")
    change_provenance = _read_gate_verdict(base, "change_provenance_gate.json")
    # commit_execution_gate is downstream — reads OUR verdict, so we don't read it
    # (avoids circular dependency). We expose it in output for informational use.
    commit_execution_gate = _read_gate_verdict(base, "commit_execution_gate.json")

    verification_tests = _read_json(base / "verification_tests.json")

    unresolved_findings = _collect_unresolved_findings(base, task_ids)
    test_status = _aggregate_test_status(base, task_ids)

    if (
        isinstance(verification_tests, dict)
        and verification_tests.get("exit_code") == 0
        and verification_tests.get("passed", 0) > 0
        and verification_tests.get("failed", 0) == 0
    ):
        test_status["ran"] = True
        test_status["passed"] += verification_tests["passed"]
        test_status["failed"] += verification_tests.get("failed", 0)

    token_status = _token_status(base, task_ids)

    evidence_completeness = _evidence_completeness(base, task_ids)
    missing_evidence = sorted(
        name for name, present in evidence_completeness.items() if not present
    )

    upstream_gate_verdicts = {
        "fresh_evidence_gate": fresh_evidence_gate,
        "artifact_contract_gate": artifact_contract_gate,
        "runtime_integration_gate": runtime_integration_gate,
        "change_provenance_gate": change_provenance,
    }
    any_core_gate_blocked = any(
        v == "BLOCKED" for v in upstream_gate_verdicts.values() if v
    )

    file_alignment_blocked = (
        file_alignment["file_set_alignment_status"] == "BLOCKED"
    )
    file_alignment_risky = (
        file_alignment["file_set_alignment_status"] == "PASS_WITH_RISKS"
    )
    gates_blocked = (
        scratch_file_guard == "BLOCKED"
        or spec_compliance == "BLOCKED"
        or any_core_gate_blocked
        or file_alignment_blocked
    )
    needs_repair = (
        bool(unresolved_findings)
        or spec_compliance == "FAIL"
        or test_status["failed"] > 0
    )

    tests_verified = (
        isinstance(verification_tests, dict)
        and verification_tests.get("exit_code") == 0
        and verification_tests.get("passed", 0) > 0
        and verification_tests.get("failed", 0) == 0
    )
    effective_missing_tests = missing_tests_gate
    if tests_verified and missing_tests_gate == "NEEDS_TESTS":
        effective_missing_tests = "PASS"

    if gates_blocked:
        verdict = "BLOCKED"
    elif effective_missing_tests == "NEEDS_TESTS":
        verdict = "NEEDS_TESTS"
    elif needs_repair:
        verdict = "NEEDS_REPAIR"
    elif missing_evidence or file_alignment_risky:
        verdict = "PASS_WITH_RISKS"
    else:
        verdict = "PASS"

    also_needs_repair = needs_repair and verdict == "NEEDS_TESTS"
    recommended_action = _RECOMMENDED_ACTION[verdict]
    if also_needs_repair:
        recommended_action += (
            " Open findings / failing tests are also present; resolve them too."
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "verdict": verdict,
        "also_needs_repair": also_needs_repair,
        "changed_files": changed_files,
        "changed_line_ranges": changed_line_ranges,
        "authoritative_changed_files": file_alignment["authoritative_changed_files"],
        "change_source_mismatches": file_alignment["change_source_mismatches"],
        "review_subject_uncovered_files": file_alignment["review_subject_uncovered_files"],
        "content_hash_mismatches": file_alignment["content_hash_mismatches"],
        "file_set_alignment_status": file_alignment["file_set_alignment_status"],
        "unresolved_findings": unresolved_findings,
        "test_status": test_status,
        "missing_tests_gate": missing_tests_gate,
        "scratch_file_guard": scratch_file_guard,
        "change_provenance": change_provenance,
        "change_provenance_gate": change_provenance,
        "fresh_evidence_gate": fresh_evidence_gate,
        "artifact_contract_gate": artifact_contract_gate,
        "runtime_integration_gate": runtime_integration_gate,
        "commit_execution_gate": commit_execution_gate,
        "spec_compliance": spec_compliance,
        "token_status": token_status,
        "evidence_completeness": evidence_completeness,
        "missing_evidence": missing_evidence,
        "recommended_action": recommended_action,
    }


def write_final_verifier_report(evidence_dir: str, written: dict[str, str]) -> None:
    """Build and write ``final_verifier_report.json`` to the evidence dir.

    No-op without an evidence dir. Registers the output path in ``written``.
    """
    if not evidence_dir:
        return

    report = build_final_verifier_report(evidence_dir)

    out_dir = Path(evidence_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "final_verifier_report.json"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    written["final_verifier_report.json"] = str(json_path)
