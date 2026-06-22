"""Staging Workspace — isolated apply/test/proof before target promotion.

Creates a filtered copy of the target repo, runs all gates in isolation,
and promotes changed files to the real target only after all gates pass.

Design:
  - Filtered copy excludes: .git, .env*, node_modules, venv, __pycache__, .data
  - Symlinks resolving outside repo root are excluded (escape detection)
  - Apply uses patch_apply with target_repo_override (no metadata mutation)
  - Tests run with cwd=staging dir
  - Proof built against staging artifacts
  - Promotion: Markdown-only, prefix-based append-only for existing files
  - Non-markdown files blocked during promotion with blockers recorded
  - Failure discards staging dir entirely — target untouched
"""
from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Directories excluded from filtered copy
_EXCLUDE_DIRS: frozenset[str] = frozenset({
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    ".data", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".tox", "dist", "build", ".eggs",
})


# ---------------------------------------------------------------------------
# Safety helpers
# ---------------------------------------------------------------------------

def _is_env_file(name: str) -> bool:
    """Return True for .env, .env.*, .env-* files."""
    if name == ".env":
        return True
    if name.startswith(".env.") or name.startswith(".env-"):
        return True
    return False


def _should_exclude_dir(name: str) -> bool:
    """Check if a directory name should be excluded from filtered copy."""
    if name in _EXCLUDE_DIRS:
        return True
    # Skip hidden dot-directories
    if name.startswith(".") and name != ".":
        return True
    return False


def _is_symlink_escape(item: Path, repo_root: Path) -> bool:
    """Return True if item is a symlink resolving outside repo_root."""
    if not item.is_symlink():
        return False
    try:
        resolved = item.resolve()
        root_resolved = repo_root.resolve()
        return not resolved.is_relative_to(root_resolved)
    except (OSError, ValueError):
        return True  # Cannot resolve — treat as escape


def _check_path_containment(path: Path, root: Path) -> bool:
    """Return True if resolved path is inside resolved root."""
    try:
        return path.resolve().is_relative_to(root.resolve())
    except (OSError, ValueError):
        return False


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

@dataclass
class StagingWorkspace:
    """Isolated workspace for apply/test/proof gates."""
    staging_dir: Path
    target_repo: Path
    job_id: str
    fulfillment_id: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    files_copied: int = 0
    dirs_copied: int = 0
    excluded_dirs: list[str] = field(default_factory=list)
    excluded_symlinks: list[str] = field(default_factory=list)
    excluded_env_files: list[str] = field(default_factory=list)
    active: bool = True


@dataclass
class StagingApplyRecord:
    """Record of a file applied in staging."""
    relative_path: str
    action: str  # "create" | "modify"
    scope: str = "staged"  # "staged" | "target"
    bytes_written: int = 0
    staged: bool = True
    promoted: bool = False
    promoted_at: str = ""


@dataclass
class PromotionResult:
    """Result of promoting staged changes to target repo."""
    promoted: bool = False
    files_promoted: list[str] = field(default_factory=list)
    files_skipped: list[str] = field(default_factory=list)
    files_blocked: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    reason: str = ""
    promoted_at: str = ""


@dataclass
class StagingResult:
    """Complete result of staged fulfillment cycle."""
    workspace: StagingWorkspace | None = None
    apply_records: list[StagingApplyRecord] = field(default_factory=list)
    test_passed: bool = False
    proof_status: str = ""
    promotion: PromotionResult | None = None
    discarded: bool = False
    discard_reason: str = ""


# ---------------------------------------------------------------------------
# Filtered copy
# ---------------------------------------------------------------------------

def create_staging_workspace(
    target_repo: Path,
    staging_parent: Path,
    job_id: str,
    *,
    fulfillment_id: str = "",
) -> StagingWorkspace:
    """Create a filtered copy of target_repo in an isolated staging directory.

    Copies all files except excluded dirs/patterns. Preserves directory structure.
    Excludes symlinks that resolve outside repo root and .env* files.
    staging_parent should be a Remedy workspace-scoped directory.
    """
    staging_dir = staging_parent / f"staging_{job_id[:16]}"
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)

    files_copied = 0
    dirs_copied = 0
    excluded: list[str] = []
    excluded_symlinks: list[str] = []
    excluded_env_files: list[str] = []

    repo_root_resolved = target_repo.resolve()

    def _copy_tree(src: Path, dst: Path) -> None:
        nonlocal files_copied, dirs_copied
        dst.mkdir(parents=True, exist_ok=True)
        dirs_copied += 1

        for item in sorted(src.iterdir()):
            rel = str(item.relative_to(target_repo))

            # Symlink escape check
            if _is_symlink_escape(item, target_repo):
                excluded_symlinks.append(rel)
                continue

            if item.is_dir():
                if _should_exclude_dir(item.name):
                    excluded.append(rel)
                    continue
                _copy_tree(item, dst / item.name)
            elif item.is_file():
                if _is_env_file(item.name):
                    excluded_env_files.append(rel)
                    continue
                shutil.copy2(str(item), str(dst / item.name))
                files_copied += 1

    _copy_tree(target_repo, staging_dir)

    return StagingWorkspace(
        staging_dir=staging_dir,
        target_repo=target_repo,
        job_id=job_id,
        fulfillment_id=fulfillment_id,
        files_copied=files_copied,
        dirs_copied=dirs_copied,
        excluded_dirs=excluded,
        excluded_symlinks=excluded_symlinks,
        excluded_env_files=excluded_env_files,
    )


# ---------------------------------------------------------------------------
# Find changed files in staging
# ---------------------------------------------------------------------------

def find_staged_changes(workspace: StagingWorkspace) -> list[StagingApplyRecord]:
    """Find files in staging that differ from target or are new."""
    records: list[StagingApplyRecord] = []
    staging = workspace.staging_dir
    target = workspace.target_repo

    for staged_file in sorted(staging.rglob("*")):
        if staged_file.is_dir():
            continue
        rel = staged_file.relative_to(staging)
        target_file = target / rel

        if not target_file.exists():
            records.append(StagingApplyRecord(
                relative_path=str(rel),
                action="create",
                scope="staged",
                bytes_written=staged_file.stat().st_size,
            ))
        else:
            staged_content = staged_file.read_bytes()
            target_content = target_file.read_bytes()
            if staged_content != target_content:
                records.append(StagingApplyRecord(
                    relative_path=str(rel),
                    action="modify",
                    scope="staged",
                    bytes_written=len(staged_content),
                ))

    return records


# ---------------------------------------------------------------------------
# Promotion gate
# ---------------------------------------------------------------------------

def promote_staged_changes(
    workspace: StagingWorkspace,
    apply_records: list[StagingApplyRecord],
    *,
    gates_passed: bool = False,
) -> PromotionResult:
    """Promote staged changes to target repo.

    Only runs if gates_passed=True. Rules:
    - New .md files: copy from staging to target
    - Modified .md files: prefix-based append-only (staged must start with
      exact target content; only the suffix is appended)
    - Non-.md files: BLOCKED (not promoted, recorded in blockers)
    - No file deletions. No overwrites of existing content.
    - Path containment verified for all operations.
    """
    if not gates_passed:
        return PromotionResult(
            promoted=False,
            reason="gates_not_passed",
        )

    if not workspace.active:
        return PromotionResult(
            promoted=False,
            reason="workspace_not_active",
        )

    promoted_files: list[str] = []
    skipped_files: list[str] = []
    blocked_files: list[str] = []
    blockers: list[str] = []
    now = datetime.now(timezone.utc).isoformat()

    for rec in apply_records:
        staged_path = workspace.staging_dir / rec.relative_path
        target_path = workspace.target_repo / rec.relative_path

        if not staged_path.exists():
            skipped_files.append(rec.relative_path)
            continue

        # Path containment check
        if not _check_path_containment(staged_path, workspace.staging_dir):
            blocked_files.append(rec.relative_path)
            blockers.append(f"path_escape:{rec.relative_path}")
            continue
        if not _check_path_containment(target_path, workspace.target_repo):
            blocked_files.append(rec.relative_path)
            blockers.append(f"target_path_escape:{rec.relative_path}")
            continue

        # Non-markdown files are blocked
        if not rec.relative_path.endswith(".md"):
            blocked_files.append(rec.relative_path)
            blockers.append(f"non_markdown:{rec.relative_path}")
            continue

        if rec.action == "create":
            if target_path.exists():
                skipped_files.append(rec.relative_path)
                continue
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(staged_path), str(target_path))
            rec.promoted = True
            rec.promoted_at = now
            rec.scope = "target"
            promoted_files.append(rec.relative_path)

        elif rec.action == "modify":
            if not target_path.exists():
                skipped_files.append(rec.relative_path)
                continue
            # Prefix-based append-only: staged content must start with
            # exact target content. Only the new suffix is appended.
            staged_content = staged_path.read_text(encoding="utf-8")
            target_content = target_path.read_text(encoding="utf-8")

            if not staged_content.startswith(target_content):
                # Staged content doesn't preserve target prefix — blocked
                blocked_files.append(rec.relative_path)
                blockers.append(f"prefix_mismatch:{rec.relative_path}")
                continue

            new_suffix = staged_content[len(target_content):]
            if new_suffix:
                with open(target_path, "a", encoding="utf-8") as f:
                    f.write(new_suffix)

            rec.promoted = True
            rec.promoted_at = now
            rec.scope = "target"
            promoted_files.append(rec.relative_path)

    return PromotionResult(
        promoted=len(promoted_files) > 0,
        files_promoted=promoted_files,
        files_skipped=skipped_files,
        files_blocked=blocked_files,
        blockers=blockers,
        reason="promoted" if promoted_files else "no_changes",
        promoted_at=now,
    )


# ---------------------------------------------------------------------------
# Discard
# ---------------------------------------------------------------------------

def discard_staging(workspace: StagingWorkspace, reason: str = "") -> None:
    """Discard staging workspace entirely. Target repo untouched."""
    if workspace.staging_dir.exists():
        shutil.rmtree(workspace.staging_dir)
    workspace.active = False


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def export_staging_result_json(result: StagingResult) -> dict[str, Any]:
    """Export staging result as safe JSON (no absolute paths)."""
    ws = result.workspace
    promo = result.promotion
    return {
        "staging_active": ws.active if ws else False,
        "files_copied": ws.files_copied if ws else 0,
        "dirs_copied": ws.dirs_copied if ws else 0,
        "excluded_count": len(ws.excluded_dirs) if ws else 0,
        "excluded_symlinks": len(ws.excluded_symlinks) if ws else 0,
        "excluded_env_files": len(ws.excluded_env_files) if ws else 0,
        "apply_count": len(result.apply_records),
        "test_passed": result.test_passed,
        "proof_status": result.proof_status,
        "promoted": promo.promoted if promo else False,
        "files_promoted": promo.files_promoted if promo else [],
        "files_skipped": promo.files_skipped if promo else [],
        "files_blocked": promo.files_blocked if promo else [],
        "blockers": promo.blockers if promo else [],
        "discarded": result.discarded,
        "discard_reason": result.discard_reason,
    }
