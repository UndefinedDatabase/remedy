#!/usr/bin/env python3
"""Build a valid JSON review zip manifest.

Called by make_review_zip.sh. Produces always-valid JSON regardless of
git state, file paths, or evidence dir contents.

Usage:
    python3 scripts/build_review_manifest.py [--evidence-dir <path>] [--output <path>]
"""
from __future__ import annotations

import argparse
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
                if line.strip()][:20]
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
        result.append({
            "task": entry,
            "prompt_trace": _check(os.path.join(task_path, "prompt_trace.jsonl")),
            "prompt_trace_summary": _check(os.path.join(task_path, "prompt_trace_summary.json")),
            "review": _check(os.path.join(task_path, "review.json")),
            "repair_loop": _check(os.path.join(task_path, "repair_loop.json")),
            "token_accounting": _check(os.path.join(task_path, "token_accounting.json")),
            "provider_evidence": _check(os.path.join(task_path, "provider_evidence.json")),
        })
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
    if os.path.isdir(task_runs_dir):
        for entry in sorted(os.listdir(task_runs_dir)):
            task_path = os.path.join(task_runs_dir, entry)
            if not os.path.isdir(task_path):
                continue
            task_run_count += 1
            task_missing = []
            for art in REQUIRED_TASK_ARTIFACTS:
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
        "job_id": job_id,
        "final_audit_status": final_audit_status,
        "missing_observability_artifacts": missing_obs,
        "target_mutation_detected": target_mutation_detected,
    }


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

        current_evidence = {
            "job_id": job_id,
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

    manifest = {
        "bundle_kind": "remedy_review_zip",
        "bundle_version": 9,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "review_subject": review_subject,
        "review_state": review_state,
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
