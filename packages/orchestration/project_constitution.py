"""
Project Constitution v1 — read-only, deterministic policy extraction.

Extracts structured policy signals from known project files in an attached
target repository.  No command execution, no secrets, no recursive scanning.

Purpose:
  Provide Remedy with a machine-readable description of the project's expected
  commands, risky paths, coding conventions, and approval hints — as a foundation
  for future Context Inspector, Verifier Marketplace, MCP Quarantine, Autonomy Modes,
  and Memory/MemPalace integration.  Not an enforcement layer in v1.

Safety constraints:
  - Read-only.  No subprocess, no shell, no writes.
  - Only reads from a fixed set of known root files.
  - Never reads .env, secrets, credentials, key files.
  - Path boundary enforced via Path.resolve().relative_to() — symlink-safe.
  - Max-lines cap per file to avoid reading huge files.
  - Extraction is purely lexical (string/regex); no eval, no import.

Public API::

    load_project_constitution(repo_root: Path | None) -> ProjectConstitution
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


class ProjectConstitution(BaseModel):
    """Structured policy summary extracted from known project files."""

    source_files: list[str] = Field(default_factory=list)
    """Which known files were successfully read."""

    test_commands: list[str] = Field(default_factory=list)
    """Suggested test invocations detected from project files."""

    build_commands: list[str] = Field(default_factory=list)
    """Suggested build invocations detected from project files."""

    lint_commands: list[str] = Field(default_factory=list)
    """Suggested lint/format invocations detected from project files."""

    forbidden_commands: list[str] = Field(default_factory=list)
    """Commands or patterns explicitly forbidden in project docs."""

    risky_paths: list[str] = Field(default_factory=list)
    """Paths detected as sensitive or high-risk (e.g. .env, migrations/)."""

    protected_paths: list[str] = Field(default_factory=list)
    """Paths that should not be overwritten without explicit approval."""

    doc_paths: list[str] = Field(default_factory=list)
    """Documentation directories detected in the repository."""

    repo_conventions: list[str] = Field(default_factory=list)
    """Conventions extracted from AGENTS.md / CLAUDE.md / README / CONTRIBUTING."""

    approval_rules: list[str] = Field(default_factory=list)
    """Approval / review hints extracted from project docs."""

    definition_of_done: list[str] = Field(default_factory=list)
    """'Done' criteria detected from project docs or tool config."""

    warnings: list[str] = Field(default_factory=list)
    """Non-fatal issues encountered during extraction."""


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Files read from the repo root only (never recursed).
_ROOT_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "pyproject.toml",
    "package.json",
    "Makefile",
    "justfile",
    "tox.ini",
    "pytest.ini",
]

# Never read files whose name matches these prefixes/suffixes (case-insensitive).
_SECRET_PREFIXES = (".env", "secret", "credential", "token", ".netrc", "password")
_SECRET_SUFFIXES = (".key", ".pem", ".p12", ".pfx", ".crt", ".cer")

# Max content lines read per file to avoid reading huge files.
_MAX_LINES = 200

# Max workflow files scanned.
_MAX_WORKFLOWS = 10

# Keywords whose presence in a text line makes it a candidate convention/rule.
_CONVENTION_KEYWORDS = re.compile(
    r"\b(do not|never|must not|forbidden|required|always|must|"
    r"test with|run tests|run lint|format with|approved by|review required|"
    r"before merging|before submitting|do not modify)\b",
    re.IGNORECASE,
)

_APPROVAL_KEYWORDS = re.compile(
    r"\b(approval|approved|review|reviewer|must be reviewed|"
    r"require.*approval|sign.?off|lgtm)\b",
    re.IGNORECASE,
)

_DOC_DIRS = ["docs", "doc", "documentation", "wiki"]
_COMMON_PROTECTED = [
    "pyproject.toml",
    "package.json",
    "package-lock.json",
    "requirements.txt",
    ".github/workflows",
]
_COMMON_RISKY = [
    ".env",
    ".env.local",
    ".env.production",
    "migrations",
    "secrets",
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_project_constitution(repo_root: Path | None) -> ProjectConstitution:
    """Extract a ProjectConstitution from a repo directory.

    Returns a constitution with appropriate warnings if ``repo_root`` is None,
    does not exist, or is not a directory.  All extraction is read-only and
    deterministic.

    Args:
        repo_root: Absolute path to the target repository root, or None.

    Returns:
        A populated ProjectConstitution.  Never raises.
    """
    if repo_root is None:
        return ProjectConstitution(warnings=["no attached repo — constitution unavailable"])

    repo_root = Path(repo_root)
    if not repo_root.exists():
        return ProjectConstitution(
            warnings=[f"attached repo does not exist: {repo_root}"]
        )
    if not repo_root.is_dir():
        return ProjectConstitution(
            warnings=[f"attached repo path is not a directory: {repo_root}"]
        )

    source_files: list[str] = []
    test_commands: list[str] = []
    build_commands: list[str] = []
    lint_commands: list[str] = []
    forbidden_commands: list[str] = []
    risky_paths: list[str] = []
    protected_paths: list[str] = []
    doc_paths: list[str] = []
    repo_conventions: list[str] = []
    approval_rules: list[str] = []
    definition_of_done: list[str] = []
    warnings: list[str] = []

    # ── Detect known paths ────────────────────────────────────────────────
    for name in _DOC_DIRS:
        p = repo_root / name
        if p.is_dir():
            doc_paths.append(name + "/")

    for name in _COMMON_PROTECTED:
        p = repo_root / name
        if p.exists():
            protected_paths.append(name)

    for name in _COMMON_RISKY:
        # Glob for .env* variants
        if name.startswith(".env"):
            for candidate in repo_root.glob(".env*"):
                if _is_safe_path(candidate, repo_root):
                    risky_paths.append(candidate.name)
        else:
            p = repo_root / name
            if p.exists() and _is_safe_path(p, repo_root):
                risky_paths.append(name)

    # Also look for src/ packages/ apps/ as doc/convention signals
    for src_dir in ("src", "packages", "apps", "tests", "test"):
        if (repo_root / src_dir).is_dir():
            if src_dir in ("tests", "test"):
                definition_of_done.append(f"detected test directory: {src_dir}/")

    # ── Read known root files ─────────────────────────────────────────────
    for filename in _ROOT_FILES:
        content = _safe_read(repo_root / filename, repo_root)
        if content is None:
            continue
        source_files.append(filename)

        if filename == "pyproject.toml":
            r = _extract_pyproject(content)
            test_commands.extend(r.get("test", []))
            build_commands.extend(r.get("build", []))
            lint_commands.extend(r.get("lint", []))
            definition_of_done.extend(r.get("done", []))

        elif filename == "package.json":
            r = _extract_package_json(content)
            test_commands.extend(r.get("test", []))
            build_commands.extend(r.get("build", []))
            lint_commands.extend(r.get("lint", []))

        elif filename in ("Makefile", "justfile"):
            r = _extract_makefile(content, prefix="make" if filename == "Makefile" else "just")
            test_commands.extend(r.get("test", []))
            build_commands.extend(r.get("build", []))
            lint_commands.extend(r.get("lint", []))

        elif filename in ("tox.ini", "pytest.ini"):
            if "pytest" not in test_commands:
                test_commands.append("pytest")
            definition_of_done.append(f"detected {filename} — tests expected to pass")

        elif filename in ("AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "README.md"):
            convs, approvals, forbidden = _extract_text_rules(content, filename)
            repo_conventions.extend(convs)
            approval_rules.extend(approvals)
            forbidden_commands.extend(forbidden)

        elif filename == "SECURITY.md":
            approval_rules.append("detected SECURITY.md — security review may be required")

    # ── Scan .github/workflows/ (names only, first N files) ───────────────
    workflows_dir = repo_root / ".github" / "workflows"
    if workflows_dir.is_dir() and _is_safe_path(workflows_dir, repo_root):
        wf_files = sorted(workflows_dir.glob("*.yml"))[:_MAX_WORKFLOWS]
        for wf in wf_files:
            if not _is_safe_path(wf, repo_root):
                continue
            source_files.append(f".github/workflows/{wf.name}")
            content = _safe_read(wf, repo_root)
            if content and "pytest" in content and "pytest" not in test_commands:
                test_commands.append("pytest")
            if content and "npm test" in content and "npm test" not in test_commands:
                test_commands.append("npm test")

    # Deduplicate while preserving order
    test_commands    = _dedup(test_commands)
    build_commands   = _dedup(build_commands)
    lint_commands    = _dedup(lint_commands)
    forbidden_commands = _dedup(forbidden_commands)
    risky_paths      = _dedup(risky_paths)
    protected_paths  = _dedup(protected_paths)
    repo_conventions = _dedup(repo_conventions)
    approval_rules   = _dedup(approval_rules)
    definition_of_done = _dedup(definition_of_done)

    return ProjectConstitution(
        source_files=source_files,
        test_commands=test_commands,
        build_commands=build_commands,
        lint_commands=lint_commands,
        forbidden_commands=forbidden_commands,
        risky_paths=risky_paths,
        protected_paths=protected_paths,
        doc_paths=doc_paths,
        repo_conventions=repo_conventions,
        approval_rules=approval_rules,
        definition_of_done=definition_of_done,
        warnings=warnings,
    )


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def render_constitution(constitution: ProjectConstitution, repo_root: Path | None) -> str:
    """Render a ProjectConstitution as a human-readable plain-text report."""
    _LINE = "─"
    _INFO = "○"
    _WARN = "!"
    _OK   = "✓"

    def _section(title: str) -> str:
        bar = _LINE * (50 - len(title) - 1)
        return f"\n{_LINE}{_LINE} {title} {bar}"

    parts: list[str] = []
    parts.append("Remedy Project Constitution")
    repo_str = str(repo_root) if repo_root else "(no attached repo)"
    parts.append(f"Repo: {repo_str}")
    parts.append(f"Sources: {len(constitution.source_files)} file(s) read")
    if constitution.warnings:
        for w in constitution.warnings:
            parts.append(f"  {_WARN} {w}")

    parts.append(_section("Source files"))
    if constitution.source_files:
        for f in constitution.source_files:
            parts.append(f"  {_OK} {f}")
    else:
        parts.append("  (none found)")

    parts.append(_section("Test commands"))
    if constitution.test_commands:
        for c in constitution.test_commands:
            parts.append(f"  {_INFO} {c}")
    else:
        parts.append("  (none detected)")

    parts.append(_section("Build commands"))
    if constitution.build_commands:
        for c in constitution.build_commands:
            parts.append(f"  {_INFO} {c}")
    else:
        parts.append("  (none detected)")

    parts.append(_section("Lint / format commands"))
    if constitution.lint_commands:
        for c in constitution.lint_commands:
            parts.append(f"  {_INFO} {c}")
    else:
        parts.append("  (none detected)")

    parts.append(_section("Risky / protected paths"))
    for p in constitution.risky_paths:
        parts.append(f"  {_WARN} {p}  (risky)")
    for p in constitution.protected_paths:
        parts.append(f"  {_WARN} {p}  (protected)")
    if not constitution.risky_paths and not constitution.protected_paths:
        parts.append("  (none detected)")

    parts.append(_section("Documentation paths"))
    if constitution.doc_paths:
        for p in constitution.doc_paths:
            parts.append(f"  {_INFO} {p}")
    else:
        parts.append("  (none detected)")

    parts.append(_section("Repo conventions"))
    if constitution.repo_conventions:
        for c in constitution.repo_conventions:
            parts.append(f"  {_INFO} {c}")
    else:
        parts.append("  (none detected)")

    parts.append(_section("Approval hints"))
    if constitution.approval_rules:
        for r in constitution.approval_rules:
            parts.append(f"  {_INFO} {r}")
    else:
        parts.append("  (none detected)")

    parts.append(_section("Forbidden commands"))
    if constitution.forbidden_commands:
        for c in constitution.forbidden_commands:
            parts.append(f"  {_WARN} {c}")
    else:
        parts.append("  (none detected)")

    parts.append(_section("Definition of done"))
    if constitution.definition_of_done:
        for d in constitution.definition_of_done:
            parts.append(f"  {_INFO} {d}")
    else:
        parts.append("  (none detected)")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Extractors (private)
# ---------------------------------------------------------------------------


def _extract_pyproject(content: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {"test": [], "build": [], "lint": [], "done": []}

    # Test tool detection
    if re.search(r"\[tool\.pytest|^\[pytest\]|\bpytest\b", content, re.MULTILINE):
        result["test"].append("pytest")
        result["done"].append("detected pytest configuration — tests must pass")

    # Lint/format tools
    if re.search(r"\[tool\.ruff", content):
        result["lint"].append("ruff check .")
    if re.search(r"\[tool\.mypy", content):
        result["lint"].append("mypy .")
    if re.search(r"\[tool\.black", content):
        result["lint"].append("black .")
    if re.search(r"\[tool\.isort", content):
        result["lint"].append("isort .")
    if re.search(r"\[tool\.flake8|^\[flake8\]", content, re.MULTILINE):
        result["lint"].append("flake8 .")

    # Build system
    if re.search(r"\[build-system\]", content):
        if "hatch" in content:
            result["build"].append("hatch build")
        elif "flit" in content:
            result["build"].append("flit build")
        elif "poetry" in content:
            result["build"].append("poetry build")
        else:
            result["build"].append("python -m build")

    # Scripts section (hatch / pdm style)
    for m in re.finditer(r'^\[tool\.\w+\.scripts\](.+?)(?=^\[|\Z)', content,
                         re.MULTILINE | re.DOTALL):
        block = m.group(1)
        if re.search(r'^\s*test\s*=', block, re.MULTILINE):
            if "pytest" not in result["test"]:
                result["test"].append("pytest")
        if re.search(r'^\s*(lint|check)\s*=', block, re.MULTILINE):
            if not result["lint"]:
                result["lint"].append("(see pyproject.toml scripts)")

    return result


def _extract_package_json(content: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {"test": [], "build": [], "lint": []}
    try:
        data = json.loads(content)
    except (json.JSONDecodeError, ValueError):
        return result
    scripts = data.get("scripts", {})
    if not isinstance(scripts, dict):
        return result
    for key, cmd in scripts.items():
        if not isinstance(cmd, str):
            continue
        # Only use safe, non-empty short commands (avoid shell injection display)
        safe_cmd = cmd.strip()[:80]
        if key == "test":
            result["test"].append(f"npm test  # {safe_cmd}" if safe_cmd != "npm test" else "npm test")
        elif key == "build":
            result["build"].append(f"npm run build")
        elif key in ("lint", "check"):
            result["lint"].append(f"npm run {key}")
        elif key == "format":
            result["lint"].append("npm run format")
    return result


def _extract_makefile(content: str, prefix: str = "make") -> dict[str, list[str]]:
    result: dict[str, list[str]] = {"test": [], "build": [], "lint": []}
    # Makefile targets: lines starting at col 0 with `<target>:`
    target_re = re.compile(r'^([a-zA-Z][\w.-]*):', re.MULTILINE)
    for m in target_re.finditer(content):
        name = m.group(1).lower()
        cmd = f"{prefix} {m.group(1)}"
        if name in ("test", "tests", "check"):
            result["test"].append(cmd)
        elif name in ("build",):
            result["build"].append(cmd)
        elif name in ("lint", "format", "fmt", "typecheck", "mypy", "ruff"):
            result["lint"].append(cmd)
    return result


_FORBIDDEN_PATTERNS = re.compile(
    r"\b(do not run|never run|do not execute|never execute|"
    r"do not use|never use|forbidden|banned|prohibited)\s+[`'\"]?([^\s`'\"]{1,60})",
    re.IGNORECASE,
)


def _extract_text_rules(content: str, filename: str) -> tuple[list[str], list[str], list[str]]:
    """Extract conventions, approval rules, and forbidden commands from a text file."""
    conventions: list[str] = []
    approvals: list[str] = []
    forbidden: list[str] = []

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Cap line length for safety
        display = line[:120]

        if _FORBIDDEN_PATTERNS.search(line):
            m = _FORBIDDEN_PATTERNS.search(line)
            if m:
                cmd = m.group(2)[:60]
                forbidden.append(f"{filename}: {cmd}")

        if _APPROVAL_KEYWORDS.search(line):
            approvals.append(f"{filename}: {display}")

        if _CONVENTION_KEYWORDS.search(line):
            conventions.append(f"{filename}: {display}")

    # Deduplicate and cap
    conventions = _dedup(conventions)[:15]
    approvals   = _dedup(approvals)[:10]
    forbidden   = _dedup(forbidden)[:10]
    return conventions, approvals, forbidden


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _safe_read(path: Path, repo_root: Path) -> str | None:
    """Read a file only if it is within repo_root and is not a secret file.

    Returns None if the file should not be read (out-of-bounds, secret,
    missing, or unreadable).  Caps output at _MAX_LINES lines.
    """
    if not _is_safe_path(path, repo_root):
        return None
    name = path.name.lower()
    if any(name.startswith(p) for p in _SECRET_PREFIXES):
        return None
    if any(name.endswith(s) for s in _SECRET_SUFFIXES):
        return None
    if not path.is_file():
        return None
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        return "\n".join(lines[:_MAX_LINES])
    except OSError:
        return None


def _is_safe_path(path: Path, repo_root: Path) -> bool:
    """Return True iff the resolved path is inside repo_root.

    Resolves symlinks before comparison, so symlink-escape attempts fail.
    """
    try:
        path.resolve().relative_to(repo_root.resolve())
        return True
    except (ValueError, OSError):
        return False


def _dedup(items: list[str]) -> list[str]:
    """Remove duplicates while preserving insertion order."""
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
