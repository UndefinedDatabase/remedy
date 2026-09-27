"""F030 T001 — a steering message addressed to one task.

Address a steering message to one task (`task_id` on `record_steering_message`), drain it only
in that task's own round (`consume_pending_steering`), carry it in that task's builder prompt
as its own segment (`builder_operator_notes`, DECISION F030 D1), and list it in the job report
when the task finished without taking it in. Scripted providers only (the `FakeProvider`
pattern of `test_steering_consumption.py`); `REMEDY_DATA_DIR` is set under `tmp_path` in every
test that touches the run loop or the job report, since both read the default data root.
"""
from __future__ import annotations

import pytest

from packages.orchestration import pingpong_job as PJ
from packages.orchestration import steering as ST
from packages.orchestration.mission_contract import read_mission_contract
from packages.orchestration.mission_state import (
    MISSION_ROLE_INITIAL,
    create_mission,
    link_job_to_mission,
    load_mission,
)
from packages.orchestration.pingpong_loop import compose_builder_prompt, run_pingpong
from packages.orchestration.pingpong_provider import FakeProvider
from packages.orchestration.prompt_segments import SegmentStabilityRank
from packages.orchestration.timeline import load_run_events

JOB = "f0300f0300f0300f"
TASK = "T1"
OTHER_TASK = "T2"
NOTE = "Resize the widget before you commit."


@pytest.fixture
def root(tmp_path):
    return tmp_path / "remedy_data"


def _repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "README.md").write_text("# Demo\n")
    (repo / "docs" / "README.md").write_text("# Docs\n")
    return repo


def _received_events(root, job_id=JOB):
    return [e for e in load_run_events(root, job_id)
            if e.get("event") == "steering_message_received"]


def _consumed_events(root, job_id=JOB):
    return [e for e in load_run_events(root, job_id)
            if e.get("event") == "steering_message_consumed"]


# --- S1: the address --------------------------------------------------------------------------

class TestTheAddress:
    def test_a_note_carries_its_task_id_and_verifies(self, root):
        record = ST.record_steering_message(
            JOB, "Use pnpm.", job_state="running", channel="cli", task_id=TASK, root=root)
        path = ST.steering_dir(JOB, root) / f"{record['message_id']}.json"
        assert record["task_id"] == TASK
        assert ST.verify_steering_record(path) == []
        [event] = _received_events(root)
        # The run log writer lifts a `task_id` keyword to the event's own top-level field
        # (`run_log.RunLogWriter.log`'s named parameter), exactly as it already does for the
        # consumption event's `task_id` (`steering_acknowledgements`'s "read both places").
        assert event["task_id"] == TASK

    def test_a_job_wide_records_key_set_is_exactly_f264s(self, root):
        record = ST.record_steering_message(
            JOB, "Use pnpm.", job_state="running", channel="cli", root=root)
        assert set(record) == {
            "schema", "message_id", "job_id", "text", "channel", "received_at", "record_sha256"}
        [event] = _received_events(root)
        assert "task_id" not in event["metadata"]

    def test_a_non_string_task_id_refuses_with_nothing_written(self, root):
        with pytest.raises(ST.SteeringError, match="task id must be text"):
            ST.record_steering_message(
                JOB, "Use pnpm.", job_state="running", channel="cli", task_id=3, root=root)
        assert not ST.steering_dir(JOB, root).exists()
        assert _received_events(root) == []


# --- S2: the drain ------------------------------------------------------------------------------

class TestTheDrain:
    def test_a_note_to_another_task_waits_and_is_consumed_at_its_own_round(self, root):
        ST.record_steering_message(
            JOB, "for T2", job_state="running", channel="cli", task_id=OTHER_TASK, root=root)

        result = ST.consume_pending_steering(JOB, task_id=TASK, round_number=1, root=root)
        assert result == []
        assert ST.list_steering_consumptions(JOB, root) == {}
        assert _consumed_events(root) == []

        result2 = ST.consume_pending_steering(JOB, task_id=OTHER_TASK, round_number=2, root=root)
        assert result2 == []  # a note is never in the return value
        marker = ST.list_steering_consumptions(JOB, root)["sm-0001"]
        assert (marker["task_id"], marker["round_number"]) == (OTHER_TASK, 2)
        assert len(_consumed_events(root)) == 1

    def test_the_return_value_holds_a_job_wide_message_and_never_a_note(self, root):
        ST.record_steering_message(JOB, "job wide", job_state="running", channel="cli", root=root)
        ST.record_steering_message(
            JOB, "for T1 only", job_state="running", channel="cli", task_id=TASK, root=root)

        result = ST.consume_pending_steering(JOB, task_id=TASK, round_number=1, root=root)
        assert [r["text"] for r in result] == ["job wide"]


# --- S3: the notes --------------------------------------------------------------------------

class TestTheNotes:
    def test_three_notes_render_numbered_and_a_second_consume_publishes_nothing_new(self, root):
        ST.record_steering_message(
            JOB, "one", job_state="running", channel="cli", task_id=TASK, root=root)
        ST.record_steering_message(
            JOB, "two", job_state="running", channel="cli", task_id=TASK, root=root)
        ST.record_steering_message(
            JOB, "three\nfour", job_state="running", channel="cli", task_id=TASK, root=root)

        ST.consume_pending_steering(JOB, task_id=TASK, round_number=2, root=root)
        assert len(_consumed_events(root)) == 3

        notes = ST.consumed_task_notes(JOB, TASK, root)
        text = ST.render_operator_notes_segment(notes)
        assert text == (
            "OPERATOR NOTES (binding):\n"
            "1. one\n"
            "2. two\n"
            "3. three\n   four\n"
        )

        ST.consume_pending_steering(JOB, task_id=TASK, round_number=3, root=root)
        assert len(_consumed_events(root)) == 3  # nothing new published


class TestTheMission:
    def test_a_note_leaves_the_mission_contract_unamended(self, root):
        made = create_mission("p-f030", "Ship the tool", root=root)
        link_job_to_mission("p-f030", made.id, JOB, MISSION_ROLE_INITIAL, root=root)
        ST.record_steering_message(
            JOB, "Use pnpm, never npm.", job_state="running", channel="cli",
            task_id=TASK, root=root)

        ST.consume_pending_steering(JOB, task_id=TASK, round_number=2, root=root)

        marker = ST.list_steering_consumptions(JOB, root)["sm-0001"]
        assert (marker["mission_id"], marker["amendment_id"]) == ("", "")
        # `create_mission` writes no contract of its own; a job-wide message would have
        # compiled one via `_amend_mission` (`test_steering_mission.py`'s own fixture proves
        # that). A task-addressed note never looks the mission up at all (S2), so the mission
        # is left exactly as `create_mission` left it: no contract on disk yet.
        assert read_mission_contract(load_mission("p-f030", made.id, root)) is None


# --- S4: the segment ----------------------------------------------------------------------------

class TestTheSegment:
    def test_the_manifest_order_and_rank_with_both_texts(self):
        composed = compose_builder_prompt(
            "goal", "ctx", steering_text="STEER\n", operator_notes_text="NOTES\n")
        names = [row.name for row in composed.manifest]
        assert names[-3:] == ["builder_steering", "builder_operator_notes", "builder_directive"]
        [row] = [r for r in composed.manifest if r.name == "builder_operator_notes"]
        assert row.rank == SegmentStabilityRank.STEERING

    def test_no_operator_notes_row_without_operator_notes_text(self):
        composed = compose_builder_prompt("goal", "ctx", steering_text="STEER\n")
        assert "builder_operator_notes" not in [row.name for row in composed.manifest]
        composed_plain = compose_builder_prompt("goal", "ctx")
        assert "builder_operator_notes" not in [row.name for row in composed_plain.manifest]


class _NoteRecording(FakeProvider):
    """Records every builder prompt; on the FIRST call (round 1, in flight, when
    ``send_mid_call``) sends a note addressed to ``task_id``. Mirrors ``_Recording`` of
    ``test_steering_consumption.py``, restated here for the reason that suite's own neighbours
    give for restating a recipe rather than importing it across test files."""

    def __init__(self, *, send_mid_call: bool, task_id: str, pass_on_round: int = 2):
        super().__init__(pass_on_round=pass_on_round)
        self.builder_prompts: list[str] = []
        self.send_mid_call = send_mid_call
        self._task_id = task_id

    def build(self, prompt, **kw):
        self.builder_prompts.append(prompt)
        if self.send_mid_call and len(self.builder_prompts) == 1:
            ST.record_steering_message(
                JOB, NOTE, job_state="running", channel="cli", task_id=self._task_id)
        return super().build(prompt, **kw)


class TestTheCallBoundary:
    def test_round_one_is_untouched_and_round_two_differs_by_exactly_the_segment(
        self, tmp_path, monkeypatch,
    ):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "a" / "data"))
        without = _NoteRecording(send_mid_call=False, task_id=TASK)
        run_pingpong("Fix README", str(_repo(tmp_path / "a")), builder_provider=without,
                     reviewer_provider=without, max_rounds=3, repair_rounds=2,
                     job_id=JOB, task_id=TASK)

        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "b" / "data"))
        with_note = _NoteRecording(send_mid_call=True, task_id=TASK)
        result = run_pingpong("Fix README", str(_repo(tmp_path / "b")), builder_provider=with_note,
                              reviewer_provider=with_note, max_rounds=3, repair_rounds=2,
                              job_id=JOB, task_id=TASK)

        assert len(without.builder_prompts) == len(with_note.builder_prompts) == 2
        assert with_note.builder_prompts[0] == without.builder_prompts[0]
        assert NOTE not in with_note.builder_prompts[0]

        segment = ST.render_operator_notes_segment([{"text": NOTE}])
        assert NOTE not in without.builder_prompts[1]
        assert f"1. {NOTE}\n" in with_note.builder_prompts[1]
        assert with_note.builder_prompts[1].count(segment + "\n") == 1
        assert with_note.builder_prompts[1].replace(segment + "\n", "", 1) == without.builder_prompts[1]

        builder_entries = sorted(
            (e for e in result.prompt_traces if e.role == "builder"), key=lambda e: e.round)
        assert len(builder_entries) == 2
        round1_names = [row["name"] for row in builder_entries[0].segment_manifest]
        round2_rows = builder_entries[1].segment_manifest
        assert "builder_operator_notes" not in round1_names
        [row2] = [r for r in round2_rows if r["name"] == "builder_operator_notes"]
        assert row2["rank"] == int(SegmentStabilityRank.STEERING)

    def test_a_note_addressed_to_another_task_never_appears_in_any_prompt(
        self, tmp_path, monkeypatch,
    ):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        ST.record_steering_message(
            JOB, NOTE, job_state="running", channel="cli", task_id=OTHER_TASK)
        prov = _NoteRecording(send_mid_call=False, task_id=OTHER_TASK)
        run_pingpong("Fix README", str(_repo(tmp_path)), builder_provider=prov,
                     reviewer_provider=prov, max_rounds=3, repair_rounds=2,
                     job_id=JOB, task_id=TASK)
        assert prov.builder_prompts
        assert all(NOTE not in p for p in prov.builder_prompts)

    def test_a_note_consumed_at_round_two_is_still_in_round_threes_prompt(
        self, tmp_path, monkeypatch,
    ):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        prov = _NoteRecording(send_mid_call=True, task_id=TASK, pass_on_round=3)
        run_pingpong("Fix README", str(_repo(tmp_path)), builder_provider=prov,
                     reviewer_provider=prov, max_rounds=3, repair_rounds=2,
                     job_id=JOB, task_id=TASK)
        assert len(prov.builder_prompts) == 3
        assert NOTE not in prov.builder_prompts[0]
        assert f"1. {NOTE}\n" in prov.builder_prompts[1]
        assert f"1. {NOTE}\n" in prov.builder_prompts[2]


# --- S5: the report ------------------------------------------------------------------------------

def _job(status_map: dict[str, str]) -> PJ.JobPlan:
    tasks = [PJ.TaskEntry(task_id=tid, title=tid, status=status)
             for tid, status in status_map.items()]
    return PJ.JobPlan(job_id=JOB, tasks=tasks)


class TestTheReport:
    def test_a_passed_tasks_unconsumed_note_is_in_the_report(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        record = ST.record_steering_message(
            JOB, "ship it", job_state="running", channel="cli", task_id=TASK)
        job = _job({TASK: PJ.TASK_PASSED})

        report = PJ.export_job_report(job)
        [t1] = report["tasks"]
        assert t1["steering_not_consumed"] == [{
            "message_id": record["message_id"], "text": "ship it",
            "received_at": record["received_at"],
        }]

        text = PJ.format_job_report_text(job)
        assert "Steering not consumed: “ship it”" in text

    def test_a_pending_tasks_note_and_a_consumed_note_give_no_key(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        ST.record_steering_message(
            JOB, "for pending T1", job_state="running", channel="cli", task_id=TASK)
        ST.record_steering_message(
            JOB, "for consumed T2", job_state="running", channel="cli", task_id=OTHER_TASK)
        ST.consume_pending_steering(JOB, task_id=OTHER_TASK, round_number=1)

        job = _job({TASK: PJ.TASK_PENDING, OTHER_TASK: PJ.TASK_PASSED})
        report = PJ.export_job_report(job)
        assert all("steering_not_consumed" not in t for t in report["tasks"])

        text = PJ.format_job_report_text(job)
        assert "Steering not consumed" not in text

    def test_a_job_with_no_note_exports_the_same_keys_as_before(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job = _job({TASK: PJ.TASK_PASSED})
        report = PJ.export_job_report(job)
        [t1] = report["tasks"]
        assert "steering_not_consumed" not in t1
        assert "veto" not in t1
