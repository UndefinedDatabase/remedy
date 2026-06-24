"""Ping-pong promotion — apply reviewed staged artifacts into target repo.

Promotion is a separate explicit human-approved action.
Never auto-promotes. Requires --approve flag.
No git commit, no git push.
"""
from __future__ import annotations

import hashlib
import json
import os
import shlex
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

# ---------------------------------------------------------------------------
# Blocked path patterns
# ---------------------------------------------------------------------------

_BLOCKED_PREFIXES = (
    ".git/", ".git\\",
    ".env", "node_modules/", "node_modules\\",
    "__pycache__/", "__pycache__\\",
    ".mypy_cache/", ".pytest_cache/", ".ruff_cache/",
    ".tox/", "dist/", "build/", ".eggs/",
    ".cache/", "htmlcov/",
)

_BLOCKED_EXACT = frozenset({
    ".git", ".env", ".gitignore",
})

_SECRET_PATTERNS = (".env", ".env.", ".env-")

_BINARY_EXTENSIONS = frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".bmp",
    ".zip", ".gz", ".tar", ".bz2", ".xz", ".7z",
    ".whl", ".pyc", ".pyo", ".so", ".dll", ".dylib",
    ".pdf", ".woff", ".woff2", ".ttf", ".eot",
})

_MAX_FILE_SIZE = 1_000_000  # 1 MB


def _is_blocked_path(rel_path: str) -> str:
    """Return block reason or empty string if path is allowed."""
    norm = rel_path.replace("\\", "/")

    # Path traversal
    if ".." in norm.split("/"):
        return "path_traversal"

    # Absolute path
    if os.path.isabs(rel_path):
        return "absolute_path"

    # Exact blocked
    if norm in _BLOCKED_EXACT or norm.rstrip("/") in _BLOCKED_EXACT:
        return f"blocked_path: {norm}"

    # Secret files
    base = os.path.basename(norm)
    if base == ".env" or base.startswith(".env.") or base.startswith(".env-"):
        return "secret_file"

    # Blocked prefixes
    for prefix in _BLOCKED_PREFIXES:
        p = prefix.replace("\\", "/")
        if norm.startswith(p) or norm == p.rstrip("/"):
            return f"blocked_path: {p.rstrip('/')}"

    # Binary
    ext = os.path.splitext(norm)[1].lower()
    if ext in _BINARY_EXTENSIONS:
        return "binary_file"

    return ""


def _hash_file(path: Path) -> str:
    """SHA-256 hash of file contents."""
    h = hashlib.sha256()
    try:
        h.update(path.read_bytes())
    except OSError:
        return ""
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Artifact persistence (called during run_pingpong)
# ---------------------------------------------------------------------------

@dataclass
class ArtifactEntry:
    """One artifact in the manifest."""
    relative_path: str = ""
    operation: str = ""  # "create" or "modify"
    file_type: str = ""  # extension
    target_baseline_hash: str = ""  # empty if new file
    staged_hash: str = ""
    size: int = 0


def persist_artifacts(
    run_dir: Path,
    staging: Path,
    original: Path,
    staged_files: list[str],
) -> list[ArtifactEntry]:
    """Persist staged file contents and manifest under run_dir/artifacts/.

    Returns list of ArtifactEntry for each persisted file.
    Skips blocked paths, binary files, oversized files.
    """
    artifacts_dir = run_dir / "artifacts" / "staged"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    entries: list[ArtifactEntry] = []

    for rel in sorted(staged_files):
        block_reason = _is_blocked_path(rel)
        if block_reason:
            continue

        staged_file = staging / rel
        if not staged_file.is_file():
            continue

        try:
            size = staged_file.stat().st_size
        except OSError:
            continue

        if size > _MAX_FILE_SIZE:
            continue

        # Determine operation
        orig_file = original / rel
        if orig_file.exists():
            operation = "modify"
            baseline_hash = _hash_file(orig_file)
        else:
            operation = "create"
            baseline_hash = ""

        # Copy file content
        dest = artifacts_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            content = staged_file.read_bytes()
            dest.write_bytes(content)
        except OSError:
            continue

        staged_hash = hashlib.sha256(content).hexdigest()
        ext = os.path.splitext(rel)[1].lower()

        entries.append(ArtifactEntry(
            relative_path=rel,
            operation=operation,
            file_type=ext,
            target_baseline_hash=baseline_hash,
            staged_hash=staged_hash,
            size=size,
        ))

    # Write manifest
    manifest = [
        {
            "relative_path": e.relative_path,
            "operation": e.operation,
            "file_type": e.file_type,
            "target_baseline_hash": e.target_baseline_hash,
            "staged_hash": e.staged_hash,
            "size": e.size,
        }
        for e in entries
    ]
    manifest_file = run_dir / "artifacts" / "manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2) + "\n")

    return entries


def load_artifacts(run_dir: Path) -> tuple[list[ArtifactEntry], Path]:
    """Load artifact manifest and return (entries, artifacts_staged_dir)."""
    manifest_file = run_dir / "artifacts" / "manifest.json"
    staged_dir = run_dir / "artifacts" / "staged"

    if not manifest_file.exists():
        return [], staged_dir

    try:
        data = json.loads(manifest_file.read_text())
    except (OSError, json.JSONDecodeError):
        return [], staged_dir

    entries = []
    for item in data:
        entries.append(ArtifactEntry(
            relative_path=item.get("relative_path", ""),
            operation=item.get("operation", ""),
            file_type=item.get("file_type", ""),
            target_baseline_hash=item.get("target_baseline_hash", ""),
            staged_hash=item.get("staged_hash", ""),
            size=item.get("size", 0),
        ))
    return entries, staged_dir


# ---------------------------------------------------------------------------
# Promotion result
# ---------------------------------------------------------------------------

@dataclass
class PromotionResult:
    """Result of a promotion attempt."""
    run_id: str = ""
    promotion_id: str = field(default_factory=lambda: uuid4().hex[:16])
    status: str = ""  # promoted, blocked, dry_run, promoted_test_failed
    approved: bool = False
    dry_run: bool = False
    target_repo: str = ""
    changed_target_files: list[str] = field(default_factory=list)
    applied_files: list[str] = field(default_factory=list)
    blocked_reason: str = ""
    baseline_mismatches: list[str] = field(default_factory=list)
    unsupported_files: list[str] = field(default_factory=list)
    post_test_command: str = ""
    post_test_passed: bool | None = None
    post_test_summary: str = ""
    git_status_hint: str = ""
    started_at: str = ""
    finished_at: str = ""


# ---------------------------------------------------------------------------
# Promotion logic
# ---------------------------------------------------------------------------

_TEST_OUTPUT_CAP = 10000


def _run_post_test(
    command: str,
    target: Path,
    *,
    timeout_sec: int = 120,
) -> tuple[bool, str]:
    """Run post-promotion test command in target repo."""
    try:
        argv = shlex.split(command)
    except ValueError as exc:
        return False, f"Invalid test command: {exc}"
    try:
        proc = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            cwd=str(target),
        )
    except FileNotFoundError:
        return False, f"Test command not found: {argv[0]}"
    except subprocess.TimeoutExpired:
        return False, f"Test command timed out after {timeout_sec}s"

    output = (proc.stdout or "") + (proc.stderr or "")
    if len(output) > _TEST_OUTPUT_CAP:
        output = output[:_TEST_OUTPUT_CAP] + "\n[OUTPUT TRUNCATED]"
    passed = proc.returncode == 0
    summary = f"exit={proc.returncode}"
    if output.strip():
        last_lines = output.strip().splitlines()[-5:]
        summary += " | " + " ".join(last_lines)
    return passed, summary


def promote_run(
    run_id: str,
    *,
    target_repo: str = ".",
    approve: bool = False,
    dry_run: bool = False,
    test_command: str = "",
) -> PromotionResult:
    """Promote reviewed staged artifacts into target repo.

    Without --approve, returns preview only. Never auto-promotes.
    """
    from packages.orchestration.pingpong_loop import _pingpong_runs_dir, load_run

    result = PromotionResult(
        run_id=run_id,
        approved=approve,
        dry_run=dry_run,
        target_repo=target_repo,
        post_test_command=test_command,
        started_at=datetime.now(timezone.utc).isoformat(),
    )

    # --- Load run ---
    run_data = load_run(run_id)
    if run_data is None:
        result.status = "blocked"
        result.blocked_reason = f"run_not_found: {run_id}"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    # --- Eligibility checks ---
    final_status = run_data.get("final_status", "")
    if final_status != "staged_review_passed":
        result.status = "blocked"
        result.blocked_reason = f"ineligible_status: {final_status}"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    if run_data.get("mode", "") != "staged":
        result.status = "blocked"
        result.blocked_reason = "mode_not_staged"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    staged_files = run_data.get("staged_files", [])
    if not staged_files:
        result.status = "blocked"
        result.blocked_reason = "no_staged_files"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    if run_data.get("target_mutated", False):
        result.status = "blocked"
        result.blocked_reason = "target_mutated_during_run"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    if run_data.get("changed_target_files", []):
        result.status = "blocked"
        result.blocked_reason = "changed_target_files_during_run"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    # Check reviewer verdict from rounds
    rounds = run_data.get("rounds", [])
    last_reviewer = None
    for rd in reversed(rounds):
        rv = rd.get("reviewer", {})
        if rv.get("verdict"):
            last_reviewer = rv
            break
    if not last_reviewer or last_reviewer.get("verdict") != "pass":
        result.status = "blocked"
        result.blocked_reason = "reviewer_verdict_not_pass"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    # --- Load artifacts ---
    run_dir = _pingpong_runs_dir() / run_id
    entries, artifacts_dir = load_artifacts(run_dir)
    if not entries:
        result.status = "blocked"
        result.blocked_reason = "no_artifacts"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    # --- Validate target repo path ---
    target = Path(target_repo).resolve()
    if not target.is_dir():
        result.status = "blocked"
        result.blocked_reason = f"target_not_directory: {target_repo}"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    # --- Validate each artifact ---
    blocked_files: list[str] = []
    unsupported: list[str] = []
    baseline_mismatches: list[str] = []
    valid_entries: list[ArtifactEntry] = []

    for entry in entries:
        # Block check
        block_reason = _is_blocked_path(entry.relative_path)
        if block_reason:
            blocked_files.append(f"{entry.relative_path}: {block_reason}")
            continue

        # Path containment
        dest = (target / entry.relative_path).resolve()
        try:
            dest.relative_to(target)
        except ValueError:
            blocked_files.append(f"{entry.relative_path}: path_escape")
            continue

        # Delete check (v0: no deletes)
        artifact_file = artifacts_dir / entry.relative_path
        if not artifact_file.exists():
            unsupported.append(f"{entry.relative_path}: delete_not_supported")
            continue

        # Size check
        try:
            size = artifact_file.stat().st_size
        except OSError:
            unsupported.append(f"{entry.relative_path}: unreadable")
            continue
        if size > _MAX_FILE_SIZE:
            unsupported.append(f"{entry.relative_path}: too_large ({size})")
            continue

        # Baseline validation
        target_file = target / entry.relative_path
        if entry.operation == "modify":
            if not target_file.exists():
                baseline_mismatches.append(f"{entry.relative_path}: target_file_missing")
                continue
            current_hash = _hash_file(target_file)
            if current_hash != entry.target_baseline_hash:
                baseline_mismatches.append(
                    f"{entry.relative_path}: target_changed_since_run"
                )
                continue
        elif entry.operation == "create":
            if target_file.exists():
                baseline_mismatches.append(
                    f"{entry.relative_path}: target_file_now_exists"
                )
                continue

        valid_entries.append(entry)

    result.unsupported_files = unsupported
    result.baseline_mismatches = baseline_mismatches

    if blocked_files:
        result.status = "blocked"
        result.blocked_reason = f"blocked_paths: {blocked_files}"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    if baseline_mismatches:
        result.status = "blocked"
        result.blocked_reason = f"baseline_mismatch: {baseline_mismatches}"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    if unsupported:
        result.status = "blocked"
        result.blocked_reason = f"unsupported: {unsupported}"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    if not valid_entries:
        result.status = "blocked"
        result.blocked_reason = "no_valid_artifacts"
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    # --- Dry-run or unapproved: preview only ---
    if dry_run or not approve:
        result.status = "dry_run"
        result.applied_files = [e.relative_path for e in valid_entries]
        result.finished_at = datetime.now(timezone.utc).isoformat()
        return result

    # --- Apply artifacts ---
    applied: list[str] = []
    for entry in valid_entries:
        artifact_file = artifacts_dir / entry.relative_path
        dest = target / entry.relative_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            content = artifact_file.read_bytes()
            dest.write_bytes(content)
            applied.append(entry.relative_path)
        except OSError as exc:
            result.status = "blocked"
            result.blocked_reason = f"write_failed: {entry.relative_path}: {exc}"
            result.applied_files = applied
            result.finished_at = datetime.now(timezone.utc).isoformat()
            return result

    result.applied_files = applied
    result.changed_target_files = applied

    # --- Post-promotion tests ---
    if test_command:
        passed, summary = _run_post_test(test_command, target)
        result.post_test_passed = passed
        result.post_test_summary = summary
        if not passed:
            result.status = "promoted_test_failed"
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _persist_promotion(run_dir, result)
            return result

    result.status = "promoted"
    result.git_status_hint = f"Run 'git status --short' in {target_repo} to see changes."
    result.finished_at = datetime.now(timezone.utc).isoformat()

    # Persist promotion result
    _persist_promotion(run_dir, result)

    return result


def _persist_promotion(run_dir: Path, result: PromotionResult) -> None:
    """Persist promotion result under the run directory."""
    try:
        promo_file = run_dir / "promotion.json"
        data = export_promotion_json(result)
        promo_file.write_text(json.dumps(data, indent=2) + "\n")
    except OSError:
        pass


def load_promotion(run_id: str) -> dict[str, Any] | None:
    """Load promotion result for a run."""
    from packages.orchestration.pingpong_loop import _pingpong_runs_dir
    promo_file = _pingpong_runs_dir() / run_id / "promotion.json"
    if not promo_file.exists():
        return None
    try:
        return json.loads(promo_file.read_text())
    except (OSError, json.JSONDecodeError):
        return None


# ---------------------------------------------------------------------------
# Export / summary
# ---------------------------------------------------------------------------

def export_promotion_json(result: PromotionResult) -> dict[str, Any]:
    """Export promotion result as JSON."""
    return {
        "run_id": result.run_id,
        "promotion_id": result.promotion_id,
        "status": result.status,
        "approved": result.approved,
        "dry_run": result.dry_run,
        "target_repo": result.target_repo,
        "changed_target_files": result.changed_target_files,
        "applied_files": result.applied_files,
        "blocked_reason": result.blocked_reason,
        "baseline_mismatches": result.baseline_mismatches,
        "unsupported_files": result.unsupported_files,
        "post_test_command": result.post_test_command,
        "post_test_passed": result.post_test_passed,
        "post_test_summary": result.post_test_summary,
        "git_status_hint": result.git_status_hint,
        "started_at": result.started_at,
        "finished_at": result.finished_at,
    }


def summarize_promotion(result: PromotionResult) -> str:
    """Human-readable promotion summary."""
    lines = [
        f"Run: {result.run_id}",
        f"Promotion: {result.promotion_id}",
        f"Status: {result.status}",
        f"Approved: {result.approved}",
        f"Target: {result.target_repo}",
    ]

    if result.status == "dry_run":
        lines.append("")
        lines.append("Promotion preview only.")
        lines.append("No target files changed.")
        if result.applied_files:
            lines.append(f"Would apply: {', '.join(result.applied_files)}")
        lines.append(f"To apply: remedy do promote {result.run_id} --repo {result.target_repo} --approve")

    elif result.status == "promoted":
        lines.append(f"Applied files: {', '.join(result.applied_files)}")
        lines.append(f"Changed target files: {', '.join(result.changed_target_files)}")
        if result.post_test_passed is not None:
            lines.append(f"Post-test: {'passed' if result.post_test_passed else 'FAILED'}")
            if result.post_test_summary:
                lines.append(f"  {result.post_test_summary}")
        lines.append(result.git_status_hint)

    elif result.status == "promoted_test_failed":
        lines.append(f"Applied files: {', '.join(result.applied_files)}")
        lines.append("Post-promotion test FAILED")
        if result.post_test_summary:
            lines.append(f"  {result.post_test_summary}")
        lines.append("WARNING: Files were applied but tests failed.")

    elif result.status == "blocked":
        lines.append(f"Blocked: {result.blocked_reason}")
        if result.baseline_mismatches:
            lines.append(f"Baseline mismatches: {', '.join(result.baseline_mismatches)}")
        if result.unsupported_files:
            lines.append(f"Unsupported: {', '.join(result.unsupported_files)}")

    return "\n".join(lines)
