"""The worker cap, the CPU priority and the one-line run record (amend0930-test-load).

``tests/load_governor.py`` holds the logic and ``tests/conftest.py`` wires it into every pytest run of
this repository. The child runs below use one small existing test file, so the wiring itself is
under test and not only the helper.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from tests import load_governor

REPO_ROOT = Path(__file__).resolve().parents[2]
SMALL_TEST_FILE = "tests/regression/test_data_root_guard.py"


def _child_run(extra_args, env_overrides):
    env = {k: v for k, v in os.environ.items() if not k.startswith("REMEDY_TEST_")}
    env.update(env_overrides)
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *extra_args, SMALL_TEST_FILE],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=300)


class TestWorkerCap:
    def test_auto_is_six_on_a_24_cpu_machine_with_no_variable_set(self):
        assert load_governor.auto_worker_count(cpus=24, environ={}) == 6

    def test_auto_follows_the_variable(self):
        assert load_governor.auto_worker_count(cpus=24, environ={"REMEDY_TEST_MAX_WORKERS": "3"}) == 3

    def test_zero_means_no_cap(self):
        assert load_governor.auto_worker_count(cpus=24, environ={"REMEDY_TEST_MAX_WORKERS": "0"}) == 24

    def test_a_machine_with_fewer_cpus_than_the_cap_gets_its_cpu_count(self):
        assert load_governor.auto_worker_count(cpus=4, environ={}) == 4

    def test_a_value_that_is_not_a_number_falls_back_to_six(self):
        assert load_governor.worker_cap({"REMEDY_TEST_MAX_WORKERS": "many"}) == 6

    def test_an_explicit_number_above_the_cap_is_reduced(self):
        assert load_governor.clamped_worker_count(24, environ={}) == 6
        assert load_governor.clamped_worker_count(2, environ={}) == 2
        assert load_governor.clamped_worker_count("auto", environ={}) == "auto"
        assert load_governor.clamped_worker_count(24, environ={"REMEDY_TEST_MAX_WORKERS": "0"}) == 24

    def test_a_real_run_asking_for_five_workers_under_a_cap_of_three_says_so(self):
        done = _child_run(["-n", "5"], {"REMEDY_TEST_MAX_WORKERS": "3", "REMEDY_TEST_LOAD_LOG": ""})
        assert done.returncode == 0, done.stdout + done.stderr
        assert "remedy tests: -n 5 is above the worker cap, running 3 workers" in done.stdout

    def test_a_real_run_asking_for_auto_gets_the_cap(self, tmp_path):
        log = tmp_path / "load.jsonl"
        done = _child_run(["-n", "auto"], {"REMEDY_TEST_MAX_WORKERS": "2", "REMEDY_TEST_LOAD_LOG": str(log)})
        assert done.returncode == 0, done.stdout + done.stderr
        assert json.loads(log.read_text(encoding="utf-8"))["workers"] == min(2, os.cpu_count() or 1)

    def test_a_real_run_within_the_cap_prints_no_reduction_line(self):
        done = _child_run(["-n", "2"], {"REMEDY_TEST_MAX_WORKERS": "3", "REMEDY_TEST_LOAD_LOG": ""})
        assert done.returncode == 0, done.stdout + done.stderr
        assert "worker cap" not in done.stdout


class TestPriority:
    def test_it_never_raises_priority(self, monkeypatch):
        calls = []
        monkeypatch.setattr(os, "nice", lambda inc: calls.append(inc) or 15)
        assert load_governor.lower_priority({}) == 15
        assert calls == [0]

    def test_it_lowers_to_the_wanted_niceness(self, monkeypatch):
        state = {"nice": 2}

        def fake_nice(increment):
            state["nice"] += increment
            return state["nice"]

        monkeypatch.setattr(os, "nice", fake_nice)
        assert load_governor.lower_priority({}) == 10
        assert load_governor.lower_priority({"REMEDY_TEST_NICE": "0"}) == 10
        assert state["nice"] == 10

    def test_zero_leaves_the_priority_alone(self, monkeypatch):
        calls = []
        monkeypatch.setattr(os, "nice", lambda inc: calls.append(inc) or 0)
        assert load_governor.lower_priority({"REMEDY_TEST_NICE": "0"}) == 0
        assert calls == [0]

    def test_an_oserror_is_ignored(self, monkeypatch):
        def refuse(increment):
            raise OSError("not permitted")

        monkeypatch.setattr(os, "nice", refuse)
        assert load_governor.lower_priority({}) is None


class TestRunRecord:
    def test_a_child_run_leaves_exactly_one_well_formed_line(self, tmp_path):
        log = tmp_path / "load.jsonl"
        done = _child_run(["-n", "2"], {"REMEDY_TEST_LOAD_LOG": str(log)})
        assert done.returncode == 0, done.stdout + done.stderr
        lines = log.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        record = json.loads(lines[0])
        assert set(record) == {"utc", "command", "collected", "exit_status", "wall_seconds",
                               "cpu_seconds", "workers"}
        assert record["collected"] > 0
        assert record["exit_status"] == 0
        assert record["workers"] == 2
        assert record["cpu_seconds"] > 0
        assert record["wall_seconds"] > 0
        assert len(record["command"]) <= load_governor.LOAD_LOG_COMMAND_CHARS

    def test_an_empty_variable_writes_nothing(self):
        default_file = load_governor.load_log_path({})
        before = default_file.stat().st_size if default_file and default_file.exists() else None
        done = _child_run([], {"REMEDY_TEST_LOAD_LOG": ""})
        assert done.returncode == 0, done.stdout + done.stderr
        after = default_file.stat().st_size if default_file and default_file.exists() else None
        assert after == before

    def test_an_unwritable_path_does_not_change_the_exit_code(self, tmp_path):
        blocker = tmp_path / "a-file"
        blocker.write_text("x", encoding="utf-8")
        done = _child_run([], {"REMEDY_TEST_LOAD_LOG": str(blocker / "load.jsonl")})
        assert done.returncode == 0, done.stdout + done.stderr

    def test_this_run_blanks_the_variable_so_a_nested_run_records_nothing(self):
        assert os.environ.get("REMEDY_TEST_LOAD_LOG") == ""

    def test_an_unset_variable_uses_the_loop_folder_only_when_it_exists(self, tmp_path):
        assert load_governor.load_log_path({}, home=tmp_path) is None
        (tmp_path / ".remedy-loop").mkdir()
        assert load_governor.load_log_path({}, home=tmp_path) == tmp_path / ".remedy-loop" / "test_load.jsonl"
        assert load_governor.load_log_path({"REMEDY_TEST_LOAD_LOG": ""}, home=tmp_path) is None

    def test_a_file_above_the_limit_is_cut_to_its_newer_half(self, tmp_path):
        log = tmp_path / "load.jsonl"
        old = [json.dumps({"n": n}) for n in range(100)]
        log.write_text("\n".join(old) + "\n", encoding="utf-8")
        assert load_governor.append_record(log, {"n": 100}, limit=100)
        kept = [json.loads(line)["n"] for line in log.read_text(encoding="utf-8").splitlines()]
        assert kept[-1] == 100
        assert 0 < len(kept) < 101
        assert kept[0] >= 40
        assert kept == sorted(kept)

    def test_a_file_under_the_limit_is_only_appended_to(self, tmp_path):
        log = tmp_path / "load.jsonl"
        assert load_governor.append_record(log, {"n": 1})
        assert load_governor.append_record(log, {"n": 2})
        assert len(log.read_text(encoding="utf-8").splitlines()) == 2
