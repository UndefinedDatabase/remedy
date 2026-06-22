"""Staging Workspace — isolated apply/test/proof before target promotion.

Creates a filtered copy of the target repo, runs all gates in isolation,
and promotes changed files to the real target only after all gates pass.

Design:
  - Filtered copy excludes: .git, .env*, node_modules, venv, __pycache__, .data
  - Apply uses patch_apply with target_repo overridden to staging dir
  - Tests run with cwd=staging dir
  - Proof built against staging artifacts
  - Promotion: copy only changed files from staging to target
  - Markdown append-only for existing target files (no overwrite, no delete)
  - Failure discards staging dir entirely — target untouched
"""
from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Directories/patterns excluded from filtered copy
_EXCLUDE_DIRS: frozenset[str] = frozenset({
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    ".data", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".tox", "dist", "build", ".eggs",
})

_EXCLUDE_PATTERNS: frozenset[str] = frozenset({
    ".env", ".env.local", ".env.production",
})


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

@dataclass
class StagingWorkspace:
    """Isolated workspace for apply/test/proof gates."""
    staging_dir: Path
    target_repo: Path
    job_id: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    files_copied: int = 0
    dirs_copied: int = 0
    excluded_dirs: list[str] = field(default_factory=list)
    active: bool = True


@dataclass
class StagingApplyRecord:
    """Record of a file applied in staging."""
    relative_path: str
    action: str  # "create" | "modify"
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

def _should_exclude(path: Path) -> bool:
    """Check if a path should be excluded from filtered copy."""
    name = path.name
    if name in _EXCLUDE_DIRS:
        return True
    if name in _EXCLUDE_PATTERNS:
        return True
    # Skip hidden dot-directories (but not dot-files like .gitignore)
    if path.is_dir() and name.startswith(".") and name not in ("."):
        return True
    return False


def create_staging_workspace(
    target_repo: Path,
    staging_parent: Path,
    job_id: str,
) -> StagingWorkspace:
    """Create a filtered copy of target_repo in an isolated staging directory.

    Copies all files except excluded dirs/patterns. Preserves directory structure.
    staging_parent should be a tmpdir or workspace-scoped directory.
    """
    staging_dir = staging_parent / f"staging_{job_id[:16]}"
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)

    files_copied = 0
    dirs_copied = 0
    excluded: list[str] = []

    def _copy_tree(src: Path, dst: Path) -> None:
        nonlocal files_copied, dirs_copied
        dst.mkdir(parents=True, exist_ok=True)
        dirs_copied += 1

        for item in sorted(src.iterdir()):
            if _should_exclude(item):
                excluded.append(str(item.relative_to(target_repo)))
                continue
            dest_item = dst / item.name
            if item.is_dir():
                _copy_tree(item, dest_item)
            elif item.is_file():
                shutil.copy2(str(item), str(dest_item))
                files_copied += 1

    _copy_tree(target_repo, staging_dir)

    return StagingWorkspace(
        staging_dir=staging_dir,
        target_repo=target_repo,
        job_id=job_id,
        files_copied=files_copied,
        dirs_copied=dirs_copied,
        excluded_dirs=excluded,
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
                bytes_written=staged_file.stat().st_size,
            ))
        else:
            # Compare content
            staged_content = staged_file.read_bytes()
            target_content = target_file.read_bytes()
            if staged_content != target_content:
                records.append(StagingApplyRecord(
                    relative_path=str(rel),
                    action="modify",
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

    Only runs if gates_passed=True. For each changed file:
    - New files: copy from staging to target
    - Modified .md files: append new content (never overwrite)
    - Modified non-.md files: copy from staging (only .md expected in v0)
    No file deletions. No overwrites of existing content.
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
    now = datetime.now(timezone.utc).isoformat()

    for rec in apply_records:
        staged_path = workspace.staging_dir / rec.relative_path
        target_path = workspace.target_repo / rec.relative_path

        if not staged_path.exists():
            skipped_files.append(rec.relative_path)
            continue

        if rec.action == "create":
            if target_path.exists():
                # Target already has this file — skip (safety)
                skipped_files.append(rec.relative_path)
                continue
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(staged_path), str(target_path))
            rec.promoted = True
            rec.promoted_at = now
            promoted_files.append(rec.relative_path)

        elif rec.action == "modify":
            if not target_path.exists():
                # Target file was deleted between staging and promotion — skip
                skipped_files.append(rec.relative_path)
                continue
            # For .md files: append-only (no overwrite)
            if rec.relative_path.endswith(".md"):
                staged_content = staged_path.read_text(encoding="utf-8")
                target_content = target_path.read_text(encoding="utf-8")
                # Find new content (lines in staged not in target)
                new_lines = []
                target_lines_set = set(target_content.splitlines())
                for line in staged_content.splitlines():
                    if line not in target_lines_set:
                        new_lines.append(line)
                if new_lines:
                    append_text = "\n" + "\n".join(new_lines) + "\n"
                    with open(target_path, "a", encoding="utf-8") as f:
                        f.write(append_text)
                rec.promoted = True
                rec.promoted_at = now
                promoted_files.append(rec.relative_path)
            else:
                # Non-md: direct copy (v0 only expects .md)
                shutil.copy2(str(staged_path), str(target_path))
                rec.promoted = True
                rec.promoted_at = now
                promoted_files.append(rec.relative_path)

    return PromotionResult(
        promoted=len(promoted_files) > 0,
        files_promoted=promoted_files,
        files_skipped=skipped_files,
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
        "apply_count": len(result.apply_records),
        "test_passed": result.test_passed,
        "proof_status": result.proof_status,
        "promoted": promo.promoted if promo else False,
        "files_promoted": promo.files_promoted if promo else [],
        "files_skipped": promo.files_skipped if promo else [],
        "discarded": result.discarded,
        "discard_reason": result.discard_reason,
    }
