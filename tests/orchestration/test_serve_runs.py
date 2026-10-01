"""The runs the `remedy serve start` supervisor starts (F200, DECISIONs F200 D1 (4) and D4).

Every run here is a stand-in for `remedy job run`: a Python child that prints its
job id and its environment's two settings, waits until the test creates its
release file, and exits with the code the test chose. Each test releases every
child it started, so no run outlives the test.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from packages.orchestration import serve_runs as SR
from packages.orchestration.serve_paths import serve_paths

_CHILD = """\
import os, sys, time
from pathlib import Path
job_id, release, code = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3])
print("run", job_id, os.environ.get("REMEDY_SERVE_DIRECT"), os.environ.get("REMEDY_DATA_DIR"),
      os.getsid(0) == os.getpid())
print("to stderr", file=sys.stderr)
sys.stdout.flush()
deadline = time.monotonic() + 60
while not release.exists() and time.monotonic() < deadline:
    time.sleep(0.01)
sys.exit(code)
"""


@pytest.fixture
def setup(tmp_path_factory):
    root = tmp_path_factory.mktemp("sr")
    release = root / "release"
    paths = serve_paths(root)

    def argv(job_id: str) -> list[str]:
        return [sys.executable, "-c", _CHILD, job_id, str(release), "3"]

    launcher = SR.RunLauncher(paths, argv_for=argv)
    yield root, paths, launcher, release
    release.touch()
    for record in paths.runs_dir.glob("*.json") if paths.runs_dir.is_dir() else ():
        launcher.wait(record.stem, timeout=30)


def test_the_default_command_is_job_run_through_this_interpreter():
    assert SR.job_run_argv("abc") == [sys.executable, "-m", "apps.cli.main", "job", "run", "abc"]


def test_a_started_run_is_recorded_then_recorded_again_with_its_exit_code(setup):
    root, paths, launcher, release = setup
    record = launcher.start("job1")
    assert record.exit_code is None and record.ended_at is None
    assert SR.read_run_record(paths, "job1") == record
    assert launcher.running("job1")
    release.touch()
    assert launcher.wait("job1", timeout=30) == 3
    ended = SR.read_run_record(paths, "job1")
    assert (ended.pid, ended.started_at, ended.exit_code) == (record.pid, record.started_at, 3)
    assert ended.ended_at is not None
    assert not launcher.running("job1")


def test_a_run_runs_direct_in_its_own_session_on_the_supervisors_data_root(setup):
    root, paths, launcher, release = setup
    record = launcher.start("job2")
    release.touch()
    launcher.wait("job2", timeout=30)
    assert Path(record.out_log).read_text() == f"run job2 1 {root} True\n"
    assert Path(record.err_log).read_text() == "to stderr\n"
    assert (Path(record.out_log).parent, Path(record.out_log).name) == (paths.runs_dir, "job2.out")


def test_a_second_start_of_a_running_job_is_refused_and_starts_nothing(setup):
    root, paths, launcher, release = setup
    first = launcher.start("job3")
    with pytest.raises(SR.RunRefused) as caught:
        launcher.start("job3")
    assert caught.value.token == "job_already_running"
    assert str(first.pid) in str(caught.value)
    assert SR.read_run_record(paths, "job3") == first


def test_different_jobs_run_side_by_side(setup):
    root, paths, launcher, release = setup
    a, b = launcher.start("job4"), launcher.start("job5")
    assert a.pid != b.pid and launcher.running("job4") and launcher.running("job5")


def test_a_job_whose_run_ended_can_be_started_again(setup):
    root, paths, launcher, release = setup
    first = launcher.start("job6")
    release.touch()
    launcher.wait("job6", timeout=30)
    second = launcher.start("job6")
    assert second.pid != first.pid
    assert SR.read_run_record(paths, "job6") == second


def test_the_record_file_is_the_records_json(setup):
    root, paths, launcher, release = setup
    record = launcher.start("job7")
    data = json.loads((paths.runs_dir / "job7.json").read_text(encoding="utf-8"))
    assert data == record.to_json()
    assert sorted(data) == ["ended_at", "err_log", "exit_code", "job_id", "out_log", "pid",
                            "started_at"]


def test_a_record_that_cannot_be_read_is_none(tmp_path):
    paths = serve_paths(tmp_path)
    assert SR.read_run_record(paths, "missing") is None
    paths.runs_dir.mkdir(parents=True)
    (paths.runs_dir / "bad.json").write_text("{not json", encoding="utf-8")
    assert SR.read_run_record(paths, "bad") is None


def test_waiting_for_a_job_this_launcher_never_started_is_none(setup):
    root, paths, launcher, release = setup
    assert launcher.wait("never") is None
