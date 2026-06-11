"""
Review Bundle v1 — safe state package for reviewers.

Generates a zip file containing safe summaries only:
manifest, job summary, proof chains, event summary, trust report,
context inspection, changed files, repair summary, command summary,
and a readme.

No raw artifact bodies. No raw diffs. No raw source files.
No stdout/stderr. No secrets. No .env. No __pycache__.

Public API::

    build_review_bundle(job_id, output_path=None) -> ReviewBundleResult
    export_review_bundle_json(result) -> dict
    summarize_review_bundle(result) -> str
"""

from __future__ import annotations

import json
import re
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID


BUNDLE_VERSION = 1

REQUIRED_SECTIONS = (
    "manifest.json",
    "job_summary.json",
    "proof_chains.json",
    "event_summary.json",
    "trust_report.json",
    "context_inspection.json",
    "changed_files_safe.json",
    "repair_summary.json",
    "command_summary.json",
    "progress_ledger.json",
    "integrity_summary.json",
    "bundle_readme.md",
)

_UNSAFE_PATTERNS = frozenset({
    "__pycache__", ".pyc", ".pyo", ".env", ".data",
    "node_modules", "dist", "build", ".cache", ".git",
    "secrets", "credentials", "token",
})

_PROTECTED_OUTPUT_DIRS = frozenset({
    ".git", ".env", "node_modules", "__pycache__",
    ".venv", "venv", "dist", "build", ".cache",
})


# ---------------------------------------------------------------------------
# Models (Step 977)
# ---------------------------------------------------------------------------


@dataclass
class ReviewBundleSection:
    """One section in the review bundle."""

    filename: str
    status: str = "included"
    error: str = ""
    byte_count: int = 0


@dataclass
class BundleSafetyReport:
    """Safety check results for the bundle."""

    has_raw_artifacts: bool = False
    has_raw_diffs: bool = False
    has_raw_output: bool = False
    has_secrets: bool = False
    has_pycache: bool = False
    has_env_files: bool = False
    warnings: list[str] = field(default_factory=list)

    @property
    def is_safe(self) -> bool:
        return not any([
            self.has_raw_artifacts,
            self.has_raw_diffs,
            self.has_raw_output,
            self.has_secrets,
            self.has_pycache,
            self.has_env_files,
        ])


@dataclass
class ChangedFileSafe:
    """Safe representation of a changed file."""

    path: str = ""
    status: str = "unknown"
    proof_status: str = ""
    related_task_id: str = ""
    related_intent_id: str = ""
    tested_after_change: bool = False
    safety_flags: list[str] = field(default_factory=list)


@dataclass
class ReviewBundleManifest:
    """Bundle manifest."""

    bundle_version: int = BUNDLE_VERSION
    job_id: str = ""
    generated_at: str = ""
    included_sections: list[str] = field(default_factory=list)
    skipped_sections: list[str] = field(default_factory=list)
    safety_warnings: list[str] = field(default_factory=list)


@dataclass
class ReviewBundleResult:
    """Result of building a review bundle."""

    job_id: str = ""
    output_path: str = ""
    bundle_version: int = BUNDLE_VERSION
    generated_at: str = ""
    sections: list[ReviewBundleSection] = field(default_factory=list)
    safety: BundleSafetyReport = field(default_factory=BundleSafetyReport)
    file_count: int = 0
    byte_count: int = 0
    error: str = ""


# ---------------------------------------------------------------------------
# Text redaction (Step 997)
# ---------------------------------------------------------------------------


_PROTECTED_PATH_RE = re.compile(
    r"(?:^|[\s\"'/,;:(\[{])"
    r"("
    r"(?:[a-zA-Z0-9_./-]*/)?"                       # optional directory prefix
    r"(?:\.env(?:\.[a-zA-Z0-9_.-]+)?)"               # .env, .env.secret, .env.local, etc.
    r"|(?:[a-zA-Z0-9_./-]*/)?credentials\.json"      # credentials.json
    r"|(?:[a-zA-Z0-9_./-]*/)?service-account\.json"  # service-account.json
    r"|(?:[a-zA-Z0-9_./-]*/)?secrets\.ya?ml"         # secrets.yaml/yml
    r"|(?:[a-zA-Z0-9_./-]*/)?id_(?:rsa|ed25519|ecdsa)" # SSH keys
    r")"
)


def redact_safe_text(text: str, max_len: int = 200) -> tuple[str, int]:
    """Redact secrets and protected paths from text and bound length.

    Returns (redacted_text, redaction_count).
    """
    from packages.orchestration.redaction_patterns import _SECRET_RE

    redaction_count = 0

    def _replace(m: "re.Match[str]") -> str:
        nonlocal redaction_count
        redaction_count += 1
        return "[REDACTED]"

    result = _SECRET_RE.sub(_replace, text)

    def _replace_path(m: "re.Match[str]") -> str:
        nonlocal redaction_count
        full = m.group(0)
        path_part = m.group(1)
        prefix = full[: full.index(path_part[0])] if path_part else ""
        redaction_count += 1
        return prefix + "[PROTECTED_PATH]"

    result = _PROTECTED_PATH_RE.sub(_replace_path, result)

    if len(result) > max_len:
        result = result[:max_len] + "..."
        redaction_count += 1

    return result, redaction_count


def _is_protected_path(path: str) -> bool:
    """Check if path is protected — reuses context inspector policy."""
    from packages.orchestration.context_inspector import (
        _PROTECTED_EXACT,
        _PROTECTED_PREFIXES,
        _PROTECTED_DIRS,
        _SECRET_NAMES,
    )
    p = Path(path)
    name = p.name
    if name in _PROTECTED_EXACT:
        return True
    if any(name.startswith(pf) for pf in _PROTECTED_PREFIXES):
        return True
    if name in _SECRET_NAMES:
        return True
    for part in p.parts:
        if part in _PROTECTED_DIRS:
            return True
    return False


# ---------------------------------------------------------------------------
# Path safety (Step 1000)
# ---------------------------------------------------------------------------


def _is_safe_output_path(path: str) -> bool:
    """Reject traversal and protected output destinations. Segment-based."""
    p = Path(path)
    for part in p.parts:
        if part == "..":
            return False
        if part in _PROTECTED_OUTPUT_DIRS:
            return False
        if part.startswith(".env"):
            return False
    return True


def _default_output_path(job_id: str, data_dir: Path) -> Path:
    """Default bundle output path."""
    bundles_dir = data_dir / "review_bundles"
    bundles_dir.mkdir(parents=True, exist_ok=True)
    return bundles_dir / f"{job_id[:8]}-review-bundle.zip"


# ---------------------------------------------------------------------------
# Section builders (Steps 978-983)
# ---------------------------------------------------------------------------


def _build_job_summary(job: Any) -> dict:
    """Safe job summary — no raw content, no raw prompt."""
    tasks_summary = []
    for t in job.tasks:
        safe_desc, _ = redact_safe_text(t.description, max_len=100)
        tasks_summary.append({
            "task_id": str(t.id)[:8],
            "description": safe_desc,
            "status": t.status.value,
            "task_type": t.inputs.get("task_type", "unknown"),
        })

    artifacts_summary = []
    for a in job.artifacts:
        safe_name, _ = redact_safe_text(a.name, max_len=60)
        artifacts_summary.append({
            "artifact_id": str(a.id)[:8],
            "name": safe_name,
            "kind": a.kind.value if hasattr(a.kind, "value") else str(a.kind),
            "has_patch_intent": bool(a.metadata.get("patch_intent_explanations")),
            "is_test_failure": bool(a.metadata.get("test_failure")),
            "is_repair": bool(a.metadata.get("repair")),
        })

    prompt = job.user_prompt or ""
    safe_prompt, prompt_redactions = redact_safe_text(prompt, max_len=200)

    return {
        "job_id": str(job.id),
        "name": job.name[:60],
        "state": job.state.value,
        "user_prompt_present": bool(prompt),
        "user_prompt_length": len(prompt),
        "user_prompt_safe_summary": safe_prompt if prompt_redactions == 0 else None,
        "user_prompt_redacted": prompt_redactions > 0,
        "task_count": len(job.tasks),
        "artifact_count": len(job.artifacts),
        "tasks": tasks_summary,
        "artifacts": artifacts_summary,
    }


def _build_event_summary(events: list[dict]) -> dict:
    """Safe event summary — counts by type, no raw metadata."""
    counts: dict[str, int] = {}
    latest_ts = ""
    for ev in events:
        etype = ev.get("event", "unknown")
        counts[etype] = counts.get(etype, 0) + 1
        ts = ev.get("timestamp", ev.get("ts", ""))
        if ts > latest_ts:
            latest_ts = ts

    repair_events = sum(v for k, v in counts.items() if "repair" in k or "failure" in k)
    proof_events = counts.get("proof_chain_built", 0)
    apply_events = sum(v for k, v in counts.items() if "apply" in k)
    test_events = sum(v for k, v in counts.items() if "test" in k)

    return {
        "total_events": len(events),
        "event_counts": counts,
        "latest_timestamp": latest_ts,
        "repair_events": repair_events,
        "proof_events": proof_events,
        "apply_events": apply_events,
        "test_events": test_events,
    }


def _build_changed_files_safe(job: Any, events: list[dict]) -> dict:
    """Safe changed file list from available sources. Protected paths excluded."""
    files: dict[str, ChangedFileSafe] = {}
    redacted_count = 0

    for a in job.artifacts:
        explanations = a.metadata.get("patch_intent_explanations", [])
        for exp in explanations:
            path = exp.get("file", "")
            if not path or path.startswith("/") or ".." in Path(path).parts:
                continue
            if _is_protected_path(path):
                redacted_count += 1
                continue
            if path not in files:
                files[path] = ChangedFileSafe(path=path)
            files[path].status = exp.get("action", "unknown")
            if a.task_id:
                files[path].related_task_id = str(a.task_id)[:8]
            from packages.orchestration.approval_queue import make_intent_id
            files[path].related_intent_id = make_intent_id(a.id, 0)

    for ev in events:
        if ev.get("event") == "test_completed" or ev.get("event") == "test_passed":
            tested_path = ev.get("path", "")
            if tested_path in files:
                files[tested_path].tested_after_change = True

    return {
        "files": [
            {
                "path": f.path,
                "status": f.status,
                "proof_status": f.proof_status,
                "related_task_id": f.related_task_id,
                "related_intent_id": f.related_intent_id,
                "tested_after_change": f.tested_after_change,
                "safety_flags": f.safety_flags,
            }
            for f in files.values()
        ],
        "redacted_protected_path_count": redacted_count,
    }


def _build_repair_summary(job: Any, events: list[dict]) -> dict:
    """Safe repair summary — no raw test output."""
    failure_count = 0
    fix_task_count = 0
    repair_intent_count = 0
    pending_intents = 0
    latest_failure_kind = ""
    next_safe_action = None

    for a in job.artifacts:
        if a.metadata.get("test_failure"):
            failure_count += 1
            kind = a.metadata.get("failure_kind", "")
            if kind:
                latest_failure_kind = kind
        if a.metadata.get("repair"):
            repair_intent_count += 1
            approvals = a.metadata.get("patch_intent_approvals", {})
            explanations = a.metadata.get("patch_intent_explanations", [])
            for idx, _exp in enumerate(explanations):
                from packages.orchestration.approval_queue import make_intent_id
                iid = make_intent_id(a.id, idx)
                state = approvals.get(iid, {}).get("state", "pending")
                if state == "pending":
                    pending_intents += 1

    for t in job.tasks:
        if t.inputs.get("failure_artifact_id"):
            fix_task_count += 1

    for ev in events:
        if ev.get("event") == "repair_loop_stopped":
            meta = ev
            if meta.get("stop_reason") == "awaiting_approval":
                next_safe_action = f"remedy patch approve {str(job.id)} {meta.get('fix_task_id', '?')[:8]}"

    return {
        "failure_artifact_count": failure_count,
        "fix_task_count": fix_task_count,
        "repair_patch_intent_count": repair_intent_count,
        "pending_repair_intents": pending_intents,
        "latest_failure_kind": latest_failure_kind,
        "next_safe_action": next_safe_action,
    }


def _build_context_inspection_safe(job: Any, events: list[dict]) -> dict:
    """Safe context inspection summary — no file bodies."""
    try:
        from packages.orchestration.context_inspector import inspect_context
        inspection = inspect_context(job, events)
        return {
            "included_count": len(inspection.included_paths),
            "excluded_count": len(inspection.excluded_paths),
            "protected_count": len(inspection.protected_paths),
            "unsupported_count": len(inspection.unsupported_paths),
            "budget_tokens": inspection.budget_tokens,
            "budget_used_tokens": inspection.budget_used_tokens,
            "budget_remaining_tokens": inspection.budget_remaining_tokens,
            "policy_gates": [
                {"name": g.name, "status": g.status, "reason": g.reason[:100]}
                for g in inspection.policy_gates
            ],
            "tooling": {
                "has_mcp": inspection.tooling.has_mcp,
                "mcp_server_count": inspection.tooling.mcp_server_count,
            } if inspection.tooling else {},
        }
    except Exception:
        return {"status": "section_unavailable", "reason": "context inspection not available"}


def _build_trust_report_safe(job: Any, events: list[dict], data_dir: Path) -> dict:
    """Safe trust report — redacted text summary only."""
    try:
        from packages.orchestration.trust_report import summarize_trust_report
        text = summarize_trust_report(job, events, data_dir=data_dir)
        safe_text, redactions = redact_safe_text(text, max_len=5000)
        return {
            "status": "available",
            "summary_text": safe_text,
            "summary_length": len(safe_text),
            "redaction_count": redactions,
        }
    except Exception:
        return {"status": "section_unavailable", "reason": "trust report not available"}


def _build_proof_chains_safe(job: Any, events: list[dict]) -> dict:
    """Safe proof chains — no raw diffs, no raw goal text."""
    try:
        from packages.orchestration.proof_chain import build_proof_chain, export_proof_chain_json
        chain = build_proof_chain(job, events)
        exported = export_proof_chain_json(chain)
        if "goal" in exported:
            safe_goal, _ = redact_safe_text(str(exported["goal"]), max_len=200)
            exported["goal"] = safe_goal
        safe_changes = []
        redacted_path_count = 0
        for change in exported.get("changes", []):
            path = change.get("target_path", change.get("path", change.get("file", "")))
            if _is_protected_path(path):
                redacted_path_count += 1
                continue
            change.pop("diff_preview", None)
            change.pop("content", None)
            change.pop("raw_diff", None)
            for field in ("reason", "summary", "description"):
                if field in change:
                    change[field], _ = redact_safe_text(str(change[field]), max_len=300)
            safe_changes.append(change)
        exported["changes"] = safe_changes
        exported["redacted_protected_path_count"] = redacted_path_count
        return exported
    except Exception:
        return {"status": "section_unavailable", "reason": "proof chains not available"}


def _build_command_summary(job: Any) -> dict:
    """Safe command summary — commands available for this job."""
    from apps.cli.command_catalog import CATALOG
    relevant_groups = {"repair", "patch", "job", "change", "brain", "review"}
    commands = []
    for cmd in CATALOG:
        if cmd.group_id in relevant_groups:
            commands.append({
                "command_id": cmd.command_id,
                "description": cmd.description[:80],
                "action_class": cmd.action_class,
                "supports_json": cmd.supports_json,
            })
    return {"available_commands": commands, "command_count": len(commands)}


def _build_progress_ledger_safe(job: Any, events: list[dict]) -> dict:
    """Safe progress ledger section — no raw content."""
    try:
        from packages.orchestration.progress_ledger import (
            build_progress_ledger,
            export_progress_ledger_json,
        )
        plan_text = ""
        live_review_text = ""
        context_text = ""
        agent_dir = Path(".agent")
        if agent_dir.exists():
            for name, target_ref in [("plan.md", "plan"), ("live_review.md", "review"), ("context.md", "ctx")]:
                p = agent_dir / name
                if p.exists():
                    text = p.read_text(encoding="utf-8", errors="replace")
                    if target_ref == "plan":
                        plan_text = text
                    elif target_ref == "review":
                        live_review_text = text
                    else:
                        context_text = text

        ledger = build_progress_ledger(
            plan_text=plan_text,
            live_review_text=live_review_text,
            context_text=context_text,
            job=job,
            events=events,
        )
        exported = export_progress_ledger_json(ledger)
        for item in exported.get("items", []):
            if item.get("safe_summary"):
                item["safe_summary"], _ = redact_safe_text(item["safe_summary"], max_len=200)
        return exported
    except Exception:
        return {"status": "section_unavailable", "reason": "progress ledger not available"}


def _build_integrity_summary() -> dict:
    """Safe integrity summary — no raw command output."""
    try:
        from packages.orchestration.integrity_gate import (
            export_integrity_json,
            run_integrity_checks,
        )
        result = run_integrity_checks(collect_only=False)
        exported = export_integrity_json(result)
        # Strip any message content that might leak paths/secrets
        for check in exported.get("checks", []):
            msg = check.get("message", "")
            safe_msg, _ = redact_safe_text(msg, max_len=200)
            check["message"] = safe_msg
        return exported
    except Exception:
        return {"status": "section_unavailable", "reason": "integrity gate not available"}


def _build_contract_summary(job_id: str) -> dict:
    """Safe run contract summary for the review bundle."""
    try:
        from packages.orchestration.run_contract import (
            ensure_contract,
            export_run_contract_json,
            load_usage,
            export_usage_json,
        )
        from packages.orchestration.storage import load_job

        job = load_job(job_id)
        contract = ensure_contract(job)
        exported = export_run_contract_json(contract)
        # Strip fields that might trigger safety scanners
        exported.pop("notes", None)
        exported.pop("denied_paths", None)
        exported.pop("allowed_paths", None)
        exported["denied_paths_count"] = len(contract.denied_paths)
        exported["allowed_paths_count"] = len(contract.allowed_paths)
        exported["usage"] = export_usage_json(load_usage(job))
        return exported
    except Exception:
        return {"status": "section_unavailable", "reason": "run contract not available"}


def _build_test_execution_summary(job: Any, events: list[dict]) -> dict:
    """Safe test execution summary for the review bundle. No raw output."""
    try:
        from packages.orchestration.run_contract import load_usage, export_usage_json

        # Collect test run records from job metadata
        test_runs = job.metadata.get("test_runs") or []
        safe_runs = []
        for r in test_runs[-20:]:  # last 20 only
            safe_runs.append({
                "test_run_id": r.get("test_run_id", ""),
                "contract_id": r.get("contract_id", ""),
                "status": r.get("status", ""),
                "exit_code": r.get("exit_code"),
                "duration_ms": r.get("duration_ms", 0),
                "command_safe": r.get("command_safe", ""),
                "linked_intent_id": r.get("linked_intent_id", ""),
                "linked_task_id": r.get("linked_task_id", ""),
                "linked_apply_id": r.get("linked_apply_id", ""),
                "created_at": r.get("created_at", ""),
            })

        # Count results from events
        passed = sum(1 for e in events if e.get("event") == "test_run_completed"
                     and e.get("metadata", {}).get("status") == "passed")
        failed = sum(1 for e in events if e.get("event") in ("test_run_completed", "test_run_timed_out")
                     and e.get("metadata", {}).get("status") in ("failed", "timeout"))

        # Find failure artifact IDs
        artifact_ids = [
            e.get("metadata", {}).get("failure_artifact_id", "")
            for e in events
            if e.get("event") == "test_failure_artifact_created"
            and e.get("metadata", {}).get("failure_artifact_id")
        ]

        usage = load_usage(job)

        return {
            "version": 1,
            "run_count": len(safe_runs),
            "passed_count": passed,
            "failed_count": failed,
            "failure_artifact_ids": artifact_ids,
            "usage": export_usage_json(usage),
            "recent_runs": safe_runs,
        }
    except Exception:
        return {"status": "section_unavailable", "reason": "test execution data not available"}


def _build_bundle_readme(job_id: str, sections: list[str]) -> str:
    """Generate bundle readme."""
    lines = [
        "# Remedy Review Bundle",
        "",
        f"Job: {job_id[:8]}",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Contents",
        "",
    ]
    for s in sections:
        lines.append(f"- {s}")
    lines.extend([
        "",
        "## Safety",
        "",
        "This bundle contains safe summaries only.",
        "No raw artifact bodies, diffs, source files, stdout/stderr, or secrets.",
        "No __pycache__, .pyc, .env, .data, node_modules, or .git content.",
        "",
        "## How to review",
        "",
        "1. Start with `manifest.json` for overview",
        "2. Check `job_summary.json` for task/artifact state",
        "3. Review `proof_chains.json` for change verification",
        "4. Check `trust_report.json` for audit trail",
        "5. Review `repair_summary.json` for failure/fix status",
        "6. Check `event_summary.json` for timeline",
    ])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Bundle builder (Step 978)
# ---------------------------------------------------------------------------


def build_review_bundle(
    job_id: str,
    output_path: str | None = None,
) -> ReviewBundleResult:
    """Build safe review bundle zip for a job."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job
    from packages.orchestration.timeline import load_run_events

    result = ReviewBundleResult(
        job_id=job_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

    data_dir = resolve_data_root()

    # Validate output path
    if output_path:
        if not _is_safe_output_path(output_path):
            result.error = "Unsafe output path — contains traversal or protected directory"
            return result
        out_path = Path(output_path)
    else:
        out_path = _default_output_path(job_id, data_dir)

    result.output_path = str(out_path)

    # Load job
    try:
        job = load_job(job_id)
    except Exception:
        result.error = f"Job {job_id[:8]} not found"
        return result

    events = load_run_events(data_dir, UUID(job_id))

    # Build sections
    section_data: dict[str, bytes] = {}

    # job_summary.json
    try:
        js = _build_job_summary(job)
        content = json.dumps(js, indent=2).encode()
        section_data["job_summary.json"] = content
        result.sections.append(ReviewBundleSection("job_summary.json", byte_count=len(content)))
    except Exception:
        result.sections.append(ReviewBundleSection("job_summary.json", status="error", error="build failed"))

    # proof_chains.json
    try:
        pc = _build_proof_chains_safe(job, events)
        content = json.dumps(pc, indent=2).encode()
        section_data["proof_chains.json"] = content
        result.sections.append(ReviewBundleSection("proof_chains.json", byte_count=len(content)))
    except Exception:
        result.sections.append(ReviewBundleSection("proof_chains.json", status="error", error="build failed"))

    # event_summary.json
    try:
        es = _build_event_summary(events)
        content = json.dumps(es, indent=2).encode()
        section_data["event_summary.json"] = content
        result.sections.append(ReviewBundleSection("event_summary.json", byte_count=len(content)))
    except Exception:
        result.sections.append(ReviewBundleSection("event_summary.json", status="error", error="build failed"))

    # trust_report.json
    try:
        tr = _build_trust_report_safe(job, events, data_dir)
        content = json.dumps(tr, indent=2).encode()
        section_data["trust_report.json"] = content
        result.sections.append(ReviewBundleSection("trust_report.json", byte_count=len(content)))
    except Exception:
        result.sections.append(ReviewBundleSection("trust_report.json", status="error", error="build failed"))

    # context_inspection.json
    try:
        ci = _build_context_inspection_safe(job, events)
        content = json.dumps(ci, indent=2).encode()
        section_data["context_inspection.json"] = content
        result.sections.append(ReviewBundleSection("context_inspection.json", byte_count=len(content)))
    except Exception:
        result.sections.append(ReviewBundleSection("context_inspection.json", status="error", error="build failed"))

    # changed_files_safe.json
    try:
        cf = _build_changed_files_safe(job, events)
        content = json.dumps(cf, indent=2).encode()
        section_data["changed_files_safe.json"] = content
        result.sections.append(ReviewBundleSection("changed_files_safe.json", byte_count=len(content)))
    except Exception:
        result.sections.append(ReviewBundleSection("changed_files_safe.json", status="error", error="build failed"))

    # repair_summary.json
    try:
        rs = _build_repair_summary(job, events)
        content = json.dumps(rs, indent=2).encode()
        section_data["repair_summary.json"] = content
        result.sections.append(ReviewBundleSection("repair_summary.json", byte_count=len(content)))
    except Exception:
        result.sections.append(ReviewBundleSection("repair_summary.json", status="error", error="build failed"))

    # command_summary.json
    try:
        cs = _build_command_summary(job)
        content = json.dumps(cs, indent=2).encode()
        section_data["command_summary.json"] = content
        result.sections.append(ReviewBundleSection("command_summary.json", byte_count=len(content)))
    except Exception:
        result.sections.append(ReviewBundleSection("command_summary.json", status="error", error="build failed"))

    # progress_ledger.json
    try:
        pl = _build_progress_ledger_safe(job, events)
        content = json.dumps(pl, indent=2).encode()
        section_data["progress_ledger.json"] = content
        result.sections.append(ReviewBundleSection("progress_ledger.json", byte_count=len(content)))
    except Exception:
        result.sections.append(ReviewBundleSection("progress_ledger.json", status="error", error="build failed"))

    # integrity_summary.json
    try:
        ig = _build_integrity_summary()
        content = json.dumps(ig, indent=2).encode()
        section_data["integrity_summary.json"] = content
        result.sections.append(ReviewBundleSection("integrity_summary.json", byte_count=len(content)))
    except Exception:
        result.sections.append(ReviewBundleSection("integrity_summary.json", status="error", error="build failed"))

    # run_contract_summary.json
    try:
        rcs = _build_contract_summary(job_id)
        content = json.dumps(rcs, indent=2).encode()
        section_data["run_contract_summary.json"] = content
        result.sections.append(ReviewBundleSection("run_contract_summary.json", byte_count=len(content)))
    except Exception:
        result.sections.append(ReviewBundleSection("run_contract_summary.json", status="error", error="build failed"))

    # test_execution_summary.json
    try:
        tes = _build_test_execution_summary(job, events)
        content = json.dumps(tes, indent=2).encode()
        section_data["test_execution_summary.json"] = content
        result.sections.append(ReviewBundleSection("test_execution_summary.json", byte_count=len(content)))
    except Exception:
        result.sections.append(ReviewBundleSection("test_execution_summary.json", status="error", error="build failed"))

    # manifest.json (built from above)
    included = [s.filename for s in result.sections if s.status == "included"]
    skipped = [s.filename for s in result.sections if s.status != "included"]
    manifest = ReviewBundleManifest(
        job_id=job_id,
        generated_at=result.generated_at,
        included_sections=included,
        skipped_sections=skipped,
        safety_warnings=result.safety.warnings,
    )
    manifest_content = json.dumps({
        "bundle_version": manifest.bundle_version,
        "job_id": manifest.job_id,
        "generated_at": manifest.generated_at,
        "included_sections": manifest.included_sections,
        "skipped_sections": manifest.skipped_sections,
        "safety_warnings": manifest.safety_warnings,
    }, indent=2).encode()
    section_data["manifest.json"] = manifest_content
    result.sections.insert(0, ReviewBundleSection("manifest.json", byte_count=len(manifest_content)))

    # bundle_readme.md
    readme = _build_bundle_readme(job_id, list(section_data.keys()))
    readme_content = readme.encode()
    section_data["bundle_readme.md"] = readme_content
    result.sections.append(ReviewBundleSection("bundle_readme.md", byte_count=len(readme_content)))

    # Write zip
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in sorted(section_data.items()):
            zf.writestr(name, data)

    result.file_count = len(section_data)
    result.byte_count = sum(len(d) for d in section_data.values())

    # Safety audit
    _audit_bundle_safety(result, section_data)

    return result


def _audit_bundle_safety(result: ReviewBundleResult, section_data: dict[str, bytes]) -> None:
    """Post-build safety audit — scans all sections for forbidden content."""
    from packages.orchestration.redaction_patterns import (
        find_forbidden_surface_tokens,
        _SECRET_RE,
    )

    _SAFE_MENTION_FILES = {"bundle_readme.md", "manifest.json"}

    for name, data in section_data.items():
        text = data.decode("utf-8", errors="replace")
        text_lower = text.lower()

        # Secret pattern detection
        if _SECRET_RE.search(text):
            result.safety.has_secrets = True
            result.safety.warnings.append(f"Secret-like pattern in {name}")

        # Traceback detection
        if "traceback (most recent" in text_lower and name not in _SAFE_MENTION_FILES:
            result.safety.has_raw_output = True
            result.safety.warnings.append(f"Traceback in {name}")

        # Raw output field names
        for field in ("command_output", "raw_stdout", "raw_stderr"):
            if f'"{field}"' in text_lower:
                result.safety.has_raw_output = True
                result.safety.warnings.append(f"Raw output field '{field}' in {name}")

        # __pycache__ / .pyc detection
        if name not in _SAFE_MENTION_FILES:
            if "__pycache__" in text or ".pyc" in text_lower:
                result.safety.has_pycache = True
                result.safety.warnings.append(f"Cache reference in {name}")

        # .env file reference detection (not category word "environment")
        if name not in _SAFE_MENTION_FILES:
            if '".env"' in text_lower or '".env.' in text_lower or "/.env" in text_lower:
                result.safety.has_env_files = True
                result.safety.warnings.append(f".env reference in {name}")

        # Raw diff markers
        if name not in _SAFE_MENTION_FILES:
            if "\n--- a/" in text or "\n+++ b/" in text:
                result.safety.has_raw_diffs = True
                result.safety.warnings.append(f"Raw diff markers in {name}")


# ---------------------------------------------------------------------------
# Export / summary
# ---------------------------------------------------------------------------


def export_review_bundle_json(result: ReviewBundleResult) -> dict[str, Any]:
    """Export bundle result as safe JSON dict."""
    return {
        "job_id": result.job_id,
        "output_path": result.output_path,
        "bundle_version": result.bundle_version,
        "generated_at": result.generated_at,
        "file_count": result.file_count,
        "byte_count": result.byte_count,
        "sections": [
            {"filename": s.filename, "status": s.status, "byte_count": s.byte_count}
            for s in result.sections
        ],
        "safety": {
            "is_safe": result.safety.is_safe,
            "warnings": result.safety.warnings,
        },
        "error": result.error or None,
    }


def summarize_review_bundle(result: ReviewBundleResult) -> str:
    """Human-readable bundle summary."""
    if result.error:
        return f"Review Bundle: ERROR — {result.error}"

    lines = [
        f"Review Bundle: {result.job_id[:8]}",
        f"Output: {result.output_path}",
        f"Sections: {result.file_count}",
        f"Size: {result.byte_count} bytes",
        "",
    ]

    for s in result.sections:
        status_mark = "+" if s.status == "included" else "!"
        lines.append(f"  [{status_mark}] {s.filename} ({s.byte_count}B)")

    if result.safety.warnings:
        lines.append("\nWarnings:")
        for w in result.safety.warnings:
            lines.append(f"  - {w}")
    else:
        lines.append("\nSafety: PASS — no unsafe content detected")

    return "\n".join(lines)
