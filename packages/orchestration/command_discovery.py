"""
Project Command Discovery v0 — Step 34.

Scans a target repository for test / build / lint command candidates from
known project configuration files.  Returns structured CommandCandidate
objects.  **No commands are executed here.  No shell=True.  All argv fields
are immutable tuples of strings.**

Execution of candidates remains fully policy-gated at the CLI / runner layer.

Detectors (in priority order):
  constitution  — explicit test_commands from Project Constitution
  pyproject     — pytest config / tests/ directory presence
  package_json  — scripts.test / scripts.lint / scripts.build
  makefile      — Makefile targets: test, lint, build, check
  justfile      — justfile / Justfile recipes: test, lint, build
  taskfile      — Taskfile.yml tasks: test, lint, build
  cargo         — Cargo.toml presence → cargo test
  go            — go.mod presence → go test ./...

Public API::

    discover_commands(job, repo_root) -> list[CommandCandidate]
        Collect all candidates from all detectors.

    select_best_test_candidate(candidates) -> CommandCandidate | None
        Return the single highest-confidence, lowest-risk test candidate,
        or None if none qualify.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import uuid4

if TYPE_CHECKING:
    from packages.core.models import Job


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Purposes we recognise.
_VALID_PURPOSES = frozenset({"test", "build", "lint", "format", "unknown"})

# Map of well-known script / target names to purposes.
_PURPOSE_MAP: dict[str, str] = {
    "test":      "test",
    "tests":     "test",
    "check":     "test",
    "test:ci":   "test",
    "test:unit": "test",
    "test:e2e":  "test",
    "lint":      "lint",
    "lint:ci":   "lint",
    "linting":   "lint",
    "eslint":    "lint",
    "tslint":    "lint",
    "format":    "format",
    "fmt":       "format",
    "prettier":  "format",
    "build":     "build",
    "build:ci":  "build",
    "compile":   "build",
    "bundle":    "build",
    "dist":      "build",
}

# Tokens whose presence in a command string marks it high-risk.
_RISKY_RE = re.compile(
    r"\b(?:rm|sudo|curl|wget|ssh|scp|deploy|publish|push|kubectl"
    r"|docker\s+(?:run|compose|push)|ansible)\b",
    re.IGNORECASE,
)

# Source types with explicit, trusted origins → higher confidence.
_EXPLICIT_SOURCE_TYPES = frozenset(
    {"constitution", "pyproject", "cargo", "go"}
)

# Permission required per purpose.
_PERMISSION_MAP: dict[str, str] = {
    "test":    "repo_test_run",
    "build":   "repo_build_run",
    "lint":    "repo_lint_run",
    "format":  "repo_format_run",
    "unknown": "",
}


# ---------------------------------------------------------------------------
# Candidate model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CommandCandidate:
    """Structured description of a discovered project command.

    argv is an immutable tuple of strings — never a shell string.
    No subprocess.run call is made here; this is pure data.
    """

    id: str
    purpose: str               # test | build | lint | format | unknown
    argv: tuple[str, ...]      # e.g. ("python3", "-m", "pytest")
    display: str               # human-readable, e.g. "python3 -m pytest"
    source_type: str           # package_json | pyproject | makefile | ...
    source_path: str           # relative path to source file, e.g. "Makefile"
    confidence: str            # high | medium | low
    risk: str                  # low | medium | high
    reason: str                # brief explanation of why this candidate exists
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
    """
    repo_root = Path(repo_root)
    all_candidates: list[CommandCandidate] = []
    for detector in (
        _detect_constitution,
        _detect_pyproject,
        _detect_package_json,
        _detect_makefile,
        _detect_justfile,
        _detect_taskfile,
        _detect_cargo,
        _detect_go,
    ):
        try:
            if detector is _detect_constitution:
                all_candidates.extend(detector(job, repo_root))  # type: ignore[call-arg]
            else:
                all_candidates.extend(detector(repo_root))
        except Exception:
            # A broken detector must never crash discovery.
            pass

    # Deduplicate by (purpose, argv) — keep first (highest-priority) occurrence.
    seen: set[tuple[str, tuple[str, ...]]] = set()
    result: list[CommandCandidate] = []
    for c in all_candidates:
        key = (c.purpose, c.argv)
        if key not in seen:
            seen.add(key)
            result.append(c)
    return result


def select_best_test_candidate(
    candidates: list[CommandCandidate],
) -> CommandCandidate | None:
    """Return the single best test candidate, or None.

    Selection criteria (in order):
      1. purpose == "test"
      2. risk in ("low", "medium")  — high-risk commands never auto-run
      3. confidence: "high" before "medium" before "low"
      4. source_type: explicit sources before heuristic
    """
    test_candidates = [
        c for c in candidates
        if c.purpose == "test" and c.risk != "high"
    ]
    if not test_candidates:
        return None

    _conf_order = {"high": 0, "medium": 1, "low": 2}
    _src_order = {s: 0 for s in _EXPLICIT_SOURCE_TYPES}
    # non-explicit sources get order 1

    def _sort_key(c: CommandCandidate) -> tuple[int, int]:
        conf = _conf_order.get(c.confidence, 9)
        src = _src_order.get(c.source_type, 1)
        return (conf, src)

    return min(test_candidates, key=_sort_key)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _candidate_id(purpose: str, source_type: str, variant: str = "") -> str:
    base = f"{purpose}:{source_type}"
    if variant:
        base += f":{variant}"
    return base


def _assess_risk(argv: tuple[str, ...], extra_text: str = "") -> str:
    combined = " ".join(argv) + (" " + extra_text if extra_text else "")
    if _RISKY_RE.search(combined):
        return "high"
    # Known-safe first arguments → low risk
    _safe_first = frozenset(
        {"python3", "python", "pytest", "make", "cargo", "go", "just", "task"}
    )
    if argv and argv[0] in _safe_first:
        return "low"
    return "medium"


def _permission_for(purpose: str) -> str:
    return _PERMISSION_MAP.get(purpose, "")


# ---------------------------------------------------------------------------
# Detectors
# ---------------------------------------------------------------------------


def _detect_constitution(job: "Job", repo_root: Path) -> list[CommandCandidate]:
    """Extract test commands from the Project Constitution if available."""
    try:
        from packages.orchestration.project_constitution import load_project_constitution
        constitution = load_project_constitution(repo_root)
        candidates: list[CommandCandidate] = []
        for cmd in constitution.test_commands:
            stripped = cmd.strip()
            if not stripped:
                continue
            parts = tuple(stripped.split())
            risk = _assess_risk(parts)
            candidates.append(CommandCandidate(
                id=_candidate_id("test", "constitution", stripped[:40]),
                purpose="test",
                argv=parts,
                display=stripped,
                source_type="constitution",
                source_path=str(repo_root / "CONSTITUTION.md"),
                confidence="high",
                risk=risk,
                reason="Explicit test command from Project Constitution.",
                requires_permission=_permission_for("test"),
            ))
        return candidates
    except Exception:
        return []


def _detect_pyproject(repo_root: Path) -> list[CommandCandidate]:
    """Detect pytest setup from pyproject.toml."""
    pyproject = repo_root / "pyproject.toml"
    if not pyproject.is_file():
        return []

    try:
        text = pyproject.read_text(errors="replace")
    except OSError:
        return []

    has_pytest_section = (
        "[tool.pytest" in text
        or "testpaths" in text
        or "pytest" in text.lower()
    )
    has_tests_dir = (repo_root / "tests").is_dir()

    if not (has_pytest_section or has_tests_dir):
        return []

    argv = ("python3", "-m", "pytest")
    risk = _assess_risk(argv)
    reason = "pyproject.toml present"
    if has_pytest_section:
        reason += " with pytest configuration"
    if has_tests_dir:
        reason += "; tests/ directory found"

    return [CommandCandidate(
        id=_candidate_id("test", "pyproject"),
        purpose="test",
        argv=argv,
        display="python3 -m pytest",
        source_type="pyproject",
        source_path="pyproject.toml",
        confidence="high",
        risk=risk,
        reason=reason.strip("; "),
        requires_permission=_permission_for("test"),
    )]


def _detect_package_json(repo_root: Path) -> list[CommandCandidate]:
    """Detect test/lint/build scripts from package.json."""
    pj = repo_root / "package.json"
    if not pj.is_file():
        return []

    try:
        data = json.loads(pj.read_text())
    except Exception:
        return []

    scripts: dict = data.get("scripts", {})
    if not isinstance(scripts, dict):
        return []

    candidates: list[CommandCandidate] = []
    for script_name, script_value in scripts.items():
        purpose = _PURPOSE_MAP.get(str(script_name).lower())
        if purpose is None:
            continue
        if not isinstance(script_value, str):
            continue
        argv = ("npm", "run", script_name)
        # Assess risk using both argv and the actual script value.
        risk = _assess_risk(argv, extra_text=str(script_value))
        candidates.append(CommandCandidate(
            id=_candidate_id(purpose, "package_json", script_name),
            purpose=purpose,
            argv=argv,
            display=f"npm run {script_name}",
            source_type="package_json",
            source_path="package.json",
            confidence="high",
            risk=risk,
            reason=f"package.json scripts.{script_name} = {script_value!r}",
            requires_permission=_permission_for(purpose),
        ))
    return candidates


def _detect_makefile(repo_root: Path) -> list[CommandCandidate]:
    """Detect test/lint/build targets from Makefile."""
    makefile = repo_root / "Makefile"
    if not makefile.is_file():
        return []

    try:
        text = makefile.read_text(errors="replace")
    except OSError:
        return []

    candidates: list[CommandCandidate] = []
    seen_targets: set[str] = set()
    for line in text.splitlines():
        m = re.match(r'^([a-zA-Z][a-zA-Z0-9_-]*)\s*:', line)
        if not m:
            continue
        target = m.group(1)
        purpose = _PURPOSE_MAP.get(target.lower())
        if purpose is None or target.lower() in seen_targets:
            continue
        seen_targets.add(target.lower())
        argv = ("make", target)
        risk = _assess_risk(argv)
        candidates.append(CommandCandidate(
            id=_candidate_id(purpose, "makefile", target),
            purpose=purpose,
            argv=argv,
            display=f"make {target}",
            source_type="makefile",
            source_path="Makefile",
            confidence="medium",
            risk=risk,
            reason=f"Makefile target '{target}'.",
            requires_permission=_permission_for(purpose),
        ))
    return candidates


def _detect_justfile(repo_root: Path) -> list[CommandCandidate]:
    """Detect test/lint/build recipes from justfile."""
    for name in ("justfile", "Justfile", ".justfile"):
        jf = repo_root / name
        if jf.is_file():
            source_path = name
            break
    else:
        return []

    try:
        text = jf.read_text(errors="replace")
    except OSError:
        return []

    candidates: list[CommandCandidate] = []
    seen: set[str] = set()
    # Recipes: lines like "recipe_name:" or "recipe_name arg1 arg2:"
    for line in text.splitlines():
        m = re.match(r'^([a-zA-Z][a-zA-Z0-9_-]*)', line)
        if not m:
            continue
        recipe = m.group(1)
        purpose = _PURPOSE_MAP.get(recipe.lower())
        if purpose is None or recipe.lower() in seen:
            continue
        seen.add(recipe.lower())
        argv = ("just", recipe)
        risk = _assess_risk(argv)
        candidates.append(CommandCandidate(
            id=_candidate_id(purpose, "justfile", recipe),
            purpose=purpose,
            argv=argv,
            display=f"just {recipe}",
            source_type="justfile",
            source_path=source_path,
            confidence="medium",
            risk=risk,
            reason=f"justfile recipe '{recipe}'.",
            requires_permission=_permission_for(purpose),
        ))
    return candidates


def _detect_taskfile(repo_root: Path) -> list[CommandCandidate]:
    """Detect test/lint/build tasks from Taskfile.yml."""
    for name in ("Taskfile.yml", "Taskfile.yaml", "taskfile.yml", "taskfile.yaml"):
        tf = repo_root / name
        if tf.is_file():
            source_path = name
            break
    else:
        return []

    try:
        text = tf.read_text(errors="replace")
    except OSError:
        return []

    candidates: list[CommandCandidate] = []
    seen: set[str] = set()
    in_tasks = False
    for line in text.splitlines():
        if re.match(r'^tasks\s*:', line):
            in_tasks = True
            continue
        if in_tasks:
            # Task names are 2-space indented keys
            m = re.match(r'^  ([a-zA-Z][a-zA-Z0-9_-]*)\s*:', line)
            if m:
                task_name = m.group(1)
                purpose = _PURPOSE_MAP.get(task_name.lower())
                if purpose is not None and task_name.lower() not in seen:
                    seen.add(task_name.lower())
                    argv = ("task", task_name)
                    risk = _assess_risk(argv)
                    candidates.append(CommandCandidate(
                        id=_candidate_id(purpose, "taskfile", task_name),
                        purpose=purpose,
                        argv=argv,
                        display=f"task {task_name}",
                        source_type="taskfile",
                        source_path=source_path,
                        confidence="medium",
                        risk=risk,
                        reason=f"Taskfile task '{task_name}'.",
                        requires_permission=_permission_for(purpose),
                    ))
            elif line and not line.startswith(" ") and not line.startswith("#"):
                in_tasks = False
    return candidates


def _detect_cargo(repo_root: Path) -> list[CommandCandidate]:
    """Detect Rust test command from Cargo.toml."""
    if not (repo_root / "Cargo.toml").is_file():
        return []
    argv = ("cargo", "test")
    return [CommandCandidate(
        id=_candidate_id("test", "cargo"),
        purpose="test",
        argv=argv,
        display="cargo test",
        source_type="cargo",
        source_path="Cargo.toml",
        confidence="high",
        risk=_assess_risk(argv),
        reason="Cargo.toml present → standard Rust test command.",
        requires_permission=_permission_for("test"),
    )]


def _detect_go(repo_root: Path) -> list[CommandCandidate]:
    """Detect Go test command from go.mod."""
    if not (repo_root / "go.mod").is_file():
        return []
    argv = ("go", "test", "./...")
    return [CommandCandidate(
        id=_candidate_id("test", "go"),
        purpose="test",
        argv=argv,
        display="go test ./...",
        source_type="go",
        source_path="go.mod",
        confidence="high",
        risk=_assess_risk(argv),
        reason="go.mod present → standard Go test command.",
        requires_permission=_permission_for("test"),
    )]
