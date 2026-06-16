"""
Context Inspector v1 — "What will the worker see?"

Safe preflight inspection showing file-level included/excluded paths,
inclusion/exclusion reasons, token estimates, policy gates, and readiness.

No raw source content, file bodies, secrets, prompts, MCP config content,
stdout/stderr, or raw diffs in output.

Public API::

    inspect_context(job, events, task_id=None, repo_root=None, budget_tokens=None) -> ContextInspection
    export_context_inspection_json(inspection) -> dict
    summarize_context_inspection(inspection) -> str
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.core.models import Job

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_DEFAULT_BUDGET_TOKENS = 4000
_DEFAULT_MAX_BYTES_PER_FILE = 100_000

# Paths always excluded — never read content
# Pattern-based: any file named .env or .env.* is protected
_PROTECTED_EXACT = frozenset({".env"})
_PROTECTED_PREFIXES = (".env.",)

_PROTECTED_DIRS = frozenset({
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "dist", "build", ".tox", ".mypy_cache", ".pytest_cache",
    ".cache", "vendor", "target", ".data",
})

_UNSUPPORTED_EXTENSIONS = frozenset({
    ".exe", ".dll", ".so", ".dylib",
    ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar",
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".bmp", ".webp",
    ".woff", ".woff2", ".ttf", ".eot",
    ".pyc", ".pyo", ".class",
    ".pem", ".key", ".p12", ".pfx", ".jks",
    ".sqlite", ".sqlite3", ".db",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
})

_SECRET_NAMES = frozenset({
    "id_rsa", "id_ed25519", "id_ecdsa",
    "credentials.json", "service-account.json",
    "secrets.yaml", "secrets.yml",
})

# Manifest/config files — high inclusion priority
_MANIFEST_NAMES = frozenset({
    "package.json", "pyproject.toml", "Cargo.toml", "go.mod",
    "Makefile", "Dockerfile", "docker-compose.yml",
    "setup.py", "setup.cfg", "requirements.txt",
    "tsconfig.json", "vite.config.ts", "webpack.config.js",
})

_README_NAMES = frozenset({
    "README.md", "README.rst", "README.txt", "README",
    "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md",
})

# Source extensions we include
_SOURCE_EXTENSIONS = frozenset({
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs",
    ".java", ".rb", ".sh", ".bash", ".zsh",
})

_CONFIG_EXTENSIONS = frozenset({
    ".toml", ".yaml", ".yml", ".json", ".cfg", ".ini",
    ".md", ".rst", ".txt",
})


# ---------------------------------------------------------------------------
# Data model (Steps 866, 870)
# ---------------------------------------------------------------------------

READINESS_READY = "ready"
READINESS_WARNINGS = "ready_with_warnings"
READINESS_BLOCKED = "blocked"
READINESS_UNKNOWN = "unknown"

BUDGET_WITHIN = "within_budget"
BUDGET_NEAR = "near_budget"
BUDGET_OVER = "over_budget"
BUDGET_UNKNOWN = "unknown_budget"


@dataclass(frozen=True)
class ContextPathEntry:
    """One file in the context inspection."""

    path: str
    included: bool
    reason: str
    category: str  # manifest, readme, source, test, config, protected, unsupported, large, symlink
    size_bytes: int = 0
    estimated_tokens: int = 0


@dataclass(frozen=True)
class ContextBudget:
    """Token budget assessment."""

    limit_tokens: int
    estimated_total_tokens: int
    estimated_total_bytes: int
    status: str  # within_budget, near_budget, over_budget, unknown_budget
    file_count: int = 0
    truncated_count: int = 0


@dataclass(frozen=True)
class ContextPolicyGate:
    """One policy gate status."""

    name: str
    status: str  # enforced, not_enforced, unknown
    reason: str


@dataclass(frozen=True)
class ContextToolingPresence:
    """Agent tooling config presence — no content dumped."""

    pi_exists: bool = False
    claude_exists: bool = False
    mcp_exists: bool = False
    mcp_active_servers: int = 0
    vscode_mcp_exists: bool = False
    vscode_mcp_active_servers: int = 0


@dataclass(frozen=True)
class ContextReadiness:
    """Overall inspection readiness."""

    status: str  # ready, ready_with_warnings, blocked, unknown
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ContextInspection:
    """Full context inspection result."""

    version: int
    job_id: str
    task_id: str
    repo_root_safe: str  # redacted/relative repo root
    included_paths: tuple[ContextPathEntry, ...]
    excluded_paths: tuple[ContextPathEntry, ...]
    protected_paths: tuple[str, ...]
    unsupported_paths: tuple[str, ...]
    budget: ContextBudget
    policy_gates: tuple[ContextPolicyGate, ...]
    tooling: ContextToolingPresence
    readiness: ContextReadiness
    missing_context: list[str] = field(default_factory=list)
    generated_at: str = ""


# ---------------------------------------------------------------------------
# Path classification (Step 867)
# ---------------------------------------------------------------------------


def _is_protected(rel_path: Path) -> bool:
    """Check if path is protected/excluded."""
    name = rel_path.name
    if name in _PROTECTED_EXACT:
        return True
    if any(name.startswith(p) for p in _PROTECTED_PREFIXES):
        return True
    if name in _SECRET_NAMES:
        return True
    for part in rel_path.parts:
        if part in _PROTECTED_DIRS:
            return True
    return False


def _is_unsupported(rel_path: Path) -> bool:
    """Check if extension is unsupported (binary/non-text)."""
    return rel_path.suffix.lower() in _UNSUPPORTED_EXTENSIONS


def _is_path_traversal(path_str: str) -> bool:
    """Check for path traversal — segment-based, not substring."""
    if path_str.startswith("/"):
        return True
    return ".." in Path(path_str).parts


def _classify_path(
    rel_path: Path,
    *,
    size_bytes: int,
    is_symlink: bool,
    max_bytes: int,
    task_target_paths: frozenset[str],
    intent_target_paths: frozenset[str],
    event_target_paths: frozenset[str] = frozenset(),
) -> ContextPathEntry:
    """Classify a single path for inclusion/exclusion."""
    path_str = str(rel_path)

    # Exclusion checks
    if _is_path_traversal(path_str):
        return ContextPathEntry(path=path_str, included=False, reason="path_traversal", category="protected")

    if _is_protected(rel_path):
        return ContextPathEntry(path=path_str, included=False, reason="protected_path", category="protected")

    if _is_unsupported(rel_path):
        return ContextPathEntry(path=path_str, included=False, reason="unsupported_extension", category="unsupported")

    if is_symlink:
        return ContextPathEntry(path=path_str, included=False, reason="symlink_excluded", category="symlink")

    if size_bytes > max_bytes:
        return ContextPathEntry(
            path=path_str, included=False, reason="over_size_limit",
            category="large", size_bytes=size_bytes,
        )

    if size_bytes == 0:
        return ContextPathEntry(path=path_str, included=False, reason="empty_file", category="source")

    # Inclusion with reasons
    estimated_tokens = math.ceil(size_bytes / 4)

    # Determine category and reason
    name = rel_path.name
    if name in _MANIFEST_NAMES:
        return ContextPathEntry(
            path=path_str, included=True, reason="manifest_file",
            category="manifest", size_bytes=size_bytes, estimated_tokens=estimated_tokens,
        )
    if name in _README_NAMES:
        return ContextPathEntry(
            path=path_str, included=True, reason="documentation_file",
            category="readme", size_bytes=size_bytes, estimated_tokens=estimated_tokens,
        )

    # Task/intent target paths
    if path_str in task_target_paths:
        return ContextPathEntry(
            path=path_str, included=True, reason="task_target_path",
            category="source", size_bytes=size_bytes, estimated_tokens=estimated_tokens,
        )
    if path_str in intent_target_paths:
        return ContextPathEntry(
            path=path_str, included=True, reason="patch_intent_target",
            category="source", size_bytes=size_bytes, estimated_tokens=estimated_tokens,
        )
    if path_str in event_target_paths:
        return ContextPathEntry(
            path=path_str, included=True, reason="event_target_path",
            category="source", size_bytes=size_bytes, estimated_tokens=estimated_tokens,
        )

    # Related tests by naming convention
    if "test" in name.lower() or rel_path.parent.name == "tests":
        return ContextPathEntry(
            path=path_str, included=True, reason="related_test_file",
            category="test", size_bytes=size_bytes, estimated_tokens=estimated_tokens,
        )

    # Source files
    if rel_path.suffix.lower() in _SOURCE_EXTENSIONS:
        return ContextPathEntry(
            path=path_str, included=True, reason="source_file",
            category="source", size_bytes=size_bytes, estimated_tokens=estimated_tokens,
        )

    # Config files
    if rel_path.suffix.lower() in _CONFIG_EXTENSIONS:
        return ContextPathEntry(
            path=path_str, included=True, reason="config_file",
            category="config", size_bytes=size_bytes, estimated_tokens=estimated_tokens,
        )

    # Unknown extension — exclude
    return ContextPathEntry(
        path=path_str, included=False, reason="unknown_file_type",
        category="unsupported", size_bytes=size_bytes,
    )


# ---------------------------------------------------------------------------
# Token/budget estimation (Step 869)
# ---------------------------------------------------------------------------


def _compute_budget(
    included: list[ContextPathEntry],
    budget_tokens: int,
) -> ContextBudget:
    """Compute budget assessment from included paths."""
    total_bytes = sum(p.size_bytes for p in included)
    total_tokens = sum(p.estimated_tokens for p in included)

    if budget_tokens <= 0:
        status = BUDGET_UNKNOWN
    elif total_tokens <= budget_tokens * 0.8:
        status = BUDGET_WITHIN
    elif total_tokens <= budget_tokens:
        status = BUDGET_NEAR
    else:
        status = BUDGET_OVER

    return ContextBudget(
        limit_tokens=budget_tokens,
        estimated_total_tokens=total_tokens,
        estimated_total_bytes=total_bytes,
        status=status,
        file_count=len(included),
    )


# ---------------------------------------------------------------------------
# Policy gates (Step 870)
# ---------------------------------------------------------------------------


def _build_policy_gates() -> tuple[ContextPolicyGate, ...]:
    """Build read-only policy gate summaries."""
    return (
        ContextPolicyGate(
            name="protected_paths_enforced",
            status="enforced",
            reason="Protected paths (.env, .data, .git, secrets) are excluded from context.",
        ),
        ContextPolicyGate(
            name="token_budget_assessed",
            status="assessed",
            reason="Token budget assessed and reported. No automatic file trimming.",
        ),
        ContextPolicyGate(
            name="raw_content_redaction",
            status="enforced",
            reason="Context inspector output contains path metadata only, no file contents.",
        ),
        ContextPolicyGate(
            name="no_shell_true",
            status="enforced",
            reason="No shell=True in context inspection or downstream execution.",
        ),
        ContextPolicyGate(
            name="no_mutation_from_inspect",
            status="enforced",
            reason="Context inspection is read-only. No writes, no side effects.",
        ),
        ContextPolicyGate(
            name="source_apply_requires_approval",
            status="enforced",
            reason="Applying changes to source requires approval gate.",
        ),
        ContextPolicyGate(
            name="mcp_inactive_by_default",
            status="enforced",
            reason="MCP servers are configured but inactive by default.",
        ),
    )


# ---------------------------------------------------------------------------
# Tooling awareness (Step 876)
# ---------------------------------------------------------------------------


def _detect_tooling(repo_root: Path | None) -> ContextToolingPresence:
    """Detect agent tooling presence — no content dumped."""
    if repo_root is None or not repo_root.is_dir():
        return ContextToolingPresence()

    pi_exists = (repo_root / ".pi").is_dir()
    claude_exists = (repo_root / ".claude").is_dir()

    mcp_exists = False
    mcp_active = 0
    mcp_path = repo_root / ".mcp.json"
    if mcp_path.is_file():
        mcp_exists = True
        mcp_active = _count_active_mcp_servers(mcp_path)

    vscode_mcp_exists = False
    vscode_mcp_active = 0
    vscode_mcp_path = repo_root / ".vscode" / "mcp.json"
    if vscode_mcp_path.is_file():
        vscode_mcp_exists = True
        vscode_mcp_active = _count_active_mcp_servers(vscode_mcp_path)

    return ContextToolingPresence(
        pi_exists=pi_exists,
        claude_exists=claude_exists,
        mcp_exists=mcp_exists,
        mcp_active_servers=mcp_active,
        vscode_mcp_exists=vscode_mcp_exists,
        vscode_mcp_active_servers=vscode_mcp_active,
    )


def _count_active_mcp_servers(path: Path) -> int:
    """Count active MCP servers from config. Does not dump config content."""
    import json
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return 0
    servers = data.get("mcpServers", data.get("servers", {}))
    if not isinstance(servers, dict):
        return 0
    return sum(
        1 for s in servers.values()
        if isinstance(s, dict) and not s.get("disabled", False)
    )


# ---------------------------------------------------------------------------
# Readiness (Step 866)
# ---------------------------------------------------------------------------


def _assess_readiness(
    included: list[ContextPathEntry],
    excluded: list[ContextPathEntry],
    budget: ContextBudget,
    repo_root: Path | None,
    missing: list[str],
) -> ContextReadiness:
    """Assess whether context is enough to proceed."""
    warnings: list[str] = []
    blockers: list[str] = []

    if not included:
        blockers.append("no_included_files")

    if budget.status == BUDGET_OVER:
        warnings.append("over_token_budget")

    if budget.status == BUDGET_UNKNOWN:
        warnings.append("unknown_budget")

    if repo_root is None:
        warnings.append("no_repo_root")

    manifest_count = sum(1 for p in included if p.category == "manifest")
    if manifest_count == 0:
        warnings.append("no_manifest_files")

    if missing:
        warnings.extend(missing)

    if blockers:
        status = READINESS_BLOCKED
    elif warnings:
        status = READINESS_WARNINGS
    else:
        status = READINESS_READY

    return ContextReadiness(status=status, warnings=warnings, blockers=blockers)


# ---------------------------------------------------------------------------
# Builder (Step 871)
# ---------------------------------------------------------------------------


def _resolve_repo_root(job: Job, explicit_root: Path | None) -> Path | None:
    """Resolve repo root safely. Returns None if unknown."""
    if explicit_root is not None and explicit_root.is_dir():
        return explicit_root

    # Try job metadata
    for artifact in job.artifacts:
        repo_path = artifact.metadata.get("repo_path")
        if isinstance(repo_path, str) and repo_path:
            p = Path(repo_path)
            if p.is_dir():
                return p

    return None


def _collect_task_target_paths(job: Job, task_id: str | None) -> frozenset[str]:
    """Collect target paths from task inputs (safe metadata only)."""
    paths: set[str] = set()
    for task in job.tasks:
        if task_id and str(task.id) != task_id:
            continue
        # Extract paths from task inputs if available
        inputs = task.inputs or {}
        for key in ("target_path", "file_path"):
            val = inputs.get(key, "")
            if isinstance(val, str) and val and not _is_path_traversal(val):
                paths.add(val)
    return frozenset(paths)


def _collect_event_target_paths(events: list[dict[str, Any]]) -> frozenset[str]:
    """Collect target paths from run events (applied changes, patch intents)."""
    paths: set[str] = set()
    for ev in events:
        meta = ev.get("metadata", {})
        if not isinstance(meta, dict):
            continue
        tp = meta.get("target_path", "")
        if isinstance(tp, str) and tp and not _is_path_traversal(tp):
            paths.add(tp)
    return frozenset(paths)


def _collect_intent_target_paths(job: Job) -> frozenset[str]:
    """Collect target paths from patch intents."""
    from packages.orchestration.approval_queue import list_patch_intents
    paths: set[str] = set()
    for intent in list_patch_intents(job):
        tp = intent.get("target_path", "")
        if tp and not _is_path_traversal(tp):
            paths.add(tp)
    return frozenset(paths)


def _walk_repo_shallow(
    repo_root: Path,
    *,
    max_depth: int = 3,
    max_files: int = 500,
) -> list[tuple[Path, int, bool]]:
    """Walk repo shallowly. Returns (relative_path, size_bytes, is_symlink)."""
    results: list[tuple[Path, int, bool]] = []
    count = 0

    for depth in range(max_depth + 1):
        pattern = "/".join(["*"] * (depth + 1))
        for p in repo_root.glob(pattern):
            if count >= max_files:
                return results
            try:
                is_link = p.is_symlink()
                if p.is_file() or is_link:
                    rel = p.relative_to(repo_root)
                    size = p.stat().st_size if not is_link else 0
                    results.append((rel, size, is_link))
                    count += 1
            except (OSError, ValueError):
                continue

    return results


def inspect_context(
    job: Job,
    events: list[dict[str, Any]],
    *,
    task_id: str | None = None,
    repo_root: Path | None = None,
    budget_tokens: int | None = None,
) -> ContextInspection:
    """Build context inspection. Read-only, deterministic, no raw content.

    Args:
        job: Job to inspect.
        events: Run events for the job.
        task_id: Optional task ID to focus inspection.
        repo_root: Explicit repo root path.
        budget_tokens: Token budget limit.
    """
    job_id_str = str(job.id)
    task_id_str = task_id or ""
    effective_budget = budget_tokens or _DEFAULT_BUDGET_TOKENS

    resolved_root = _resolve_repo_root(job, repo_root)
    repo_root_safe = ""
    if resolved_root is not None:
        # Redact to relative-safe representation
        repo_root_safe = resolved_root.name

    task_targets = _collect_task_target_paths(job, task_id)
    intent_targets = _collect_intent_target_paths(job)
    event_targets = _collect_event_target_paths(events)

    included: list[ContextPathEntry] = []
    excluded: list[ContextPathEntry] = []
    protected: list[str] = []
    unsupported: list[str] = []

    if resolved_root is not None:
        entries = _walk_repo_shallow(resolved_root)
        for rel_path, size, is_link in entries:
            entry = _classify_path(
                rel_path,
                size_bytes=size,
                is_symlink=is_link,
                max_bytes=_DEFAULT_MAX_BYTES_PER_FILE,
                task_target_paths=task_targets,
                intent_target_paths=intent_targets,
                event_target_paths=event_targets,
            )
            if entry.included:
                included.append(entry)
            else:
                excluded.append(entry)
                if entry.category == "protected":
                    protected.append(entry.path)
                elif entry.category == "unsupported":
                    unsupported.append(entry.path)

    # Sort included: targets first within category, then stable by path
    _reason_priority = {
        "task_target_path": 0, "patch_intent_target": 1, "event_target_path": 2,
    }
    _cat_order = {"manifest": 0, "readme": 1, "source": 2, "test": 3, "config": 4}
    included.sort(key=lambda e: (
        _cat_order.get(e.category, 9),
        _reason_priority.get(e.reason, 9),
        e.path,
    ))

    budget = _compute_budget(included, effective_budget)

    # Missing context signals
    missing: list[str] = []
    if resolved_root is None:
        missing.append("repo_root_unknown")
    if not job.tasks:
        missing.append("no_tasks")

    tooling = _detect_tooling(resolved_root)
    policy_gates = _build_policy_gates()
    readiness = _assess_readiness(included, excluded, budget, resolved_root, missing)

    return ContextInspection(
        version=1,
        job_id=job_id_str,
        task_id=task_id_str,
        repo_root_safe=repo_root_safe,
        included_paths=tuple(included),
        excluded_paths=tuple(excluded),
        protected_paths=tuple(sorted(set(protected))),
        unsupported_paths=tuple(sorted(set(unsupported))),
        budget=budget,
        policy_gates=policy_gates,
        tooling=tooling,
        readiness=readiness,
        missing_context=missing,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def _export_path_entry(entry: ContextPathEntry) -> dict[str, Any]:
    d: dict[str, Any] = {
        "path": entry.path,
        "included": entry.included,
        "reason": entry.reason,
        "category": entry.category,
    }
    if entry.size_bytes:
        d["size_bytes"] = entry.size_bytes
    if entry.estimated_tokens:
        d["estimated_tokens"] = entry.estimated_tokens
    return d


def export_context_inspection_json(inspection: ContextInspection) -> dict[str, Any]:
    """Export context inspection as safe JSON dict."""
    return {
        "version": inspection.version,
        "job_id": inspection.job_id,
        "task_id": inspection.task_id,
        "repo_root_safe": inspection.repo_root_safe,
        "included_paths": [_export_path_entry(p) for p in inspection.included_paths],
        "excluded_paths": [_export_path_entry(p) for p in inspection.excluded_paths],
        "protected_paths": list(inspection.protected_paths),
        "unsupported_paths": list(inspection.unsupported_paths),
        "budget": {
            "limit_tokens": inspection.budget.limit_tokens,
            "estimated_total_tokens": inspection.budget.estimated_total_tokens,
            "estimated_total_bytes": inspection.budget.estimated_total_bytes,
            "status": inspection.budget.status,
            "file_count": inspection.budget.file_count,
        },
        "policy_gates": [
            {"name": g.name, "status": g.status, "reason": g.reason}
            for g in inspection.policy_gates
        ],
        "tooling": {
            "pi_exists": inspection.tooling.pi_exists,
            "claude_exists": inspection.tooling.claude_exists,
            "mcp_exists": inspection.tooling.mcp_exists,
            "mcp_active_servers": inspection.tooling.mcp_active_servers,
            "vscode_mcp_exists": inspection.tooling.vscode_mcp_exists,
            "vscode_mcp_active_servers": inspection.tooling.vscode_mcp_active_servers,
        },
        "readiness": {
            "status": inspection.readiness.status,
            "warnings": inspection.readiness.warnings,
            "blockers": inspection.readiness.blockers,
        },
        "missing_context": inspection.missing_context,
        "generated_at": inspection.generated_at,
    }


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


def summarize_context_inspection(inspection: ContextInspection) -> str:
    """Human-readable context inspection summary."""
    lines: list[str] = []
    lines.append(f"Context Inspection: {inspection.job_id[:8]}")
    if inspection.task_id:
        lines.append(f"Task: {inspection.task_id[:8]}")
    if inspection.repo_root_safe:
        lines.append(f"Repo: {inspection.repo_root_safe}")

    lines.append(f"Readiness: {inspection.readiness.status}")

    b = inspection.budget
    lines.append(f"Budget: {b.estimated_total_tokens}/{b.limit_tokens} tokens ({b.status})")
    lines.append(f"Files: {b.file_count} included, {len(inspection.excluded_paths)} excluded")

    if inspection.readiness.warnings:
        lines.append(f"Warnings: {', '.join(inspection.readiness.warnings)}")
    if inspection.readiness.blockers:
        lines.append(f"Blockers: {', '.join(inspection.readiness.blockers)}")
    if inspection.missing_context:
        lines.append(f"Missing: {', '.join(inspection.missing_context)}")

    # Top included
    if inspection.included_paths:
        lines.append(f"\nIncluded ({len(inspection.included_paths)}):")
        for p in inspection.included_paths[:20]:
            lines.append(f"  {p.path}  [{p.category}] ~{p.estimated_tokens}t — {p.reason}")
        if len(inspection.included_paths) > 20:
            lines.append(f"  ... and {len(inspection.included_paths) - 20} more")

    # Top excluded
    if inspection.excluded_paths:
        lines.append(f"\nExcluded ({len(inspection.excluded_paths)}):")
        for p in inspection.excluded_paths[:10]:
            lines.append(f"  {p.path}  [{p.category}] — {p.reason}")
        if len(inspection.excluded_paths) > 10:
            lines.append(f"  ... and {len(inspection.excluded_paths) - 10} more")

    # Policy gates
    lines.append(f"\nPolicy Gates ({len(inspection.policy_gates)}):")
    for g in inspection.policy_gates:
        lines.append(f"  [{g.status}] {g.name}")

    # Tooling
    t = inspection.tooling
    tooling_items = []
    if t.pi_exists:
        tooling_items.append(".pi")
    if t.claude_exists:
        tooling_items.append(".claude")
    if t.mcp_exists:
        tooling_items.append(f".mcp.json({t.mcp_active_servers} active)")
    if t.vscode_mcp_exists:
        tooling_items.append(f".vscode/mcp.json({t.vscode_mcp_active_servers} active)")
    if tooling_items:
        lines.append(f"Tooling: {', '.join(tooling_items)}")
    else:
        lines.append("Tooling: none detected")

    return "\n".join(lines)
