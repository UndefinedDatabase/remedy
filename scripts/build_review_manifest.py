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


def _has_commits() -> bool:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return r.returncode == 0 and len(r.stdout.strip()) >= 7
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


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


def build_manifest(evidence_dir: str | None = None) -> dict:
    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"])
    commit = _git(["rev-parse", "HEAD"])
    has_commits = _has_commits()

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

        current_evidence = {
            "job_id": job_id,
            "zip_prefix": "evidence/current",
            "root_artifacts": root_artifacts,
            "task_runs": task_runs,
            "trace_sources": trace_sources,
            "final_audit_status": audit.get("status", "unknown"),
            "missing_observability_artifacts": audit.get(
                "missing_observability_artifacts", []
            ),
        }

    manifest = {
        "bundle_kind": "remedy_review_zip",
        "bundle_version": 7,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "git": {
            "branch": branch,
            "commit": commit,
            "has_commits": has_commits,
            "dirty_files": _dirty_files(),
            "degraded_metadata": not has_commits,
        },
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
    parser.add_argument("--output", default=".review_zip_manifest.json")
    args = parser.parse_args()

    manifest = build_manifest(args.evidence_dir)
    out = json.dumps(manifest, indent=2) + "\n"

    if args.output == "-":
        sys.stdout.write(out)
    else:
        with open(args.output, "w") as f:
            f.write(out)


if __name__ == "__main__":
    main()
