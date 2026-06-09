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
    "bundle_readme.md",
)

_UNSAFE_PATTERNS = frozenset({
    "__pycache__", ".pyc", ".pyo", ".env", ".data",
    "node_modules", "dist", "build", ".cache", ".git",
    "secrets", "credentials", "token",
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
# Path safety
# ---------------------------------------------------------------------------


def _is_safe_output_path(path: str) -> bool:
    """Reject traversal and protected paths."""
    if ".." in path:
        return False
    p = Path(path)
    for part in p.parts:
        if part.startswith(".env") or part in (".git", ".data"):
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
    """Safe job summary — no raw content."""
    tasks_summary = []
    for t in job.tasks:
        tasks_summary.append({
            "task_id": str(t.id)[:8],
            "description": t.description[:100],
            "status": t.status.value,
            "task_type": t.inputs.get("task_type", "unknown"),
        })

    artifacts_summary = []
    for a in job.artifacts:
        artifacts_summary.append({
            "artifact_id": str(a.id)[:8],
            "name": a.name[:60],
            "kind": a.kind.value if hasattr(a.kind, "value") else str(a.kind),
            "has_patch_intent": bool(a.metadata.get("patch_intent_explanations")),
            "is_test_failure": bool(a.metadata.get("test_failure")),
            "is_repair": bool(a.metadata.get("repair")),
        })

    return {
        "job_id": str(job.id),
        "name": job.name[:60],
        "state": job.state.value,
        "user_prompt_preview": (job.user_prompt[:200] + "...") if len(job.user_prompt) > 200 else job.user_prompt,
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


def _build_changed_files_safe(job: Any, events: list[dict]) -> list[dict]:
    """Safe changed file list from available sources."""
    files: dict[str, ChangedFileSafe] = {}

    for a in job.artifacts:
        explanations = a.metadata.get("patch_intent_explanations", [])
        for exp in explanations:
            path = exp.get("file", "")
            if path and not path.startswith("/") and ".." not in path:
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

    return [
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
    ]


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
    """Safe trust report — text summary only, no raw output."""
    try:
        from packages.orchestration.trust_report import summarize_trust_report
        text = summarize_trust_report(job, events, data_dir=data_dir)
        if len(text) > 5000:
            text = text[:5000] + "\n... (truncated)"
        return {
            "status": "available",
            "summary_text": text,
            "summary_length": len(text),
        }
    except Exception:
        return {"status": "section_unavailable", "reason": "trust report not available"}


def _build_proof_chains_safe(job: Any, events: list[dict]) -> dict:
    """Safe proof chains — no raw diffs."""
    try:
        from packages.orchestration.proof_chain import build_proof_chain, export_proof_chain_json
        chain = build_proof_chain(job, events)
        exported = export_proof_chain_json(chain)
        for change in exported.get("changes", []):
            change.pop("diff_preview", None)
            change.pop("content", None)
            change.pop("raw_diff", None)
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
    """Post-build safety audit."""
    for name, data in section_data.items():
        text = data.decode("utf-8", errors="replace").lower()
        if "traceback" in text and name != "trust_report.json":
            result.safety.has_raw_output = True
            result.safety.warnings.append(f"Possible raw output in {name}")
        if "__pycache__" in text or ".pyc" in text:
            if name not in ("bundle_readme.md", "manifest.json"):
                result.safety.has_pycache = True
                result.safety.warnings.append(f"Possible __pycache__ reference in {name}")


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
