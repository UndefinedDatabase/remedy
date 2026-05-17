"""
Patch Apply v0 — approval-gated patch application for Remedy.

Applies an approved PatchIntent to the attached target repository.
Markdown-only, append-only for existing files, no shell execution,
no Git operations, no arbitrary diff application, no repo_overwrite.

v0 constraints (see docs/architecture.md):
  - Only approved intents with create or modify action.
  - Only .md target paths.
  - high/unknown risk intents are blocked.
  - repo_generated_write permission is required.
  - repo_overwrite is NOT used or required.
  - shell_exec is NOT used.
  - modify: appends a plain Markdown section; never replaces content.
  - create: writes new file; blocked if target already exists.
  - Second apply on same intent is a no-op (already_applied).
  - No Remedy control markers or raw HTML comments are written into repo files.
  - Generated lines pass through _neutralize (output boundary).
  - Idempotency is metadata-only via patch_intent_apply_records.

Apply record schema (stored under artifact.metadata["patch_intent_apply_records"][intent_id]):
  {
    "state":         "applied" | "noop" | "blocked",
    "applied_at":    ISO timestamp,
    "target_path":   str,
    "action":        "create" | "modify",
    "bytes_written": int,
    "line_count":    int,
    "reason":        "applied" | "already_applied" | <blocked_reason>,
  }

Run-log event: patch_intent_applied
Metadata exact keys: {intent_id, target_path, action, outcome, bytes_written, line_count}

No artifact content, approval reasons, diff text, or exception text is stored in
any apply record, run-log event, or summary output.

Public API::
  apply_patch_intent(job, intent_id, *, data_dir=None) -> PatchApplyResult
  format_apply_result(result) -> str
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from packages.orchestration.approval_queue import APPROVAL_APPROVED, get_patch_intent
from packages.orchestration.markdown_output_safety import (
    neutralize_markdown_html_comment_start as _neutralize,
)
from packages.orchestration.patch_intent import RISK_HIGH, RISK_UNKNOWN
from packages.orchestration.permissions import Capability, is_allowed

if TYPE_CHECKING:
    from packages.core.models import Job


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_BLOCKED_RISKS: frozenset[str] = frozenset({RISK_HIGH, RISK_UNKNOWN})

# Section headers in the builder artifact content format (kept local).
_ARTIFACT_SECTION_HEADERS: frozenset[str] = frozenset(
    {"Summary:", "Proposed Changes:", "Notes:", "Risks:"}
)


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PatchApplyResult:
    """Immutable outcome of a patch intent apply operation."""

    state: str            # "applied" | "noop" | "blocked"
    intent_id: str
    target_path: str
    action: str
    outcome: str          # "applied" | "already_applied" | <blocked_reason>
    bytes_written: int
    line_count: int
    blocked_reason: str | None  # set when state == "blocked"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def apply_patch_intent(
    job: "Job",
    intent_id: str,
    *,
    data_dir: Path | None = None,
) -> PatchApplyResult:
    """Apply an approved PatchIntent to the attached target repository.

    Validates approval state, path safety, risk level, and permissions
    before writing to disk.  On success, persists an apply record to
    artifact metadata, saves the job, and emits a run-log event.

    Returns a PatchApplyResult for all outcomes.  Never raises exceptions
    for operational failures — those are returned as blocked results.

    Args:
        job:       The job whose patch intent will be applied.
        intent_id: The intent ID string (e.g. "a1b2c3d4-0").
        data_dir:  REMEDY_DATA_DIR root; used for run-log path resolution.
                   Defaults to the env-var / repo-local resolution.

    Returns:
        PatchApplyResult with state "applied", "noop", or "blocked".
    """
    from packages.orchestration.storage import save_job

    def _blocked(reason: str, target_path: str = "", action: str = "") -> PatchApplyResult:
        result = PatchApplyResult(
            state="blocked",
            intent_id=intent_id,
            target_path=target_path,
            action=action,
            outcome=reason,
            bytes_written=0,
            line_count=0,
            blocked_reason=reason,
        )
        _emit_run_log(job, result, data_dir)
        return result

    # ── 1/2. Target repo from job metadata ──────────────────────────────
    target_repo_str: str = job.metadata.get("target_repo", "") or ""
    if not target_repo_str:
        return _blocked("repo_missing")
    repo_root = Path(target_repo_str)
    if not repo_root.exists() or not repo_root.is_dir():
        return _blocked("repo_missing")

    # ── 3/4. Load and validate intent ────────────────────────────────────
    intent = get_patch_intent(job, intent_id)
    if intent is None:
        return _blocked("intent_not_found")

    target_path: str = intent["target_path"]
    action: str      = intent["action"]
    risk: str        = intent["risk"]
    state: str       = intent["state"]

    # ── 5. Approval state ─────────────────────────────────────────────────
    if state != APPROVAL_APPROVED:
        return _blocked(f"not_approved:{state}", target_path, action)

    # ── 6. Path safety ────────────────────────────────────────────────────
    path_err = _validate_target_path(target_path)
    if path_err:
        return _blocked(path_err, target_path, action)
    resolved_root   = repo_root.resolve()
    resolved_target = (repo_root / target_path).resolve()
    if not resolved_target.is_relative_to(resolved_root):
        return _blocked("unsafe_path", target_path, action)

    # ── 7. Action + risk ─────────────────────────────────────────────────
    # Note: .md enforcement is authoritative in _validate_target_path above;
    # no second check here.
    if action not in ("create", "modify"):
        return _blocked(f"unsupported_action:{action}", target_path, action)
    if risk in _BLOCKED_RISKS:
        return _blocked(f"unsupported_risk:{risk}", target_path, action)

    # ── 8. Permissions ────────────────────────────────────────────────────
    # repo_overwrite is NOT required or consulted here.
    # shell_exec is NOT used here.
    if not is_allowed(job, Capability.repo_generated_write):
        return _blocked("permission_denied", target_path, action)

    # ── 9a. Owning artifact ───────────────────────────────────────────────
    artifact = next(
        (a for a in job.artifacts if str(a.id) == intent["artifact_id"]), None
    )
    if artifact is None:
        return _blocked("artifact_missing", target_path, action)

    # ── 9b. Already-applied guard ─────────────────────────────────────────
    existing_records: dict = artifact.metadata.get("patch_intent_apply_records", {})
    if existing_records.get(intent_id, {}).get("state") == "applied":
        result = PatchApplyResult(
            state="noop",
            intent_id=intent_id,
            target_path=target_path,
            action=action,
            outcome="already_applied",
            bytes_written=0,
            line_count=0,
            blocked_reason=None,
        )
        _emit_run_log(job, result, data_dir)
        return result

    # ── 9c. Extract proposed lines from artifact content ──────────────────
    proposed_lines = _extract_proposed_lines(artifact.content)

    # ── 9d. Apply ──────────────────────────────────────────────────────────
    if action == "create":
        if resolved_target.exists():
            return _blocked("target_exists", target_path, action)
        content = _build_create_content(target_path, proposed_lines)
        resolved_target.parent.mkdir(parents=True, exist_ok=True)
        resolved_target.write_text(content, encoding="utf-8")
        bytes_written = len(content.encode("utf-8"))
        line_count = content.count("\n") + 1

    else:  # modify
        if not resolved_target.exists():
            return _blocked("target_missing", target_path, action)
        # Idempotency is metadata-only (step 9b above); no file-content check here.
        section = _build_modify_section(proposed_lines)
        append_text = "\n\n" + section  # section already ends with exactly one newline
        with resolved_target.open("a", encoding="utf-8") as fh:
            fh.write(append_text)
        bytes_written = len(append_text.encode("utf-8"))
        line_count = append_text.count("\n")

    # ── 10. Apply record ──────────────────────────────────────────────────
    if "patch_intent_apply_records" not in artifact.metadata:
        artifact.metadata["patch_intent_apply_records"] = {}
    artifact.metadata["patch_intent_apply_records"][intent_id] = {
        "state": "applied",
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "target_path": target_path,
        "action": action,
        "bytes_written": bytes_written,
        "line_count": line_count,
        "reason": "applied",
    }

    # ── 11. Save job ──────────────────────────────────────────────────────
    save_job(job)

    result = PatchApplyResult(
        state="applied",
        intent_id=intent_id,
        target_path=target_path,
        action=action,
        outcome="applied",
        bytes_written=bytes_written,
        line_count=line_count,
        blocked_reason=None,
    )

    # ── 12. Run-log event ─────────────────────────────────────────────────
    _emit_run_log(job, result, data_dir)

    return result


def format_apply_result(result: PatchApplyResult) -> str:
    """Format a PatchApplyResult for CLI output.

    Returns a multi-line string.
    No raw artifact content, diff text, or approval reasons are included.
    """
    if result.state == "applied":
        lines = [
            f"Applied: {result.intent_id} ({result.target_path})",
            f"  action: {result.action}",
            f"  outcome: applied",
            f"  bytes_written: {result.bytes_written}",
            f"  lines_written: {result.line_count}",
            "Note: patch application is limited to approved Markdown intents in v0.",
        ]
        return "\n".join(lines)

    if result.state == "noop":
        return (
            f"No-op: {result.intent_id} ({result.target_path})\n"
            f"  outcome: already_applied"
        )

    # blocked
    reason = result.blocked_reason or result.outcome
    return f"Error: {reason}"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------




def _validate_target_path(target_path: str) -> str | None:
    """Return an error reason string if target_path fails safety checks, else None."""
    if not target_path:
        return "empty_target_path"
    if "\x00" in target_path:
        return "null_byte_in_path"
    if target_path.startswith("/"):
        return "absolute_path"
    parts = target_path.split("/")
    if ".." in parts:
        return "path_traversal"
    if not target_path.lower().endswith(".md"):
        return "unsupported_file_type"
    return None


def _extract_proposed_lines(content: str) -> list[str]:
    """Extract plain-text lines from the 'Proposed Changes:' section of artifact content.

    Section-aware: stops at any other recognised section header.
    Strips leading '  - ' prefix from each line.
    Returns empty list if section is absent.
    """
    lines: list[str] = []
    in_section = False
    for line in content.splitlines():
        if line == "Proposed Changes:":
            in_section = True
        elif line in _ARTIFACT_SECTION_HEADERS:
            in_section = False
        elif in_section and line.startswith("  - "):
            lines.append(line[4:])
    return lines


def _build_create_content(
    target_path: str,
    proposed_lines: list[str],
) -> str:
    """Build plain Markdown content for a new (create) file.

    No Remedy control markers, intent IDs, or provenance metadata are written
    into the file.  Provenance is recorded externally in apply records and run logs.
    """
    # Belt-and-suspenders: hyphen replacement already prevents "<!--" in normal
    # path-derived stems (the "--" in "<!--" becomes spaces first).  _neutralize
    # is applied as output-boundary defense for any residual edge cases.
    stem = _neutralize(Path(target_path).stem.replace("_", " ").replace("-", " ").title())
    safe_lines = [_neutralize(ln) for ln in proposed_lines]
    bullet_block = (
        "\n".join(f"- {ln}" for ln in safe_lines)
        if safe_lines
        else "(no proposed changes found in artifact)"
    )
    return (
        f"# {stem}\n"
        f"\n"
        f"## Proposed Update\n"
        f"\n"
        f"{bullet_block}\n"
    )


def _build_modify_section(proposed_lines: list[str]) -> str:
    """Build a plain Markdown section appended to an existing (modify) file.

    No Remedy control markers, intent IDs, or provenance metadata are written
    into the file.  Idempotency is metadata-only via patch_intent_apply_records.
    """
    safe_lines = [_neutralize(ln) for ln in proposed_lines]
    bullet_block = (
        "\n".join(f"- {ln}" for ln in safe_lines)
        if safe_lines
        else "(no proposed changes found in artifact)"
    )
    return f"## Proposed Update\n\n{bullet_block}\n"


def _emit_run_log(
    job: "Job",
    result: PatchApplyResult,
    data_dir: Path | None,
) -> None:
    """Emit a patch_intent_applied run-log event.

    Metadata exact keys: intent_id, target_path, action, outcome,
    bytes_written, line_count.
    No raw content, approval reasons, diff text, or exception text.
    """
    from packages.orchestration.run_log import RunEvent, RunLogWriter

    runs_root = (data_dir / "runs") if data_dir is not None else None
    log = RunLogWriter(job_id=job.id, runs_root=runs_root)
    log.append(
        RunEvent(
            event="patch_intent_applied",
            job_id=str(job.id),
            run_id=log.run_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            outcome=result.state,
            metadata={
                "intent_id":     result.intent_id,
                "target_path":   result.target_path,
                "action":        result.action,
                "outcome":       result.state,
                "bytes_written": result.bytes_written,
                "line_count":    result.line_count,
            },
        )
    )
