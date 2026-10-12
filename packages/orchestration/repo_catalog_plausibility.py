"""F206 T003 — the lockfile plausibility check (DECISION F206 D3).

The repository catalog (`packages/orchestration/repo_catalog.py`) is written by hand and never
replaced by this check (feature file P6: plausibility helps, never replaces). This module reads
each repository's own lockfile, at its root only, and warns when a repository's lockfile — or
its catalog-declared `consumes` — names a package another catalog entry `publishes`, while the
catalog gives the consumer no `depends_on` edge, direct or transitive, to that publisher. The
check never edits the catalog and never fails it: its answer is a list of warnings and a list of
entries it could not check (no root, or a root that is not a directory).
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import NamedTuple

from packages.orchestration.project_registry import list_projects
from packages.orchestration.repo_catalog import RepoCatalog, RepoCatalogEntry

try:                                   # Python >= 3.11
    import tomllib
except ModuleNotFoundError:            # Python 3.10 with the tomli backport
    import tomli as tomllib  # type: ignore[no-redef]

#: The four lockfiles read, in the order DECISION F206 D3 (5) walks a consumer's evidence; a
#: lockfile anywhere else in a repository's tree is not read (no crawler, feature file anti-goal).
LOCKFILE_NAMES = ("package-lock.json", "uv.lock", "poetry.lock", "Cargo.lock")

_NORMALIZE_RUN = re.compile(r"[-_.]+")


# WHY: a lockfile and a catalog's `publishes`/`consumes` spell the same package differently
# (`Foo_Bar` against `foo-bar`), so every comparison DECISION F206 D3 (5) makes runs on this.
def normalize_package_name(name: str) -> str:
    """Lowercased, with every run of `-`, `_` and `.` folded into one `-` (DECISION F206 D3 (4))."""
    return _NORMALIZE_RUN.sub("-", name.lower())


def _npm_names_from_packages(packages: dict) -> set[str]:
    """`npm`'s v2+ `packages` map: the key's last `node_modules/`-relative segment."""
    names: set[str] = set()
    for key in packages:
        if key == "":
            continue
        marker = "node_modules/"
        idx = key.rfind(marker)
        name = key[idx + len(marker):] if idx != -1 else key
        if name:
            names.add(name)
    return names


def _npm_names_from_dependencies(deps: dict) -> set[str]:
    """`npm`'s v1 `dependencies` map, walked into nested `dependencies` too."""
    names: set[str] = set()
    for name, meta in deps.items():
        names.add(name)
        if isinstance(meta, dict) and isinstance(meta.get("dependencies"), dict):
            names |= _npm_names_from_dependencies(meta["dependencies"])
    return names


def _read_package_lock_json(path: Path) -> frozenset[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("not the expected mapping")
    if isinstance(data.get("packages"), dict):
        names = _npm_names_from_packages(data["packages"])
    elif isinstance(data.get("dependencies"), dict):
        names = _npm_names_from_dependencies(data["dependencies"])
    else:
        names = set()
    return frozenset(normalize_package_name(n) for n in names)


def _read_toml_package_names(path: Path) -> frozenset[str]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    tables = data.get("package")
    if not isinstance(tables, list):
        raise ValueError("not the expected mapping")
    names: set[str] = set()
    for table in tables:
        if not isinstance(table, dict):
            raise ValueError("not the expected mapping")
        name = table.get("name")
        if isinstance(name, str) and name:
            names.add(name)
    return frozenset(normalize_package_name(n) for n in names)


# WHY: a broken lockfile must warn, not crash the whole check — one entry's bad JSON or TOML
# never hides the rest of the catalog's plausibility answer.
def read_lockfile_packages(root: Path) -> tuple[dict[str, frozenset[str]], dict[str, str]]:
    """Each of the four lockfiles present at `root` (only there), normalized names by file name,
    and, by file name, the reason a present lockfile could not be read."""
    packages: dict[str, frozenset[str]] = {}
    errors: dict[str, str] = {}
    for filename in LOCKFILE_NAMES:
        path = root / filename
        if not path.is_file():
            continue
        try:
            if filename == "package-lock.json":
                packages[filename] = _read_package_lock_json(path)
            else:
                packages[filename] = _read_toml_package_names(path)
        except (json.JSONDecodeError, tomllib.TOMLDecodeError, OSError, ValueError) as exc:
            errors[filename] = str(exc)
    return packages, errors


# WHY: the CLI (T004) prints a warning's proof and sentence directly; keeping them here, beside
# the check that builds them, is the one place their wording can drift from the sentence D3 (5)
# states.
class RepoCatalogWarning(NamedTuple):
    """One plausibility warning: `library`/`package` empty for an unreadable lockfile."""

    consumer: str
    library: str
    package: str
    proof: str
    sentence: str


# WHY: an entry with no resolvable root is not a false negative — it is unchecked, and the CLI
# (T004) must say so rather than stay silent about it.
class RepoCatalogSkip(NamedTuple):
    """One catalog entry the check could not read: no root, or a root that is not a directory."""

    pid: str
    reason: str


# WHY: the check's whole answer is these two lists; a NamedTuple keeps them paired so neither is
# read in isolation of the other.
class RepoCatalogPlausibility(NamedTuple):
    """`warnings` and `skipped`, each in the order `check_repo_catalog_plausibility` found them."""

    warnings: tuple[RepoCatalogWarning, ...]
    skipped: tuple[RepoCatalogSkip, ...]


def _reachable_pids(catalog: RepoCatalog, pid: str) -> frozenset[str]:
    """Every catalog pid reachable from `pid` through `depends_on`, transitively."""
    entry = catalog.entry(pid)
    if entry is None:
        return frozenset()
    seen: set[str] = set()
    stack = list(entry.depends_on)
    while stack:
        dep = stack.pop()
        if dep in seen:
            continue
        seen.add(dep)
        dep_entry = catalog.entry(dep)
        if dep_entry is not None:
            stack.extend(dep_entry.depends_on)
    return frozenset(seen)


def _resolve_entry_root(
        entry: RepoCatalogEntry, project_roots: Mapping[str, Path] | None) -> Path | None:
    """DECISION F206 D3 (3): the entry's own `root`, then `project_roots`, then the registry."""
    if entry.root:
        return Path(entry.root).expanduser()
    if project_roots is not None:
        return project_roots.get(entry.pid)
    for project in list_projects():
        if entry.pid in (str(project.id), project.slug):
            return Path(project.canonical_repo_path) if project.canonical_repo_path else None
    return None


def _emit_rule_warnings(
        consumer: str, name: str, proof: str,
        publishers: Mapping[str, list[tuple[str, str]]],
        reach: Mapping[str, frozenset[str]],
        seen_pairs: set[tuple[str, str]],
        warnings: list[RepoCatalogWarning]) -> None:
    """DECISION F206 D3 (5): one warning per (consumer, library, name), the first proof winning."""
    for library, published_as in publishers.get(name, ()):
        if library == consumer or library in reach[consumer]:
            continue
        key = (library, name)
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        warnings.append(RepoCatalogWarning(
            consumer=consumer, library=library, package=published_as, proof=proof,
            sentence=(
                f"{consumer} consumes {published_as} ({proof}), which {library} publishes, "
                f"but the catalog gives {consumer} no dependency on {library}"
            ),
        ))


# WHY: T004's `remedy project catalog-check` is this function's only caller outside its own
# tests; everything the command prints is this answer, read and formatted, never recomputed.
def check_repo_catalog_plausibility(
        catalog: RepoCatalog,
        project_roots: Mapping[str, Path] | None = None) -> RepoCatalogPlausibility:
    """Every lockfile-plausibility warning and every entry the check could not read."""
    warnings: list[RepoCatalogWarning] = []
    skipped: list[RepoCatalogSkip] = []

    publishers: dict[str, list[tuple[str, str]]] = {}
    for entry in catalog.entries:
        for published_name in entry.publishes:
            publishers.setdefault(normalize_package_name(published_name), []).append(
                (entry.pid, published_name))

    reach = {entry.pid: _reachable_pids(catalog, entry.pid) for entry in catalog.entries}

    for entry in catalog.entries:
        root = _resolve_entry_root(entry, project_roots)
        if root is None:
            skipped.append(RepoCatalogSkip(pid=entry.pid, reason=f"{entry.pid} has no root"))
            continue
        if not root.is_dir():
            skipped.append(RepoCatalogSkip(
                pid=entry.pid, reason=f"{entry.pid}'s root {root} is not a directory"))
            continue

        lockfile_packages, lockfile_errors = read_lockfile_packages(root)
        for filename in LOCKFILE_NAMES:
            if filename in lockfile_errors:
                warnings.append(RepoCatalogWarning(
                    consumer=entry.pid, library="", package="", proof=filename,
                    sentence=f"{entry.pid}'s {filename} cannot be read: {lockfile_errors[filename]}",
                ))

        seen_pairs: set[tuple[str, str]] = set()
        for filename in LOCKFILE_NAMES:
            for name in sorted(lockfile_packages.get(filename, frozenset())):
                _emit_rule_warnings(entry.pid, name, filename, publishers, reach, seen_pairs, warnings)
        for name in sorted(normalize_package_name(n) for n in entry.consumes):
            _emit_rule_warnings(entry.pid, name, "consumes", publishers, reach, seen_pairs, warnings)

    return RepoCatalogPlausibility(warnings=tuple(warnings), skipped=tuple(skipped))
