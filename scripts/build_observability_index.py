#!/usr/bin/env python3
"""Build ``self_run_observability_index.json`` from an evidence directory.

The index answers, in one place, what happened during a self-run:

- Which tasks were generated?              (job_flow.json)
- Which worker/reviewer prompts were sent?  (task_runs/*/prompt_trace.jsonl — summary only)
- Which findings were opened / rechecked?   (task_runs/*/review.json, repair_loop.json)
- Which repair prompt followed each finding? (task_runs/*/prompt_trace.jsonl, repair_loop.json)
- Which artifacts changed?                  (job_flow.json final_audit / agent_run_trace_summary.json)
- Which tests ran?                          (command_transcript.json / job_flow.json final_audit)
- How many estimated/actual tokens used?    (task_runs/*/token_accounting.json)
- Where are the relevant evidence files?    (relative paths only)
- What was the final audit status?          (job_flow.json)
- What is the agent-run timeline?           (agent_run_trace_summary.json)
- What is the next safe human action?

Safety guarantees:
- Only safe, relative artifact references are emitted (never absolute local paths).
- Absolute paths in any file list are dropped, not emitted.
- No raw secrets, raw full prompts, raw stdout/stderr, or full diffs are copied.
  Prompts are reduced to metadata summaries (kind, round, sha256, token estimate).
- Missing data is explicitly marked ``"absent"`` rather than fabricated.
- Works on partial/incomplete evidence directories, including skipped tasks.

Usage:
    python3 scripts/build_observability_index.py --evidence-dir <path> [--output <path>]

The default output is ``<evidence-dir>/self_run_observability_index.json``.
Pass ``--output -`` to write the index to stdout.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

ABSENT = "absent"

# Root-level evidence artifacts we reference (relative paths only).
ROOT_ARTIFACTS = [
    "job_flow.json",
    "manifest.json",
    "agent_run_trace.jsonl",
    "agent_run_trace_summary.json",
    "prompt_trace_summary.json",
    "command_transcript.json",
    "tasks.json",
    "job_report.json",
    "job_timeline.json",
]

# Per-task evidence artifacts we reference (relative to task_runs/<task>/).
TASK_ARTIFACTS = [
    "prompt_trace.jsonl",
    "prompt_trace_summary.json",
    "review.json",
    "repair_loop.json",
    "token_accounting.json",
    "provider_evidence.json",
    "summary.md",
    "tests.txt",
]


def _load_json(path: str):
    """Load JSON, returning (data, status). status is 'present', 'absent', or 'unreadable'."""
    if not os.path.isfile(path):
        return None, ABSENT
    try:
        with open(path) as f:
            return json.load(f), "present"
    except (json.JSONDecodeError, OSError, ValueError):
        return None, "unreadable"


def _load_jsonl(path: str):
    """Load JSONL, returning (rows, status)."""
    if not os.path.isfile(path):
        return [], ABSENT
    rows = []
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return rows, "present"
    except OSError:
        return [], "unreadable"


def _artifact_ref(rel_path: str, evidence_dir: str) -> str:
    """Return the relative ref if the file exists under evidence_dir, else ABSENT."""
    if evidence_dir and os.path.isfile(os.path.join(evidence_dir, rel_path)):
        return rel_path
    return ABSENT


def _safe_rel_paths(paths) -> list:
    """Keep only safe relative paths.

    Drops absolute paths and parent-traversal refs so no local filesystem
    layout leaks into the index. Non-string entries are ignored.
    """
    safe: list = []
    for p in paths or []:
        if not isinstance(p, str) or not p:
            continue
        if os.path.isabs(p) or p.startswith("~"):
            continue
        if ".." in p.split("/") or ".." in p.split(os.sep):
            continue
        safe.append(p)
    return safe


def _summarise_prompt(entry: dict) -> dict:
    """Reduce a prompt_trace.jsonl entry to safe metadata (no raw prompt text)."""
    return {
        "round": entry.get("round"),
        "role": entry.get("role", ABSENT),
        "prompt_kind": entry.get("prompt_kind", ABSENT),
        "provider": entry.get("provider", ABSENT),
        "prompt_sha256": entry.get("prompt_sha256", ABSENT),
        "prompt_chars": entry.get("prompt_chars"),
        "prompt_tokens_estimated": entry.get("prompt_tokens_estimated"),
        "context_categories": entry.get("context_categories", []),
        "changed_files": _safe_rel_paths(entry.get("changed_files")),
    }


def _build_task_section(task_id: str, evidence_dir: str, job_task: dict) -> dict:
    """Build one observability section for a single task."""
    job_task = job_task or {}
    task_dir = os.path.join(evidence_dir, "task_runs", task_id)
    rel_task_dir = os.path.join("task_runs", task_id)

    # --- Evidence file references (relative, present/absent) ---
    evidence_refs = {
        name: _artifact_ref(os.path.join(rel_task_dir, name), evidence_dir)
        for name in TASK_ARTIFACTS
    }

    # --- Prompts (summary only — never raw prompt text) ---
    prompt_rows, prompt_status = _load_jsonl(
        os.path.join(task_dir, "prompt_trace.jsonl")
    )
    worker_prompts = [
        _summarise_prompt(r) for r in prompt_rows if r.get("role") == "builder"
    ]
    reviewer_prompts = [
        _summarise_prompt(r) for r in prompt_rows if r.get("role") == "reviewer"
    ]
    repair_prompts = [
        _summarise_prompt(r)
        for r in prompt_rows
        if r.get("prompt_kind") == "repair"
    ]

    # --- Findings opened + rechecked (from review.json) ---
    review, review_status = _load_json(os.path.join(task_dir, "review.json"))
    findings_opened: list = []
    findings_rechecked: list = []
    final_reviewer_verdict = ABSENT
    if review_status == "present" and isinstance(review, dict):
        final_reviewer_verdict = review.get("final_verdict", ABSENT)
        for rv in review.get("reviews", []):
            rnd = rv.get("round")
            kind = rv.get("kind", "")
            for finding in rv.get("findings", []):
                rec = {
                    "id": finding.get("id", ABSENT),
                    "severity": finding.get("severity", ABSENT),
                    "file": finding.get("file", ABSENT),
                    "summary": finding.get("summary", ABSENT),
                    "round": rnd,
                }
                # A finding raised in a repair/re-review round is also a recheck.
                if kind in ("repair", "re-review"):
                    findings_rechecked.append(rec)
                else:
                    findings_opened.append(rec)

    # --- Repair loop (which repair followed each finding, recheck outcome) ---
    repair, repair_status = _load_json(os.path.join(task_dir, "repair_loop.json"))
    repair_section: dict
    repair_to_finding: list = []
    if repair_status == "present" and isinstance(repair, dict):
        repair_section = {
            "status": repair.get("status", ABSENT),
            "enabled": repair.get("enabled"),
            "rounds_used": repair.get("repair_rounds_used"),
            "rounds_allowed": repair.get("repair_rounds_allowed"),
            "open_findings": repair.get("open_findings", []),
            "resolved_findings": repair.get("resolved_findings", []),
            "final_reviewer_verdict": repair.get("final_reviewer_verdict", ABSENT),
            "decisions": [
                {
                    "round": d.get("round"),
                    "reviewer_verdict": d.get("reviewer_verdict", ABSENT),
                    "repair_decision": d.get("repair_decision", ABSENT),
                    "reason": d.get("reason", ABSENT),
                    "finding_count": d.get("finding_count"),
                }
                for d in repair.get("decisions", [])
            ],
            "finding_status_map": repair.get("finding_status_map", []),
        }
        # Findings rechecked per the repair-loop finding_status_map.
        for entry in repair.get("finding_status_map", []):
            findings_rechecked.append(
                {
                    "id": entry.get("prior_finding_id", ABSENT),
                    "status": entry.get("status", ABSENT),
                    "evidence_round": entry.get("evidence_round"),
                    "source": "repair_loop",
                }
            )
        # Map each repair prompt to the findings it was meant to resolve. The
        # repair prompt for round N addresses findings recorded for round N-1.
        prior_findings = [f for f in findings_opened]
        for rp in repair_prompts:
            rnd = rp.get("round")
            addressed = [
                f.get("id")
                for f in prior_findings
                if rnd is None or f.get("round") in (None, (rnd - 1) if isinstance(rnd, int) else None)
            ]
            repair_to_finding.append(
                {
                    "repair_round": rnd,
                    "prompt_sha256": rp.get("prompt_sha256", ABSENT),
                    "prompt_kind": rp.get("prompt_kind", ABSENT),
                    "addresses_findings": addressed or ABSENT,
                }
            )
    else:
        repair_section = {"status": repair_status}

    # --- Tokens (from token_accounting.json) ---
    tokens, tokens_status = _load_json(
        os.path.join(task_dir, "token_accounting.json")
    )
    if tokens_status == "present" and isinstance(tokens, dict):
        token_section = {
            "kind": tokens.get("kind", ABSENT),
            "actual_tokens_available": tokens.get("actual_tokens_available", False),
            "builder_prompt_tokens_estimated": tokens.get(
                "builder_prompt_tokens_estimated"
            ),
            "reviewer_prompt_tokens_estimated": tokens.get(
                "reviewer_prompt_tokens_estimated"
            ),
            "repair_prompt_tokens_estimated": tokens.get(
                "repair_prompt_tokens_estimated"
            ),
            "task_tokens_estimated": tokens.get("task_tokens_estimated"),
            "note": tokens.get("token_note", ""),
        }
    else:
        token_section = {"status": tokens_status}

    # --- Changed files (from the job_flow task record; safe relative paths) ---
    changed_files = _safe_rel_paths(job_task.get("safe_diff_files"))
    if not changed_files:
        apply_manifest = job_task.get("apply_manifest") or {}
        changed_files = _safe_rel_paths(apply_manifest.get("applied_files"))

    # --- Tests (per-task; command_transcript is the canonical source) ---
    test_passed = job_task.get("test_passed")
    test_section = {
        "test_passed": test_passed,
        "result": "not_run" if test_passed is None else (
            "passed" if test_passed else "failed"
        ),
        "source": _artifact_ref(
            os.path.join(rel_task_dir, "tests.txt"), evidence_dir
        ),
    }

    return {
        "task_id": task_id,
        "title": job_task.get("title", ABSENT),
        "status": job_task.get("status", ABSENT),
        "final_status": job_task.get("final_status", ABSENT),
        "reviewer_verdict": job_task.get("reviewer_verdict", final_reviewer_verdict),
        "run_id": job_task.get("run_id", ABSENT),
        "prompts": {
            "status": prompt_status,
            "worker_prompts": worker_prompts,
            "reviewer_prompts": reviewer_prompts,
            "repair_prompts": repair_prompts,
        },
        "findings_opened": findings_opened or ABSENT,
        "findings_rechecked": findings_rechecked or ABSENT,
        "repair_loop": repair_section,
        "repair_to_finding_map": repair_to_finding or ABSENT,
        "changed_files": changed_files or ABSENT,
        "tests": test_section,
        "tokens": token_section,
        "evidence_refs": evidence_refs,
    }


def _build_timeline_summary(evidence_dir: str, dir_present: bool) -> dict:
    """Summarise the agent-run timeline from agent_run_trace_summary.json."""
    summary, status = (
        _load_json(os.path.join(evidence_dir, "agent_run_trace_summary.json"))
        if dir_present
        else (None, ABSENT)
    )
    if status != "present" or not isinstance(summary, dict):
        return {
            "status": status,
            "source": _artifact_ref("agent_run_trace_summary.json", evidence_dir),
        }
    return {
        "status": "present",
        "total_events": summary.get("total_events"),
        "event_counts": summary.get("event_counts", {}),
        "tasks_traced": summary.get("tasks_traced", []),
        "providers": summary.get("providers", []),
        "max_round": summary.get("max_round"),
        "has_builder_events": summary.get("has_builder_events"),
        "has_reviewer_events": summary.get("has_reviewer_events"),
        "has_repair_events": summary.get("has_repair_events"),
        "has_final_audit": summary.get("has_final_audit"),
        "source": _artifact_ref("agent_run_trace_summary.json", evidence_dir),
    }


def build_observability_index(evidence_dir: str) -> dict:
    """Build the observability index dict for ``evidence_dir``.

    Always returns a valid dict, even when the directory is missing or evidence
    is incomplete. Missing inputs are marked ``"absent"`` rather than invented.
    """
    evidence_name = (
        os.path.basename(os.path.normpath(evidence_dir)) if evidence_dir else ""
    )
    dir_present = bool(evidence_dir) and os.path.isdir(evidence_dir)

    job_flow, job_flow_status = (
        _load_json(os.path.join(evidence_dir, "job_flow.json"))
        if dir_present
        else (None, ABSENT)
    )
    report = (job_flow or {}).get("report", {}) if isinstance(job_flow, dict) else {}
    final_audit = (
        (job_flow or {}).get("final_audit", {}) if isinstance(job_flow, dict) else {}
    )

    # Job-level task records keyed by task_id (source: job_flow.report.tasks).
    job_tasks = {
        t.get("task_id"): t
        for t in report.get("tasks", [])
        if isinstance(t, dict) and t.get("task_id")
    }

    # Tasks generated: prefer job_flow tasks; fall back to scanning task_runs/.
    task_ids = list(job_tasks.keys())
    task_runs_dir = os.path.join(evidence_dir, "task_runs") if dir_present else ""
    if dir_present and os.path.isdir(task_runs_dir):
        for entry in sorted(os.listdir(task_runs_dir)):
            if (
                os.path.isdir(os.path.join(task_runs_dir, entry))
                and entry not in task_ids
            ):
                task_ids.append(entry)
    task_ids = sorted(set(task_ids))

    tasks = [
        _build_task_section(tid, evidence_dir, job_tasks.get(tid, {}))
        for tid in task_ids
    ]

    # Job-level token rollup (sum of per-task estimates).
    total_estimated = 0
    any_actual = False
    for t in tasks:
        tok = t.get("tokens", {})
        for key in (
            "builder_prompt_tokens_estimated",
            "reviewer_prompt_tokens_estimated",
            "repair_prompt_tokens_estimated",
        ):
            val = tok.get(key)
            if isinstance(val, (int, float)):
                total_estimated += val
        if tok.get("actual_tokens_available"):
            any_actual = True

    # Changed artifacts at the job level (safe relative paths).
    trace_summary, _ = (
        _load_json(os.path.join(evidence_dir, "agent_run_trace_summary.json"))
        if dir_present
        else (None, ABSENT)
    )
    job_changed_files = _safe_rel_paths(final_audit.get("changed_files"))
    if not job_changed_files and isinstance(trace_summary, dict):
        job_changed_files = _safe_rel_paths(trace_summary.get("changed_files"))

    # Audit + next action.
    audit_status = final_audit.get("status", ABSENT) if final_audit else ABSENT
    next_action = ABSENT
    if final_audit:
        next_action = final_audit.get("recommended_next_action") or ABSENT
    if next_action == ABSENT and report.get("next_command"):
        next_action = report.get("next_command")

    # Data availability map (root artifacts, relative refs).
    data_availability = {
        name: _artifact_ref(name, evidence_dir) if dir_present else ABSENT
        for name in ROOT_ARTIFACTS
    }

    return {
        "index_kind": "self_run_observability_index",
        "index_version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "evidence_dir": evidence_name or ABSENT,
        "evidence_dir_present": dir_present,
        "job_id": report.get("job_id") or (job_flow or {}).get("job_id") or ABSENT,
        "job_title": report.get("job_title", ABSENT),
        "tasks_generated": task_ids or ABSENT,
        "tasks": tasks,
        "timeline_summary": _build_timeline_summary(evidence_dir, dir_present),
        "tokens": {
            "actual_tokens_available": any_actual,
            "total_prompt_tokens_estimated": total_estimated,
            "note": (
                "Estimated token counts only; provider did not expose actuals."
                if not any_actual
                else "Includes provider-reported actual token counts."
            ),
        },
        "changed_artifacts": job_changed_files or ABSENT,
        "tests": {
            "summary": final_audit.get("test_summary", ABSENT)
            if final_audit
            else ABSENT,
            "source": _artifact_ref("command_transcript.json", evidence_dir)
            if dir_present
            else ABSENT,
        },
        "audit": {
            "status": audit_status,
            "promote_ready": final_audit.get("promote_ready") if final_audit else ABSENT,
            "human_decision_required": final_audit.get("human_decision_required")
            if final_audit
            else ABSENT,
            "missing_observability_artifacts": final_audit.get(
                "missing_observability_artifacts", []
            )
            if final_audit
            else ABSENT,
            "known_limitations": final_audit.get("known_limitations", [])
            if final_audit
            else [],
            "source": _artifact_ref("job_flow.json", evidence_dir)
            if dir_present
            else ABSENT,
        },
        "next_action": next_action,
        "data_availability": data_availability,
    }


def write_observability_index(
    evidence_dir: str, output_path: str | None = None
) -> str:
    """Build and write the index. Returns the path written to."""
    index = build_observability_index(evidence_dir)
    if output_path is None:
        output_path = os.path.join(
            evidence_dir, "self_run_observability_index.json"
        )
    with open(output_path, "w") as f:
        f.write(json.dumps(index, indent=2) + "\n")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build self_run_observability_index.json from an evidence dir"
    )
    parser.add_argument("--evidence-dir", required=True)
    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Output path ('-' for stdout). "
            "Default: <evidence-dir>/self_run_observability_index.json"
        ),
    )
    args = parser.parse_args()

    if args.output == "-":
        index = build_observability_index(args.evidence_dir)
        sys.stdout.write(json.dumps(index, indent=2) + "\n")
        return

    path = write_observability_index(args.evidence_dir, args.output)
    sys.stderr.write(f"Wrote {path}\n")


if __name__ == "__main__":
    main()
