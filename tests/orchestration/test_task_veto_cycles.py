"""F027 R3 — the cycle executor's own fold of a veto (DECISION F027 D3 (3)).

``ready_tasks`` gains a ``vetoed_ids`` seed set, withheld with its transitive
dependents exactly as the paused seeds are, except the inertness rule reads
"not completed" rather than "pending" — the cycle executor never writes
``vetoed`` into a task's own status, so a vetoed seed can stand at any other
status the veto still reaches. ``run_cycles`` re-reads ``task_veto.vetoed_tasks``
at the batch boundary and before every pick, and ends the run ``TERMINAL_BLOCKED``
naming both sets when the vetoed seeds withhold the last pending work, or with
``task_veto_control_error`` when the control area cannot be read.

Driven through an injected ``task_step`` exactly as
``tests/orchestration/test_pause_resume_cycles.py`` drives the pause brought to
the cycle executor: the same ``isolate_data_root``/``control_root`` fixtures,
the same ``FakeProvider``/``FakeClock``, and the same ``SteeredStep``/diamond
job for DAG withholding.
"""
from __future__ import annotations

import json
from pathlib import Path

import packages.orchestration.long_run_executor as lre
from packages.core.models import RunState
from packages.orchestration import task_veto as tv
from packages.orchestration.long_run_executor import (
    TERMINAL_ALL_GREEN,
    TERMINAL_BLOCKED,
    CycleLimits,
    ready_tasks,
    run_cycles,
)

# Reused exactly, per the block: the fixtures and fakes the pause counterpart
# (test_pause_resume_cycles.py) is already driven through.
from tests.orchestration.test_long_run_executor import (  # noqa: F401
    FakeClock,
    FakeProvider,
    SteeredStep,
    control_root,
    isolate_data_root,
    make_diamond_job,
    make_job,
    never_called_step,
    no_save,
    passing_verify,
    planned_id_of,
    task_by_planned_id,
)


def _events(data_root: Path, job_id: str, event: str) -> list[dict]:
    """Mirrors `test_pause_resume_cycles._events`: every ledger event of this
    name for this job, across every run-log file `RunLogWriter` produced."""
    runs = data_root / "job_logs" / job_id
    out: list[dict] = []
    for f in sorted(runs.glob("*.jsonl")) if runs.is_dir() else []:
        for line in f.read_text().splitlines():
            if line.strip():
                raw = json.loads(line)
                if raw.get("event") == event:
                    out.append(raw)
    return out


# ---------------------------------------------------------------------------
# ready_tasks unit tests over the diamond
# ---------------------------------------------------------------------------


class TestReadyTasksVetoedIds:
    def test_a_vetoed_branch_withholds_itself_and_its_dependent(self):
        job = make_diamond_job()
        a_task = task_by_planned_id(job, "A")
        a_task.status = RunState.COMPLETED       # B and C are otherwise ready
        b_id = str(task_by_planned_id(job, "B").task_id)
        c_id = str(task_by_planned_id(job, "C").task_id)
        d_id = str(task_by_planned_id(job, "D").task_id)

        ready = ready_tasks(job, 10, vetoed_ids=(b_id,))

        assert b_id not in ready
        assert d_id not in ready
        assert ready == [c_id]

    def test_a_veto_of_a_completed_task_is_inert(self):
        job = make_diamond_job()
        a_task = task_by_planned_id(job, "A")
        a_task.status = RunState.COMPLETED
        a_id = str(a_task.task_id)
        b_id = str(task_by_planned_id(job, "B").task_id)
        c_id = str(task_by_planned_id(job, "C").task_id)

        ready = ready_tasks(job, 10, vetoed_ids=(a_id,))

        assert set(ready) == {b_id, c_id}          # A's own completion withholds nothing

    def test_a_vetoed_seed_joins_the_downstream_computation(self, monkeypatch):
        """White-box: a vetoed seed alone is already unready by DAG completion
        rules (B's own dependent never becomes ready while B stays PENDING), so
        the black-box ready-list cannot by itself prove the seed reached
        ``blocked_downstream`` — this pins the CALL, exactly the way the paused
        seeds are already proven to join it."""
        job = make_diamond_job()
        a_task = task_by_planned_id(job, "A")
        a_task.status = RunState.COMPLETED
        b_id = str(task_by_planned_id(job, "B").task_id)

        calls: list[set] = []
        real_blocked_downstream = lre.blocked_downstream

        def spy(tasks, blocked_ids):
            calls.append(set(blocked_ids))
            return real_blocked_downstream(tasks, blocked_ids)

        monkeypatch.setattr(lre, "blocked_downstream", spy)

        lre.ready_tasks(job, 10, vetoed_ids=(b_id,))

        assert calls, "blocked_downstream must run when a veto is the only seed"
        assert b_id in calls[0]


# ---------------------------------------------------------------------------
# B vetoed before the run
# ---------------------------------------------------------------------------


class TestVetoBeforeTheRun:
    def test_a_and_c_complete_b_and_d_stay_pending_with_the_exact_stop_reason(
            self, isolate_data_root, control_root):
        job = make_diamond_job()
        b_task = task_by_planned_id(job, "B")
        d_task = task_by_planned_id(job, "D")
        veto = tv.veto_task_command(
            job, task_id=str(b_task.task_id), reason="known-bad approach for B",
            actor="alice", control_root_path=control_root)
        assert veto["outcome"] == "vetoed"
        step = SteeredStep()

        result = run_cycles(
            job, CycleLimits(max_cycles=10, batch_size=1), FakeProvider(),
            task_step=step, verify=passing_verify, clock=FakeClock(),
            save=no_save, control_root_path=control_root,
        )

        assert set(step.executed) == {"A", "C"}
        assert result.terminal_status == TERMINAL_BLOCKED
        assert result.stop_reason == (
            f"all_remaining_work_vetoed; vetoed={b_task.task_id}; "
            f"unreachable={d_task.task_id}")
        assert b_task.status == RunState.PENDING
        assert d_task.status == RunState.PENDING


# ---------------------------------------------------------------------------
# A veto recorded DURING the run
# ---------------------------------------------------------------------------


class TestVetoDuringTheRun:
    def test_a_step_of_a_vetoes_c_and_c_is_never_picked(
            self, isolate_data_root, control_root):
        job = make_diamond_job()
        c_task = task_by_planned_id(job, "C")
        step = SteeredStep()

        def vetoing_step(j, provider_call, task_id=None):
            attempt = step(j, provider_call, task_id=task_id)
            if attempt.task_id is not None and planned_id_of(j, attempt.task_id) == "A":
                result = tv.veto_task_command(
                    j, task_id=str(c_task.task_id), reason="stop C while A runs",
                    actor="ci", control_root_path=control_root)
                assert result["outcome"] == "vetoed"
            return attempt

        result = run_cycles(
            job, CycleLimits(max_cycles=10, batch_size=1), FakeProvider(),
            task_step=vetoing_step, verify=passing_verify, clock=FakeClock(),
            save=no_save, control_root_path=control_root,
        )

        assert "C" not in step.executed
        assert set(step.executed) == {"A", "B"}    # B is independent of C: it still runs
        assert result.terminal_status == TERMINAL_BLOCKED
        assert result.stop_reason.startswith("all_remaining_work_vetoed;")
        assert f"vetoed={c_task.task_id}" in result.stop_reason


# ---------------------------------------------------------------------------
# The only veto names a completed task
# ---------------------------------------------------------------------------


class TestVetoOfACompletedTaskStaysGreen:
    def test_the_run_still_ends_all_green(self, isolate_data_root, control_root):
        job = make_diamond_job()
        a_task = task_by_planned_id(job, "A")
        step = SteeredStep()
        # Run one cycle so A completes, then veto it after the fact (inert).
        run_cycles(
            job, CycleLimits(max_cycles=1, batch_size=1), FakeProvider(),
            task_step=step, verify=passing_verify, clock=FakeClock(),
            save=no_save, control_root_path=control_root,
        )
        assert a_task.status == RunState.COMPLETED
        tv.record_task_veto(str(job.job_id), str(a_task.task_id), "too late now",
                            "alice", RunState.COMPLETED, control_root_path=control_root)

        result = run_cycles(
            job, CycleLimits(max_cycles=10, batch_size=1), FakeProvider(),
            task_step=step, verify=passing_verify, clock=FakeClock(),
            save=no_save, control_root_path=control_root,
        )

        assert result.terminal_status == TERMINAL_ALL_GREEN
        assert set(step.executed) == {"A", "B", "C", "D"}


# ---------------------------------------------------------------------------
# The veto area is unreadable
# ---------------------------------------------------------------------------


class TestUnreadableVetoArea:
    def test_blocks_with_task_veto_control_error_and_zero_task_steps(
            self, isolate_data_root, control_root):
        from packages.orchestration.safe_points import job_control_dir

        job = make_job(2)
        vdir = job_control_dir(str(job.job_id), control_root) / tv.VETOED_TASKS_DIRNAME
        vdir.mkdir(parents=True, exist_ok=True)
        (vdir / "bogus.json").write_text("not json")

        result = run_cycles(
            job, CycleLimits(max_cycles=5), FakeProvider(),
            task_step=never_called_step, verify=passing_verify,
            clock=FakeClock(), save=no_save, control_root_path=control_root,
        )

        assert result.terminal_status == TERMINAL_BLOCKED
        assert result.stop_reason.startswith("task_veto_control_error:")
        assert result.cycles_run == 0
