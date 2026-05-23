"""
Project Command Discovery v1 — Step 34.1.

Scans a target repository for test / build / lint / format command candidates
from known project configuration files.  Returns structured CommandCandidate
objects.  **No commands are executed here.  No shell=True.  All argv fields
are immutable tuples of strings.**

Execution of candidates remains fully policy-gated at the CLI / runner layer.

Design:
  Discovery is organised as a registry of detector functions.  Adding support
  for a new ecosystem means adding one detector — no other lists to update.

Supported ecosystems (detectors in priority order):
  constitution  — explicit test_commands from Project Constitution
  makefile      — Makefile targets: test, lint, build, check
  justfile      — justfile / Justfile recipes: test, lint, build
  taskfile      — Taskfile.yml / Taskfile.yaml tasks: test, lint, build
  package_json  — package.json scripts (pnpm / yarn / bun / npm by lockfile)
  pyproject     — pytest / poetry / uv / hatch config or tests/ dir
  cargo         — Cargo.toml presence → cargo test (bounded scan)
  go            — go.mod presence → go test ./... (bounded scan)
  gradle        — build.gradle / gradlew (bounded scan)
  maven         — pom.xml / mvnw (bounded scan)
  dotnet        — *.sln / *.csproj (bounded scan)
  ruby          — Rakefile (bounded scan)
  composer      — composer.json scripts.test (bounded scan)

Safety invariants:
  - No subprocess call anywhere in this module.
  - All source_path values are repo-relative strings (never absolute).
  - Symlinks that escape the repo boundary are not followed.
  - Ignored directories (_SCAN_IGNORE_DIRS) are never walked.
  - Maximum scan depth is bounded by _SCAN_MAX_DEPTH.

Public API::

    discover_commands(job, repo_root) -> list[CommandCandidate]
        Collect all candidates from all detectors.

    select_best_test_candidate(candidates) -> CommandCandidate | None
        Return the single highest-priority, lowest-risk test candidate,
        or None if none qualify for execution.
"""

from __future__ import annotations

import fnmatch
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packages.core.models import Job


# ---------------------------------------------------------------------------
# Scan policy
# ---------------------------------------------------------------------------

# Directories that are never walked during discovery.
# Centralised here — detectors use _find_files which respects this set.
_SCAN_IGNORE_DIRS: frozenset[str] = frozenset({
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "target",       # Rust/Maven build output
    "dist",
    "build",
    ".data",        # Remedy's own data directory
    ".pytest_cache",
    ".tox",
    ".mypy_cache",
    ".ruff_cache",
    "coverage",
    ".coverage",
    ".hg",
    ".svn",
})

# Maximum directory depth to walk (0 = root only, 1 = root + direct children).
_SCAN_MAX_DEPTH: int = 2


# ---------------------------------------------------------------------------
# Purpose and permission mappings
# ---------------------------------------------------------------------------

# Map of well-known script / target names to standard purposes.
_PURPOSE_MAP: dict[str, str] = {
    "test":       "test",
    "tests":      "test",
    "check":      "test",
    "test:ci":    "test",
    "test:unit":  "test",
    "test:e2e":   "test",
    "test:watch": "test",
    "lint":       "lint",
    "lint:ci":    "lint",
    "linting":    "lint",
    "eslint":     "lint",
    "tslint":     "lint",
    "typecheck":  "lint",
    "type-check": "lint",
    "format":     "format",
    "fmt":        "format",
    "prettier":   "format",
    "build":      "build",
    "build:ci":   "build",
    "compile":    "build",
    "bundle":     "build",
    "dist":       "build",
}

# Permission required per purpose.
_PERMISSION_MAP: dict[str, str] = {
    "test":    "repo_test_run",
    "build":   "repo_build_run",
    "lint":    "repo_lint_run",
    "format":  "repo_format_run",
    "unknown": "",
}

# Source-type priority for candidate selection.
# Lower value = higher priority.
# 0: Project Constitution (explicit, authoritative)
# 1: repo-local scripts (Makefile / Justfile / Taskfile)
# 2: ecosystem manifest (package.json, pyproject, cargo, go, gradle, maven, …)
# 3: less common manifests (dotnet, ruby, composer)
# 9: heuristic / unknown
_SOURCE_PRIORITY: dict[str, int] = {
    "constitution": 0,
    "makefile":     1,
    "justfile":     1,
    "taskfile":     1,
    "pyproject":    2,
    "package_json": 2,
    "cargo":        2,
    "go":           2,
    "gradle":       2,
    "maven":        2,
    "dotnet":       3,
    "ruby":         3,
    "composer":     3,
    "heuristic":    9,
}

# Source types whose test commands originate from an explicit, trusted declaration.
_EXPLICIT_SOURCE_TYPES: frozenset[str] = frozenset(
    {"constitution", "pyproject", "cargo", "go", "gradle", "maven"}
)

# Risky patterns: commands that suggest destructive, network, or system-mutating
# intent.  Kept compact and centralised here — not scattered across detectors.
_RISKY_RE: re.compile = re.compile(
    r"\b(?:rm\s+-[rf]+|sudo|curl\s+.*\|\s*(?:sh|bash)|wget\s+.*\|\s*(?:sh|bash)"
    r"|dd\s+|mkfs|docker\s+run\s+--privileged|chmod\s+-[Rr]\s+777"
    r"|deploy|publish|push|kubectl\s+(?:apply|delete)|ansible"
    r"|secrets?|credentials?)\b",
    re.IGNORECASE,
)

# Simpler token check for short strings (script names, argv tokens).
_RISKY_TOKENS_RE: re.compile = re.compile(
    r"\b(?:rm|sudo|curl|wget|ssh|scp|deploy|publish|push"
    r"|docker|kubectl|ansible|mkfs|dd)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Candidate model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CommandCandidate:
    """Structured description of a discovered project command.

    argv is an immutable tuple of strings — never a shell string.
    source_path is always repo-relative (never absolute).
    No subprocess.run call is made here; this is pure data.
    """

    id: str
    purpose: str               # test | build | lint | format | unknown
    argv: tuple[str, ...]      # e.g. ("python3", "-m", "pytest")
    display: str               # human-readable, e.g. "python3 -m pytest"
    source_type: str           # makefile | package_json | pyproject | …
    source_path: str           # repo-relative path, e.g. "Makefile"
    confidence: str            # high | medium | low
    risk: str                  # low | medium | high
    reason: str                # brief explanation
    requires_permission: str   # e.g. "repo_test_run"

    def argv_list(self) -> list[str]:
        """Return argv as a plain list, ready for subprocess.run."""
        return list(self.argv)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def discover_commands(
    job: "Job",
    repo_root: Path,
) -> list[CommandCandidate]:
    """Run all detectors and return deduplicated CommandCandidate list.

    Does not execute any command.  Safe to call at any time.
    Deduplication key: (purpose, argv, source_type) — same argv from different
    sources is intentionally kept so the user can see all origins.
    """
    repo_root = Path(repo_root).resolve()
    all_candidates: list[CommandCandidate] = []
    for detector in _DETECTORS:
        try:
            if detector is _detect_constitution:
                all_candidates.extend(detector(job, repo_root))  # type: ignore[call-arg]
            else:
                all_candidates.extend(detector(repo_root))
        except Exception:
            # A broken detector must never crash discovery.
            pass

    # Deduplicate: (purpose, argv, source_type) is the uniqueness key.
    seen: set[tuple[str, tuple[str, ...], str]] = set()
    result: list[CommandCandidate] = []
    for c in all_candidates:
        key = (c.purpose, c.argv, c.source_type)
        if key not in seen:
            seen.add(key)
            result.append(c)
    return result


def select_best_test_candidate(
    candidates: list[CommandCandidate],
) -> CommandCandidate | None:
    """Return the single best executable test candidate, or None.

    Candidates are ranked by:
      1. source_type priority  (constitution=0 > makefile/justfile/taskfile=1
                                > manifests=2 > uncommon=3 > heuristic=9)
      2. confidence            (high=0 > medium=1 > low=2)
      3. risk                  (low=0 > medium=1 > high excluded)
      4. source_path depth     (shallower wins)
      5. id                    (lexicographic, for stability)

    High-risk candidates are never returned.
    """
    test_candidates = [
        c for c in candidates
        if c.purpose == "test" and c.risk != "high"
    ]
    if not test_candidates:
        return None

    _conf_order = {"high": 0, "medium": 1, "low": 2}
    _risk_order = {"low": 0, "medium": 1}

    def _sort_key(c: CommandCandidate) -> tuple[int, int, int, int, str]:
        src  = _SOURCE_PRIORITY.get(c.source_type, 9)
        conf = _conf_order.get(c.confidence, 9)
        risk = _risk_order.get(c.risk, 9)
        depth = c.source_path.count("/") + c.source_path.count("\\")
        return (src, conf, risk, depth, c.id)

    return min(test_candidates, key=_sort_key)


# ---------------------------------------------------------------------------
# Boundary + scan helpers
# ---------------------------------------------------------------------------


def _is_within_repo(path: Path, repo_root: Path) -> bool:
    """Return True if resolved path stays inside repo_root (no symlink escapes)."""
    try:
        resolved = path.resolve()
        resolved.relative_to(repo_root)
        return True
    except ValueError:
        return False


def _find_files(
    repo_root: Path,
    filename: str,
    max_depth: int = _SCAN_MAX_DEPTH,
) -> list[Path]:
    """Find files named exactly `filename` within repo_root up to max_depth.

    Skips _SCAN_IGNORE_DIRS and does not follow symlinks outside repo_root.
    Returns absolute paths (all within repo_root).
    """
    results: list[Path] = []
    _walk_for_file(repo_root, filename, max_depth, 0, results, repo_root)
    return results


def _find_files_pattern(
    repo_root: Path,
    pattern: str,
    max_depth: int = _SCAN_MAX_DEPTH,
) -> list[Path]:
    """Like _find_files but matches filenames via fnmatch glob pattern."""
    results: list[Path] = []
    _walk_for_pattern(repo_root, pattern, max_depth, 0, results, repo_root)
    return results


def _walk_for_file(
    base: Path,
    filename: str,
    max_depth: int,
    depth: int,
    results: list[Path],
    repo_root: Path,
) -> None:
    try:
        for child in sorted(base.iterdir()):
            if child.is_symlink() and not _is_within_repo(child, repo_root):
                continue
            if child.is_dir():
                if child.name in _SCAN_IGNORE_DIRS:
                    continue
                if depth < max_depth:
                    _walk_for_file(child, filename, max_depth, depth + 1, results, repo_root)
            elif child.is_file() and child.name == filename:
                results.append(child)
    except (PermissionError, OSError):
        pass


def _walk_for_pattern(
    base: Path,
    pattern: str,
    max_depth: int,
    depth: int,
    results: list[Path],
    repo_root: Path,
) -> None:
    try:
        for child in sorted(base.iterdir()):
            if child.is_symlink() and not _is_within_repo(child, repo_root):
                continue
            if child.is_dir():
                if child.name in _SCAN_IGNORE_DIRS:
                    continue
                if depth < max_depth:
                    _walk_for_pattern(child, pattern, max_depth, depth + 1, results, repo_root)
            elif child.is_file() and fnmatch.fnmatch(child.name, pattern):
                results.append(child)
    except (PermissionError, OSError):
        pass


def _rel(path: Path, repo_root: Path) -> str:
    """Return a repo-relative string path, never absolute."""
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return path.name


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _candidate_id(purpose: str, source_type: str, variant: str = "") -> str:
    base = f"{purpose}:{source_type}"
    if variant:
        # Sanitise variant to a safe id fragment.
        safe = re.sub(r"[^a-zA-Z0-9._/-]", "_", variant)[:60]
        base += f":{safe}"
    return base


def _assess_risk(argv: tuple[str, ...], extra_text: str = "") -> str:
    """Return 'low', 'medium', or 'high' based on argv and optional extra context.

    Checks both argv tokens and extra_text (e.g. recipe/script body).
    Known-safe executables with no risky context → 'low'.
    """
    combined = " ".join(argv) + (" " + extra_text if extra_text else "")
    if _RISKY_RE.search(combined) or _RISKY_TOKENS_RE.search(" ".join(argv)):
        return "high"
    # Check extra_text separately (body/script value may contain risky tokens).
    if extra_text and _RISKY_TOKENS_RE.search(extra_text):
        return "high"
    _safe_first = frozenset({
        "python3", "python", "pytest",
        "make", "cargo", "go",
        "just", "task",
        "gradle", "gradlew", "mvn", "mvnw",
        "dotnet",
        "rake", "bundle",
        "composer",
    })
    if argv and argv[0] in _safe_first:
        return "low"
    return "medium"


def _permission_for(purpose: str) -> str:
    return _PERMISSION_MAP.get(purpose, "")


def _parse_makefile(text: str) -> list[tuple[str, str]]:
    """Parse a Makefile into (target_name, recipe_body) tuples.

    Returns only targets whose names appear in _PURPOSE_MAP.
    The recipe_body is the concatenated content of indented lines after the target.
    """
    results: list[tuple[str, str]] = []
    current: str | None = None
    body: list[str] = []

    for line in text.splitlines():
        m = re.match(r'^([a-zA-Z][a-zA-Z0-9_-]*)\s*:', line)
        if m:
            if current is not None:
                results.append((current, "\n".join(body)))
            current = m.group(1)
            body = []
        elif current is not None and (line.startswith("\t") or line.startswith("  ")):
            body.append(line.strip())
        elif current is not None and not line.strip():
            pass  # blank line inside recipe is fine
        else:
            if current is not None:
                results.append((current, "\n".join(body)))
            current = None
            body = []

    if current is not None:
        results.append((current, "\n".join(body)))
    return results


def _js_package_manager(pkg_dir: Path) -> str:
    """Detect JS package manager from lockfiles in the same directory."""
    if (pkg_dir / "pnpm-lock.yaml").is_file():
        return "pnpm"
    if (pkg_dir / "yarn.lock").is_file():
        return "yarn"
    if (pkg_dir / "bun.lock").is_file() or (pkg_dir / "bun.lockb").is_file():
        return "bun"
    if (pkg_dir / "package-lock.json").is_file():
        return "npm"
    return "npm"


# ---------------------------------------------------------------------------
# Detectors
# ---------------------------------------------------------------------------


def _detect_constitution(job: "Job", repo_root: Path) -> list[CommandCandidate]:
    """Extract test/build/lint commands from the Project Constitution."""
    try:
        from packages.orchestration.project_constitution import load_project_constitution
        constitution = load_project_constitution(repo_root)
        candidates: list[CommandCandidate] = []
        for purpose, commands in (
            ("test",  constitution.test_commands),
            ("build", constitution.build_commands),
            ("lint",  constitution.lint_commands),
        ):
            for cmd in commands:
                stripped = cmd.strip()
                if not stripped:
                    continue
                parts = tuple(stripped.split())
                risk = _assess_risk(parts)
                candidates.append(CommandCandidate(
                    id=_candidate_id(purpose, "constitution", stripped[:40]),
                    purpose=purpose,
                    argv=parts,
                    display=stripped,
                    source_type="constitution",
                    source_path="(project-constitution)",  # virtual — derived from multiple files
                    confidence="high",
                    risk=risk,
                    reason=f"Explicit {purpose} command from Project Constitution.",
                    requires_permission=_permission_for(purpose),
                ))
        return candidates
    except Exception:
        return []


def _detect_makefile(repo_root: Path) -> list[CommandCandidate]:
    """Detect test/lint/build targets from Makefile, including recipe body risk."""
    makefile = repo_root / "Makefile"
    if not makefile.is_file() or not _is_within_repo(makefile, repo_root):
        return []
    try:
        text = makefile.read_text(errors="replace")
    except OSError:
        return []

    candidates: list[CommandCandidate] = []
    seen: set[str] = set()
    rel_path = _rel(makefile, repo_root)

    for target, body in _parse_makefile(text):
        purpose = _PURPOSE_MAP.get(target.lower())
        if purpose is None or target.lower() in seen:
            continue
        seen.add(target.lower())
        argv = ("make", target)
        # Inspect the recipe body for risky content.
        risk = _assess_risk(argv, extra_text=body)
        candidates.append(CommandCandidate(
            id=_candidate_id(purpose, "makefile", target),
            purpose=purpose,
            argv=argv,
            display=f"make {target}",
            source_type="makefile",
            source_path=rel_path,
            confidence="medium",
            risk=risk,
            reason=f"Makefile target '{target}'.",
            requires_permission=_permission_for(purpose),
        ))
    return candidates


def _detect_justfile(repo_root: Path) -> list[CommandCandidate]:
    """Detect test/lint/build recipes from justfile."""
    jf_path: Path | None = None
    jf_name: str = ""
    for name in ("justfile", "Justfile", ".justfile"):
        p = repo_root / name
        if p.is_file() and _is_within_repo(p, repo_root):
            jf_path, jf_name = p, name
            break
    if jf_path is None:
        return []

    try:
        text = jf_path.read_text(errors="replace")
    except OSError:
        return []

    candidates: list[CommandCandidate] = []
    seen: set[str] = set()
    rel_path = _rel(jf_path, repo_root)

    # Collect recipes and their bodies.
    current_recipe: str | None = None
    current_body: list[str] = []
    recipes: list[tuple[str, str]] = []

    for line in text.splitlines():
        m = re.match(r'^([a-zA-Z][a-zA-Z0-9_-]*)(?:\s.*)?:', line)
        if m:
            if current_recipe:
                recipes.append((current_recipe, "\n".join(current_body)))
            current_recipe = m.group(1)
            current_body = []
        elif current_recipe and (line.startswith("    ") or line.startswith("\t")):
            current_body.append(line.strip())
    if current_recipe:
        recipes.append((current_recipe, "\n".join(current_body)))

    for recipe, body in recipes:
        purpose = _PURPOSE_MAP.get(recipe.lower())
        if purpose is None or recipe.lower() in seen:
            continue
        seen.add(recipe.lower())
        argv = ("just", recipe)
        risk = _assess_risk(argv, extra_text=body)
        candidates.append(CommandCandidate(
            id=_candidate_id(purpose, "justfile", recipe),
            purpose=purpose,
            argv=argv,
            display=f"just {recipe}",
            source_type="justfile",
            source_path=rel_path,
            confidence="medium",
            risk=risk,
            reason=f"justfile recipe '{recipe}'.",
            requires_permission=_permission_for(purpose),
        ))
    return candidates


def _detect_taskfile(repo_root: Path) -> list[CommandCandidate]:
    """Detect test/lint/build tasks from Taskfile.yml."""
    tf_path: Path | None = None
    for name in ("Taskfile.yml", "Taskfile.yaml", "taskfile.yml", "taskfile.yaml"):
        p = repo_root / name
        if p.is_file() and _is_within_repo(p, repo_root):
            tf_path = p
            break
    if tf_path is None:
        return []

    try:
        text = tf_path.read_text(errors="replace")
    except OSError:
        return []

    candidates: list[CommandCandidate] = []
    seen: set[str] = set()
    rel_path = _rel(tf_path, repo_root)
    in_tasks = False

    for line in text.splitlines():
        if re.match(r'^tasks\s*:', line):
            in_tasks = True
            continue
        if in_tasks:
            m = re.match(r'^  ([a-zA-Z][a-zA-Z0-9_-]*)\s*:', line)
            if m:
                task_name = m.group(1)
                purpose = _PURPOSE_MAP.get(task_name.lower())
                if purpose is not None and task_name.lower() not in seen:
                    seen.add(task_name.lower())
                    argv = ("task", task_name)
                    candidates.append(CommandCandidate(
                        id=_candidate_id(purpose, "taskfile", task_name),
                        purpose=purpose,
                        argv=argv,
                        display=f"task {task_name}",
                        source_type="taskfile",
                        source_path=rel_path,
                        confidence="medium",
                        risk=_assess_risk(argv),
                        reason=f"Taskfile task '{task_name}'.",
                        requires_permission=_permission_for(purpose),
                    ))
            elif line and not line.startswith(" ") and not line.startswith("#"):
                in_tasks = False
    return candidates


def _detect_package_json(repo_root: Path) -> list[CommandCandidate]:
    """Detect test/lint/build scripts from package.json.

    Selects the package manager based on lockfiles in the same directory:
    pnpm-lock.yaml → pnpm, yarn.lock → yarn, bun.lock/bun.lockb → bun,
    package-lock.json → npm.  Default: npm.
    """
    pj_files = _find_files(repo_root, "package.json", max_depth=_SCAN_MAX_DEPTH)
    candidates: list[CommandCandidate] = []

    for pj in pj_files:
        if not _is_within_repo(pj, repo_root):
            continue
        try:
            data = json.loads(pj.read_text())
        except Exception:
            continue
        scripts: dict = data.get("scripts", {})
        if not isinstance(scripts, dict):
            continue

        pm = _js_package_manager(pj.parent)
        rel_path = _rel(pj, repo_root)

        for script_name, script_value in scripts.items():
            purpose = _PURPOSE_MAP.get(str(script_name).lower())
            if purpose is None or not isinstance(script_value, str):
                continue
            argv = (pm, "run", script_name)
            risk = _assess_risk(argv, extra_text=str(script_value))
            candidates.append(CommandCandidate(
                id=_candidate_id(purpose, "package_json", f"{rel_path}:{script_name}"),
                purpose=purpose,
                argv=argv,
                display=f"{pm} run {script_name}",
                source_type="package_json",
                source_path=rel_path,
                confidence="high",
                risk=risk,
                reason=f"package.json scripts.{script_name} = {script_value!r} ({pm})",
                requires_permission=_permission_for(purpose),
            ))
    return candidates


def _detect_pyproject(repo_root: Path) -> list[CommandCandidate]:
    """Detect Python test command from pyproject.toml.

    Generates a candidate when:
    - [tool.pytest.ini_options] or [tool.pytest] section is present, OR
    - a tests/ directory exists alongside pyproject.toml.

    Also emits candidates for poetry/uv/hatch if inferable.
    """
    pj_files = _find_files(repo_root, "pyproject.toml", max_depth=_SCAN_MAX_DEPTH)
    candidates: list[CommandCandidate] = []

    for pj in pj_files:
        if not _is_within_repo(pj, repo_root):
            continue
        try:
            text = pj.read_text(errors="replace")
        except OSError:
            continue

        has_pytest = "[tool.pytest" in text or "testpaths" in text or "[pytest]" in text
        has_tests = (pj.parent / "tests").is_dir()
        has_poetry = "[tool.poetry" in text or "[poetry]" in text
        has_hatch = "[tool.hatch" in text
        has_uv = "[tool.uv" in text

        rel_path = _rel(pj, repo_root)

        if has_pytest or has_tests:
            argv = ("python3", "-m", "pytest")
            reason = f"pyproject.toml"
            if has_pytest:
                reason += " with pytest configuration"
            if has_tests:
                reason += "; tests/ directory found"
            candidates.append(CommandCandidate(
                id=_candidate_id("test", "pyproject", rel_path),
                purpose="test",
                argv=argv,
                display="python3 -m pytest",
                source_type="pyproject",
                source_path=rel_path,
                confidence="high",
                risk=_assess_risk(argv),
                reason=reason.lstrip(";").strip(),
                requires_permission=_permission_for("test"),
            ))

        # poetry run pytest (only if poetry + pytest config)
        if has_poetry and (has_pytest or has_tests):
            argv = ("poetry", "run", "pytest")
            candidates.append(CommandCandidate(
                id=_candidate_id("test", "pyproject", f"poetry:{rel_path}"),
                purpose="test",
                argv=argv,
                display="poetry run pytest",
                source_type="pyproject",
                source_path=rel_path,
                confidence="medium",
                risk=_assess_risk(argv),
                reason="pyproject.toml with poetry + pytest setup.",
                requires_permission=_permission_for("test"),
            ))

    return candidates


def _detect_cargo(repo_root: Path) -> list[CommandCandidate]:
    """Detect Rust test command from Cargo.toml (bounded scan)."""
    paths = _find_files(repo_root, "Cargo.toml", max_depth=_SCAN_MAX_DEPTH)
    candidates: list[CommandCandidate] = []
    seen_dirs: set[str] = set()

    for path in paths:
        if not _is_within_repo(path, repo_root):
            continue
        dir_key = _rel(path.parent, repo_root) if path.parent != repo_root else "."
        if dir_key in seen_dirs:
            continue
        seen_dirs.add(dir_key)
        rel = _rel(path, repo_root)
        argv = ("cargo", "test")
        candidates.append(CommandCandidate(
            id=_candidate_id("test", "cargo", rel),
            purpose="test",
            argv=argv,
            display="cargo test",
            source_type="cargo",
            source_path=rel,
            confidence="high",
            risk=_assess_risk(argv),
            reason=f"Cargo.toml present ({rel}) → standard Rust test command.",
            requires_permission=_permission_for("test"),
        ))
    return candidates


def _detect_go(repo_root: Path) -> list[CommandCandidate]:
    """Detect Go test command from go.mod (bounded scan)."""
    paths = _find_files(repo_root, "go.mod", max_depth=_SCAN_MAX_DEPTH)
    candidates: list[CommandCandidate] = []
    seen_dirs: set[str] = set()

    for path in paths:
        if not _is_within_repo(path, repo_root):
            continue
        dir_key = _rel(path.parent, repo_root) if path.parent != repo_root else "."
        if dir_key in seen_dirs:
            continue
        seen_dirs.add(dir_key)
        rel = _rel(path, repo_root)
        argv = ("go", "test", "./...")
        candidates.append(CommandCandidate(
            id=_candidate_id("test", "go", rel),
            purpose="test",
            argv=argv,
            display="go test ./...",
            source_type="go",
            source_path=rel,
            confidence="high",
            risk=_assess_risk(argv),
            reason=f"go.mod present ({rel}) → standard Go test command.",
            requires_permission=_permission_for("test"),
        ))
    return candidates


def _detect_gradle(repo_root: Path) -> list[CommandCandidate]:
    """Detect JVM Gradle test command from build.gradle / build.gradle.kts."""
    candidates: list[CommandCandidate] = []
    seen_dirs: set[str] = set()

    for pattern in ("build.gradle", "build.gradle.kts"):
        for path in _find_files(repo_root, pattern, max_depth=_SCAN_MAX_DEPTH):
            if not _is_within_repo(path, repo_root):
                continue
            dir_key = _rel(path.parent, repo_root) if path.parent != repo_root else "."
            if dir_key in seen_dirs:
                continue
            seen_dirs.add(dir_key)
            rel = _rel(path, repo_root)
            # Prefer gradlew in the same directory.
            gradlew = path.parent / "gradlew"
            if gradlew.is_file() and _is_within_repo(gradlew, repo_root):
                gradlew_rel = _rel(gradlew, repo_root)
                argv = ("gradlew", "test")
                display = f"gradlew test  ({gradlew_rel})"
            else:
                argv = ("gradle", "test")
                display = "gradle test"
            candidates.append(CommandCandidate(
                id=_candidate_id("test", "gradle", rel),
                purpose="test",
                argv=argv,
                display=display,
                source_type="gradle",
                source_path=rel,
                confidence="high",
                risk=_assess_risk(argv),
                reason=f"Gradle build file present ({rel}).",
                requires_permission=_permission_for("test"),
            ))
    return candidates


def _detect_maven(repo_root: Path) -> list[CommandCandidate]:
    """Detect JVM Maven test command from pom.xml."""
    candidates: list[CommandCandidate] = []
    seen_dirs: set[str] = set()

    for path in _find_files(repo_root, "pom.xml", max_depth=_SCAN_MAX_DEPTH):
        if not _is_within_repo(path, repo_root):
            continue
        dir_key = _rel(path.parent, repo_root) if path.parent != repo_root else "."
        if dir_key in seen_dirs:
            continue
        seen_dirs.add(dir_key)
        rel = _rel(path, repo_root)
        mvnw = path.parent / "mvnw"
        if mvnw.is_file() and _is_within_repo(mvnw, repo_root):
            argv = ("mvnw", "test")
            display = "mvnw test"
        else:
            argv = ("mvn", "test")
            display = "mvn test"
        candidates.append(CommandCandidate(
            id=_candidate_id("test", "maven", rel),
            purpose="test",
            argv=argv,
            display=display,
            source_type="maven",
            source_path=rel,
            confidence="high",
            risk=_assess_risk(argv),
            reason=f"pom.xml present ({rel}) → Maven test command.",
            requires_permission=_permission_for("test"),
        ))
    return candidates


def _detect_dotnet(repo_root: Path) -> list[CommandCandidate]:
    """Detect .NET test command from *.sln or *.csproj files."""
    candidates: list[CommandCandidate] = []
    seen: set[str] = set()

    for pattern in ("*.sln", "*.csproj"):
        for path in _find_files_pattern(repo_root, pattern, max_depth=_SCAN_MAX_DEPTH):
            if not _is_within_repo(path, repo_root):
                continue
            rel = _rel(path, repo_root)
            if rel in seen:
                continue
            seen.add(rel)
            argv = ("dotnet", "test")
            candidates.append(CommandCandidate(
                id=_candidate_id("test", "dotnet", rel),
                purpose="test",
                argv=argv,
                display="dotnet test",
                source_type="dotnet",
                source_path=rel,
                confidence="medium",
                risk=_assess_risk(argv),
                reason=f".NET project file present ({rel}).",
                requires_permission=_permission_for("test"),
            ))
    return candidates


def _detect_ruby(repo_root: Path) -> list[CommandCandidate]:
    """Detect Ruby test command from Rakefile."""
    candidates: list[CommandCandidate] = []
    seen_dirs: set[str] = set()

    for path in _find_files(repo_root, "Rakefile", max_depth=_SCAN_MAX_DEPTH):
        if not _is_within_repo(path, repo_root):
            continue
        dir_key = _rel(path.parent, repo_root) if path.parent != repo_root else "."
        if dir_key in seen_dirs:
            continue
        seen_dirs.add(dir_key)
        rel = _rel(path, repo_root)
        argv = ("rake", "test")
        candidates.append(CommandCandidate(
            id=_candidate_id("test", "ruby", rel),
            purpose="test",
            argv=argv,
            display="rake test",
            source_type="ruby",
            source_path=rel,
            confidence="medium",
            risk=_assess_risk(argv),
            reason=f"Rakefile present ({rel}) → rake test.",
            requires_permission=_permission_for("test"),
        ))
    return candidates


def _detect_composer(repo_root: Path) -> list[CommandCandidate]:
    """Detect PHP test command from composer.json scripts.test."""
    candidates: list[CommandCandidate] = []

    for pj in _find_files(repo_root, "composer.json", max_depth=_SCAN_MAX_DEPTH):
        if not _is_within_repo(pj, repo_root):
            continue
        try:
            data = json.loads(pj.read_text())
        except Exception:
            continue
        scripts = data.get("scripts", {})
        if not isinstance(scripts, dict) or "test" not in scripts:
            continue
        rel = _rel(pj, repo_root)
        script_value = scripts.get("test", "")
        argv = ("composer", "test")
        risk = _assess_risk(argv, extra_text=str(script_value))
        candidates.append(CommandCandidate(
            id=_candidate_id("test", "composer", rel),
            purpose="test",
            argv=argv,
            display="composer test",
            source_type="composer",
            source_path=rel,
            confidence="medium",
            risk=risk,
            reason=f"composer.json scripts.test present ({rel}).",
            requires_permission=_permission_for("test"),
        ))
    return candidates


# ---------------------------------------------------------------------------
# Detector registry — order matters: higher-priority sources first.
# ---------------------------------------------------------------------------

_DETECTORS = (
    _detect_constitution,
    _detect_makefile,
    _detect_justfile,
    _detect_taskfile,
    _detect_package_json,
    _detect_pyproject,
    _detect_cargo,
    _detect_go,
    _detect_gradle,
    _detect_maven,
    _detect_dotnet,
    _detect_ruby,
    _detect_composer,
)
