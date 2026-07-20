"""
Scope Fences — path-level write restrictions for Remedy jobs (F017).

A job can only write inside declared path fences. Violations produce a
blocking, visible artifact — never a silent skip, never a half-applied
change set.

T001: FenceSpec, load precedence, pure checker, builtin deny list.
T002: applicator enforcement, atomicity, violation Evidence, postmortem.
T003 (future): job field, config keys, CLI display.

Builtin deny list (reviewable constant — additions are visible in diffs):
  .git/                   — git directory (component match: anywhere in path)
  remedy.toml             — project configuration file
  .remedy/                — project configuration directory
  .data/                  — default Remedy data directory
  docs/roadmap/STATUS.md  — execution ledger (A4: human/operator territory)

The effective Remedy data directory (resolved via REMEDY_DATA_DIR, config,
or default .data/) is also denied when it falls inside the worktree.

Case sensitivity: paths are compared as-is. No case folding is applied.
On case-insensitive filesystems (macOS default, Windows), a path differing
only in case will bypass fence checks but the filesystem will still route to
the same file. This is the documented as-is behavior; explicit case folding
is not applied because it would be wrong on case-sensitive Linux filesystems.

Public API::

    FenceSpec              — allow/deny specification
    FenceCheckResult       — outcome of a single path check
    TouchedPath            — one path in a change set with operation and role
    FenceViolation         — one violation with full context
    ChangeSetFenceResult   — outcome of preflight for a complete change set
    FenceViolationError    — typed blocking exception
    BUILTIN_DENY           — always-active deny entries (reviewable constant)
    check_path(path, worktree_root, spec) -> FenceCheckResult
    check_change_set(worktree_root, spec, touched) -> ChangeSetFenceResult
    load_fence_spec(job_fences=None, config_path=None, worktree_root=None) -> FenceSpec
    resolve_effective_builtins(worktree_root) -> tuple[tuple[str, str], ...]
    write_fence_violations_artifact(result, evidence_dir, **ctx) -> Path | None
"""

from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Builtin deny list (reviewable constant — additions visible in diffs)
# ---------------------------------------------------------------------------

# Each entry: (pattern, reason, match_mode).
# match_mode meanings:
#   "prefix"    — path starts with pattern (stripped of trailing /) or equals it
#   "exact"     — path equals pattern exactly
#   "component" — pattern (stripped of trailing /) appears as a path component
#                  ANYWHERE in the path (e.g. .git in vendor/.git/config)
BUILTIN_DENY: tuple[tuple[str, str], ...] = (
    (".git/", "git directory"),
    ("remedy.toml", "project config file"),
    (".remedy/", "project config directory"),
    (".data/", "default Remedy data directory"),
    ("docs/roadmap/STATUS.md", "execution ledger (operator territory)"),
)

# .git/ uses component matching — all others use prefix/exact as before.
_COMPONENT_MATCH_PATTERNS: frozenset[str] = frozenset({".git/"})


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FenceSpec:
    """Path fence specification for a job.

    allow_globs: glob patterns for allowed paths (empty = allow all).
    deny_globs:  glob patterns for denied paths (checked before allow).
    extra_builtin_denies: dynamic builtin denies (e.g. resolved data dir).
    """

    allow_globs: tuple[str, ...] = ()
    deny_globs: tuple[str, ...] = ()
    extra_builtin_denies: tuple[tuple[str, str], ...] = ()


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


def _matches_builtin(
    normalized: str,
    extra: tuple[tuple[str, str], ...] = (),
) -> tuple[bool, str]:
    """Check if a normalized path matches any builtin deny entry.

    Returns (matched, reason).
    """
    parts: list[str] | None = None
    for pattern, reason in (*BUILTIN_DENY, *extra):
        if pattern in _COMPONENT_MATCH_PATTERNS:
            component = pattern.rstrip("/")
            if parts is None:
                parts = normalized.split("/")
            if component in parts:
                return True, f"builtin:{reason}"
        elif pattern.endswith("/"):
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

    is_builtin, builtin_reason = _matches_builtin(
        normalized, spec.extra_builtin_denies
    )
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


def resolve_effective_builtins(
    worktree_root: Path,
) -> tuple[tuple[str, str], ...]:
    """Return dynamic builtin deny entries for the given worktree.

    When the resolved data directory (via REMEDY_DATA_DIR / config / default)
    falls inside the worktree and differs from the static ``.data/`` default,
    an additional deny entry is returned for it.
    """
    try:
        from packages.orchestration.data_paths import resolve_data_root

        data_root = resolve_data_root().resolve()
    except Exception:
        return ()

    resolved_wt = worktree_root.resolve()
    try:
        rel = data_root.relative_to(resolved_wt)
    except ValueError:
        return ()

    rel_str = str(rel).replace("\\", "/")
    if rel_str == ".data":
        return ()

    return ((rel_str + "/", f"effective Remedy data directory ({rel_str}/)"),)


def load_fence_spec(
    *,
    job_fences: dict | None = None,
    config_path: Path | None = None,
    worktree_root: Path | None = None,
) -> FenceSpec:
    """Load FenceSpec with precedence: per-job > [scope] config > defaults.

    Args:
        job_fences: Per-job fence dict with optional ``allow`` and ``deny``
                    lists of glob strings.
        config_path: Path to remedy.toml for reading a ``[remedy.scope]``
                     table.
        worktree_root: Worktree root for resolving dynamic builtin denies.

    Returns:
        Resolved FenceSpec.  Default is empty (allow everything, deny nothing
        beyond builtins).
    """
    extra = ()
    if worktree_root is not None:
        extra = resolve_effective_builtins(worktree_root)

    if job_fences is not None:
        allow = job_fences.get("allow", [])
        deny = job_fences.get("deny", [])
        if isinstance(allow, list) and isinstance(deny, list):
            spec = FenceSpec(
                allow_globs=tuple(str(g) for g in allow),
                deny_globs=tuple(str(g) for g in deny),
                extra_builtin_denies=extra,
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
                    extra_builtin_denies=extra,
                )
                if not spec.allow_globs:
                    logger.warning(
                        "F017: empty allow list in [scope] config — "
                        "treating as allow-all (no path restrictions "
                        "beyond denies)"
                    )
                return spec

    return FenceSpec(extra_builtin_denies=extra)


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


# ---------------------------------------------------------------------------
# Change-set preflight API (T002)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TouchedPath:
    """One path in a change set."""

    path: str
    operation: str  # "create", "modify", "delete", "rename_src", "rename_dst"
    role: str = "target"  # "target", "source", "rename_source", "rename_dest"


@dataclass(frozen=True)
class FenceViolation:
    """One violation with full context."""

    path: str
    normalized: str
    operation: str
    role: str
    reason: str


@dataclass(frozen=True)
class ChangeSetFenceResult:
    """Outcome of preflight for a complete change set."""

    allowed: bool
    violations: tuple[FenceViolation, ...]
    touched_count: int


class FenceViolationError(Exception):
    """Typed blocking exception carrying a stable violation set."""

    def __init__(self, result: ChangeSetFenceResult) -> None:
        self.result = result
        paths = ", ".join(v.path for v in result.violations[:3])
        count = len(result.violations)
        suffix = f" (and {count - 3} more)" if count > 3 else ""
        super().__init__(
            f"F017 scope fence violation: {count} path(s) blocked: "
            f"{paths}{suffix}"
        )


def check_change_set(
    worktree_root: Path,
    spec: FenceSpec,
    touched: list[TouchedPath],
) -> ChangeSetFenceResult:
    """Preflight an entire change set against fence spec.

    Checks every touched path. Collects ALL violations (never short-circuits).
    Returns deterministic ordering by (path, operation).
    """
    violations: list[FenceViolation] = []
    seen: set[tuple[str, str]] = set()

    for tp in touched:
        key = (tp.path, tp.operation)
        if key in seen:
            continue
        seen.add(key)

        result = check_path(tp.path, worktree_root, spec)
        if not result.allowed:
            violations.append(
                FenceViolation(
                    path=tp.path,
                    normalized=_normalize_path(tp.path) if tp.path else "",
                    operation=tp.operation,
                    role=tp.role,
                    reason=result.reason,
                )
            )

    violations.sort(key=lambda v: (v.path, v.operation))

    return ChangeSetFenceResult(
        allowed=len(violations) == 0,
        violations=tuple(violations),
        touched_count=len(seen),
    )


# ---------------------------------------------------------------------------
# Violation Evidence artifact (T002)
# ---------------------------------------------------------------------------


def write_fence_violations_artifact(
    result: ChangeSetFenceResult,
    evidence_dir: Path,
    *,
    applicator: str = "",
    job_id: str = "",
    intent_id: str = "",
) -> Path | None:
    """Write fence_violations.json to evidence_dir. Returns path or None."""
    if result.allowed:
        return None

    evidence_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = evidence_dir / "fence_violations.json"

    payload = {
        "schema": "fence_violations/v1",
        "applicator": applicator,
        "job_id": job_id,
        "intent_id": intent_id,
        "touched_count": result.touched_count,
        "violation_count": len(result.violations),
        "violations": [
            {
                "path": v.path,
                "normalized": v.normalized,
                "operation": v.operation,
                "role": v.role,
                "reason": v.reason,
            }
            for v in result.violations
        ],
    }

    artifact_path.write_text(
        json.dumps(payload, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    return artifact_path
