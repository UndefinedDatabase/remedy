"""The prototype-cluster deletion map: per cluster module, the consumers that must be cut first.

WHY THIS EXISTS. Finding R-0830 established that every one of the twenty-four
prototype-cluster modules is reachable from the six D11 (c) entry points, so
F260's Design cannot order the deletion from its module list alone — a module
is not deletable because it appears on a list, it is deletable when nothing
outside the cluster still imports it. This map turns that around and measures
the graph by its EDGES: for each cluster module, every SURVIVING consumer that
has to be cut before the module can go. The deletion is bounded by those edges,
not by the module list, and the two modules with no edge at all are where it
starts.

WHY A TEST RATHER THAN A DOCUMENT. `cluster_deletion_map.txt` is generated from
the measurement below, and this module holds it against the live import graph in
BOTH directions. An edge that APPEARS is a consumer newly reaching the cluster,
which enlarges the deletion; an edge that DISAPPEARS is a cut whose line the
deletion round forgot to remove, which is how a plan goes quietly stale. Either
one reds. A prose inventory that nothing re-measures is exactly the artefact
that told three consecutive features this deletion was cheap.

WHY THE WALKER IS IMPORTED RATHER THAN REWRITTEN. `test_import_reachability.py`
already ships a static `ast`-based first-party import walker, and this
repository keeps ONE call-directory walker on purpose. A second one would drift
from the first and the two guards would disagree about the same graph.
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.orchestration.test_import_reachability import (
    REPO_ROOT,
    first_party_imports,
    resolve_module_path,
)

MAP_PATH = Path(__file__).resolve().parent / "cluster_deletion_map.txt"

EDGE_SEPARATOR = " <- "

# The modules of F260's prototype cluster that are still tracked in the repo.
# One module group leaves this tuple per deletion round, so it deliberately
# states no count: any numeral written here is stale from the next commit on.
CLUSTER_MODULES = (
    "packages.orchestration.provider_trust",
    "packages.orchestration.provider_trust_verification",
    "packages.orchestration.worker_registry",
    "packages.orchestration.overnight_executor",
    "packages.orchestration.overnight_readiness",
    "packages.orchestration.main_builder_adapter",
    "packages.orchestration.managed_builder_execution",
)

# The handlers of cluster COMMANDS. They die with the cluster, so their imports
# are not blockers. Listed BY PATH and never matched by filename pattern:
# `apps/cli/commands/worker.py` and `apps/cli/commands/context.py` keep only
# SURVIVING commands and are deliberately NOT listed here, so they stay
# measurable. F274 round 4 moved their cluster-bound handlers out into
# their own deletion-bound handler files for exactly that reason.
CLUSTER_COMMAND_HANDLERS = (
    "apps/cli/commands/dogfood_cmd.py",
    "apps/cli/commands/main_builder_adapter_cmd.py",
    "apps/cli/commands/managed_builder_execution_cmd.py",
    "apps/cli/commands/overnight_cmd.py",
    "apps/cli/commands/overnight_mission_cmd.py",
    "apps/cli/commands/progress_cmd.py",
    "apps/cli/commands/provider_cmd.py",
    "apps/cli/commands/repair_loop_v2_cmd.py",
    "apps/cli/commands/review_cmd.py",
    "apps/cli/commands/route_policy_cmd.py",
    "apps/cli/commands/self_repair_cmd.py",
)

# Production trees a surviving consumer can live in. `tests/` is deliberately
# excluded: a test of a deleted module is deleted with it and blocks nothing.
CONSUMER_ROOTS = ("packages", "apps", "scripts")

# A python import statement naming a first-party module, matched as TEXT rather
# than parsed. Finding R-0834: `scripts/remedy_smoke.sh` embeds its checks in
# `python3 -c "..."` heredocs, so the module it imports is real, executed and
# breaks on deletion exactly like an import in a `.py` file — but `ast` cannot
# reach it, because the file it lives in is not python. The walker below is
# therefore deliberately a REGEX over non-python files and deliberately matches
# only the two IMPORT FORMS: a bare mention of a dotted name is not an edge, and
# `cluster_deletion_map.txt` is itself full of bare mentions.
_EMBEDDED_IMPORT = re.compile(
    r"^[ \t]*(?:from|import)[ \t]+(packages\.[A-Za-z0-9_.]+)", re.MULTILINE
)


def embedded_first_party_imports(path: Path) -> set[str]:
    """First-party modules imported by python EMBEDDED in a non-python file."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return set()
    return set(_EMBEDDED_IMPORT.findall(text))


def _cluster_module_of(dotted: str) -> str | None:
    """The cluster module a dotted import name refers to, or None.

    `from packages.orchestration.worker_registry import run` contributes both the
    module and `module.run`, so an attribute suffix still names the module.
    """
    for module in CLUSTER_MODULES:
        if dotted == module or dotted.startswith(module + "."):
            return module
    return None


def _excluded_paths() -> set[Path]:
    """Resolved files that can never be a surviving consumer: the cluster and its handlers."""
    excluded = {resolve_module_path(m) for m in CLUSTER_MODULES}
    excluded |= {(REPO_ROOT / h).resolve() for h in CLUSTER_COMMAND_HANDLERS}
    excluded.discard(None)
    return excluded


def measured_edges() -> set[tuple[str, str]]:
    """Every `(cluster module, surviving consumer path)` edge in the live tree."""
    excluded = _excluded_paths()
    edges: set[tuple[str, str]] = set()
    for root in CONSUMER_ROOTS:
        for path in sorted((REPO_ROOT / root).rglob("*")):
            if not path.is_file() or path.resolve() in excluded:
                continue
            if path.suffix == ".py":
                dotted_names = first_party_imports(path)
            else:
                dotted_names = embedded_first_party_imports(path)
            for dotted in dotted_names:
                module = _cluster_module_of(dotted)
                if module is not None:
                    edges.add((module, str(path.relative_to(REPO_ROOT))))
    return edges


def recorded_edges() -> set[tuple[str, str]]:
    """The map file as an edge set; blank lines and hash-comment lines are ignored."""
    raw = MAP_PATH.read_text(encoding="utf-8").splitlines()
    edges: set[tuple[str, str]] = set()
    for line in raw:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        module, _, consumer = line.partition(EDGE_SEPARATOR)
        edges.add((module.strip(), consumer.strip()))
    return edges


def _one_per_line(edges: set[tuple[str, str]]) -> str:
    return "\n".join(m + EDGE_SEPARATOR + c for m, c in sorted(edges))


def test_every_cluster_module_still_resolves_to_a_file_on_disk():
    """Without this the map could quietly describe a tree that no longer exists."""
    missing = {m for m in CLUSTER_MODULES if resolve_module_path(m) is None}
    assert not missing, (
        "These cluster modules resolve to no file on disk, so the edges recorded "
        "against them describe a tree that is already gone. A deletion round "
        "removes a module's lines in the same commit that removes the module:\n"
        + "\n".join(sorted(missing))
    )


def test_the_recorded_map_equals_the_measured_import_graph():
    """The ratchet, both ways: an edge that appeared and an edge that disappeared each red here."""
    measured = measured_edges()
    recorded = recorded_edges()
    appeared = measured - recorded
    disappeared = recorded - measured
    assert not appeared and not disappeared, (
        "The deletion map no longer matches the live import graph.\n\n"
        f"APPEARED ({len(appeared)}) — a consumer newly reaches the cluster, so the "
        "deletion just got larger. Record the edge or remove the import:\n"
        + (_one_per_line(appeared) or "  (none)")
        + f"\n\nDISAPPEARED ({len(disappeared)}) — an edge was cut but its line was left "
        "behind, so the map overstates the work remaining. Remove the line in the "
        "commit that cuts the edge:\n"
        + (_one_per_line(disappeared) or "  (none)")
    )


def test_no_recorded_consumer_is_itself_a_cluster_module():
    """A cluster-internal edge blocks no deletion and must never be recorded as a blocker."""
    cluster_files = {
        str(path.relative_to(REPO_ROOT))
        for path in (resolve_module_path(m) for m in CLUSTER_MODULES)
        if path is not None
    }
    internal = {(m, c) for m, c in recorded_edges() if c in cluster_files}
    assert not internal, (
        "These recorded edges name a consumer that is itself a cluster module. A "
        "cluster module dies WITH the cluster, so an edge between two of them blocks "
        "nothing and would overstate the deletion:\n" + _one_per_line(internal)
    )
