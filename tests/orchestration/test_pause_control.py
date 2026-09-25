"""F025 T001 first half — the pause control files of both scopes and the mask arithmetic.

One class per scope (job, task) and one for the pure mask, over a ``tmp_path`` control root.
The graph rows build their plan with ``test_dag_schedule.flight_task``, imported, so the
mask's ``downstream`` and ``dag_schedule.blocked_downstream`` cannot drift apart.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration import dag_schedule as ds
from packages.orchestration import pause_control as pc
from packages.orchestration import safe_points as sp
from tests.orchestration.test_dag_schedule import flight_task
from tests.orchestration.test_dag_schedule import ids as dag_ids

JOB = "f025job0000000a"


@pytest.fixture
def control(tmp_path) -> Path:
    """A control root of our own. Nothing here touches the developer's real data dir."""
    return tmp_path / "control"


def _diamond(**states: RunState) -> list:
    """A -> (B, C) -> D, built with dag_schedule's own ``flight_task`` helper — the same
    shape ``test_dag_schedule.diamond`` builds, so the two readings cannot drift apart."""
    return [
        flight_task("A", status=states.get("A", RunState.PENDING)),
        flight_task("B", "A", status=states.get("B", RunState.PENDING)),
        flight_task("C", "A", status=states.get("C", RunState.PENDING)),
        flight_task("D", "B", "C", status=states.get("D", RunState.PENDING)),
    ]


# ---------------------------------------------------------------------------
# Job scope
# ---------------------------------------------------------------------------


class TestJobScopePause:
    def test_idempotent_second_request_returns_the_first_signal(self, control):
        first = pc.request_pause(JOB, "first", "cli", control_root_path=control)
        second = pc.request_pause(JOB, "second", "ui", control_root_path=control)
        assert second.request_id == first.request_id
        assert second.reason == "first"            # the pending request stands, unchanged

    def test_a_publication_race_converges_on_the_winners_signal(self, control, monkeypatch):
        """Force the exact interleaving: our caller reads "nothing pending", another caller
        publishes, and only THEN does our caller try to link."""
        winner: dict[str, pc.PauseSignal] = {}
        real_write = pc._fs.write_file_atomically

        def _slip_in_first(dir_fd, name, data, **kw):
            if name == pc.PAUSE_REQUEST_FILENAME and "winner" not in winner:
                winner["winner"] = None                    # re-entry guard
                monkeypatch.undo()
                winner["winner"] = pc.request_pause(
                    JOB, "the other terminal", "cli", control_root_path=control)
            return real_write(dir_fd, name, data, **kw)

        monkeypatch.setattr(
            "packages.orchestration.pause_control._fs.write_file_atomically", _slip_in_first)

        got = pc.request_pause(JOB, "our terminal", "cli", control_root_path=control)
        assert got.request_id == winner["winner"].request_id
        assert got.reason == "the other terminal"          # the winner's request stands

    def test_cheap_check_is_none_on_a_missing_root_or_job(self, control):
        assert pc.pause_requested(JOB, control_root_path=control) is None
        assert pc.pause_requested(JOB, control_root_path=control / "nested" / "deeper") is None

    def test_settle_archives_before_removing_the_pending_file(self, control):
        signal = pc.request_pause(JOB, "x", "cli", control_root_path=control)
        path = pc.settle_pause(JOB, signal, "served", control_root_path=control)

        assert path == f"jobs/{JOB}/pause_archive/{signal.request_id}.json"
        assert pc.pause_requested(JOB, control_root_path=control) is None

        archived = control / "jobs" / JOB / "pause_archive" / f"{signal.request_id}.json"
        assert archived.is_file()
        payload = json.loads(archived.read_text())
        assert payload["outcome"] == "served"
        assert payload["settled_at"]
        assert payload["request_id"] == signal.request_id

        # Nothing here goes under the stop's own archive/ directory.
        assert sp.stop_status(JOB, control_root_path=control).consumed_count == 0

    def test_a_failed_archive_publication_leaves_the_request_pending(self, control):
        signal = pc.request_pause(JOB, "x", "cli", control_root_path=control)
        adir = control / "jobs" / JOB / "pause_archive"
        adir.mkdir(parents=True, exist_ok=True)
        os.chmod(adir, 0o500)
        try:
            with pytest.raises(pc.PauseControlError):
                pc.settle_pause(JOB, signal, "served", control_root_path=control)
            assert pc.pause_requested(JOB, control_root_path=control) == signal
        finally:
            os.chmod(adir, 0o700)

    def test_a_second_settle_of_an_already_archived_request_writes_nothing_new(self, control):
        signal = pc.request_pause(JOB, "x", "cli", control_root_path=control)
        first_path = pc.settle_pause(JOB, signal, "served", control_root_path=control)
        archived = control / "jobs" / JOB / "pause_archive" / f"{signal.request_id}.json"
        before = archived.read_text()

        second_path = pc.settle_pause(JOB, signal, "served", control_root_path=control)
        assert second_path == first_path
        assert archived.read_text() == before           # not rewritten

    def test_settling_an_old_request_leaves_a_newer_pending_request_in_place(self, control):
        first = pc.request_pause(JOB, "first", "cli", control_root_path=control)
        pc.settle_pause(JOB, first, "served", control_root_path=control)
        second = pc.request_pause(JOB, "second", "cli", control_root_path=control)
        assert second.request_id != first.request_id

        # Settling the OLD (already-archived) signal again must not touch the new pending one.
        pc.settle_pause(JOB, first, "served", control_root_path=control)
        assert pc.pause_requested(JOB, control_root_path=control) == second

    def test_an_unknown_outcome_is_refused_and_nothing_changes(self, control):
        signal = pc.request_pause(JOB, "x", "cli", control_root_path=control)
        with pytest.raises(pc.PauseControlError):
            pc.settle_pause(JOB, signal, "not_a_real_outcome", control_root_path=control)
        assert pc.pause_requested(JOB, control_root_path=control) == signal
        archive_dir = control / "jobs" / JOB / "pause_archive"
        assert not archive_dir.exists()

    def test_withdraw_settles_pending_as_withdrawn_else_none(self, control):
        assert pc.withdraw_pause(JOB, control_root_path=control) is None
        signal = pc.request_pause(JOB, "x", "cli", control_root_path=control)
        withdrawn = pc.withdraw_pause(JOB, control_root_path=control)
        assert withdrawn == signal
        assert pc.pause_requested(JOB, control_root_path=control) is None
        archived = control / "jobs" / JOB / "pause_archive" / f"{signal.request_id}.json"
        assert json.loads(archived.read_text())["outcome"] == "withdrawn"


class TestReasonAndSourceAreBounded:
    def test_an_over_long_reason_is_truncated_never_refused(self, control):
        signal = pc.request_pause(JOB, "x" * 5000, "y" * 5000, control_root_path=control)
        assert len(signal.reason) == sp.MAX_REASON_CHARS
        assert len(signal.source) == sp.MAX_SOURCE_CHARS


# ---------------------------------------------------------------------------
# Task scope
# ---------------------------------------------------------------------------


class TestTaskScopePause:
    def test_idempotent_pause_of_an_already_paused_task_returns_the_existing_entry(
            self, control):
        first = pc.request_task_pause(JOB, "T001", "first", control_root_path=control)
        second = pc.request_task_pause(JOB, "T001", "second", control_root_path=control)
        assert second == first

    def test_releasing_an_unpaused_task_returns_none_and_writes_nothing(self, control):
        # A different task IS paused, so paused_tasks/ exists: this must reach the "no entry
        # for T404" branch, not short-circuit on a wholly missing paused_tasks/ directory.
        pc.request_task_pause(JOB, "T001", control_root_path=control)
        assert pc.release_task_pause(JOB, "T404", control_root_path=control) is None
        archive_dir = control / "jobs" / JOB / "pause_archive"
        assert not archive_dir.exists()
        still = [p.task_id for p in pc.paused_tasks(JOB, control_root_path=control)]
        assert still == ["T001"]

    def test_release_archives_under_pause_archive_tasks_and_removes_the_entry(self, control):
        paused = pc.request_task_pause(JOB, "T001", "x", control_root_path=control)
        released = pc.release_task_pause(JOB, "T001", control_root_path=control)
        assert released == paused
        assert pc.paused_tasks(JOB, control_root_path=control) == ()

        name = pc._task_pause_filename("T001")
        archived = control / "jobs" / JOB / "pause_archive" / "tasks" / name
        assert archived.is_file()
        payload = json.loads(archived.read_text())
        assert payload["outcome"] == "released"
        assert payload["settled_at"]

    @pytest.mark.parametrize("times", [
        ["2026-01-01T00:00:03+00:00", "2026-01-01T00:00:01+00:00",
         "2026-01-01T00:00:02+00:00"],                       # chronological, not insertion
        ["2026-01-01T00:00:00+00:00"] * 3,                   # a tie breaks by task_id
    ])
    def test_paused_tasks_orders_by_requested_at_then_task_id(self, control, monkeypatch,
                                                              times):
        it = iter(times)
        monkeypatch.setattr(pc._sp, "utc_now_iso", lambda: next(it))
        pc.request_task_pause(JOB, "T003", control_root_path=control)
        pc.request_task_pause(JOB, "T001", control_root_path=control)
        pc.request_task_pause(JOB, "T002", control_root_path=control)
        got = [p.task_id for p in pc.paused_tasks(JOB, control_root_path=control)]
        assert got == ["T001", "T002", "T003"]

    def test_a_corrupt_entry_raises_rather_than_being_dropped(self, control):
        pc.request_task_pause(JOB, "T001", control_root_path=control)
        name = pc._task_pause_filename("T001")
        path = control / "jobs" / JOB / "paused_tasks" / name
        path.write_text("not json")
        with pytest.raises(pc.PauseControlError):
            pc.paused_tasks(JOB, control_root_path=control)

    def test_a_path_shaped_task_id_round_trips_and_names_no_path_shaped_file(self, control):
        weird = "../../etc/passwd"
        paused = pc.request_task_pause(JOB, weird, control_root_path=control)
        assert paused.task_id == weird

        got = pc.paused_tasks(JOB, control_root_path=control)
        assert len(got) == 1 and got[0].task_id == weird

        tasks_dir = control / "jobs" / JOB / "paused_tasks"
        names = [entry.name for entry in tasks_dir.iterdir()]
        assert len(names) == 1
        for name in names:
            assert "/" not in name and ".." not in name
        assert names[0] == pc._task_pause_filename(weird)

        released = pc.release_task_pause(JOB, weird, control_root_path=control)
        assert released.task_id == weird

    def test_the_task_file_is_named_by_digest_not_by_the_raw_id(self, control):
        pc.request_task_pause(JOB, "simple-id", control_root_path=control)
        tasks_dir = control / "jobs" / JOB / "paused_tasks"
        names = {entry.name for entry in tasks_dir.iterdir()}
        assert names == {pc._task_pause_filename("simple-id")}
        assert "simple-id.json" not in names

    @pytest.mark.parametrize("bad_id", ["", "x" * (pc.MAX_TASK_ID_CHARS + 1)])
    def test_an_empty_or_over_long_task_id_is_refused(self, control, bad_id):
        with pytest.raises(pc.PauseControlError):
            pc.request_task_pause(JOB, bad_id, control_root_path=control)

    def test_a_symlinked_paused_tasks_directory_is_refused(self, control):
        job_dir = control / "jobs" / JOB
        job_dir.mkdir(parents=True)
        real_target = control / "elsewhere"
        real_target.mkdir()
        (job_dir / "paused_tasks").symlink_to(real_target)
        with pytest.raises(pc.PauseControlError):
            pc.paused_tasks(JOB, control_root_path=control)


# ---------------------------------------------------------------------------
# The mask
# ---------------------------------------------------------------------------


class TestTheMask:
    @pytest.mark.parametrize("paused_id,withheld,downstream", [
        ("A", ("A", "B", "C"), ("B", "C")),   # first: spares nothing after it
        ("B", ("B", "C"), ("C",)),            # middle: spares the tasks before it
        ("C", ("C",), ()),                    # last: withholds only itself
    ])
    def test_linear_paused_position_decides_what_is_spared(self, paused_id, withheld,
                                                            downstream):
        order = ["A", "B", "C"]
        res = pc.withheld_task_ids(order, order, [paused_id])
        assert res.withheld == withheld
        assert res.paused == (paused_id,)
        assert res.downstream == downstream
        assert res.inert == ()

    def test_linear_a_paused_task_already_done_is_inert_and_withholds_nothing(self):
        order = ["A", "B", "C"]
        res = pc.withheld_task_ids(order, ["B", "C"], ["A"])    # A is done, not pending
        assert res.withheld == ()
        assert res.paused == ()
        assert res.downstream == ()
        assert res.inert == ("A",)

    def test_linear_two_paused_tasks(self):
        order = ["A", "B", "C", "D"]
        res = pc.withheld_task_ids(order, order, ["B", "D"])
        assert res.withheld == ("B", "C", "D")
        assert res.paused == ("B", "D")
        assert res.downstream == ("C",)
        assert res.inert == ()

    def test_inert_ids_are_reported_in_the_order_given_and_deduplicated(self):
        res = pc.withheld_task_ids(["A", "B"], [], ["Z", "Y", "Z", "A"])
        assert res.inert == ("Z", "Y", "A")

    def test_graph_downstream_equals_dag_schedule_blocked_downstream_on_the_diamond(self):
        tasks = _diamond(A=RunState.COMPLETED)
        nodes = ds.build_graph(tasks)
        depends_on = {n.task_id: n.depends_on for n in nodes}
        order = [t.task_id for t in tasks]
        pending = [t.task_id for t in tasks if t.status == RunState.PENDING]
        seeds = dag_ids(tasks, "B")

        res = pc.withheld_task_ids(order, pending, seeds, depends_on=depends_on)
        expected = ds.blocked_downstream(tasks, seeds)
        assert set(res.downstream) == expected
        assert res.paused == tuple(seeds)

    def test_graph_transitive_dependents_beyond_the_immediate_child_are_withheld(self):
        order = ["A", "B", "C", "D"]
        depends_on = {"A": (), "B": ("A",), "C": ("B",), "D": ("C",)}
        res = pc.withheld_task_ids(order, order, ["A"], depends_on=depends_on)
        assert res.withheld == ("A", "B", "C", "D")
        assert res.downstream == ("B", "C", "D")

    def test_graph_a_paused_task_that_is_not_pending_does_not_withhold_its_dependents(self):
        # A completed, B running (paused but NOT pending), C and D pending.
        tasks = _diamond(A=RunState.COMPLETED, B=RunState.RUNNING)
        nodes = ds.build_graph(tasks)
        depends_on = {n.task_id: n.depends_on for n in nodes}
        order = [t.task_id for t in tasks]
        pending = [t.task_id for t in tasks if t.status == RunState.PENDING]
        seeds = dag_ids(tasks, "B")

        res = pc.withheld_task_ids(order, pending, seeds, depends_on=depends_on)
        assert res.withheld == ()
        assert res.downstream == ()
        assert res.inert == tuple(seeds)
        assert dag_ids(tasks, "D")[0] not in res.withheld
