"""The runs the `remedy serve start` supervisor starts (F200, DECISIONs F200 D1 (4) and D4).

Every run here is a stand-in for `remedy job run`: a Python child that prints its
job id and its environment's two settings, waits until the test creates its
release file, and exits with the code the test chose. Each test releases every
child it started, so no run outlives the test.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from packages.orchestration import serve_runs as SR
from packages.orchestration.serve_paths import serve_paths

_CHILD = """\
import os, sys, time
from pathlib import Path
job_id, release, code = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3])
print("run", job_id, os.environ.get("REMEDY_SERVE_DIRECT"), os.environ.get("REMEDY_DATA_DIR"),
      os.getsid(0) == os.getpid(), sys.argv[4:], os.environ["PYTHONPATH"].split(os.pathsep)[0])
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
    assert Path(record.out_log).read_text() == f"run job2 1 {root} True [] {SR.CODE_ROOT}\n"
    assert Path(record.err_log).read_text() == "to stderr\n"
    assert (Path(record.out_log).parent, Path(record.out_log).name) == (paths.runs_dir, "job2.out")


def test_a_json_run_adds_the_one_option_a_supervised_run_takes(setup):
    root, paths, launcher, release = setup
    record = launcher.start("job8", json_output=True)
    release.touch()
    launcher.wait("job8", timeout=30)
    assert Path(record.out_log).read_text().split(" ")[5] == "['--json']"


def test_a_run_starts_with_the_child_environment(setup):
    root, paths, launcher, release = setup
    env = SR.child_environment(paths)
    assert env[SR.DIRECT_ENV] == "1" and env["REMEDY_DATA_DIR"] == str(root)
    assert env["PYTHONPATH"].split(os.pathsep)[0] == str(SR.CODE_ROOT)
    record = launcher.start("jobenv")
    release.touch()
    launcher.wait("jobenv", timeout=30)
    assert Path(record.out_log).read_text().split(" ")[2:4] == ["1", str(root)]


def test_the_code_root_holds_the_command_line_the_run_imports():
    assert (SR.CODE_ROOT / "apps" / "cli" / "main.py").is_file()


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


# ---------------------------------------------------------------------------
# resume_registered (DECISION F200 D7): adopt / restart / lose a stale record
# ---------------------------------------------------------------------------


def _plant_record(paths, record: SR.RunRecord) -> None:
    """Write RECORD directly, the way a crashed supervisor would leave it behind."""
    paths.runs_dir.mkdir(parents=True, exist_ok=True)
    (paths.runs_dir / f"{record.job_id}.json").write_text(
        json.dumps(record.to_json()), encoding="utf-8")


def _dead_pid() -> int:
    """A process id guaranteed to name no process: spawned, then reaped."""
    proc = subprocess.Popen([sys.executable, "-c", "pass"])
    proc.wait()
    return proc.pid


def _spawn_child(job_id: str, release: Path, code: int = 0) -> subprocess.Popen:
    """A real `_CHILD` process, started OUTSIDE any `RunLauncher` (no reaper of its own)."""
    return subprocess.Popen(
        [sys.executable, "-c", _CHILD, job_id, str(release), str(code)],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        env={**os.environ, "PYTHONPATH": str(SR.CODE_ROOT)})


def test_resume_registered_restarts_a_job_whose_own_record_still_reads_running(setup):
    root, paths, launcher, release = setup
    _plant_record(paths, SR.RunRecord(
        job_id="jobR", pid=_dead_pid(), started_at="2026-01-01T00:00:00Z",
        out_log=str(paths.runs_dir / "jobR.out"), err_log=str(paths.runs_dir / "jobR.err")))
    outcomes = launcher.resume_registered(job_is_running=lambda jid: jid == "jobR")
    assert outcomes == [{"job_id": "jobR", "action": "restarted"}]
    assert launcher.running("jobR")
    release.touch()
    assert launcher.wait("jobR", timeout=30) == 3


def test_resume_registered_marks_a_lost_run_when_the_job_is_not_running(setup):
    root, paths, launcher, release = setup
    _plant_record(paths, SR.RunRecord(
        job_id="jobL", pid=_dead_pid(), started_at="2026-01-01T00:00:00Z",
        out_log="o", err_log="e"))
    outcomes = launcher.resume_registered(job_is_running=lambda jid: False)
    assert outcomes == [{"job_id": "jobL", "action": "lost"}]
    ended = SR.read_run_record(paths, "jobL")
    assert ended.exit_code is None
    assert ended.ended_at is not None


def test_resume_registered_leaves_an_already_ended_record_alone(setup):
    root, paths, launcher, release = setup
    ended_record = SR.RunRecord(
        job_id="jobE", pid=_dead_pid(), started_at="2026-01-01T00:00:00Z",
        out_log="o", err_log="e", exit_code=0, ended_at="2026-01-01T00:00:03Z")
    _plant_record(paths, ended_record)
    before = (paths.runs_dir / "jobE.json").read_bytes()

    outcomes = launcher.resume_registered(job_is_running=lambda jid: True)

    assert outcomes == []
    assert not launcher.running("jobE")
    after = (paths.runs_dir / "jobE.json").read_bytes()
    assert after == before, "a record whose end was already recorded must not be touched"


def test_resume_registered_skips_a_record_that_cannot_be_read(setup):
    root, paths, launcher, release = setup
    paths.runs_dir.mkdir(parents=True, exist_ok=True)
    (paths.runs_dir / "bad.json").write_text("{not json", encoding="utf-8")
    assert launcher.resume_registered(job_is_running=lambda jid: True) == []


def test_resume_registered_adopts_a_still_running_process_and_refuses_a_second_start(setup):
    root, paths, launcher, release = setup
    proc = _spawn_child("jobA", release, 3)
    try:
        _plant_record(paths, SR.RunRecord(
            job_id="jobA", pid=proc.pid, started_at="2026-01-01T00:00:00Z",
            out_log="o", err_log="e"))
        outcomes = launcher.resume_registered(job_is_running=lambda jid: False)
        assert outcomes == [{"job_id": "jobA", "action": "adopted"}]
        assert launcher.running("jobA")
        with pytest.raises(SR.RunRefused) as caught:
            launcher.start("jobA")
        assert caught.value.token == "job_already_running"

        release.touch()
        deadline = time.monotonic() + 30
        while launcher.running("jobA") and time.monotonic() < deadline:
            time.sleep(0.02)
        assert not launcher.running("jobA"), "the adopted watcher never noticed the end"
        ended = SR.read_run_record(paths, "jobA")
        assert ended.exit_code is None, "this supervisor is not the process's parent"
        assert ended.ended_at is not None
    finally:
        release.touch()
        proc.wait(timeout=10)


def test_resume_registered_does_not_adopt_a_live_pid_whose_cmdline_names_another_job(setup):
    root, paths, launcher, release = setup
    proc = _spawn_child("some-other-job", release, 0)
    try:
        _plant_record(paths, SR.RunRecord(
            job_id="jobB", pid=proc.pid, started_at="2026-01-01T00:00:00Z",
            out_log="o", err_log="e"))
        outcomes = launcher.resume_registered(job_is_running=lambda jid: False)
        assert outcomes == [{"job_id": "jobB", "action": "lost"}]
        assert not launcher.running("jobB")
        ended = SR.read_run_record(paths, "jobB")
        assert ended.exit_code is None
        assert ended.ended_at is not None
    finally:
        release.touch()
        proc.wait(timeout=10)


# ---------------------------------------------------------------------------
# The default reader (`_job_is_running`, no override) against a real data root
# ---------------------------------------------------------------------------


def test_the_default_reader_restarts_a_job_whose_own_plan_reads_running(setup):
    from packages.orchestration.pingpong_job import JOB_RUNNING, JobPlan, TaskEntry, save_job_plan

    root, paths, launcher, release = setup
    job = JobPlan(job_title="running-job", state=JOB_RUNNING,
                 tasks=[TaskEntry(title="t0", body="d")])
    save_job_plan(job, root)
    job_id = str(job.job_id)
    _plant_record(paths, SR.RunRecord(
        job_id=job_id, pid=_dead_pid(), started_at="2026-01-01T00:00:00Z",
        out_log=str(paths.runs_dir / f"{job_id}.out"), err_log=str(paths.runs_dir / f"{job_id}.err")))
    outcomes = launcher.resume_registered()                       # no override: the default reader
    assert outcomes == [{"job_id": job_id, "action": "restarted"}]
    assert launcher.running(job_id)
    release.touch()
    assert launcher.wait(job_id, timeout=30) == 3


def test_the_default_reader_marks_a_completed_jobs_run_as_lost(setup):
    from packages.orchestration.pingpong_job import JOB_COMPLETED, JobPlan, TaskEntry, save_job_plan

    root, paths, launcher, release = setup
    job = JobPlan(job_title="completed-job", state=JOB_COMPLETED,
                 tasks=[TaskEntry(title="t0", body="d")])
    save_job_plan(job, root)
    job_id = str(job.job_id)
    _plant_record(paths, SR.RunRecord(
        job_id=job_id, pid=_dead_pid(), started_at="2026-01-01T00:00:00Z",
        out_log="o", err_log="e"))
    outcomes = launcher.resume_registered()
    assert outcomes == [{"job_id": job_id, "action": "lost"}]
    ended = SR.read_run_record(paths, job_id)
    assert ended.exit_code is None
    assert ended.ended_at is not None


def test_the_default_reader_treats_a_wrong_shaped_job_record_as_not_running(setup):
    """`load_job_plan` would RAISE on this record; the default reader must not."""
    root, paths, launcher, release = setup
    job_id = "0123456789abcdef"
    job_dir = root / "jobs" / job_id
    job_dir.mkdir(parents=True)
    (job_dir / "job.json").write_text(
        json.dumps({"job_id": job_id, "run_manifest": {"required_v": "oops"}}),
        encoding="utf-8")
    _plant_record(paths, SR.RunRecord(
        job_id=job_id, pid=_dead_pid(), started_at="2026-01-01T00:00:00Z",
        out_log="o", err_log="e"))

    outcomes = launcher.resume_registered()           # must not raise
    assert outcomes == [{"job_id": job_id, "action": "lost"}]
    ended = SR.read_run_record(paths, job_id)
    assert ended.exit_code is None
    assert ended.ended_at is not None


# ---------------------------------------------------------------------------
# A restart that cannot even launch (DECISION F200 D7's "failed" outcome)
# ---------------------------------------------------------------------------


def test_resume_registered_marks_a_failed_restart_and_leaves_the_record_untouched(setup):
    root, paths, launcher, release = setup
    bad_launcher = SR.RunLauncher(paths, argv_for=lambda job_id: ["/no/such/remedy-exe", job_id])

    first = SR.RunRecord(
        job_id="jobF", pid=_dead_pid(), started_at="2026-01-01T00:00:00Z",
        out_log=str(paths.runs_dir / "jobF.out"), err_log=str(paths.runs_dir / "jobF.err"))
    _plant_record(paths, first)
    before = (paths.runs_dir / "jobF.json").read_bytes()

    # a second stale record in the same registry, which must still be
    # reconciled even though the first one's restart failed
    _plant_record(paths, SR.RunRecord(
        job_id="jobG", pid=_dead_pid(), started_at="2026-01-01T00:00:00Z",
        out_log="o", err_log="e"))

    outcomes = bad_launcher.resume_registered(job_is_running=lambda jid: True)
    assert outcomes == [
        {"job_id": "jobF", "action": "failed"},
        {"job_id": "jobG", "action": "failed"},
    ]
    after = (paths.runs_dir / "jobF.json").read_bytes()
    assert after == before, "a failed restart must not touch the stale record"


# ---------------------------------------------------------------------------
# CommandRunner (DECISION F253 D9): a command as a child, its envelope returned
# ---------------------------------------------------------------------------


def _runner(tmp_path, code: str, **keywords) -> SR.CommandRunner:
    """A runner whose command is the Python CODE, so that no Remedy command runs."""
    return SR.CommandRunner(serve_paths(tmp_path), argv_prefix=[sys.executable, "-c", code],
                            **keywords)


def test_the_runner_returns_the_envelope_line_as_a_dict(tmp_path):
    code = 'import json, sys; print(json.dumps({"ok": True, "argv": sys.argv[1:]}))'
    assert _runner(tmp_path, code).run("j", ["a", "--b=c"]) == {"ok": True, "argv": ["a", "--b=c"]}


def test_the_runner_ignores_the_output_before_the_last_line(tmp_path):
    code = 'print("a note"); print("{}"); print(\'{"ok": false, "error": "x"}\'); print()'
    assert _runner(tmp_path, code).run("j", []) == {"ok": False, "error": "x"}


@pytest.mark.parametrize("last_line", ["not json", "[1, 2]", '"ok"', '{"error": "x"}', ""])
def test_a_last_line_that_is_no_envelope_gives_none(tmp_path, last_line):
    code = f"print({last_line!r})"
    assert _runner(tmp_path, code).run("j", []) is None


def test_a_command_that_cannot_start_gives_none(tmp_path):
    runner = SR.CommandRunner(serve_paths(tmp_path), argv_prefix=["/no/such/remedy-exe"])
    assert runner.run("j", []) is None


def test_a_command_past_the_timeout_gives_none_and_leaves_no_live_child(tmp_path):
    pid_file = tmp_path / "pid"
    code = ("import os, sys, time; open(sys.argv[1], 'w').write(str(os.getpid())); "
            "time.sleep(60)")
    started = time.monotonic()
    assert _runner(tmp_path, code, timeout=1).run("j", [str(pid_file)]) is None
    # R-1194: the ceiling bites, rather than the child ending on its own after its sleep.
    assert time.monotonic() - started < 30
    assert not SR._process_is_alive(int(pid_file.read_text()))


def test_the_default_timeout_is_the_ceiling_the_decision_names():
    assert SR.PUBLIC_API_COMMAND_TIMEOUT_SECONDS == 120
    assert SR.CommandRunner(serve_paths(Path("/x"))).timeout == 120


def test_the_command_sees_the_direct_setting_and_the_supervisors_data_root(tmp_path):
    code = ('import json, os; print(json.dumps({"ok": True, "direct": os.environ["REMEDY_SERVE_DIRECT"], '
            '"data": os.environ["REMEDY_DATA_DIR"]}))')
    answer = _runner(tmp_path, code).run("j", [])
    assert (answer["direct"], answer["data"]) == ("1", str(tmp_path))


_TIMED = """\
import sys, time
start = time.time()
time.sleep(0.6)
with open(sys.argv[1], "a") as handle:
    handle.write(f"{start} {time.time()}\\n")
print('{"ok": true}')
"""


def _timed_intervals(tmp_path, jobs: tuple[str, str]) -> list[tuple[float, float]]:
    log = tmp_path / "times"
    runner = _runner(tmp_path, _TIMED)
    threads = [threading.Thread(target=runner.run, args=(job, [str(log)])) for job in jobs]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=60)
    assert not any(thread.is_alive() for thread in threads)
    rows = [tuple(map(float, line.split())) for line in log.read_text().splitlines()]
    return sorted(rows)


def test_two_commands_for_one_job_never_overlap(tmp_path):
    (first_start, first_end), (second_start, _) = _timed_intervals(tmp_path, ("one", "one"))
    assert second_start >= first_end


def test_commands_for_two_jobs_overlap(tmp_path):
    (first_start, first_end), (second_start, _) = _timed_intervals(tmp_path, ("one", "two"))
    assert second_start < first_end


# ---------------------------------------------------------------------------
# OrderLauncher (F253 S5a, DECISION F253 D13): an order kept as a record of
# its own, run the way `remedy do` runs an order file.
# ---------------------------------------------------------------------------

#: A stand-in for `remedy do run`: it prints one JSON envelope naming its own arguments,
#: its working folder and its `REMEDY_DATA_DIR`, then waits for a release file (its path
#: at argv[3], the exit code to use at argv[4] — both OPTIONS the test passes through
#: `OrderLauncher.start`) before exiting with that code.
_ORDER_CHILD = """\
import json, os, sys, time
from pathlib import Path
release, code = Path(sys.argv[3]), int(sys.argv[4])
print(json.dumps({"ok": True, "argv": sys.argv[1:], "cwd": os.getcwd(),
                  "data_dir": os.environ.get("REMEDY_DATA_DIR")}))
sys.stdout.flush()
deadline = time.monotonic() + 60
while not release.exists() and time.monotonic() < deadline:
    time.sleep(0.01)
sys.exit(code)
"""


@pytest.fixture
def order_setup(tmp_path_factory):
    root = tmp_path_factory.mktemp("so")
    release = root / "release"
    paths = serve_paths(root)
    launcher = SR.OrderLauncher(paths, argv_prefix=[sys.executable, "-c", _ORDER_CHILD])
    yield root, paths, launcher, release
    release.touch()
    for order_dir in (paths.orders_dir.glob("*") if paths.orders_dir.is_dir() else ()):
        launcher.wait(order_dir.name, timeout=30)


def _order_printed(record: SR.OrderRecord) -> dict:
    return json.loads(Path(record.out_log).read_text(encoding="utf-8").splitlines()[0])


def test_the_childs_arguments_after_the_prefix_equal_the_built_command(order_setup):
    root, paths, launcher, release = order_setup
    record = launcher.start("do something", [str(release), "0"])
    release.touch()
    launcher.wait(record.order_id, timeout=30)
    assert _order_printed(record)["argv"] == [
        "do", "run", str(release), "0", "--json", "--no-ui", "--yes", "--", "order.md"]


def test_the_orders_working_folder_is_its_own_folder_on_its_data_root(order_setup):
    root, paths, launcher, release = order_setup
    record = launcher.start("x", [str(release), "0"])
    release.touch()
    launcher.wait(record.order_id, timeout=30)
    printed = _order_printed(record)
    assert Path(printed["cwd"]) == paths.orders_dir / record.order_id
    assert printed["data_dir"] == str(root)


def test_order_md_holds_the_text_byte_for_byte(order_setup):
    root, paths, launcher, release = order_setup
    text = "---\nmax-cost-usd: 1\n---\nWrite étoile to a file.\n"
    record = launcher.start(text, [str(release), "0"])
    assert Path(record.order_file).read_bytes() == text.encode("utf-8")
    assert Path(record.order_file) == paths.orders_dir / record.order_id / "order.md"
    release.touch()
    launcher.wait(record.order_id, timeout=30)


@pytest.mark.parametrize("code", [0, 7])
def test_the_record_has_no_end_at_start_and_the_exit_code_at_the_end(order_setup, code):
    root, paths, launcher, release = order_setup
    record = launcher.start("x", [str(release), str(code)])
    assert record.exit_code is None and record.ended_at is None
    assert SR.read_order_record(paths, record.order_id) == record
    release.touch()
    assert launcher.wait(record.order_id, timeout=30) == code
    ended = SR.read_order_record(paths, record.order_id)
    assert (ended.exit_code, ended.pid, ended.started_at) == (code, record.pid, record.started_at)
    assert ended.ended_at is not None


def test_two_starts_get_two_different_ids_and_folders(order_setup):
    root, paths, launcher, release = order_setup
    first = launcher.start("x", [str(release), "0"])
    second = launcher.start("y", [str(release), "0"])
    assert first.order_id != second.order_id
    assert Path(first.order_file).parent != Path(second.order_file).parent
    release.touch()
    launcher.wait(first.order_id, timeout=30)
    launcher.wait(second.order_id, timeout=30)


def test_start_removes_the_orders_folder_and_reraises_when_the_child_cannot_start(tmp_path):
    """R-1201: when `subprocess.Popen` cannot start the child, `OrderLauncher.start` removes
    the order's own folder whole and raises `OSError` again, leaving no half-made order."""
    paths = serve_paths(tmp_path)
    missing_program = tmp_path / "no-such-program"
    launcher = SR.OrderLauncher(paths, argv_prefix=[str(missing_program)])
    with pytest.raises(OSError):
        launcher.start("x", [])
    assert list(paths.orders_dir.glob("*")) == []


@pytest.mark.parametrize("bad_id", [
    "../../x", "0123456789ABCDEF", "0123456789abcde", "0123456789abcdef"])
def test_read_order_record_refuses_a_malformed_or_unknown_id(tmp_path, bad_id):
    paths = serve_paths(tmp_path)
    assert SR.read_order_record(paths, bad_id) is None


def test_read_order_record_refuses_a_malformed_id_with_a_real_file_at_its_path(tmp_path):
    """R-1198: the id shape guard must itself refuse a malformed id — a readable,
    well-formed record planted exactly where that id's path would point must not be
    found, so a loosened regex cannot hide behind "no file to find"."""
    paths = serve_paths(tmp_path)
    good = SR.OrderRecord(order_id="placeholder", pid=1, started_at="t",
                          order_file="o", out_log="o", err_log="e")
    for bad_id in ("../x", "0123456789ABCDEF"):
        order_dir = paths.orders_dir / bad_id
        order_dir.mkdir(parents=True)
        (order_dir / "order.json").write_text(json.dumps(good.to_json()), encoding="utf-8")
        assert SR.read_order_record(paths, bad_id) is None


def test_order_state_is_running_then_ended(order_setup):
    root, paths, launcher, release = order_setup
    record = launcher.start("x", [str(release), "0"])
    assert SR.order_state(paths, record) == "running"
    release.touch()
    launcher.wait(record.order_id, timeout=30)
    ended = SR.read_order_record(paths, record.order_id)
    assert SR.order_state(paths, ended) == "ended"


def test_order_state_is_running_under_a_data_root_reached_through_a_symlink(tmp_path):
    """R-1197: `/proc/<pid>/cwd` answers the RESOLVED path, so a data root reached
    through a symbolic link must not read a running order as `lost`."""
    real_root = tmp_path / "real"
    real_root.mkdir()
    link_root = tmp_path / "link"
    link_root.symlink_to(real_root)
    release = tmp_path / "release"
    paths = serve_paths(link_root)
    launcher = SR.OrderLauncher(paths, argv_prefix=[sys.executable, "-c", _ORDER_CHILD])
    record = launcher.start("x", [str(release), "0"])
    try:
        assert SR.order_state(paths, record) == "running"
    finally:
        release.touch()
        launcher.wait(record.order_id, timeout=30)
    ended = SR.read_order_record(paths, record.order_id)
    assert SR.order_state(paths, ended) == "ended"


def test_order_state_is_lost_for_a_record_with_no_end_whose_process_is_gone(tmp_path):
    paths = serve_paths(tmp_path)
    record = SR.OrderRecord(order_id="0123456789abcdef", pid=_dead_pid(),
                            started_at="2026-01-01T00:00:00Z",
                            order_file="o", out_log="o", err_log="e")
    assert SR.order_state(paths, record) == "lost"


def test_order_state_is_lost_when_the_pid_is_alive_in_another_folder(tmp_path):
    """R-1199: the identity check must not reduce to whether the pid is alive — a live
    process (this test's own) working in another folder must still read `lost`."""
    paths = serve_paths(tmp_path)
    record = SR.OrderRecord(order_id="0123456789abcdef", pid=os.getpid(),
                            started_at="2026-01-01T00:00:00Z",
                            order_file="o", out_log="o", err_log="e")
    assert SR.order_state(paths, record) == "lost"


@pytest.mark.parametrize("last_line", ["not json", '{"no_ok": true}'])
def test_order_answer_is_none_when_the_last_line_is_no_envelope(tmp_path, last_line):
    out = tmp_path / "out.log"
    out.write_text(last_line + "\n", encoding="utf-8")
    record = SR.OrderRecord(order_id="o", pid=1, started_at="t", order_file="o",
                            out_log=str(out), err_log="e")
    assert SR.order_answer(record) is None


def test_order_answer_is_the_object_when_the_last_line_is_one(tmp_path):
    out = tmp_path / "out.log"
    out.write_text('{"ok": true, "mission_id": "m1"}\n', encoding="utf-8")
    record = SR.OrderRecord(order_id="o", pid=1, started_at="t", order_file="o",
                            out_log=str(out), err_log="e")
    assert SR.order_answer(record) == {"ok": True, "mission_id": "m1"}
