"""Operator amendment amend1027-green-builds, Part B: the builder's own test runs count.

Synthetic claude-cli streams only; no provider runs. Each stream has the shape the CLI writes in
`--output-format stream-json`: an assistant message with a `tool_use` Bash part, then a user
message with its `tool_result`, and a final `result` line.
"""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from packages.orchestration import order_verification as OV
from packages.orchestration.builder_test_runs import (
    BUILDER_BASH_CALLS_FILENAME,
    NO_TEST_COMMAND_SUMMARY,
    bash_calls_of_stream,
    is_test_command,
    load_builder_test_runs,
    read_test_result,
    round_test_reading,
)
from packages.orchestration.pingpong_job import JobPlan, TaskEntry

VITEST_GREEN = """ RUN  v5.0.2 /w
 ✓ tests/unit/quiet-shared-605.test.tsx (5 tests) 41ms
 Test Files  1 passed (1)
      Tests  5 passed (5)
"""
VITEST_RED = """ FAIL  tests/unit/a.test.ts > adds
AssertionError: expected 2 to be 3
 Test Files  1 failed (1)
      Tests  1 failed | 4 passed (5)
"""
PLAYWRIGHT_GREEN = "Running 3 tests using 1 worker\n  3 passed (4.1s)\n"
PYTEST_GREEN = "........\n8 passed in 0.12s\n"
PYTEST_RED = "F.\nFAILED tests/test_a.py::test_x - assert 1 == 2\n1 failed, 1 passed in 0.10s\n"
CARGO_GREEN = "running 3 tests\ntest result: ok. 3 passed; 0 failed; 0 ignored\n"


@pytest.fixture()
def data_root(tmp_path, monkeypatch):
    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    return tmp_path / "data"


def _stream(path: Path, calls: list[tuple[str, str, bool]], denied: tuple[str, ...] = ()) -> Path:
    """Write a raw stream of Bash calls (command, result, is_error) and the final result line."""
    lines = []
    for n, (command, result, is_error) in enumerate(calls):
        lines.append({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": f"t{n}", "name": "Bash", "input": {"command": command}}]}})
        lines.append({"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": f"t{n}", "content": result, "is_error": is_error}]}})
    lines.append({"type": "result", "subtype": "success", "permission_denials": [
        {"tool_name": "Bash", "tool_input": {"command": command}} for command in denied]})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(line) for line in lines) + "\n")
    return path


def _node_project(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "package.json").write_text(json.dumps({"scripts": {"test": "vitest run", "e2e": "playwright test"}}))
    return root


class TestReadingAResult:
    @pytest.mark.parametrize(("text", "is_error", "expected"), [
        (VITEST_GREEN, False, (True, "5 passed, 0 failed")),
        (VITEST_RED, True, (False, "4 passed, 1 failed")),
        ("ok  \texample.com/a\t0.01s\nFAIL\texample.com/b\t0.02s\n", True, (False, "1 passed, 1 failed")),
        (PLAYWRIGHT_GREEN, False, (True, "3 passed, 0 failed")),
        (PYTEST_GREEN, False, (True, "8 passed, 0 failed")),
        (PYTEST_RED, True, (False, "1 passed, 1 failed")),
        (CARGO_GREEN, False, (True, "3 passed, 0 failed")),
        ("no summary at all", False, (None, "0 passed, 0 failed")),
        ("sh: 1: vitest: not found", True, (None, "0 passed, 0 failed")),
    ])
    def test_the_runners_own_summary_decides(self, text, is_error, expected):
        assert read_test_result(text, is_error) == expected

    @pytest.mark.parametrize(("command", "expected"), [
        ("pnpm vitest run tests/unit/a.test.ts", True), ("npm test", True),
        ("pnpm vitest run 2>&1 | tail -20", True), ("pnpm e2e -g net", True),
        ("pnpm build", False), ("cat package.json", False), ("echo npm test", False),
    ])
    def test_a_test_command_is_recognised_by_its_beginning(self, command, expected, tmp_path):
        from packages.orchestration.claude_cli_command import builder_test_commands

        assert is_test_command(command, builder_test_commands(str(_node_project(tmp_path / "p")))) is expected


class TestTheStream:
    def test_every_bash_call_comes_with_its_result(self, tmp_path):
        raw = _stream(tmp_path / "raw_stream.jsonl", [("ls", "a\nb", False), ("npm test", VITEST_GREEN, False)])
        calls = bash_calls_of_stream(raw)
        assert [c["command"] for c in calls] == ["ls", "npm test"]
        assert calls[1]["is_error"] is False and "5 passed" in calls[1]["result_tail"]

    def test_an_unreadable_stream_has_no_calls(self, tmp_path):
        assert bash_calls_of_stream(tmp_path / "missing.jsonl") == []


class TestARoundsReading:
    def _run(self, tmp_path, calls, denied=(), project=True, round_num=1):
        workspace = _node_project(tmp_path / "ws") if project else (tmp_path / "ws")
        workspace.mkdir(exist_ok=True)
        run_dir = tmp_path / "run"
        _stream(run_dir / "streams" / "builder" / f"round-{round_num:02d}" / "attempt-01" / "raw_stream.jsonl",
                calls, denied)
        _stream(run_dir / "streams" / "reviewer" / f"round-{round_num:02d}" / "attempt-01" / "raw_stream.jsonl",
                [("npm test", VITEST_RED, True)])
        reading = round_test_reading(stream_dir=str(run_dir), round_num=round_num, workspace=str(workspace),
                                     job_id="j1", run_id="r1", task_id="t1")
        return reading, run_dir

    def test_the_builders_last_test_run_decides_and_is_recorded(self, tmp_path, data_root):
        reading, run_dir = self._run(tmp_path, [("npm test", VITEST_RED, True), ("pnpm vitest run", VITEST_GREEN, False)])
        assert reading == (True, "builder ran `pnpm vitest run`: 5 passed, 0 failed", False)
        assert len(json.loads((run_dir / BUILDER_BASH_CALLS_FILENAME).read_text())) == 2   # the reviewer's is no call
        assert [row["passed"] for row in load_builder_test_runs("j1")] == [False, True]

    def test_a_round_of_another_number_is_not_read(self, tmp_path, data_root):
        reading, _ = self._run(tmp_path, [("npm test", VITEST_GREEN, False)], round_num=2)
        assert reading[0] is True
        assert round_test_reading(stream_dir=str(tmp_path / "run"), round_num=1, workspace=str(tmp_path / "ws"),
                                  job_id="j1")[2] is True

    def test_a_refused_test_command_says_permission_was_denied(self, tmp_path, data_root):
        reading, _ = self._run(tmp_path, [("ls", "x", False)], denied=("npx playwright test",))
        assert reading == (None, "tests_not_run: Erlaubnis verweigert", True)
        assert load_builder_test_runs("j1")[-1]["reason_key"] == "permission_denied"

    def test_a_missing_runner_says_the_command_was_not_found(self, tmp_path, data_root):
        reading, _ = self._run(tmp_path, [("npm test", "sh: 1: vitest: not found", True)])
        assert reading == (None, "tests_not_run: Befehl nicht gefunden", True)

    def test_a_project_without_a_test_command_needs_no_test(self, tmp_path, data_root):
        reading, _ = self._run(tmp_path, [("ls", "x", False)], project=False)
        assert reading == (None, NO_TEST_COMMAND_SUMMARY, False)


class TestTheJobsVerification:
    def _job(self, passed):
        job = JobPlan(job_title="t", mission="m", tasks=[TaskEntry(title="x", test_passed=passed)])
        job.tasks[0].run_id = "r1"
        job.state = SimpleNamespace(value="completed")
        return job

    def test_a_builders_green_run_names_the_builder(self, tmp_path, data_root):
        job = self._job(True)
        TestARoundsReading()._run(tmp_path, [("npm test", VITEST_GREEN, False)])
        rows = load_builder_test_runs("j1")
        from packages.orchestration.builder_test_runs import BUILDER_TEST_RUNS_FILENAME, _append_json
        from packages.orchestration.data_paths import job_evidence_dir

        _append_json(Path(job_evidence_dir(str(job.job_id))) / BUILDER_TEST_RUNS_FILENAME, rows)
        found = OV.job_verification(job)
        assert found["status"] == "passed" and found["tested_by"] == ["builder"]
        assert found["runs"] == [{"source": "builder", "task_id": str(job.tasks[0].task_id), "status": "passed",
                                  "command": "npm test"}]

    def test_the_final_check_decides_over_a_red_builder_run_and_both_are_named(self, data_root):
        from packages.orchestration.dod_gate import result_path

        job = self._job(True)
        path = result_path(str(job.job_id))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"released": True, "checks": [
            {"check_id": "order-tests", "kind": "project_tests", "status": "passed", "blocking": True,
             "command": "npm test", "exit_code": 0, "reason": ""}]}))
        found = OV.job_verification(job)
        assert found["status"] == "passed" and found["tested_by"] == ["final_check"]
        assert [run["source"] for run in found["runs"]] == ["dod"]

    def test_a_red_final_check_carries_its_output_without_host_paths(self, data_root):
        from packages.orchestration.dod_gate import result_path

        job = self._job(None)
        job.job_workspace_path = "/home/x/repo/.remedy-wt/job-1"
        path = result_path(str(job.job_id))
        path.parent.mkdir(parents=True, exist_ok=True)
        tail = "x" * 5000 + "\nFAIL /home/x/repo/.remedy-wt/job-1/tests/a.test.ts\n"
        path.write_text(json.dumps({"released": False, "checks": [
            {"check_id": "order-tests", "kind": "project_tests", "status": "failed", "blocking": True,
             "command": "npm test", "exit_code": 1, "reason": "nonzero_exit", "output_tail": tail}]}))
        found = OV.job_verification(job)
        assert found["status"] == "failed" and len(found["output"]) == 4000
        assert found["output"].endswith("FAIL tests/a.test.ts\n") and "/home/x" not in found["output"]

    def test_a_round_nobody_tested_carries_its_reason(self, tmp_path, data_root):
        job = self._job(None)
        job.state = SimpleNamespace(value="blocked")
        job.metadata[OV.ORDER_TEST_REQUEST_KEY] = OV.PROJECT_TESTS_REQUEST
        from packages.orchestration.builder_test_runs import BUILDER_TEST_RUNS_FILENAME, _append_json
        from packages.orchestration.data_paths import job_evidence_dir

        _append_json(Path(job_evidence_dir(str(job.job_id))) / BUILDER_TEST_RUNS_FILENAME,
                     [{"run_id": "r1", "passed": None, "reason_key": "timeout"}])
        found = OV.job_verification(job)
        assert (found["status"], found["reason_key"], found["reason"]) == ("not_run", "timeout", "Zeitlimit")
