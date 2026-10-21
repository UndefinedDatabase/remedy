"""F203 T001 — the structured log setup: lines, context ids, redaction, rotation, reset."""

from __future__ import annotations

import json
import logging
import logging.handlers
import os
import pathlib
import re
import stat

import pytest

from packages.orchestration import structured_log as structured_log_module
from packages.orchestration.config import load_config
from packages.orchestration.run_log import RunLogWriter
from packages.orchestration.structured_log import (
    DEFAULT_LOG_BACKUP_COUNT,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_MAX_BYTES,
    FILE_ONLY_ATTR,
    LOG_CONTEXT_KEYS,
    LOG_FILE_NAME,
    MIN_LOG_BACKUP_COUNT,
    MIN_LOG_MAX_BYTES,
    REMEDY_LOGGER_NAMES,
    bind_call_log_context,
    bind_log_context,
    configure_structured_logging,
    log_files_oldest_first,
    logs_dir,
    read_log_entries,
    remedy_log_job_id,
    remedy_log_run_id,
    remedy_log_task_id,
    reset_structured_logging,
)

# The keys of every JSON line, in order (R-1294: the tests' own copy, no production reader).
LOG_FIELD_NAMES = ("ts", "level", "logger", "message", "job_id", "task_id", "run_id")


def current_log_context() -> dict[str, str | None]:
    """The three ids bound now, read from the public context variables (R-1294)."""
    return {"job_id": remedy_log_job_id.get(), "task_id": remedy_log_task_id.get(),
            "run_id": remedy_log_run_id.get()}


CHILD = logging.getLogger("packages.orchestration.fixture")
APPS_CHILD = logging.getLogger("apps.cli.fixture")
LIBRARY = logging.getLogger("fixture_library.client")
TS_SHAPE = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$")
SECRET_PARTS = (
    "sk-ant-api03-AbCdEfGhIjKlMnOpQrStUvWxYz0123456789",
    "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
)


@pytest.fixture(autouse=True)
def _clean_logging(monkeypatch):
    for name in (
        "REMEDY_LOG_LEVEL", "REMEDY_LOG_JSON_LINES", "REMEDY_LOG_MAX_BYTES", "REMEDY_LOG_BACKUP_COUNT",
    ):
        monkeypatch.delenv(name, raising=False)
    reset_structured_logging()
    yield
    reset_structured_logging()


def _config(tmp_path: pathlib.Path, body: str = ""):
    toml = tmp_path / "remedy.toml"
    toml.write_text("[remedy.logging]\n" + body)
    return load_config(project_path=toml, user_path=pathlib.Path("/nonexistent/user.toml"))


def _setup(tmp_path: pathlib.Path, body: str = ""):
    root = tmp_path / "data"
    path = configure_structured_logging(root, _config(tmp_path, body))
    return root, path


def _flush() -> None:
    for handler in logging.getLogger().handlers:
        handler.flush()


def _lines(path: pathlib.Path) -> list[str]:
    _flush()
    return path.read_text(encoding="utf-8").splitlines()


def test_a_child_logger_record_carries_the_bound_ids_and_exact_keys(tmp_path):
    root, path = _setup(tmp_path)
    assert path == root / "logs" / LOG_FILE_NAME == logs_dir(root) / LOG_FILE_NAME
    with bind_log_context(job_id="j1", task_id="t1", run_id="r1"):
        CHILD.info("hello %s", "world")
    CHILD.info("outside")
    first, second = (json.loads(line) for line in _lines(path))
    assert list(first) == list(LOG_FIELD_NAMES)
    assert (first["job_id"], first["task_id"], first["run_id"]) == ("j1", "t1", "r1")
    assert first["level"] == "INFO"
    assert first["logger"] == "packages.orchestration.fixture"
    assert first["message"] == "hello world"
    assert TS_SHAPE.match(first["ts"])
    assert (second["job_id"], second["task_id"], second["run_id"]) == (None, None, None)


def test_nested_bindings_restore_what_was_before(tmp_path):
    with bind_log_context(job_id="outer"):
        with bind_log_context(task_id="inner"):
            assert current_log_context() == {"job_id": "outer", "task_id": "inner", "run_id": None}
        assert current_log_context() == {"job_id": "outer", "task_id": None, "run_id": None}
    assert current_log_context() == {"job_id": None, "task_id": None, "run_id": None}


def test_a_decorated_call_binds_the_ids_its_arguments_carry_for_the_whole_call():
    seen = []

    @bind_call_log_context(job_id="job", run_id="run")
    def work(job, *, run="", other=""):
        seen.append(current_log_context())

    with bind_log_context(task_id="outer-task", run_id="outer-run"):
        work("j1", run="r1")
        work("j2")
    assert seen == [{"job_id": "j1", "task_id": "outer-task", "run_id": "r1"},
                    {"job_id": "j2", "task_id": "outer-task", "run_id": "outer-run"}]
    assert current_log_context() == {"job_id": None, "task_id": None, "run_id": None}


def test_a_call_given_no_run_id_is_given_a_fresh_one_it_also_receives():
    received = []

    @bind_call_log_context(run_id="run_id", mint_run_id=lambda: "minted")
    def work(*, run_id=""):
        received.append((run_id, current_log_context()["run_id"]))

    work()
    work(run_id="given")
    assert received == [("minted", "minted"), ("given", "given")]


class _ProbeProvider:
    """A builder and reviewer stand-in that logs one line from inside the run, through a Remedy logger."""

    name = "fake"
    supports_resume = False

    def build(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume=None):
        from packages.orchestration.pingpong_provider import BuilderOutput

        CHILD.warning("probe from the builder")
        return BuilderOutput(summary="ok", provider="fake")

    def review(self, prompt, *, timeout_sec=120, max_output_chars=50000, resume=None):
        from packages.orchestration.pingpong_provider import ReviewerOutput

        return ReviewerOutput(verdict="pass", provider="fake")


def _probe_lines(path: pathlib.Path) -> list[dict]:
    return [entry for entry in map(json.loads, _lines(path)) if entry["message"] == "probe from the builder"]


def test_a_line_a_run_logs_carries_its_job_task_and_run_ids(tmp_path, monkeypatch):
    """R-1279: through `run_pingpong`, as `run_job` calls it, and on its own."""
    from packages.orchestration.pingpong_loop import run_pingpong

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    _root, path = _setup(tmp_path)
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n")
    probe = _ProbeProvider()
    given = run_pingpong("Fix README", str(repo), builder_provider=probe, reviewer_provider=probe,
                         max_rounds=1, job_id="job-1", task_id="task-1", run_id="run-given")
    alone = run_pingpong("Fix README", str(repo), builder_provider=probe, reviewer_provider=probe, max_rounds=1)

    first, second = _probe_lines(path)
    assert (first["job_id"], first["task_id"], first["run_id"]) == ("job-1", "task-1", "run-given")
    assert given.run_id == "run-given"
    assert (second["job_id"], second["task_id"], second["run_id"]) == (None, None, alone.run_id)
    assert alone.run_id


def test_a_line_a_job_logs_carries_its_job_id(tmp_path, monkeypatch):
    """R-1279: `run_job` binds the job's id around everything the job does, outside its runs too."""
    from packages.orchestration import pingpong_job
    from packages.orchestration.pingpong_job import load_job_plan, parse_job_file, run_job

    monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
    _root, path = _setup(tmp_path)
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# Demo\n")
    job = parse_job_file("# Job: Probe\n\n## Task 1\nFix the README.\n\nAcceptance:\n- README fixed\n", str(repo))
    started = pingpong_job._log_task_started

    def logged_start(*args, **kwargs):
        CHILD.warning("probe from the job")
        return started(*args, **kwargs)

    monkeypatch.setattr(pingpong_job, "_log_task_started", logged_start)
    probe = _ProbeProvider()
    run_job(job.job_id, builder_provider=probe, reviewer_provider=probe, repair_rounds=0)

    entries = [json.loads(line) for line in _lines(path)]
    (job_line,) = [entry for entry in entries if entry["message"] == "probe from the job"]
    (run_line,) = _probe_lines(path)
    task = load_job_plan(job.job_id).tasks[0]
    assert (job_line["job_id"], job_line["task_id"], job_line["run_id"]) == (job.job_id, None, None)
    assert (run_line["job_id"], run_line["task_id"], run_line["run_id"]) == (job.job_id, task.task_id, task.run_id)


def test_an_exception_in_a_block_resets_all_ids():
    with pytest.raises(RuntimeError):
        with bind_log_context(job_id="j", task_id="t", run_id="r"):
            raise RuntimeError("boom")
    assert current_log_context() == {"job_id": None, "task_id": None, "run_id": None}


def test_a_uuid_argument_is_stored_as_its_string():
    import uuid

    value = uuid.uuid4()
    with bind_log_context(job_id=value):
        assert current_log_context()["job_id"] == str(value)


def test_current_log_context_answers_the_three_keys_in_order():
    assert tuple(current_log_context()) == LOG_CONTEXT_KEYS == ("job_id", "task_id", "run_id")


def test_an_explicit_extra_wins_over_a_bound_id(tmp_path):
    _, path = _setup(tmp_path)
    with bind_log_context(job_id="bound", task_id="t1"):
        CHILD.info("x", extra={"job_id": "explicit"})
    entry = json.loads(_lines(path)[0])
    assert entry["job_id"] == "explicit"
    assert entry["task_id"] == "t1"


def test_an_exception_adds_a_last_key_and_a_plain_line_has_none(tmp_path):
    _, path = _setup(tmp_path)
    try:
        raise KeyError("missing-thing")
    except KeyError:
        CHILD.exception("it failed")
    CHILD.info("fine")
    failed, fine = (json.loads(line) for line in _lines(path))
    assert list(failed)[-1] == "exception"
    assert "KeyError" in failed["exception"]
    assert "exception" not in fine


@pytest.mark.parametrize("as_json", [True, False])
def test_planted_secrets_never_reach_the_file_and_every_line_parses(tmp_path, as_json):
    _, path = _setup(tmp_path, f"json_lines = {'true' if as_json else 'false'}\n")
    CHILD.info("failed with %s and %s", *SECRET_PARTS)
    try:
        raise RuntimeError("inside " + " ".join(SECRET_PARTS))
    except RuntimeError:
        CHILD.exception("crashed")
    _flush()
    raw = path.read_bytes()
    for secret in SECRET_PARTS:
        assert secret.encode() not in raw
    assert b"AbCdEfGhIjKl" not in raw
    assert b"[REDACTED]" in raw
    if as_json:
        for line in raw.decode("utf-8").splitlines():
            json.loads(line)


def test_json_false_writes_a_text_line(tmp_path):
    _, path = _setup(tmp_path, "json_lines = false\n")
    with bind_log_context(job_id="j1"):
        CHILD.info("plain words")
    line = _lines(path)[0]
    assert re.match(r"^\S+ INFO packages\.orchestration\.fixture job=j1 task=- run=- plain words$", line)


def test_a_private_key_in_a_text_line_hides_only_the_message(tmp_path):
    """R-1280, DECISION F307 D5: the time, level, logger and ids of the line survive."""
    _, path = _setup(tmp_path, "json_lines = false\n")
    with bind_log_context(job_id="j1"):
        CHILD.info("bad key %s", "-----BEGIN RSA " + "PRIVATE KEY-----\nMIIEabcdef")
    (line,) = _lines(path)
    assert re.match(
        r"^\S+ INFO packages\.orchestration\.fixture job=j1 task=- run=- \[PRIVATE_KEY_REDACTED\]$", line)


def test_default_level_writes_info_and_not_debug(tmp_path):
    _, path = _setup(tmp_path)
    CHILD.debug("quiet one")
    CHILD.info("loud one")
    messages = [json.loads(line)["message"] for line in _lines(path)]
    assert messages == ["loud one"]


def test_debug_level_writes_the_debug_record(tmp_path):
    _, path = _setup(tmp_path, 'level = "DEBUG"\n')
    CHILD.debug("quiet one")
    assert [json.loads(line)["message"] for line in _lines(path)] == ["quiet one"]


def test_an_unknown_level_writes_info_and_one_warning_naming_it(tmp_path):
    _, path = _setup(tmp_path, 'level = "loud"\n')
    CHILD.debug("quiet one")
    CHILD.info("info one")
    entries = [json.loads(line) for line in _lines(path)]
    assert [e["level"] for e in entries] == ["WARNING", "INFO"]
    assert "'loud'" in entries[0]["message"]


def test_folder_and_file_modes_and_rotation_keep_owner_only_files(tmp_path):
    root, path = _setup(tmp_path, "max_bytes = 2000\nbackup_count = 2\n")
    assert not (root / "logs").exists()
    for index in range(60):
        CHILD.info("record number %d with some padding to fill the file quickly", index)
    _flush()
    assert stat.S_IMODE(os.stat(root / "logs").st_mode) == 0o700
    folder = root / "logs"
    names = sorted(p.name for p in folder.iterdir())
    # The rotation lock (operator amendment amend1014-luna-mission-fixes B.2) is owner-only too.
    assert names == [LOG_FILE_NAME, LOG_FILE_NAME + ".1", LOG_FILE_NAME + ".2", LOG_FILE_NAME + ".lock"]
    for name in names:
        assert stat.S_IMODE(os.stat(folder / name).st_mode) == 0o600
    assert not (folder / (LOG_FILE_NAME + ".3")).exists()
    assert path == folder / LOG_FILE_NAME


def test_a_warning_reaches_the_error_stream_bare_and_an_info_does_not(tmp_path, capsys):
    _setup(tmp_path)
    CHILD.info("not on the terminal")
    CHILD.warning("on the terminal")
    err = capsys.readouterr().err
    assert "on the terminal" in err
    assert "not on the terminal" not in err
    assert err.strip() == "on the terminal"


def test_configuring_twice_leaves_two_handlers_and_one_line_per_record(tmp_path):
    root = tmp_path / "data"
    config = _config(tmp_path)
    configure_structured_logging(root, config)
    path = configure_structured_logging(root, config)
    marked = [h for h in logging.getLogger().handlers if getattr(h, "_remedy_structured_log", False)]
    assert len(marked) == 2
    CHILD.info("once")
    assert len(_lines(path)) == 1


def test_reset_removes_its_handlers_keeps_foreign_ones_and_restores_the_levels(tmp_path):
    """R-1293 and R-1312, DECISION F307 D2: the setup lowers Remedy's two loggers, never the
    root, and a reset restores both and leaves nothing saved."""
    root_logger = logging.getLogger()
    foreign = logging.NullHandler()
    root_logger.addHandler(foreign)
    before = {name: logging.getLogger(name).level for name in ("", *REMEDY_LOGGER_NAMES)}
    try:
        _setup(tmp_path, 'level = "DEBUG"\n')
        assert REMEDY_LOGGER_NAMES == ("packages", "apps")
        assert [logging.getLogger(name).level for name in REMEDY_LOGGER_NAMES] == [logging.DEBUG] * 2
        assert root_logger.level == before[""]
        reset_structured_logging()
        assert not [h for h in root_logger.handlers if getattr(h, "_remedy_structured_log", False)]
        assert foreign in root_logger.handlers
        assert {name: logging.getLogger(name).level for name in before} == before
        assert structured_log_module._saved_logger_levels is None
    finally:
        root_logger.removeHandler(foreign)


def test_a_library_info_stays_out_of_the_file_while_remedy_info_is_written(tmp_path):
    """R-1293: a library's logger keeps the root's level, so only its warning reaches the file."""
    root_logger = logging.getLogger()
    before = root_logger.level
    root_logger.setLevel(logging.WARNING)
    try:
        _, path = _setup(tmp_path)
        LIBRARY.info("library chatter")
        CHILD.info("packages line")
        APPS_CHILD.info("apps line")
        LIBRARY.warning("library warning")
        messages = [json.loads(line)["message"] for line in _lines(path)]
        assert messages == ["packages line", "apps line", "library warning"]
    finally:
        root_logger.setLevel(before)


def test_an_error_level_keeps_a_remedy_warning_on_the_terminal_and_out_of_the_file(tmp_path, capsys):
    _, path = _setup(tmp_path, 'level = "ERROR"\n')
    CHILD.warning("shown, not written")
    CHILD.error("shown and written")
    assert capsys.readouterr().err.splitlines() == ["shown, not written", "shown and written"]
    assert [json.loads(line)["message"] for line in _lines(path)] == ["shown and written"]


def test_a_rotation_setting_below_its_floor_is_raised_with_one_warning_each(tmp_path, capsys):
    """R-1312, DECISION F307 D2: 0 would be a file that never rotates, or one truncated."""
    _setup(tmp_path, "max_bytes = 0\nbackup_count = 0\n")
    (handler,) = [h for h in logging.getLogger().handlers
                  if isinstance(h, logging.handlers.RotatingFileHandler)]
    assert (handler.maxBytes, handler.backupCount) == (MIN_LOG_MAX_BYTES, MIN_LOG_BACKUP_COUNT) == (1024, 1)
    assert capsys.readouterr().err.splitlines() == [
        "logging.max_bytes 0 is below its floor; 1024 is used",
        "logging.backup_count 0 is below its floor; 1 is used",
    ]


def test_a_root_that_cannot_be_written_drops_lines_silently_and_keeps_the_error_stream(
    tmp_path, capsys,
):
    blocker = tmp_path / "blocker"
    blocker.write_text("not a folder")
    path = configure_structured_logging(blocker, _config(tmp_path))
    assert path == blocker / "logs" / LOG_FILE_NAME
    CHILD.info("dropped")
    CHILD.warning("still shown")
    err = capsys.readouterr().err
    assert err.strip() == "still shown"
    assert "Logging error" not in err


def test_a_file_only_record_is_in_the_file_and_not_on_the_error_stream(tmp_path, capsys):
    _, path = _setup(tmp_path)
    CHILD.error("file only line", extra={FILE_ONLY_ATTR: True})
    CHILD.error("both places line")
    err = capsys.readouterr().err
    assert "file only line" not in err
    assert "both places line" in err
    messages = [json.loads(line)["message"] for line in _lines(path)]
    assert messages == ["file only line", "both places line"]


def test_the_defaults_of_the_four_keys_read_from_an_empty_configuration(tmp_path):
    config = load_config(
        project_path=tmp_path / "absent.toml", user_path=pathlib.Path("/nonexistent/user.toml"),
    )
    assert config.get("logging.level") == "INFO" == DEFAULT_LOG_LEVEL
    assert config.get("logging.json_lines") is True
    assert config.get("logging.max_bytes") == 10000000 == DEFAULT_LOG_MAX_BYTES
    assert config.get("logging.backup_count") == 5 == DEFAULT_LOG_BACKUP_COUNT


def _write_log(root: pathlib.Path, name: str, *lines: str) -> None:
    folder = logs_dir(root)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text("".join(line + "\n" for line in lines), encoding="utf-8")


def _entry(job_id: object, message: str, run_id: object = None) -> str:
    return json.dumps({"job_id": job_id, "run_id": run_id, "message": message})


def test_the_read_answers_the_three_files_oldest_first(tmp_path):
    _write_log(tmp_path, "remedy.log.2", _entry("abc123", "oldest"))
    _write_log(tmp_path, "remedy.log.1", _entry("abc123", "middle"))
    _write_log(tmp_path, LOG_FILE_NAME, _entry("abc123", "newest"))
    result = read_log_entries(job_id="abc123", root=tmp_path)
    assert [entry["message"] for entry in result.entries] == ["oldest", "middle", "newest"]
    assert result.files == ("remedy.log.2", "remedy.log.1", "remedy.log")
    assert result.unreadable == 0


def test_a_non_numeric_suffix_is_never_read_and_ten_comes_before_two(tmp_path):
    _write_log(tmp_path, "remedy.log.x", _entry("abc123", "never"))
    _write_log(tmp_path, "remedy.log.2", _entry("abc123", "two"))
    _write_log(tmp_path, "remedy.log.10", _entry("abc123", "ten"))
    assert [path.name for path in log_files_oldest_first(tmp_path)] == [
        "remedy.log.10", "remedy.log.2",
    ]
    result = read_log_entries(job_id="abc123", root=tmp_path)
    assert [entry["message"] for entry in result.entries] == ["ten", "two"]


def test_the_job_id_matches_by_prefix_only_and_an_empty_one_matches_nothing(tmp_path):
    _write_log(tmp_path, LOG_FILE_NAME, _entry("abc123", "mine"), _entry("xabc", "other"))
    by_prefix = read_log_entries(job_id="abc", root=tmp_path)
    assert [entry["message"] for entry in by_prefix.entries] == ["mine"]
    assert read_log_entries(job_id="", root=tmp_path).entries == ()


def test_a_run_id_keeps_only_the_lines_of_its_run(tmp_path):
    _write_log(
        tmp_path, LOG_FILE_NAME,
        _entry("abc123", "first", "r1"), _entry("abc123", "second", "r2"), _entry("abc123", "bare"),
    )
    result = read_log_entries(job_id="abc123", run_id="r2", root=tmp_path)
    assert [entry["message"] for entry in result.entries] == ["second"]


def test_a_text_line_and_a_json_list_are_counted_and_a_blank_line_is_ignored(tmp_path):
    _write_log(
        tmp_path, LOG_FILE_NAME,
        "2026-10-13T08:05:09.042Z INFO x job=abc123 hello", "", "[1, 2]", _entry("abc123", "ok"),
    )
    result = read_log_entries(job_id="abc123", root=tmp_path)
    assert result.unreadable == 2
    assert [entry["message"] for entry in result.entries] == ["ok"]


def test_no_folder_answers_nothing(tmp_path):
    assert log_files_oldest_first(tmp_path) == []
    result = read_log_entries(job_id="abc", root=tmp_path)
    assert (result.entries, result.files, result.unreadable) == ((), (), 0)


def test_an_event_written_through_the_setup_is_read_back_with_its_run(tmp_path):
    root, _ = _setup(tmp_path)
    RunLogWriter("job-e2e", data_root=tmp_path).log("task_run_started", attempt_id="att-9")
    _flush()
    result = read_log_entries(job_id="job-e", root=root)
    (entry,) = result.entries
    assert entry["job_id"] == "job-e2e"
    assert entry["run_id"] == "att-9"


_WRITER = r"""
import logging, sys
sys.path.insert(0, sys.argv[3])
from packages.orchestration.structured_log import (
    JsonLogFormatter, LogContextFilter, OwnerOnlyRotatingFileHandler)
handler = OwnerOnlyRotatingFileHandler(sys.argv[1], maxBytes=4000, backupCount=200,
                                       encoding="utf-8", delay=True)
handler.setFormatter(JsonLogFormatter())
handler.addFilter(LogContextFilter())
logger = logging.getLogger("writer")
logger.propagate = False
logger.setLevel(logging.INFO)
logger.addHandler(handler)
for counter in range(400):
    logger.info("line %d of %s", counter, sys.argv[2], extra={"job_id": sys.argv[2]})
handler.close()
"""


def test_four_processes_sharing_the_file_lose_no_line_and_read_back_in_time_order(tmp_path):
    """Operator amendment amend1014-luna-mission-fixes B.2: rotation is exclusive across
    processes, a writer follows a file another process rotated, and the reader orders by time."""
    import subprocess
    import sys

    from packages.orchestration.structured_log import LOG_FILE_NAME, logs_dir, read_log_entries

    path = logs_dir(tmp_path) / LOG_FILE_NAME
    repo = str(pathlib.Path(__file__).resolve().parents[2])
    jobs = [f"job{index}{'0' * 12}" for index in range(4)]
    writers = [subprocess.Popen([sys.executable, "-c", _WRITER, str(path), job, repo])
               for job in jobs]
    assert [writer.wait(timeout=120) for writer in writers] == [0, 0, 0, 0]

    seen: list[tuple[str, str]] = []
    for file in path.parent.glob(LOG_FILE_NAME + "*"):
        if file.name.endswith(".lock"):
            continue
        for line in file.read_text(encoding="utf-8").splitlines():
            entry = json.loads(line)
            seen.append((entry["job_id"], entry["message"]))
    expected = {(job, f"line {n} of {job}") for job in jobs for n in range(400)}
    assert len(seen) == len(expected) == 1600
    assert set(seen) == expected

    entries = read_log_entries(job_id=jobs[0], root=tmp_path).entries
    assert len(entries) == 400
    stamps = [entry["ts"] for entry in entries]
    assert stamps == sorted(stamps)
