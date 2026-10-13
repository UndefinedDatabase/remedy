"""F203 T001 — the structured log setup: lines, context ids, redaction, rotation, reset."""

from __future__ import annotations

import json
import logging
import os
import pathlib
import re
import stat

import pytest

from packages.orchestration.config import load_config
from packages.orchestration.structured_log import (
    DEFAULT_LOG_BACKUP_COUNT,
    DEFAULT_LOG_LEVEL,
    DEFAULT_LOG_MAX_BYTES,
    FILE_ONLY_ATTR,
    LOG_CONTEXT_KEYS,
    LOG_FIELD_NAMES,
    LOG_FILE_NAME,
    bind_log_context,
    configure_structured_logging,
    current_log_context,
    logs_dir,
    reset_structured_logging,
)

CHILD = logging.getLogger("packages.orchestration.fixture")
TS_SHAPE = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$")
SECRET_PARTS = (
    "sk-ant-api03-AbCdEfGhIjKlMnOpQrStUvWxYz0123456789",
    "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
)


@pytest.fixture(autouse=True)
def _clean_logging(monkeypatch):
    for name in (
        "REMEDY_LOG_LEVEL", "REMEDY_LOG_JSON", "REMEDY_LOG_MAX_BYTES", "REMEDY_LOG_BACKUP_COUNT",
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
    _, path = _setup(tmp_path, f"json = {'true' if as_json else 'false'}\n")
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
    _, path = _setup(tmp_path, "json = false\n")
    with bind_log_context(job_id="j1"):
        CHILD.info("plain words")
    line = _lines(path)[0]
    assert re.match(r"^\S+ INFO packages\.orchestration\.fixture job=j1 task=- run=- plain words$", line)


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
    assert names == [LOG_FILE_NAME, LOG_FILE_NAME + ".1", LOG_FILE_NAME + ".2"]
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


def test_reset_removes_its_handlers_keeps_foreign_ones_and_restores_the_level(tmp_path):
    root_logger = logging.getLogger()
    foreign = logging.NullHandler()
    root_logger.addHandler(foreign)
    before = root_logger.level
    try:
        _setup(tmp_path, 'level = "DEBUG"\n')
        assert root_logger.level == logging.DEBUG
        reset_structured_logging()
        assert not [h for h in root_logger.handlers if getattr(h, "_remedy_structured_log", False)]
        assert foreign in root_logger.handlers
        assert root_logger.level == before
    finally:
        root_logger.removeHandler(foreign)


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
    assert config.get("logging.json") is True
    assert config.get("logging.max_bytes") == 10000000 == DEFAULT_LOG_MAX_BYTES
    assert config.get("logging.backup_count") == 5 == DEFAULT_LOG_BACKUP_COUNT
