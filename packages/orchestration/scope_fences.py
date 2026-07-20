"""
Scope Fences — path-level write restrictions for Remedy jobs (F017).

A job can only write inside declared path fences. Violations produce a
blocking, visible artifact — never a silent skip, never a half-applied
change set.

T001: FenceSpec, load precedence, pure checker, builtin deny list.
T002 (future): applicator enforcement at the choke point.
T003 (future): job field, config keys, CLI display.

Builtin deny list (reviewable constant — additions are visible in diffs):
  .git/                   — git directory
  remedy.toml             — project configuration file
  .remedy/                — project configuration directory
  .data/                  — default Remedy data directory
  docs/roadmap/STATUS.md  — execution ledger (A4: human/operator territory)

Case sensitivity: paths are compared as-is. No case folding is applied.
On case-insensitive filesystems (macOS default, Windows), a path differing
only in case will bypass fence checks but the filesystem will still route to
the same file. This is the documented as-is behavior; explicit case folding
is not applied because it would be wrong on case-sensitive Linux filesystems.

Public API::

    FenceSpec              — allow/deny specification
    FenceCheckResult       — outcome of a single path check
    BUILTIN_DENY           — always-active deny entries (reviewable constant)
    check_path(path, worktree_root, spec) -> FenceCheckResult
    load_fence_spec(job_fences=None, config_path=None) -> FenceSpec
"""

from __future__ import annotations

import logging
import os
import sys
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Builtin deny list (reviewable constant — additions visible in diffs)
# ---------------------------------------------------------------------------

# Each entry: (pattern, reason).
# Entries ending with "/" are directory prefixes: any path starting with the
# prefix, or equal to the prefix without trailing /, is denied.
# Entries without trailing "/" are exact file matches.
BUILTIN_DENY: tuple[tuple[str, str], ...] = (
    (".git/", "git directory"),
    ("remedy.toml", "project config file"),
    (".remedy/", "project config directory"),
    (".data/", "default Remedy data directory"),
    ("docs/roadmap/STATUS.md", "execution ledger (operator territory)"),
)


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FenceSpec:
    """Path fence specification for a job.

    allow_globs: glob patterns for allowed paths (empty = allow all).
    deny_globs:  glob patterns for denied paths (checked before allow).
    """

    allow_globs: tuple[str, ...] = ()
    deny_globs: tuple[str, ...] = ()


@dataclass(frozen=True)
class FenceCheckResult:
    """Outcome of checking one path against fences."""

    allowed: bool
    reason: str


# ---------------------------------------------------------------------------
# Path normalization
# ---------------------------------------------------------------------------


def _normalize_path(path: str) -> str:
    """Normalize a relative path for fence matching.

    Splits on '/', removes empty segments (from '//') and '.' segments.
    Does NOT resolve '..' — those are caught as escapes before matching.
    """
    parts = path.split("/")
    cleaned = [p for p in parts if p and p != "."]
    return "/".join(cleaned)


# ---------------------------------------------------------------------------
# Builtin deny matching
# ---------------------------------------------------------------------------


def _matches_builtin(normalized: str) -> tuple[bool, str]:
    """Check if a normalized path matches any builtin deny entry.

    Returns (matched, reason).
    """
    for pattern, reason in BUILTIN_DENY:
        if pattern.endswith("/"):
            prefix = pattern[:-1]
            if normalized == prefix or normalized.startswith(pattern):
                return True, f"builtin:{reason}"
        else:
            if normalized == pattern:
                return True, f"builtin:{reason}"
    return False, ""


# ---------------------------------------------------------------------------
# Pure path checker
# ---------------------------------------------------------------------------


def check_path(
    path: str,
    worktree_root: Path,
    spec: FenceSpec,
) -> FenceCheckResult:
    """Check whether a path is allowed by the fence spec.

    Read-only: performs no writes. May stat/readlink for symlink resolution
    and worktree escape detection.

    Evaluation order:
      1. Escape detection (empty, absolute, .., symlink) → escapes_worktree
      2. Builtin deny → denied (cannot be overridden by allow globs)
      3. Configured deny globs → denied
      4. Configured allow globs (empty = allow all) → allowed or denied
    """
    if not path:
        return FenceCheckResult(
            allowed=False,
            reason="escapes_worktree:empty_path",
        )

    if os.path.isabs(path):
        return FenceCheckResult(
            allowed=False,
            reason="escapes_worktree:absolute_path",
        )

    normalized = _normalize_path(path)
    if not normalized:
        return FenceCheckResult(
            allowed=False,
            reason="escapes_worktree:empty_path",
        )

    if ".." in normalized.split("/"):
        return FenceCheckResult(
            allowed=False,
            reason="escapes_worktree:dot_dot_traversal",
        )

    resolved_root = worktree_root.resolve()
    resolved_target = (worktree_root / normalized).resolve()
    try:
        resolved_target.relative_to(resolved_root)
    except ValueError:
        return FenceCheckResult(
            allowed=False,
            reason="escapes_worktree:symlink_escape",
        )

    is_builtin, builtin_reason = _matches_builtin(normalized)
    if is_builtin:
        return FenceCheckResult(allowed=False, reason=f"denied:{builtin_reason}")

    for pattern in spec.deny_globs:
        if fnmatch(normalized, pattern):
            return FenceCheckResult(
                allowed=False,
                reason=f"denied:deny_glob:{pattern}",
            )

    if spec.allow_globs:
        for pattern in spec.allow_globs:
            if fnmatch(normalized, pattern):
                return FenceCheckResult(allowed=True, reason="allowed:allow_glob")
        return FenceCheckResult(
            allowed=False,
            reason="denied:not_in_allow_list",
        )

    return FenceCheckResult(allowed=True, reason="allowed:default")


# ---------------------------------------------------------------------------
# Load precedence
# ---------------------------------------------------------------------------


def load_fence_spec(
    *,
    job_fences: dict | None = None,
    config_path: Path | None = None,
) -> FenceSpec:
    """Load FenceSpec with precedence: per-job > [scope] config > defaults.

    Args:
        job_fences: Per-job fence dict with optional ``allow`` and ``deny``
                    lists of glob strings.
        config_path: Path to remedy.toml for reading a ``[remedy.scope]``
                     table.

    Returns:
        Resolved FenceSpec.  Default is empty (allow everything, deny nothing
        beyond builtins).
    """
    if job_fences is not None:
        allow = job_fences.get("allow", [])
        deny = job_fences.get("deny", [])
        if isinstance(allow, list) and isinstance(deny, list):
            spec = FenceSpec(
                allow_globs=tuple(str(g) for g in allow),
                deny_globs=tuple(str(g) for g in deny),
            )
            if not spec.allow_globs:
                logger.warning(
                    "F017: empty allow list in per-job fences — "
                    "treating as allow-all (no path restrictions beyond denies)"
                )
            return spec

    if config_path is not None:
        scope = _read_scope_table(config_path)
        if scope is not None:
            allow = scope.get("allow", [])
            deny = scope.get("deny", [])
            if isinstance(allow, list) and isinstance(deny, list):
                spec = FenceSpec(
                    allow_globs=tuple(str(g) for g in allow),
                    deny_globs=tuple(str(g) for g in deny),
                )
                if not spec.allow_globs:
                    logger.warning(
                        "F017: empty allow list in [scope] config — "
                        "treating as allow-all (no path restrictions "
                        "beyond denies)"
                    )
                return spec

    return FenceSpec()


def _read_scope_table(config_path: Path) -> dict | None:
    """Read the ``[remedy.scope]`` table from a remedy.toml file."""
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        try:
            import tomli as tomllib  # type: ignore[no-redef]
        except ImportError:
            return None

    if not config_path.is_file():
        return None
    try:
        with open(config_path, "rb") as f:
            parsed = tomllib.load(f)
    except Exception:
        return None

    remedy = parsed.get("remedy", {})
    if not isinstance(remedy, dict):
        return None
    scope = remedy.get("scope")
    if isinstance(scope, dict):
        return scope
    return None
