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
    resolve_fence_spec(worktree_root, job_fences=None) -> FenceSpec
    resolve_fence_spec_effective(worktree_root, job_fences=None) -> EffectiveFenceResult
    resolve_effective_builtins(worktree_root) -> tuple[tuple[str, str], ...]
    BuiltinResolutionResult — typed outcome of dynamic builtin resolution
    EffectiveFenceRule — one effective rule with exact provenance
    EffectiveFenceResult — provenance carrier for resolved fence spec
    FenceConfigError — raised on malformed config (fail closed, not allow-all)
    EnforceResult — outcome of enforce_change_set
    enforce_change_set(worktree_root, touched, **ctx) -> EnforceResult
    write_fence_violations_artifact(result, evidence_dir, **ctx) -> Path | None
"""

from __future__ import annotations

import json
import logging
import os
import uuid
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


@dataclass(frozen=True)
class BuiltinResolutionResult:
    """Typed outcome of dynamic builtin resolution — never silently empty."""

    extra_denies: tuple[tuple[str, str], ...]
    resolved: bool
    error: str = ""


def resolve_effective_builtins(
    worktree_root: Path,
) -> tuple[tuple[str, str], ...]:
    """Return dynamic builtin deny entries for the given worktree.

    When the resolved data directory (via REMEDY_DATA_DIR / config / default)
    falls inside the worktree and differs from the static ``.data/`` default,
    an additional deny entry is returned for it.

    Raises RuntimeError on resolution failure — never silently disables
    a required builtin deny.
    """
    return _resolve_effective_builtins_typed(worktree_root).extra_denies


def _resolve_effective_builtins_typed(
    worktree_root: Path,
) -> BuiltinResolutionResult:
    """Typed resolution — callers needing error detail use this."""
    try:
        from packages.orchestration.data_paths import resolve_data_root

        data_root = resolve_data_root().resolve()
    except Exception as exc:
        raise RuntimeError(
            f"F017: cannot resolve effective builtins — data root "
            f"resolution failed: {exc}"
        ) from exc

    resolved_wt = worktree_root.resolve()
    try:
        rel = data_root.relative_to(resolved_wt)
    except ValueError:
        return BuiltinResolutionResult(extra_denies=(), resolved=True)

    rel_str = str(rel).replace("\\", "/")
    if rel_str == ".data":
        return BuiltinResolutionResult(extra_denies=(), resolved=True)

    extra = ((rel_str + "/", f"effective Remedy data directory ({rel_str}/)"),)
    return BuiltinResolutionResult(extra_denies=extra, resolved=True)


class FenceConfigError(Exception):
    """Raised when scope fence config is malformed — fail closed, not allow-all."""


def _validate_glob_list(items: object, label: str) -> list[str]:
    """Validate that items is a list of strings. Raise FenceConfigError if not."""
    if not isinstance(items, list):
        raise FenceConfigError(
            f"F017: {label} must be a list, got {type(items).__name__}"
        )
    result: list[str] = []
    for i, item in enumerate(items):
        if not isinstance(item, str):
            raise FenceConfigError(
                f"F017: {label}[{i}] must be a string, got {type(item).__name__}"
            )
        trimmed = item.strip()
        if not trimmed:
            raise FenceConfigError(
                f"F017: {label}[{i}] is empty or whitespace-only after trimming"
            )
        result.append(trimmed)
    return result


@dataclass(frozen=True)
class EffectiveFenceRule:
    """One effective rule with exact provenance."""

    pattern: str
    kind: str  # "allow", "deny", "builtin"
    source: str  # "per_job", "environment", "project", "default", "builtin", "dynamic_builtin"
    reason: str = ""


@dataclass(frozen=True)
class EffectiveFenceResult:
    """Provenance carrier for resolved fence spec."""

    spec: FenceSpec
    source: str  # "per-job", "central-config", "defaults" (compat)
    allow_rules: tuple[EffectiveFenceRule, ...] = ()
    deny_rules: tuple[EffectiveFenceRule, ...] = ()
    builtin_rules: tuple[EffectiveFenceRule, ...] = ()
    warnings: tuple[str, ...] = ()
    diagnostics: tuple[str, ...] = ()
    case_sensitivity: str = "as-is"


def load_fence_spec(
    *,
    job_fences: dict | None = None,
    config_path: Path | None = None,
    worktree_root: Path | None = None,
) -> FenceSpec:
    """Load FenceSpec with precedence: per-job > central config > defaults.

    Uses the central config system (env > project TOML > user TOML > default)
    for scope.allow/scope.deny resolution. Env vars REMEDY_SCOPE_ALLOW and
    REMEDY_SCOPE_DENY are properly enforced.

    Raises FenceConfigError if config exists but is malformed or contains
    invalid values — never silently defaults to allow-all on parse error.
    """
    return _load_fence_spec_effective(
        job_fences=job_fences,
        config_path=config_path,
        worktree_root=worktree_root,
    ).spec


def _build_builtin_rules(
    extra: tuple[tuple[str, str], ...] = (),
) -> tuple[EffectiveFenceRule, ...]:
    """Build EffectiveFenceRule records for all builtin and dynamic builtin denies."""
    rules: list[EffectiveFenceRule] = []
    for pattern, reason in BUILTIN_DENY:
        rules.append(EffectiveFenceRule(
            pattern=pattern, kind="builtin", source="builtin", reason=reason,
        ))
    for pattern, reason in extra:
        rules.append(EffectiveFenceRule(
            pattern=pattern, kind="builtin", source="dynamic_builtin",
            reason=_redact_path(reason),
        ))
    return tuple(rules)


def _load_fence_spec_effective(
    *,
    job_fences: dict | None = None,
    config_path: Path | None = None,
    worktree_root: Path | None = None,
) -> EffectiveFenceResult:
    """Internal: resolve fence spec with provenance tracking."""
    extra: tuple[tuple[str, str], ...] = ()
    if worktree_root is not None:
        extra = resolve_effective_builtins(worktree_root)

    builtin_rules = _build_builtin_rules(extra)
    warnings: list[str] = []

    if job_fences is not None:
        allow = _validate_glob_list(job_fences.get("allow", []), "job_fences.allow")
        deny = _validate_glob_list(job_fences.get("deny", []), "job_fences.deny")
        spec = FenceSpec(
            allow_globs=tuple(allow),
            deny_globs=tuple(deny),
            extra_builtin_denies=extra,
        )
        if not spec.allow_globs:
            w = (
                "F017: empty allow list in per-job fences — "
                "treating as allow-all (no path restrictions beyond denies)"
            )
            logger.warning(w)
            warnings.append(w)
        return EffectiveFenceResult(
            spec=spec, source="per-job",
            allow_rules=tuple(
                EffectiveFenceRule(pattern=p, kind="allow", source="per_job")
                for p in allow
            ),
            deny_rules=tuple(
                EffectiveFenceRule(pattern=p, kind="deny", source="per_job")
                for p in deny
            ),
            builtin_rules=builtin_rules,
            warnings=tuple(warnings),
        )

    if config_path is not None:
        from packages.orchestration.config import ConfigSource, load_config

        cfg = load_config(project_path=config_path)
        diagnostics = tuple(cfg.load_report.warnings)

        for d in diagnostics:
            if "Malformed TOML" in d:
                raise FenceConfigError(
                    f"F017: refusing to default to allow-all on malformed config: {d}"
                )

        scope_allow = cfg.get("scope.allow")
        scope_deny = cfg.get("scope.deny")

        if scope_allow is not None or scope_deny is not None:
            allow = _validate_glob_list(
                scope_allow if scope_allow is not None else [], "scope.allow",
            )
            deny = _validate_glob_list(
                scope_deny if scope_deny is not None else [], "scope.deny",
            )
            spec = FenceSpec(
                allow_globs=tuple(allow),
                deny_globs=tuple(deny),
                extra_builtin_denies=extra,
            )
            if not spec.allow_globs and scope_allow is not None:
                w = (
                    "F017: empty allow list in config — "
                    "treating as allow-all (no path restrictions beyond denies)"
                )
                logger.warning(w)
                warnings.append(w)
            _SOURCE_MAP = {
                ConfigSource.ENV: "environment",
                ConfigSource.PROJECT: "project",
                ConfigSource.USER: "user",
                ConfigSource.DEFAULT: "default",
            }
            allow_src = _SOURCE_MAP.get(cfg.get_source("scope.allow"), "project")
            deny_src = _SOURCE_MAP.get(cfg.get_source("scope.deny"), "project")
            return EffectiveFenceResult(
                spec=spec, source="central-config",
                allow_rules=tuple(
                    EffectiveFenceRule(pattern=p, kind="allow", source=allow_src)
                    for p in allow
                ),
                deny_rules=tuple(
                    EffectiveFenceRule(pattern=p, kind="deny", source=deny_src)
                    for p in deny
                ),
                builtin_rules=builtin_rules,
                warnings=tuple(warnings), diagnostics=diagnostics,
            )

        return EffectiveFenceResult(
            spec=FenceSpec(extra_builtin_denies=extra),
            source="defaults", builtin_rules=builtin_rules,
            diagnostics=diagnostics,
        )

    return EffectiveFenceResult(
        spec=FenceSpec(extra_builtin_denies=extra), source="defaults",
        builtin_rules=builtin_rules,
    )


def resolve_fence_spec(
    worktree_root: Path,
    *,
    job_fences: dict | None = None,
) -> FenceSpec:
    """Shared effective-spec resolver used by every production write path.

    Combines per-job fences > central config (env > project > user > default) >
    defaults. Always passes config_path so env vars and project config are
    properly enforced.
    """
    config_path = worktree_root / "remedy.toml"
    return load_fence_spec(
        job_fences=job_fences,
        config_path=config_path,
        worktree_root=worktree_root,
    )


def resolve_fence_spec_effective(
    worktree_root: Path,
    *,
    job_fences: dict | None = None,
) -> EffectiveFenceResult:
    """Public provenance-carrying resolver — used by CLI for source detection."""
    config_path = worktree_root / "remedy.toml"
    return _load_fence_spec_effective(
        job_fences=job_fences,
        config_path=config_path,
        worktree_root=worktree_root,
    )


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

    def __init__(
        self,
        result: ChangeSetFenceResult,
        *,
        effective_result: EffectiveFenceResult | None = None,
        artifact_path: Path | None = None,
        persistence_status: str = "not_attempted",
        secondary_diagnostic: str = "",
    ) -> None:
        self.result = result
        self.effective_result = effective_result
        self.artifact_path = artifact_path
        self.persistence_status = persistence_status
        self.secondary_diagnostic = secondary_diagnostic
        paths = ", ".join(_redact_path(v.path) for v in result.violations[:3])
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
    seen: set[tuple[str, str, str]] = set()

    for tp in touched:
        key = (tp.path, tp.operation, tp.role)
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

    violations.sort(key=lambda v: (v.path, v.operation, v.role))

    return ChangeSetFenceResult(
        allowed=len(violations) == 0,
        violations=tuple(violations),
        touched_count=len(seen),
    )


# ---------------------------------------------------------------------------
# Violation Evidence artifact (T002)
# ---------------------------------------------------------------------------


def _redact_path(path_str: str) -> str:
    """Redact absolute paths to prevent filesystem layout leaks in artifacts."""
    if not path_str:
        return path_str
    if os.path.isabs(path_str):
        return "<abs-redacted>"
    return path_str


def _match_violation_rule(
    v: FenceViolation,
    effective: EffectiveFenceResult | None,
) -> tuple[str, str, str]:
    """Return (matched_rule, rule_kind, rule_source) for a violation."""
    if effective is None:
        return ("", "", "")
    reason = v.reason
    if reason.startswith("denied:builtin:"):
        for r in effective.builtin_rules:
            builtin_tag = f"builtin:{r.reason}"
            if builtin_tag in reason:
                return (r.pattern, r.kind, r.source)
        return ("", "builtin", "builtin")
    if reason.startswith("denied:deny_glob:"):
        matched_pattern = reason.split("denied:deny_glob:", 1)[1]
        for r in effective.deny_rules:
            if r.pattern == matched_pattern:
                return (r.pattern, r.kind, r.source)
        return (matched_pattern, "deny", "")
    if reason.startswith("denied:not_in_allow_list"):
        return ("", "allow", "")
    return ("", "", "")


def _path_kind(path: str) -> str:
    """Classify a path for artifact reporting."""
    if os.path.isabs(path):
        return "absolute"
    if ".." in path.split("/"):
        return "traversal"
    return "relative"


def write_fence_violations_artifact(
    result: ChangeSetFenceResult,
    evidence_dir: Path,
    *,
    applicator: str = "",
    job_id: str = "",
    task_id: str = "",
    run_id: str = "",
    intent_id: str = "",
    effective: EffectiveFenceResult | None = None,
) -> Path | None:
    """Write fence_violations.json to evidence_dir. Returns path or None.

    No-clobber: uuid-based event_id guarantees unique artifact names.
    Atomic write via write_file_atomically (O_NOFOLLOW, O_EXCL, fsync).
    Redacts absolute paths in violation details.
    Persistence failure raises — must block repo mutation.
    """
    if result.allowed:
        return None

    evidence_dir.mkdir(parents=True, exist_ok=True)

    event_id = str(uuid.uuid4())[:8]
    suffix = f"_{event_id}"
    if job_id:
        suffix = f"_{job_id[:12]}{suffix}"
    if applicator:
        suffix = f"{suffix}_{applicator}"
    artifact_name = f"fence_violations{suffix}.json"

    violations_payload = []
    for v in result.violations:
        matched_rule, rule_kind, rule_source = _match_violation_rule(v, effective)
        reason_code = v.reason.split(":")[0] if ":" in v.reason else v.reason
        violations_payload.append({
            "path": _redact_path(v.path),
            "normalized": _redact_path(v.normalized),
            "path_kind": _path_kind(v.path),
            "operation": v.operation,
            "role": v.role,
            "reason_code": reason_code,
            "reason": v.reason,
            "matched_rule": matched_rule,
            "rule_kind": rule_kind,
            "rule_source": rule_source,
        })

    payload: dict = {
        "schema": "fence_violations/v2",
        "schema_version": "2.0.0",
        "event_id": event_id,
        "applicator": applicator,
        "job_id": job_id,
        "task_id": task_id,
        "run_id": run_id,
        "intent_id": intent_id,
        "case_sensitivity": "as-is",
        "touched_count": result.touched_count,
        "violation_count": len(result.violations),
        "violations": violations_payload,
        "persistence_status": "persisted",
        "secondary_persistence_diagnostic": "",
    }
    if effective:
        payload["warnings"] = list(effective.warnings)

    data = (json.dumps(payload, indent=2, sort_keys=False) + "\n").encode("utf-8")

    from packages.common.secure_fs import write_file_atomically

    dir_fd = os.open(
        str(evidence_dir),
        os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        write_file_atomically(dir_fd, artifact_name, data, create_only=True)
    finally:
        os.close(dir_fd)

    return evidence_dir / artifact_name


@dataclass(frozen=True)
class EnforceResult:
    """Outcome of enforce_change_set — carries both check result and artifact path."""

    fence_result: ChangeSetFenceResult
    artifact_path: Path | None = None


def enforce_change_set(
    worktree_root: Path,
    touched: list[TouchedPath],
    *,
    applicator: str = "",
    job_id: str = "",
    task_id: str = "",
    run_id: str = "",
    intent_id: str = "",
    evidence_dir: Path | None = None,
    job_fences: dict | None = None,
) -> EnforceResult:
    """Shared enforcement adapter for all production write paths.

    1. Resolves effective fence spec with provenance (per-job > config > defaults).
    2. Runs change-set preflight.
    3. On violation: writes durable Evidence artifact, raises FenceViolationError.
    4. Artifact persistence failure preserves the primary FenceViolationError —
       repo mutation stays blocked, persistence_status = "failed".
    """
    effective = resolve_fence_spec_effective(worktree_root, job_fences=job_fences)
    fence_result = check_change_set(worktree_root, effective.spec, touched)

    if fence_result.allowed:
        return EnforceResult(fence_result=fence_result)

    edir = evidence_dir
    if edir is None:
        from packages.orchestration.data_paths import resolve_data_root
        edir = resolve_data_root()
    if job_id:
        edir = edir / "jobs" / job_id[:36]

    artifact_path: Path | None = None
    persistence_status = "not_attempted"
    secondary_diagnostic = ""

    try:
        artifact_path = write_fence_violations_artifact(
            fence_result, edir,
            applicator=applicator,
            job_id=job_id,
            task_id=task_id,
            run_id=run_id,
            intent_id=intent_id,
            effective=effective,
        )
        persistence_status = "persisted"
    except Exception as persist_exc:
        persistence_status = "failed"
        raw = str(persist_exc)
        secondary_diagnostic = _redact_path(raw)[:200]
        logger.error(
            "F017: fence violation Evidence persistence failed: %s",
            secondary_diagnostic,
        )

    raise FenceViolationError(
        fence_result,
        effective_result=effective,
        artifact_path=artifact_path,
        persistence_status=persistence_status,
        secondary_diagnostic=secondary_diagnostic,
    )
