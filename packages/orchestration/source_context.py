"""
Source Context Injection v1 — dynamic source context selector for builder calls.

Selects relevant files from the target repo based on signals:
- manifest files (package.json, pyproject.toml, etc.)
- README, AGENTS.md, constitution
- git status
- test files related by name/path
- file names mentioned in task

Budget-aware: respects token policy, max files, max bytes.
Local-first, deterministic, no secrets.

Public API::

    inject_source_context(job, repo_path, *, data_dir) -> SourceContext
    select_relevant_files(repo_path, *, budget, mode) -> list[SelectedFile]
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class SelectedFile:
    """A file selected for context injection."""
    path: str
    category: str  # manifest, readme, source, test, config
    size: int
    estimated_tokens: int
    truncated: bool = False


@dataclass(frozen=True)
class SourceContext:
    """Complete source context pack for builder injection."""
    version: int
    file_count: int
    manifest_count: int
    test_file_count: int
    estimated_tokens: int
    mode: str
    truncated: bool
    selection_hash: str
    files: tuple[SelectedFile, ...]


# Files that should never be included
_DENY_NAMES = frozenset({
    ".env", ".env.local", ".env.production",
    "id_rsa", "id_ed25519", "id_ecdsa",
})

_DENY_EXTENSIONS = frozenset({
    ".pem", ".key", ".p12", ".pfx", ".jks",
    ".sqlite", ".sqlite3", ".db",
    ".exe", ".dll", ".so", ".dylib",
    ".zip", ".tar", ".gz", ".bz2",
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".eot",
    ".pyc", ".pyo", ".class",
})

_DENY_DIRS = frozenset({
    "node_modules", ".git", "__pycache__", ".venv", "venv",
    "dist", "build", ".tox", ".mypy_cache", ".pytest_cache",
    "vendor", ".cache", "target",
})

# Manifest/config files (high priority)
_MANIFEST_NAMES = frozenset({
    "package.json", "pyproject.toml", "Cargo.toml", "go.mod",
    "Makefile", "Dockerfile", "docker-compose.yml",
    "setup.py", "setup.cfg", "requirements.txt",
    "tsconfig.json", "vite.config.ts", "webpack.config.js",
})

# README/docs (high priority)
_README_NAMES = frozenset({
    "README.md", "README.rst", "README.txt", "README",
    "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md",
})


def _is_denied(path: Path) -> bool:
    """Check if a path should be excluded."""
    if path.name in _DENY_NAMES:
        return True
    if path.suffix.lower() in _DENY_EXTENSIONS:
        return True
    for part in path.parts:
        if part in _DENY_DIRS:
            return True
    return False


def _is_text_file(path: Path, max_bytes: int = 100_000) -> bool:
    """Check if file is a readable text file under size limit."""
    try:
        if not path.is_file():
            return False
        size = path.stat().st_size
        if size > max_bytes or size == 0:
            return False
        # Quick binary check
        with open(path, "rb") as f:
            chunk = f.read(512)
            if b"\x00" in chunk:
                return False
        return True
    except (OSError, PermissionError):
        return False


def _estimate_tokens(text: str) -> int:
    """Rough token estimate (~4 chars per token)."""
    return max(1, len(text) // 4)


def select_relevant_files(
    repo_path: Path,
    *,
    budget: int = 4000,
    mode: str = "compact",
    max_files: int = 20,
    max_bytes_per_file: int = 50_000,
) -> list[SelectedFile]:
    """Select relevant files from repo for context injection."""
    if not repo_path.is_dir():
        return []

    candidates: list[tuple[int, Path, str]] = []  # (priority, path, category)

    # Walk repo (shallow — max 3 levels)
    for depth in range(4):
        pattern = "/".join(["*"] * (depth + 1))
        for p in repo_path.glob(pattern):
            if not p.is_file():
                continue
            rel = p.relative_to(repo_path)
            if _is_denied(rel):
                continue

            # Categorize
            if p.name in _MANIFEST_NAMES:
                candidates.append((0, p, "manifest"))
            elif p.name in _README_NAMES:
                candidates.append((1, p, "readme"))
            elif "test" in p.name.lower() or p.parent.name == "tests":
                candidates.append((3, p, "test"))
            elif p.suffix in (".py", ".ts", ".js", ".go", ".rs", ".java", ".rb", ".sh"):
                candidates.append((2, p, "source"))
            elif p.suffix in (".toml", ".yaml", ".yml", ".json", ".cfg", ".ini"):
                candidates.append((4, p, "config"))

    # Sort by priority
    candidates.sort(key=lambda c: (c[0], str(c[1])))

    # Select within budget
    selected: list[SelectedFile] = []
    total_tokens = 0

    for _prio, path, category in candidates[:max_files * 2]:
        if len(selected) >= max_files:
            break
        if not _is_text_file(path, max_bytes_per_file):
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue

        tokens = _estimate_tokens(content)
        truncated = False

        if total_tokens + tokens > budget:
            # Truncate to fit
            remaining = budget - total_tokens
            if remaining < 50:
                break
            content = content[:remaining * 4]
            tokens = remaining
            truncated = True

        rel_path = str(path.relative_to(repo_path))
        selected.append(SelectedFile(
            path=rel_path,
            category=category,
            size=len(content.encode()),
            estimated_tokens=tokens,
            truncated=truncated,
        ))
        total_tokens += tokens

        if total_tokens >= budget:
            break

    return selected


def inject_source_context(
    job: Any,
    repo_path: Path,
    *,
    data_dir: str | None = None,
    budget: int = 4000,
    mode: str = "compact",
) -> SourceContext:
    """Select relevant files and record injection event."""
    files = select_relevant_files(repo_path, budget=budget, mode=mode)

    total_tokens = sum(f.estimated_tokens for f in files)
    manifest_count = sum(1 for f in files if f.category == "manifest")
    test_count = sum(1 for f in files if f.category == "test")
    truncated = any(f.truncated for f in files)

    # Selection hash for determinism check
    hash_input = "|".join(f"{f.path}:{f.size}" for f in files)
    selection_hash = hashlib.md5(hash_input.encode()).hexdigest()[:12]

    ctx = SourceContext(
        version=1,
        file_count=len(files),
        manifest_count=manifest_count,
        test_file_count=test_count,
        estimated_tokens=total_tokens,
        mode=mode,
        truncated=truncated,
        selection_hash=selection_hash,
        files=tuple(files),
    )

    # Record event
    if data_dir is not None:
        from packages.orchestration.timeline import append_run_event
        append_run_event(data_dir, job.id, event="source_context_injected", metadata={
            "file_count": ctx.file_count,
            "manifest_count": ctx.manifest_count,
            "test_file_count": ctx.test_file_count,
            "estimated_tokens": ctx.estimated_tokens,
            "mode": ctx.mode,
            "truncated": ctx.truncated,
            "selection_hash": ctx.selection_hash,
        })

    return ctx
