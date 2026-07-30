"""Topological scheduling for the multi-cycle executor (F050 T001).

Pure functions only: no I/O, no clock, no randomness, no threading.  The same
task list always produces the same answer, which is what makes the executor's
schedule reproducible across a kill and a resume.

Dependency edges
----------------
A task carries its Flight Plan metadata in ``task.inputs["flight"]``:
``planned_id`` is its own plan-level id and ``depends_on`` lists the planned
ids it waits for (producer: ``map_flight_plan_to_tasks``, flight_plan.py).
Planned ids are resolved to task ids through the plan itself, so this module
never needs the FlightPlan object.

ONE rule covers plans that have no such metadata (legacy plans, heuristic
fallback plans): **a task without ``inputs["flight"]`` implicitly depends on
its predecessor in plan order.**  A legacy plan therefore schedules exactly
linearly, as it did before this module existed, and a plan mixing flight and
legacy tasks resolves each task by its own kind.

Unknown or dangling dependency ids — a ``depends_on`` entry naming no task in
the plan — are treated as a dependency that can never complete, so the
dependent task is never ready.  Plan-time Flight Plan validation rejects such
plans, which makes this a legacy-only corner; it is handled rather than
raised so one malformed legacy plan cannot crash the loop.

Cycles are likewise a plan-time concern: the Flight Plan schema validates the
DAG before execution, so a cycle cannot reach this module.  Should one appear
anyway, its members simply never become ready — the executor's existing
terminal-blocked path reports it instead of this module looping forever.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence
from uuid import UUID

from packages.core.models import RunState, Task

#: Task states that block everything downstream of them.  A task rolled back
#: to PENDING after a failed attempt is NOT in here — in-run failure tracking
#: is the executor's job (it alone knows what it attempted this run); these
#: are the states that block on their own, whenever they are encountered.
BLOCKING_STATES = frozenset({RunState.FAILED, RunState.CANCELLED})

__all__ = [
    "BLOCKING_STATES",
    "TaskNode",
    "build_graph",
    "ready_set",
    "blocked_downstream",
]


@dataclass(frozen=True)
class TaskNode:
    """One task's resolved position in the dependency graph."""

    task_id: UUID
    #: Position in plan order — the stable tie-break for every ordering here.
    index: int
    #: Task ids this task waits for, in the order they were declared.
    depends_on: tuple[UUID, ...]
    #: True when at least one declared dependency named no task in the plan.
    #: Such a task is never ready (see module docstring).
    has_unresolved_dependency: bool = False


def _flight_meta(task: Task) -> Mapping[str, Any] | None:
    """The task's flight metadata, or None when it carries none."""
    flight = task.inputs.get("flight")
    return flight if isinstance(flight, Mapping) else None


def build_graph(tasks: Sequence[Task]) -> tuple[TaskNode, ...]:
    """Resolve every task's dependencies to task ids, in plan order.

    Applies the two rules from the module docstring: flight metadata resolves
    ``depends_on`` planned ids through the plan; a task without it depends on
    its predecessor.
    """
    by_planned: dict[str, UUID] = {}
    for task in tasks:
        flight = _flight_meta(task)
        if flight is None:
            continue
        planned_id = flight.get("planned_id")
        if planned_id is None:
            continue
        # First declaration wins, so a duplicated planned id cannot silently
        # redirect earlier tasks' edges to a later task.
        by_planned.setdefault(str(planned_id), task.id)

    nodes: list[TaskNode] = []
    for index, task in enumerate(tasks):
        flight = _flight_meta(task)
        if flight is None:
            # Legacy rule: depend on the predecessor; the first task is free.
            predecessor = (tasks[index - 1].id,) if index > 0 else ()
            nodes.append(TaskNode(task_id=task.id, index=index,
                                  depends_on=predecessor))
            continue

        declared = flight.get("depends_on") or []
        resolved: list[UUID] = []
        unresolved = False
        for dep in declared:
            target = by_planned.get(str(dep))
            if target is None or target == task.id:
                # Names no task in the plan, or names itself: a dependency
                # that can never complete.
                unresolved = True
                continue
            if target not in resolved:
                resolved.append(target)
        nodes.append(TaskNode(
            task_id=task.id,
            index=index,
            depends_on=tuple(resolved),
            has_unresolved_dependency=unresolved,
        ))
    return tuple(nodes)


def ready_set(tasks: Sequence[Task]) -> list[UUID]:
    """Ids of the PENDING tasks whose dependencies are ALL completed.

    Returned in plan order — stable and deterministic, with no timestamp or
    set iteration anywhere in the decision.  A task is withheld when any
    dependency is not COMPLETED, including a dependency that is itself still
    pending, running, failed, or unresolvable.
    """
    status_by_id = {task.id: task.status for task in tasks}
    ready: list[UUID] = []
    for node in build_graph(tasks):
        if status_by_id.get(node.task_id) != RunState.PENDING:
            continue
        if node.has_unresolved_dependency:
            continue
        if all(status_by_id.get(dep) == RunState.COMPLETED
               for dep in node.depends_on):
            ready.append(node.task_id)
    return ready


def blocked_downstream(tasks: Sequence[Task],
                       blocked_ids: Iterable[UUID]) -> set[UUID]:
    """Transitive dependents of ``blocked_ids`` — the skipped-blocked set.

    The seeds themselves are NOT included: they are blocked for their own
    reason (a failed attempt this run, or a blocking state), while the result
    is the work that is blocked only because of them.  A task depending on a
    skipped-blocked task is itself skipped-blocked, transitively.

    Tasks already COMPLETED are never reported: a finished task cannot be
    skipped, even when something it depended on later failed and re-ran.
    """
    seeds = set(blocked_ids)
    if not seeds:
        return set()

    nodes = build_graph(tasks)
    dependents: dict[UUID, list[UUID]] = {}
    for node in nodes:
        for dep in node.depends_on:
            dependents.setdefault(dep, []).append(node.task_id)

    status_by_id = {task.id: task.status for task in tasks}
    blocked: set[UUID] = set()
    # Plan-order queue: deterministic traversal, though the result is a set.
    queue = [seed for seed in (node.task_id for node in nodes)
             if seed in seeds]
    # Seeds that are not tasks of this plan still propagate nothing, which is
    # the honest answer rather than an error.
    while queue:
        current = queue.pop(0)
        for dependent in dependents.get(current, ()):
            if dependent in blocked or dependent in seeds:
                continue
            if status_by_id.get(dependent) == RunState.COMPLETED:
                continue
            blocked.add(dependent)
            queue.append(dependent)
    return blocked
