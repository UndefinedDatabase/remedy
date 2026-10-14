"""F203 — Remedy's operations log: one setup, one JSON line per record, the job, task and run ids on every line.

DECISION F203 D1: Remedy writes its own log under `<data root>/logs/`. The log is operations
data and never evidence. Every line is redacted like evidence before it is written, and the
terminal keeps showing warnings and errors exactly as before: the error stream handler this
setup installs prints the bare message at WARNING and above.

The folder and the file are made by the first line written, so a command that logs nothing
writes nothing, and a line that cannot be written is dropped silently (DECISION F203 D2).
"""

from __future__ import annotations

import contextlib
import fcntl
import json
import logging
import logging.handlers
import os
import sys
from collections.abc import Iterator
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import IO, Any

from packages.orchestration.config import RemedyConfig, get_config
from packages.orchestration.data_paths import data_class_dir
from packages.orchestration.stream_evidence import redact_text

# The one file name of the operations log inside its folder.
LOG_FILE_NAME = "remedy.log"

# The keys of every JSON line, in order; the text line carries the same fields.
LOG_FIELD_NAMES: tuple[str, ...] = (
    "ts", "level", "logger", "message", "job_id", "task_id", "run_id",
)

# The three ids a record carries so one night's work can be looked up by job, task or run.
LOG_CONTEXT_KEYS: tuple[str, ...] = ("job_id", "task_id", "run_id")

# The level used when `logging.level` is missing or names nothing known.
DEFAULT_LOG_LEVEL = "INFO"

# The rotation size used when `logging.max_bytes` does not read as an integer.
DEFAULT_LOG_MAX_BYTES = 10_000_000

# The rotated files kept when `logging.backup_count` does not read as an integer.
DEFAULT_LOG_BACKUP_COUNT = 5

_KNOWN_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

# The marker on every handler this module installs, so a reset removes only its own.
_MARKER = "_remedy_structured_log"

# The job id bound for the code running now, None outside any binding.
remedy_log_job_id: ContextVar[str | None] = ContextVar("remedy_log_job_id", default=None)

# The task id bound for the code running now, None outside any binding.
remedy_log_task_id: ContextVar[str | None] = ContextVar("remedy_log_task_id", default=None)

# The run id bound for the code running now, None outside any binding.
remedy_log_run_id: ContextVar[str | None] = ContextVar("remedy_log_run_id", default=None)

_CONTEXT_VARS: dict[str, ContextVar[str | None]] = {
    "job_id": remedy_log_job_id,
    "task_id": remedy_log_task_id,
    "run_id": remedy_log_run_id,
}

# The root logger's level before the first configure since the last reset; None when not saved.
_SAVED_ROOT_LEVEL: list[int] = []


# Binds ids for the code inside the block; an argument left None leaves that id as it was.
@contextlib.contextmanager
def bind_log_context(
    *, job_id: object = None, task_id: object = None, run_id: object = None,
) -> Iterator[None]:
    tokens = []
    try:
        for key, value in (("job_id", job_id), ("task_id", task_id), ("run_id", run_id)):
            if value is not None:
                tokens.append((_CONTEXT_VARS[key], _CONTEXT_VARS[key].set(str(value))))
        yield
    finally:
        for var, token in reversed(tokens):
            var.reset(token)


# The three ids bound now, keyed in the order of `LOG_CONTEXT_KEYS`.
def current_log_context() -> dict[str, str | None]:
    return {key: _CONTEXT_VARS[key].get() for key in LOG_CONTEXT_KEYS}


# Stamps the bound ids on a record; an id the record already carries (`extra=`) wins.
class LogContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        for key in LOG_CONTEXT_KEYS:
            if getattr(record, key, None) is None:
                setattr(record, key, _CONTEXT_VARS[key].get())
        return True


# The UTC time of a record with millisecond digits, e.g. 2026-10-13T08:05:09.042Z.
def log_timestamp(created: float) -> str:
    moment = datetime.fromtimestamp(created, tz=timezone.utc)
    return moment.strftime("%Y-%m-%dT%H:%M:%S") + f".{moment.microsecond // 1000:03d}Z"


# One JSON object per line; redaction runs on each value before the dump so a line always parses.
class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entry: dict[str, object] = {
            "ts": log_timestamp(record.created),
            "level": record.levelname,
            "logger": record.name,
            "message": redact_text(record.getMessage()),
        }
        for key in LOG_CONTEXT_KEYS:
            entry[key] = getattr(record, key, None)
        if record.exc_info:
            entry["exception"] = redact_text(self.formatException(record.exc_info))
        return json.dumps(entry, ensure_ascii=False)


# One plain line per record for a reader without a JSON tool; redacted like the JSON line.
class TextLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        line = (
            f"{log_timestamp(record.created)} {record.levelname} {record.name} "
            f"job={getattr(record, 'job_id', None) or '-'} "
            f"task={getattr(record, 'task_id', None) or '-'} "
            f"run={getattr(record, 'run_id', None) or '-'} {record.getMessage()}"
        )
        if record.exc_info:
            line += "\n" + self.formatException(record.exc_info)
        return redact_text(line)


# Several processes share the file (the supervisor runs every job as a process of its own), so a
# rotation holds an exclusive lock and re-checks under it, and every write first follows a file
# another process rotated away (operator amendment amend1014-luna-mission-fixes B.2).
class OwnerOnlyRotatingFileHandler(logging.handlers.RotatingFileHandler):
    # The file and every rotated successor are owner-only, like a crash report.
    def _open(self) -> IO[str]:
        Path(self.baseFilename).parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        descriptor = os.open(self.baseFilename, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        return os.fdopen(descriptor, "a", encoding=self.encoding, errors=self.errors)

    # Closes the open stream when the name now points at another file or at none; True if so.
    def _follow_rotation(self) -> bool:
        if self.stream is None:
            return False
        try:
            on_disk = os.stat(self.baseFilename)
        except FileNotFoundError:
            on_disk = None
        held = os.fstat(self.stream.fileno())
        if on_disk is not None and (on_disk.st_dev, on_disk.st_ino) == (held.st_dev, held.st_ino):
            return False
        self.stream.close()
        self.stream = None  # type: ignore[assignment]
        return True

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self._follow_rotation()
        except OSError:
            self.handleError(record)
            return
        super().emit(record)

    # Rolls under an exclusive lock on `<log>.lock`; a file another process already rolled is
    # followed and rolled again only when it is itself still over the size.
    def doRollover(self) -> None:
        Path(self.baseFilename).parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        lock = os.open(self.baseFilename + ".lock", os.O_RDWR | os.O_CREAT, 0o600)
        try:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if self._follow_rotation():
                try:
                    size = os.stat(self.baseFilename).st_size
                except FileNotFoundError:
                    size = 0
                if size < self.maxBytes:
                    return
            super().doRollover()
        finally:
            os.close(lock)

    # A line that cannot be written never reaches the terminal and never breaks a command.
    def handleError(self, record: logging.LogRecord) -> None:
        return None


# The record attribute that keeps a record off the terminal; the file still gets it.
FILE_ONLY_ATTR = "remedy_file_only"


# Lets a record through to the terminal unless it carries the file-only attribute.
class TerminalFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return not getattr(record, FILE_ONLY_ATTR, False)


# The one folder the operations log lives in; the class name is a literal so the class registry test finds it.
def logs_dir(root: Path | None = None) -> Path:
    return data_class_dir("logs", root)


def _int_or_default(value: object, default: int) -> int:
    try:
        return int(value)  # type: ignore[call-overload]
    except (ValueError, TypeError):
        return default


# Installs the error-stream handler and the rotating file handler on the root logger; answers the file's path.
def configure_structured_logging(
    root: Path | None = None, config: RemedyConfig | None = None,
) -> Path:
    reset_structured_logging()
    resolved = config if config is not None else get_config()
    name = str(resolved.get("logging.level") or DEFAULT_LOG_LEVEL).upper()
    unknown_name: str | None = None
    if name not in _KNOWN_LEVELS:
        unknown_name = str(resolved.get("logging.level"))
        name = DEFAULT_LOG_LEVEL
    level = logging.getLevelName(name)
    as_json = bool(resolved.get("logging.json_lines"))
    max_bytes = _int_or_default(resolved.get("logging.max_bytes"), DEFAULT_LOG_MAX_BYTES)
    backup_count = _int_or_default(resolved.get("logging.backup_count"), DEFAULT_LOG_BACKUP_COUNT)

    root_logger = logging.getLogger()
    _SAVED_ROOT_LEVEL.append(root_logger.level)
    _install_stream_handler(root_logger)

    path = logs_dir(root) / LOG_FILE_NAME
    handler = OwnerOnlyRotatingFileHandler(
        path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8", delay=True,
    )
    handler.setLevel(level)
    handler.setFormatter(JsonLogFormatter() if as_json else TextLogFormatter())
    handler.addFilter(LogContextFilter())
    setattr(handler, _MARKER, True)
    root_logger.addHandler(handler)

    root_logger.setLevel(min(level, logging.WARNING))
    if unknown_name is not None:
        logging.getLogger(__name__).warning("unknown logging.level %r; INFO is used", unknown_name)
    return path


# The terminal's handler: the bare message at WARNING and above, file-only records left out.
def _install_stream_handler(root_logger: logging.Logger) -> None:
    stream = logging.StreamHandler(sys.stderr)
    stream.setLevel(logging.WARNING)
    stream.setFormatter(logging.Formatter("%(message)s"))
    stream.addFilter(TerminalFilter())
    setattr(stream, _MARKER, True)
    root_logger.addHandler(stream)


# The terminal handler alone, with no configuration read: what a command gets when the
# configuration itself cannot be read (operator amendment amend1014-luna-mission-fixes B.1).
def configure_stream_logging_only() -> None:
    reset_structured_logging()
    root_logger = logging.getLogger()
    _SAVED_ROOT_LEVEL.append(root_logger.level)
    _install_stream_handler(root_logger)


# Removes and closes every handler this module installed and restores the root level it found.
def reset_structured_logging() -> None:
    root_logger = logging.getLogger()
    for handler in list(root_logger.handlers):
        if getattr(handler, _MARKER, False):
            root_logger.removeHandler(handler)
            handler.close()
    if _SAVED_ROOT_LEVEL:
        root_logger.setLevel(_SAVED_ROOT_LEVEL[0])
        _SAVED_ROOT_LEVEL.clear()


# The log files of the folder, oldest first: `remedy.log.<n>` by descending n, then `remedy.log`.
def log_files_oldest_first(root: Path | None = None) -> list[Path]:
    folder = logs_dir(root)
    if not folder.is_dir():
        return []
    prefix = LOG_FILE_NAME + "."
    rotated: list[tuple[int, Path]] = []
    for path in folder.iterdir():
        suffix = path.name[len(prefix):]
        if path.name.startswith(prefix) and suffix.isascii() and suffix.isdigit():
            rotated.append((int(suffix), path))
    files = [path for _, path in sorted(rotated, key=lambda pair: pair[0], reverse=True)]
    current = folder / LOG_FILE_NAME
    if current.is_file():
        files.append(current)
    return files


# What a read of the log answers: the matching lines, the lines that were not JSON, the files read.
@dataclass(frozen=True)
class LogReadResult:
    entries: tuple[dict[str, Any], ...]
    unreadable: int
    files: tuple[str, ...]


# Reads the lines of one job (by id prefix), optionally of one run, ordered by their time.
def read_log_entries(
    *, job_id: str, run_id: str | None = None, root: Path | None = None,
) -> LogReadResult:
    entries: list[dict[str, Any]] = []
    unreadable = 0
    names: list[str] = []
    for path in log_files_oldest_first(root):
        try:
            with path.open(encoding="utf-8", errors="replace") as handle:
                lines = handle.readlines()
        except OSError:
            continue
        names.append(path.name)
        for line in lines:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except ValueError:
                unreadable += 1
                continue
            if not isinstance(entry, dict):
                unreadable += 1
                continue
            found = entry.get("job_id")
            if not job_id or not isinstance(found, str) or not found.startswith(job_id):
                continue
            if run_id is not None and entry.get("run_id") != run_id:
                continue
            entries.append(entry)
    # Several processes write the file, so file order is not time order; a stable sort makes it.
    entries.sort(key=lambda entry: str(entry.get("ts") or ""))
    return LogReadResult(entries=tuple(entries), unreadable=unreadable, files=tuple(names))
