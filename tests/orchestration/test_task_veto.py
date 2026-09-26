"""F027 T001 — the veto control protocol (DECISION F027 D1): the mandatory verbatim reason,
the pure state gate, the unreachable set through ``dag_schedule.blocked_downstream``, the
create-only control file per vetoed task, the command effect and its ``task_vetoed`` event.

Graph rows build their plan with ``test_dag_schedule.flight_task`` and ``legacy_task``,
imported, so this module's ``downstream`` reading and ``dag_schedule.blocked_downstream``
cannot drift apart — the same discipline ``test_pause_control.py`` follows.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from packages.core.models import RunState
from packages.orchestration import pingpong_job as pj
from packages.orchestration import task_veto as tv
from tests.orchestration.test_dag_schedule import flight_task, legacy_task
from tests.orchestration.test_dag_schedule import ids as dag_ids

JOB = "f027job0000000a"


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch):
    """REMEDY_DATA_DIR to tmp so the ledger reader/writer never touch the real data root."""
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def control(tmp_path: Path) -> Path:
    """A control root of our own. Nothing here touches the developer's real data dir."""
    return tmp_path / "control"


def _secret_shaped_reason() -> str:
    """Built at run time from parts, so no secret-shaped literal sits in the source."""
    parts = ["sk", "-", "ant", "-"] + ["a"] * 24
    return "".join(parts)


def _job(tasks: list, state: RunState = RunState.RUNNING, job_id: str = JOB) -> pj.JobPlan:
    return pj.JobPlan(job_id=job_id, tasks=tasks, state=state)


def _veto_filename(task_id: str) -> str:
    return hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:32] + ".json"


def _read_events(job_id: str) -> list[dict]:
    from packages.orchestration.data_paths import run_log_dir

    out: list[dict] = []
    job_runs = run_log_dir(job_id)
    if not job_runs.is_dir():
        return out
    for jsonl in sorted(job_runs.glob("*.jsonl")):
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_the_reason_cap_and_the_vetoable_statuses():
    assert tv.MAX_VETO_REASON_CHARS == 500
    assert tv.VETOABLE_TASK_STATUSES == (
        pj.TASK_PENDING, pj.TASK_RUNNING, pj.TASK_BLOCKED, pj.TASK_FAILED, pj.TASK_SKIPPED)


# ---------------------------------------------------------------------------
# S3 — the reason, mandatory and kept verbatim
# ---------------------------------------------------------------------------


class TestVetoReason:
    def test_none_is_refused_reason_required(self):
        with pytest.raises(tv.TaskVetoRefused) as exc:
            tv.validate_veto_reason(None)
        assert exc.value.code == "reason_required"

    def test_a_non_string_is_refused_reason_required(self):
        with pytest.raises(tv.TaskVetoRefused) as exc:
            tv.validate_veto_reason(12345)
        assert exc.value.code == "reason_required"

    def test_an_empty_string_is_refused_reason_required(self):
        with pytest.raises(tv.TaskVetoRefused) as exc:
            tv.validate_veto_reason("")
        assert exc.value.code == "reason_required"

    def test_a_whitespace_only_reason_is_refused_reason_required(self):
        with pytest.raises(tv.TaskVetoRefused) as exc:
            tv.validate_veto_reason("   \t  ")
        assert exc.value.code == "reason_required"

    def test_exactly_500_characters_is_accepted_unchanged(self):
        reason = "x" * 500
        assert tv.validate_veto_reason(reason) == reason

    def test_501_characters_is_refused_reason_too_long(self):
        with pytest.raises(tv.TaskVetoRefused) as exc:
            tv.validate_veto_reason("x" * 501)
        assert exc.value.code == "reason_too_long"

    def test_a_newline_is_refused_reason_invalid(self):
        with pytest.raises(tv.TaskVetoRefused) as exc:
            tv.validate_veto_reason("bad\nreason")
        assert exc.value.code == "reason_invalid"

    def test_a_tab_is_refused_reason_invalid(self):
        with pytest.raises(tv.TaskVetoRefused) as exc:
            tv.validate_veto_reason("bad\treason")
        assert exc.value.code == "reason_invalid"

    def test_a_del_character_is_refused_reason_invalid(self):
        with pytest.raises(tv.TaskVetoRefused) as exc:
            tv.validate_veto_reason("bad\x7freason")
        assert exc.value.code == "reason_invalid"

    def test_a_secret_shaped_reason_is_refused_reason_invalid(self):
        with pytest.raises(tv.TaskVetoRefused) as exc:
            tv.validate_veto_reason(_secret_shaped_reason())
        assert exc.value.code == "reason_invalid"

    def test_leading_and_trailing_spaces_are_returned_unchanged(self):
        reason = "  wrong environment, redo after rollback  "
        assert tv.validate_veto_reason(reason) == reason

    def test_a_path_is_returned_unchanged(self):
        reason = "the deploy target was /srv/prod-app/releases/current, stop it"
        assert tv.validate_veto_reason(reason) == reason


# ---------------------------------------------------------------------------
# S4 — the gate, pure
# ---------------------------------------------------------------------------

_ALL_JOB_STATES = list(RunState)
_ALL_TASK_STATUSES = [
    pj.TASK_PENDING, pj.TASK_RUNNING, pj.TASK_PASSED, pj.TASK_APPLIED,
    pj.TASK_BLOCKED, pj.TASK_FAILED, pj.TASK_SKIPPED, pj.TASK_SPLIT, pj.TASK_VETOED,
]
_TERMINAL_JOB_STATES = frozenset({RunState.COMPLETED, RunState.FAILED, RunState.CANCELLED})
_VETOABLE_STATUSES = frozenset(
    {pj.TASK_PENDING, pj.TASK_RUNNING, pj.TASK_BLOCKED, pj.TASK_FAILED, pj.TASK_SKIPPED})


class TestVetoGate:
    @pytest.mark.parametrize("job_state", _ALL_JOB_STATES)
    @pytest.mark.parametrize("task_status", _ALL_TASK_STATUSES)
    def test_the_full_matrix(self, job_state, task_status):
        refusal = tv.veto_refusal(job_state, task_status, already_vetoed=False)
        if job_state in _TERMINAL_JOB_STATES:
            assert refusal is not None
            assert refusal.code == "job_not_vetoable"
            assert job_state.value in refusal.detail
        elif task_status == pj.TASK_VETOED:
            assert refusal is not None
            assert refusal.code == "task_already_vetoed"
            assert task_status in refusal.detail
        elif task_status not in _VETOABLE_STATUSES:
            assert refusal is not None
            assert refusal.code == "task_not_vetoable"
            assert task_status in refusal.detail
        else:
            assert refusal is None

    def test_the_already_vetoed_flag_refuses_an_otherwise_vetoable_status(self):
        refusal = tv.veto_refusal(RunState.RUNNING, pj.TASK_PENDING, already_vetoed=True)
        assert refusal is not None
        assert refusal.code == "task_already_vetoed"

    def test_a_running_job_is_vetoable(self):
        assert tv.veto_refusal(RunState.RUNNING, pj.TASK_PENDING, already_vetoed=False) is None

    def test_a_plain_string_job_state_reads_the_same_as_a_runstate(self):
        by_string = tv.veto_refusal("completed", pj.TASK_PENDING, already_vetoed=False)
        by_enum = tv.veto_refusal(RunState.COMPLETED, pj.TASK_PENDING, already_vetoed=False)
        assert by_string.code == by_enum.code == "job_not_vetoable"


# ---------------------------------------------------------------------------
# S5 — the unreachable set, pure
# ---------------------------------------------------------------------------


class TestVetoUnreachable:
    def _diamond(self, **states):
        return [
            flight_task("A", status=states.get("A", RunState.PENDING)),
            flight_task("B", "A", status=states.get("B", RunState.PENDING)),
            flight_task("C", "A", status=states.get("C", RunState.PENDING)),
            flight_task("D", "B", "C", status=states.get("D", RunState.PENDING)),
        ]

    def test_diamond_veto_b_unreaches_d(self):
        tasks = self._diamond()
        b_id, d_id = dag_ids(tasks, "B", "D")
        assert tv.veto_unreachable(tasks, [b_id]) == (d_id,)

    def test_diamond_veto_a_unreaches_b_c_and_d_in_plan_order(self):
        tasks = self._diamond()
        a_id = dag_ids(tasks, "A")[0]
        b_id, c_id, d_id = dag_ids(tasks, "B", "C", "D")
        assert tv.veto_unreachable(tasks, [a_id]) == (b_id, c_id, d_id)

    def test_diamond_veto_b_and_c_unreaches_only_d(self):
        tasks = self._diamond()
        b_id, c_id, d_id = dag_ids(tasks, "B", "C", "D")
        assert tv.veto_unreachable(tasks, [b_id, c_id]) == (d_id,)

    def test_legacy_tasks_veto_the_second_of_four_unreaches_the_last_two(self):
        tasks = [legacy_task("1"), legacy_task("2"), legacy_task("3"), legacy_task("4")]
        assert tv.veto_unreachable(tasks, [tasks[1].task_id]) == (
            tasks[2].task_id, tasks[3].task_id)

    def test_a_done_task_and_an_already_vetoed_task_are_left_out(self):
        tasks = self._diamond(C=RunState.COMPLETED, D=pj.TASK_VETOED)
        a_id = dag_ids(tasks, "A")[0]
        b_id = dag_ids(tasks, "B")[0]
        assert tv.veto_unreachable(tasks, [a_id]) == (b_id,)


# ---------------------------------------------------------------------------
# S6 — the control files
# ---------------------------------------------------------------------------


class TestControlFiles:
    def test_record_creates_a_file_named_by_digest_with_expected_content(self, control):
        veto, created = tv.record_task_veto(
            JOB, "T001", "bad build target", "alice", pj.TASK_PENDING,
            control_root_path=control)
        assert created is True
        path = control / "jobs" / JOB / "vetoed_tasks" / _veto_filename("T001")
        assert path.is_file()
        payload = json.loads(path.read_text())
        assert payload["task_veto_v"] == 1
        assert payload["job_id"] == JOB
        assert payload["task_id"] == "T001"
        assert payload["reason"] == "bad build target"
        assert payload["actor"] == "alice"
        assert payload["status_at_veto"] == pj.TASK_PENDING
        assert payload["request_id"] == veto.request_id

    def test_a_second_record_of_the_same_task_answers_the_first_unchanged_and_false(
            self, control):
        first, created1 = tv.record_task_veto(
            JOB, "T001", "first reason", "alice", pj.TASK_PENDING, control_root_path=control)
        second, created2 = tv.record_task_veto(
            JOB, "T001", "second reason", "bob", pj.TASK_RUNNING, control_root_path=control)
        assert created1 is True
        assert created2 is False
        assert second == first
        assert second.reason == "first reason"

    def test_a_publication_race_converges_on_the_winner(self, control, monkeypatch):
        winner: dict[str, object] = {}
        real_write = tv._fs.write_file_atomically

        def _slip_in_first(dir_fd, name, data, **kw):
            if "veto" not in winner:
                winner["veto"] = None                      # re-entry guard
                monkeypatch.undo()
                winner["veto"], _ = tv.record_task_veto(
                    JOB, "T001", "the other caller's reason", "carol",
                    pj.TASK_PENDING, control_root_path=control)
            return real_write(dir_fd, name, data, **kw)

        monkeypatch.setattr(
            "packages.orchestration.task_veto._fs.write_file_atomically", _slip_in_first)

        got, created = tv.record_task_veto(
            JOB, "T001", "our reason", "dave", pj.TASK_PENDING, control_root_path=control)
        assert created is False
        assert got.request_id == winner["veto"].request_id
        assert got.reason == "the other caller's reason"

    def test_a_symlinked_vetoed_tasks_directory_is_refused(self, control):
        job_dir = control / "jobs" / JOB
        job_dir.mkdir(parents=True)
        elsewhere = control / "elsewhere"
        elsewhere.mkdir()
        (job_dir / "vetoed_tasks").symlink_to(elsewhere)
        with pytest.raises(tv.TaskVetoError):
            tv.vetoed_tasks(JOB, control_root_path=control)

    def test_an_unparsable_entry_raises(self, control):
        tv.record_task_veto(
            JOB, "T001", "x", "alice", pj.TASK_PENDING, control_root_path=control)
        path = control / "jobs" / JOB / "vetoed_tasks" / _veto_filename("T001")
        path.write_text("not json")
        with pytest.raises(tv.TaskVetoError):
            tv.vetoed_tasks(JOB, control_root_path=control)

    def test_an_entry_with_a_tampered_reason_raises(self, control):
        tv.record_task_veto(
            JOB, "T001", "x", "alice", pj.TASK_PENDING, control_root_path=control)
        path = control / "jobs" / JOB / "vetoed_tasks" / _veto_filename("T001")
        payload = json.loads(path.read_text())
        payload["reason"] = "bad\nreason"
        path.write_text(json.dumps(payload))
        with pytest.raises(tv.TaskVetoError):
            tv.vetoed_tasks(JOB, control_root_path=control)

    @pytest.mark.parametrize("times", [
        ["2026-01-01T00:00:03+00:00", "2026-01-01T00:00:01+00:00",
         "2026-01-01T00:00:02+00:00"],                       # chronological, not insertion
        ["2026-01-01T00:00:00+00:00"] * 3,                   # a tie breaks by task_id
    ])
    def test_vetoed_tasks_orders_by_requested_at_then_task_id(self, control, monkeypatch,
                                                              times):
        it = iter(times)
        monkeypatch.setattr(tv._sp, "utc_now_iso", lambda: next(it))
        tv.record_task_veto(JOB, "T003", "x", "a", pj.TASK_PENDING, control_root_path=control)
        tv.record_task_veto(JOB, "T001", "x", "a", pj.TASK_PENDING, control_root_path=control)
        tv.record_task_veto(JOB, "T002", "x", "a", pj.TASK_PENDING, control_root_path=control)
        got = [v.task_id for v in tv.vetoed_tasks(JOB, control_root_path=control)]
        assert got == ["T001", "T002", "T003"]

    def test_vetoed_tasks_is_empty_on_a_missing_root(self, control):
        assert tv.vetoed_tasks(JOB, control_root_path=control) == ()
        assert tv.vetoed_tasks(JOB, control_root_path=control / "nested" / "deeper") == ()

    def test_an_invalid_job_id_raises_task_veto_error(self, control):
        with pytest.raises(tv.TaskVetoError):
            tv.record_task_veto(
                "", "T001", "x", "a", pj.TASK_PENDING, control_root_path=control)

    def test_an_invalid_task_id_raises_task_veto_error(self, control):
        with pytest.raises(tv.TaskVetoError):
            tv.record_task_veto(
                JOB, "", "x", "a", pj.TASK_PENDING, control_root_path=control)

    def test_a_blank_actor_falls_back_to_unknown(self, control):
        veto, _ = tv.record_task_veto(
            JOB, "T001", "x", "   ", pj.TASK_PENDING, control_root_path=control)
        assert veto.actor == "unknown"


# ---------------------------------------------------------------------------
# S7 — the command effect
# ---------------------------------------------------------------------------


class TestVetoTaskCommand:
    def test_a_blank_reason_with_an_unknown_task_answers_reason_required(self, control):
        job = _job([flight_task("A")])
        result = tv.veto_task_command(
            job, task_id="no-such-task", reason="   ", actor="alice",
            control_root_path=control)
        assert result["outcome"] == "refused"
        assert result["code"] == "reason_required"
        assert result["task_id"] == "no-such-task"

    def test_unknown_task_is_refused_once_the_reason_is_valid(self, control):
        job = _job([flight_task("A")])
        result = tv.veto_task_command(
            job, task_id="no-such-task", reason="stop this", actor="alice",
            control_root_path=control)
        assert result["outcome"] == "refused"
        assert result["code"] == "unknown_task"

    def test_job_not_vetoable_refusal(self, control):
        tasks = [flight_task("A")]
        job = _job(tasks, state=RunState.COMPLETED)
        result = tv.veto_task_command(
            job, task_id=tasks[0].task_id, reason="stop", actor="a", control_root_path=control)
        assert result["outcome"] == "refused"
        assert result["code"] == "job_not_vetoable"

    def test_task_not_vetoable_refusal(self, control):
        tasks = [flight_task("A", status=RunState.COMPLETED)]
        job = _job(tasks)
        result = tv.veto_task_command(
            job, task_id=tasks[0].task_id, reason="stop", actor="a", control_root_path=control)
        assert result["outcome"] == "refused"
        assert result["code"] == "task_not_vetoable"

    def test_task_already_vetoed_refusal_when_an_entry_already_exists(self, control):
        tasks = [flight_task("A")]
        job = _job(tasks)
        first = tv.veto_task_command(
            job, task_id=tasks[0].task_id, reason="stop", actor="a", control_root_path=control)
        assert first["outcome"] == "vetoed"
        second = tv.veto_task_command(
            job, task_id=tasks[0].task_id, reason="stop again", actor="b",
            control_root_path=control)
        assert second["outcome"] == "refused"
        assert second["code"] == "task_already_vetoed"

    def test_nothing_is_written_by_a_refusal(self, control):
        tasks = [flight_task("A")]
        job = _job(tasks, state=RunState.COMPLETED)
        tv.veto_task_command(
            job, task_id=tasks[0].task_id, reason="stop", actor="a", control_root_path=control)
        assert not (control / "jobs").exists()
        assert _read_events(job.job_id) == []

    def test_a_successful_veto_answers_the_unreachable_set(self, control):
        tasks = [flight_task("A"), flight_task("B", "A")]
        job = _job(tasks)
        result = tv.veto_task_command(
            job, task_id=tasks[0].task_id, reason="stop everything", actor="alice",
            control_root_path=control)
        assert result["outcome"] == "vetoed"
        assert result["reason"] == "stop everything"
        assert result["actor"] == "alice"
        assert result["status_at_veto"] == pj.TASK_PENDING
        assert result["unreachable"] == [tasks[1].task_id]

    def test_the_jobs_job_json_is_byte_identical_after_a_successful_veto(self, control,
                                                                         tmp_path):
        tasks = [flight_task("A"), flight_task("B", "A")]
        job = _job(tasks)
        jobs_root = tmp_path / "jobs_root"
        job_json_path = pj.save_job_plan(job, root=jobs_root)
        before = job_json_path.read_bytes()

        tv.veto_task_command(
            job, task_id=tasks[0].task_id, reason="stop everything", actor="alice",
            control_root_path=control)

        assert job_json_path.read_bytes() == before

    def test_unreachable_excludes_a_task_another_entry_already_vetoes(self, control):
        # B depends on A. B is vetoed first (on its own); A is vetoed second — its own
        # downstream is B, but B already carries its own veto entry and must not be
        # reported a second time as merely "unreachable".
        tasks = [flight_task("A"), flight_task("B", "A")]
        job = _job(tasks)
        a_id, b_id = dag_ids(tasks, "A", "B")

        first = tv.veto_task_command(
            job, task_id=b_id, reason="stop B", actor="a", control_root_path=control)
        assert first["outcome"] == "vetoed"
        assert first["unreachable"] == []

        second = tv.veto_task_command(
            job, task_id=a_id, reason="stop A too", actor="a", control_root_path=control)
        assert second["outcome"] == "vetoed"
        assert second["unreachable"] == []


# ---------------------------------------------------------------------------
# S8 — the event
# ---------------------------------------------------------------------------


class TestTaskVetoedEvent:
    def test_one_event_carries_the_reason_verbatim(self, control):
        tasks = [flight_task("A")]
        job = _job(tasks)
        result = tv.veto_task_command(
            job, task_id=tasks[0].task_id, reason="rollback needed", actor="alice",
            control_root_path=control)
        assert result["outcome"] == "vetoed"

        events = [e for e in _read_events(job.job_id) if e["event"] == "task_vetoed"]
        assert len(events) == 1
        meta = events[0]["metadata"]
        assert meta["reason"] == "rollback needed"
        assert meta["request_id"] == result["request_id"]
        assert events[0]["task_id"] == tasks[0].task_id

    def test_repair_never_writes_a_second_event_for_an_entry_already_covered(self, control):
        """Direct coverage of ``_maybe_repair_task_vetoed_event``'s own idempotency: the
        ledger read must gate the write, not merely happen to run once in practice."""
        tasks = [flight_task("A")]
        job = _job(tasks)
        veto, _ = tv.record_task_veto(
            JOB, tasks[0].task_id, "x", "a", pj.TASK_PENDING, control_root_path=control)
        tv._maybe_repair_task_vetoed_event(job, veto, [])
        tv._maybe_repair_task_vetoed_event(job, veto, [])
        events = [e for e in _read_events(job.job_id) if e["event"] == "task_vetoed"]
        assert len(events) == 1

    def test_no_second_event_on_a_repeated_veto(self, control):
        tasks = [flight_task("A")]
        job = _job(tasks)
        tv.veto_task_command(
            job, task_id=tasks[0].task_id, reason="x", actor="a", control_root_path=control)
        second = tv.veto_task_command(
            job, task_id=tasks[0].task_id, reason="y", actor="b", control_root_path=control)
        assert second["outcome"] == "refused"
        events = [e for e in _read_events(job.job_id) if e["event"] == "task_vetoed"]
        assert len(events) == 1

    def test_a_retry_repairs_a_missing_event_after_a_failed_write(self, control, monkeypatch):
        """The loser of a create-only race repairs the winner's event when the winner's own
        write of it failed — a retry after a failed event write repairs the audit line
        exactly once."""
        tasks = [flight_task("A")]
        job = _job(tasks)
        real_write = tv._fs.write_file_atomically

        def _boom_event(*_a, **_kw):
            raise OSError("simulated ledger failure")

        def _slip_in_first(dir_fd, name, data, **kw):
            if "ran" not in winner:
                winner["ran"] = True
                monkeypatch.undo()
                monkeypatch.setattr(tv, "_write_task_vetoed_event", _boom_event)
                with pytest.raises(OSError):
                    tv.veto_task_command(
                        job, task_id=tasks[0].task_id, reason="winner reason", actor="winner",
                        control_root_path=control)
                monkeypatch.undo()
            return real_write(dir_fd, name, data, **kw)

        winner: dict[str, object] = {}
        monkeypatch.setattr(
            "packages.orchestration.task_veto._fs.write_file_atomically", _slip_in_first)

        result = tv.veto_task_command(
            job, task_id=tasks[0].task_id, reason="loser reason", actor="loser",
            control_root_path=control)
        assert result["outcome"] == "task_already_vetoed"

        events = [e for e in _read_events(job.job_id) if e["event"] == "task_vetoed"]
        assert len(events) == 1
        assert events[0]["metadata"]["reason"] == "winner reason"
