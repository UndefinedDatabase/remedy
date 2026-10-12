"""F206 — the repository dependency catalog: a hand-written file naming which of the
operator's repositories depends on which, its parsing and validation, and the order it
gives an order's repositories so a library's jobs run before the jobs of whoever depends
on it.

The file is ``<data root>/org/catalog.toml``, a durable class of the data root
(``packages.orchestration.data_paths.DURABLE_CLASSES``) the operator writes by hand — no
crawler derives it (DECISION F206 D1). Each ``[[repo]]`` table names one repository by its
``pid``, the slug or id an order file's ``project`` line also uses, and optionally its
``name``, ``root``, ``owner``, the ``pid``s it ``depends_on``, and the package names it
``publishes``/``consumes`` for a later plausibility check (T003). A broken file, an unknown
key, a missing or duplicate ``pid``, a dependency on a ``pid`` the catalog does not hold, or
a dependency cycle each refuse to parse rather than guess; a cycle's refusal shows the exact
path, ``a -> b -> a``. :func:`repo_catalog_order` is this slice's other half: given a list of
``pid``s, it returns them in the order the catalog's ``depends_on`` edges require, citing
each edge, for the planner coupling T002 lands next.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

from packages.orchestration.data_paths import data_class_dir

try:                                   # Python >= 3.11
    import tomllib
except ModuleNotFoundError:            # Python 3.10 with the tomli backport
    import tomli as tomllib  # type: ignore[no-redef]


# The catalog's own filename below the "org" data-root class — never read from elsewhere.
REPO_CATALOG_FILENAME = "catalog.toml"

# Every key a `[[repo]]` table may hold; anything else refuses to parse (DECISION F206 D1).
REPO_CATALOG_KEYS = frozenset({
    "pid", "name", "root", "owner", "depends_on", "publishes", "consumes",
})


class RepoCatalogError(ValueError):
    """Any invalid catalog — broken TOML, an unknown key, or a dangling reference."""


class RepoCatalogCycleError(RepoCatalogError):
    """A catalog whose `depends_on` edges loop; `cycle` is the path, shown and re-raised."""

    def __init__(self, source: str, cycle: tuple[str, ...]) -> None:
        self.cycle = cycle
        super().__init__(
            f"{source}: the repository catalog has a dependency cycle: {' -> '.join(cycle)}")


@dataclass(frozen=True)
class RepoCatalogEntry:
    """One `[[repo]]` table, validated: a `pid` and the fields an order's planner reads."""

    pid: str
    name: str = ""
    root: str = ""
    owner: str = ""
    depends_on: tuple[str, ...] = ()
    publishes: tuple[str, ...] = ()
    consumes: tuple[str, ...] = ()


@dataclass(frozen=True)
class RepoCatalog:
    """A validated, cycle-free catalog — `entries` in file order, from `source`."""

    entries: tuple[RepoCatalogEntry, ...]
    source: str

    def entry(self, pid: str) -> RepoCatalogEntry | None:
        """The entry named `pid`, or None when the catalog does not hold it."""
        for candidate in self.entries:
            if candidate.pid == pid:
                return candidate
        return None

    @property
    def pids(self) -> tuple[str, ...]:
        """Every held `pid`, in the file's own order."""
        return tuple(entry.pid for entry in self.entries)


class RepoCatalogEdge(NamedTuple):
    """One ordering constraint `consumer` after `library`; `path` runs consumer to library."""

    consumer: str
    library: str
    path: tuple[str, ...]


class RepoCatalogOrder(NamedTuple):
    """`pids` in the order `repo_catalog_order` computed, with the edges that required it."""

    pids: tuple[str, ...]
    edges: tuple[RepoCatalogEdge, ...]


def repo_catalog_path(root: Path | None = None) -> Path:
    """The catalog file's path below the "org" data-root class."""
    return data_class_dir("org", root) / REPO_CATALOG_FILENAME


def _require_str(table: dict, key: str, idx: int, source: str) -> str:
    """`table[key]`, defaulting to "", refusing a present value that is not a string."""
    if key not in table:
        return ""
    value = table[key]
    if not isinstance(value, str):
        raise RepoCatalogError(f"{source}: repo[{idx}]: {key!r} must be a string")
    return value


def _require_name_list(table: dict, key: str, idx: int, source: str) -> tuple[str, ...]:
    """`table[key]`, defaulting to (), refusing anything but a list of distinct non-empty strings."""
    if key not in table:
        return ()
    value = table[key]
    if not isinstance(value, list):
        raise RepoCatalogError(
            f"{source}: repo[{idx}]: {key!r} must be a list of non-empty strings")
    seen: set[str] = set()
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item:
            raise RepoCatalogError(
                f"{source}: repo[{idx}]: {key!r} must be a list of non-empty strings")
        if item in seen:
            raise RepoCatalogError(f"{source}: repo[{idx}]: {key!r} names {item!r} twice")
        seen.add(item)
        result.append(item)
    return tuple(result)


def parse_repo_catalog(text: str, source: str = "<text>") -> RepoCatalog:
    """Parse and validate catalog TOML text; refuse anything invalid, raising with `source`."""
    try:
        raw = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise RepoCatalogError(f"{source}: not valid TOML: {exc}") from exc

    for key in raw:
        if key != "repo":
            raise RepoCatalogError(f"{source}: unknown top-level key {key!r}; only 'repo' is allowed")

    raw_repo = raw.get("repo", [])
    if not isinstance(raw_repo, list) or not all(isinstance(t, dict) for t in raw_repo):
        raise RepoCatalogError(f"{source}: 'repo' must be an array of tables")

    entries: list[RepoCatalogEntry] = []
    seen_pids: dict[str, int] = {}
    for idx, table in enumerate(raw_repo, start=1):
        for key in table:
            if key not in REPO_CATALOG_KEYS:
                raise RepoCatalogError(f"{source}: repo[{idx}]: unknown key {key!r}")

        pid = table.get("pid")
        if not isinstance(pid, str) or not pid:
            raise RepoCatalogError(f"{source}: repo[{idx}]: 'pid' is required and must be a non-empty string")
        if pid in seen_pids:
            raise RepoCatalogError(
                f"{source}: pid {pid!r} is defined more than once (repo[{seen_pids[pid]}] and repo[{idx}])")
        seen_pids[pid] = idx

        entries.append(RepoCatalogEntry(
            pid=pid,
            name=_require_str(table, "name", idx, source),
            root=_require_str(table, "root", idx, source),
            owner=_require_str(table, "owner", idx, source),
            depends_on=_require_name_list(table, "depends_on", idx, source),
            publishes=_require_name_list(table, "publishes", idx, source),
            consumes=_require_name_list(table, "consumes", idx, source),
        ))

    known_pids = set(seen_pids)
    for idx, entry in enumerate(entries, start=1):
        for dep in entry.depends_on:
            if dep not in known_pids:
                raise RepoCatalogError(
                    f"{source}: repo[{idx}] pid {entry.pid!r} depends on {dep!r}, "
                    "which the catalog does not hold")

    depends = {entry.pid: entry.depends_on for entry in entries}
    cycle = find_repo_catalog_cycle(depends)
    if cycle is not None:
        raise RepoCatalogCycleError(source, cycle)

    return RepoCatalog(entries=tuple(entries), source=source)


def find_repo_catalog_cycle(depends: Mapping[str, Sequence[str]]) -> tuple[str, ...] | None:
    """The first dependency cycle a depth-first walk finds, or None when there is none.

    Walks `depends` in mapping order and each pid's dependencies in listed order; the first
    back edge found returns the stack from the repeated pid to the top, plus that pid again —
    a pid depending on itself is the cycle `(pid, pid)`.
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    state: dict[str, int] = {pid: WHITE for pid in depends}
    stack: list[str] = []

    def visit(pid: str) -> tuple[str, ...] | None:
        state[pid] = GRAY
        stack.append(pid)
        for dep in depends.get(pid, ()):
            if dep not in state:
                continue
            if state[dep] == GRAY:
                start = stack.index(dep)
                return tuple(stack[start:]) + (dep,)
            if state[dep] == WHITE:
                found = visit(dep)
                if found is not None:
                    return found
        state[pid] = BLACK
        stack.pop()
        return None

    for pid in depends:
        if state[pid] == WHITE:
            found = visit(pid)
            if found is not None:
                return found
    return None


def load_repo_catalog(path: Path | None = None) -> RepoCatalog | None:
    """The catalog at `path` (default `repo_catalog_path()`), or None when it does not exist."""
    if path is None:
        path = repo_catalog_path()
    if not path.exists():
        return None
    return parse_repo_catalog(path.read_text(encoding="utf-8"), str(path))


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


def _shortest_depends_path(catalog: RepoCatalog, consumer: str, library: str) -> tuple[str, ...]:
    """The shortest `depends_on` path from `consumer` to `library`, ties broken breadth-first."""
    if consumer == library:
        return (consumer,)
    parent: dict[str, str] = {}
    seen = {consumer}
    queue: deque[str] = deque([consumer])
    while queue:
        current = queue.popleft()
        entry = catalog.entry(current)
        if entry is None:
            continue
        for dep in entry.depends_on:
            if dep in seen:
                continue
            seen.add(dep)
            parent[dep] = current
            if dep == library:
                path = [dep]
                node = current
                while node != consumer:
                    path.append(node)
                    node = parent[node]
                path.append(consumer)
                return tuple(reversed(path))
            queue.append(dep)
    raise RepoCatalogError(f"{catalog.source}: no depends_on path from {consumer!r} to {library!r}")


def repo_catalog_order(catalog: RepoCatalog, pids: Sequence[str]) -> RepoCatalogOrder:
    """`pids` ordered so each comes after every repository it depends on, directly or not.

    A `pid` given twice raises `ValueError`. A given `pid` the catalog does not hold keeps
    its place; it has no edge to or from any other given `pid`.
    """
    given = list(pids)
    if len(set(given)) != len(given):
        dupes = sorted({p for p in given if given.count(p) > 1})
        raise ValueError(f"pid given more than once: {', '.join(dupes)}")

    given_set = set(given)
    reach = {pid: _reachable_pids(catalog, pid) for pid in given}
    required = {pid: frozenset(q for q in given_set if q != pid and q in reach[pid]) for pid in given}

    placed: list[str] = []
    placed_set: set[str] = set()
    remaining = list(given)
    while remaining:
        for position, pid in enumerate(remaining):
            if required[pid] <= placed_set:
                placed.append(pid)
                placed_set.add(pid)
                del remaining[position]
                break
        else:
            raise RepoCatalogError(f"{catalog.source}: cannot order {remaining!r}")

    index = {pid: position for position, pid in enumerate(placed)}
    edges: list[RepoCatalogEdge] = []
    for consumer in placed:
        targets = reach[consumer] & given_set
        for library in targets:
            if any(other != library and other in targets and library in reach[other]
                   for other in targets):
                continue  # reached through another given pid; not a covering edge
            edges.append(RepoCatalogEdge(
                consumer=consumer, library=library,
                path=_shortest_depends_path(catalog, consumer, library)))
    edges.sort(key=lambda edge: (index[edge.consumer], index[edge.library]))
    return RepoCatalogOrder(pids=tuple(placed), edges=tuple(edges))


def describe_repo_catalog_edge(edge: RepoCatalogEdge) -> str:
    """"app depends on toolbox", or "... through brain" when the path passes other repositories."""
    if len(edge.path) <= 2:
        return f"{edge.path[0]} depends on {edge.path[-1]}"
    middle = ", ".join(edge.path[1:-1])
    return f"{edge.path[0]} depends on {edge.path[-1]} through {middle}"
