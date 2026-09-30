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


SLEEPER = [sys.executable, "-c", "import sys, time; time.sleep(120)"]
STRIPPED_ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin")}
LEAKING_TEST = '''
import subprocess, sys
from pathlib import Path


def test_it_starts_a_process_and_never_stops_it(tmp_path):
    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"], cwd=tmp_path,
                            env={{"PATH": "/usr/bin:/bin"}}, start_new_session=True)
    Path({pid_file!r}).write_text(str(proc.pid), encoding="utf-8")
'''


def _stop(proc):
    proc.kill()
    proc.wait(timeout=10)


class TestNoProcessLeftBehind:
    """F293 T003 (R-1118): a test run that leaves a process behind fails, and the process is ended."""

    def test_a_process_carrying_the_mark_is_found_and_ended(self):
        mark = load_governor.new_run_mark()
        proc = subprocess.Popen(SLEEPER, env={**os.environ, load_governor.RUN_MARK_VARIABLE: mark})
        try:
            found = load_governor.leftover_processes(mark, [])
            assert [p.pid for p in found] == [proc.pid]
            ended = load_governor.end_processes(found, grace=0.2)
            assert len(ended) == 1 and ended[0].startswith(f"pid {proc.pid}: ")
            assert proc.wait(timeout=10) is not None
        finally:
            _stop(proc)

    def test_a_process_with_a_stripped_environment_is_found_by_its_folder(self, tmp_path):
        proc = subprocess.Popen(SLEEPER, cwd=tmp_path, env=STRIPPED_ENV, start_new_session=True)
        try:
            found = load_governor.leftover_processes(load_governor.new_run_mark(), [tmp_path])
            assert [p.pid for p in found] == [proc.pid]
        finally:
            _stop(proc)

    def test_an_argument_counts_inside_the_folder_and_not_in_a_sibling_with_a_longer_name(self, tmp_path):
        run, sibling = tmp_path / "run", tmp_path / "run2"
        run.mkdir()
        sibling.mkdir()
        proc = subprocess.Popen([*SLEEPER, str(sibling / "x")], cwd="/", env=STRIPPED_ENV)
        try:
            mark = load_governor.new_run_mark()
            assert load_governor.leftover_processes(mark, [run]) == []
            assert [p.pid for p in load_governor.leftover_processes(mark, [sibling])] == [proc.pid]
        finally:
            _stop(proc)

    def test_this_process_and_its_parents_never_count(self):
        import psutil

        me = psutil.Process()
        found = {p.pid for p in load_governor.leftover_processes(
            load_governor.new_run_mark(), [Path(me.exe()).parent])}
        assert me.pid not in found
        assert not found & {parent.pid for parent in me.parents()}

    def test_a_process_that_exits_within_the_grace_is_not_reported(self):
        import psutil

        proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(0.3)"])
        try:
            assert load_governor.end_processes([psutil.Process(proc.pid)], grace=10) == []
        finally:
            _stop(proc)

    def test_a_run_that_leaves_a_process_behind_fails_and_the_process_is_ended(self, tmp_path):
        import psutil

        pid_file = tmp_path / "pid"
        test_file = tmp_path / "leak" / "test_leak.py"
        test_file.parent.mkdir()
        test_file.write_text(LEAKING_TEST.format(pid_file=str(pid_file)), encoding="utf-8")
        env = {k: v for k, v in os.environ.items() if not k.startswith("REMEDY_TEST_")}
        env["REMEDY_TEST_LOAD_LOG"] = ""
        done = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "tests.conftest",
             "-n", "0", "--basetemp", str(tmp_path / "base"), str(test_file)],
            cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=300)
        pid = int(pid_file.read_text(encoding="utf-8"))
        assert done.returncode == 1, done.stdout + done.stderr
        assert "1 passed" in done.stdout
        assert f"the run left 1 process(es) behind, now ended (F293 T003): pid {pid}: " in done.stdout
        assert not psutil.pid_exists(pid) or psutil.Process(pid).status() == psutil.STATUS_ZOMBIE


class TestOneCheckoutIdentityPerProcess:
    """DECISION F293 D6: ``tests/conftest.py`` reads Remedy's own checkout identity once per process."""

    def test_every_reading_in_a_process_is_the_one_taken_at_session_start(self):
        from packages.orchestration import run_manifest

        first = run_manifest.remedy_worktree_identity()
        assert run_manifest.remedy_worktree_identity() is first
        assert first.status in (run_manifest.GIT_OK, run_manifest.GIT_INCOMPLETE,
                                run_manifest.GIT_UNAVAILABLE)
