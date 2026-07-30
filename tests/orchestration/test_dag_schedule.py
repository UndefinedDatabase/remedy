"""F050 T001 — the pure DAG scheduling functions.

Table tests over the plan shapes named in the feature order: diamond, chain,
independent islands, the legacy-linear rule, a mixed plan, a single-task plan,
skipped-blocked transitivity, and determinism.  Everything here is pure: no
clock, no filesystem, no provider.
"""
from __future__ import annotations

import pytest

from packages.core.models import RunState, Task
from packages.orchestration.dag_schedule import (
    BLOCKING_STATES,
    blocked_downstream,
    build_graph,
    ready_set,
)


# ---------------------------------------------------------------------------
# Fixture builders
# ---------------------------------------------------------------------------


def flight_task(planned_id: str, *depends_on: str,
                status: RunState = RunState.PENDING) -> Task:
    """A task carrying Flight Plan metadata, shaped like the real mapper's."""
    return Task(
        description=f"task {planned_id}",
        inputs={"flight": {
            "planned_id": planned_id,
            "title": planned_id,
            "depends_on": list(depends_on),
        }},
        status=status,
    )


def legacy_task(name: str, *, status: RunState = RunState.PENDING) -> Task:
    """A task with no flight metadata — the legacy/heuristic-fallback shape."""
    return Task(description=f"legacy {name}", status=status)


def ids(tasks: list[Task], *planned_ids: str) -> list:
    """Task ids for the given planned ids, in the order asked for."""
    by_planned = {t.inputs["flight"]["planned_id"]: t.id
                  for t in tasks if "flight" in t.inputs}
    return [by_planned[p] for p in planned_ids]


def diamond(**states: RunState) -> list[Task]:
    """A -> (B, C) -> D.  States passed by planned id override PENDING."""
    return [
        flight_task("A", status=states.get("A", RunState.PENDING)),
        flight_task("B", "A", status=states.get("B", RunState.PENDING)),
        flight_task("C", "A", status=states.get("C", RunState.PENDING)),
        flight_task("D", "B", "C", status=states.get("D", RunState.PENDING)),
    ]


# ---------------------------------------------------------------------------
# ready_set — plan shapes
# ---------------------------------------------------------------------------


def test_diamond_root_is_the_only_ready_task_at_the_start():
    tasks = diamond()
    assert ready_set(tasks) == ids(tasks, "A")


def test_diamond_opens_both_branches_when_the_root_completes():
    tasks = diamond(A=RunState.COMPLETED)
    # Both branches ready at once, in plan order — this is the whole feature.
    assert ready_set(tasks) == ids(tasks, "B", "C")


def test_diamond_join_waits_for_both_branches():
    tasks = diamond(A=RunState.COMPLETED, B=RunState.COMPLETED)
    assert ready_set(tasks) == ids(tasks, "C")


def test_diamond_join_becomes_ready_only_after_both_parents():
    tasks = diamond(A=RunState.COMPLETED, B=RunState.COMPLETED,
                    C=RunState.COMPLETED)
    assert ready_set(tasks) == ids(tasks, "D")


def test_chain_releases_exactly_one_task_at_a_time():
    tasks = [flight_task("A"), flight_task("B", "A"), flight_task("C", "B")]
    assert ready_set(tasks) == ids(tasks, "A")

    tasks[0].status = RunState.COMPLETED
    assert ready_set(tasks) == ids(tasks, "B")

    tasks[1].status = RunState.COMPLETED
    assert ready_set(tasks) == ids(tasks, "C")


def test_independent_islands_are_all_ready_at_once():
    tasks = [flight_task("A"), flight_task("B"), flight_task("C", "B")]
    # A and B have no dependencies; C waits for B.
    assert ready_set(tasks) == ids(tasks, "A", "B")


def test_single_task_plan_degenerates_correctly():
    tasks = [flight_task("only")]
    assert ready_set(tasks) == ids(tasks, "only")

    tasks[0].status = RunState.COMPLETED
    assert ready_set(tasks) == []


def test_empty_plan_is_empty():
    assert ready_set([]) == []
    assert blocked_downstream([], []) == set()


# ---------------------------------------------------------------------------
# The legacy-linear rule
# ---------------------------------------------------------------------------


def test_legacy_plan_without_metadata_schedules_linearly():
    tasks = [legacy_task("one"), legacy_task("two"), legacy_task("three")]
    # One rule: each task depends on its predecessor.
    assert ready_set(tasks) == [tasks[0].id]

    tasks[0].status = RunState.COMPLETED
    assert ready_set(tasks) == [tasks[1].id]

    tasks[1].status = RunState.COMPLETED
    assert ready_set(tasks) == [tasks[2].id]


def test_legacy_plan_holds_the_tail_while_the_head_is_unfinished():
    tasks = [legacy_task("one", status=RunState.RUNNING), legacy_task("two")]
    assert ready_set(tasks) == []


def test_mixed_plan_resolves_each_task_by_its_own_kind():
    # Legacy task at index 1 depends on its predecessor (the flight task A);
    # the flight task C declares its edge explicitly and ignores position.
    a = flight_task("A")
    mid = legacy_task("mid")
    c = flight_task("C", "A")
    tasks = [a, mid, c]

    assert ready_set(tasks) == [a.id]

    a.status = RunState.COMPLETED
    # mid unblocks by predecessor rule, C unblocks by its declared edge.
    assert ready_set(tasks) == [mid.id, c.id]


def test_flight_task_after_a_legacy_task_does_not_inherit_position():
    legacy = legacy_task("first")
    independent = flight_task("B")          # declares no dependency at all
    tasks = [legacy, independent]
    # The flight task is ready immediately: it is not the legacy chain's tail.
    assert ready_set(tasks) == [legacy.id, independent.id]


# ---------------------------------------------------------------------------
# Dangling / self edges
# ---------------------------------------------------------------------------


def test_dangling_dependency_is_never_ready():
    tasks = [flight_task("A"), flight_task("B", "GHOST")]
    assert ready_set(tasks) == ids(tasks, "A")

    tasks[0].status = RunState.COMPLETED
    # GHOST names no task in the plan, so B's dependency never completes.
    assert ready_set(tasks) == []
    assert build_graph(tasks)[1].has_unresolved_dependency is True


def test_self_dependency_is_never_ready():
    tasks = [flight_task("A", "A")]
    assert ready_set(tasks) == []


def test_duplicate_declared_edge_is_collapsed():
    tasks = [flight_task("A", status=RunState.COMPLETED),
             flight_task("B", "A", "A")]
    assert build_graph(tasks)[1].depends_on == (tasks[0].id,)
    assert ready_set(tasks) == ids(tasks, "B")


# ---------------------------------------------------------------------------
# Non-pending and blocking states
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("state", [
    RunState.RUNNING,
    RunState.PLANNED,
    RunState.PAUSED,
    RunState.COMPLETED,
    RunState.FAILED,
    RunState.CANCELLED,
])
def test_only_pending_tasks_are_ever_ready(state):
    tasks = [flight_task("A", status=state)]
    assert ready_set(tasks) == []


@pytest.mark.parametrize("state", sorted(BLOCKING_STATES, key=lambda s: s.value))
def test_a_dependency_in_a_blocking_state_withholds_its_dependents(state):
    tasks = [flight_task("A", status=state), flight_task("B", "A")]
    assert ready_set(tasks) == []


# ---------------------------------------------------------------------------
# blocked_downstream — transitivity
# ---------------------------------------------------------------------------


def test_blocked_downstream_is_transitive():
    tasks = [flight_task("A"), flight_task("B", "A"), flight_task("C", "B"),
             flight_task("D", "C")]
    blocked = blocked_downstream(tasks, ids(tasks, "B"))
    # B's whole tail, and B itself is not in its own downstream.
    assert blocked == set(ids(tasks, "C", "D"))


def test_blocked_downstream_spares_the_independent_branch():
    tasks = diamond(A=RunState.COMPLETED)
    blocked = blocked_downstream(tasks, ids(tasks, "B"))
    # Only the join is blocked; C is an independent branch and stays runnable.
    assert blocked == set(ids(tasks, "D"))
    assert ids(tasks, "C")[0] not in blocked


def test_blocked_downstream_excludes_the_seeds():
    tasks = diamond()
    seeds = ids(tasks, "B", "C")
    assert blocked_downstream(tasks, seeds) == set(ids(tasks, "D"))


def test_blocked_downstream_never_reports_a_completed_task():
    tasks = diamond(A=RunState.COMPLETED, B=RunState.COMPLETED)
    # B finished, then A is somehow blocked again: B cannot be "skipped".
    blocked = blocked_downstream(tasks, ids(tasks, "A"))
    assert ids(tasks, "B")[0] not in blocked
    assert blocked == set(ids(tasks, "C", "D"))


def test_blocked_downstream_follows_the_legacy_chain():
    tasks = [legacy_task("one"), legacy_task("two"), legacy_task("three")]
    assert blocked_downstream(tasks, [tasks[0].id]) == {tasks[1].id,
                                                        tasks[2].id}


def test_blocked_downstream_of_an_unknown_id_is_empty():
    tasks = diamond()
    stranger = flight_task("STRANGER")
    assert blocked_downstream(tasks, [stranger.id]) == set()


def test_blocked_downstream_of_a_leaf_is_empty():
    tasks = diamond()
    assert blocked_downstream(tasks, ids(tasks, "D")) == set()


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


def test_ready_set_is_deterministic_across_calls():
    tasks = diamond(A=RunState.COMPLETED)
    first = ready_set(tasks)
    second = ready_set(tasks)
    assert first == second
    assert len(first) == 2


def test_ready_set_follows_plan_order_not_id_order():
    tasks = diamond(A=RunState.COMPLETED)
    expected = ids(tasks, "B", "C")
    # Plan order is the contract; uuid4 ids sort differently often enough that
    # an id-ordered implementation would fail this on most runs.
    assert ready_set(tasks) == expected


def test_blocked_downstream_is_deterministic_across_calls():
    tasks = diamond(A=RunState.COMPLETED)
    seeds = ids(tasks, "B")
    assert blocked_downstream(tasks, seeds) == blocked_downstream(tasks, seeds)


def test_build_graph_is_deterministic_and_in_plan_order():
    tasks = diamond()
    first = build_graph(tasks)
    second = build_graph(tasks)
    assert first == second
    assert [node.task_id for node in first] == [t.id for t in tasks]
    assert [node.index for node in first] == [0, 1, 2, 3]
