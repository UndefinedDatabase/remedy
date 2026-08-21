"""F009 T002 — `secure_fs.append_line_at`, the append-only line writer.

An audit log only ever grows, so it cannot be written by the whole-file publisher every
other Remedy writer uses. These tests hold the append half to the promises the audit record
depends on: one call is one record, a record lands intact even when several threads append
at once, the file is private from the moment it exists, and a name that is not a plain file
under the held directory is refused rather than followed.
"""
from __future__ import annotations

import os
import stat as _stat
import threading
from pathlib import Path

import pytest

from packages.common.secure_fs import (
    MAX_APPEND_LINE_BYTES,
    SecureFsError,
    append_line_at,
)

LOG = "attempts.jsonl"


@pytest.fixture
def dir_fd(tmp_path: Path):
    """A held descriptor for a directory of our own — the only way in, as in production."""
    fd = os.open(tmp_path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        yield fd
    finally:
        os.close(fd)


def test_two_records_are_appended_in_order(tmp_path: Path, dir_fd: int) -> None:
    append_line_at(dir_fd, LOG, b'{"n": 1}\n')
    append_line_at(dir_fd, LOG, b'{"n": 2}\n')

    assert (tmp_path / LOG).read_bytes() == b'{"n": 1}\n{"n": 2}\n'


def test_the_file_is_created_at_the_requested_mode(tmp_path: Path, dir_fd: int) -> None:
    append_line_at(dir_fd, LOG, b"first\n", file_mode=0o600)

    mode = _stat.S_IMODE((tmp_path / LOG).stat().st_mode)
    assert mode == 0o600, f"expected a private 0o600 record, got {oct(mode)}"


def test_a_line_without_a_trailing_newline_is_refused(tmp_path: Path, dir_fd: int) -> None:
    with pytest.raises(SecureFsError, match="must end in a newline"):
        append_line_at(dir_fd, LOG, b"no newline here")

    assert not (tmp_path / LOG).exists(), "a refused line must not create the file"


def test_an_interior_newline_is_refused(tmp_path: Path, dir_fd: int) -> None:
    with pytest.raises(SecureFsError, match="interior newline"):
        append_line_at(dir_fd, LOG, b"one\ntwo\n")

    assert not (tmp_path / LOG).exists()


def test_a_trailing_double_newline_is_refused(tmp_path: Path, dir_fd: int) -> None:
    """`b"x\\n\\n"` ends in a newline and is still two lines; the interior rule catches it."""
    with pytest.raises(SecureFsError, match="interior newline"):
        append_line_at(dir_fd, LOG, b"x\n\n")


def test_an_oversize_line_is_refused(tmp_path: Path, dir_fd: int) -> None:
    oversize = b"x" * MAX_APPEND_LINE_BYTES + b"\n"

    with pytest.raises(SecureFsError, match="over the .* limit for one record"):
        append_line_at(dir_fd, LOG, oversize)

    assert not (tmp_path / LOG).exists()


def test_a_line_at_exactly_the_limit_is_accepted(tmp_path: Path, dir_fd: int) -> None:
    at_limit = b"x" * (MAX_APPEND_LINE_BYTES - 1) + b"\n"

    append_line_at(dir_fd, LOG, at_limit)

    assert (tmp_path / LOG).read_bytes() == at_limit


def test_a_symlink_at_the_name_is_refused_not_followed(tmp_path: Path, dir_fd: int) -> None:
    outside = tmp_path / "outside.txt"
    outside.write_bytes(b"untouched\n")
    os.symlink(outside, tmp_path / LOG)

    with pytest.raises(SecureFsError, match="could not be opened for append"):
        append_line_at(dir_fd, LOG, b"redirected\n")

    assert outside.read_bytes() == b"untouched\n", "the symlink's target was written through"


def test_a_name_that_is_not_a_single_component_is_refused(dir_fd: int) -> None:
    with pytest.raises(SecureFsError, match="not a single component"):
        append_line_at(dir_fd, "../escaped.jsonl", b"out\n")


def test_a_non_bytes_line_is_refused(dir_fd: int) -> None:
    with pytest.raises(SecureFsError, match="must be bytes"):
        append_line_at(dir_fd, LOG, "a str is not a record\n")  # type: ignore[arg-type]


def test_concurrent_appenders_each_land_exactly_one_intact_line(
        tmp_path: Path, dir_fd: int) -> None:
    """The single `os.write` under O_APPEND is what makes this hold; a retry loop would not.

    Each thread writes a distinct, non-trivially-long record. Every record must appear
    exactly once, whole, on a line of its own — no interleaving, no loss, no duplication.
    """
    threads_count = 12
    per_thread = 8
    filler = "y" * 512
    expected = {
        f'{{"t": {t}, "i": {i}, "pad": "{filler}"}}\n'.encode()
        for t in range(threads_count)
        for i in range(per_thread)
    }
    start = threading.Barrier(threads_count)
    errors: list[BaseException] = []

    def appender(t: int) -> None:
        try:
            start.wait(timeout=10)
            for i in range(per_thread):
                append_line_at(dir_fd, LOG, f'{{"t": {t}, "i": {i}, "pad": "{filler}"}}\n'
                               .encode())
        except BaseException as exc:                     # noqa: BLE001 — reported, not hidden
            errors.append(exc)

    threads = [threading.Thread(target=appender, args=(t,)) for t in range(threads_count)]
    for th in threads:
        th.start()
    for th in threads:
        th.join(timeout=30)

    assert errors == [], f"appenders raised: {errors!r}"
    assert all(not th.is_alive() for th in threads), "an appender did not finish"

    written = (tmp_path / LOG).read_bytes()
    lines = written.splitlines(keepends=True)
    assert len(lines) == threads_count * per_thread, (
        f"expected {threads_count * per_thread} lines, got {len(lines)}")
    assert set(lines) == expected, "a record was lost, duplicated or interleaved"
