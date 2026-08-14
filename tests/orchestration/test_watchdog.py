"""F077 T001 — each watchdog tripwire and the near miss that must NOT fire.

Every tripwire is paired with its just-under-threshold twin, because a
tripwire that only ever fires proves nothing about where its edge is. What
each test pins:

  * no_progress fires at the threshold, not one dispatch earlier, and any
    ``declare_milestone_done`` clears the run — progress is read off the
    LEDGER, not the plan body;
  * a REFUSED dispatch (no ``outcome.job_id``) is not a dispatch, so
    repeating one never trips no_progress — the loop's own second-refusal
    escalation owns that event;
  * burn fires strictly above the multiple, not at it, stays INERT below the
    minimum sample count, and treats an UNMEASURED entry as absent rather
    than as a zero (P6: no estimate is ever written into ``usage``);
  * goal_drift fires on the first dispatched milestone the plan never named
    and stays silent when every dispatch is on plan;
  * ``evaluate_ledger`` reports in a fixed order;
  * every evaluator tolerates a torn entry without raising.

Every assertion names the Trip's ``kind``, ``since_iteration`` and the
``numbers`` it carries: a test that only asserts "a trip happened" does not
pin the evidence triple the human is meant to judge.

Fixtures are built IN-PROCESS by ``_entry`` below — plain dicts in exactly
the shape ``read_ledger`` returns. No JSONL fixture file, no disk, no conftest.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pytest

from packages.core.models import Job, RunState, Task
from packages.orchestration.escalation import (
    answer_task_decision,
    open_task_decisions,
)
from packages.orchestration.mission_state import (
    MISSION_ROLE_INITIAL,
    MISSION_STATUS_ACHIEVED,
    MISSION_STATUS_ACTIVE,
    MISSION_STATUS_PAUSED,
    create_mission,
    link_job_to_mission,
    load_mission,
    set_mission_status,
)
from packages.orchestration.orchestrator_loop import (
    ledger_path,
    read_ledger,
    render_ledger,
)
from packages.orchestration.orchestrator_move_schema import (
    MOVE_DECLARE_MILESTONE_DONE,
    MOVE_DISPATCH_JOB,
)
from packages.orchestration.storage import load_job, save_job
from packages.orchestration.watchdog import (
    DECISION_OPTION_ABORT,
    DECISION_OPTION_RESUME,
    MOVE_WATCHDOG_TRIPPED,
    OUTCOME_WATCHDOG_TRIPPED,
    TRIP_BURN_ANOMALY,
    TRIP_GOAL_DRIFT,
    TRIP_NO_PROGRESS,
    Trip,
    WatchdogThresholds,
    act_on_trips,
    dispatched_entries,
    evaluate_burn_anomaly,
    evaluate_goal_drift,
    evaluate_ledger,
    evaluate_no_progress,
    measured_tokens,
    watchdog_decision_marker,
)


def _entry(iteration: int, *, kind: str = MOVE_DISPATCH_JOB,
           milestone_id: str = "M1", job_id: str | None = "job-1",
           tokens: int | None = None) -> dict[str, Any]:
    """One ledger entry in the seven-key shape ``read_ledger`` hands back.

    ``job_id=None`` builds a REFUSED dispatch; ``tokens=None`` builds an
    UNMEASURED entry, whose ``cost.usage`` is None exactly as the loop writes
    it when nothing measured the call.
    """
    outcome: dict[str, Any] = {"executed": job_id is not None}
    if job_id is not None:
        outcome["job_id"] = job_id
    else:
        outcome["refused_reason"] = "gate blocked"
    usage = (None if tokens is None
             else {"input_tokens": tokens, "output_tokens": 0,
                   "cache_read": 0, "cache_creation": 0,
                   "total_cost_usd": 0.0})
    return {
        "iteration": iteration,
        "context_digest": f"digest-{iteration}",
        "move": {
            "schema_v": "om1",
            "kind": kind,
            "payload": {"milestone_id": milestone_id, "step": "build"},
            "rationale": "recorded for the audit trail",
        },
        "outcome": outcome,
        "cost": {
            "calls": 1,
            "usage": usage,
            "usage_source": "unmeasured" if usage is None else "measured",
        },
        "protocol_version": "op1",
        "recorded_at": f"2026-08-14T00:{iteration:02d}:00+00:00",
    }


#: A malformed entry of every shape the module promises to survive: a
#: non-dict, an empty entry, a non-dict ``move``, a null ``outcome`` and a
#: list where ``cost`` belongs.
_TORN_ENTRIES: list[Any] = [
    "not an entry at all",
    {},
    {"iteration": 1, "move": "dispatch_job"},
    {"iteration": 2, "move": {"kind": MOVE_DISPATCH_JOB}, "outcome": None},
    {"iteration": 3, "move": {"kind": MOVE_DISPATCH_JOB, "payload": []},
     "outcome": {"job_id": "job-x"}, "cost": []},
]


# ── no_progress ────────────────────────────────────────────────────────────


def test_no_progress_fires_at_the_repeat_threshold():
    entries = [_entry(i) for i in (4, 5, 6)]

    trip = evaluate_no_progress(entries, repeats=3)

    assert trip is not None
    assert trip.kind == TRIP_NO_PROGRESS
    assert trip.since_iteration == 4
    assert trip.numbers == {"repeats": 3, "threshold": 3, "milestone_id": "M1"}
    assert trip.to_json()["numbers"]["milestone_id"] == "M1"


def test_no_progress_does_not_fire_one_repeat_under_the_threshold():
    entries = [_entry(i) for i in (4, 5)]

    assert evaluate_no_progress(entries, repeats=3) is None


def test_no_progress_run_is_reset_by_a_declared_milestone():
    entries = [
        _entry(1), _entry(2),
        _entry(3, kind=MOVE_DECLARE_MILESTONE_DONE, job_id=None),
        _entry(4), _entry(5),
    ]

    assert evaluate_no_progress(entries, repeats=3) is None


def test_no_progress_ignores_repeated_refused_dispatches():
    entries = [_entry(i, job_id=None) for i in (1, 2, 3, 4, 5)]

    assert evaluate_no_progress(entries, repeats=3) is None


def test_no_progress_starts_a_new_run_on_a_different_milestone():
    entries = [_entry(1, milestone_id="M1"), _entry(2, milestone_id="M2"),
               _entry(3, milestone_id="M2"), _entry(4, milestone_id="M2")]

    trip = evaluate_no_progress(entries, repeats=3)

    assert trip is not None
    assert trip.since_iteration == 2
    assert trip.numbers["milestone_id"] == "M2"


# ── burn_anomaly ───────────────────────────────────────────────────────────


def _burn_ledger(baseline: int, window: int) -> list[dict[str, Any]]:
    """Five measured iterations at ``baseline``, then three at ``window``."""
    return ([_entry(i, tokens=baseline) for i in range(1, 6)]
            + [_entry(i, tokens=window) for i in range(6, 9)])


def test_burn_fires_when_the_window_beats_the_multiple():
    trip = evaluate_burn_anomaly(_burn_ledger(100, 1000), window=3,
                                 min_samples=5, multiplier=3.0)

    assert trip is not None
    assert trip.kind == TRIP_BURN_ANOMALY
    assert trip.since_iteration == 6
    assert trip.numbers == {"window_mean": 1000.0, "baseline_mean": 100.0,
                            "multiplier": 3.0, "baseline_samples": 5}


def test_burn_does_not_fire_just_under_or_at_the_multiple():
    just_under = evaluate_burn_anomaly(_burn_ledger(100, 299), window=3,
                                       min_samples=5, multiplier=3.0)
    exactly_at = evaluate_burn_anomaly(_burn_ledger(100, 300), window=3,
                                       min_samples=5, multiplier=3.0)

    assert just_under is None
    # Strictly greater: equalling the multiple is not exceeding it.
    assert exactly_at is None


def test_burn_is_inert_below_the_minimum_sample_count():
    entries = ([_entry(i, tokens=100) for i in range(1, 5)]
               + [_entry(i, tokens=100000) for i in range(5, 8)])

    assert len([e for e in entries if measured_tokens(e) is not None]) == 7
    assert evaluate_burn_anomaly(entries, window=3, min_samples=5,
                                 multiplier=3.0) is None


def test_burn_skips_unmeasured_entries_instead_of_counting_them_as_zero():
    measured_only = _burn_ledger(100, 1000)
    interleaved: list[dict[str, Any]] = []
    for entry in measured_only:
        interleaved.append(_entry(entry["iteration"], tokens=None))
        interleaved.append(entry)
    interleaved.append(_entry(99, tokens=None))

    clean = evaluate_burn_anomaly(measured_only, window=3, min_samples=5,
                                  multiplier=3.0)
    torn = evaluate_burn_anomaly(interleaved, window=3, min_samples=5,
                                 multiplier=3.0)

    assert clean is not None and torn is not None
    # A zero would drag the baseline down and move the window's last slot.
    assert torn.numbers == clean.numbers
    assert torn.numbers["baseline_mean"] == 100.0
    assert torn.numbers["baseline_samples"] == 5
    assert torn.since_iteration == clean.since_iteration == 6
    assert measured_tokens(_entry(1, tokens=None)) is None
    assert measured_tokens(_entry(1, tokens=42)) == 42


# ── goal_drift ─────────────────────────────────────────────────────────────


def test_goal_drift_fires_on_a_milestone_the_plan_never_named():
    entries = [_entry(7, milestone_id="M1"), _entry(8, milestone_id="M-ghost")]

    trip = evaluate_goal_drift(entries, milestone_ids=["M1", "M2"])

    assert trip is not None
    assert trip.kind == TRIP_GOAL_DRIFT
    assert trip.since_iteration == 8
    assert trip.numbers == {"milestone_id": "M-ghost",
                            "known_milestones": ["M1", "M2"]}


def test_goal_drift_stays_silent_when_every_dispatch_is_on_plan():
    entries = [_entry(7, milestone_id="M1"), _entry(8, milestone_id="M2"),
               _entry(9, milestone_id="M-ghost", job_id=None)]

    assert evaluate_goal_drift(entries, milestone_ids=["M1", "M2"]) is None


# ── the aggregate ──────────────────────────────────────────────────────────


def test_evaluate_ledger_reports_trips_in_the_fixed_order():
    entries = ([_entry(i, milestone_id="M-ghost", tokens=100)
                for i in range(1, 6)]
               + [_entry(i, milestone_id="M-ghost", tokens=1000)
                  for i in range(6, 9)])

    trips = evaluate_ledger(entries, milestone_ids=["M1"],
                            thresholds=WatchdogThresholds())

    assert [t.kind for t in trips] == [TRIP_NO_PROGRESS, TRIP_BURN_ANOMALY,
                                       TRIP_GOAL_DRIFT]
    assert [t.since_iteration for t in trips] == [1, 6, 1]
    assert trips[0].numbers["threshold"] == 3
    assert trips[1].numbers["baseline_samples"] == 5
    assert trips[2].numbers["milestone_id"] == "M-ghost"


def test_every_evaluator_tolerates_a_torn_entry_without_raising():
    assert evaluate_no_progress(_TORN_ENTRIES, repeats=3) is None
    assert evaluate_burn_anomaly(_TORN_ENTRIES, window=3, min_samples=5,
                                 multiplier=3.0) is None
    assert evaluate_goal_drift(_TORN_ENTRIES, milestone_ids=["M1"]) is None
    assert evaluate_ledger(_TORN_ENTRIES, milestone_ids=["M1"],
                           thresholds=WatchdogThresholds()) == []

    mixed = [_TORN_ENTRIES[0], _entry(4), _TORN_ENTRIES[1], _entry(5),
             _TORN_ENTRIES[2], _entry(6)]
    trip = evaluate_no_progress(mixed, repeats=3)

    assert trip is not None
    assert trip.kind == TRIP_NO_PROGRESS
    assert trip.since_iteration == 4
    assert trip.numbers == {"repeats": 3, "threshold": 3, "milestone_id": "M1"}


# ── the action: pause, decide, record (F077 T002) ──────────────────────────
#
# These tests DO touch disk, unlike everything above: the action's whole
# subject is what it writes. Every one of them runs under its own ``tmp_path``
# and passes ``root=`` explicitly, and ``REMEDY_DATA_DIR`` points at the same
# directory because ``load_job`` — the one call the action makes that takes no
# root — resolves the job store through it.
#
# Nothing here asserts anything about ``orchestrator_loop.run_mission``:
# ``act_on_trips`` has no call site in the loop at this commit (DECISION F077
# D8), so a green file below proves the action in isolation and nothing else.

ACTION_PROJECT = "p-f077"
T0 = datetime(2026, 8, 14, 9, 0, 0, tzinfo=timezone.utc)


def _trip(kind: str = TRIP_NO_PROGRESS, *, what: str = "") -> Trip:
    """One trip of the given class, carrying the evidence triple T001 builds."""
    return Trip(
        kind=kind,
        what=what or f"{kind} tripped on the evidence below",
        since_iteration=4,
        numbers={"threshold": 3, "milestone_id": "M001"},
    )


def _job_with_tasks(task_count: int = 2) -> Job:
    """The escalation suite's job shape: a planned job with attachable tasks."""
    return Job(
        name="watchdog-job",
        user_prompt="build the watched thing",
        tasks=[Task(description=f"task {i}",
                    inputs={"task_type": "documentation"})
               for i in range(task_count)],
        state=RunState.PLANNED,
    )


@pytest.fixture()
def data_root(tmp_path, monkeypatch):
    """One root for the mission record, its evidence and the job store alike."""
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
    return tmp_path


@pytest.fixture()
def mission(data_root):
    """A persisted ACTIVE mission with no job linked to it yet."""
    created = create_mission(ACTION_PROJECT, "Ship the watched thing",
                             root=data_root)
    return load_mission(ACTION_PROJECT, created.id, data_root)


@pytest.fixture()
def linked_job(mission, data_root):
    """The mission's one linked, persisted job — what a decision attaches to."""
    job = _job_with_tasks()
    save_job(job)
    link_job_to_mission(ACTION_PROJECT, mission.id, str(job.id),
                        MISSION_ROLE_INITIAL, root=data_root)
    return job


def _status(mission_id: str, root: Any) -> str:
    return load_mission(ACTION_PROJECT, mission_id, root).status


def _watchdog_entries(mission_id: str, root: Any) -> list[dict[str, Any]]:
    return [e for e in read_ledger(ACTION_PROJECT, mission_id, root)
            if (e.get("move") or {}).get("kind") == MOVE_WATCHDOG_TRIPPED]


def test_an_empty_trip_list_writes_nothing_at_all(mission, linked_job,
                                                  data_root):
    actions = act_on_trips(ACTION_PROJECT, mission.id, [], root=data_root)

    assert actions == []
    assert _status(mission.id, data_root) == MISSION_STATUS_ACTIVE
    assert not ledger_path(ACTION_PROJECT, mission.id, data_root).is_file()
    assert open_task_decisions(load_job(linked_job.id)) == []


def test_one_trip_pauses_an_active_mission(mission, linked_job, data_root):
    act_on_trips(ACTION_PROJECT, mission.id, [_trip()], root=data_root)

    assert _status(mission.id, data_root) == MISSION_STATUS_PAUSED


def test_an_achieved_mission_is_not_overwritten_by_a_trip(mission, linked_job,
                                                          data_root):
    set_mission_status(ACTION_PROJECT, mission.id, MISSION_STATUS_ACHIEVED,
                       data_root)

    act_on_trips(ACTION_PROJECT, mission.id, [_trip()], root=data_root)

    # Terminal is terminal: the watchdog reports, it does not reopen.
    assert _status(mission.id, data_root) == MISSION_STATUS_ACHIEVED
    assert len(_watchdog_entries(mission.id, data_root)) == 1


def test_the_ledger_entry_carries_the_trip_payload_unchanged(mission,
                                                             linked_job,
                                                             data_root):
    trip = _trip(TRIP_BURN_ANOMALY)

    act_on_trips(ACTION_PROJECT, mission.id, [trip], root=data_root)

    entries = _watchdog_entries(mission.id, data_root)
    assert len(entries) == 1
    entry = entries[0]
    assert entry["move"]["kind"] == MOVE_WATCHDOG_TRIPPED
    assert entry["move"]["payload"] == trip.to_json()
    assert entry["outcome"]["status"] == OUTCOME_WATCHDOG_TRIPPED
    assert entry["outcome"]["detail"] == trip.what
    assert entry["context_digest"] == ""
    assert entry["cost"] == {"calls": 0, "usage": None,
                             "usage_source": "unmeasured"}


def test_the_rendered_ledger_shows_the_evidence_triple(mission, linked_job,
                                                       data_root):
    trip = _trip(TRIP_GOAL_DRIFT, what="dispatched a job for milestone M-ghost")

    act_on_trips(ACTION_PROJECT, mission.id, [trip], root=data_root)

    text = render_ledger(read_ledger(ACTION_PROJECT, mission.id, data_root))
    assert MOVE_WATCHDOG_TRIPPED in text
    assert f"kind: {TRIP_GOAL_DRIFT}" in text
    assert f"what: {trip.what}" in text
    assert f"since_iteration: {trip.since_iteration}" in text
    assert "numbers: " in text
    assert "milestone_id" in text


def test_a_second_trip_of_the_same_class_is_suppressed(mission, linked_job,
                                                       data_root):
    first = act_on_trips(ACTION_PROJECT, mission.id, [_trip()], root=data_root,
                         now=T0)
    second = act_on_trips(ACTION_PROJECT, mission.id, [_trip()], root=data_root,
                          now=T0)

    assert first[0].suppressed is False
    assert first[0].decision_id
    assert second[0].suppressed is True
    assert second[0].decision_id == ""
    assert watchdog_decision_marker(TRIP_NO_PROGRESS) in second[0].note
    # One record, not two — dedup is the point of the marker.
    records = open_task_decisions(load_job(linked_job.id))
    assert len(records) == 1
    assert records[0]["options"] == [DECISION_OPTION_RESUME,
                                     DECISION_OPTION_ABORT]
    assert records[0]["safe_default"] == ""
    # Both calls still recorded themselves.
    assert len(_watchdog_entries(mission.id, data_root)) == 2


def test_two_trip_classes_in_one_call_raise_two_decisions(mission, linked_job,
                                                          data_root):
    trips = [_trip(TRIP_NO_PROGRESS), _trip(TRIP_BURN_ANOMALY)]

    actions = act_on_trips(ACTION_PROJECT, mission.id, trips, root=data_root,
                           now=T0)

    assert [a.suppressed for a in actions] == [False, False]
    questions = [r["question"]
                 for r in open_task_decisions(load_job(linked_job.id))]
    assert len(questions) == 2
    assert questions[0].startswith(watchdog_decision_marker(TRIP_NO_PROGRESS))
    assert questions[1].startswith(watchdog_decision_marker(TRIP_BURN_ANOMALY))


def test_answering_the_decision_lifts_the_suppression(mission, linked_job,
                                                      data_root):
    first = act_on_trips(ACTION_PROJECT, mission.id, [_trip()], root=data_root,
                         now=T0)
    assert act_on_trips(ACTION_PROJECT, mission.id, [_trip()],
                        root=data_root, now=T0)[0].suppressed is True

    job = load_job(linked_job.id)
    assert answer_task_decision(job, first[0].decision_id,
                                answer=DECISION_OPTION_RESUME, now=T0)
    save_job(job)

    third = act_on_trips(ACTION_PROJECT, mission.id, [_trip()], root=data_root,
                         now=T0)

    assert third[0].suppressed is False
    assert third[0].decision_id
    assert third[0].decision_id != first[0].decision_id


def test_a_mission_with_no_linked_job_still_pauses_and_still_records(mission,
                                                                    data_root):
    actions = act_on_trips(ACTION_PROJECT, mission.id, [_trip()],
                           root=data_root)

    assert len(actions) == 1
    assert actions[0].decision_id == ""
    assert actions[0].suppressed is False
    assert "no job is linked" in actions[0].note
    assert _status(mission.id, data_root) == MISSION_STATUS_PAUSED
    entries = _watchdog_entries(mission.id, data_root)
    assert len(entries) == 1
    # The gap is reported in the entry a human reads, not swallowed.
    assert "no job is linked" in entries[0]["outcome"]["detail"]


def test_a_watchdog_entry_is_inert_to_a_later_watchdog_pass(mission,
                                                            linked_job,
                                                            data_root):
    act_on_trips(ACTION_PROJECT, mission.id, [_trip()], root=data_root)
    written = _watchdog_entries(mission.id, data_root)[0]

    assert dispatched_entries([written]) == []
    assert measured_tokens(written) is None

    without = [_entry(4), _entry(5)]
    with_entry = [_entry(4), written, _entry(5)]
    verdict_without = evaluate_no_progress(without, repeats=2)
    verdict_with = evaluate_no_progress(with_entry, repeats=2)

    assert verdict_without is not None
    assert verdict_with == verdict_without


def test_a_caller_supplied_iteration_is_the_number_the_entry_carries(
        mission, linked_job, data_root):
    act_on_trips(ACTION_PROJECT, mission.id,
                 [_trip(TRIP_NO_PROGRESS), _trip(TRIP_BURN_ANOMALY)],
                 root=data_root, iteration=17)

    numbers = [e["iteration"] for e in _watchdog_entries(mission.id, data_root)]
    # Simultaneous trips genuinely happened in ONE iteration (DECISION D6).
    assert numbers == [17, 17]


def test_without_an_iteration_the_entries_number_themselves_consecutively(
        mission, linked_job, data_root):
    act_on_trips(ACTION_PROJECT, mission.id,
                 [_trip(TRIP_NO_PROGRESS), _trip(TRIP_BURN_ANOMALY)],
                 root=data_root)

    numbers = [e["iteration"] for e in _watchdog_entries(mission.id, data_root)]
    assert numbers == [1, 2]
