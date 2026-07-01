#!/usr/bin/env python3
"""Build a valid JSON review zip manifest.

Called by make_review_zip.sh. Produces always-valid JSON regardless of
git state, file paths, or evidence dir contents.

Usage:
    python3 scripts/build_review_manifest.py [--evidence-dir <path>] [--output <path>]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone


def _git(cmd: list[str]) -> str:
    try:
        r = subprocess.run(
            ["git"] + cmd,
            capture_output=True, text=True, timeout=10,
        )
        return r.stdout.strip().split("\n")[0] if r.returncode == 0 else "unknown"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return "unknown"


def _check(path: str) -> str:
    return "present" if os.path.isfile(path) else "absent"


def _dirty_files() -> list[str]:
    try:
        r = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode != 0:
            return []
        return [line.strip() for line in r.stdout.strip().split("\n")
                if line.strip()]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []


def _has_untracked_files() -> bool:
    try:
        r = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode != 0:
            return False
        return any(line.startswith("??") for line in r.stdout.strip().split("\n")
                   if line.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _has_commits() -> bool:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return r.returncode == 0 and len(r.stdout.strip()) >= 7
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _classify_review_subject(
    branch: str, commit: str, dirty: list[str],
    has_untracked: bool, has_commits_val: bool,
) -> dict:
    is_main = branch in ("main", "master")
    is_dirty = len(dirty) > 0

    if not has_commits_val:
        kind = "unknown"
        summary = "No commits — fresh git init or degraded metadata"
    elif is_main and not is_dirty:
        kind = "clean_commit"
        summary = f"Clean main at {commit[:12]}"
    elif is_main and is_dirty:
        kind = "dirty_working_tree"
        summary = f"Dirty working tree on main ({len(dirty)} changed file(s))"
    elif not is_main and not is_dirty:
        kind = "feature_branch"
        summary = f"Feature branch {branch} at {commit[:12]}"
    else:
        kind = "dirty_working_tree"
        summary = f"Dirty feature branch {branch} ({len(dirty)} changed file(s))"

    return {
        "kind": kind,
        "branch": branch,
        "commit": commit,
        "dirty_files": dirty,
        "dirty_file_count_total": len(dirty),
        "dirty_files_truncated": False,
        "has_untracked_files": has_untracked,
        "has_commits": has_commits_val,
        "degraded_metadata": not has_commits_val,
        "human_summary": summary,
    }


def _extract_review_state() -> dict:
    lr_path = ".agent/live_review.md"
    plan_path = ".agent/plan.md"

    verdict = "absent"
    open_findings: list[str] = []
    builder_handoff_present = False

    if os.path.isfile(lr_path):
        try:
            with open(lr_path) as f:
                full_content = f.read()
            blocks = re.split(r"\n---\n+(?=# Live Review)", full_content)
            content = blocks[0] if blocks else full_content

            verdict_match = re.search(
                r"##\s+Verdict\s+\(reviewer-owned\)\s*\n\s*\*?\*?([A-Z_]+)\*?\*?",
                content,
            )
            if verdict_match:
                verdict = verdict_match.group(1).strip("*").strip()
            elif "pending" in content[:500].lower():
                verdict = "PENDING"

            for m in re.finditer(
                r"###\s+(R-\d+)\s+.*?\n.*?(?=\n###|\n---|\Z)",
                content, re.DOTALL,
            ):
                block = m.group(0)
                finding_id = m.group(1)
                if "**Resolved" not in block and "resolved" not in block.lower()[:200]:
                    open_findings.append(finding_id)

            builder_handoff_present = "## Builder Handoff" in content
        except OSError:
            pass

    plan_step_range = ""
    plan_goal_present = False
    if os.path.isfile(plan_path):
        try:
            with open(plan_path) as f:
                plan_content = f.read()
            step_match = re.search(r"Steps?\s+(\d+\s*[-–]\s*\d+)", plan_content)
            if step_match:
                plan_step_range = step_match.group(1).replace("–", "-").strip()
            plan_goal_present = "## Goal" in plan_content
        except OSError:
            pass

    review_ready = (
        verdict == "PASS"
        and len(open_findings) == 0
        and builder_handoff_present
    )

    return {
        "latest_live_review_verdict": verdict,
        "open_findings": open_findings,
        "builder_handoff_present": builder_handoff_present,
        "review_ready": review_ready,
        "review_state_source": lr_path if os.path.isfile(lr_path) else "missing",
        "plan_step_range": plan_step_range,
        "plan_goal_present": plan_goal_present,
    }


def _scan_task_runs(evidence_dir: str) -> list[dict]:
    task_runs_dir = os.path.join(evidence_dir, "task_runs")
    if not os.path.isdir(task_runs_dir):
        return []
    result = []
    for entry in sorted(os.listdir(task_runs_dir)):
        task_path = os.path.join(task_runs_dir, entry)
        if not os.path.isdir(task_path):
            continue
        mrp_path = os.path.join(task_path, "manual_repair_provenance.json")
        is_manual = os.path.isfile(mrp_path)
        info: dict = {
            "task": entry,
            "prompt_trace": _check(os.path.join(task_path, "prompt_trace.jsonl")),
            "prompt_trace_summary": _check(os.path.join(task_path, "prompt_trace_summary.json")),
            "review": _check(os.path.join(task_path, "review.json")),
            "repair_loop": _check(os.path.join(task_path, "repair_loop.json")),
            "token_accounting": _check(os.path.join(task_path, "token_accounting.json")),
            "provider_evidence": _check(os.path.join(task_path, "provider_evidence.json")),
            "manual_repair_provenance": _check(mrp_path),
            "is_manual_repair": is_manual,
        }
        result.append(info)
    return result


def _read_job_id(evidence_dir: str) -> str:
    jf = os.path.join(evidence_dir, "job_flow.json")
    if not os.path.isfile(jf):
        return ""
    try:
        with open(jf) as f:
            data = json.load(f)
        return data.get("job_id", "")
    except (json.JSONDecodeError, OSError):
        return ""


def _read_final_audit(evidence_dir: str) -> dict:
    jf = os.path.join(evidence_dir, "job_flow.json")
    if not os.path.isfile(jf):
        return {}
    try:
        with open(jf) as f:
            data = json.load(f)
        return data.get("final_audit", {})
    except (json.JSONDecodeError, OSError):
        return {}


def _read_trace_sources(evidence_dir: str) -> list[str]:
    sf = os.path.join(evidence_dir, "agent_run_trace_summary.json")
    if not os.path.isfile(sf):
        return []
    try:
        with open(sf) as f:
            data = json.load(f)
        return data.get("trace_sources", [])
    except (json.JSONDecodeError, OSError):
        return []


REQUIRED_ROOT_ARTIFACTS = [
    "job_flow.json",
    "manifest.json",
    "agent_run_trace.jsonl",
    "agent_run_trace_summary.json",
    "prompt_trace_summary.json",
    "command_transcript.json",
]

REQUIRED_TASK_ARTIFACTS = [
    "prompt_trace.jsonl",
    "prompt_trace_summary.json",
    "review.json",
    "repair_loop.json",
    "token_accounting.json",
    "provider_evidence.json",
]

MANUAL_REPAIR_EXEMPT_ARTIFACTS = frozenset({
    "prompt_trace.jsonl",
    "prompt_trace_summary.json",
    "provider_evidence.json",
})


def _read_evidence_gate(evidence_dir: str, filename: str) -> dict:
    """Read a gate JSON from the evidence dir, or {} if absent."""
    path = os.path.join(evidence_dir, filename)
    if os.path.isfile(path):
        try:
            with open(path) as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _read_fresh_evidence_gate(evidence_dir: str) -> dict:
    return _read_evidence_gate(evidence_dir, "fresh_evidence_gate.json")


def _build_alignment(
    dirty_files: list[str], evidence_dir: str,
) -> dict:
    """Build review_subject/evidence alignment proof."""
    _EXCLUDE_DIRS = {
        "remedy-job-evidence", "__pycache__", ".git", ".agent",
        "node_modules", ".data", ".mypy_cache", ".pytest_cache",
        ".venv", "venv", "dist", "build", "egg-info",
    }
    _EXCLUDE_SUBS = (
        "remedy-review-", "remedy-job-evidence", "run_transcript",
        ".coverage", "htmlcov/",
    )
    _EXCLUDE_SUFFS = (
        ".pyc", ".pyo", ".egg", ".whl", ".zip", ".tar",
        ".gz", ".log", ".tmp",
    )

    def _is_source(raw: str) -> bool:
        path = raw.split()[-1] if raw.strip() else ""
        path = path.replace("\\", "/").strip()
        while path.startswith("./"):
            path = path[2:]
        if not path:
            return False
        parts = path.split("/")
        if any(p in _EXCLUDE_DIRS or p.lstrip(".") in _EXCLUDE_DIRS
               or p.endswith(".egg-info") for p in parts):
            return False
        if path.endswith(_EXCLUDE_SUFFS):
            return False
        if any(sub in path for sub in _EXCLUDE_SUBS):
            return False
        return True

    dirty_source_test = sorted({
        f.split()[-1] for f in dirty_files if _is_source(f)
    })

    cp_gate = _read_evidence_gate(evidence_dir, "change_provenance_gate.json")
    fv_report = _read_evidence_gate(evidence_dir, "final_verifier_report.json")
    ce_gate = _read_evidence_gate(evidence_dir, "commit_execution_gate.json")
    ac_gate = _read_evidence_gate(evidence_dir, "artifact_contract_gate.json")

    cp_covered = sorted(cp_gate.get("covered_files", []))
    fv_changed = sorted(fv_report.get("authoritative_changed_files", []))
    hash_mismatches = cp_gate.get("hash_mismatches", [])

    covered_set = set(cp_covered)
    fv_set = set(fv_changed)
    dirty_src_set = set(dirty_source_test)

    uncovered = sorted(dirty_src_set - covered_set)

    issues: list[str] = []
    if uncovered:
        issues.append(f"uncovered dirty source/test files: {uncovered}")
    if hash_mismatches:
        issues.append(
            f"content hash mismatches: {[m['file'] for m in hash_mismatches]}"
        )

    alignment_verdict = "PASS" if not issues else "BLOCKED"

    return {
        "dirty_file_count_total": len(dirty_files),
        "dirty_source_test_files": dirty_source_test,
        "intended_commit_files": fv_changed or cp_covered,
        "change_provenance_covered_files": cp_covered,
        "final_verifier_changed_files": fv_changed,
        "uncovered_source_test_files": uncovered,
        "hash_mismatches": hash_mismatches,
        "gate_verdicts": {
            "change_provenance_gate": cp_gate.get("verdict", ""),
            "final_verifier": fv_report.get("verdict", ""),
            "commit_execution_gate": ce_gate.get("verdict", ""),
            "artifact_contract_gate": ac_gate.get("verdict", ""),
        },
        "issues": issues,
        "verdict": alignment_verdict,
    }


def validate_evidence_candidate(evidence_dir: str) -> dict:
    errors: list[str] = []
    missing_root: list[str] = []
    missing_task: dict[str, list[str]] = {}

    for art in REQUIRED_ROOT_ARTIFACTS:
        if not os.path.isfile(os.path.join(evidence_dir, art)):
            missing_root.append(art)
            errors.append(f"missing root artifact: {art}")

    jf_path = os.path.join(evidence_dir, "job_flow.json")
    job_id = ""
    final_audit_status = ""
    missing_obs: list[str] = []
    target_mutation_detected = False

    if os.path.isfile(jf_path):
        try:
            with open(jf_path) as f:
                jf_data = json.load(f)
            job_id = jf_data.get("job_id", "")
            if not job_id:
                errors.append("job_flow.json: job_id is empty")
            audit = jf_data.get("final_audit", {})
            final_audit_status = audit.get("status", "")
            if not final_audit_status:
                errors.append("job_flow.json: final_audit.status missing")
            missing_obs = audit.get("missing_observability_artifacts", [])
            if missing_obs:
                errors.append(
                    f"final_audit.missing_observability_artifacts: {missing_obs}"
                )
            tg = jf_data.get("target_guard", {})
            if tg.get("mutated_target", False):
                target_mutation_detected = True
                errors.append("target_guard indicates target mutation")
        except (json.JSONDecodeError, OSError) as exc:
            errors.append(f"job_flow.json: parse error: {exc}")

    task_runs_dir = os.path.join(evidence_dir, "task_runs")
    task_run_count = 0
    manual_repair_tasks: list[str] = []
    if os.path.isdir(task_runs_dir):
        for entry in sorted(os.listdir(task_runs_dir)):
            task_path = os.path.join(task_runs_dir, entry)
            if not os.path.isdir(task_path):
                continue
            task_run_count += 1
            mrp_path = os.path.join(task_path, "manual_repair_provenance.json")
            is_manual_repair = os.path.isfile(mrp_path)
            if is_manual_repair:
                try:
                    with open(mrp_path) as f:
                        mrp = json.load(f)
                    if not (isinstance(mrp, dict) and mrp.get("manual_operator_repair") is True
                            and mrp.get("no_provider_calls") is True):
                        is_manual_repair = False
                        errors.append(
                            f"task_runs/{entry}: manual_repair_provenance.json invalid"
                        )
                except (json.JSONDecodeError, OSError):
                    is_manual_repair = False
                    errors.append(
                        f"task_runs/{entry}: manual_repair_provenance.json unreadable"
                    )
            if is_manual_repair:
                manual_repair_tasks.append(entry)
            task_missing = []
            for art in REQUIRED_TASK_ARTIFACTS:
                if is_manual_repair and art in MANUAL_REPAIR_EXEMPT_ARTIFACTS:
                    continue
                if not os.path.isfile(os.path.join(task_path, art)):
                    task_missing.append(art)
            if task_missing:
                missing_task[entry] = task_missing
                errors.append(
                    f"task_runs/{entry}: missing {task_missing}"
                )
    else:
        errors.append("no task_runs/ directory")

    if task_run_count == 0:
        errors.append("no task runs found")

    is_valid = len(errors) == 0

    return {
        "is_valid_current_run": is_valid,
        "validation_errors": errors,
        "required_root_artifacts": {
            art: "present" if art not in missing_root else "absent"
            for art in REQUIRED_ROOT_ARTIFACTS
        },
        "required_task_artifacts": missing_task,
        "task_run_count": task_run_count,
        "manual_repair_tasks": manual_repair_tasks,
        "job_id": job_id,
        "final_audit_status": final_audit_status,
        "missing_observability_artifacts": missing_obs,
        "target_mutation_detected": target_mutation_detected,
    }


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _check_bundle_integrity(
    evidence_dir: str | None,
    source_root: str,
) -> dict:
    result: dict = {
        "current_content_hash_checked": False,
        "current_content_hash_mismatches": [],
        "current_content_hash_missing_proofs": [],
        "packaged_file_hashes": {},
        "verdict": "PASS",
    }

    if not evidence_dir or not os.path.isdir(evidence_dir):
        return result

    proof_path = os.path.join(
        evidence_dir, "current_change_content_proof.json"
    )
    if not os.path.isfile(proof_path):
        return result

    try:
        proof = json.loads(open(proof_path).read())
    except (json.JSONDecodeError, OSError):
        return result

    file_hashes = proof.get("file_hashes", {})
    if not file_hashes:
        return result

    result["current_content_hash_checked"] = True
    mismatches = []
    missing_proofs = []
    packaged_hashes = {}

    for rel_path, expected_hash in file_hashes.items():
        abs_path = os.path.join(source_root, rel_path)
        if not os.path.isfile(abs_path):
            missing_proofs.append(rel_path)
            continue
        actual_hash = _sha256_file(abs_path)
        packaged_hashes[rel_path] = actual_hash
        if actual_hash != expected_hash:
            mismatches.append({
                "file": rel_path,
                "expected": expected_hash,
                "actual": actual_hash,
            })

    result["current_content_hash_mismatches"] = mismatches
    result["current_content_hash_missing_proofs"] = missing_proofs
    result["packaged_file_hashes"] = packaged_hashes

    if mismatches or missing_proofs:
        result["verdict"] = "BLOCKED"

    return result


def build_manifest(
    evidence_dir: str | None = None,
    selection_mode: str = "",
    selection_reason: str = "",
    candidate_count: int = 0,
    selected_mtime: str = "",
    rejected_candidate_count: int = 0,
) -> dict:
    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"])
    commit = _git(["rev-parse", "HEAD"])
    has_commits_val = _has_commits()
    dirty = _dirty_files()
    has_untracked = _has_untracked_files()

    review_subject = _classify_review_subject(
        branch, commit, dirty, has_untracked, has_commits_val,
    )

    root_artifacts = {
        "job_flow.json": "absent_no_evidence_dir",
        "agent_run_trace.jsonl": "absent_no_evidence_dir",
        "agent_run_trace_summary.json": "absent_no_evidence_dir",
        "prompt_trace_summary.json": "absent_no_evidence_dir",
        "manifest.json": "absent_no_evidence_dir",
        "command_transcript.json": "absent_no_evidence_dir",
    }
    task_runs: list[dict] = []
    current_evidence: dict = {}

    if evidence_dir and os.path.isdir(evidence_dir):
        for artifact_name in root_artifacts:
            root_artifacts[artifact_name] = _check(
                os.path.join(evidence_dir, artifact_name)
            )
        task_runs = _scan_task_runs(evidence_dir)
        job_id = _read_job_id(evidence_dir)
        audit = _read_final_audit(evidence_dir)
        trace_sources = _read_trace_sources(evidence_dir)

        validation = validate_evidence_candidate(evidence_dir)

        fresh_gate = _read_fresh_evidence_gate(evidence_dir)
        freshness_ok = bool(
            fresh_gate.get("evidence_freshness", {}).get("is_fresh", False)
        )
        validity_ok = validation["is_valid_current_run"]

        current_evidence = {
            "job_id": job_id,
            "evidence_freshness": {
                "is_fresh": freshness_ok,
                "evidence_validity": {"is_valid_current_run": validity_ok},
                "evidence_authoritative": freshness_ok and validity_ok,
            },
            "zip_prefix": "evidence/current",
            "validation": {
                "is_valid_current_run": validation["is_valid_current_run"],
                "validation_errors": validation["validation_errors"],
                "required_root_artifacts": validation[
                    "required_root_artifacts"
                ],
                "required_task_artifacts": validation[
                    "required_task_artifacts"
                ],
                "manual_repair_tasks": validation.get(
                    "manual_repair_tasks", []
                ),
                "selected_candidate_status": (
                    "valid" if validation["is_valid_current_run"]
                    else "incomplete"
                ),
                "selection_mode": selection_mode or "unknown",
                "selection_reason": selection_reason or "unknown",
                "selected_from_candidate_count": candidate_count,
                "rejected_candidate_count": rejected_candidate_count,
            },
            "selection_mode": selection_mode or "unknown",
            "selection_reason": selection_reason or "unknown",
            "selected_from_candidate_count": candidate_count,
            "selected_modified_time": selected_mtime or "",
            "root_artifacts": root_artifacts,
            "task_runs": task_runs,
            "trace_sources": trace_sources,
            "final_audit_status": audit.get("status", "unknown"),
            "missing_observability_artifacts": audit.get(
                "missing_observability_artifacts", []
            ),
        }

    review_state = _extract_review_state()

    alignment: dict | None = None
    if evidence_dir and os.path.isdir(evidence_dir):
        alignment = _build_alignment(dirty, evidence_dir)
        if alignment["verdict"] == "BLOCKED" and current_evidence:
            current_evidence["evidence_freshness"]["evidence_authoritative"] = False

    # Source-root containment check
    source_root = _git(["rev-parse", "--show-toplevel"]).strip()
    cwd = os.getcwd()
    containment_blockers: list[str] = []
    external_paths: list[str] = []

    cwd_resolved = os.path.realpath(cwd)
    root_resolved = os.path.realpath(source_root)

    if not cwd_resolved.startswith(root_resolved):
        containment_blockers.append(
            f"packaging cwd {cwd} is outside source_root {source_root}"
        )
        external_paths.append(cwd)

    if evidence_dir:
        ev_resolved = os.path.realpath(evidence_dir)
        if not ev_resolved.startswith(root_resolved):
            containment_blockers.append(
                f"evidence_dir {evidence_dir} is outside source_root"
            )
            external_paths.append(ev_resolved)

    containment_ok = len(containment_blockers) == 0
    containment_verdict = "PASS" if containment_ok else "BLOCKED"

    # Determine package status
    packaging_warnings: list[str] = []
    evidence_valid = bool(
        current_evidence
        and current_evidence.get("evidence_freshness", {}).get(
            "evidence_authoritative", False
        )
    )
    alignment_ok = alignment and alignment.get("verdict") != "BLOCKED"

    if not current_evidence:
        packaging_warnings.append("no evidence directory provided or found")
    if current_evidence and not evidence_valid:
        packaging_warnings.append("evidence is not authoritative")
    if alignment and not alignment_ok:
        packaging_warnings.append("review subject/evidence alignment is BLOCKED")
    if not containment_ok:
        packaging_warnings.extend(containment_blockers)

    package_status = (
        "READY_FOR_REVIEW"
        if (evidence_valid and alignment_ok and containment_ok)
        else "BLOCKED_EVIDENCE"
    )

    # Packaging proof — record what was actually packaged
    ev_manifest_task_count = 0
    ev_manifest_task_ids: list[str] = []
    ev_manifest_job_id = ""
    ev_manifest_mtime = ""
    if evidence_dir and os.path.isdir(evidence_dir):
        ev_mf_path = os.path.join(evidence_dir, "manifest.json")
        if os.path.isfile(ev_mf_path):
            try:
                ev_mf = json.loads(open(ev_mf_path).read())
                ev_manifest_task_count = ev_mf.get("task_count", 0)
                ev_manifest_task_ids = ev_mf.get("task_ids", [])
                ev_manifest_job_id = ev_mf.get("job_id", "")
                ev_manifest_mtime = datetime.fromtimestamp(
                    os.path.getmtime(ev_mf_path), tz=timezone.utc
                ).strftime("%Y-%m-%dT%H:%M:%SZ")
            except (json.JSONDecodeError, OSError):
                packaging_warnings.append(
                    "evidence manifest.json unreadable"
                )

    # Review-bundle integrity: compare packaged files against content proof
    bundle_integrity = _check_bundle_integrity(evidence_dir, source_root)
    if bundle_integrity["verdict"] == "BLOCKED":
        packaging_warnings.append("review bundle content hash mismatch or missing proofs")
        package_status = "BLOCKED_EVIDENCE"

    manifest = {
        "bundle_kind": "remedy_review_zip",
        "bundle_version": 12,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "review_package_created": True,
        "package_status": package_status,
        "review_subject": review_subject,
        "review_state": review_state,
        "review_subject_evidence_alignment": alignment,
        "packaged_evidence_dir": (
            os.path.abspath(evidence_dir) if evidence_dir else ""
        ),
        "packaged_evidence_job_id": ev_manifest_job_id,
        "packaged_evidence_manifest_task_count": ev_manifest_task_count,
        "packaged_evidence_manifest_task_ids": ev_manifest_task_ids,
        "packaged_evidence_modified_at": ev_manifest_mtime,
        "source_root": source_root,
        "packaging_command_context": {
            "cwd": os.getcwd(),
            "evidence_dir_arg": evidence_dir or "",
        },
        "source_root_containment": {
            "verdict": containment_verdict,
            "blockers": containment_blockers,
        },
        "external_paths_detected": external_paths,
        "review_bundle_integrity": bundle_integrity,
        "packaging_warnings": packaging_warnings,
        "policy": (
            "Current-run evidence under evidence/current/. "
            "Stale evidence dirs excluded by default. "
            "Excludes .git, .data, node_modules, caches, build outputs, "
            "env files, private keys, logs, old archives."
        ),
        "agent_state": {
            ".agent/live_review.md": _check(".agent/live_review.md"),
            ".agent/plan.md": _check(".agent/plan.md"),
            ".agent/review_protocol.md": _check(".agent/review_protocol.md"),
        },
        "current_evidence": current_evidence if current_evidence else None,
    }
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build review zip manifest")
    parser.add_argument("--evidence-dir", default=None)
    parser.add_argument("--selection-mode", default="")
    parser.add_argument("--selection-reason", default="")
    parser.add_argument("--candidate-count", type=int, default=0)
    parser.add_argument("--rejected-candidate-count", type=int, default=0)
    parser.add_argument("--selected-mtime", default="")
    parser.add_argument("--output", default=".review_zip_manifest.json")
    args = parser.parse_args()

    manifest = build_manifest(
        args.evidence_dir,
        selection_mode=args.selection_mode,
        selection_reason=args.selection_reason,
        candidate_count=args.candidate_count,
        selected_mtime=args.selected_mtime,
        rejected_candidate_count=args.rejected_candidate_count,
    )
    out = json.dumps(manifest, indent=2) + "\n"

    if args.output == "-":
        sys.stdout.write(out)
    else:
        with open(args.output, "w") as f:
            f.write(out)


if __name__ == "__main__":
    main()
