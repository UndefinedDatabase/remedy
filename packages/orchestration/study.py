"""F266 T001 — Bounded read-only repository comprehension pass.

Walks a repository (bounded entry cap, honest partial result), detects
structure/core modules/conventions/entry points heuristically, and optionally
narrates each category through an injectable `call_fn` bounded by the existing
`should_stop`/`evaluate_budget` machinery (`max_provider_calls`), falling back
to the heuristic value on exhaustion or on any call_fn exception — it never
crashes. Each category is written as one card via `store_memory(...,
provenance="machine-study")`, so auto-approval connects end to end per
DECISION F266 D2. Read-only against the studied repository, proved by test.
"""
from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4

from packages.core.models import JobBudgets
from packages.memory.local_gateway import store_memory
from packages.orchestration.budget_guard import BudgetCounters
from packages.orchestration.safe_points import should_stop

#: Directories to prune while walking (matching pingpong_loop.py pattern).
STUDY_EXCLUDE_DIRS: frozenset[str] = frozenset({
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    ".data",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
})

#: Fixed category order for study output.
STUDY_CATEGORIES = ("structure", "core_modules", "conventions", "entry_points")

#: Default maximum number of directory+file entries to scan.
DEFAULT_MAX_ENTRIES = 2000


def _walk_repo(repo_root: str, max_entries: int) -> tuple[list[str], list[str], bool]:
    """Walk repo yielding relative paths, bounded by max_entries.

    Returns (relative_dir_paths, relative_file_paths, hit_cap).
    Prunes STUDY_EXCLUDE_DIRS and dotdirs. Sorted for determinism.
    """
    dirs: list[str] = []
    files: list[str] = []
    hit_cap = False

    root = Path(repo_root)

    for dirpath, dirnames, filenames in os.walk(repo_root, followlinks=False):
        # Prune in place: remove excluded dirs and dotdirs from dirnames
        dirnames[:] = sorted([
            d for d in dirnames
            if d not in STUDY_EXCLUDE_DIRS and not d.startswith(".")
        ])

        # Check cap BEFORE appending directory
        if len(dirs) + len(files) >= max_entries:
            hit_cap = True
            dirnames.clear()
            break

        # Add this directory (if not root)
        rel_dirpath = os.path.relpath(dirpath, repo_root)
        if rel_dirpath != ".":
            dirs.append(rel_dirpath)

        # Check cap BEFORE appending files
        if len(dirs) + len(files) >= max_entries:
            hit_cap = True
            dirnames.clear()
            break

        # Add files in this directory
        for filename in sorted(filenames):
            rel_filepath = os.path.join(rel_dirpath if rel_dirpath != "." else "", filename).lstrip("./")
            files.append(rel_filepath)

            # Check cap after each file
            if len(dirs) + len(files) >= max_entries:
                hit_cap = True
                dirnames.clear()
                break

        if hit_cap:
            break

    return sorted(dirs), sorted(files), hit_cap


def _detect_entry_points(files: list[str]) -> list[str]:
    """Which entry-point files exist at repo root.

    Checks for pyproject.toml, setup.py, package.json, Makefile,
    main.py, manage.py at root (no directory component).
    """
    candidates = {"pyproject.toml", "setup.py", "package.json", "Makefile", "main.py", "manage.py"}
    found = []
    for f in files:
        if f in candidates:
            found.append(f)
    return sorted(found)


def _detect_conventions(files: list[str]) -> list[str]:
    """Short English notes about recognized convention markers.

    Checks for test directories, AGENTS.md, README files.
    """
    notes = []

    # Check for test directories
    has_tests = any(f.startswith("tests/") or f.startswith("test/") for f in files)
    if has_tests:
        notes.append("has a top-level tests/ directory")

    # Check for AGENTS.md
    if "AGENTS.md" in files:
        notes.append("carries an AGENTS.md agent-operating-rules file")

    # Check for README
    if any(f in files for f in ("README.md", "README.rst", "README.txt")):
        notes.append("has a root README")

    return notes


@dataclass
class StudyResult:
    """Result of a study run."""

    project_id: str
    job_id: str
    cards_written: list[str] = field(default_factory=list)
    partial: bool = False
    stopped_reason: str | None = None
    entries_scanned: int = 0


def run_study(
    repo_root: str,
    *,
    project_id: str,
    job_id: str | None = None,
    max_entries: int = DEFAULT_MAX_ENTRIES,
    max_provider_calls: int = 4,
    call_fn: Callable[[str, int], str] | None = None,
) -> StudyResult:
    """Run a bounded study pass on a repository.

    Walks the repo (bounded by max_entries), detects structure/core modules/
    conventions/entry points heuristically, optionally narrates each via
    call_fn (bounded by max_provider_calls budget), and writes four memory
    cards with provenance="machine-study" (auto-approved per D2).

    Never writes to repo_root. Never raises on call_fn exception.
    Returns result with partial=True and stopped_reason set if cap hit or
    budget exhausted.
    """
    if job_id is None:
        job_id = f"study-{uuid4().hex[:12]}"

    # Validate job_id
    from packages.orchestration.safe_points import validate_job_id
    job_id = validate_job_id(job_id)

    result = StudyResult(project_id=project_id, job_id=job_id)

    # Walk the repo (bounded)
    dirs, files, hit_cap = _walk_repo(repo_root, max_entries)
    result.entries_scanned = len(dirs) + len(files)

    if hit_cap:
        result.partial = True
        if result.stopped_reason:
            result.stopped_reason += f"; entry_cap_reached:{max_entries}"
        else:
            result.stopped_reason = f"entry_cap_reached:{max_entries}"

    # Compute heuristic values for all four categories (before any model call)
    top_dirs = sorted(set(d.split("/")[0] for d in dirs))[:20]
    dirs_summary = ", ".join(top_dirs) if top_dirs else "(none)"

    heuristic_structure = (
        f"Repository contains {len(dirs)} directories and {len(files)} files scanned. "
        f"Top-level directories: {dirs_summary}. "
        + ("(PARTIAL — stopped at the " + str(max_entries) + "-entry cap)" if hit_cap else "")
    )

    heuristic_core_modules = f"Top-level directories: {dirs_summary}"

    conventions_list = _detect_conventions(files)
    heuristic_conventions = (
        "; ".join(conventions_list)
        if conventions_list
        else "No recognised convention markers found."
    )

    entry_points_list = _detect_entry_points(files)
    heuristic_entry_points = (
        ", ".join(entry_points_list)
        if entry_points_list
        else "No recognised entry-point files found at the repository root."
    )

    # Build category values (heuristic defaults)
    category_values = {
        "structure": heuristic_structure,
        "core_modules": heuristic_core_modules,
        "conventions": heuristic_conventions,
        "entry_points": heuristic_entry_points,
    }

    # Optionally invoke call_fn with budget guard
    if call_fn is not None:
        budgets = JobBudgets(max_provider_calls=max_provider_calls)
        counters = BudgetCounters()

        for category in STUDY_CATEGORIES:
            # Check budget before attempting this category
            check = should_stop(job_id, budgets=budgets, counters=counters)
            if check.should_stop:
                result.partial = True
                if result.stopped_reason:
                    result.stopped_reason += f"; {check.reason}"
                else:
                    result.stopped_reason = check.reason
                break

            # Try to call the function (never raises)
            heuristic_value = category_values[category]
            prompt = f"Summarize in one paragraph: {heuristic_value}"
            try:
                narrated = call_fn(prompt, 300)
                if narrated and narrated.strip():
                    category_values[category] = narrated.strip()
            except Exception:
                pass  # Fall back to heuristic on any exception

            # Increment counter for next check
            counters = BudgetCounters(
                provider_calls=counters.provider_calls + 1,
                unmeasured_call_count=counters.unmeasured_call_count + 1,
            )

    # Write memory cards
    for category in STUDY_CATEGORIES:
        entry = store_memory(
            key=f"study:{category}",
            value=category_values[category],
            project_id=project_id,
            job_id=job_id,
            tags=["study", category],
            source_type="agent",
            provenance="machine-study",
        )
        result.cards_written.append(entry.key)

    return result
