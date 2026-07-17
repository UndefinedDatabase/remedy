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

# Shared canonical provenance-hash implementation — the validator and the
# attestation writer MUST use the same code so they cannot drift apart.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)
try:
    from packages.orchestration.repair_attest import (
        build_safe_diff_text as _canon_safe_diff_text,
        canonical_provenance_sha256 as _canon_provenance_sha256,
        parse_safe_diff_paths as _canon_parse_safe_diff_paths,
        sha256_text as _canon_sha256_text,
    )
    _CANON_AVAILABLE = True
except Exception:  # pragma: no cover - defensive; canonical impl must exist
    _CANON_AVAILABLE = False


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


SOURCE_ROOT_TOKEN = "[source_root]"
EXTERNAL_EVIDENCE_TOKEN = "[external_evidence]"


def _shareable_path(path: str, source_root: str) -> str:
    """Render a filesystem path so it carries no machine-specific root.

    The review manifest is shared with external reviewers, so it must never
    disclose ``/home/<user>``, ``/Users/<user>``, ``/tmp/...`` or any other
    private absolute prefix. Paths inside the repository become
    ``[source_root]/<relative>``; anything outside collapses to its basename
    under ``[external_evidence]``.
    """
    if not path:
        return ""
    root = os.path.realpath(source_root) if source_root else ""
    resolved = os.path.realpath(path)
    if root and (resolved == root):
        return SOURCE_ROOT_TOKEN
    if root and resolved.startswith(root + os.sep):
        rel = os.path.relpath(resolved, root).replace(os.sep, "/")
        return f"{SOURCE_ROOT_TOKEN}/{rel}"
    return f"{EXTERNAL_EVIDENCE_TOKEN}/{os.path.basename(resolved.rstrip(os.sep))}"


def _dirty_files() -> list[str]:
    # ``-u`` lists untracked files individually. Without it git collapses an
    # untracked directory to ``dir/``, which can never match a covered file and
    # would wrongly report the whole directory as uncovered.
    try:
        r = subprocess.run(
            ["git", "status", "--porcelain", "-u"],
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


def _load_json(path: str) -> dict:
    if not os.path.isfile(path):
        return {}
    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def _read_job_id(evidence_dir: str) -> str:
    """Job ID from provider-flow evidence, else from the bundle manifest.

    ``job_flow.json`` is intentionally absent for an operator-attested manual
    completion, so falling back to ``manifest.json`` is what keeps the shared
    manifest from reporting an empty Job ID for a perfectly valid bundle.
    """
    jf = _load_json(os.path.join(evidence_dir, "job_flow.json"))
    job_id = str(jf.get("job_id") or "")
    if job_id:
        return job_id
    mf = _load_json(os.path.join(evidence_dir, "manifest.json"))
    job_id = str(mf.get("job_id") or "")
    if job_id:
        return job_id
    fjr = _load_json(os.path.join(evidence_dir, "final_job_review.json"))
    return str(fjr.get("job_id") or "")


def _read_final_audit(evidence_dir: str) -> dict:
    """Final audit from provider-flow evidence, else the manual-completion verdict.

    No provider observability artifact is fabricated: for a manual completion the
    status comes from the verifier/review artifacts that actually exist.
    """
    jf = _load_json(os.path.join(evidence_dir, "job_flow.json"))
    audit = jf.get("final_audit")
    if isinstance(audit, dict) and audit:
        return audit

    fv = _load_json(os.path.join(evidence_dir, "final_verifier_report.json"))
    status = str(fv.get("verdict") or "")
    source = "final_verifier_report.json"
    if not status:
        fjr = _load_json(os.path.join(evidence_dir, "final_job_review.json"))
        status = str(fjr.get("verdict") or "")
        source = "final_job_review.json"
    if not status:
        return {}
    return {
        "status": status,
        "source": source,
        "missing_observability_artifacts": [],
    }


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
    "repair_loop.json",
})

# Provider-flow-only root artifacts that a deterministic manual-only completion
# legitimately does not produce. They are marked not-applicable — never
# fabricated — when a valid operator-attested completion contract is present.
MANUAL_COMPLETION_EXEMPT_ROOT_ARTIFACTS = frozenset({
    "job_flow.json",
    "agent_run_trace.jsonl",
    "agent_run_trace_summary.json",
    "command_transcript.json",
})


def _mc_read_json(evidence_dir: str, rel: str) -> dict:
    """Read a JSON object from the evidence dir, or {} if absent/invalid."""
    path = os.path.join(evidence_dir, rel)
    if not os.path.isfile(path):
        return {}
    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def _mc_task_dirs(evidence_dir: str) -> list[str]:
    task_runs_dir = os.path.join(evidence_dir, "task_runs")
    if not os.path.isdir(task_runs_dir):
        return []
    return [
        e for e in sorted(os.listdir(task_runs_dir))
        if os.path.isdir(os.path.join(task_runs_dir, e))
    ]


def _mc_norm(p: str) -> str:
    p = str(p or "").replace("\\", "/").strip()
    while p.startswith("./"):
        p = p[2:]
    if p.startswith(("a/", "b/")):
        p = p[2:]
    return p


def _is_sha256(v) -> bool:
    return isinstance(v, str) and len(v) == 64 and all(c in "0123456789abcdef" for c in v.lower())


def _all_task_runs_manual(evidence_dir: str) -> bool:
    """True when every task_run has a valid manual_repair_provenance."""
    task_dirs = _mc_task_dirs(evidence_dir)
    if not task_dirs:
        return False
    for entry in task_dirs:
        mrp = _mc_read_json(evidence_dir, os.path.join("task_runs", entry, "manual_repair_provenance.json"))
        if not (mrp.get("manual_operator_repair") is True and mrp.get("no_provider_calls") is True):
            return False
    return True


def _is_manual_completion(evidence_dir: str) -> bool:
    """A manual-only completion candidate: the final job review declares the
    manual completion mode AND every task run carries manual provenance. No
    bespoke root artifact — detection rides existing artifacts only."""
    fjr = _mc_read_json(evidence_dir, "final_job_review.json")
    if fjr.get("completion_mode") != "manual_operator_repair":
        return False
    return _all_task_runs_manual(evidence_dir)


def _verify_commit_chain(evidence_dir: str, per_task_union: set) -> list:
    """Round 15 (F7): the packaged commit history is recomputed, not narrated.

    The operator's handoff used to say "there were six commits" in prose. A reader could not check
    that, could not tell whether an unrelated commit had been swept in, and could not tell whether
    the packaged history actually ends at the reviewed HEAD. So the chain is an artifact, and this
    recomputes it from the repository and holds the artifact to it.
    """
    errors: list = []
    chain = _mc_read_json(evidence_dir, "review_commit_chain.json")
    subject = _mc_read_json(evidence_dir, "review_subject.json")
    if not chain and not subject:
        return errors                     # no declared base: the legacy dirty-tree subject
    base = str(chain.get("base_commit") or "")
    head = str(chain.get("head_commit") or "")
    if not base:
        return errors                     # nothing was declared; nothing to verify

    if subject:
        if str(subject.get("base_commit") or "") != base:
            errors.append("review_commit_chain base_commit disagrees with review_subject")
        if str(subject.get("head_commit") or "") != head:
            errors.append("review_commit_chain head_commit disagrees with review_subject")
        if subject.get("base_is_ancestor") is not True:
            errors.append("review_subject does not record the base as an ancestor of HEAD")

    try:
        from packages.orchestration.review_subject import resolve_commit_chain
        actual = resolve_commit_chain(".", base, head)
    except Exception as exc:                       # unreadable repo/base: say so, never assume
        errors.append(f"cannot recompute the commit chain: {str(exc)[:160]}")
        return errors

    recorded = chain.get("commits") or []
    if len(recorded) != len(actual):
        errors.append(
            f"review_commit_chain records {len(recorded)} commit(s); the repository's "
            f"{base[:12]}..{head[:12]} ancestry path has {len(actual)}")
        return errors
    for rec, act in zip(recorded, actual):
        for field in ("commit", "tree", "patch_sha256"):
            if str(rec.get(field) or "") != getattr(act, field):
                errors.append(
                    f"review_commit_chain commit {str(rec.get('commit'))[:12]} {field} does not "
                    f"match the repository")
        if [str(x) for x in (rec.get("parents") or [])] != list(act.parents):
            errors.append(
                f"review_commit_chain commit {act.commit[:12]} parents do not match")
    if actual and actual[-1].commit != head:
        errors.append("the packaged commit chain does not end at the review head")
    if actual and base not in actual[0].parents:
        errors.append("the packaged commit chain does not start after the declared base")

    # Every file the commits touched must be part of the reviewed subject — no commit may carry
    # work the review does not account for.
    union_committed = {_mc_norm(f) for c in actual for f in c.changed_files}
    from packages.orchestration.final_verifier import _is_source_for_alignment
    stray = sorted({f for f in union_committed
                    if _is_source_for_alignment(f)} - {_mc_norm(f) for f in per_task_union})
    if stray:
        errors.append(
            f"the packaged commits change source files the review does not account for: {stray}")
    return errors


def _verify_task_provenance_integrity(
    evidence_dir: str, tid: str, mrp: dict, proof: dict, fjr: dict,
) -> list[str]:
    """Finding 1: recompute and verify every provenance hash for one task.

    Nothing is trusted at face value: the safe.diff content is re-hashed, the
    provenance and tracked-diff hashes are recomputed from the recorded inputs
    via the SHARED canonical implementation, the safe.diff paths must match every
    changed-file view, and each untracked entry is cross-checked against the
    current content proof.
    """
    errors: list[str] = []
    if not _CANON_AVAILABLE:
        return [f"{tid}: canonical provenance-hash implementation unavailable"]

    safe_diff_path = os.path.join(evidence_dir, "task_runs", tid, "safe.diff")
    try:
        with open(safe_diff_path, encoding="utf-8") as f:
            safe_content = f.read()
    except OSError:
        return [f"{tid}: safe.diff unreadable"]

    # 8: empty / whitespace-only safe.diff is rejected.
    if not safe_content.strip():
        errors.append(f"{tid}: safe.diff is empty")

    untracked = mrp.get("untracked_file_hashes") or []
    tracked_sha = str(mrp.get("tracked_diff_sha256") or "")

    # 1: the emitted safe.diff must hash to the recorded safe_diff_sha256.
    actual_safe_sha = _canon_sha256_text(safe_content)
    if actual_safe_sha != str(mrp.get("safe_diff_sha256") or ""):
        errors.append(f"{tid}: safe_diff_sha256 mismatch (safe.diff modified)")

    # 4/2: provenance hash recomputed from tracked-diff hash + untracked entries.
    recomputed_prov = _canon_provenance_sha256(tracked_sha, untracked)
    if recomputed_prov != str(mrp.get("provenance_sha256") or ""):
        errors.append(f"{tid}: provenance_sha256 does not match recomputed value")
    if recomputed_prov != str(mrp.get("diff_sha256") or ""):
        errors.append(f"{tid}: diff_sha256 does not match recomputed provenance")

    # 2: tracked_diff_sha256 must equal the hash of the tracked portion of
    #    safe.diff (safe.diff = tracked_diff + untracked headers).
    suffix = _canon_safe_diff_text("", untracked)
    if suffix and safe_content.endswith(suffix):
        tracked_portion = safe_content[: len(safe_content) - len(suffix)]
    elif not suffix:
        tracked_portion = safe_content
    else:
        tracked_portion = None
        errors.append(f"{tid}: safe.diff untracked headers do not match provenance")
    if tracked_portion is not None:
        if _canon_sha256_text(tracked_portion) != tracked_sha:
            errors.append(f"{tid}: tracked_diff_sha256 does not match safe.diff content")

    # 5/6: exact path equality across every changed-file view.
    diff_paths = set(_canon_parse_safe_diff_paths(safe_content))
    changed = {_mc_norm(f) for f in (mrp.get("changed_files") or [])}
    scoped = {_mc_norm(f) for f in (mrp.get("task_scoped_files") or [])}
    rsp = _mc_read_json(evidence_dir, os.path.join("task_runs", tid, "review_scope_packet.json"))
    rsp_files = {_mc_norm(f) for f in (rsp.get("changed_files") or [])}
    fjr_task = {_mc_norm(f) for f in ((fjr.get("per_task_changed_files") or {}).get(tid) or [])}
    diff_paths_n = {_mc_norm(f) for f in diff_paths}
    for label, s in (
        ("provenance.changed_files", changed),
        ("provenance.task_scoped_files", scoped),
        ("review_scope.changed_files", rsp_files),
        ("final_job_review.per_task_changed_files", fjr_task),
    ):
        if s != diff_paths_n:
            errors.append(
                f"{tid}: safe.diff paths != {label} "
                f"(only_in_diff={sorted(diff_paths_n - s)} only_in_view={sorted(s - diff_paths_n)})"
            )

    # 7: each untracked entry — unique path, valid sha matching the content
    #    proof, non-negative size, path within the task changed set.
    proof_hashes = proof.get("file_hashes") or {}
    proof_norm = {_mc_norm(k): v for k, v in proof_hashes.items()}
    seen_paths: set[str] = set()
    for uf in untracked:
        p = _mc_norm(uf.get("path", ""))
        sha = uf.get("sha256", "")
        size = uf.get("size_bytes", -1)
        if p in seen_paths:
            errors.append(f"{tid}: untracked path {p!r} appears more than once")
        seen_paths.add(p)
        if not _is_sha256(sha):
            errors.append(f"{tid}: untracked {p!r} has an invalid sha256")
        elif p in proof_norm and proof_norm[p] != sha:
            errors.append(f"{tid}: untracked {p!r} sha256 disagrees with content proof")
        if not isinstance(size, int) or size < 0:
            errors.append(f"{tid}: untracked {p!r} has a negative/invalid size")
        if p not in changed:
            errors.append(f"{tid}: untracked {p!r} is not in the task changed set")

    return errors


def validate_manual_completion(evidence_dir: str) -> list[str]:
    """Strictly and independently validate a manual-only completion candidate.

    Returns a list of human-readable errors; empty means authoritative. Every
    condition below is checked independently so any single tampering (a flag, a
    call count, a task id, a changed-file set, the changed-file union, a root
    test exit code / failure count, a content-proof hash, the job id, a
    provenance hash, or task overlap) invalidates the candidate.
    """
    errors: list[str] = []
    manifest = _mc_read_json(evidence_dir, "manifest.json")
    fjr = _mc_read_json(evidence_dir, "final_job_review.json")
    proof = _mc_read_json(evidence_dir, "current_change_content_proof.json")
    fv = _mc_read_json(evidence_dir, "final_verifier_report.json")
    cp = _mc_read_json(evidence_dir, "change_provenance_gate.json")
    vt = _mc_read_json(evidence_dir, "verification_tests.json")

    package_job_id = str(manifest.get("job_id") or "")
    planned_task_ids = [str(t) for t in (manifest.get("task_ids") or [])]
    task_dirs = _mc_task_dirs(evidence_dir)

    # 14 + planned-task coverage: package job id must equal the completion job id
    # and every planned task must have exactly one task run.
    fjr_job_id = str(fjr.get("job_id") or "")
    if not package_job_id:
        errors.append("manifest.json: job_id is empty")
    if fjr_job_id != package_job_id:
        errors.append(f"job_id mismatch: manifest={package_job_id!r} final_job_review={fjr_job_id!r}")
    if planned_task_ids and sorted(task_dirs) != sorted(planned_task_ids):
        errors.append(f"task runs {sorted(task_dirs)} != planned tasks {sorted(planned_task_ids)}")

    # completion facts on the existing final job review
    if fjr.get("completion_mode") != "manual_operator_repair":
        errors.append("final_job_review.completion_mode != manual_operator_repair")
    if fjr.get("human_final_reviewer_required") is not True:
        errors.append("final_job_review.human_final_reviewer_required is not true")
    if fjr.get("completion_provider_call_count", -1) != 0:
        errors.append("final_job_review.completion_provider_call_count != 0")

    # Finding 7: the linked prior-job summaries must match the linked ids exactly
    # (an honest historical record, never a fabricated call count).
    linked_ids = [str(x) for x in (fjr.get("linked_prior_job_ids") or [])]
    summaries = fjr.get("linked_prior_job_summaries") or []
    summary_ids = [str(s.get("job_id")) for s in summaries if isinstance(s, dict)]
    if sorted(summary_ids) != sorted(linked_ids):
        errors.append(
            f"linked_prior_job_summaries ids {sorted(summary_ids)} != "
            f"linked_prior_job_ids {sorted(linked_ids)}"
        )
    for s in summaries:
        if not isinstance(s, dict):
            continue
        # provider_call_count may be null (unknown) but must be present.
        if "provider_call_count" not in s:
            errors.append(f"linked job {s.get('job_id')!r} summary missing provider_call_count")
        if not s.get("status"):
            errors.append(f"linked job {s.get('job_id')!r} summary missing status")

    # per-task attestation validity + union of changed files
    per_task_union: set[str] = set()
    overlap_owner: dict[str, str] = {}
    for tid in task_dirs:
        rv = _mc_read_json(evidence_dir, os.path.join("task_runs", tid, "review.json"))
        pe = _mc_read_json(evidence_dir, os.path.join("task_runs", tid, "provider_evidence.json"))
        mrp = _mc_read_json(evidence_dir, os.path.join("task_runs", tid, "manual_repair_provenance.json"))
        safe_diff = os.path.join(evidence_dir, "task_runs", tid, "safe.diff")

        if str(rv.get("final_verdict") or rv.get("verdict") or "") != "operator_attested":
            errors.append(f"{tid}: review verdict is not operator_attested")
        if rv.get("human_final_reviewer_required") is not True:
            errors.append(f"{tid}: review.human_final_reviewer_required is not true")

        if pe.get("execution_mode") != "manual_operator_repair":
            errors.append(f"{tid}: provider_evidence.execution_mode != manual_operator_repair")
        if pe.get("provider_call_count", -1) != 0:
            errors.append(f"{tid}: provider_evidence.provider_call_count != 0")
        if pe.get("actual_provider_available") is True:
            errors.append(f"{tid}: provider_evidence claims provider availability (provider-backed PASS)")

        if mrp.get("manual_operator_repair") is not True:
            errors.append(f"{tid}: provenance manual_operator_repair is not true")
        if mrp.get("no_provider_calls") is not True:
            errors.append(f"{tid}: provenance no_provider_calls is not true")
        if str(mrp.get("job_id") or "") != package_job_id:
            errors.append(f"{tid}: provenance job_id != package job id")
        if str(mrp.get("task_id") or "") != tid:
            errors.append(f"{tid}: provenance task_id mismatch")
        if not str(mrp.get("note") or "").strip():
            errors.append(f"{tid}: provenance note is empty")
        for hf in ("provenance_sha256", "diff_sha256", "tracked_diff_sha256"):
            if not _is_sha256(mrp.get(hf)):
                errors.append(f"{tid}: provenance {hf} is not a valid sha256")
        if not os.path.isfile(safe_diff):
            errors.append(f"{tid}: safe.diff missing")

        changed = [_mc_norm(f) for f in (mrp.get("changed_files") or [])]
        if not changed:
            errors.append(f"{tid}: provenance changed_files is empty")
        for f in changed:
            if f in overlap_owner:
                errors.append(f"file {f!r} owned by both {overlap_owner[f]} and {tid} (overlap)")
            else:
                overlap_owner[f] = tid
            per_task_union.add(f)

        # ---- Finding 1: actually RECOMPUTE and verify every provenance hash,
        #      the safe.diff content, its paths, and the untracked entries. ----
        errors.extend(_verify_task_provenance_integrity(evidence_dir, tid, mrp, proof, fjr))

        # ---- Finding 5: a task manifest may not claim evidence unavailable
        #      without an explicit effective operator-attested completion state.
        tm = _mc_read_json(evidence_dir, os.path.join("task_runs", tid, "manifest.json"))
        if (tm.get("evidence_available") is not True
                and tm.get("effective_status") != "operator_attested_complete"):
            errors.append(
                f"{tid}: task manifest shows evidence unavailable without an "
                "effective operator-attested completion state"
            )

    # 7: union must exactly equal every authoritative changed-file view.
    fjr_actual = {_mc_norm(f) for f in (fjr.get("actual_changed_files") or [])}
    fjr_expected = {_mc_norm(f) for f in (fjr.get("expected_changed_files") or [])}
    # Round 15 (F4): a DELETED path is proven by its tombstone (its base_sha256), not by a
    # current hash it cannot have. Counting only file_hashes would report a real, proven
    # part of the change as an uncovered file.
    proof_files = {_mc_norm(f) for f in (proof.get("file_hashes") or {})}
    proof_files |= {_mc_norm(f) for f in (proof.get("tombstones") or {})}
    fv_auth = {_mc_norm(f) for f in (fv.get("authoritative_changed_files") or [])}
    cp_covered = {_mc_norm(f) for f in (cp.get("covered_files") or [])}
    for label, s in (
        ("final_job_review.actual_changed_files", fjr_actual),
        ("final_job_review.expected_changed_files", fjr_expected),
        ("current_change_content_proof.file_hashes", proof_files),
        ("final_verifier.authoritative_changed_files", fv_auth),
        ("change_provenance.covered_files", cp_covered),
    ):
        if s != per_task_union:
            errors.append(
                f"changed-file union mismatch vs {label}: "
                f"only_in_union={sorted(per_task_union - s)} only_in_{label.split('.')[0]}={sorted(s - per_task_union)}"
            )

    # 7b: the packaged commit chain is recomputed and verified against the review subject.
    errors.extend(_verify_commit_chain(evidence_dir, per_task_union))

    # 8: root verification must exist, exit 0, >=1 passed, 0 failed.
    if not vt:
        errors.append("verification_tests.json missing")
    else:
        if vt.get("exit_code", -1) != 0:
            errors.append(f"root verification exit_code != 0 ({vt.get('exit_code')})")
        if int(vt.get("passed", 0) or 0) < 1:
            errors.append("root verification passed < 1")
        if int(vt.get("failed", 0) or 0) != 0:
            errors.append(f"root verification failed != 0 ({vt.get('failed')})")

    # 9-12: alignment / uncovered / hash mismatches / missing proofs (final verifier + gates).
    if fv.get("file_set_alignment_status") not in ("PASS", "PASS_WITH_RISKS"):
        errors.append(f"file_set_alignment_status={fv.get('file_set_alignment_status')}")
    if fv.get("review_subject_uncovered_files"):
        errors.append(f"uncovered files: {fv.get('review_subject_uncovered_files')}")
    if fv.get("content_hash_mismatches"):
        errors.append(f"final verifier content hash mismatches: {fv.get('content_hash_mismatches')}")
    if cp.get("hash_mismatches"):
        errors.append(f"change provenance hash mismatches: {cp.get('hash_mismatches')}")
    if cp.get("uncovered_files"):
        errors.append(f"change provenance uncovered files: {cp.get('uncovered_files')}")
    if not proof_files:
        errors.append("current_change_content_proof.json has no file hashes (missing proofs)")

    return errors


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
        ".coverage", "htmlcov/", ".review_zip_manifest",
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

    manual_completion = _is_manual_completion(evidence_dir)
    manual_completion_errors: list[str] = []
    not_applicable_root: list[str] = []

    if manual_completion:
        # Strict, independent validation of the manual-completion contract.
        # Any mismatch invalidates the candidate and blocks authoritativeness.
        manual_completion_errors = validate_manual_completion(evidence_dir)
        errors.extend(manual_completion_errors)

    for art in REQUIRED_ROOT_ARTIFACTS:
        if os.path.isfile(os.path.join(evidence_dir, art)):
            continue
        if manual_completion and art in MANUAL_COMPLETION_EXEMPT_ROOT_ARTIFACTS:
            # A deterministic manual-only completion legitimately has no
            # provider-flow root artifact — mark not-applicable, never missing.
            not_applicable_root.append(art)
            continue
        missing_root.append(art)
        errors.append(f"missing root artifact: {art}")

    jf_path = os.path.join(evidence_dir, "job_flow.json")
    job_id = ""
    final_audit_status = ""
    missing_obs: list[str] = []
    target_mutation_detected = False

    if manual_completion and not os.path.isfile(jf_path):
        # Derive identity/verdict from the existing final job review + final
        # verifier, without fabricating a provider job_flow.json.
        fjr = _mc_read_json(evidence_dir, "final_job_review.json")
        manifest_obj = _mc_read_json(evidence_dir, "manifest.json")
        job_id = str(fjr.get("job_id") or manifest_obj.get("job_id") or "")
        if not job_id:
            errors.append("manual completion: job_id could not be derived")
        fv = _read_evidence_gate(evidence_dir, "final_verifier_report.json")
        final_audit_status = str(fv.get("verdict", "") or "")
        if not final_audit_status:
            errors.append("final_verifier_report.json: verdict missing")

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

    def _root_status(art: str) -> str:
        if art in not_applicable_root:
            return "not_applicable_manual_completion"
        return "present" if art not in missing_root else "absent"

    is_valid = len(errors) == 0

    return {
        "is_valid_current_run": is_valid,
        "validation_errors": errors,
        "manual_completion": manual_completion,
        "manual_completion_errors": manual_completion_errors,
        "not_applicable_root_artifacts": not_applicable_root,
        "required_root_artifacts": {
            art: _root_status(art) for art in REQUIRED_ROOT_ARTIFACTS
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
            f"packaging cwd {_shareable_path(cwd, source_root)} is outside source_root"
        )
        external_paths.append(_shareable_path(cwd, source_root))

    if evidence_dir:
        ev_resolved = os.path.realpath(evidence_dir)
        if not ev_resolved.startswith(root_resolved):
            containment_blockers.append(
                f"evidence_dir {_shareable_path(ev_resolved, source_root)} "
                "is outside source_root"
            )
            external_paths.append(_shareable_path(ev_resolved, source_root))

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

    if evidence_valid and alignment_ok and containment_ok:
        package_status = "READY_FOR_REVIEW"
    elif not current_evidence:
        package_status = "NO_EVIDENCE"
    else:
        package_status = "BLOCKED_EVIDENCE"

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
    elif (
        package_status == "READY_FOR_REVIEW"
        and not bundle_integrity.get("current_content_hash_checked", False)
    ):
        # Evidence passed other checks but content hashes were not verified
        # (no proof file or no file_hashes). Mark as unverified so reviewers
        # know integrity was not confirmed.
        package_status = "READY_FOR_REVIEW_UNVERIFIED"
        packaging_warnings.append(
            "content hash verification was not performed; integrity unconfirmed"
        )

    _subject = _mc_read_json(evidence_dir, "review_subject.json") if evidence_dir else {}
    _chain = _mc_read_json(evidence_dir, "review_commit_chain.json") if evidence_dir else {}
    _proof_doc = _mc_read_json(evidence_dir, "current_change_content_proof.json") \
        if evidence_dir else {}

    manifest = {
        "bundle_kind": "remedy_review_zip",
        "bundle_version": 13,
        # Round 15: which base this is a review OF, and the machine-verifiable history that got
        # from there to HEAD. A deleted path is packaged as a TOMBSTONE — the ZIP cannot carry a
        # file that no longer exists, and pretending otherwise would be a missing-proof error for
        # a real, proven part of the change.
        #
        # Deliberately NOT named `review_subject`: that key already exists below with an older,
        # different meaning (branch/kind/dirty summary), and silently redefining it would break
        # every existing reader of that field.
        "committed_review_subject": {
            "base_commit": str(_subject.get("base_commit") or ""),
            "head_commit": str(_subject.get("head_commit") or ""),
            "base_is_ancestor": bool(_subject.get("base_is_ancestor") or False),
            "commit_count": len(_chain.get("commits") or []),
            "file_count": len(_subject.get("files") or []),
            "tombstones": sorted(_proof_doc.get("tombstones") or {}),
        },
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "review_package_created": True,
        "package_status": package_status,
        "review_subject": review_subject,
        "review_state": review_state,
        "review_subject_evidence_alignment": alignment,
        "packaged_evidence_dir": (
            _shareable_path(evidence_dir, source_root) if evidence_dir else ""
        ),
        "packaged_evidence_job_id": ev_manifest_job_id,
        "packaged_evidence_manifest_task_count": ev_manifest_task_count,
        "packaged_evidence_manifest_task_ids": ev_manifest_task_ids,
        "packaged_evidence_modified_at": ev_manifest_mtime,
        "source_root": SOURCE_ROOT_TOKEN,
        "packaging_command_context": {
            "cwd": _shareable_path(cwd, source_root),
            "evidence_dir_arg": (
                _shareable_path(evidence_dir, source_root) if evidence_dir else ""
            ),
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
