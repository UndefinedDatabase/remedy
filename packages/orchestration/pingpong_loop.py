"""Ping-pong loop — Builder <> Reviewer repair cycle orchestrator.

Runs the core loop:
  1. Builder works (in staging cwd)
  2. Tests run (in staging)
  3. Reviewer reviews (read-only, no staging cwd)
  4. If pass -> done
  5. If findings -> Builder repairs
  6. Repeat until pass, max rounds, timeout, or blocker

All repo mutation happens in staging. Target repo is never modified.
Target snapshot guard enforces this invariant.
"""
from __future__ import annotations

import difflib
import hashlib
import json as _json
import os
import shlex
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from packages.orchestration.pingpong_provider import (
    _REVIEWER_RETRY_PROMPT,
    BuilderOutput,
    ClaudeCliProvider,
    FakeProvider,
    PingPongProvider,
    ReviewerOutput,
    ReviewFinding,
    create_provider,
)

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class PingPongRound:
    """One round of the Builder -> Test -> Reviewer cycle."""
    round_number: int = 0
    builder_output: BuilderOutput | None = None
    test_passed: bool | None = None
    test_summary: str = ""
    reviewer_output: ReviewerOutput | None = None
    repair_prompt: str = ""
    started_at: str = ""
    finished_at: str = ""


@dataclass
class PingPongResult:
    """Complete result of a ping-pong run."""
    run_id: str = field(default_factory=lambda: uuid4().hex[:16])
    job_id: str = ""
    goal: str = ""
    repo_path: str = ""
    mode: str = "staged"
    builder_provider: str = ""
    reviewer_provider: str = ""
    max_rounds: int = 3
    rounds: list[PingPongRound] = field(default_factory=list)
    final_status: str = ""  # staged_review_passed, staged_blocked, max_rounds_reached,
                             # provider_unavailable, test_failed, review_failed,
                             # target_mutation_blocked, builder_no_changes
    staged_files: list[str] = field(default_factory=list)
    changed_target_files: list[str] = field(default_factory=list)
    ignored_target_noise_files: list[str] = field(default_factory=list)
    target_noise_detected: bool = False
    target_mutated: bool = False
    tests_not_run: bool = False
    safe_diff_summary: str = ""
    safe_diff_files: list[str] = field(default_factory=list)
    safe_diff_truncated: bool = False
    staging_path: str = ""
    context_categories: list[str] = field(default_factory=list)
    reviewer_parse_retry_count: int = 0
    reviewer_parse_error: str = ""
    reviewer_malformed_excerpt: str = ""
    reviewer_json_recovered: bool = False
    error: str = ""
    started_at: str = ""
    finished_at: str = ""


# ---------------------------------------------------------------------------
# Context pack v0
# ---------------------------------------------------------------------------

_EXCLUDE_DIRS = frozenset({
    ".git", "node_modules", "venv", ".venv", "__pycache__",
    ".data", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".tox", "dist", "build", ".eggs", ".agent",
})

_MAX_TREE_ENTRIES = 200
_MAX_FILE_CHARS = 8000
_MAX_TOTAL_CONTEXT_CHARS = 100000


def _is_secret_file(name: str) -> bool:
    if name == ".env" or name.startswith(".env.") or name.startswith(".env-"):
        return True
    if name in ("credentials.json", "secrets.json", ".secrets", "api_key.txt"):
        return True
    return False


def build_repo_context(
    repo_path: str,
    goal: str,
    *,
    mentioned_files: list[str] | None = None,
) -> tuple[str, list[str]]:
    """Build a safe, bounded context pack for provider prompts.

    Returns (context_text, categories_included).
    Never includes .env*, secrets, .git, node_modules, caches.
    """
    root = Path(repo_path).resolve()
    categories: list[str] = []
    sections: list[str] = []

    # 1. Goal
    sections.append(f"## Goal\n{goal}\n")
    categories.append("goal")

    # 2. File tree summary
    tree_lines: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _EXCLUDE_DIRS and not d.startswith(".")]
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == ".":
            rel_dir = ""
        for fn in sorted(filenames):
            if _is_secret_file(fn):
                continue
            rel = os.path.join(rel_dir, fn) if rel_dir else fn
            tree_lines.append(rel)
            if len(tree_lines) >= _MAX_TREE_ENTRIES:
                break
        if len(tree_lines) >= _MAX_TREE_ENTRIES:
            tree_lines.append(f"... ({_MAX_TREE_ENTRIES}+ files, truncated)")
            break

    sections.append("## File Tree\n```\n" + "\n".join(tree_lines) + "\n```\n")
    categories.append("file_tree")

    # 3. Mentioned files content
    total_chars = sum(len(s) for s in sections)
    if mentioned_files:
        for mf in mentioned_files:
            fp = root / mf
            if fp.exists() and fp.is_file() and not _is_secret_file(fp.name):
                try:
                    content = fp.read_text(errors="replace")
                    if len(content) > _MAX_FILE_CHARS:
                        content = content[:_MAX_FILE_CHARS] + "\n[TRUNCATED]"
                    total_chars += len(content)
                    if total_chars > _MAX_TOTAL_CONTEXT_CHARS:
                        break
                    sections.append(f"## File: {mf}\n```\n{content}\n```\n")
                except OSError:
                    pass
        categories.append("mentioned_files")

    # 4. README if exists and not too big
    readme = root / "README.md"
    if readme.exists() and "mentioned_files" not in categories:
        try:
            content = readme.read_text(errors="replace")
            if len(content) > _MAX_FILE_CHARS:
                content = content[:_MAX_FILE_CHARS] + "\n[TRUNCATED]"
            sections.append(f"## README.md\n```\n{content}\n```\n")
            categories.append("readme")
        except OSError:
            pass

    return "\n".join(sections), categories


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

_BUILDER_SYSTEM = """\
You are a Builder working on a software task.
Rules:
- Make minimal, focused changes only.
- Do not claim tests passed unless the test runner confirmed it.
- Do not make broad rewrites.
- Only modify files directly relevant to the goal.
- All changes happen in a staging workspace — the real repo is not modified.
- Report what you changed clearly.
"""

_REVIEWER_SYSTEM = """\
You are a code Reviewer.
Review the builder's changes against the original goal.
Be strict but fair. Only flag real issues.
Return ONLY valid JSON. No markdown. No code fence. No explanation outside JSON.
"""


_REPAIR_DIFF_CAP = 20000


def _build_builder_prompt(
    goal: str,
    context: str,
    *,
    round_number: int = 1,
    findings: list[ReviewFinding] | None = None,
    staged_state: str = "",
    safe_diff: str = "",
) -> str:
    parts = [_BUILDER_SYSTEM, "\n", context, "\n"]
    parts.append(f"## Task (Round {round_number})\n{goal}\n")
    if staged_state:
        parts.append(f"## Current Staged State\n{staged_state}\n")
    if safe_diff and findings:
        capped = safe_diff[:_REPAIR_DIFF_CAP]
        if len(safe_diff) > _REPAIR_DIFF_CAP:
            capped += "\n[DIFF TRUNCATED]"
        parts.append(f"## Current Staged Diff\n```diff\n{capped}\n```\n")
    if findings:
        parts.append("## Reviewer Findings to Fix\n")
        for f in findings:
            parts.append(f"- [{f.severity}] {f.id}: {f.summary}")
            if f.required_fix:
                parts.append(f"  Fix: {f.required_fix}")
            parts.append("")
    parts.append("\nProvide your changes and a summary of what you did.")
    return "\n".join(parts)


_REVIEWER_DIFF_CAP = 30000


def _build_reviewer_prompt(
    goal: str,
    builder_summary: str,
    *,
    diff_summary: str = "",
    safe_diff: str = "",
    test_result: str = "",
    files_changed: list[str] | None = None,
) -> str:
    parts = [_REVIEWER_SYSTEM, "\n"]
    parts.append(f"## Original Goal\n{goal}\n")
    parts.append(f"## Builder Summary\n{builder_summary}\n")
    if files_changed:
        parts.append("## Files Changed\n" + "\n".join(f"- {f}" for f in files_changed) + "\n")
    if safe_diff:
        capped = safe_diff[:_REVIEWER_DIFF_CAP]
        if len(safe_diff) > _REVIEWER_DIFF_CAP:
            capped += "\n[DIFF TRUNCATED]"
        parts.append(f"## Staged Unified Diff\n```diff\n{capped}\n```\n")
    elif diff_summary:
        parts.append(f"## Staged Diff\n```\n{diff_summary}\n```\n")
    if test_result:
        parts.append(f"## Test Result\n{test_result}\n")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Staged workspace helpers
# ---------------------------------------------------------------------------

def _create_staging(repo_path: str, run_id: str) -> Path:
    """Create a minimal staging workspace as a filtered copy."""
    staging = Path(f"/tmp/remedy-pingpong-{run_id}")
    if staging.exists():
        shutil.rmtree(staging)
    root = Path(repo_path).resolve()
    staging.mkdir(parents=True)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in _EXCLUDE_DIRS and not d.startswith(".")]
        rel = os.path.relpath(dirpath, root)
        target_dir = staging / rel if rel != "." else staging
        target_dir.mkdir(parents=True, exist_ok=True)
        for fn in filenames:
            if _is_secret_file(fn):
                continue
            src = Path(dirpath) / fn
            dst = target_dir / fn
            try:
                shutil.copy2(src, dst)
            except OSError:
                pass
    return staging


def _find_staging_changes(staging: Path, original: Path) -> list[str]:
    """Find files that differ between staging and original."""
    changed: list[str] = []
    for dirpath, _, filenames in os.walk(staging):
        rel_dir = os.path.relpath(dirpath, staging)
        for fn in filenames:
            rel = os.path.join(rel_dir, fn) if rel_dir != "." else fn
            staging_file = staging / rel
            original_file = original / rel
            if not original_file.exists():
                changed.append(rel)
            else:
                try:
                    if staging_file.read_bytes() != original_file.read_bytes():
                        changed.append(rel)
                except OSError:
                    pass
    return sorted(changed)


def _discard_staging(staging: Path) -> None:
    """Remove staging workspace."""
    if staging.exists():
        shutil.rmtree(staging, ignore_errors=True)


# ---------------------------------------------------------------------------
# Safe diff summary
# ---------------------------------------------------------------------------

_SAFE_DIFF_CAP = 50000
_BINARY_EXTENSIONS = frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".bmp",
    ".zip", ".gz", ".tar", ".bz2", ".xz", ".7z",
    ".whl", ".pyc", ".pyo", ".so", ".dll", ".dylib",
    ".pdf", ".woff", ".woff2", ".ttf", ".eot",
})


def _compute_safe_diff(
    staging: Path,
    original: Path,
    changed_files: list[str],
) -> tuple[str, list[str], bool]:
    """Compute a safe, capped unified diff between original and staging.

    Excludes secret files, binary files, and absolute paths.
    Returns (diff_text, diff_files, truncated).
    """
    if not changed_files:
        return "", [], False

    diff_lines: list[str] = []
    diff_files: list[str] = []
    total_chars = 0
    truncated = False

    for rel in sorted(changed_files):
        if _is_secret_file(os.path.basename(rel)):
            continue
        ext = os.path.splitext(rel)[1].lower()
        if ext in _BINARY_EXTENSIONS:
            diff_lines.append(f"--- a/{rel}\n+++ b/{rel}\n[binary file]\n")
            diff_files.append(rel)
            continue

        orig_file = original / rel
        staged_file = staging / rel

        try:
            if orig_file.exists():
                orig_text = orig_file.read_text(errors="replace").splitlines(keepends=True)
            else:
                orig_text = []
            if staged_file.exists():
                staged_text = staged_file.read_text(errors="replace").splitlines(keepends=True)
            else:
                staged_text = []
        except OSError:
            continue

        file_diff = list(difflib.unified_diff(
            orig_text, staged_text,
            fromfile=f"a/{rel}", tofile=f"b/{rel}",
        ))
        if not file_diff:
            continue

        diff_files.append(rel)
        chunk = "".join(file_diff)
        if total_chars + len(chunk) > _SAFE_DIFF_CAP:
            remaining = _SAFE_DIFF_CAP - total_chars
            if remaining > 0:
                diff_lines.append(chunk[:remaining])
            diff_lines.append("\n[DIFF TRUNCATED]\n")
            truncated = True
            break
        diff_lines.append(chunk)
        total_chars += len(chunk)

    return "".join(diff_lines), diff_files, truncated


# ---------------------------------------------------------------------------
# Target snapshot guard
# ---------------------------------------------------------------------------

_TARGET_IGNORE = frozenset({
    ".pytest_cache", "__pycache__", ".mypy_cache", ".ruff_cache",
})

# Volatile tool-cache directories/patterns — never meaningful target mutations.
_TARGET_NOISE_DIRS = frozenset({
    ".mypy_cache", ".pytest_cache", ".ruff_cache", "__pycache__",
    ".coverage", "htmlcov", "node_modules", "dist", "build", ".cache",
})
_TARGET_NOISE_EXTENSIONS = frozenset({".pyc"})


def _is_target_noise(rel_path: str) -> bool:
    """Return True if rel_path is volatile tool-cache noise, not a real product file."""
    # Directory entries (e.g. ".pytest_cache/")
    stripped = rel_path.rstrip("/")
    if stripped in _TARGET_NOISE_DIRS:
        return True
    # Files inside noise dirs (e.g. ".pytest_cache/v/cache/...")
    top = rel_path.split("/")[0] if "/" in rel_path else ""
    if top in _TARGET_NOISE_DIRS:
        return True
    # Noise file extensions
    ext = os.path.splitext(rel_path)[1].lower()
    if ext in _TARGET_NOISE_EXTENSIONS:
        return True
    return False


def _snapshot_target(repo_path: Path) -> dict[str, bytes]:
    """Take a lightweight snapshot of target repo: {rel_path: content_hash}."""
    snap: dict[str, bytes] = {}
    for dirpath, dirnames, filenames in os.walk(repo_path):
        dirnames[:] = [
            d for d in dirnames
            if d not in _EXCLUDE_DIRS and d not in _TARGET_IGNORE and not d.startswith(".")
        ]
        rel_dir = os.path.relpath(dirpath, repo_path)
        for fn in filenames:
            rel = os.path.join(rel_dir, fn) if rel_dir != "." else fn
            fp = Path(dirpath) / fn
            try:
                snap[rel] = hashlib.sha256(fp.read_bytes()).digest()
            except OSError:
                pass
    return snap


def _check_target_mutation(
    repo_path: Path, before: dict[str, bytes],
) -> tuple[list[str], list[str]]:
    """Compare current target state against snapshot.

    Returns (meaningful_changes, noise_changes).
    Noise = volatile cache dirs/files that don't indicate real product mutation.
    """
    after = _snapshot_target(repo_path)
    all_changes: list[str] = []

    for rel, digest in after.items():
        if rel not in before:
            all_changes.append(rel)
        elif before[rel] != digest:
            all_changes.append(rel)

    for rel in before:
        if rel not in after:
            all_changes.append(rel)

    # Snapshot skips _TARGET_IGNORE dirs, so flag any that exist now as changes
    for artifact_dir in _TARGET_IGNORE:
        entry = artifact_dir + "/"
        if (repo_path / artifact_dir).exists() and entry not in all_changes:
            all_changes.append(entry)

    meaningful: list[str] = []
    noise: list[str] = []
    for rel in sorted(all_changes):
        if _is_target_noise(rel):
            noise.append(rel)
        else:
            meaningful.append(rel)

    return meaningful, noise


# ---------------------------------------------------------------------------
# Fake staging mutation (for FakeProvider)
# ---------------------------------------------------------------------------

def _apply_fake_builder_changes(
    staging: Path,
    builder_output: BuilderOutput,
    goal: str,
) -> None:
    """Apply deterministic changes to staging for fake provider."""
    for rel_path in builder_output.files_changed:
        fp = staging / rel_path
        fp.parent.mkdir(parents=True, exist_ok=True)
        if fp.exists():
            content = fp.read_text(errors="replace")
            content += f"\n\n<!-- Remedy: {goal} -->\n"
            fp.write_text(content)
        else:
            fp.write_text(f"# {rel_path}\n\n<!-- Remedy: {goal} -->\n")


# ---------------------------------------------------------------------------
# Core loop
# ---------------------------------------------------------------------------

def run_pingpong(
    goal: str,
    repo_path: str,
    *,
    builder_provider: PingPongProvider | None = None,
    reviewer_provider: PingPongProvider | None = None,
    builder_name: str = "fake",
    reviewer_name: str = "fake",
    max_rounds: int = 3,
    timeout_sec: int = 120,
    max_output_chars: int = 50000,
    mentioned_files: list[str] | None = None,
    test_command: str = "",
    keep_staging: bool = False,
    claude_cli_write_mode: str = "none",
) -> PingPongResult:
    """Run the Builder <> Reviewer ping-pong loop.

    All mutation happens in staging. Target repo is never modified.
    Target snapshot guard enforces this.
    """
    result = PingPongResult(
        goal=goal,
        repo_path=str(Path(repo_path).resolve()),
        builder_provider=builder_name,
        reviewer_provider=reviewer_name,
        max_rounds=max_rounds,
        started_at=datetime.now(timezone.utc).isoformat(),
    )

    original = Path(repo_path).resolve()

    # --- Target snapshot BEFORE anything runs ---
    target_snap = _snapshot_target(original)

    # Create staging BEFORE providers (so Builder cwd can be set)
    staging = _create_staging(repo_path, result.run_id)

    # Create providers — ClaudeCliProvider Builder gets cwd=staging
    if builder_provider is None:
        try:
            builder_provider = _create_provider_with_cwd(
                builder_name, role="builder", staging_dir=str(staging),
                write_mode=claude_cli_write_mode,
            )
        except RuntimeError as exc:
            result.final_status = "provider_unavailable"
            result.error = str(exc)
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _discard_staging(staging)
            return result

    # Reviewer: no staging cwd (read-only, prompt-only)
    if reviewer_provider is None:
        try:
            reviewer_provider = _create_provider_with_cwd(
                reviewer_name, role="reviewer", staging_dir=None,
            )
        except RuntimeError as exc:
            result.final_status = "provider_unavailable"
            result.error = str(exc)
            result.finished_at = datetime.now(timezone.utc).isoformat()
            _discard_staging(staging)
            return result

    # Build context
    context, categories = build_repo_context(
        repo_path, goal, mentioned_files=mentioned_files,
    )
    result.context_categories = categories

    is_fake = isinstance(builder_provider, FakeProvider)
    has_test_command = bool(test_command)

    try:
        findings: list[ReviewFinding] = []

        for round_num in range(1, max_rounds + 1):
            rd = PingPongRound(
                round_number=round_num,
                started_at=datetime.now(timezone.utc).isoformat(),
            )

            # --- Builder phase ---
            # Compute repair diff for builder (from previous round)
            repair_diff = ""
            if round_num > 1 and result.staged_files and staging.exists():
                rd_repair, _, _ = _compute_safe_diff(
                    staging, original, result.staged_files,
                )
                repair_diff = rd_repair
            builder_prompt = _build_builder_prompt(
                goal, context,
                round_number=round_num,
                findings=findings if round_num > 1 else None,
                staged_state="" if round_num == 1 else f"Files changed: {result.staged_files}",
                safe_diff=repair_diff,
            )
            builder_out = builder_provider.build(
                builder_prompt,
                timeout_sec=timeout_sec,
                max_output_chars=max_output_chars,
            )
            rd.builder_output = builder_out

            if builder_out.error:
                rd.finished_at = datetime.now(timezone.utc).isoformat()
                result.rounds.append(rd)
                result.final_status = "provider_unavailable"
                result.error = builder_out.error
                break

            # Apply changes to staging (fake provider applies deterministically)
            if is_fake:
                _apply_fake_builder_changes(staging, builder_out, goal)

            # --- Target snapshot check after Builder ---
            meaningful, noise = _check_target_mutation(original, target_snap)
            if noise:
                result.ignored_target_noise_files = sorted(set(result.ignored_target_noise_files) | set(noise))
                result.target_noise_detected = True
            if meaningful:
                # Compute staged evidence before blocking
                result.staged_files = _find_staging_changes(staging, original)
                rd.finished_at = datetime.now(timezone.utc).isoformat()
                result.rounds.append(rd)
                result.final_status = "target_mutation_blocked"
                result.target_mutated = True
                result.changed_target_files = meaningful
                result.error = f"Builder mutated target repo: {meaningful}"
                break

            # Track staged files
            result.staged_files = _find_staging_changes(staging, original)

            # --- Builder no-changes check ---
            if not result.staged_files and round_num == 1 and not is_fake:
                rd.finished_at = datetime.now(timezone.utc).isoformat()
                result.rounds.append(rd)
                result.final_status = "builder_no_changes"
                result.error = "Builder produced no file changes in staging"
                break

            # --- Test phase ---
            if has_test_command:
                rd.test_passed, rd.test_summary = _run_test_command(
                    test_command, staging, timeout_sec=timeout_sec,
                )
            else:
                rd.test_passed = None
                rd.test_summary = "tests_not_run"
                result.tests_not_run = True

            # If explicit test command failed, stop
            if has_test_command and not rd.test_passed:
                rd.finished_at = datetime.now(timezone.utc).isoformat()
                result.rounds.append(rd)
                result.final_status = "test_failed"
                result.error = rd.test_summary
                break

            # --- Target snapshot check after tests ---
            meaningful, noise = _check_target_mutation(original, target_snap)
            if noise:
                result.ignored_target_noise_files = sorted(set(result.ignored_target_noise_files) | set(noise))
                result.target_noise_detected = True
            if meaningful:
                rd.finished_at = datetime.now(timezone.utc).isoformat()
                result.rounds.append(rd)
                result.final_status = "target_mutation_blocked"
                result.target_mutated = True
                result.changed_target_files = meaningful
                result.error = f"Test execution mutated target repo: {meaningful}"
                break

            # --- Reviewer phase ---
            diff_summary = "\n".join(f"M {f}" for f in result.staged_files)
            # Compute safe diff for reviewer (before reviewer runs)
            reviewer_safe_diff = ""
            if result.staged_files and staging.exists():
                rd_diff, _, _ = _compute_safe_diff(
                    staging, original, result.staged_files,
                )
                reviewer_safe_diff = rd_diff
            reviewer_prompt = _build_reviewer_prompt(
                goal,
                builder_out.summary,
                diff_summary=diff_summary,
                safe_diff=reviewer_safe_diff,
                test_result=rd.test_summary,
                files_changed=result.staged_files,
            )

            # Snapshot staging before reviewer (to detect reviewer mutation)
            staging_snap_before = _find_staging_changes(staging, original)

            reviewer_out = reviewer_provider.review(
                reviewer_prompt,
                timeout_sec=timeout_sec,
                max_output_chars=max_output_chars,
            )

            # --- Bounded parse retry (one attempt) ---
            if reviewer_out.error and reviewer_out.error.startswith("malformed_output:"):
                result.reviewer_parse_retry_count += 1
                result.reviewer_parse_error = reviewer_out.error
                result.reviewer_malformed_excerpt = reviewer_out.raw_text[:300]
                retry_prompt = _REVIEWER_RETRY_PROMPT.format(
                    excerpt=reviewer_out.raw_text[:500],
                )
                retry_out = reviewer_provider.review(
                    retry_prompt,
                    timeout_sec=timeout_sec,
                    max_output_chars=max_output_chars,
                )
                retry_out.parse_retried = True
                if not retry_out.error:
                    retry_out.parse_retry_recovered = True
                    result.reviewer_json_recovered = True
                reviewer_out = retry_out

            rd.reviewer_output = reviewer_out

            # --- Target snapshot check after Reviewer ---
            meaningful, noise = _check_target_mutation(original, target_snap)
            if noise:
                result.ignored_target_noise_files = sorted(set(result.ignored_target_noise_files) | set(noise))
                result.target_noise_detected = True
            if meaningful:
                rd.finished_at = datetime.now(timezone.utc).isoformat()
                result.rounds.append(rd)
                result.final_status = "target_mutation_blocked"
                result.target_mutated = True
                result.changed_target_files = meaningful
                result.error = f"Reviewer mutated target repo: {meaningful}"
                break

            # Detect reviewer staging mutation
            staging_snap_after = _find_staging_changes(staging, original)
            reviewer_staging_changes = set(staging_snap_after) - set(staging_snap_before)
            if reviewer_staging_changes:
                rd.finished_at = datetime.now(timezone.utc).isoformat()
                result.rounds.append(rd)
                result.final_status = "review_failed"
                result.error = f"Reviewer mutated staging: {sorted(reviewer_staging_changes)}"
                break

            if reviewer_out.error:
                rd.finished_at = datetime.now(timezone.utc).isoformat()
                result.rounds.append(rd)
                result.final_status = "review_failed"
                result.error = reviewer_out.error
                break

            rd.finished_at = datetime.now(timezone.utc).isoformat()
            result.rounds.append(rd)

            if reviewer_out.verdict == "pass":
                result.final_status = "staged_review_passed"
                break
            elif reviewer_out.verdict == "blocked":
                result.final_status = "staged_blocked"
                break
            elif reviewer_out.verdict in ("needs_repair", "fail"):
                findings = reviewer_out.findings
                if round_num >= max_rounds:
                    result.final_status = "max_rounds_reached"
                    break
                # Continue to next round with repair
            else:
                result.final_status = "review_failed"
                result.error = f"Unknown verdict: {reviewer_out.verdict}"
                break

        if not result.final_status:
            result.final_status = "max_rounds_reached"

    finally:
        # --- Final target snapshot check ---
        if not result.target_mutated:
            meaningful, noise = _check_target_mutation(original, target_snap)
            if noise:
                result.ignored_target_noise_files = sorted(set(result.ignored_target_noise_files) | set(noise))
                result.target_noise_detected = True
            if meaningful:
                result.final_status = "target_mutation_blocked"
                result.target_mutated = True
                result.changed_target_files = meaningful
                result.error = f"Target mutated during run: {meaningful}"

        # --- Staged evidence (always compute before discard, even on block) ---
        if not result.staged_files:
            result.staged_files = _find_staging_changes(staging, original)
        if result.staged_files and staging.exists():
            diff_text, diff_files, diff_trunc = _compute_safe_diff(
                staging, original, result.staged_files,
            )
            result.safe_diff_summary = diff_text
            result.safe_diff_files = diff_files
            result.safe_diff_truncated = diff_trunc

        # --- Persist artifacts for promotion (before discard) ---
        if (result.staged_files
                and staging.exists()
                and result.final_status == "staged_review_passed"):
            from packages.orchestration.pingpong_promote import persist_artifacts
            run_dir = _pingpong_runs_dir() / result.run_id
            run_dir.mkdir(parents=True, exist_ok=True)
            persist_artifacts(run_dir, staging, original, result.staged_files)

        # Record staging path if retained
        if keep_staging:
            result.staging_path = str(staging)
        else:
            _discard_staging(staging)

    if not result.target_mutated:
        result.changed_target_files = []
    result.finished_at = datetime.now(timezone.utc).isoformat()

    # Persist durable run record (outside target repo)
    _persist_run(result)

    return result


def _create_provider_with_cwd(
    name: str,
    *,
    role: str,
    staging_dir: str | None,
    write_mode: str = "none",
) -> PingPongProvider:
    """Create provider with role-appropriate cwd and write mode.

    Builder claude-cli gets cwd=staging_dir and write_mode from CLI.
    Reviewer claude-cli gets cwd=None and write_mode="none" (read-only).
    """
    if name == "claude-cli":
        if role == "builder" and staging_dir:
            return ClaudeCliProvider(cwd=staging_dir, write_mode=write_mode)
        # Reviewer: no cwd, no write permissions
        return ClaudeCliProvider()
    return create_provider(name)


# ---------------------------------------------------------------------------
# Test command execution
# ---------------------------------------------------------------------------

_TEST_OUTPUT_CAP = 10000


def _run_test_command(
    command: str,
    staging: Path,
    *,
    timeout_sec: int = 120,
) -> tuple[bool, str]:
    """Run a test command in the staging workspace.

    Returns (passed, summary). Uses shlex.split — no shell=True.
    """
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
            cwd=str(staging),
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
        # Last few lines for summary
        last_lines = output.strip().splitlines()[-5:]
        summary += " | " + " ".join(last_lines)
    return passed, summary


# ---------------------------------------------------------------------------
# Durable run storage (Remedy data root, NOT target repo)
# ---------------------------------------------------------------------------

def _pingpong_runs_dir() -> Path:
    """Return the ping-pong runs storage directory (Remedy data root)."""
    from packages.orchestration.data_paths import resolve_data_root
    return resolve_data_root() / "pingpong_runs"


def _persist_run(result: PingPongResult) -> Path | None:
    """Persist run result as JSON under <remedy_data_root>/pingpong_runs/<run_id>/."""
    try:
        run_dir = _pingpong_runs_dir() / result.run_id
        run_dir.mkdir(parents=True, exist_ok=True)
        data = export_pingpong_json(result)
        out_file = run_dir / "result.json"
        out_file.write_text(_json.dumps(data, indent=2) + "\n")
        return out_file
    except OSError:
        return None


def load_run(run_id: str) -> dict[str, Any] | None:
    """Load a persisted run result by ID from Remedy data root."""
    result_file = _pingpong_runs_dir() / run_id / "result.json"
    if not result_file.exists():
        return None
    try:
        return _json.loads(result_file.read_text())
    except (OSError, _json.JSONDecodeError):
        return None


def list_runs() -> list[dict[str, str]]:
    """List all persisted run IDs from Remedy data root."""
    runs_dir = _pingpong_runs_dir()
    if not runs_dir.exists():
        return []
    results: list[dict[str, str]] = []
    for entry in sorted(runs_dir.iterdir()):
        if entry.is_dir():
            result_file = entry / "result.json"
            if result_file.exists():
                try:
                    data = _json.loads(result_file.read_text())
                    results.append({
                        "run_id": data.get("run_id", entry.name),
                        "goal": data.get("goal", "")[:80],
                        "status": data.get("final_status", ""),
                        "finished_at": data.get("finished_at", ""),
                    })
                except (OSError, _json.JSONDecodeError):
                    results.append({"run_id": entry.name, "goal": "", "status": "corrupt", "finished_at": ""})
    return results


# ---------------------------------------------------------------------------
# Export / report helpers
# ---------------------------------------------------------------------------


def _build_next_commands(result: PingPongResult) -> dict[str, str]:
    """Build copy-paste next commands with actual run_id."""
    rid = result.run_id
    cmds: dict[str, str] = {
        "report": f"remedy do report {rid}",
        "report_json": f"remedy do report {rid} --json",
        "promote_dry_run": f"remedy do promote {rid} --repo . --dry-run",
        "promote_dry_run_json": f"remedy do promote {rid} --repo . --dry-run --json",
        "promote_approve": f"remedy do promote {rid} --repo . --approve",
        "promote_approve_json": f"remedy do promote {rid} --repo . --approve --json",
    }
    return cmds


def _build_provider_evidence(result: PingPongResult) -> dict[str, Any]:
    """Build provider identity evidence."""
    evidence: dict[str, Any] = {
        "builder_provider": result.builder_provider,
        "reviewer_provider": result.reviewer_provider,
    }
    # Extract per-round provider details from first round if available
    for rd in result.rounds:
        if rd.builder_output and rd.builder_output.provider:
            evidence["builder_provider_kind"] = (
                "external_cli" if "cli" in rd.builder_output.provider else "internal"
            )
            break
    for rd in result.rounds:
        if rd.reviewer_output and rd.reviewer_output.provider:
            evidence["reviewer_provider_kind"] = (
                "external_cli" if "cli" in rd.reviewer_output.provider else "internal"
            )
            break
    return evidence


def _estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token."""
    return max(1, len(text) // 4)


def _build_token_accounting(result: PingPongResult) -> dict[str, Any]:
    """Build honest token accounting — estimated unless actual data available."""
    # Check if any round has actual token usage
    actual_available = False
    total_builder_tokens = 0
    total_reviewer_tokens = 0
    for rd in result.rounds:
        if rd.builder_output and rd.builder_output.tokens_used and rd.builder_output.tokens_used > 0:
            actual_available = True
            total_builder_tokens += rd.builder_output.tokens_used
        if rd.reviewer_output and rd.reviewer_output.tokens_used and rd.reviewer_output.tokens_used > 0:
            actual_available = True
            total_reviewer_tokens += rd.reviewer_output.tokens_used

    diff_tokens = _estimate_tokens(result.safe_diff_summary) if result.safe_diff_summary else 0

    accounting: dict[str, Any] = {
        "kind": "actual" if actual_available else "estimated",
        "actual_tokens_available": actual_available,
        "context_categories": result.context_categories,
        "safe_diff_tokens_estimated": diff_tokens,
    }

    if actual_available:
        accounting["builder_tokens_actual"] = total_builder_tokens
        accounting["reviewer_tokens_actual"] = total_reviewer_tokens
    else:
        accounting["token_note"] = (
            "Claude CLI did not expose actual token usage; values are estimates."
        )

    return accounting


def export_pingpong_json(result: PingPongResult) -> dict[str, Any]:
    """Export result as safe JSON (no raw prompts, no secrets)."""
    rounds = []
    for rd in result.rounds:
        round_data: dict[str, Any] = {
            "round": rd.round_number,
            "started_at": rd.started_at,
            "finished_at": rd.finished_at,
        }
        if rd.builder_output:
            round_data["builder"] = {
                "summary": rd.builder_output.summary[:500],
                "files_changed": rd.builder_output.files_changed,
                "provider": rd.builder_output.provider,
                "duration_ms": rd.builder_output.duration_ms,
                "tokens_used": rd.builder_output.tokens_used,
                "error": rd.builder_output.error,
            }
        round_data["test_passed"] = rd.test_passed
        round_data["test_summary"] = rd.test_summary
        if rd.reviewer_output:
            round_data["reviewer"] = {
                "verdict": rd.reviewer_output.verdict,
                "confidence": rd.reviewer_output.confidence,
                "summary": rd.reviewer_output.summary,
                "finding_count": len(rd.reviewer_output.findings),
                "findings": [
                    {
                        "id": f.id,
                        "severity": f.severity,
                        "file": f.file,
                        "summary": f.summary,
                    }
                    for f in rd.reviewer_output.findings
                ],
                "provider": rd.reviewer_output.provider,
                "duration_ms": rd.reviewer_output.duration_ms,
                "error": rd.reviewer_output.error,
                "parse_retried": rd.reviewer_output.parse_retried,
                "parse_retry_recovered": rd.reviewer_output.parse_retry_recovered,
            }
        rounds.append(round_data)

    report_path = str(_pingpong_runs_dir() / result.run_id / "result.json")

    return {
        "run_id": result.run_id,
        "job_id": result.job_id,
        "goal": result.goal,
        "repo_path": result.repo_path,
        "mode": result.mode,
        "builder_provider": result.builder_provider,
        "reviewer_provider": result.reviewer_provider,
        "max_rounds": result.max_rounds,
        "total_rounds": len(result.rounds),
        "final_status": result.final_status,
        "staged_files": result.staged_files,
        "changed_target_files": result.changed_target_files,
        "ignored_target_noise_files": result.ignored_target_noise_files,
        "target_noise_detected": result.target_noise_detected,
        "target_mutated": result.target_mutated,
        "tests_not_run": result.tests_not_run,
        "context_categories": result.context_categories,
        "reviewer_parse_retry_count": result.reviewer_parse_retry_count,
        "reviewer_parse_error": result.reviewer_parse_error,
        "reviewer_malformed_excerpt": result.reviewer_malformed_excerpt,
        "reviewer_json_recovered": result.reviewer_json_recovered,
        "error": result.error,
        "rounds": rounds,
        "started_at": result.started_at,
        "finished_at": result.finished_at,
        "safe_diff_files": result.safe_diff_files,
        "safe_diff_truncated": result.safe_diff_truncated,
        "safe_diff_summary": result.safe_diff_summary,
        "staging_retained": bool(result.staging_path),
        "staging_path": result.staging_path,
        "report_command": f"remedy do report {result.run_id}",
        "report_json_command": f"remedy do report {result.run_id} --json",
        "report_path": report_path,
        "next_commands": _build_next_commands(result),
        "provider_evidence": _build_provider_evidence(result),
        "token_accounting": _build_token_accounting(result),
    }


def summarize_pingpong(result: PingPongResult) -> str:
    """Human-readable summary of a ping-pong run."""
    lines = [
        f"Run: {result.run_id}",
        f"Goal: {result.goal}",
        f"Mode: {result.mode}",
        f"Builder: {result.builder_provider}",
        f"Reviewer: {result.reviewer_provider}",
        f"Rounds: {len(result.rounds)}/{result.max_rounds}",
        f"Status: {result.final_status}",
    ]
    if result.tests_not_run:
        lines.append("Tests: not run (no --test-command)")
    if result.target_mutated:
        lines.append(f"TARGET MUTATED: {result.changed_target_files}")
    elif result.target_noise_detected:
        lines.append("Target mutation: no meaningful target changes")
        lines.append(f"Ignored target noise: {', '.join(result.ignored_target_noise_files)}")
    if result.reviewer_parse_retry_count > 0:
        if result.reviewer_json_recovered:
            lines.append(f"Reviewer parse: retried {result.reviewer_parse_retry_count}x, recovered")
        else:
            lines.append(f"Reviewer parse: retried {result.reviewer_parse_retry_count}x, NOT recovered")
            if result.reviewer_parse_error:
                lines.append(f"Parse error: {result.reviewer_parse_error}")
    if result.error:
        lines.append(f"Error: {result.error}")
    lines.append("")

    for rd in result.rounds:
        lines.append(f"--- Round {rd.round_number} ---")
        if rd.builder_output:
            lines.append(f"  Builder: {rd.builder_output.summary[:200]}")
            if rd.builder_output.files_changed:
                lines.append(f"  Files: {', '.join(rd.builder_output.files_changed)}")
        if rd.test_passed is None:
            lines.append("  Tests: not run")
        else:
            lines.append(f"  Tests: {'passed' if rd.test_passed else 'failed'} — {rd.test_summary}")
        if rd.reviewer_output:
            lines.append(f"  Reviewer: {rd.reviewer_output.verdict}")
            if rd.reviewer_output.findings:
                for f in rd.reviewer_output.findings:
                    lines.append(f"    [{f.severity}] {f.id}: {f.summary}")
            if rd.reviewer_output.summary:
                lines.append(f"  Summary: {rd.reviewer_output.summary}")
        lines.append("")

    lines.append(f"Staged files: {result.staged_files}")
    lines.append(f"Target mutated: {result.target_mutated}")
    lines.append(f"Changed target files: {result.changed_target_files}")

    if result.safe_diff_files:
        lines.append(f"\nDiff files ({len(result.safe_diff_files)}): {', '.join(result.safe_diff_files)}")
        if result.safe_diff_truncated:
            lines.append("[diff truncated]")
        if result.safe_diff_summary:
            lines.append("\n" + result.safe_diff_summary)

    if result.final_status == "staged_review_passed":
        lines.append("\nResult: STAGED REVIEW PASSED — target not modified (staged mode).")
    elif result.final_status == "max_rounds_reached":
        lines.append(f"\nResult: MAX ROUNDS REACHED ({result.max_rounds}) — review not passed.")
    elif result.final_status == "target_mutation_blocked":
        lines.append("\nResult: TARGET MUTATION BLOCKED — safety guard caught target modification.")
    else:
        lines.append(f"\nResult: {result.final_status}")

    lines.append(f"\nReport: remedy do report {result.run_id}")
    return "\n".join(lines)
