"""F033: the JOB level reads a task's recorded hunk decision and hands it to the loop.

THE LAST HOP, and the reason this file exists. ``hunk_decision_record.py`` records each
operator decision onto ``job.metadata``; ``run_pingpong`` forwards a ``hunk_ledger`` into
``compose_builder_prompt``; and ``packages/orchestration/pingpong_job.py`` is the ONE place
that holds both the job and the task, so it is where the two ends are joined. What is pinned
here is ``_recorded_hunk_ledger_for_task``'s TRUTH — which decision it returns, which ones it
refuses to return, and that it never raises — not the call site's shape.

WHY A NEW FILE. There is no ``tests/orchestration/test_pingpong_job.py``; the nearest
neighbour is ``test_job_task_runner.py``, which pins the runner's task sequencing. A focused
file sits beside it the way ``test_builder_prompt_hunk_rejections.py`` sits beside
``test_builder_prompt_golden.py``.

THE JOB AND THE TASK ARE FAKES — two small objects carrying only the attributes the helper
reads. Constructing a real ``JobPlan`` and driving a real run would test the runner instead of
the lookup, and would make the totality cases below unconstructible: "a job whose ``metadata``
attribute RAISES" is not a state a real ``JobPlan`` can be put into.

ONE ASSERTION HERE IS A SHAPE CHECK AND IS LABELLED AS SUCH — the AST test at the bottom only
proves the helper is REFERENCED at the ``run_pingpong`` call, so that it cannot be shipped
unreferenced. Everything above it is what proves the behaviour.
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from packages.orchestration import pingpong_job
from packages.orchestration.diff_view_source import DIFF_SCOPE_JOB
from packages.orchestration.hunk_decision_record import HUNK_DECISIONS_METADATA_KEY
from packages.orchestration.hunk_ledger import (
    HUNK_LANDING_NOT_LANDED,
    HUNK_STATE_REJECTED,
)
from packages.orchestration.pingpong_job import _recorded_hunk_ledger_for_task
from packages.orchestration.pingpong_loop import compose_builder_prompt

#: Chosen to BREAK under any normalisation: leading spaces, an interior blank line and a tab
#: indent. A reason that survives this survives an operator's real words.
_HOSTILE_REASON = "  keep the old parameter name\n\n\tand do not reflow this line\n"

_TASK = "t-1"
_OTHER_TASK = "t-2"
_HUNK = "h-9c1f"

_GOAL = "make the failing test pass"
_CONTEXT = "the repository under review"


class _FakeJob:
    """Only what the helper reads: a ``metadata`` mapping."""

    def __init__(self, metadata: object) -> None:
        self.metadata = metadata


class _FakeTask:
    """Only what the helper reads: a ``task_id``."""

    def __init__(self, task_id: object) -> None:
        self.task_id = task_id


class _UnreadableJob:
    """A job whose ``metadata`` RAISES on access — the fault no inner guard can absorb."""

    @property
    def metadata(self) -> object:
        raise RuntimeError("this job cannot be read")


class _TasklessTask:
    """A task carrying no ``task_id`` at all."""


def _record(task_id: str, *, attempt: int, decided_at: str, reason: str) -> dict:
    """One decision in the shape the recording door writes onto ``job.metadata``.

    The four keys are ``hunk_decision_record._RECORD_KEYS`` and the row keys are
    ``hunk_ledger.export_hunk_ledger``'s. They are written out rather than produced by calling
    the door because this suite is about the READ side: going through the door would make a
    failure here ambiguous between the two.
    """
    return {
        "task_id": task_id,
        "attempt": attempt,
        "decided_at": decided_at,
        "hunks": [
            {
                "id": _HUNK,
                "state": HUNK_STATE_REJECTED,
                "reason": reason,
                "landing": HUNK_LANDING_NOT_LANDED,
            }
        ],
    }


def _job_with(*records: dict) -> _FakeJob:
    decisions = {
        f"{rec['task_id']}:{rec['attempt']}": rec for rec in records
    }
    return _FakeJob({HUNK_DECISIONS_METADATA_KEY: decisions})


# ---------------------------------------------------------------- C1


def test_a_recorded_decision_comes_back_as_that_tasks_ledger_byte_for_byte() -> None:
    """C1: the reason the operator typed survives the round trip unchanged."""
    job = _job_with(_record(_TASK, attempt=1, decided_at="2026-08-29T09:00:00",
                            reason=_HOSTILE_REASON))

    ledger = _recorded_hunk_ledger_for_task(job, _FakeTask(_TASK))

    assert [entry.hunk_id for entry in ledger.entries] == [_HUNK]
    assert [entry.state for entry in ledger.entries] == [HUNK_STATE_REJECTED]
    # BYTE FOR BYTE, on the RAW reason — a stripped or re-wrapped comparison would pass while
    # something on the route quietly rewrote what the operator typed.
    assert ledger.entries[0].reason == _HOSTILE_REASON


# ---------------------------------------------------------------- C2


def test_the_ledger_the_job_reads_composes_into_the_builder_prompt() -> None:
    """C2: job metadata → ledger → prompt. This link is the round's point.

    ``run_pingpong`` forwards its ``hunk_ledger`` argument to ``compose_builder_prompt``
    unchanged — that hop is pinned by
    ``tests/orchestration/test_builder_prompt_hunk_rejections.py`` over the REAL loop — so
    composing directly with the ledger this helper returned is what closes the chain from the
    job's stored decision to the next builder's prompt.
    """
    job = _job_with(_record(_TASK, attempt=1, decided_at="2026-08-29T09:00:00",
                            reason=_HOSTILE_REASON))

    ledger = _recorded_hunk_ledger_for_task(job, _FakeTask(_TASK))
    composed = compose_builder_prompt(_GOAL, _CONTEXT, hunk_ledger=ledger)

    assert _HOSTILE_REASON in composed.text


# ---------------------------------------------------------------- C3


def test_a_different_tasks_decision_is_never_returned() -> None:
    """C3: the other task's record is the ONLY one present, so a lookup that ignored the
    task id would answer with it instead of with nothing."""
    job = _job_with(_record(_OTHER_TASK, attempt=1, decided_at="2026-08-29T09:00:00",
                            reason=_HOSTILE_REASON))

    # The premise: that record really is readable for the task it belongs to. Without this the
    # test would also pass against a helper that returned empty for everything.
    assert _recorded_hunk_ledger_for_task(job, _FakeTask(_OTHER_TASK)).entries != ()

    assert _recorded_hunk_ledger_for_task(job, _FakeTask(_TASK)).entries == ()


# ---------------------------------------------------------------- C4


def test_a_job_scoped_decision_is_not_quoted_into_a_tasks_prompt() -> None:
    """C4: a decision taken at JOB scope was never attributed to one task, so no one task
    inherits it. The sentinel is referenced BY NAME — a test that retyped ``"job"`` would keep
    passing the day the constant moved."""
    job = _job_with(_record(DIFF_SCOPE_JOB, attempt=1, decided_at="2026-08-29T09:00:00",
                            reason=_HOSTILE_REASON))

    # The premise again: the record is there and is readable under the sentinel itself.
    assert _recorded_hunk_ledger_for_task(job, _FakeTask(DIFF_SCOPE_JOB)).entries != ()

    assert _recorded_hunk_ledger_for_task(job, _FakeTask(_TASK)).entries == ()


# ---------------------------------------------------------------- C5


def _job_with_one_record() -> _FakeJob:
    return _job_with(_record(_TASK, attempt=1, decided_at="2026-08-29T09:00:00",
                             reason=_HOSTILE_REASON))


@pytest.mark.parametrize(
    ("make_job", "make_task"),
    [
        pytest.param(lambda: _FakeJob(None), lambda: _FakeTask(_TASK),
                     id="metadata_is_none"),
        pytest.param(lambda: _FakeJob("not a mapping"), lambda: _FakeTask(_TASK),
                     id="metadata_is_not_a_mapping"),
        pytest.param(lambda: _FakeJob({}), lambda: _FakeTask(_TASK),
                     id="no_decisions_key"),
        pytest.param(_job_with_one_record, _TasklessTask,
                     id="task_carries_no_task_id"),
        pytest.param(_UnreadableJob, lambda: _FakeTask(_TASK),
                     id="job_metadata_raises_on_access"),
    ],
)
def test_every_unusable_shape_yields_an_empty_ledger_and_raises_nothing(
    make_job, make_task
) -> None:
    """C5: TOTAL. Each case is its own parameter so a red-proof names which shape broke."""
    ledger = _recorded_hunk_ledger_for_task(make_job(), make_task())

    assert ledger.entries == ()


# ---------------------------------------------------------------- C6


def test_the_run_pingpong_call_passes_a_hunk_ledger_keyword() -> None:
    """C6, and it is a SHAPE CHECK — said plainly rather than dressed up.

    It proves only that the helper above is REFERENCED at the call site, so it cannot be
    shipped unreferenced. C1 to C5 are what prove the behaviour. The source is located through
    the imported module's own ``__file__`` rather than by a path spelled here, so this reads
    the file that was actually imported — including inside a disposable worktree.
    """
    source = Path(pingpong_job.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)

    calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "run_pingpong"
    ]

    # Non-vacuity: a walk that found nothing would make the assertion below trivially true.
    assert calls, "no run_pingpong call found in pingpong_job.py"

    passing = [
        call for call in calls
        if any(kw.arg == "hunk_ledger" for kw in call.keywords)
    ]
    assert passing, (
        "no run_pingpong call in pingpong_job.py passes a hunk_ledger keyword"
    )
