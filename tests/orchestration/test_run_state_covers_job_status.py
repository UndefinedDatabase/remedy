"""F272 T002 — ``RunState`` covers every value ``JobPlan.status`` can hold.

DECISION F272 D5 rules the ``state`` collapse in two moves. The classic ``Job``
already spells the lifecycle field ``state: RunState``; ``JobPlan`` still spells
it ``status: str`` out of the six ``JOB_*`` constants. Those two vocabularies
differed in BOTH directions — ``blocked`` and ``stopped`` had no ``RunState``
member — so a bare rename would have silently lost two states. Round 8 widens
``RunState`` with those two; these tests pin the coverage that makes round 9's
one-commit rename lossless, the survival of the seven pre-existing members, the
``RunState(value)`` lookup round 9's importer performs on a stored string, and a
non-vacuity control without which a membership reading that answered True for
everything would pass.
"""
from __future__ import annotations

import pytest

from packages.core.models import RunState
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    JOB_PAUSED,
    JOB_PLANNED,
    JOB_RUNNING,
    JOB_STOPPED,
)

# The six values ``JobPlan.status`` can hold today, named so a failure names the
# constant it lost rather than an index.
JOB_STATUS_CONSTANTS = (
    ("JOB_PLANNED", JOB_PLANNED),
    ("JOB_RUNNING", JOB_RUNNING),
    ("JOB_BLOCKED", JOB_BLOCKED),
    ("JOB_COMPLETED", JOB_COMPLETED),
    ("JOB_PAUSED", JOB_PAUSED),
    ("JOB_STOPPED", JOB_STOPPED),
)

# The seven members that existed before F272 round 8 widened the enum.
PRE_EXISTING_RUN_STATE_VALUES = (
    "pending",
    "planned",
    "running",
    "paused",
    "completed",
    "failed",
    "cancelled",
)


def _run_state_values() -> set[str]:
    return {member.value for member in RunState}


@pytest.mark.parametrize("constant_name,constant_value", JOB_STATUS_CONSTANTS)
def test_job_status_constant_is_a_run_state_value(constant_name: str, constant_value: str) -> None:
    """Pins that this one ``JOB_*`` value has a ``RunState`` member.

    Breaks if round 9's rename of ``status`` to ``state`` would drop this state,
    or if a later edit removes the member that carries it.
    """
    assert constant_value in _run_state_values(), (
        f"{constant_name} = {constant_value!r} has no RunState member; "
        "renaming JobPlan.status to state would lose it"
    )


@pytest.mark.parametrize("value", PRE_EXISTING_RUN_STATE_VALUES)
def test_pre_existing_run_state_member_survives(value: str) -> None:
    """Pins that a member that existed before the widening is still there.

    Breaks if the edit that added ``BLOCKED`` and ``STOPPED`` renamed, revalued
    or removed one of the seven members it was supposed to leave alone.
    """
    assert value in _run_state_values(), f"pre-existing RunState value {value!r} disappeared"


def test_the_seven_pre_existing_members_keep_their_order() -> None:
    """Pins the seven original members as the enum's first seven, in order.

    Breaks if a member is inserted among them or the list is reordered, which
    would change every ``list(RunState)`` reading a later feature might take.
    """
    assert [member.value for member in RunState][:7] == list(PRE_EXISTING_RUN_STATE_VALUES)


@pytest.mark.parametrize("constant_name,constant_value", JOB_STATUS_CONSTANTS)
def test_run_state_round_trips_a_stored_job_status(constant_name: str, constant_value: str) -> None:
    """Pins ``RunState(value)`` for a stored status string.

    This is the exact lookup round 9's ``_import_job`` performs on a record's
    stored ``"status"`` key, so it breaks if the value is coverable but the
    lookup is not.
    """
    assert RunState(constant_value).value == constant_value, (
        f"RunState({constant_value!r}) did not round-trip for {constant_name}"
    )


def test_a_value_that_is_not_a_state_is_rejected() -> None:
    """The non-vacuity control: a made-up value must NOT be a ``RunState``.

    Without it, a membership reading that answered True for everything would
    pass every test above while pinning nothing.
    """
    assert "no_such_state" not in _run_state_values()
    with pytest.raises(ValueError):
        RunState("no_such_state")
