"""F025 R2 T001 (second half) — the pause at `run_job`'s own safe points.

DECISION F025 D1's semantics table (clause 5), proved row by row: every provider
call already in flight finishes and nothing new starts, a park persists `paused`
with a pause record before it archives the request, the relaunch is the resume,
a stop always beats a pause, and the wall clock keeps counting through one.

Reuses the fake providers and fixtures of `test_job_stop_integration.py` exactly
as that file drives a real stop: the actual `run_job` caller loop and the actual
ping-pong loop, deterministic fake providers, and a pause requested the way an
operator requests it — by writing the control file — from inside a provider call
where that matters.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta

import pytest

from packages.orchestration import pause_control as pc
from packages.orchestration import pingpong_job as pj
from packages.orchestration.job_plan import APPROVED_PLAN_HASH_KEY
from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_COMPLETED,
    JOB_PAUSED,
    JOB_STOPPED,
    TASK_APPLIED,
    TASK_PENDING,
    format_job_report_text,
    load_job_plan,
    parse_job_file,
    run_job,
    save_job_plan,
)
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration.safe_points import job_control_dir, request_stop

# Reused exactly, per the block: the fixtures and fakes a real stop is already
# driven through, so a pause is driven the same honest way.
from tests.orchestration.test_job_stop_integration import (  # noqa: F401
    _ONE_TASK_JOB,
    _THREE_TASK_JOB,
    _TWO_TASK_JOB,
    _events,
    _pass_provider,
    demo_repo,
    isolate_data_root,
)


class PauseTriggerProvider(FakeProvider):
    """A fake Builder that fires *trigger* while its Nth call is IN FLIGHT — the
    same race `CountingProvider` proves for a stop, reused for a pause: the
    control file appears mid-call, and the call still returns normally."""

    def __init__(self, *, on_build: int = 0, trigger=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.on_build = on_build
        self.trigger = trigger
        self.build_calls = 0
        self.review_calls = 0

    def build(self, prompt, **kwargs):
        self.build_calls += 1
        if self.on_build and self.build_calls == self.on_build and self.trigger:
            self.trigger()
        return super().build(prompt, **kwargs)

    def review(self, prompt, **kwargs):
        self.review_calls += 1
        return super().review(prompt, **kwargs)


class TestRow1JobPauseDuringABuildCall:
    def test_lets_the_call_finish_and_starts_no_reviewer(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        builder = PauseTriggerProvider(
            on_build=1,
            trigger=lambda: pc.request_pause(job.job_id, "mid-build pause", "cli"),
            pass_on_round=1, fail_on_round=99)
        reviewer = _pass_provider()

        parked = run_job(job.job_id, builder_provider=builder,
                         reviewer_provider=reviewer, repair_rounds=0)

        assert builder.build_calls == 1
        assert reviewer.review_calls == 0
        assert parked.state == JOB_PAUSED
        assert parked.pause.get("scope") == "job"
        assert parked.tasks[0].status == TASK_PENDING
        assert len(_events(isolate_data_root, job.job_id, "job_paused")) == 1

        # the request is archived `served` and no `pause.json` remains.
        assert pc.pause_requested(job.job_id) is None
        archive_dir = job_control_dir(job.job_id) / pc.PAUSE_ARCHIVE_DIRNAME
        archived = list(archive_dir.glob("*.json"))
        assert len(archived) == 1
        record = json.loads(archived[0].read_text())
        assert record["outcome"] == "served"


class TestRow2JobPauseBeforeTheRun:
    def test_parks_with_zero_provider_calls(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        pc.request_pause(job.job_id, "taking a break", "cli")
        builder = _pass_provider()
        reviewer = _pass_provider()

        parked = run_job(job.job_id, builder_provider=builder,
                         reviewer_provider=reviewer, repair_rounds=0)

        assert parked.state == JOB_PAUSED
        assert builder.build_calls == 0 and reviewer.review_calls == 0
        assert all(t.status == TASK_PENDING for t in parked.tasks)
        assert parked.pause.get("scope") == "job"


class TestRow3TheRelaunchResumes:
    def test_writes_one_job_resumed_and_matches_an_unpaused_control_run(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        builder = PauseTriggerProvider(
            on_build=1,
            trigger=lambda: pc.request_pause(job.job_id, "reason", "cli"),
            pass_on_round=1, fail_on_round=99)
        parked = run_job(job.job_id, builder_provider=builder,
                         reviewer_provider=_pass_provider(), repair_rounds=0)
        assert parked.state == JOB_PAUSED

        resumed = run_job(job.job_id, builder_provider=_pass_provider(),
                          reviewer_provider=_pass_provider(), repair_rounds=0)
        assert resumed.state == JOB_COMPLETED
        assert [t.status for t in resumed.tasks] == [TASK_APPLIED, TASK_APPLIED]
        assert len(_events(isolate_data_root, job.job_id, "job_resumed")) == 1
        assert resumed.pause == {}
        # S5: "first_running_at is never reset by a park or a relaunch."
        assert resumed.first_running_at == parked.first_running_at

        control = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        control_done = run_job(control.job_id, builder_provider=_pass_provider(),
                               reviewer_provider=_pass_provider(), repair_rounds=0)
        assert control_done.state == resumed.state
        assert [t.status for t in control_done.tasks] == [t.status for t in resumed.tasks]


class TestRow4AMidPlanTaskPause:
    def test_earlier_task_runs_and_the_rest_park_withheld(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_THREE_TASK_JOB, str(demo_repo))
        task2_id = job.tasks[1].task_id
        task3_id = job.tasks[2].task_id
        pc.request_task_pause(job.job_id, task2_id, "second task needs a human", "cli")

        builder = _pass_provider()
        reviewer = _pass_provider()
        parked = run_job(job.job_id, builder_provider=builder,
                         reviewer_provider=reviewer, repair_rounds=0)

        assert parked.tasks[0].status == TASK_APPLIED
        assert parked.state == JOB_PAUSED
        assert parked.pause.get("scope") == "task"
        assert parked.pause.get("paused_task_ids") == [task2_id]
        assert parked.pause.get("withheld_task_ids") == [task2_id, task3_id]
        assert builder.build_calls == 1        # only task 1's Builder ran
        # The PRE-TASK safe point blocks task 2 before it is EVER dispatched —
        # never mind halted after starting — so it never earns a run id.
        assert parked.tasks[1].run_id == ""
        assert parked.tasks[2].run_id == ""


class TestRow5AnInFlightTaskPause:
    def test_halts_then_stays_parked_until_released_then_resumes(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        task_id = job.tasks[0].task_id
        builder = PauseTriggerProvider(
            on_build=1,
            trigger=lambda: pc.request_task_pause(job.job_id, task_id, "look at this", "cli"),
            pass_on_round=1, fail_on_round=99)
        reviewer = _pass_provider()

        parked = run_job(job.job_id, builder_provider=builder,
                         reviewer_provider=reviewer, repair_rounds=0)
        assert builder.build_calls == 1 and reviewer.review_calls == 0
        assert parked.state == JOB_PAUSED
        assert parked.pause.get("scope") == "task"
        assert parked.tasks[0].status == TASK_PENDING
        assert len(_events(isolate_data_root, job.job_id, "job_paused")) == 1

        # still paused: the relaunch stays parked, no event, zero calls.
        builder2 = _pass_provider()
        reviewer2 = _pass_provider()
        still = run_job(job.job_id, builder_provider=builder2,
                        reviewer_provider=reviewer2, repair_rounds=0)
        assert still.state == JOB_PAUSED
        assert builder2.build_calls == 0 and reviewer2.review_calls == 0
        assert len(_events(isolate_data_root, job.job_id, "job_paused")) == 1
        assert len(_events(isolate_data_root, job.job_id, "job_resumed")) == 0

        pc.release_task_pause(job.job_id, task_id)
        done = run_job(job.job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), repair_rounds=0)
        assert done.state == JOB_COMPLETED
        assert len(_events(isolate_data_root, job.job_id, "job_resumed")) == 1


class TestRow6AStopBeatsAPause:
    def test_a_pending_stop_and_a_pending_job_pause_the_stop_wins(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        request_stop(job.job_id, "operator stop", "cli")
        pending_pause = pc.request_pause(job.job_id, "operator pause", "cli")

        done = run_job(job.job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), repair_rounds=0)

        assert done.state == JOB_STOPPED
        assert len(_events(isolate_data_root, job.job_id, "job_paused")) == 0
        archive_path = (job_control_dir(job.job_id) / pc.PAUSE_ARCHIVE_DIRNAME
                        / f"{pending_pause.request_id}.json")
        assert archive_path.is_file()
        assert json.loads(archive_path.read_text())["outcome"] == "superseded_by_stop"
        assert pc.pause_requested(job.job_id) is None

    def test_a_stop_on_a_parked_job_ends_it_stopped_at_relaunch_with_zero_calls(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        pc.request_pause(job.job_id, "operator pause", "cli")
        parked = run_job(job.job_id, builder_provider=_pass_provider(),
                         reviewer_provider=_pass_provider(), repair_rounds=0)
        assert parked.state == JOB_PAUSED

        request_stop(job.job_id, "operator stop", "cli")
        builder2 = _pass_provider()
        reviewer2 = _pass_provider()
        done = run_job(job.job_id, builder_provider=builder2,
                       reviewer_provider=reviewer2, repair_rounds=0)
        assert done.state == JOB_STOPPED
        assert builder2.build_calls == 0 and reviewer2.review_calls == 0


class TestRow7TheDeadlineKeepsCountingThroughAPause:
    def test_a_parked_relaunch_with_an_exhausted_wall_clock_budget_stops_at_zero_calls(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        builder = PauseTriggerProvider(
            on_build=1,
            trigger=lambda: pc.request_pause(job.job_id, "mid-build pause", "cli"),
            pass_on_round=1, fail_on_round=99)
        parked = run_job(job.job_id, builder_provider=builder,
                         reviewer_provider=_pass_provider(), repair_rounds=0)
        assert parked.state == JOB_PAUSED
        assert parked.first_running_at

        reloaded = load_job_plan(job.job_id)
        moved = (datetime.fromisoformat(reloaded.first_running_at)
                - timedelta(days=1)).isoformat()
        reloaded.first_running_at = moved
        # The persisted actuals' own `started_at` must agree with `first_running_at`
        # (`decode_persisted_budget_actuals`'s wall-clock-split guard) — cleared
        # here, not moved, since only the deadline itself is this test's subject.
        reloaded.budget_actuals = None
        save_job_plan(reloaded)

        builder2 = _pass_provider()
        reviewer2 = _pass_provider()
        done = run_job(job.job_id, builder_provider=builder2,
                       reviewer_provider=reviewer2, repair_rounds=0,
                       budgets={"max_wall_clock_minutes": 60})

        assert done.state == JOB_STOPPED
        assert builder2.build_calls == 0 and reviewer2.review_calls == 0
        assert "max_wall_clock_minutes" in (done.stop_reason or "")
        assert done.first_running_at == moved


class TestRow8AFailedSettleReparksWithoutADuplicateEvent:
    def test_the_next_run_reparks_and_settles_without_a_second_job_paused(
            self, isolate_data_root, demo_repo, monkeypatch):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        pc.request_pause(job.job_id, "operator pause", "cli")

        real_settle = pc.settle_pause
        calls = {"n": 0}

        def flaky_settle(*args, **kwargs):
            calls["n"] += 1
            if calls["n"] == 1:
                raise pc.PauseControlError("simulated settle failure")
            return real_settle(*args, **kwargs)

        monkeypatch.setattr(pc, "settle_pause", flaky_settle)

        parked = run_job(job.job_id, builder_provider=_pass_provider(),
                         reviewer_provider=_pass_provider(), repair_rounds=0)
        assert parked.state == JOB_PAUSED
        assert parked.pause.get("scope") == "job"
        assert pc.pause_requested(job.job_id) is not None   # still pending
        assert len(_events(isolate_data_root, job.job_id, "job_paused")) == 1

        again = run_job(job.job_id, builder_provider=_pass_provider(),
                        reviewer_provider=_pass_provider(), repair_rounds=0)
        assert again.state == JOB_PAUSED
        assert pc.pause_requested(job.job_id) is None        # now settled
        assert len(_events(isolate_data_root, job.job_id, "job_paused")) == 1
        assert calls["n"] == 2


class TestRow9AnUnreadablePausedTasksEntry:
    def test_blocks_the_job_with_pause_control_error_and_dispatches_nothing(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        # A real entry first, so `paused_tasks/` exists, then corrupted directly
        # on disk — a write no `pause_control` API produces.
        pc.request_task_pause(job.job_id, "some-other-task", "reason", "cli")
        paused_dir = job_control_dir(job.job_id) / pc.PAUSED_TASKS_DIRNAME
        entry = next(paused_dir.iterdir())
        entry.write_bytes(b"{not valid json")

        builder = _pass_provider()
        reviewer = _pass_provider()
        done = run_job(job.job_id, builder_provider=builder,
                       reviewer_provider=reviewer, repair_rounds=0)

        assert done.state == JOB_BLOCKED
        assert (done.error or "").startswith("pause_control_error:")
        assert builder.build_calls == 0 and reviewer.review_calls == 0


class TestRow10MaxTasksVsAnOperatorPause:
    def test_max_tasks_leaves_pause_empty(self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        capped = run_job(job.job_id, builder_provider=_pass_provider(),
                         reviewer_provider=_pass_provider(), repair_rounds=0,
                         max_tasks=1)
        assert capped.state == JOB_PAUSED
        assert capped.pause == {}
        text = format_job_report_text(capped)
        assert "Paused: " in text
        assert "Paused by" not in text

    def test_the_summary_lines_for_job_scope(self, isolate_data_root, demo_repo):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        pc.request_pause(job.job_id, "taking a break", "cli")
        parked = run_job(job.job_id, builder_provider=_pass_provider(),
                         reviewer_provider=_pass_provider(), repair_rounds=0)
        text = format_job_report_text(parked)
        assert "Paused by cli: taking a break" in text
        assert "Withheld tasks:" not in text

    def test_the_summary_lines_for_task_scope(self, isolate_data_root, demo_repo):
        job = parse_job_file(_THREE_TASK_JOB, str(demo_repo))
        task2_id = job.tasks[1].task_id
        task3_id = job.tasks[2].task_id
        pc.request_task_pause(job.job_id, task2_id, "second task needs a human", "cli")
        parked = run_job(job.job_id, builder_provider=_pass_provider(),
                         reviewer_provider=_pass_provider(), repair_rounds=0)
        text = format_job_report_text(parked)
        assert "Paused by cli: second task needs a human" in text
        assert f"Withheld tasks: {task2_id}, {task3_id}" in text


class TestRow11AStaleApprovalRefusesTheRelaunch:
    def test_the_relaunch_is_refused_exactly_as_an_unpaused_run_and_the_pause_stays(
            self, isolate_data_root, demo_repo):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        pc.request_pause(job.job_id, "operator pause", "cli")
        parked = run_job(job.job_id, builder_provider=_pass_provider(),
                         reviewer_provider=_pass_provider(), repair_rounds=0)
        assert parked.state == JOB_PAUSED
        assert parked.pause

        reloaded = load_job_plan(job.job_id)
        reloaded.task_plan = {
            "_approval": "approved",
            APPROVED_PLAN_HASH_KEY: "sha256:0000000000000000000000000000000000000000000000000000000000000000",
            "tasks": [],
        }
        save_job_plan(reloaded)

        refused = run_job(job.job_id, builder_provider=_pass_provider(),
                          reviewer_provider=_pass_provider(), repair_rounds=0)
        assert refused.state == JOB_BLOCKED
        assert (refused.error or "").startswith("plan_changed_since_approval:")
        assert refused.pause == parked.pause


class TestParkNeverSettlesBeforeItIsDurable:
    """S3's own ordering claim, white-box: "the pending request is now the
    transaction's commit record" — exactly `_stop_job`'s reasoning, reused for
    `_park_job`. A `_persist_job` failure must find the pause_control request
    STILL PENDING, never already consumed by a settle that ran ahead of it."""

    def test_a_persist_failure_leaves_the_pause_control_request_pending(
            self, isolate_data_root, demo_repo, monkeypatch):
        job = parse_job_file(_ONE_TASK_JOB, str(demo_repo))
        requested = pc.request_pause(job.job_id, "operator pause", "cli")
        signal = pj._PauseSignal(
            job_id=job.job_id, request_id=requested.request_id,
            reason=f"operator_pause: {requested.reason}",
            source=requested.source, requested_at=requested.requested_at,
            scope="job")

        real_persist = pj._persist_job
        calls = {"n": 0}

        def flaky_persist(job_arg, root=None):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RuntimeError("simulated durability failure")
            return real_persist(job_arg, root)

        monkeypatch.setattr(pj, "_persist_job", flaky_persist)

        with pytest.raises(RuntimeError):
            pj._park_job(job, signal, task=None)

        assert pc.pause_requested(job.job_id) is not None


class TestR1049APauseSettleFailureInsideAServedStopStillStops:
    """R-1049's FIX clause: `_stop_job`'s pause-settle-on-stop catch now names
    only the two errors that settle can raise (`pause_control.PauseControlError`
    and `safe_points.StopControlError`) instead of a blind `except Exception`,
    and logs rather than passes — but the stop it guards must still finish
    exactly as it did before, never mind what the settle did."""

    def test_a_pause_control_error_from_the_settle_does_not_block_the_stop(
            self, isolate_data_root, demo_repo, monkeypatch):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        request_stop(job.job_id, "operator stop", "cli")
        pc.request_pause(job.job_id, "operator pause", "cli")

        def raising_settle(*args, **kwargs):
            raise pc.PauseControlError("simulated settle failure")

        monkeypatch.setattr(pc, "settle_pause", raising_settle)

        done = run_job(job.job_id, builder_provider=_pass_provider(),
                       reviewer_provider=_pass_provider(), repair_rounds=0)

        assert done.state == JOB_STOPPED
        # the settle never landed: the pause request is still pending.
        assert pc.pause_requested(job.job_id) is not None


class TestR1050AFailedPausedEventReparksAndClearsTheError:
    """R-1050's FIX clause, `job_paused` half: a write that raises is recorded
    on the pause record as `event_error` rather than vanishing, and a
    job-scope request stays pending until the event actually lands — the next
    run re-parks on the SAME request, writes exactly one `job_paused`, settles
    the request, and clears `event_error` (because `park_job_pause` always
    rebuilds `job.pause` fresh from the signal)."""

    def test_the_next_run_writes_one_job_paused_and_clears_event_error(
            self, isolate_data_root, demo_repo, monkeypatch):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        pc.request_pause(job.job_id, "operator pause", "cli")

        from packages.orchestration.run_log import RunLogWriter

        real_log = RunLogWriter.log
        calls = {"n": 0}

        def flaky_log(self, event, **kwargs):
            if event == "job_paused":
                calls["n"] += 1
                if calls["n"] == 1:
                    raise RuntimeError("simulated ledger failure")
            return real_log(self, event, **kwargs)

        monkeypatch.setattr(RunLogWriter, "log", flaky_log)

        parked = run_job(job.job_id, builder_provider=_pass_provider(),
                         reviewer_provider=_pass_provider(), repair_rounds=0)
        assert parked.state == JOB_PAUSED
        assert parked.pause.get("event_error", "").startswith(
            "job_paused_event_failed:")
        assert pc.pause_requested(job.job_id) is not None   # NOT settled
        assert len(_events(isolate_data_root, job.job_id, "job_paused")) == 0

        again = run_job(job.job_id, builder_provider=_pass_provider(),
                        reviewer_provider=_pass_provider(), repair_rounds=0)
        assert again.state == JOB_PAUSED
        assert "event_error" not in again.pause
        assert pc.pause_requested(job.job_id) is None       # now settled
        assert len(_events(isolate_data_root, job.job_id, "job_paused")) == 1
        assert calls["n"] == 2


class TestR1050AFailedResumedEventStillCompletesTheRun:
    """R-1050's FIX clause, `job_resumed` half: a write that raises is recorded
    as `job.metadata["pause_event_error"]` and the resume PROCEEDS regardless
    — the run is not held hostage by a ledger that cannot be written."""

    def test_the_run_completes_with_pause_event_error_recorded(
            self, isolate_data_root, demo_repo, monkeypatch):
        job = parse_job_file(_TWO_TASK_JOB, str(demo_repo))
        pc.request_pause(job.job_id, "operator pause", "cli")
        parked = run_job(job.job_id, builder_provider=_pass_provider(),
                         reviewer_provider=_pass_provider(), repair_rounds=0)
        assert parked.state == JOB_PAUSED

        from packages.orchestration.run_log import RunLogWriter

        real_log = RunLogWriter.log

        def flaky_log(self, event, **kwargs):
            if event == "job_resumed":
                raise RuntimeError("simulated ledger failure")
            return real_log(self, event, **kwargs)

        monkeypatch.setattr(RunLogWriter, "log", flaky_log)

        resumed = run_job(job.job_id, builder_provider=_pass_provider(),
                          reviewer_provider=_pass_provider(), repair_rounds=0)
        assert resumed.state == JOB_COMPLETED
        assert resumed.pause == {}
        assert resumed.metadata.get("pause_event_error", "").startswith(
            "job_resumed_event_failed:")
        assert len(_events(isolate_data_root, job.job_id, "job_resumed")) == 0
