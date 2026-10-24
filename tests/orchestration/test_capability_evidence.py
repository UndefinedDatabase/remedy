"""Tests for packages.orchestration.capability_evidence — F157 T003 (DECISION F157 D5 (2)): the
run's and a job task's capability degradations read back, and the report line both surfaces print.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.contracts.capability_matrix import CAPABILITY_DEGRADATIONS_FIELD
from packages.orchestration import data_paths
from packages.orchestration.capability_evidence import (
    capability_report_line,
    run_capability_degradations,
    task_capability_degradations,
)
from packages.orchestration.capability_routes import CAPABILITY_DECISIONS_FILENAME
from packages.orchestration.job_report import format_job_report_text
from packages.orchestration.job_report_task_lines import task_report_detail_lines
from packages.orchestration.pingpong_job import JobPlan, TaskEntry, save_job_plan


@pytest.fixture(autouse=True)
def isolate_data_root(tmp_path: Path, monkeypatch) -> Path:
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


_DEGRADED_LINE = json.dumps({
    "role": "builder", "provider": "claude-cli", "model": "m",
    "decisions": [
        {"feature_key": "stream_evidence_capture", "mode": "degraded",
         "strategy": "buffered_output", "missing": ["streaming"]},
    ],
})
_OTHER_DEGRADED_LINE = json.dumps({
    "role": "reviewer", "provider": "claude-cli", "model": "m",
    "decisions": [
        {"feature_key": "reviewer_schema_gate", "mode": "degraded",
         "strategy": "schema_in_prompt", "missing": ["json_schema"]},
    ],
})
_DEGRADED_ENTRY = {"feature_key": "stream_evidence_capture", "mode": "degraded",
                   "strategy": "buffered_output", "missing": ["streaming"]}
_OTHER_DEGRADED_ENTRY = {"feature_key": "reviewer_schema_gate", "mode": "degraded",
                         "strategy": "schema_in_prompt", "missing": ["json_schema"]}


def _write_decisions(directory: Path, *lines: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / CAPABILITY_DECISIONS_FILENAME).write_text("\n".join(lines) + "\n", encoding="utf-8")


class TestTaskCapabilityDegradations:
    def test_a_line_in_the_runs_own_directory_only(self):
        _write_decisions(data_paths.run_dir("run-1"), _DEGRADED_LINE)
        assert task_capability_degradations("job-1", "T001", "run-1") == [_DEGRADED_ENTRY]

    def test_a_line_in_the_tasks_directory_only(self):
        _write_decisions(data_paths.job_evidence_dir("job-1") / "task_runs" / "T001", _DEGRADED_LINE)
        assert task_capability_degradations("job-1", "T001", "run-1") == [_DEGRADED_ENTRY]

    def test_a_line_in_each_directory_gives_both(self):
        _write_decisions(data_paths.run_dir("run-1"), _DEGRADED_LINE)
        _write_decisions(
            data_paths.job_evidence_dir("job-1") / "task_runs" / "T001", _OTHER_DEGRADED_LINE,
        )
        assert task_capability_degradations("job-1", "T001", "run-1") == [
            _DEGRADED_ENTRY, _OTHER_DEGRADED_ENTRY,
        ]

    def test_neither_directory_answers_empty(self):
        assert task_capability_degradations("job-1", "T001", "run-1") == []

    def test_an_empty_run_id_reads_only_the_tasks_directory(self):
        _write_decisions(data_paths.job_evidence_dir("job-1") / "task_runs" / "T001", _DEGRADED_LINE)
        assert task_capability_degradations("job-1", "T001", "") == [_DEGRADED_ENTRY]


class TestRunCapabilityDegradations:
    def test_the_runs_own_directory_alone_with_no_job_id(self):
        _write_decisions(data_paths.run_dir("run-1"), _DEGRADED_LINE)
        assert run_capability_degradations("run-1", {"job_id": ""}) == [_DEGRADED_ENTRY]

    def test_the_plan_lookup_reaches_the_tasks_directory(self):
        job = JobPlan(job_title="t", tasks=[TaskEntry(title="only")])
        job.tasks[0].run_id = "run-1"
        save_job_plan(job)
        _write_decisions(
            data_paths.job_evidence_dir(job.job_id) / "task_runs" / job.tasks[0].task_id,
            _OTHER_DEGRADED_LINE,
        )
        assert run_capability_degradations("run-1", {"job_id": job.job_id}) == [_OTHER_DEGRADED_ENTRY]

    def test_a_plan_that_cannot_be_read_leaves_the_runs_own_directory_alone(self):
        _write_decisions(data_paths.run_dir("run-1"), _DEGRADED_LINE)
        bad_job_id = "job-unreadable"
        record_path = data_paths.job_record_path(bad_job_id)
        record_path.parent.mkdir(parents=True, exist_ok=True)
        record_path.write_text("not json", encoding="utf-8")
        assert run_capability_degradations("run-1", {"job_id": bad_job_id}) == [_DEGRADED_ENTRY]

    def test_no_task_matching_the_run_id_leaves_the_runs_own_directory_alone(self):
        job = JobPlan(job_title="t", tasks=[TaskEntry(title="only")])
        job.tasks[0].run_id = "some-other-run"
        save_job_plan(job)
        _write_decisions(data_paths.run_dir("run-1"), _DEGRADED_LINE)
        assert run_capability_degradations("run-1", {"job_id": job.job_id}) == [_DEGRADED_ENTRY]


class TestCapabilityReportLine:
    def test_missing_key_is_none(self):
        assert capability_report_line({}) is None

    def test_empty_list_is_none(self):
        assert capability_report_line({CAPABILITY_DEGRADATIONS_FIELD: []}) is None

    def test_a_degraded_entry_gives_the_wording(self):
        assert capability_report_line({CAPABILITY_DEGRADATIONS_FIELD: [_DEGRADED_ENTRY]}) == (
            "Degradations: stream_evidence_capture as buffered_output"
        )


class TestJobReportPrintsATasksDegradations:
    def test_a_tasks_directory_degradation_prints_under_the_task(self):
        job = JobPlan(job_title="t", tasks=[TaskEntry(title="only")])
        job.tasks[0].run_id = "run-1"
        _write_decisions(
            data_paths.job_evidence_dir(job.job_id) / "task_runs" / job.tasks[0].task_id,
            _DEGRADED_LINE,
        )
        text = format_job_report_text(job)
        assert "      Degradations: stream_evidence_capture as buffered_output" in text

    def test_a_job_with_no_degradation_prints_no_such_line(self):
        job = JobPlan(job_title="t", tasks=[TaskEntry(title="only")])
        job.tasks[0].run_id = "run-1"
        text = format_job_report_text(job)
        assert "Degradations:" not in text

    def test_task_report_detail_lines_still_carries_the_steering_lines(self):
        job = JobPlan(job_title="t", tasks=[TaskEntry(title="only")])
        task = job.tasks[0]
        steering_map = {task.task_id: [{"text": "please wait", "message_id": "m1", "received_at": ""}]}
        lines = task_report_detail_lines(job, task, steering_map)
        assert any("Steering not consumed" in line for line in lines)
