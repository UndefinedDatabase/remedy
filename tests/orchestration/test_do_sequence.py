"""F268 T001 — the `remedy do` sequence is DATA and one walker obeys it (DECISION F268 D4).

Pure unit tests over `packages/orchestration/do_sequence.py`: a spy step table
stands in for the real steps, so nothing here touches a repository, the data
root or a provider.
"""
from __future__ import annotations

import pytest

from packages.orchestration.do_sequence import (
    DO_SEQUENCE,
    DO_STEP_DONE,
    DO_STEP_FAILED,
    DO_STEP_SKIPPED,
    DO_STEP_STOPPED,
    DO_STEP_TABLE,
    DoContext,
    walk_do_sequence,
)


def _spy_table(calls: list[str], *, outcomes: dict[str, str] | None = None) -> dict:
    """A step table whose every step records its name and returns a set status."""
    outcomes = outcomes or {}

    def make(name: str):
        def step(ctx: DoContext) -> tuple[str, str]:
            calls.append(name)
            return outcomes.get(name, DO_STEP_DONE), f"{name} spy"
        return step

    table = {name: make(name) for name in DO_SEQUENCE}
    table["not-in-the-sequence"] = make("not-in-the-sequence")
    return table


def test_the_sequence_is_exactly_the_seven_step_names_in_order():
    assert DO_SEQUENCE == ("init", "study", "plan", "shape", "run", "ui", "apply")


def test_the_real_table_holds_a_step_for_every_name_and_nothing_else():
    assert set(DO_STEP_TABLE) == set(DO_SEQUENCE)


def test_the_walker_calls_the_table_in_sequence_order_and_nothing_outside_it():
    calls: list[str] = []

    ctx = walk_do_sequence(DoContext(order="o"), _spy_table(calls))

    assert calls == list(DO_SEQUENCE)
    assert [r.name for r in ctx.results] == list(DO_SEQUENCE)
    assert [r.detail for r in ctx.results] == [f"{n} spy" for n in DO_SEQUENCE]


def test_a_skipped_step_does_not_end_the_walk():
    calls: list[str] = []

    walk_do_sequence(DoContext(order="o"),
                     _spy_table(calls, outcomes={"study": DO_STEP_SKIPPED,
                                                 "ui": DO_STEP_SKIPPED}))

    assert calls == list(DO_SEQUENCE)


@pytest.mark.parametrize("status", [DO_STEP_STOPPED, DO_STEP_FAILED])
@pytest.mark.parametrize("ending", ["init", "shape", "run"])
def test_a_step_that_stops_or_fails_ends_the_walk(ending, status):
    calls: list[str] = []

    ctx = walk_do_sequence(DoContext(order="o"),
                           _spy_table(calls, outcomes={ending: status}))

    cut = DO_SEQUENCE.index(ending) + 1
    assert calls == list(DO_SEQUENCE[:cut])
    assert ctx.results[-1].name == ending
    assert ctx.results[-1].status == status
    assert ctx.failed is (status == DO_STEP_FAILED)


def test_stopping_at_apply_is_stopping_before_apply():
    ctx = walk_do_sequence(DoContext(order="o"),
                           _spy_table([], outcomes={"apply": DO_STEP_STOPPED}))

    assert ctx.stopped_before_apply is True
    assert ctx.failed is False


def test_a_completed_apply_step_is_not_stopping_before_apply():
    ctx = walk_do_sequence(DoContext(order="o"), _spy_table([]))

    assert ctx.stopped_before_apply is False
