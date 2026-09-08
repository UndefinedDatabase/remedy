"""The order the prototype cluster is deleted in: importers first, their targets last.

WHY THIS EXISTS. Operator ruling amend0908-f275-finish RULE 2 orders the deletion
to proceed "in dependency order — leaf modules first, the modules they import
last — so that each group commit leaves no dangling import", and orders that
order derived from the map and written down BEFORE the first ``git rm``.

WHY THE UNIT IS A COMPONENT AND NOT A MODULE. The cluster's internal import graph
is CYCLIC — ``provider_trust`` and ``provider_trust_verification`` import each
other, and so do four more pairs across three groups. No ordering of single
modules can satisfy RULE 2 against a cycle: whichever of two mutual importers
goes first leaves the other importing a deleted module. So the atomic unit is the
STRONGLY CONNECTED COMPONENT, which is a single module wherever the graph is
acyclic and is the whole cycle where it is not. DECISION F275 D2 records that
ruling and the measurement behind it.

WHY A TEST RATHER THAN A DOCUMENT. This module's own neighbour
``test_cluster_deletion_map.py`` says it plainly: a prose inventory that nothing
re-measures is exactly the artefact that told three consecutive features this
deletion was cheap. The recorded order is held against the live import graph, so
a group commit that deletes its modules without shrinking the order reds here, and
so does an order that no longer matches the dependencies it claims to respect.

WHY THE WALKER IS IMPORTED RATHER THAN REWRITTEN. Same reason the map gives: this
repository keeps ONE first-party import walker, and a second would drift.
"""
from __future__ import annotations

import sys

from tests.orchestration.test_cluster_deletion_map import (
    CLUSTER_MODULES,
    _cluster_module_of,
)
from tests.orchestration.test_import_reachability import (
    REPO_ROOT,
    first_party_imports,
    resolve_module_path,
)

ORDER_PATH = REPO_ROOT / ".agent" / "f275_deletion_order.md"

#: Tarjan on 24 nodes needs nothing like this much, but the walker it calls is
#: shared and its depth is not this module's to assume.
_RECURSION_FLOOR = 10_000


def internal_dependencies() -> dict[str, set[str]]:
    """Per cluster module, the OTHER cluster modules it imports."""
    deps: dict[str, set[str]] = {m: set() for m in CLUSTER_MODULES}
    for module in CLUSTER_MODULES:
        path = resolve_module_path(module)
        if path is None:
            continue
        for dotted in first_party_imports(path):
            target = _cluster_module_of(dotted)
            if target is not None and target != module and target in deps:
                deps[module].add(target)
    return deps


def strongly_connected_components(deps: dict[str, set[str]]) -> list[tuple[str, ...]]:
    """Tarjan's algorithm. Every neighbour set is walked SORTED, so the result is stable."""
    if sys.getrecursionlimit() < _RECURSION_FLOOR:
        sys.setrecursionlimit(_RECURSION_FLOOR)
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    on_stack: dict[str, bool] = {}
    stack: list[str] = []
    found: list[tuple[str, ...]] = []
    counter = [0]

    def walk(v: str) -> None:
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on_stack[v] = True
        for w in sorted(deps[v]):
            if w not in index:
                walk(w)
                low[v] = min(low[v], low[w])
            elif on_stack.get(w):
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            component = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                component.append(w)
                if w == v:
                    break
            found.append(tuple(sorted(component)))

    for module in sorted(deps):
        if module not in index:
            walk(module)
    return found


def measured_order() -> list[tuple[str, ...]]:
    """The deletion order the live graph implies: a component goes when nothing left imports it.

    Ties are broken by the component's own sorted module names, so two runs over
    one tree always agree — a flapping order would make this ratchet useless.
    """
    deps = internal_dependencies()
    components = strongly_connected_components(deps)
    component_of = {m: c for c in components for m in c}
    importers: dict[tuple[str, ...], set[tuple[str, ...]]] = {c: set() for c in components}
    for module, targets in deps.items():
        for target in targets:
            if component_of[module] != component_of[target]:
                importers[component_of[target]].add(component_of[module])

    order: list[tuple[str, ...]] = []
    remaining = set(components)
    while remaining:
        free = sorted(c for c in remaining if not (importers[c] & remaining))
        assert free, "the condensation of a directed graph is acyclic by construction"
        for component in free:
            order.append(component)
            remaining.discard(component)
    return order


def recorded_order() -> list[tuple[str, ...]]:
    """The order file as a list of components; blank and hash-comment lines are ignored."""
    order: list[tuple[str, ...]] = []
    for line in ORDER_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        order.append(tuple(sorted(part.strip() for part in line.split(","))))
    return order


def _render(order: list[tuple[str, ...]]) -> str:
    return "\n".join("  " + ", ".join(c) for c in order) or "  (empty)"


def test_the_recorded_order_equals_the_measured_condensation():
    """The ratchet. A deletion that does not shrink this file reds here, and so does a reorder."""
    measured = measured_order()
    recorded = recorded_order()
    assert recorded == measured, (
        "The recorded deletion order no longer matches the live import graph.\n\n"
        "MEASURED (what the graph implies now):\n" + _render(measured)
        + "\n\nRECORDED (what the file says):\n" + _render(recorded)
        + "\n\nA group commit removes its modules from this file in the SAME commit "
        "that removes them from disk, exactly as it does for cluster_deletion_map.txt."
    )


def test_no_component_is_deleted_before_a_component_that_imports_it():
    """RULE 2's property, checked against the file rather than against the derivation."""
    deps = internal_dependencies()
    recorded = recorded_order()
    position = {m: i for i, component in enumerate(recorded) for m in component}
    violations = sorted(
        (module, target)
        for module, targets in deps.items()
        for target in targets
        if module in position and target in position
        and position[module] > position[target]
    )
    assert not violations, (
        "These modules are deleted AFTER a module they import, so their group commit "
        "would leave a dangling import:\n"
        + "\n".join(f"  {m} imports {t}, but {t} is deleted first" for m, t in violations)
    )


def test_every_cluster_module_still_on_disk_appears_exactly_once():
    """Neither a module the order forgot nor one it names twice."""
    live = {m for m in CLUSTER_MODULES if resolve_module_path(m) is not None}
    listed = [m for component in recorded_order() for m in component]
    assert sorted(listed) == sorted(set(listed)), (
        "A module is named more than once in the deletion order: "
        + str(sorted(m for m in set(listed) if listed.count(m) > 1))
    )
    assert set(listed) == live, (
        "The deletion order and the cluster modules on disk disagree.\n"
        f"  in the order but not on disk: {sorted(set(listed) - live)}\n"
        f"  on disk but not in the order: {sorted(live - set(listed))}"
    )
